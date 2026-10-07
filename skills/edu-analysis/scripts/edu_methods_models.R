# edu_methods_models.R — meta-analysis, ordinal / multinomial / count regression and Bayes factors.
# Source after edu_methods.R (uses edu_need(), edu_num(), edu_save()). Packages: metafor, ordinal,
# nnet, MASS, pscl, BayesFactor, each loaded only by the function that needs it. Every function
# returns a named list of data frames plus `notes`, so edu_save() writes it.

edu_wald <- function(term, b, se, expo = NULL, ...) {
  z <- b / se; q <- stats::qnorm(.975)
  out <- data.frame(..., term = term, B = b, SE = se, z = z, p = 2 * stats::pnorm(-abs(z)), row.names = NULL)
  if (!is.null(expo)) { out[[expo]] <- exp(b); out[[paste0(expo, "_low")]] <- exp(b - q * se); out[[paste0(expo, "_high")]] <- exp(b + q * se) }
  out
}

# ================================================================ meta-analysis (metafor)
edu_meta_data <- function(d, measure, cols, yi, vi, label) {
  edu_need("metafor")
  if (!is.null(yi)) {
    es <- data.frame(yi = as.numeric(d[[yi]]), vi = as.numeric(d[[vi]])); measure <- "GEN"
  } else {
    if (!length(cols)) stop("Give the escalc inputs as column names (e.g. m1i = \"m_t\") or give yi and vi")
    es <- do.call(metafor::escalc, c(list(measure = measure), lapply(cols, function(cn) d[[cn]])))
  }
  dat <- d; dat$yi <- as.numeric(es$yi); dat$vi <- as.numeric(es$vi)
  dat$.label <- if (is.null(label)) paste("Study", seq_len(nrow(d))) else as.character(d[[label]])
  keep <- !is.na(dat$yi) & !is.na(dat$vi); dat <- dat[keep, , drop = FALSE]
  back <- if (measure %in% c("RR", "OR", "PETO", "IRR", "ROM", "HR")) exp else if (measure %in% c("ZCOR", "ZPCOR")) tanh else
    if (measure == "PLO") stats::plogis else NULL
  list(dat = dat, measure = measure, back = back, dropped = sum(!keep))
}

edu_meta_coefs <- function(m, model) {
  data.frame(model = model, term = rownames(m$beta), estimate = as.numeric(m$beta), SE = m$se, z = m$zval,
             p = m$pval, ci_low = m$ci.lb, ci_high = m$ci.ub, row.names = NULL)
}

