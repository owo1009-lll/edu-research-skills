# edu_methods_latent.R — latent profile analysis (mclust), latent class analysis (poLCA) and IRT (mirt).
# Source after edu_methods.R (uses edu_need() and edu_num()). Same return convention: a list of data
# frames plus `notes`, so edu_save() works. Information criteria are "smaller is better":
# AIC = -2LL + 2p, BIC = -2LL + p ln(n), SABIC = -2LL + p ln((n + 2) / 24).

edu_ic <- function(ll, p, n) c(AIC = -2 * ll + 2 * p, BIC = -2 * ll + p * log(n), SABIC = -2 * ll + p * log((n + 2) / 24))

edu_entropy <- function(z) {  # relative entropy of the posterior matrix (1 = perfect separation)
  if (ncol(z) < 2) return(NA_real_)
  1 - sum(ifelse(z > 0, -z * log(z), 0)) / (nrow(z) * log(ncol(z)))
}

edu_class_sizes <- function(z, share, prefix) {  # classes in the order of the columns of z
  cl <- max.col(z, ties.method = "first"); k <- ncol(z)
  data.frame(class = paste0(prefix, seq_len(k)), model_share = share,
             n_modal = tabulate(cl, k), pct_modal = 100 * tabulate(cl, k) / nrow(z),
             avepp = vapply(seq_len(k), function(j) if (any(cl == j)) mean(z[cl == j, j]) else NA_real_, numeric(1)))
}

edu_membership <- function(z, rows, prefix) {
  colnames(z) <- paste0("post_", prefix, seq_len(ncol(z)))
  data.frame(row = rows, class = paste0(prefix, max.col(z, ties.method = "first")), max_posterior = apply(z, 1, max), z,
             check.names = FALSE)
}

edu_pick <- function(fit, min_share) {  # provisional default: lowest BIC among solutions whose smallest class >= min_share
  ok <- fit[!is.na(fit$BIC) & !is.na(fit$min_class_pct) & fit$min_class_pct >= 100 * min_share, ]
  if (!nrow(ok)) ok <- fit[!is.na(fit$BIC), ]
  ok[which.min(ok$BIC), ]
}

