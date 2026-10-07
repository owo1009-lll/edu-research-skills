# Known-answer checks for edu_methods_latent.R (LPA with mclust, LCA with poLCA, IRT with mirt).
# Relies only on check(), safely(), edu_methods.R and edu_methods_latent.R. Each block is skipped when its package is missing.
if (!exists("edu_lpa")) source(file.path(here, "..", "scripts", "edu_methods_latent.R"), encoding = "UTF-8")

if (all(vapply(c("mclust"), requireNamespace, logical(1), quietly = TRUE))) safely("LPA (mclust)", {
  # Published values: mclust vignette "A quick tour of mclust" (version 6.1.3), diabetes data with the
  # documented correction glucose[104] <- 455 (the column is named "insulin" in the installed data):
  # VVV,3 log-likelihood -2295.118, df 29, BIC -4734.561 (mclust sign), mixing .5553630/.2479432/.1966939;
  # mclustBootstrapLRT observed LRTS 1 vs 2 = 369.98537, 2 vs 3 = 121.10652, 3 vs 4 = 19.90071.
  X <- mclust::diabetes[, -1]; X$insulin[104] <- 455
  r <- edu_lpa(X, names(X), k = 1:4, models = "VVV", scale = FALSE, nboot = 19, choose_k = 3)
  f3 <- r$fit[r$fit$k == 3, ]
  check("LPA diabetes VVV,3 LL, npar, BIC (mclust vignette)", c(f3$LL, f3$npar, f3$BIC), c(-2295.118, 29, 4734.561), c(1e-3, 0, 1e-3))
  check("LPA diabetes mixing proportions (mclust vignette)", r$profile_sizes$model_share, c(0.5553630, 0.2479432, 0.1966939), 1e-6)
  check("LPA diabetes BLRT observed LRTS (mclust vignette)", r$fit$blrt_lrts[2:4], c(369.98537, 121.10652, 19.90071), 1e-4)
  check("LPA SABIC and AIC from LL (closed form)", c(f3$AIC, f3$SABIC), c(2 * 2295.118 + 2 * 29, 2 * 2295.118 + 29 * log(147 / 24)), 1e-2)
  # Invariant: three well-separated simulated profiles (means 3 SD apart, shares .5/.3/.2) are recovered.
  set.seed(2026); n <- 600; cl <- sample(1:3, n, TRUE, c(.5, .3, .2))
  mu <- rbind(c(0, 0, 0, 0), c(3, 3, 0, 0), c(0, 3, 3, 3))
  sim <- as.data.frame(mu[cl, ] + matrix(stats::rnorm(n * 4), n)); names(sim) <- paste0("y", 1:4)
  r <- edu_lpa(sim, names(sim), k = 1:5, nboot = 19)
  eei <- r$fit[r$fit$model == "EEI", ]
  check("LPA simulated: BIC minimum at k = 3 (EEI and VVI)", c(eei$k[which.min(eei$BIC)], with(r$fit[r$fit$model == "VVI", ], k[which.min(BIC)])), c(3, 3), 0)
  check("LPA simulated: provisional choice is k = 3", nrow(r$profile_sizes), 3, 0)
  check("LPA simulated: class shares equal realised shares", r$profile_sizes$model_share, as.numeric(sort(table(cl), decreasing = TRUE)) / n, 0.02)
  check("LPA simulated: raw profile means recover true means", as.matrix(r$profile_means[, -1]), t(mu), 0.2)
  check("LPA simulated: entropy > .90 and BLRT 2 vs 3 p = 1/20", c(r$fit$entropy[r$fit$model == "EEI" & r$fit$k == 3] > .90, r$fit$blrt_p[r$fit$model == "EEI" & r$fit$k == 3]), c(1, 0.05), c(0, 1e-12))
}) else message("skipped: LPA checks (package mclust not installed)")