edu_meta <- function(d, measure = "SMD", ..., yi = NULL, vi = NULL, moderators = NULL, method = "REML",
                     study_id = NULL, label = NULL, test = "z") {
  # `...` maps escalc arguments to columns, e.g. m1i = "m_t", sd1i = "sd_t", n1i = "n_t", m2i = "m_c", sd2i = "sd_c",
  # n2i = "n_c" (SMD = Hedges' g); ri = "r", ni = "n" (ZCOR); ai/bi/ci/di (OR, RR). Or give yi and vi directly.
  md <- edu_meta_data(d, measure, list(...), yi, vi, label); dat <- md$dat; measure <- md$measure; k <- nrow(dat)
  if (k < 2) stop("A meta-analysis needs at least two effect sizes")
  re <- metafor::rma(yi, vi, data = dat, method = method, test = test)
  w <- stats::weights(re)
  effects <- data.frame(study = dat$.label, yi = dat$yi, vi = dat$vi, SE = sqrt(dat$vi),
                        ci_low = dat$yi - stats::qnorm(.975) * sqrt(dat$vi), ci_high = dat$yi + stats::qnorm(.975) * sqrt(dat$vi),
                        weight_pct = as.numeric(w))
  pr <- stats::predict(re)
  pooled <- data.frame(model = if (method %in% c("FE", "EE", "CE")) "fixed (common) effect" else paste0("random effects (", method, ")"),
                       k = k, estimate = as.numeric(re$beta), SE = re$se, z = re$zval, p = re$pval, ci_low = re$ci.lb,
                       ci_high = re$ci.ub, pi_low = if (is.null(pr$pi.lb)) NA else pr$pi.lb, pi_high = if (is.null(pr$pi.ub)) NA else pr$pi.ub)
  if (!is.null(md$back)) for (v in c("estimate", "ci_low", "ci_high", "pi_low", "pi_high"))
    pooled[[paste0(v, "_back")]] <- md$back(pooled[[v]])
  ci <- tryCatch(stats::confint(re)$random, error = function(e) NULL)
  cv <- function(row, j) if (is.null(ci)) NA else unname(ci[row, j])
  het <- data.frame(Q = re$QE, df = k - 1, p_Q = re$QEp, tau2 = re$tau2, tau2_ci_low = cv(1, 2), tau2_ci_high = cv(1, 3),
                    tau = sqrt(re$tau2), I2_pct = re$I2, I2_ci_low = cv(3, 2), I2_ci_high = cv(3, 3), H2 = re$H2,
                    H2_ci_low = cv(4, 2), H2_ci_high = cv(4, 3))
  out <- list(effects = effects, pooled = pooled, heterogeneity = het)
  notes <- c(sprintf("k = %d effect sizes, measure = %s%s; %s.", k, measure,
                     if (measure == "SMD") " (Hedges' g, small-sample corrected)" else "",
                     if (md$dropped) sprintf("%d rows dropped for missing yi/vi", md$dropped) else "no rows dropped"),
             "Prediction interval (pi_low, pi_high) = range of true effects expected in a new comparable setting; report it with the CI. tau2/I2/H2 CIs use the Q-profile method.",
             "I2 is the share of observed variance not due to sampling error; it is not an absolute amount of heterogeneity (report tau and the prediction interval as well).")
  if (!is.null(md$back)) notes <- c(notes, "Columns *_back are back-transformed (exp for log ratios, tanh for Fisher z) for reporting; analysis is on the transformed scale.")
  if (test == "z" && k < 20) notes <- c(notes, "With few studies, Knapp-Hartung inference (test = \"knha\") gives better CI coverage; consider it as a sensitivity analysis.")
  if (length(moderators)) {
    mr <- metafor::rma(yi, vi, mods = stats::reformulate(moderators), data = dat, method = method, test = test)
    out$moderators <- edu_meta_coefs(mr, "meta-regression")
    out$moderator_test <- data.frame(QM = mr$QM, QM_df = mr$QMdf[1], QM_p = mr$QMp, QE = mr$QE, QE_df = mr$k - mr$p, QE_p = mr$QEp,
                                     tau2_residual = mr$tau2, I2_residual_pct = mr$I2,
                                     R2_pct = if (is.null(mr$R2)) NA else mr$R2)
    sub <- list()
    for (m in moderators[!vapply(dat[moderators], is.numeric, logical(1))]) {
      g <- factor(dat[[m]]); qb <- metafor::rma(yi, vi, mods = ~ g, data = data.frame(yi = dat$yi, vi = dat$vi, g = g), method = method, test = test)
      for (l in levels(g)) {
        s <- dat[g == l, ]
        f <- if (nrow(s) >= 2) metafor::rma(yi, vi, data = s, method = method, test = test) else NULL
        sub[[length(sub) + 1]] <- data.frame(moderator = m, level = l, k = nrow(s), estimate = if (is.null(f)) s$yi else as.numeric(f$beta),
          SE = if (is.null(f)) sqrt(s$vi) else f$se, ci_low = if (is.null(f)) NA else f$ci.lb, ci_high = if (is.null(f)) NA else f$ci.ub,
          tau2 = if (is.null(f)) NA else f$tau2, I2_pct = if (is.null(f)) NA else f$I2,
          Q_between = qb$QM, df_between = qb$QMdf[1], p_between = qb$QMp)
      }
    }
    if (length(sub)) out$subgroups <- do.call(rbind, sub)
    notes <- c(notes, "Moderators: QM tests all moderator coefficients together; R2_pct = proportional reduction in tau2. Subgroup Q_between comes from a mixed-effects model with a common tau2; per-level estimates use separate tau2. Moderator analyses are observational (study-level confounding) and need about 10 studies per moderator.")
  }
  if (k >= 3) {
  eg <- metafor::regtest(re, model = "lm")
  tf <- tryCatch(metafor::trimfill(re), error = function(e) NULL)
  out$publication_bias <- data.frame(
    test = c("Egger regression (classical, weighted lm on SE)", "Trim-and-fill (L0)"),
    statistic = c(eg$zval, if (is.null(tf)) NA else tf$k0), df = c(eg$dfs, NA), p = c(eg$pval, NA),
    detail = c(sprintf("limit estimate as SE -> 0 = %.4f", eg$est),
               if (is.null(tf)) "not available for this model" else sprintf("%d studies imputed on the %s side", tf$k0, tf$side)),
    adjusted_estimate = c(eg$est, if (is.null(tf)) NA else as.numeric(tf$beta)),
    adjusted_ci_low = c(eg$ci.lb, if (is.null(tf)) NA else tf$ci.lb), adjusted_ci_high = c(eg$ci.ub, if (is.null(tf)) NA else tf$ci.ub))
  } else notes <- c(notes, "Publication-bias tests skipped: Egger's regression needs at least 3 studies.")
  notes <- c(notes, "Egger's test and trim-and-fill detect small-study asymmetry, which can come from heterogeneity as well as publication bias; with fewer than 10 studies they have little power (Sterne et al., 2011). Trim-and-fill gives a sensitivity estimate, not a corrected effect.")
  l1 <- as.data.frame(metafor::leave1out(re)); inf <- stats::influence(re)
  for (v in c("tau2", "I2", "Q")) if (is.null(l1[[v]])) l1[[v]] <- NA_real_
  out$leave_one_out <- data.frame(omitted = dat$.label, estimate = l1$estimate, SE = l1$se, ci_low = l1$ci.lb, ci_high = l1$ci.ub,
                                  p = l1$pval, Q = l1$Q, tau2 = l1$tau2, I2_pct = l1$I2, cook_d = inf$inf$cook.d,
                                  influential = ifelse(inf$is.infl, "yes", ""))
  notes <- c(notes, "Leave-one-out: each row refits the model without that study; influential = flagged by metafor::influence (Viechtbauer & Cheung, 2010).")
  if (!is.null(study_id)) {
    dat$.study <- as.character(dat[[study_id]]); dat$.es <- seq_len(k)
    if (!anyDuplicated(dat$.study)) {
      notes <- c(notes, "study_id given but every study has one effect size, so the three-level model is not identified; the two-level model is reported.")
    } else {
      m3 <- metafor::rma.mv(yi, vi, random = ~ 1 | .study / .es, data = dat, method = "REML", test = if (test == "knha") "t" else "z")
      m2 <- metafor::rma.mv(yi, vi, random = ~ 1 | .study / .es, data = dat, method = "REML", sigma2 = c(0, NA))
      lrt <- metafor::anova.rma(m3, m2)
      wv <- 1 / dat$vi; vt <- (k - 1) * sum(wv) / (sum(wv)^2 - sum(wv^2)); tot <- sum(m3$sigma2) + vt
      out$three_level <- rbind(
        data.frame(component = "pooled estimate", value = as.numeric(m3$beta), SE = m3$se, ci_low = m3$ci.lb, ci_high = m3$ci.ub,
                   p = m3$pval, levels = m3$s.nlevels[1], variance_pct = NA),
        data.frame(component = c("sigma2 level 3 (between studies)", "sigma2 level 2 (within studies)", "sampling variance level 1 (typical)"),
                   value = c(m3$sigma2, vt), SE = NA, ci_low = NA, ci_high = NA, p = NA,
                   levels = c(m3$s.nlevels, k), variance_pct = 100 * c(m3$sigma2, vt) / tot),
        data.frame(component = "LRT: drop level 3 (chi2, df = 1)", value = lrt$LRT, SE = NA, ci_low = NA, ci_high = NA, p = lrt$pval,
                   levels = NA, variance_pct = NA))
      if (length(moderators)) {
        mm <- metafor::rma.mv(yi, vi, mods = stats::reformulate(moderators), random = ~ 1 | .study / .es, data = dat, method = "REML")
        out$moderators_three_level <- edu_meta_coefs(mm, "three-level meta-regression")
        out$moderators_three_level$QM <- mm$QM; out$moderators_three_level$QM_p <- mm$QMp
      }
      notes <- c(notes, sprintf("Three-level model (rma.mv, effects nested in %d studies): use it as the main result because effect sizes from the same study are dependent; the two-level heterogeneity, bias and leave-one-out tables ignore this dependence. Variance shares follow Cheung (2014); the LRT boundary test is conservative.", m3$s.nlevels[1]))
    }
  }
  out$notes <- notes
  out
}

