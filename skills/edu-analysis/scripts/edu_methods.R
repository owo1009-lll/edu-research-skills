# edu_methods.R — helper functions used by the edu-analysis method cards. The extra method groups
# (edu_methods_latent/causal/models/patterns.R) in the same folder are loaded at the end of this file.
# Base R plus packages loaded only by the function that needs them (psych, lavaan, semTools,
# seminr, QCA, NCA, lme4). Every function returns a list of data frames plus `notes`;
# edu_save() writes each table to output/<name>_<table>.csv and all of them to output/<name>.md.

edu_need <- function(pkgs) {
  miss <- pkgs[!vapply(pkgs, requireNamespace, logical(1), quietly = TRUE)]
  if (length(miss)) stop("Missing R packages: ", paste(miss, collapse = ", "),
                         ". Install them with install.packages(c(", paste0('"', miss, '"', collapse = ", "), ")).")
}

edu_p <- function(p) ifelse(is.na(p), NA, ifelse(p < .001, "< .001", sub("^0", "", sprintf("%.3f", p))))

edu_md <- function(t, digits = 3) {
  pcol <- grepl("^(p|pvalue|p_.*|p\\..*)$", names(t), ignore.case = TRUE)
  t[pcol] <- lapply(t[pcol], function(x) if (is.numeric(x)) edu_p(x) else x)  # "< .001", never "0.000"
  t[] <- lapply(t, function(x) {
    if (is.numeric(x)) {
      whole <- all(is.na(x) | abs(x - round(x)) < 1e-9)
      ifelse(is.na(x), "", if (whole) format(round(x), big.mark = "") else formatC(x, digits = digits, format = "f"))
    } else ifelse(is.na(x), "", as.character(x))
  })
  c(paste0("| ", paste(names(t), collapse = " | "), " |"),
    paste0("|", paste(rep("---", ncol(t)), collapse = "|"), "|"),
    apply(t, 1, function(r) paste0("| ", paste(r, collapse = " | "), " |")))
}

edu_save <- function(res, name, dir = "output") {
  dir.create(dir, showWarnings = FALSE, recursive = TRUE)
  md <- c(paste0("# ", name), "")
  for (k in names(res)) {
    if (!is.data.frame(res[[k]])) next
    utils::write.csv(res[[k]], file.path(dir, paste0(name, "_", k, ".csv")), row.names = FALSE,
                     fileEncoding = "UTF-8", na = "")
    md <- c(md, paste0("## ", k), "", edu_md(res[[k]]), "")
  }
  if (length(res$notes)) md <- c(md, "## notes", "", paste0("- ", res$notes), "")
  writeLines(enc2utf8(md), file.path(dir, paste0(name, ".md")), useBytes = TRUE)
  invisible(res)
}

edu_num <- function(d, vars) as.data.frame(lapply(d[vars], function(x) suppressWarnings(as.numeric(x))))

# ---------------------------------------------------------------- descriptives and reliability
edu_describe <- function(d, vars) {
  rows <- lapply(vars, function(v) {
    x <- suppressWarnings(as.numeric(d[[v]])); y <- x[!is.na(x)]; m <- mean(y); s <- stats::sd(y); z <- (y - m) / s
    data.frame(variable = v, n = length(y), missing = sum(is.na(x)), mean = m, sd = s, median = stats::median(y),
               min = min(y), max = max(y), skewness = mean(z^3), kurtosis = mean(z^4) - 3)
  })
  list(descriptives = do.call(rbind, rows), notes = "Skewness and excess kurtosis are moment estimates.")
}

edu_reliability <- function(d, scales) {
  edu_need("psych")
  rows <- lapply(names(scales), function(s) {
    x <- edu_num(d, scales[[s]])
    a <- suppressWarnings(psych::alpha(x, warnings = FALSE))
    om <- tryCatch(suppressWarnings(psych::omega(x, nfactors = 1, plot = FALSE))$omega.tot, error = function(e) NA_real_)
    data.frame(scale = s, items = ncol(x), n_complete = sum(stats::complete.cases(x)), alpha = a$total$raw_alpha,
               omega_total = om, min_corrected_item_total = min(a$item.stats$r.drop))
  })
  list(reliability = do.call(rbind, rows),
       notes = "alpha = Cronbach's alpha (raw); omega_total from a one-factor model (psych::omega).")
}

edu_harman <- function(d, items) {
  x <- edu_num(d, items)
  ev <- eigen(stats::cor(x, use = "pairwise.complete.obs"), symmetric = TRUE, only.values = TRUE)$values
  first <- ev[1] / length(ev)
  list(harman = data.frame(items = length(ev), eigenvalues_above_1 = sum(ev > 1),
                           first_factor_variance_pct = 100 * first),
       notes = c("Harman's single-factor test: share of total variance carried by the first unrotated component.",
                 "A first component below 40% (some journals use 50%) is the conventional report; it is a weak check, so pair it with a marker variable or a single-factor CFA when common method bias matters."))
}

# ---------------------------------------------------------------- group differences
edu_rb_paired <- function(diff) {
  diff <- diff[diff != 0]; r <- rank(abs(diff))
  (sum(r[diff > 0]) - sum(r[diff < 0])) / sum(r)
}

edu_brown_forsythe <- function(x, g) {
  dev <- abs(x - stats::ave(x, g, FUN = stats::median))
  s <- summary(stats::aov(dev ~ g))[[1]]
  c(F = s$`F value`[1], p = s$`Pr(>F)`[1])
}