if (all(vapply(c("poLCA"), requireNamespace, logical(1), quietly = TRUE))) safely("LCA (poLCA)", {
  # Published values: Linzer & Lewis (2011, J Stat Softw 42(10), section 5.1), carcinoma data.
  # 2 classes: AIC 664.5137... printed as 664.5, BIC 706.1; 3 classes: LL -293.705, 23 parameters, df 95,
  # AIC 633.41, BIC 697.1357, G2 15.26171, X2 20.50336, shares .3736/.1817/.4447; rater A positive in the
  # "problematic" class .5128; rater C positive in the "positive" class .8575.
  e <- new.env(); utils::data("carcinoma", package = "poLCA", envir = e)
  r <- edu_lca(e$carcinoma, LETTERS[1:7], k = 1:3)
  f2 <- r$fit[r$fit$k == 2, ]; f3 <- r$fit[r$fit$k == 3, ]
  check("LCA carcinoma 2-class AIC, BIC (Linzer & Lewis 2011)", c(f2$AIC, f2$BIC), c(664.5, 706.1), 0.05)
  check("LCA carcinoma 3-class LL, npar, df, AIC, BIC (Linzer & Lewis 2011)", c(f3$LL, f3$npar, f3$df, f3$AIC, f3$BIC),
        c(-293.705, 23, 95, 633.41, 697.1357), c(1e-3, 0, 0, 1e-2, 1e-3))
  check("LCA carcinoma 3-class G2, X2 (Linzer & Lewis 2011)", c(f3$G2, f3$X2), c(15.26171, 20.50336), 1e-3)
  check("LCA carcinoma class shares, ordered by size (Linzer & Lewis 2011)", r$class_sizes$model_share, c(.4447, .3736, .1817), 1e-4)
  ip <- r$item_probabilities
  check("LCA carcinoma item probabilities (A in C3, C in C1)", c(ip$C3[ip$item == "A" & ip$category == "2"], ip$C1[ip$item == "C" & ip$category == "2"]), c(.5128, .8575), 1e-4)
  # Invariant: three simulated classes (shares .5/.3/.2, 8 binary items with response probabilities .85/.15) are recovered.
  set.seed(7); n <- 1500; cl <- sample(1:3, n, TRUE, c(.5, .3, .2))
  P <- rbind(rep(.85, 8), c(rep(.85, 4), rep(.15, 4)), rep(.15, 8))
  sim <- as.data.frame(matrix(stats::rbinom(n * 8, 1, P[cl, ]), n)); names(sim) <- paste0("u", 1:8)
  r <- edu_lca(sim, names(sim), k = 1:4, nrep = 5)
  check("LCA simulated: BIC minimum at k = 3", r$fit$k[which.min(r$fit$BIC)], 3, 0)
  check("LCA simulated: class shares equal realised shares", r$class_sizes$model_share, as.numeric(table(cl)) / n, 0.03)
  ip <- r$item_probabilities[r$item_probabilities$category == "1", c("C1", "C2", "C3")]
  check("LCA simulated: P(item = 1 | class) recovers the generating table", t(as.matrix(ip)), P, 0.06)
}) else message("skipped: LCA checks (package poLCA not installed)")