edu_meta_plot <- function(d, measure = "SMD", ..., yi = NULL, vi = NULL, method = "REML", label = NULL, file = "output/meta") {
  # Writes <file>_forest.png (with prediction interval) and <file>_funnel.png (trim-and-fill points shown open).
  md <- edu_meta_data(d, measure, list(...), yi, vi, label); dat <- md$dat
  re <- metafor::rma(yi, vi, data = dat, method = method, slab = dat$.label)
  dir.create(dirname(file), showWarnings = FALSE, recursive = TRUE)
  ff <- paste0(file, "_forest.png"); fu <- paste0(file, "_funnel.png")
  grDevices::png(ff, width = 2200, height = 600 + 75 * nrow(dat), res = 300)
  if (identical(md$back, exp)) metafor::forest(re, atransf = exp, addpred = TRUE, header = TRUE)
  else if (!is.null(md$back)) metafor::forest(re, transf = md$back, addpred = TRUE, header = TRUE)
  else metafor::forest(re, addpred = TRUE, header = TRUE)
  grDevices::dev.off()
  grDevices::png(fu, width = 1800, height = 1500, res = 300)
  tf <- tryCatch(metafor::trimfill(re), error = function(e) NULL)
  if (is.null(tf)) metafor::funnel(re) else metafor::funnel(tf, legend = TRUE)
  grDevices::dev.off()
  invisible(c(forest = ff, funnel = fu))
}

