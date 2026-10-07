# edu_methods_causal.R — quasi-experimental designs for edu-analysis (source after edu_methods.R).
# edu_psm (MatchIt + cobalt + sandwich), edu_did (sandwich), edu_did_event (fixest), edu_rdd (rdrobust).
# Same return convention as edu_methods.R: a named list of data frames plus `notes`, ready for edu_save().

edu_01 <- function(x, name) {
  if (is.logical(x)) return(as.integer(x))
  v <- suppressWarnings(as.numeric(as.character(x)))
  if (!anyNA(v[!is.na(x)]) && all(v %in% c(0, 1, NA))) return(v)
  stop(name, " must be coded 0/1 (or TRUE/FALSE).")
}

edu_ci_row <- function(label, est, se, df = Inf) {
  tt <- est / se; q <- stats::qt(.975, df)
  out <- data.frame(estimate_type = label, estimate = est, SE = se, t = tt,
             p = 2 * stats::pt(-abs(tt), df), ci_low = est - q * se, ci_high = est + q * se)
  if (is.infinite(df)) names(out)[4] <- "z"
  out
}

# ---------------------------------------------------------------- propensity score matching
edu_psm <- function(d, treat, covariates, outcome, method = "nearest", distance = "glm", link = "linear.logit",
                    caliper = 0.2, ratio = 1, replace = FALSE, estimand = "ATT", doubly_robust = TRUE, ...) {
  edu_need(c("MatchIt", "cobalt", "sandwich"))
  if (method %in% c("full", "optimal")) edu_need("optmatch")
  vars <- c(treat, covariates, outcome)
  dd <- d[stats::complete.cases(d[vars]), vars, drop = FALSE]
  dd[[treat]] <- edu_01(dd[[treat]], "treat"); dd[[outcome]] <- as.numeric(dd[[outcome]])
  f <- stats::reformulate(covariates, treat)
  args <- list(formula = f, data = dd, method = method, distance = distance, estimand = estimand, ...)
  if (distance == "glm") args$link <- link
  if (method %in% c("nearest", "optimal")) { args$ratio <- ratio }
  if (method == "nearest") args$replace <- replace
  if (!is.null(caliper) && method %in% c("nearest", "full")) { args$caliper <- caliper; args$std.caliper <- TRUE }
  m <- do.call(MatchIt::matchit, args)
  b <- cobalt::bal.tab(m, un = TRUE, stats = c("mean.diffs", "variance.ratios"), binary = "std")$Balance
  bal <- data.frame(variable = rownames(b), type = b$Type, smd_before = b$Diff.Un, var_ratio_before = b$V.Ratio.Un,
                    smd_after = b$Diff.Adj, var_ratio_after = b$V.Ratio.Adj, row.names = NULL)
  bal$smd_ok <- ifelse(bal$type == "Distance", NA, ifelse(abs(bal$smd_after) < 0.1, "yes", "no"))
  bal$vr_ok <- ifelse(is.na(bal$var_ratio_after) | bal$type == "Distance", NA,
                      ifelse(bal$var_ratio_after > 0.5 & bal$var_ratio_after < 2, "yes", "no"))
  nn <- summary(m)$nn
  sizes <- data.frame(sample = rownames(nn), control = nn[, "Control"], treated = nn[, "Treated"], row.names = NULL)
  # effect: weighted regression on the matched data, cluster-robust SE by pair/subclass
  md <- MatchIt::match_data(m, data = dd)
  clus <- if ("subclass" %in% names(md) && !anyNA(md$subclass)) md$subclass else NULL
  vc <- function(fit) if (is.null(clus)) sandwich::vcovHC(fit, type = "HC1") else sandwich::vcovCL(fit, cluster = clus, type = "HC1")
  fit_row <- function(rhs, label, data, w = NULL, v = TRUE) {
    fit <- stats::lm(stats::reformulate(rhs, outcome), data = data, weights = w)
    V <- if (v) vc(fit) else sandwich::vcovHC(fit, type = "HC1")
    edu_ci_row(label, unname(stats::coef(fit)[treat]), sqrt(V[treat, treat]))
  }
  eff <- rbind(fit_row(treat, "unmatched difference (naive)", dd, v = FALSE),
               fit_row(treat, paste0(estimand, ", matched (weighted)"), md, md$weights))
  if (doubly_robust) eff <- rbind(eff, fit_row(c(treat, covariates), paste0(estimand, ", matched + covariate adjustment"), md, md$weights))
  eff <- cbind(eff, n = c(nrow(dd), nrow(md), if (doubly_robust) nrow(md)))
  dropped_t <- sum(dd[[treat]] == 1) - sum(md[[treat]] == 1)
  bad <- bal$variable[!is.na(bal$smd_ok) & bal$smd_ok == "no"]
  list(balance = bal, sample_sizes = sizes, effects = eff,
       notes = c(sprintf("n = %d complete cases; matchit(method = '%s', distance = '%s'%s%s, estimand = '%s').", nrow(dd), method, distance,
                         if (distance == "glm") paste0(", link = '", link, "'") else "",
                         if (!is.null(caliper) && method %in% c("nearest", "full")) sprintf(", caliper = %.2f SD of the distance", caliper) else "", estimand),
                 "Balance (cobalt): SMD uses the treated-group SD for ATT (pooled SD for ATE), binary variables standardized too; |SMD| < 0.1 is the usual criterion (Austin, 2009), variance ratios between 0.5 and 2 (Rubin, 2001).",
                 if (length(bad)) paste0("Not balanced after matching (|SMD| >= 0.1): ", paste(bad, collapse = ", "), ". Re-specify the propensity model or the matching method before estimating effects.") else "All covariates have |SMD| < 0.1 after matching.",
                 if (dropped_t > 0) sprintf("%d treated units were dropped by the caliper/common support: the estimate refers to the matched treated units, not all treated units.", dropped_t),
                 sprintf("Effect = coefficient of %s in a weighted regression on the matched data; SE %s; 95%% CI uses the normal approximation.", treat,
                         if (is.null(clus)) "HC1 robust (no pair/subclass membership to cluster on)" else "cluster-robust by matched pair/subclass (HC1)"),
                 "The covariate-adjusted row adds the matching covariates to the outcome regression (doubly robust in the sense of Ho et al., 2007).",
                 "Matching only removes bias from the observed covariates. It does not address unobserved confounding: state this limitation and, where possible, add a sensitivity analysis (Rosenbaum bounds or the E-value)."))
}