edu_compare <- function(d, y, group, paired = FALSE, id = NULL) {
  x <- suppressWarnings(as.numeric(d[[y]])); g <- factor(d[[group]])
  keep <- !is.na(x) & !is.na(g); x <- x[keep]; g <- droplevels(g[keep]); k <- nlevels(g)
  desc <- do.call(rbind, lapply(levels(g), function(l) {
    v <- x[g == l]; data.frame(group = l, n = length(v), mean = mean(v), sd = stats::sd(v), median = stats::median(v))
  }))
  notes <- character(); posthoc <- NULL
  if (paired) {
    if (k != 2 || is.null(id)) stop("Paired comparison needs exactly two conditions and an id column")
    ids <- d[[id]][keep]; l1 <- levels(g)[1]; l2 <- levels(g)[2]
    w <- merge(data.frame(id = ids[g == l1], a = x[g == l1]), data.frame(id = ids[g == l2], b = x[g == l2]), by = "id")
    diff <- w$b - w$a
    tt <- stats::t.test(w$b, w$a, paired = TRUE)
    wt <- suppressWarnings(stats::wilcox.test(w$b, w$a, paired = TRUE, exact = FALSE))
    tests <- data.frame(test = c("paired t", "Wilcoxon signed-rank"),
                        statistic = c(unname(tt$statistic), unname(wt$statistic)), df = c(unname(tt$parameter), NA),
                        p = c(tt$p.value, wt$p.value), effect = c("Cohen's dz", "rank-biserial r"),
                        effect_size = c(mean(diff) / stats::sd(diff), edu_rb_paired(diff)),
                        mean_diff = c(mean(diff), NA), ci_low = c(tt$conf.int[1], NA), ci_high = c(tt$conf.int[2], NA))
    notes <- c(sprintf("%d complete pairs; differences are %s minus %s.", nrow(w), l2, l1))
    if (nrow(w) >= 3 && nrow(w) <= 5000) notes <- c(notes, sprintf("Shapiro-Wilk on differences: p = %s.", edu_p(stats::shapiro.test(diff)$p.value)))
  } else if (k == 2) {
    a <- x[g == levels(g)[1]]; b <- x[g == levels(g)[2]]; n1 <- length(a); n2 <- length(b)
    welch <- stats::t.test(a, b); student <- stats::t.test(a, b, var.equal = TRUE)
    mw <- suppressWarnings(stats::wilcox.test(a, b, exact = FALSE))
    sp <- sqrt(((n1 - 1) * stats::var(a) + (n2 - 1) * stats::var(b)) / (n1 + n2 - 2)); dd <- (mean(a) - mean(b)) / sp
    tests <- data.frame(test = c("Welch t", "Student t", "Mann-Whitney U"),
                        statistic = c(unname(welch$statistic), unname(student$statistic), unname(mw$statistic)),
                        df = c(unname(welch$parameter), unname(student$parameter), NA),
                        p = c(welch$p.value, student$p.value, mw$p.value),
                        effect = c("Hedges' g", "Cohen's d", "rank-biserial r"),
                        effect_size = c(dd * (1 - 3 / (4 * (n1 + n2) - 9)), dd, 2 * unname(mw$statistic) / (n1 * n2) - 1),
                        mean_diff = c(mean(a) - mean(b), mean(a) - mean(b), NA),
                        ci_low = c(welch$conf.int[1], student$conf.int[1], NA), ci_high = c(welch$conf.int[2], student$conf.int[2], NA))
    bf <- edu_brown_forsythe(x, g)
    notes <- c(sprintf("Effect sizes are positive when %s scores higher than %s.", levels(g)[1], levels(g)[2]),
               sprintf("Brown-Forsythe (Levene, median) test of equal variances: F = %.3f, p = %s. Welch t is the default report.", bf[["F"]], edu_p(bf[["p"]])))
  } else {
    fit <- stats::aov(x ~ g); s <- summary(fit)[[1]]
    ssb <- s$`Sum Sq`[1]; ssw <- s$`Sum Sq`[2]; dfb <- s$Df[1]; msw <- s$`Mean Sq`[2]
    welch <- stats::oneway.test(x ~ g); kw <- stats::kruskal.test(x ~ g)
    tests <- data.frame(test = c("one-way ANOVA", "Welch ANOVA", "Kruskal-Wallis"),
                        statistic = c(s$`F value`[1], unname(welch$statistic), unname(kw$statistic)),
                        df = c(sprintf("%d, %d", dfb, s$Df[2]), sprintf("%.0f, %.2f", welch$parameter[1], welch$parameter[2]), as.character(kw$parameter)),
                        p = c(s$`Pr(>F)`[1], welch$p.value, kw$p.value),
                        effect = c("eta squared", "omega squared", "epsilon squared"),
                        effect_size = c(ssb / (ssb + ssw), (ssb - dfb * msw) / (ssb + ssw + msw), unname(kw$statistic) / (length(x) - 1)))
    tk <- stats::TukeyHSD(fit)$g
    pw <- suppressWarnings(stats::pairwise.wilcox.test(x, g, p.adjust.method = "holm", exact = FALSE))$p.value
    posthoc <- data.frame(contrast = rownames(tk), mean_diff = tk[, "diff"], ci_low = tk[, "lwr"], ci_high = tk[, "upr"],
                          p_tukey = tk[, "p adj"], row.names = NULL)
    posthoc$p_wilcoxon_holm <- vapply(strsplit(posthoc$contrast, "-", fixed = TRUE), function(p2) {
      v <- tryCatch(pw[p2[1], p2[2]], error = function(e) NA); if (is.na(v)) v <- tryCatch(pw[p2[2], p2[1]], error = function(e) NA); v
    }, numeric(1))
    bf <- edu_brown_forsythe(x, g)
    notes <- c(sprintf("Brown-Forsythe test of equal variances: F = %.3f, p = %s; report Welch ANOVA when variances differ.", bf[["F"]], edu_p(bf[["p"]])))
  }
  out <- list(descriptives = desc, tests = tests)
  if (!is.null(posthoc)) out$posthoc <- posthoc
  out$notes <- notes
  out
}