# ================================================================ ordinal logistic regression
edu_ordinal <- function(d, y, x, levels = NULL, weights = NULL, link = "logit") {
  edu_need("ordinal")
  dd <- d[stats::complete.cases(d[c(y, x, weights)]), c(y, x, weights), drop = FALSE]
  yy <- dd[[y]]
  dd[[y]] <- if (!is.null(levels)) factor(yy, levels = levels, ordered = TRUE) else if (is.factor(yy)) factor(yy, levels = levels(yy), ordered = TRUE) else
    factor(yy, levels = sort(unique(yy)), ordered = TRUE)
  for (v in x) if (is.ordered(dd[[v]])) dd[[v]] <- factor(dd[[v]], ordered = FALSE)  # treatment contrasts, not .L/.Q
  dd$.w <- if (is.null(weights)) 1 else as.numeric(dd[[weights]])
  f <- stats::reformulate(x, response = y)
  fit <- ordinal::clm(f, data = dd, weights = .w, link = link)
  null <- ordinal::clm(stats::reformulate("1", response = y), data = dd, weights = .w, link = link)
  ct <- summary(fit)$coefficients; nb <- names(fit$beta)
  coefs <- data.frame(term = nb, B = ct[nb, 1], SE = ct[nb, 2], z = ct[nb, 3], p = ct[nb, 4], row.names = NULL)
  ci <- tryCatch(stats::confint(fit, type = "profile"), error = function(e) stats::confint(fit, type = "Wald"))
  lab <- if (link == "logit") "OR" else "exp_B"
  coefs[[lab]] <- exp(coefs$B); coefs[[paste0(lab, "_low")]] <- exp(ci[nb, 1]); coefs[[paste0(lab, "_high")]] <- exp(ci[nb, 2])
  na <- names(fit$alpha)
  thresholds <- data.frame(threshold = na, estimate = ct[na, 1], SE = ct[na, 2], row.names = NULL)
  lr <- 2 * (fit$logLik - null$logLik); dfm <- length(nb)
  fit_t <- data.frame(n_rows = nrow(dd), n_weighted = sum(dd$.w), categories = nlevels(dd[[y]]), logLik = fit$logLik,
                      deviance = -2 * fit$logLik, AIC = stats::AIC(fit), LR_chi2 = lr, df = dfm,
                      p = stats::pchisq(lr, dfm, lower.tail = FALSE), McFadden_R2 = 1 - fit$logLik / null$logLik,
                      Hessian_condition = fit$cond.H)
  po <- lapply(c(x, ".all"), function(v) {
    nom <- stats::reformulate(if (v == ".all") x else v)
    g <- tryCatch(ordinal::clm(f, nominal = nom, data = dd, weights = .w, link = link), error = function(e) NULL)
    if (is.null(g) || !is.finite(g$logLik)) return(data.frame(predictor = if (v == ".all") "all predictors" else v, LR_chi2 = NA, df = NA, p = NA))
    lrt <- 2 * (g$logLik - fit$logLik); dfx <- g$edf - fit$edf
    data.frame(predictor = if (v == ".all") "all predictors" else v, LR_chi2 = lrt, df = dfx, p = stats::pchisq(lrt, dfx, lower.tail = FALSE))
  })
  list(coefficients = coefs, thresholds = thresholds, fit = fit_t, proportional_odds = do.call(rbind, po),
       notes = c(sprintf("Cumulative %s model (ordinal::clm, same estimates as MASS::polr); outcome order: %s.", link, paste(levels(dd[[y]]), collapse = " < ")),
                 "Parameterisation logit P(Y <= j) = threshold_j - B*x: a positive B (OR > 1) means higher outcome categories are more likely. OR CIs are profile-likelihood 95%.",
                 "Proportional odds: each row is a likelihood-ratio test of letting that predictor's effect differ across thresholds (nominal effect; the LR analogue of the Brant test). p < .05 suggests the assumption fails for that predictor; with large n small departures become significant, so also compare the separate threshold-specific estimates or fit a partial proportional odds model.",
                 "Hessian_condition above 1e4 signals an ill-defined model (sparse categories, complete separation); merge sparse outcome categories.",
                 "McFadden R2 is a likelihood ratio index, not variance explained; values .2-.4 already indicate good fit."))
}