# ---------------------------------------------------------------- difference-in-differences
edu_did <- function(d, outcome, treat, post, cluster = NULL, covariates = NULL) {
  edu_need("sandwich")
  vars <- c(outcome, treat, post, cluster, covariates)
  dd <- d[stats::complete.cases(d[vars]), vars, drop = FALSE]
  dd[[treat]] <- edu_01(dd[[treat]], "treat"); dd[[post]] <- edu_01(dd[[post]], "post")
  dd[[outcome]] <- as.numeric(dd[[outcome]])
  cells <- do.call(rbind, lapply(c(0, 1), function(g) do.call(rbind, lapply(c(0, 1), function(t) {
    y <- dd[[outcome]][dd[[treat]] == g & dd[[post]] == t]
    data.frame(group = if (g == 1) "treated" else "control", period = if (t == 1) "post" else "pre",
               n = length(y), mean = mean(y), sd = stats::sd(y))
  }))))
  mu <- function(g, t) cells$mean[cells$group == g & cells$period == t]
  did4 <- (mu("treated", "post") - mu("treated", "pre")) - (mu("control", "post") - mu("control", "pre"))
  dd$.did <- dd[[treat]] * dd[[post]]
  fit <- stats::lm(stats::reformulate(c(treat, post, ".did", covariates), outcome), dd)
  if (is.null(cluster)) { V <- sandwich::vcovHC(fit, type = "HC1"); df <- fit$df.residual; G <- NA }
  else { G <- length(unique(dd[[cluster]])); V <- sandwich::vcovCL(fit, cluster = dd[[cluster]], type = "HC1"); df <- G - 1 }
  est <- edu_ci_row(if (length(covariates)) "DID, regression with covariates" else "DID, regression", unname(stats::coef(fit)[".did"]), sqrt(V[".did", ".did"]), df)
  est$df <- df
  list(cell_means = cells,
       did = cbind(data.frame(four_mean_did = did4), est),
       notes = c(sprintf("n = %d rows%s. Four-mean DID = (treated post - treated pre) - (control post - control pre); without covariates it equals the regression estimate.",
                         nrow(dd), if (!is.null(cluster)) sprintf(", %d clusters (%s)", G, cluster) else ""),
                 if (is.null(cluster)) "SE: HC1 robust. Repeated observations of the same units or classes need cluster = the unit (or the level at which treatment was assigned)."
                 else sprintf("SE clustered by %s (HC1), t with G - 1 = %d df.%s", cluster, df, if (G < 30) " Fewer than about 30 clusters: cluster-robust SE are unreliable; use a wild cluster bootstrap (fwildclusterboot) or report the limitation." else ""),
                 "Identification rests on parallel trends: without the treatment, the two groups would have changed by the same amount. Two periods cannot test this; show pre-period trends (edu_did_event) when more periods exist.",
                 if (length(covariates)) "Time-varying covariates affected by the treatment should not be adjusted for (bad controls)."))
}