# ---------------------------------------------------------------- categorical
edu_chisq <- function(d, x, y, seed = 1, B = 1e5) {
  tab <- table(d[[x]], d[[y]], dnn = c(x, y))
  pear <- suppressWarnings(stats::chisq.test(tab, correct = FALSE)); ex <- pear$expected; N <- sum(tab)
  k <- min(dim(tab)); v <- sqrt(unname(pear$statistic) / (N * (k - 1)))
  tests <- data.frame(test = "Pearson chi-square", statistic = unname(pear$statistic), df = unname(pear$parameter),
                      p = pear$p.value, effect = if (all(dim(tab) == 2)) "phi" else "Cramer's V", effect_size = v)
  if (all(dim(tab) == 2)) {
    yates <- suppressWarnings(stats::chisq.test(tab))
    tests <- rbind(tests, data.frame(test = "Yates-corrected chi-square", statistic = unname(yates$statistic),
                                     df = unname(yates$parameter), p = yates$p.value, effect = NA, effect_size = NA))
  }
  small <- mean(ex < 5)
  if (small > 0.2 || min(ex) < 1) {
    set.seed(seed)
    fe <- if (all(dim(tab) == 2)) stats::fisher.test(tab) else stats::fisher.test(tab, simulate.p.value = TRUE, B = B)
    tests <- rbind(tests, data.frame(test = if (all(dim(tab) == 2)) "Fisher exact" else "Fisher exact (Monte Carlo)",
                                     statistic = NA, df = NA, p = fe$p.value, effect = NA, effect_size = NA))
  }
  counts <- as.data.frame.matrix(tab); counts <- cbind(category = rownames(counts), counts)
  res <- as.data.frame(as.table(pear$stdres)); names(res) <- c(x, y, "adjusted_residual")
  list(counts = counts, tests = tests, residuals = res,
       notes = c(sprintf("N = %d; %.0f%% of expected counts are below 5 (minimum %.2f).", N, 100 * small, min(ex)),
                 "Adjusted standardized residuals beyond +/-1.96 mark cells that differ from independence at about .05."))
}

# ---------------------------------------------------------------- correlation and regression
edu_cor <- function(d, vars, method = "pearson") {
  x <- edu_num(d, vars); pairs <- utils::combn(vars, 2)
  long <- do.call(rbind, lapply(seq_len(ncol(pairs)), function(i) {
    a <- pairs[1, i]; b <- pairs[2, i]; ok <- stats::complete.cases(x[[a]], x[[b]])
    ct <- suppressWarnings(stats::cor.test(x[[a]][ok], x[[b]][ok], method = method, exact = FALSE))
    data.frame(var1 = a, var2 = b, n = sum(ok), r = unname(ct$estimate), p = ct$p.value)
  }))
  star <- function(p) ifelse(p < .001, "***", ifelse(p < .01, "**", ifelse(p < .05, "*", "")))
  mat <- matrix("", length(vars), length(vars), dimnames = list(vars, vars)); diag(mat) <- "1"
  for (i in seq_len(nrow(long))) mat[long$var2[i], long$var1[i]] <- sprintf("%.3f%s", long$r[i], star(long$p[i]))
  list(pairs = long, matrix = cbind(variable = vars, as.data.frame(mat, check.names = FALSE)),
       notes = sprintf("%s correlations, pairwise complete cases; * p < .05, ** p < .01, *** p < .001.", method))
}

edu_vif <- function(fit) {
  X <- stats::model.matrix(fit)[, -1, drop = FALSE]
  if (ncol(X) < 2) return(stats::setNames(rep(1, ncol(X)), colnames(X)))
  vapply(seq_len(ncol(X)), function(j) 1 / (1 - summary(stats::lm(X[, j] ~ X[, -j]))$r.squared), numeric(1)) |>
    stats::setNames(colnames(X))
}

edu_regression <- function(d, y, blocks, family = c("gaussian", "binomial")) {
  family <- match.arg(family); vars <- c(y, unlist(blocks))
  dd <- d[stats::complete.cases(d[vars]), vars, drop = FALSE]
  num <- vapply(dd, function(v) is.numeric(v) || !anyNA(suppressWarnings(as.numeric(v))), logical(1))
  for (v in names(dd)[num]) dd[[v]] <- as.numeric(dd[[v]])
  fits <- list(); models <- list(); coefs <- list()
  for (i in seq_along(blocks)) {
    f <- stats::reformulate(unlist(blocks[seq_len(i)]), response = y)
    if (family == "gaussian") {
      m <- stats::lm(f, dd); s <- summary(m)
      zd <- dd; for (v in intersect(names(zd)[num], all.vars(f))) zd[[v]] <- as.numeric(scale(zd[[v]]))
      beta <- stats::coef(stats::lm(f, zd))
      ci <- stats::confint(m); ct <- s$coefficients
      coefs[[i]] <- data.frame(model = i, term = rownames(ct), B = ct[, 1], SE = ct[, 2], beta = beta[rownames(ct)],
                               t = ct[, 3], p = ct[, 4], ci_low = ci[, 1], ci_high = ci[, 2], row.names = NULL)
      fs <- s$fstatistic
      models[[i]] <- data.frame(model = i, n = nrow(dd), R2 = s$r.squared, adj_R2 = s$adj.r.squared, F = fs[[1]],
                                df1 = fs[[2]], df2 = fs[[3]], p = stats::pf(fs[[1]], fs[[2]], fs[[3]], lower.tail = FALSE))
      if (i > 1) {
        a <- stats::anova(fits[[i - 1]], m)
        models[[i]]$delta_R2 <- s$r.squared - summary(fits[[i - 1]])$r.squared
        models[[i]]$F_change <- a$F[2]; models[[i]]$p_change <- a$`Pr(>F)`[2]
      } else { models[[i]]$delta_R2 <- s$r.squared; models[[i]]$F_change <- fs[[1]]; models[[i]]$p_change <- models[[i]]$p }
    } else {
      m <- stats::glm(f, stats::binomial(), dd); ct <- summary(m)$coefficients
      z <- stats::qnorm(.975)
      coefs[[i]] <- data.frame(model = i, term = rownames(ct), B = ct[, 1], SE = ct[, 2], OR = exp(ct[, 1]),
                               OR_low = exp(ct[, 1] - z * ct[, 2]), OR_high = exp(ct[, 1] + z * ct[, 2]),
                               z = ct[, 3], p = ct[, 4], row.names = NULL)
      n <- nrow(dd); ll0 <- -m$null.deviance / 2; ll1 <- -m$deviance / 2
      cs <- 1 - exp(2 * (ll0 - ll1) / n); nag <- cs / (1 - exp(2 * ll0 / n))
      prev <- if (i > 1) fits[[i - 1]] else stats::glm(stats::reformulate("1", y), stats::binomial(), dd)
      lr <- stats::anova(prev, m, test = "Chisq")
      models[[i]] <- data.frame(model = i, n = n, LR_chi2 = lr$Deviance[2], df = lr$Df[2], p = lr$`Pr(>Chi)`[2],
                                Nagelkerke_R2 = nag, accuracy = mean((stats::fitted(m) > .5) == (m$y == 1)))
    }
    fits[[i]] <- m
  }
  vif <- edu_vif(fits[[length(fits)]])
  list(models = do.call(rbind, models), coefficients = do.call(rbind, coefs),
       vif = data.frame(term = names(vif), VIF = unname(vif)),
       notes = c(sprintf("All models use the same %d complete cases.", nrow(dd)),
                 if (family == "gaussian") "beta = coefficient after standardizing numeric variables (factors stay unstandardized)."
                 else "Logistic: LR chi-square compares each block with the previous model; odds-ratio intervals are Wald 95%."))
}