# ================================================================ multinomial logistic regression
edu_multinom <- function(d, y, x, ref = NULL, weights = NULL) {
  edu_need("nnet")
  dd <- d[stats::complete.cases(d[c(y, x, weights)]), c(y, x, weights), drop = FALSE]
  dd[[y]] <- factor(dd[[y]]); if (!is.null(ref)) dd[[y]] <- stats::relevel(dd[[y]], ref = as.character(ref))
  for (v in x) if (is.ordered(dd[[v]])) dd[[v]] <- factor(dd[[v]], ordered = FALSE)  # treatment contrasts, not .L/.Q
  dd$.w <- if (is.null(weights)) 1 else as.numeric(dd[[weights]])
  mfit <- function(f) nnet::multinom(f, data = dd, weights = .w, trace = FALSE, maxit = 1000, reltol = 1e-12, Hess = TRUE)
  f <- stats::reformulate(x, response = y); fit <- mfit(f); null <- mfit(stats::reformulate("1", response = y))
  s <- summary(fit); B <- s$coefficients; S <- s$standard.errors
  if (is.null(dim(B))) { B <- matrix(B, 1, dimnames = list(levels(dd[[y]])[2], names(B))); S <- matrix(S, 1, dimnames = dimnames(B)) }
  coefs <- do.call(rbind, lapply(rownames(B), function(o) edu_wald(colnames(B), B[o, ], S[o, ], expo = "RRR",
                                                                     outcome = paste(o, "vs", levels(dd[[y]])[1]))))
  ll <- as.numeric(stats::logLik(fit)); ll0 <- as.numeric(stats::logLik(null)); dfm <- fit$edf - null$edf
  fit_t <- data.frame(n_rows = nrow(dd), n_weighted = sum(dd$.w), categories = nlevels(dd[[y]]), reference = levels(dd[[y]])[1],
                      deviance = fit$deviance, AIC = fit$AIC, LR_chi2 = 2 * (ll - ll0), df = dfm,
                      p = stats::pchisq(2 * (ll - ll0), dfm, lower.tail = FALSE), McFadden_R2 = 1 - ll / ll0,
                      accuracy = stats::weighted.mean(as.character(stats::predict(fit)) == as.character(dd[[y]]), dd$.w))
  lrt <- do.call(rbind, lapply(x, function(v) {
    g <- if (length(x) > 1) mfit(stats::reformulate(setdiff(x, v), response = y)) else null
    chi <- 2 * (ll - as.numeric(stats::logLik(g))); df <- fit$edf - g$edf
    data.frame(predictor = v, LR_chi2 = chi, df = df, p = stats::pchisq(chi, df, lower.tail = FALSE))
  }))
  list(coefficients = coefs, fit = fit_t, predictor_tests = lrt,
       notes = c(sprintf("Multinomial logit (nnet::multinom); each outcome is compared with the reference category '%s'.", levels(dd[[y]])[1]),
                 "RRR = relative risk ratio exp(B): the multiplicative change in the odds of that category versus the reference per unit of x. Wald z tests and Wald 95% CIs.",
                 "predictor_tests: likelihood-ratio test of each predictor across all equations (report it before the category-specific RRRs).",
                 "Assumes independence of irrelevant alternatives; if the categories are ordered, edu_ordinal() is more efficient. Need roughly 10+ cases per parameter in the smallest category.",
                 "McFadden R2 = 1 - LL/LL0 (not variance explained)."))
}

# ================================================================ count models
edu_count_ll <- function(fit, type, y) {
  # per-observation log-likelihood, for the Vuong test
  mu <- stats::fitted(fit)
  switch(type, poisson = stats::dpois(y, mu, log = TRUE), negbin = stats::dnbinom(y, size = fit$theta, mu = mu, log = TRUE),
         { pr <- stats::predict(fit, type = "prob", at = 0:max(y)); log(pr[cbind(seq_along(y), y + 1)]) })
}