# ---------------------------------------------------------------- latent profile analysis (mclust)
edu_lpa <- function(d, vars, k = 1:6, models = c("EEI", "VVI"), scale = TRUE, choose_k = NULL, choose_model = NULL,
                    nboot = 100, seed = 123, min_share = 0.05) {
  edu_need("mclust")
  x0 <- edu_num(d, vars); keep <- stats::complete.cases(x0); x <- as.matrix(x0[keep, , drop = FALSE]); n <- nrow(x)
  ctr <- colMeans(x); sds <- apply(x, 2, stats::sd)
  if (scale) x <- sweep(sweep(x, 2, ctr), 2, sds, "/")
  fits <- list(); rows <- list()
  for (m in models) for (g in k) {
    # Mclust() evaluates its call in the caller's frame and needs mclustBIC() visible there, so run it
    # inside an environment whose parent is the mclust namespace (no attaching).
    f <- tryCatch(eval(quote(Mclust(x, G = g, modelNames = m, verbose = FALSE)),
                       list2env(list(x = x, g = g, m = m), parent = asNamespace("mclust"))), error = function(e) NULL)
    id <- paste(m, g); fits[[id]] <- f
    if (is.null(f)) { rows[[id]] <- data.frame(model = m, k = g, LL = NA, npar = NA, AIC = NA, BIC = NA, SABIC = NA,
                                               entropy = NA, min_class_pct = NA, min_class_n = NA); next }
    ic <- edu_ic(f$loglik, f$df, n)
    rows[[id]] <- data.frame(model = m, k = g, LL = f$loglik, npar = f$df, AIC = ic[["AIC"]], BIC = ic[["BIC"]],
                             SABIC = ic[["SABIC"]], entropy = edu_entropy(f$z), min_class_pct = 100 * min(f$parameters$pro),
                             min_class_n = min(tabulate(f$classification, g)))
  }
  fit <- do.call(rbind, rows); rownames(fit) <- NULL
  fit$blrt_lrts <- NA_real_; fit$blrt_p <- NA_real_
  if (nboot > 0 && max(k) > 1) for (m in models) {
    set.seed(seed)
    b <- tryCatch(eval(quote(mclustBootstrapLRT(x, modelName = m, nboot = nboot, maxG = maxG, verbose = FALSE)),
                       list2env(list(x = x, m = m, nboot = nboot, maxG = max(k) - 1), parent = asNamespace("mclust"))),
                  error = function(e) NULL)
    if (is.null(b)) next
    for (g in intersect(k, 2:max(k))) {
      i <- fit$model == m & fit$k == g
      if (g - 1 <= length(b$obs)) { fit$blrt_lrts[i] <- b$obs[g - 1]; fit$blrt_p[i] <- b$p.value[g - 1] }
    }
  }
  pick <- if (is.null(choose_k)) edu_pick(fit, min_share) else
    fit[fit$k == choose_k & fit$model == (if (is.null(choose_model)) models[1] else choose_model), ]
  f <- fits[[paste(pick$model, pick$k)]]
  if (is.null(f)) stop("The chosen solution did not converge; choose another k or model.")
  o <- order(f$parameters$pro, decreasing = TRUE); z <- f$z[, o, drop = FALSE]
  mu <- f$parameters$mean[, o, drop = FALSE]
  raw <- if (scale) mu * sds + ctr else mu
  means <- data.frame(variable = vars, raw, check.names = FALSE); names(means)[-1] <- paste0("P", seq_along(o))
  out <- list(fit = fit, profile_sizes = edu_class_sizes(z, f$parameters$pro[o], "P"), profile_means = means)
  if (scale) { zm <- data.frame(variable = vars, mu); names(zm)[-1] <- paste0("P", seq_along(o)); out$profile_means_z <- zm }
  out$membership <- edu_membership(z, which(keep), "P")
  desc <- c(EEI = "equal variances across profiles, covariances fixed at 0 (local independence)",
            VVI = "variances differ across profiles, covariances fixed at 0",
            EEE = "equal full covariance matrices", VVV = "unrestricted covariance matrices per profile")
  out$notes <- c(
    sprintf("Gaussian mixture (mclust) on %d complete cases of %d; %s. Models: %s.",
            n, nrow(d), if (scale) "indicators standardized (z) before fitting; profile_means are back-transformed to raw units" else "raw indicators",
            paste(ifelse(models %in% names(desc), paste(models, "=", desc[models]), models), collapse = "; ")),
    "AIC/BIC/SABIC are -2LL-based (smaller is better); mclust prints BIC with the opposite sign. Entropy is relative entropy (>= .80 good classification, Clark & Muthen 2009); avepp = average posterior probability of the assigned class (>= .70, Nagin 2005).",
    if (nboot > 0) sprintf("BLRT row k tests k-1 vs k classes (mclustBootstrapLRT, %d replications, seed %d); with %d replications the smallest attainable p is %.3f.", nboot, seed, nboot, 1 / (nboot + 1)) else "BLRT not run (nboot = 0).",
    if (is.null(choose_k)) sprintf("Profile tables show %s with k = %d, chosen provisionally as the lowest BIC among solutions whose smallest class is >= %.0f%%. Decide k with BIC/SABIC, BLRT, entropy, class size and interpretability (Nylund et al. 2007), then rerun with choose_k/choose_model.", pick$model, pick$k, 100 * min_share)
    else sprintf("Profile tables show %s with k = %d (chosen by the analyst).", pick$model, pick$k),
    "EM starts from model-based hierarchical clustering (deterministic); profiles are ordered by size (P1 largest). Membership uses modal assignment; relating classes to outcomes from this table ignores classification error (use a three-step/BCH approach).")
  out
}