edu_moderation <- function(d, y, x, w, covariates = NULL, center = TRUE) {
  vars <- c(y, x, w, covariates); dd <- d[stats::complete.cases(d[vars]), vars, drop = FALSE]
  for (v in c(y, x, covariates)) if (!is.factor(dd[[v]])) dd[[v]] <- as.numeric(dd[[v]])
  w_cat <- !is.numeric(suppressWarnings(as.numeric(dd[[w]]))) || anyNA(suppressWarnings(as.numeric(dd[[w]])))
  if (!w_cat) dd[[w]] <- as.numeric(dd[[w]]) else dd[[w]] <- factor(dd[[w]])
  if (center) { dd$.x <- dd[[x]] - mean(dd[[x]]); if (!w_cat) dd$.w <- dd[[w]] - mean(dd[[w]]) else dd$.w <- dd[[w]] }
  else { dd$.x <- dd[[x]]; dd$.w <- dd[[w]] }
  rhs <- c(".x", ".w", covariates)
  m0 <- stats::lm(stats::reformulate(rhs, y), dd); m1 <- stats::lm(stats::reformulate(c(rhs, ".x:.w"), y), dd)
  ct <- summary(m1)$coefficients; V <- stats::vcov(m1); a <- stats::anova(m0, m1)
  if (!w_cat) {
    s <- stats::sd(dd[[w]]); wv <- mean(dd[[w]]) + c(-s, 0, s); lab <- c("-1 SD", "mean", "+1 SD")
    at <- if (center) wv - mean(dd[[w]]) else wv
    slopes <- do.call(rbind, lapply(seq_along(at), function(i) {
      est <- stats::coef(m1)[".x"] + at[i] * stats::coef(m1)[".x:.w"]
      se <- sqrt(V[".x", ".x"] + at[i]^2 * V[".x:.w", ".x:.w"] + 2 * at[i] * V[".x", ".x:.w"])
      df <- m1$df.residual; tt <- est / se
      data.frame(moderator_at = lab[i], moderator_value = wv[i], slope = est, SE = se,
                 t = tt, p = 2 * stats::pt(-abs(tt), df), ci_low = est - stats::qt(.975, df) * se, ci_high = est + stats::qt(.975, df) * se)
    }))
  } else {
    slopes <- do.call(rbind, lapply(levels(dd$.w), function(l) {
      dl <- dd; dl$.w <- stats::relevel(dl$.w, l); ml <- stats::lm(stats::reformulate(c(rhs, ".x:.w"), y), dl)
      cl <- summary(ml)$coefficients[".x", ]; ci <- stats::confint(ml)[".x", ]
      data.frame(moderator_at = l, moderator_value = NA, slope = cl[1], SE = cl[2], t = cl[3], p = cl[4], ci_low = ci[1], ci_high = ci[2])
    }))
  }
  list(coefficients = data.frame(term = rownames(ct), B = ct[, 1], SE = ct[, 2], t = ct[, 3], p = ct[, 4], row.names = NULL),
       interaction = data.frame(delta_R2 = summary(m1)$r.squared - summary(m0)$r.squared, F = a$F[2], df1 = a$Df[2],
                                df2 = m1$df.residual, p = a$`Pr(>F)`[2]),
       simple_slopes = slopes,
       notes = c(sprintf("n = %d; predictors %s mean-centered before forming the product term.", nrow(dd), if (center) "were" else "were not"),
                 "Simple slopes of x at the listed moderator values (Aiken & West)."))
}