edu_count <- function(d, y, x, offset = NULL, zero = NULL, zero_x = x) {
  # offset = name of an exposure column (e.g. class hours); the models use log(exposure) as the offset.
  # zero = any of "zip", "zinb", "hurdle_poisson", "hurdle_nb"; zero_x = predictors of the zero / hurdle part.
  edu_need("MASS"); if (length(zero)) edu_need("pscl")
  vars <- unique(c(y, x, zero_x, offset)); dd <- d[stats::complete.cases(d[vars]), vars, drop = FALSE]
  yy <- dd[[y]]
  if (any(yy < 0 | yy != round(yy))) stop("The outcome must be a non-negative integer count")
  rhs <- paste(x, collapse = " + ")
  if (!is.null(offset)) { if (any(dd[[offset]] <= 0)) stop("Exposure must be positive"); dd$.lexp <- log(dd[[offset]]); rhs <- paste(rhs, "+ offset(.lexp)") }
  f <- stats::as.formula(paste(y, "~", rhs))
  fits <- list(); types <- list()
  fits$Poisson <- stats::glm(f, stats::poisson(), dd); types$Poisson <- "poisson"
  fits$`negative binomial` <- MASS::glm.nb(f, data = dd); types$`negative binomial` <- "negbin"
  fz <- stats::as.formula(paste(y, "~", rhs, "|", paste(zero_x, collapse = " + ")))
  for (z in zero) {
    fits[[z]] <- switch(z, zip = pscl::zeroinfl(fz, data = dd, dist = "poisson"), zinb = pscl::zeroinfl(fz, data = dd, dist = "negbin"),
                        hurdle_poisson = pscl::hurdle(fz, data = dd, dist = "poisson"), hurdle_nb = pscl::hurdle(fz, data = dd, dist = "negbin"),
                        stop("Unknown zero model: ", z))
    types[[z]] <- z
  }
  coefs <- do.call(rbind, lapply(names(fits), function(m) {
    ft <- fits[[m]]
    if (types[[m]] %in% c("poisson", "negbin")) {
      ct <- summary(ft)$coefficients; edu_wald(rownames(ct), ct[, 1], ct[, 2], expo = "ratio", model = m, part = "count (IRR)")
    } else {
      sc <- summary(ft)$coefficients
      rbind(edu_wald(rownames(sc$count), sc$count[, 1], sc$count[, 2], expo = "ratio", model = m, part = "count (IRR)"),
            edu_wald(rownames(sc$zero), sc$zero[, 1], sc$zero[, 2], expo = "ratio", model = m,
                     part = if (grepl("^hurdle", m)) "hurdle: P(y > 0) (OR)" else "zero inflation: P(structural 0) (OR)"))
    }
  }))
  coefs <- coefs[coefs$term != "Log(theta)", ]; rownames(coefs) <- NULL
  pz <- function(m) {
    ft <- fits[[m]]; mu <- stats::fitted(ft)
    switch(types[[m]], poisson = sum(stats::dpois(0, mu)), negbin = sum(stats::dnbinom(0, size = ft$theta, mu = mu)),
           sum(stats::predict(ft, type = "prob", at = 0:max(yy))[, 1]))
  }
  comp <- data.frame(model = names(fits), logLik = vapply(fits, function(m) as.numeric(stats::logLik(m)), 1),
                     df = vapply(fits, function(m) attr(stats::logLik(m), "df"), 1),
                     AIC = vapply(fits, stats::AIC, 1), BIC = vapply(fits, stats::BIC, 1),
                     theta = vapply(names(fits), function(m) if (!is.null(fits[[m]]$theta)) unname(fits[[m]]$theta) else NA_real_, 1),
                     zeros_observed = sum(yy == 0), zeros_predicted = vapply(names(fits), pz, 1), row.names = NULL)
  # overdispersion of the Poisson model
  pm <- fits$Poisson; mu <- stats::fitted(pm)
  aux <- ((yy - mu)^2 - yy) / mu; ct <- summary(stats::lm(aux ~ 0 + mu))$coefficients
  lrnb <- 2 * (as.numeric(stats::logLik(fits$`negative binomial`)) - as.numeric(stats::logLik(pm)))
  pear <- sum(stats::residuals(pm, type = "pearson")^2)
  od <- data.frame(test = c("Pearson chi2 / df (Poisson)", "Cameron-Trivedi (variance = mu + alpha*mu^2)", "LR test Poisson vs negative binomial"),
                   statistic = c(pear / pm$df.residual, ct[1, 3], lrnb), estimate = c(NA, ct[1, 1], NA),
                   p = c(NA, stats::pnorm(ct[1, 3], lower.tail = FALSE), 0.5 * stats::pchisq(max(lrnb, 0), 1, lower.tail = FALSE)))
  out <- list(comparison = comp, overdispersion = od, coefficients = coefs)
  pairs <- list()
  for (z in zero) pairs[[length(pairs) + 1]] <- c(if (grepl("nb$", z)) "negative binomial" else "Poisson", z)
  if (length(pairs)) out$vuong <- do.call(rbind, lapply(pairs, function(p) {
    m <- edu_count_ll(fits[[p[1]]], types[[p[1]]], yy) - edu_count_ll(fits[[p[2]]], types[[p[2]]], yy)
    n <- length(m); k1 <- attr(stats::logLik(fits[[p[1]]]), "df"); k2 <- attr(stats::logLik(fits[[p[2]]]), "df")
    adj <- c(0, k1 - k2, (k1 - k2) * log(n) / 2); zst <- (sum(m) - adj) / (sqrt(n) * stats::sd(m))
    data.frame(model1 = p[1], model2 = p[2], correction = c("raw", "AIC", "BIC"), z = zst,
               favours = ifelse(zst > 0, p[1], p[2]), p = stats::pnorm(-abs(zst)))
  }))
  out$notes <- c(sprintf("n = %d; %d zeros (%.1f%%).%s", length(yy), sum(yy == 0), 100 * mean(yy == 0),
                         if (is.null(offset)) "" else sprintf(" Offset = log(%s), so ratios are rate ratios per unit of exposure.", offset)),
                 "ratio = exp(B): incidence rate ratio (IRR) for count parts; odds ratio for zero-inflation / hurdle parts. Wald 95% CIs.",
                 "Overdispersion: Pearson chi2/df well above 1, a significant Cameron-Trivedi test (Cameron & Trivedi, 1990) or LR test (p halved: boundary) favours the negative binomial model; Poisson SEs are then too small.",
                 "Compare models by AIC/BIC and by how well they reproduce the observed number of zeros. Choose zero-inflated or hurdle models for a theoretical reason (a group that can never have the event, or a separate decision to start); the Vuong test is not a valid test of zero inflation itself (Wilson, 2015)." )
  out
}