if (all(vapply(c("mirt"), requireNamespace, logical(1), quietly = TRUE))) safely("IRT (mirt)", {
  # Published values: Rizopoulos (2006, J Stat Softw 17(5), pp. 10-11), LSAT data (= mirt::LSAT6, Bock & Lieberman 1970).
  # Unconstrained Rasch (common discrimination .7551, SD(theta) = 1): log-likelihood -2466.938, difficulties
  # -3.6153, -1.3224, -0.3176, -1.7301, -2.7802; 2PL log-likelihood -2466.65; LRT 0.57, df 4, p = .967.
  # mirt's Rasch fixes a = 1 and frees var(theta), so sqrt(theta_var) = .7551 and b / sqrt(theta_var) = ltm difficulty.
  # ltm uses 21 Gauss-Hermite points and mirt 61 quadrature points, hence the .01 tolerance on parameters.
  L6 <- mirt::expand.table(mirt::LSAT6)
  r <- edu_irt(L6, names(L6), "Rasch", scores = TRUE)
  check("Rasch LSAT log-likelihood (Rizopoulos 2006)", r$model_fit$LL, -2466.938, 1e-2)
  s <- sqrt(r$model_fit$theta_var)
  check("Rasch LSAT common discrimination (Rizopoulos 2006)", s, 0.7551, 0.01)
  check("Rasch LSAT difficulties in SD(theta) = 1 metric (Rizopoulos 2006)", r$item_parameters$b / s, c(-3.6153, -1.3224, -0.3176, -1.7301, -2.7802), 0.01)
  mc <- r$model_comparison
  check("Rasch vs 2PL LRT (Rizopoulos 2006: 2PL LL -2466.65, LRT 0.57, df 4, p .967)", c(mc$LL[2], mc$LR_chi2[2], mc$df[2], mc$p[2]),
        c(-2466.65, 0.57, 4, 0.967), c(1e-2, 1e-2, 0, 1e-3))
  # Closed-form Rasch properties: the sum score is sufficient, so persons with equal sum scores get identical EAP
  # scores, and item difficulties order exactly as the proportions correct (reversed).
  sc <- r$scores; ss <- rowSums(L6)[sc$row]
  check("Rasch EAP is a function of the sum score", max(tapply(sc$theta_EAP, ss, function(v) diff(range(v)))), 0, 1e-8)
  check("Rasch difficulty order = reverse order of proportion correct", rank(r$item_parameters$b), rank(-colMeans(L6)), 0)
  check("item fit table has S-X2 with RMSEA for every item", as.numeric(nrow(r$item_fit) == 5 && all(!is.na(r$item_fit$RMSEA))), 1, 0)
  # Invariant: simulated 2PL (N = 3000) and graded (N = 2000) parameters are recovered.
  a <- c(.8, 1, 1.2, 1.5, 2, .7, 1.3, 1.8, 1, 1.1); b <- seq(-1.5, 1.5, length.out = 10)
  set.seed(11); sim <- as.data.frame(mirt::simdata(matrix(a), matrix(-a * b), 3000, itemtype = "2PL"))
  r <- edu_irt(sim, names(sim), "2PL")
  check("2PL simulated: discriminations recovered", r$item_parameters$a, a, 0.2)
  check("2PL simulated: difficulties recovered", r$item_parameters$b, b, 0.15)
  check("2PL simulated: Rasch vs 2PL LRT rejects equal slopes", as.numeric(r$model_comparison$p[2] < .001), 1, 0)
  ag <- c(1, 1.4, 1.8, 2.2, 1.2, 1.6); bg <- outer(c(-.6, -.3, 0, .3, .6, 0), c(-1.5, 0, 1.5), "+")
  set.seed(12); simg <- as.data.frame(mirt::simdata(matrix(ag), -ag * bg, 2000, itemtype = "graded"))
  r <- edu_irt(simg, names(simg), "graded")
  ip <- r$item_parameters  # recovery judged as |estimate - true| / SE <= 3 (extreme thresholds have large SEs)
  check("GRM simulated: discriminations recovered (|z| <= 3)", abs(ip$a - ag) / ip$SE_a, 0, 3)
  check("GRM simulated: thresholds recovered (|z| <= 3)", abs(as.matrix(ip[, c("b1", "b2", "b3")]) - bg) / as.matrix(ip[, c("SE_b1", "SE_b2", "SE_b3")]), 0, 3)
  check("GRM simulated: reliabilities within (0, 1)", as.numeric(with(r$model_fit, marginal_rxx > 0 & marginal_rxx < 1 & empirical_rxx > 0 & empirical_rxx < 1)), 1, 0)
}) else message("skipped: IRT checks (package mirt not installed)")