edu_mediation <- function(d, y, x, m, covariates = NULL, serial = FALSE, boot = 5000, seed = 123) {
  edu_need("lavaan"); vars <- c(y, x, m, covariates)
  dd <- edu_num(d[stats::complete.cases(d[vars]), , drop = FALSE], vars)
  cv <- if (length(covariates)) paste0(" + ", paste(covariates, collapse = " + ")) else ""
  k <- length(m); lines <- character(); ind <- character()
  for (i in seq_len(k)) {
    prev <- if (serial && i > 1) paste0(" + ", paste0("d", i, seq_len(i - 1), "*", m[seq_len(i - 1)], collapse = " + ")) else ""
    lines <- c(lines, sprintf("%s ~ a%d*%s%s%s", m[i], i, x, prev, cv))
  }
  lines <- c(lines, sprintf("%s ~ c*%s + %s%s", y, x, paste0("b", seq_len(k), "*", m, collapse = " + "), cv))
  for (i in seq_len(k)) ind <- c(ind, sprintf("ind_%s := a%d*b%d", m[i], i, i))
  if (serial && k == 2) ind <- c(ind, "ind_serial := a1*d21*b2")
  if (serial && k > 2) stop("Serial mediation helper supports two mediators; write the lavaan model directly for longer chains.")
  names_ind <- sub(" :=.*", "", ind)
  model <- paste(c(lines, ind, sprintf("total_indirect := %s", paste(names_ind, collapse = " + ")),
                   sprintf("total := c + %s", paste(names_ind, collapse = " + "))), collapse = "\n")
  set.seed(seed)
  fit <- lavaan::sem(model, data = dd, se = if (boot > 0) "bootstrap" else "standard", bootstrap = boot)
  pe <- lavaan::parameterEstimates(fit, boot.ci.type = if (boot > 0) "perc" else "norm", level = .95)
  std <- lavaan::standardizedSolution(fit)
  paths <- pe[pe$op == "~", c("lhs", "rhs", "label", "est", "se", "z", "pvalue", "ci.lower", "ci.upper")]
  sr <- std[std$op == "~", ]; paths$std <- sr$est.std[match(paste(paths$lhs, paths$rhs), paste(sr$lhs, sr$rhs))]
  eff <- pe[pe$op == ":=", c("lhs", "est", "se", "pvalue", "ci.lower", "ci.upper")]
  names(eff)[1] <- "effect"
  eff$share_of_total <- eff$est / eff$est[eff$effect == "total"]
  list(paths = paths, effects = eff, model = data.frame(lavaan_syntax = model),
       notes = c(sprintf("n = %d; %s bootstrap resamples, percentile 95%% CI (seed %d).", nrow(dd), boot, seed),
                 "Indirect effects are products of coefficients; with cross-sectional data they describe statistical mediation, not a demonstrated causal mechanism."))
}

# ---------------------------------------------------------------- measurement and SEM (lavaan)
edu_fit_table <- function(fit) {
  rob <- any(lavaan::lavInspect(fit, "options")$test %in% c("satorra.bentler", "yuan.bentler", "yuan.bentler.mplus", "scaled.shifted", "mean.var.adjusted"))
  f <- lavaan::fitMeasures(fit)
  pick <- function(a, b) if (rob && !is.na(f[b])) unname(f[b]) else unname(f[a])
  data.frame(chisq = pick("chisq", "chisq.scaled"), df = unname(f["df"]), p = pick("pvalue", "pvalue.scaled"),
             chisq_df = pick("chisq", "chisq.scaled") / unname(f["df"]),
             CFI = pick("cfi", "cfi.robust"), TLI = pick("tli", "tli.robust"), RMSEA = pick("rmsea", "rmsea.robust"),
             RMSEA_low = pick("rmsea.ci.lower", "rmsea.ci.lower.robust"), RMSEA_high = pick("rmsea.ci.upper", "rmsea.ci.upper.robust"),
             SRMR = unname(f["srmr"]))
}

edu_missing <- function(d, model, estimator, ordered = NULL) {
  ov <- intersect(lavaan::lavNames(lavaan::lavaanify(model), "ov"), names(d))
  if (anyNA(d[ov]) && is.null(ordered) && estimator %in% c("ML", "MLR")) "fiml" else "listwise"
}

edu_cfa <- function(d, model, estimator = "MLR", ordered = NULL) {
  edu_need("lavaan")
  fit <- lavaan::cfa(model, data = d, estimator = estimator, ordered = ordered,
                     missing = edu_missing(d, model, estimator, ordered))
  std <- lavaan::standardizedSolution(fit)
  load <- std[std$op == "=~", c("lhs", "rhs", "est.std", "se", "pvalue")]; names(load) <- c("factor", "item", "loading", "SE", "p")
  facs <- unique(load$factor)
  conv <- do.call(rbind, lapply(facs, function(f) {
    l <- load$loading[load$factor == f]
    data.frame(factor = f, items = length(l), CR = sum(l)^2 / (sum(l)^2 + sum(1 - l^2)), AVE = mean(l^2))
  }))
  phi <- lavaan::lavInspect(fit, "cor.lv")[facs, facs, drop = FALSE]
  fl <- phi; diag(fl) <- sqrt(conv$AVE)
  fl_tab <- cbind(factor = facs, as.data.frame(fl))
  ht <- if (requireNamespace("semTools", quietly = TRUE)) tryCatch(semTools::htmt(model, data = d), error = function(e) NULL) else NULL
  out <- list(fit = edu_fit_table(fit), loadings = load, convergent = conv, fornell_larcker = fl_tab)
  if (!is.null(ht)) out$htmt <- cbind(factor = rownames(ht), as.data.frame(as.matrix(ht)))
  out$notes <- c(sprintf("Estimator %s; n = %d.", estimator, lavaan::lavInspect(fit, "nobs")),
                 "CR and AVE from standardized loadings (Fornell & Larcker 1981); CR >= .70 and AVE >= .50 are the usual reports.",
                 "Fornell-Larcker: diagonal = sqrt(AVE), off-diagonal = latent correlations. HTMT below .85 (or .90) is the usual discriminant-validity report.",
                 "Cut-offs (CFI/TLI >= .90 or .95, RMSEA <= .08, SRMR <= .08) are conventions, not proof of a correct model.")
  out
}