# ================================================================ Bayes factors (BayesFactor)
edu_bf_label <- function(bf) {
  b <- ifelse(bf >= 1, bf, 1 / bf); side <- ifelse(bf >= 1, "H1", "H0")
  lev <- ifelse(b > 100, "extreme", ifelse(b > 30, "very strong", ifelse(b > 10, "strong", ifelse(b > 3, "moderate", ifelse(b > 1, "anecdotal", "no")))))
  ifelse(lev == "no", "no evidence either way", paste(lev, "evidence for", side))
}

edu_bf_rscale <- function(type, rscale) {
  if (is.numeric(rscale)) return(rscale)
  tab <- list(ttest = c(medium = sqrt(2) / 2, wide = 1, ultrawide = sqrt(2)), anova = c(medium = 1 / 2, wide = sqrt(2) / 2, ultrawide = 1),
              regression = c(medium = sqrt(2) / 4, wide = 1 / 2, ultrawide = sqrt(2) / 2), correlation = c(medium = 1 / 3, wide = 1 / sqrt(3), ultrawide = 1))
  unname(tab[[if (type == "paired") "ttest" else type]][rscale])
}

edu_bf_post <- function(chains, keep = NULL) {
  m <- as.matrix(chains); if (!is.null(keep)) m <- m[, intersect(keep, colnames(m)), drop = FALSE]
  data.frame(parameter = colnames(m), median = apply(m, 2, stats::median), mean = colMeans(m), sd = apply(m, 2, stats::sd),
             ci_low = apply(m, 2, stats::quantile, .025), ci_high = apply(m, 2, stats::quantile, .975), row.names = NULL)
}