# ---------------------------------------------------------------- latent class analysis (poLCA)
edu_lca <- function(d, items, k = 1:5, nrep = 20, maxiter = 5000, choose_k = NULL, seed = 123, min_share = 0.05) {
  edu_need("poLCA")
  raw <- d[items]; keep <- stats::complete.cases(raw); raw <- raw[keep, , drop = FALSE]
  levs <- lapply(raw, function(v) levels(factor(v)))
  dat <- as.data.frame(lapply(raw, function(v) as.integer(factor(v))))  # poLCA needs categories coded 1, 2, ...
  names(dat) <- paste0("i", seq_along(items))
  f <- stats::as.formula(paste0("cbind(", paste(names(dat), collapse = ", "), ") ~ 1"))
  n <- nrow(dat); fits <- list(); rows <- list()
  for (g in k) {
    set.seed(seed)
    m <- tryCatch(suppressWarnings(poLCA::poLCA(f, dat, nclass = g, nrep = if (g == 1) 1 else nrep, maxiter = maxiter,
                                                 verbose = FALSE, graphs = FALSE, calc.se = FALSE)),
                  error = function(e) NULL)
    fits[[as.character(g)]] <- m
    if (is.null(m)) { rows[[as.character(g)]] <- data.frame(k = g, LL = NA, npar = NA, AIC = NA, BIC = NA, SABIC = NA, entropy = NA,
                                              min_class_pct = NA, min_class_n = NA, G2 = NA, X2 = NA, df = NA, best_ll_replicated = NA); next }
    ic <- edu_ic(m$llik, m$npar, n)
    att <- if (length(m$attempts)) m$attempts else m$llik
    rows[[as.character(g)]] <- data.frame(k = g, LL = m$llik, npar = m$npar, AIC = ic[["AIC"]], BIC = ic[["BIC"]], SABIC = ic[["SABIC"]],
                            entropy = edu_entropy(m$posterior), min_class_pct = 100 * min(m$P),
                            min_class_n = min(tabulate(m$predclass, g)), G2 = m$Gsq, X2 = m$Chisq, df = m$resid.df,
                            best_ll_replicated = sprintf("%d/%d", sum(abs(att - max(att)) < 0.01), length(att)))
  }
  fit <- do.call(rbind, rows); rownames(fit) <- NULL
  pick <- if (is.null(choose_k)) edu_pick(fit, min_share) else fit[fit$k == choose_k, ]
  m <- fits[[as.character(pick$k)]]
  if (is.null(m)) stop("The chosen solution did not converge; choose another k.")
  o <- order(m$P, decreasing = TRUE); z <- m$posterior[, o, drop = FALSE]
  probs <- do.call(rbind, lapply(seq_along(items), function(j) {
    p <- m$probs[[j]][o, , drop = FALSE]
    tab <- data.frame(item = items[j], category = levs[[j]], t(p), row.names = NULL)
    names(tab)[-(1:2)] <- paste0("C", seq_along(o)); tab
  }))
  out <- list(fit = fit, class_sizes = edu_class_sizes(z, m$P[o], "C"), item_probabilities = probs,
              membership = edu_membership(z, which(keep), "C"))
  out$notes <- c(
    sprintf("Latent class model (poLCA) on %d complete cases of %d; %d random starts per k (seed %d). best_ll_replicated = starts reaching the best log-likelihood (within .01); if it is 1/%d, raise nrep.",
            n, nrow(d), nrep, seed, nrep),
    "AIC/BIC/SABIC are -2LL-based (smaller is better). G2 and X2 compare with the observed response-pattern table; with sparse tables (many items or categories) their chi-square p values are not trustworthy, so judge by information criteria. df < 0 means the model is not identified.",
    "Entropy is relative entropy (>= .80 good); avepp >= .70 for each class. poLCA has no BLRT; if a BLRT is required, run it in Mplus or with a parametric bootstrap.",
    if (is.null(choose_k)) sprintf("Class tables show k = %d, chosen provisionally as the lowest BIC among solutions whose smallest class is >= %.0f%%; decide k with BIC/SABIC, entropy, class size and interpretability (Nylund et al. 2007), then rerun with choose_k.", pick$k, 100 * min_share)
    else sprintf("Class tables show k = %d (chosen by the analyst).", pick$k),
    "Classes are ordered by size (C1 largest). item_probabilities = probability of each response category given the class.")
  out
}