edu_sem <- function(d, model, estimator = "MLR", boot = 0, seed = 123) {
  edu_need("lavaan"); set.seed(seed)
  # Bootstrap needs ML; it keeps the same missing-data handling (FIML when data are missing) as the main model.
  est <- if (boot > 0) "ML" else estimator
  fit <- if (boot > 0) lavaan::sem(model, data = d, estimator = "ML", missing = edu_missing(d, model, "ML"), se = "bootstrap", bootstrap = boot)
         else lavaan::sem(model, data = d, estimator = estimator, missing = edu_missing(d, model, estimator))
  pe <- lavaan::parameterEstimates(fit, boot.ci.type = if (boot > 0) "perc" else "norm")
  std <- lavaan::standardizedSolution(fit)
  key <- function(x) paste(x$lhs, x$op, x$rhs)
  paths <- pe[pe$op == "~", c("lhs", "rhs", "est", "se", "z", "pvalue", "ci.lower", "ci.upper")]
  sr <- std[std$op == "~", ]; paths$beta <- sr$est.std[match(paste(paths$lhs, paths$rhs), paste(sr$lhs, sr$rhs))]
  r2 <- lavaan::lavInspect(fit, "r2")
  out <- list(fit = edu_fit_table(fit), paths = paths, r2 = data.frame(variable = names(r2), R2 = unname(r2)))
  defined <- pe[pe$op == ":=", c("lhs", "op", "rhs", "est", "se", "pvalue", "ci.lower", "ci.upper")]
  if (nrow(defined)) {
    sd <- std[std$op == ":=", ]
    m <- match(key(defined), key(sd))
    defined$std <- sd$est.std[m]; defined$std_ci_low <- sd$ci.lower[m]; defined$std_ci_high <- sd$ci.upper[m]
    out$defined <- defined[, setdiff(names(defined), c("op", "rhs"))]
  }
  out$notes <- c(sprintf("%s; n = %d (%s).", if (boot > 0) sprintf("ML with %d bootstrap resamples (percentile CI for unstandardized estimates)", boot) else paste("Estimator", est),
                         lavaan::lavInspect(fit, "nobs"), if (lavaan::lavInspect(fit, "options")$missing == "ml") "FIML for missing data" else "listwise"),
                 "Standardized effects (std) carry delta-method 95% CIs; report the bootstrap CI of the unstandardized indirect effect as the significance test.")
  out
}

edu_cmb <- function(d, model, items = NULL, estimator = "MLR") {
  edu_need("lavaan")
  ov <- intersect(lavaan::lavNames(lavaan::lavaanify(model), "ov"), names(d)); if (is.null(items)) items <- ov
  miss <- edu_missing(d, model, estimator)
  trait <- lavaan::cfa(model, data = d, estimator = estimator, missing = miss)
  one <- lavaan::cfa(paste("G =~", paste(items, collapse = " + ")), data = d, estimator = estimator, missing = miss)
  lvs <- lavaan::lavNames(lavaan::lavaanify(model), "lv")
  ulmc <- paste(model, paste("METHOD =~", paste(items, collapse = " + ")),
                paste(sprintf("METHOD ~~ 0*%s", lvs), collapse = "\n"), sep = "\n")
  meth <- tryCatch(lavaan::cfa(ulmc, data = d, estimator = estimator, missing = miss), error = function(e) NULL)
  fits <- rbind(cbind(model = "measurement model", edu_fit_table(trait)), cbind(model = "single factor", edu_fit_table(one)))
  if (!is.null(meth) && lavaan::lavInspect(meth, "converged")) fits <- rbind(fits, cbind(model = "measurement + method factor", edu_fit_table(meth)))
  lrt <- lavaan::lavTestLRT(trait, one)
  harman <- edu_harman(d, items)$harman
  delta <- if (nrow(fits) == 3) fits[3, c("CFI", "TLI", "RMSEA", "SRMR")] - fits[1, c("CFI", "TLI", "RMSEA", "SRMR")] else NULL
  out <- list(harman = harman, model_comparison = fits,
              single_factor_test = data.frame(delta_chisq = lrt$`Chisq diff`[2], delta_df = lrt$`Df diff`[2], p = lrt$`Pr(>Chisq)`[2]))
  if (!is.null(delta)) out$method_factor_change <- cbind(change = "with method factor minus without", delta)
  out$notes <- c("Three checks: Harman single factor (first component < 40%), single-factor CFA fits clearly worse than the measurement model, and adding an unmeasured latent method factor changes CFI/TLI by < .10 and RMSEA/SRMR by < .05 (common rule; stricter reports use .02/.01).",
                 if (is.null(delta)) "The method-factor model did not converge; report the other two checks." else "The method factor is orthogonal to the substantive factors (ULMC).")
  out
}

edu_nca_plot <- function(d, x, y, file = "output/nca_plot.png") {
  # Scatter plot with the CE-FDH ceiling (step function through the upper-left points).
  xv <- as.numeric(d[[x]]); yv <- as.numeric(d[[y]]); ok <- !is.na(xv) & !is.na(yv); xv <- xv[ok]; yv <- yv[ok]
  o <- order(xv); sx <- xv[o]; ceil <- cummax(yv[o])
  dir.create(dirname(file), showWarnings = FALSE, recursive = TRUE)
  grDevices::png(file, width = 1600, height = 1400, res = 300)
  on.exit(grDevices::dev.off())
  graphics::plot(xv, yv, pch = 16, col = grDevices::adjustcolor("grey30", .5), xlab = x, ylab = y, las = 1)
  graphics::lines(c(sx, max(sx)), c(ceil, max(ceil)), type = "s", lwd = 2, col = "#59788E")
  invisible(file)
}

# ---------------------------------------------------------------- PLS-SEM (seminr)
edu_pls <- function(d, measurement, structural, boot = 2000, seed = 123) {
  edu_need("seminr")
  mm <- do.call(seminr::constructs, unname(lapply(names(measurement), function(n) seminr::composite(n, measurement[[n]]))))
  sm <- do.call(seminr::relationships, unname(lapply(seq_len(nrow(structural)), function(i) seminr::paths(from = structural$from[i], to = structural$to[i]))))
  pls <- seminr::estimate_pls(data = d, measurement_model = mm, structural_model = sm)
  s <- summary(pls)
  set.seed(seed); bt <- seminr::bootstrap_model(pls, nboot = boot, cores = 1, seed = seed); sb <- summary(bt)
  rel <- as.data.frame(unclass(s$reliability)); rel <- cbind(construct = rownames(rel), rel)
  ld <- as.data.frame(unclass(s$loadings)); ld <- cbind(item = rownames(ld), ld)
  ht <- as.data.frame(unclass(s$validity$htmt)); ht <- cbind(construct = rownames(ht), ht)
  bp <- as.data.frame(unclass(sb$bootstrapped_paths)); bp <- cbind(path = rownames(bp), bp)
  bp$p_two_tailed <- 2 * stats::pnorm(-abs(bp$`T Stat.`))
  pr <- as.data.frame(unclass(s$paths)); pr <- cbind(row = rownames(pr), pr)
  list(loadings = ld, reliability = rel, htmt = ht, paths = bp, r2_and_paths = pr,
       notes = c(sprintf("PLS-SEM (seminr), %d bootstrap resamples (seed %d); p from the bootstrap t statistic (normal approximation).", boot, seed),
                 "Report loadings >= .708, rhoA/rhoC between .70 and .95, AVE >= .50 and HTMT < .85/.90 as Hair et al. (2022) conventions."))
}