edu_bayes <- function(d, type = c("ttest", "paired", "anova", "regression", "correlation"), y, x = NULL, group = NULL, id = NULL,
                      rscale = "medium", iterations = 10000, seed = 123) {
  # ttest: y + group (two independent groups); paired: y + group (two conditions) + id; anova: y + x (factors);
  # regression: y + x (numeric predictors); correlation: y + x (one variable).
  edu_need("BayesFactor"); type <- match.arg(type); r <- edu_bf_rscale(type, rscale); set.seed(seed)
  bft <- function(bf) { e <- BayesFactor::extractBF(bf); data.frame(model = rownames(e), BF10 = e$bf, BF01 = 1 / e$bf, error_pct = 100 * e$error,
                                                                   prior_scale = r, evidence = edu_bf_label(e$bf), row.names = NULL) }
  if (type %in% c("ttest", "paired")) {
    v <- suppressWarnings(as.numeric(d[[y]])); g <- factor(d[[group]]); ok <- !is.na(v) & !is.na(g); g <- droplevels(g)
    if (nlevels(g[ok]) != 2) stop("Needs exactly two groups or conditions")
    l <- levels(droplevels(g[ok]))
    if (type == "ttest") {
      a <- v[ok & g == l[1]]; b <- v[ok & g == l[2]]
      bf <- BayesFactor::ttestBF(x = a, y = b, rscale = r); n_txt <- sprintf("n = %d and %d", length(a), length(b))
      keep <- c("mu", "beta (x - y)", "delta", "sig2")
    } else {
      w <- merge(data.frame(id = d[[id]][ok & g == l[1]], a = v[ok & g == l[1]]), data.frame(id = d[[id]][ok & g == l[2]], b = v[ok & g == l[2]]), by = "id")
      bf <- BayesFactor::ttestBF(x = w$b, y = w$a, paired = TRUE, rscale = r); n_txt <- sprintf("%d complete pairs", nrow(w))
      keep <- c("mu", "delta", "sig2")
    }
    post <- edu_bf_post(BayesFactor::posterior(bf, iterations = iterations, progress = FALSE), keep)
    dirn <- if (type == "ttest") sprintf("delta = standardized difference %s minus %s", l[1], l[2]) else sprintf("delta = standardized mean of %s minus %s", l[2], l[1])
    note <- c(sprintf("JZS Bayes factor t test (Rouder et al., 2009), Cauchy prior on delta with scale r = %.3f; %s; %s.", r, n_txt, dirn))
  } else if (type == "correlation") {
    dd <- stats::na.omit(edu_num(d, c(y, x)))
    bf <- BayesFactor::correlationBF(dd[[1]], dd[[2]], rscale = r)
    utils::capture.output(ch <- suppressMessages(BayesFactor::posterior(bf, iterations = iterations, progress = FALSE))); post <- edu_bf_post(ch, "rho")
    note <- sprintf("Bayesian correlation (Ly et al., 2016), stretched beta prior with width r = %.3f; n = %d; sample r = %.3f.", r, nrow(dd), stats::cor(dd)[1, 2])
  } else {
    dd <- d[stats::complete.cases(d[c(y, x)]), c(y, x), drop = FALSE]; dd[[y]] <- as.numeric(dd[[y]])
    f <- stats::reformulate(x, response = y)
    if (type == "anova") {
      for (v in x) dd[[v]] <- factor(dd[[v]])
      bf <- BayesFactor::anovaBF(f, data = dd, rscaleFixed = r, progress = FALSE)
      note <- sprintf("Bayesian ANOVA (Rouder et al., 2012), fixed effects with prior scale r = %.3f; each model is compared with the intercept-only model; n = %d.", r, nrow(dd))
    } else {
      for (v in x) dd[[v]] <- as.numeric(dd[[v]])
      bf <- BayesFactor::regressionBF(f, data = dd, rscaleCont = r, progress = FALSE)
      note <- sprintf("Bayesian regression (Zellner-Siow / JZS prior, Liang et al., 2008), scale r = %.3f; all subsets of predictors compared with the intercept-only model; n = %d.", r, nrow(dd))
    }
    best <- bf[which.max(BayesFactor::extractBF(bf)$bf)]
    post <- edu_bf_post(BayesFactor::posterior(best, iterations = iterations, progress = FALSE))
    post <- post[!grepl("^(g_|g$)", post$parameter), ]
    note <- c(note, sprintf("Posterior summaries are for the model with the largest BF (%s).", rownames(BayesFactor::extractBF(best))))
  }
  res <- list(bayes_factors = bft(bf), posterior = post)
  if (type == "regression" && length(x) > 1) {
    full <- BayesFactor::lmBF(stats::reformulate(x, response = y), data = dd, rscaleCont = r, progress = FALSE)
    inc <- vapply(x, function(v) {
      red <- BayesFactor::lmBF(stats::reformulate(setdiff(x, v), response = y), data = dd, rscaleCont = r, progress = FALSE)
      BayesFactor::extractBF(full / red)$bf }, 1)
    res$predictor_bf <- data.frame(predictor = x, BF_full_vs_without = inc, evidence = edu_bf_label(inc), row.names = NULL)
    note <- c(note, "predictor_bf: full model versus the full model without that predictor (BF > 1 favours keeping it).")
  }
  res$notes <- c(note, sprintf("Posterior: %d MCMC iterations (seed %d); intervals are 95%% equal-tailed credible intervals.", iterations, seed),
                 "Evidence labels follow Jeffreys (1961) as adapted by Lee & Wagenmakers (2013): 1-3 anecdotal, 3-10 moderate, 10-30 strong, 30-100 very strong, > 100 extreme (BF01 = 1/BF10 for H0).",
                 "Bayes factors depend on the prior scale: report it, and report a robustness check with rscale = \"wide\" and \"ultrawide\". error_pct is the numerical error of the BF estimate.",
                 "A BF near 1 means the data do not discriminate between the hypotheses; it is not evidence for the null.")
  res
}