# ---------------------------------------------------------------- item response theory (mirt)
edu_irt <- function(d, items, model = c("Rasch", "2PL", "graded"), compare = TRUE, scores = FALSE, quadpts = 61) {
  edu_need("mirt"); model <- match.arg(model)
  x <- edu_num(d, items); keep <- rowSums(!is.na(x)) > 0; x <- x[keep, , drop = FALSE]
  ncat <- vapply(x, function(v) length(unique(v[!is.na(v)])), integer(1)); dich <- all(ncat == 2)
  if (model == "2PL" && !dich) stop("2PL needs dichotomous items; use model = \"graded\" for ordinal items.")
  fit1 <- function(type, ...) mirt::mirt(x, 1, itemtype = type, SE = TRUE, verbose = FALSE, quadpts = quadpts, ...)
  mod <- fit1(model)
  cf <- mirt::coef(mod, IRTpars = TRUE, printSE = TRUE)
  par <- do.call(rbind, lapply(items, function(it) {
    p <- cf[[it]]; keepc <- !colnames(p) %in% c("g", "u")
    est <- p["par", keepc]; se <- if ("SE" %in% rownames(p)) p["SE", keepc] else rep(NA, sum(keepc))
    r <- data.frame(item = it, t(est), check.names = FALSE); r2 <- data.frame(t(se)); names(r2) <- paste0("SE_", colnames(p)[keepc])
    cbind(r, r2)
  }))
  if (model == "Rasch") par$SE_a <- NA
  ifit <- tryCatch({
    s <- mirt::itemfit(mod, fit_stats = "S_X2")
    data.frame(item = s$item, S_X2 = s$S_X2, df = s$df.S_X2, RMSEA = s$RMSEA.S_X2, p = s$p.S_X2)
  }, error = function(e) NULL)
  m2 <- tryCatch(mirt::M2(mod), error = function(e) NULL); m2type <- "M2"
  if (is.null(m2) || !is.finite(m2$df) || m2$df <= 0) {
    m2 <- tryCatch(mirt::M2(mod, type = "C2"), error = function(e) NULL); m2type <- "C2"
  }
  n <- nrow(x); ll <- mirt::extract.mirt(mod, "logLik"); np <- mirt::extract.mirt(mod, "nest"); ic <- edu_ic(ll, np, n)
  fs <- mirt::fscores(mod, method = "EAP", full.scores.SE = TRUE)
  gp <- cf$GroupPars
  fit <- data.frame(model = model, n = n, LL = ll, npar = np, AIC = ic[["AIC"]], BIC = ic[["BIC"]], SABIC = ic[["SABIC"]],
                    stat = m2type, M2 = if (!is.null(m2)) m2[[1]][1] else NA, df = if (!is.null(m2)) m2$df[1] else NA,
                    p = if (!is.null(m2)) m2$p[1] else NA, RMSEA = if (!is.null(m2)) m2$RMSEA[1] else NA,
                    RMSEA_low = if (!is.null(m2)) m2$RMSEA_5[1] else NA, RMSEA_high = if (!is.null(m2)) m2$RMSEA_95[1] else NA,
                    SRMSR = if (!is.null(m2)) m2$SRMSR[1] else NA, CFI = if (!is.null(m2)) m2$CFI[1] else NA,
                    TLI = if (!is.null(m2)) m2$TLI[1] else NA,
                    marginal_rxx = unname(mirt::marginal_rxx(mod)), empirical_rxx = unname(mirt::empirical_rxx(fs)[1]),
                    theta_var = gp["par", "COV_11"])
  out <- list(model_fit = fit, item_parameters = par)
  if (!is.null(ifit)) out$item_fit <- ifit
  if (compare) {
    if (dich) { labs <- c("Rasch", "2PL"); m0 <- if (model == "Rasch") mod else fit1("Rasch"); m1 <- if (model == "2PL") mod else fit1("2PL") }
    else if (model == "graded") {
      labs <- c("graded, equal slopes", "graded")
      m0 <- fit1("graded", model = mirt::mirt.model(sprintf("F = 1-%d\nCONSTRAIN = (1-%d, a1)", ncol(x), ncol(x)))); m1 <- mod
    } else { labs <- c("Rasch (PCM)", "GPCM"); m0 <- mod; m1 <- fit1("gpcm") }
    lls <- c(mirt::extract.mirt(m0, "logLik"), mirt::extract.mirt(m1, "logLik"))
    nps <- c(mirt::extract.mirt(m0, "nest"), mirt::extract.mirt(m1, "nest"))
    ics <- rbind(edu_ic(lls[1], nps[1], n), edu_ic(lls[2], nps[2], n))
    lr <- 2 * (lls[2] - lls[1]); ddf <- nps[2] - nps[1]
    out$model_comparison <- data.frame(model = labs, LL = lls, npar = nps, AIC = ics[, "AIC"], BIC = ics[, "BIC"], SABIC = ics[, "SABIC"],
                                       LR_chi2 = c(NA, lr), df = c(NA, ddf), p = c(NA, stats::pchisq(lr, ddf, lower.tail = FALSE)))
  }
  if (scores) out$scores <- data.frame(row = which(keep), theta_EAP = fs[, 1], SE = fs[, 2])
  out$notes <- c(
    sprintf("Unidimensional %s model (mirt, marginal ML/EM, %d quadrature points), n = %d persons with at least one response; missing responses handled by full-information ML.", model, quadpts, n),
    "Item parameters in IRT metric: a = discrimination, b = difficulty (dichotomous) or b1..bk = category thresholds (graded: theta where P(X >= k) = .5; Rasch with polytomous items = PCM step parameters). SEs by the delta method.",
    if (model == "Rasch") sprintf("Rasch: slopes fixed at 1 and the latent variance estimated (theta_var = %.3f), so b is in logits; dividing b by sqrt(theta_var) gives the 1PL metric with SD(theta) = 1.", gp["par", "COV_11"]) else "Latent trait fixed at mean 0, variance 1.",
    sprintf("Model fit: %s statistic with RMSEA (90%% CI), SRMSR, CFI and TLI (Maydeu-Olivares & Joe 2006); RMSEA <= .05 and SRMSR <= .05 indicate close fit. Item fit: S-X2 (Orlando & Thissen 2000) with RMSEA; flag items with p < .01 (many tests) and RMSEA > .05.", m2type),
    if (is.null(ifit)) "S-X2 item fit could not be computed (often because of missing responses or too few items)." else NULL,
    "marginal_rxx = model-based marginal reliability; empirical_rxx = reliability of the EAP scores. Neither checks unidimensionality or local independence: test these first (CFA/EFA, Q3 residuals).",
    if (compare) "model_comparison: likelihood-ratio test of the nested equal-slope model against the free-slope model; p < .05 favours free slopes (items discriminate differently)." else NULL)
  out
}