# ---------------------------------------------------------------- fsQCA (QCA package)
edu_calibrate <- function(x, e, c, i) {
  edu_need("QCA")
  QCA::calibrate(as.numeric(x), type = "fuzzy", thresholds = paste0("e=", e, ", c=", c, ", i=", i))
}

edu_necessity <- function(cal, outcome, conditions) {
  y <- cal[[outcome]]
  do.call(rbind, lapply(conditions, function(v) do.call(rbind, lapply(c(FALSE, TRUE), function(neg) {
    x <- if (neg) 1 - cal[[v]] else cal[[v]]; both <- sum(pmin(x, y))
    data.frame(condition = if (neg) paste0("~", v) else v, consistency = both / sum(y), coverage = both / sum(x))
  }))))
}

edu_literals <- function(term) strsplit(gsub("\\s", "", term), "*", fixed = TRUE)[[1]]

edu_qca_solution <- function(sol, label) {
  if (label == "intermediate") sol <- sol$i.sol[[1]]  # QCA keeps the parsimonious result in $solution
  ic <- sol$IC; terms <- sol$solution[[1]]
  inc <- if (!is.null(ic$incl.cov)) ic$incl.cov else ic$individual[[1]]$incl.cov
  tab <- data.frame(solution = label, term = rownames(inc), inc, row.names = NULL, check.names = FALSE)
  overall <- if (!is.null(ic$sol.incl.cov)) ic$sol.incl.cov else ic$individual[[1]]$sol.incl.cov
  list(terms = terms, table = tab, overall = data.frame(solution = label, overall, check.names = FALSE),
       n_models = length(sol$solution))
}

edu_fsqca <- function(d, outcome, conditions, anchors = NULL, incl.cut = 0.8, n.cut = 1, pri.cut = 0.7,
                      dir.exp = NULL, neg.out = FALSE) {
  edu_need("QCA")
  vars <- c(outcome, conditions); cal <- as.data.frame(lapply(d[vars], function(x) suppressWarnings(as.numeric(x))))
  rownames(cal) <- rownames(d)
  notes <- character()
  if (!is.null(anchors)) {
    for (v in names(anchors)) cal[[v]] <- edu_calibrate(cal[[v]], anchors[[v]][1], anchors[[v]][2], anchors[[v]][3])
    at <- sapply(cal[vars], function(x) sum(abs(x - 0.5) < 1e-12))
    for (v in vars) cal[[v]][abs(cal[[v]] - 0.5) < 1e-12] <- 0.501
    notes <- c(notes, "Direct calibration (log-odds; full exclusion, crossover, full inclusion anchors).",
               if (sum(at)) sprintf("%d memberships of exactly 0.5 were set to 0.501 so the cases are not dropped from the truth table.", sum(at)))
  }
  if (any(cal < 0 | cal > 1, na.rm = TRUE)) stop("Membership scores must lie in [0, 1]; supply anchors for raw variables.")
  cal <- cal[stats::complete.cases(cal), , drop = FALSE]
  if (neg.out) cal[[outcome]] <- 1 - cal[[outcome]]
  nec <- edu_necessity(cal, outcome, conditions)
  tt <- QCA::truthTable(cal, outcome = outcome, conditions = conditions, incl.cut = incl.cut, n.cut = n.cut,
                        pri.cut = pri.cut, sort.by = c("OUT", "incl"), complete = FALSE)
  ttab <- cbind(row = rownames(tt$tt), as.data.frame(tt$tt), row.names = NULL)
  comp <- edu_qca_solution(QCA::minimize(tt, details = TRUE), "complex")
  pars <- edu_qca_solution(QCA::minimize(tt, include = "?", details = TRUE), "parsimonious")
  inter <- if (!is.null(dir.exp)) edu_qca_solution(QCA::minimize(tt, include = "?", dir.exp = paste(dir.exp, collapse = ", "), details = TRUE), "intermediate") else NULL
  base <- if (is.null(inter)) comp else inter
  core <- lapply(pars$terms, edu_literals)
  config <- do.call(cbind, lapply(seq_along(base$terms), function(j) {
    lit <- edu_literals(base$terms[j]); core_lit <- unique(unlist(Filter(function(p) all(p %in% lit), core)))
    vapply(conditions, function(v) {
      if (v %in% lit) if (v %in% core_lit) "●" else "•"
      else if (paste0("~", v) %in% lit) if (paste0("~", v) %in% core_lit) "⊗" else "⊘"
      else ""
    }, character(1))
  }))
  colnames(config) <- paste0("C", seq_along(base$terms))
  bt <- base$table
  stats_rows <- rbind(consistency = bt$inclS, PRI = bt$PRI, raw_coverage = bt$covS, unique_coverage = bt$covU)
  stats_rows <- matrix(sprintf("%.3f", stats_rows), nrow = 4, dimnames = list(rownames(stats_rows), colnames(config)))
  conf_tab <- data.frame(row = c(conditions, rownames(stats_rows)), rbind(config, stats_rows), row.names = NULL, check.names = FALSE)
  overall <- rbind(comp$overall, pars$overall, if (!is.null(inter)) inter$overall)
  if (any(c(comp$n_models, pars$n_models, inter$n_models) > 1)) notes <- c(notes, "More than one equivalent model exists; the first is tabulated, list the others from QCA::minimize output.")
  notes <- c(notes, sprintf("Truth table: consistency cut %.2f, PRI cut %.2f, frequency cut %d; %s.", incl.cut, pri.cut, n.cut,
                            if (is.null(inter)) "no directional expectations given, so the configuration table uses the complex solution"
                            else paste("directional expectations", paste(dir.exp, collapse = ", "))),
             "Configuration table: ● core present, • peripheral present, ⊗ core absent, ⊘ peripheral absent, blank = either (Fiss 2011). Core = also in the parsimonious solution.",
             "Necessity: consistency >= .90 is the usual threshold for a necessary condition.")
  list(calibrated = cbind(case = rownames(cal), cal, row.names = NULL), necessity = nec, truth_table = ttab,
       solutions = rbind(comp$table, pars$table, if (!is.null(inter)) inter$table), solution_fit = overall,
       configurations = conf_tab, notes = notes)
}