edu_did_event <- function(d, outcome, unit, time, treat_time = NULL, rel_time = NULL, covariates = NULL,
                          cluster = unit, ref = -1, window = NULL, sunab = TRUE) {
  edu_need("fixest")
  if (is.null(treat_time) == is.null(rel_time)) stop("Give either treat_time (first treated period) or rel_time (period minus first treated period).")
  vars <- c(outcome, unit, time, covariates, unique(cluster))
  dd <- d[stats::complete.cases(d[vars]), , drop = FALSE]
  tm <- as.numeric(dd[[time]])
  g <- if (!is.null(treat_time)) suppressWarnings(as.numeric(dd[[treat_time]])) else tm - suppressWarnings(as.numeric(dd[[rel_time]]))
  never <- is.na(g) | is.infinite(g) | (g == 0 & !(0 %in% tm))
  dd$.y <- as.numeric(dd[[outcome]]); dd$.t <- tm
  dd$.rel <- ifelse(never, -1000, tm - g)
  dd$.cohort <- ifelse(never, max(tm) + 1000, g)
  cohorts <- sort(unique(g[!never])); staggered <- length(cohorts) > 1
  if (!any(never) && !staggered) stop("All units are treated at the same time and there is no never-treated group: the event-study effects are not identified.")
  cv <- if (length(covariates)) paste0(" + ", paste(covariates, collapse = " + ")) else ""
  fe <- sprintf(" | %s + .t", unit)
  cl <- stats::reformulate(cluster)
  tidy <- function(m, label) {
    ct <- fixest::coeftable(m); ci <- stats::confint(m)
    keep <- grepl("::-?[0-9]+$", rownames(ct))
    out <- data.frame(estimator = label, rel_time = as.numeric(sub(".*::", "", rownames(ct)[keep])),
                      estimate = ct[keep, 1], SE = ct[keep, 2], p = ct[keep, 4],
                      ci_low = ci[keep, 1], ci_high = ci[keep, 2], row.names = NULL)
    out <- rbind(out, data.frame(estimator = label, rel_time = ref, estimate = 0, SE = NA, p = NA, ci_low = NA, ci_high = NA))
    out <- out[order(out$rel_time), ]
    if (!is.null(window)) out <- out[out$rel_time >= window[1] & out$rel_time <= window[2], ]
    out
  }
  pretest <- function(m, label) {
    w <- tryCatch(fixest::wald(m, keep = "::-", print = FALSE), error = function(e) NULL)
    if (!is.list(w) || is.null(w$stat)) return(data.frame(estimator = label, F = NA, df1 = NA, df2 = NA, p = NA))
    data.frame(estimator = label, F = w$stat, df1 = w$df1, df2 = w$df2, p = w$p)
  }
  f1 <- stats::as.formula(sprintf(".y ~ i(.rel, ref = c(%d, -1000))%s%s", ref, cv, fe))
  m1 <- fixest::feols(f1, dd, cluster = cl)
  es <- tidy(m1, "TWFE event study"); pt <- pretest(m1, "TWFE event study"); att <- NULL
  if (sunab && staggered) {
    f2 <- stats::as.formula(sprintf(".y ~ sunab(.cohort, .t, ref.p = %d)%s%s", ref, cv, fe))
    m2 <- fixest::feols(f2, dd, cluster = cl)
    es <- rbind(es, tidy(m2, "Sun & Abraham")); pt <- rbind(pt, pretest(m2, "Sun & Abraham"))
    a <- stats::aggregate(m2, agg = "ATT")
    att <- data.frame(estimator = "Sun & Abraham overall ATT (post periods)", estimate = a[1, 1], SE = a[1, 2],
                      p = a[1, 4], ci_low = a[1, 1] - 1.96 * a[1, 2], ci_high = a[1, 1] + 1.96 * a[1, 2])
  }
  out <- list(event_study = es, pretrend_test = pt)
  if (!is.null(att)) out$overall_att <- att
  out$notes <- c(sprintf("%d rows, %d units, %d periods; %d treated cohort(s)%s; %s never-treated units. Unit and period fixed effects, SE clustered by %s.",
                         nrow(dd), length(unique(dd[[unit]])), length(unique(tm)), length(cohorts),
                         if (length(cohorts)) paste0(" (first treated: ", paste(cohorts, collapse = ", "), ")") else "",
                         length(unique(dd[[unit]][never])), paste(cluster, collapse = " + ")),
                 sprintf("Coefficients are relative to rel_time = %d (fixed at 0). Leads (rel_time < 0) near zero with CIs covering zero are consistent with parallel pre-trends; the joint Wald test of all leads (for Sun & Abraham, all cohort-specific leads) is in pretrend_test.", ref),
                 "Pre-trend tests have low power: a non-significant test does not prove parallel trends (Roth, 2022). Read the size of the leads, not only p.",
                 if (staggered) paste0("Staggered adoption: TWFE event-study coefficients can be contaminated by effects from other periods and cohorts when effects differ across cohorts (Goodman-Bacon, 2021; Sun & Abraham, 2021). Report the Sun & Abraham",
                                       if (sunab) " rows (fixest::sunab, interaction-weighted)" else " estimator", " or Callaway & Sant'Anna (2021, R package did) as the main result."),
                 if (!any(never)) "No never-treated units: the latest-treated cohort serves as the comparison group, and its post-treatment periods cannot be used.")
  out
}