edu_fsqca_robust <- function(d, outcome, conditions, anchors = NULL, variants, ...) {
  rows <- lapply(names(variants), function(nm) {
    args <- utils::modifyList(list(d = d, outcome = outcome, conditions = conditions, anchors = anchors, ...), variants[[nm]])
    r <- do.call(edu_fsqca, args); sf <- r$solution_fit; last <- sf[nrow(sf), ]
    sol <- r$solutions[r$solutions$solution == last$solution, "term"]
    data.frame(variant = nm, solution_type = last$solution, terms = paste(sol, collapse = " + "),
               consistency = last$inclS, PRI = last$PRI, coverage = last$covS)
  })
  list(robustness = do.call(rbind, rows),
       notes = "Compare the solution terms across variants: identical or subset/superset solutions with similar consistency and coverage support robustness (Schneider & Wagemann 2012).")
}

# ---------------------------------------------------------------- NCA
edu_nca <- function(d, x, y, ceilings = c("ce_fdh", "cr_fdh"), test.rep = 10000, seed = 1, bottleneck_steps = 10) {
  edu_need("NCA"); set.seed(seed)
  dd <- edu_num(d, c(x, y)); dd <- dd[stats::complete.cases(dd), , drop = FALSE]
  m <- NCA::nca_analysis(dd, x, y, ceilings = ceilings, test.rep = test.rep, steps = bottleneck_steps,
                         bottleneck.x = "percentage.range", bottleneck.y = "percentage.range")
  size <- function(v) ifelse(v < .1, "small", ifelse(v < .3, "medium", ifelse(v < .5, "large", "very large")))
  eff <- do.call(rbind, lapply(x, function(v) do.call(rbind, lapply(ceilings, function(cl) {
    s <- m$summaries[[v]]$params
    data.frame(condition = v, ceiling = cl, effect_size = as.numeric(s["Effect size", cl]), p = as.numeric(s["p-value", cl]),
               accuracy = as.numeric(s["Ceiling accuracy", cl]), ceiling_zone = as.numeric(s["Ceiling zone", cl]),
               scope = as.numeric(m$summaries[[v]]$global["Scope", 1]))
  }))))
  eff$size <- size(eff$effect_size)
  bn <- lapply(ceilings, function(cl) { b <- as.data.frame(m$bottlenecks[[cl]]); cbind(ceiling = cl, b) })
  list(effects = eff, bottlenecks = do.call(rbind, bn),
       notes = c(sprintf("n = %d; permutation test with %d repetitions (seed %d).", nrow(dd), test.rep, seed),
                 "A condition is reported as necessary when d >= .10 and the permutation p < .05 (Dul 2016; Dul et al. 2020): 0-.1 small, .1-.3 medium, .3-.5 large, >= .5 very large."))
}

# ---------------------------------------------------------------- coding agreement and clustering
edu_kappa <- function(r1, r2) {
  edu_need("psych")
  lev <- sort(unique(c(as.character(r1), as.character(r2)))); a <- factor(r1, lev); b <- factor(r2, lev)
  tab <- table(a, b); k <- psych::cohen.kappa(cbind(as.integer(a), as.integer(b)))
  list(agreement = data.frame(n = sum(tab), percent_agreement = 100 * sum(diag(tab)) / sum(tab),
                              kappa = k$kappa, ci_low = k$confid[1, 1], ci_high = k$confid[1, 3]),
       notes = "Cohen's kappa (unweighted). Report it only for codebook-based coding, not for reflexive thematic analysis.")
}

edu_icc <- function(d, y, cluster) {
  edu_need("lme4")
  dd <- data.frame(y = as.numeric(d[[y]]), g = factor(d[[cluster]])); dd <- dd[stats::complete.cases(dd), ]
  m <- lme4::lmer(y ~ 1 + (1 | g), data = dd, REML = TRUE)
  vc <- as.data.frame(lme4::VarCorr(m)); tau <- vc$vcov[vc$grp == "g"]; s2 <- vc$vcov[vc$grp == "Residual"]
  icc <- tau / (tau + s2); avg <- mean(table(dd$g))
  list(icc = data.frame(clusters = nlevels(dd$g), n = nrow(dd), mean_cluster_size = avg, ICC = icc,
                        design_effect = 1 + (avg - 1) * icc),
       notes = "ICC from an intercept-only random-effects model. Design effect > 2 (or ICC >= .05) usually calls for a multilevel model.")
}

# ---------------------------------------------------------------- extra method groups
# Sourced from the folder this file was sourced from (the scripts folder, or a run folder that run_r.py
# filled with every edu_methods*.R).
local({
  here <- "."
  for (i in rev(seq_len(sys.nframe()))) {
    f <- sys.frame(i)$ofile
    if (!is.null(f)) { here <- dirname(f); break }
  }
  for (f in list.files(here, "^edu_methods_[a-z]+\\.R$", full.names = TRUE)) source(f, encoding = "UTF-8")
})