# ---------------------------------------------------------------- regression discontinuity
edu_rdd <- function(d, outcome, running, cutoff = 0, covariates = NULL, adjust = FALSE, cluster = NULL,
                    p = 1, kernel = "triangular", bwselect = "mserd", ...) {
  edu_need("rdrobust")
  dd <- d[stats::complete.cases(d[c(outcome, running, cluster)]), , drop = FALSE]
  x <- as.numeric(dd[[running]]); cl <- if (!is.null(cluster)) dd[[cluster]] else NULL
  rd <- function(y, covs = NULL) rdrobust::rdrobust(y = y, x = x, c = cutoff, covs = covs, cluster = cl,
                                                     p = p, kernel = kernel, bwselect = bwselect, ...)
  row <- function(r, label) data.frame(
    estimate_type = label, estimate = r$coef[1, 1], bias_corrected = r$coef[2, 1], robust_SE = r$se[3, 1], z_robust = r$z[3, 1],
    p_robust = r$pv[3, 1], robust_ci_low = r$ci[3, 1], robust_ci_high = r$ci[3, 2],
    h_left = r$bws[1, 1], h_right = r$bws[1, 2], b_left = r$bws[2, 1], b_right = r$bws[2, 2],
    n_left = r$N[1], n_right = r$N[2], eff_n_left = r$N_h[1], eff_n_right = r$N_h[2])
  r0 <- rd(as.numeric(dd[[outcome]]))
  est <- row(r0, "RD effect")
  if (adjust && length(covariates)) {
    cc <- stats::complete.cases(dd[covariates])
    if (!all(cc)) stop("Covariate adjustment needs complete covariates; drop or impute the missing rows first.")
    est <- rbind(est, row(rd(as.numeric(dd[[outcome]]), as.matrix(edu_num(dd, covariates))), "RD effect, covariate-adjusted"))
  }
  bal <- if (length(covariates)) do.call(rbind, lapply(covariates, function(v) {
    ok <- !is.na(dd[[v]]); r <- rdrobust::rdrobust(y = as.numeric(dd[[v]][ok]), x = x[ok], c = cutoff, cluster = if (!is.null(cl)) cl[ok],
                                                   p = p, kernel = kernel, bwselect = bwselect, ...)
    cbind(data.frame(covariate = v), row(r, "jump at cutoff")[, -1])
  })) else NULL
  # density / manipulation: counts on each side in symmetric windows (binomial test, Cattaneo et al., 2017 style)
  h <- r0$bws[1, 1]; w <- h * c(0.1, 0.25, 0.5, 1)
  dens <- do.call(rbind, lapply(w, function(wi) {
    nl <- sum(x >= cutoff - wi & x < cutoff); nr <- sum(x >= cutoff & x < cutoff + wi)
    data.frame(window = sprintf("[c - %.3g, c + %.3g)", wi, wi), half_width = wi, n_left = nl, n_right = nr,
               share_right = if (nl + nr) nr / (nl + nr) else NA,
               p = if (nl + nr) stats::binom.test(nr, nl + nr, 0.5)$p.value else NA)
  }))
  brk <- cutoff + seq(-h, h, length.out = 21)
  bins <- as.data.frame(table(cut(x[x >= cutoff - h & x < cutoff + h], brk, right = FALSE)))
  names(bins) <- c("bin", "count")
  out <- list(estimate = est)
  if (!is.null(bal)) out$covariate_balance <- bal
  out$density_windows <- dens; out$density_bins <- bins
  out$notes <- c(sprintf("Sharp RD at %s = %g; %d observations (left %d, right %d). Units with %s >= cutoff are on the right (treated) side.",
                         running, cutoff, length(x), r0$N[1], r0$N[2], running),
                 sprintf("rdrobust: local polynomial p = %d, %s kernel, %s bandwidth (h = %.3f left, %.3f right). 'estimate' is the conventional point estimate; inference uses the robust bias-corrected SE and CI (Calonico, Cattaneo & Titiunik, 2014), so the CI is not centered on the point estimate.",
                         p, kernel, bwselect, r0$bws[1, 1], r0$bws[1, 2]),
                 "The effect is local: it applies to units near the cutoff, not to the whole sample.",
                 if (!is.null(bal)) "Covariate balance: each covariate is used as the outcome; robust CIs covering zero are consistent with no sorting on these covariates.",
                 "Density check here is a simple binomial comparison of counts just below vs just above the cutoff (assumes a locally flat density, so the narrow windows matter most). The standard test is rddensity (Cattaneo, Jansson & Ma, 2020), which is not installed; report it when available. Plot density_bins as a histogram.",
                 "Robustness to report: bandwidths of half and double h, p = 2, placebo cutoffs, and dropping units very close to the cutoff (donut).")
  out
}
