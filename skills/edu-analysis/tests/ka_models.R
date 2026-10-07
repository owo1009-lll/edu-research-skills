# Known-answer checks for edu_methods_models.R (meta-analysis, ordinal, multinomial, count, Bayes factors).
# Appended to known_answers.R: uses check(), safely() and the functions from edu_methods.R / edu_methods_models.R.
have <- function(p) all(vapply(p, requireNamespace, logical(1), quietly = TRUE))

if (have(c("metafor", "metadat"))) safely("meta-analysis", {
  bcg <- metadat::dat.bcg
  r <- edu_meta(bcg, "RR", ai = "tpos", bi = "tneg", ci = "cpos", di = "cneg", moderators = "ablat")
  # Viechtbauer (2010, J Stat Softw 36(3)) and the metafor documentation (?rma, dat.bcg):
  # log RR = -0.7145, tau^2 = 0.3132, I^2 = 92.22%, H^2 = 12.86, Q(12) = 152.2330
  check("RE pooled log RR, tau2, I2, H2, Q (dat.bcg)", c(r$pooled$estimate, r$heterogeneity$tau2, r$heterogeneity$I2_pct, r$heterogeneity$H2, r$heterogeneity$Q),
        c(-0.7145, 0.3132, 92.22, 12.86, 152.2330), c(1e-4, 1e-4, 1e-2, 1e-2, 1e-3))
  # prediction interval, closed form: estimate +/- z * sqrt(tau2 + SE^2)
  p <- r$pooled; h <- sqrt(r$heterogeneity$tau2 + p$SE^2) * qnorm(.975)
  check("prediction interval equals mu +/- z*sqrt(tau2 + SE^2)", c(p$pi_low, p$pi_high), p$estimate + c(-h, h), 1e-8)
  # same sources: mixed-effects model with absolute latitude: b0 = 0.2515, b1 = -0.0291, tau^2 = 0.0764, QM(1) = 16.3571
  check("meta-regression on ablat (dat.bcg)", c(r$moderators$estimate, r$moderator_test$tau2_residual, r$moderator_test$QM),
        c(0.2515, -0.0291, 0.0764, 16.3571), c(1e-4, 1e-4, 1e-4, 1e-3))
  # Hedges' g, closed form: g = J * d, J = Gamma(m/2) / (sqrt(m/2) Gamma((m-1)/2)), m = n1 + n2 - 2; vi = 1/n1 + 1/n2 + g^2 / (2(n1 + n2))
  s <- data.frame(m1 = c(10, 12), s1 = c(2, 3), n1 = c(20, 15), m2 = c(9, 11), s2 = c(2.5, 2), n2 = c(25, 18))
  r <- edu_meta(s, "SMD", m1i = "m1", sd1i = "s1", n1i = "n1", m2i = "m2", sd2i = "s2", n2i = "n2")$effects
  sp <- sqrt(((s$n1 - 1) * s$s1^2 + (s$n2 - 1) * s$s2^2) / (s$n1 + s$n2 - 2)); m <- s$n1 + s$n2 - 2
  g <- exp(lgamma(m / 2) - log(sqrt(m / 2)) - lgamma((m - 1) / 2)) * (s$m1 - s$m2) / sp
  check("Hedges' g and its variance equal the closed form", c(r$yi, r$vi), c(g, 1 / s$n1 + 1 / s$n2 + g^2 / (2 * (s$n1 + s$n2))), 1e-10)
  # Fisher z, closed form: z = atanh(r), v = 1/(n - 3); pooled estimate back-transformed with tanh
  cr <- data.frame(r = c(.3, .45, .2, .5), n = c(50, 80, 120, 40))
  r <- edu_meta(cr, "ZCOR", ri = "r", ni = "n", method = "FE")
  w <- cr$n - 3; zbar <- sum(w * atanh(cr$r)) / sum(w)
  check("ZCOR: yi = atanh(r), vi = 1/(n-3), FE pooled r = tanh(weighted z)", c(r$effects$yi, r$effects$vi, r$pooled$estimate_back),
        c(atanh(cr$r), 1 / (cr$n - 3), tanh(zbar)), 1e-10)
  # leave-one-out under the fixed-effect model, closed form: inverse-variance mean of the remaining studies
  check("leave-one-out (FE) equals inverse-variance mean without study 1", r$leave_one_out$estimate[1], sum(w[-1] * atanh(cr$r[-1])) / sum(w[-1]), 1e-10)
  # Egger (1997): regress the standard normal deviate y/SE on precision 1/SE; the intercept t is the asymmetry test
  dd <- metafor::escalc("RR", ai = tpos, bi = tneg, ci = cpos, di = cneg, data = bcg)
  eg <- summary(lm(I(yi / sqrt(vi)) ~ I(1 / sqrt(vi)), dd))$coefficients
  r <- edu_meta(bcg, "RR", ai = "tpos", bi = "tneg", ci = "cpos", di = "cneg")$publication_bias
  check("Egger test equals the intercept t of Egger's regression", c(r$statistic[1], r$p[1]), c(eg[1, 3], eg[1, 4]), 1e-8)
  # invariant: a perfectly symmetric funnel needs no imputed studies
  sym <- data.frame(yi = 0.3 + c(-.4, .4, -.2, .2, -.1, .1, -.3, .3), vi = c(.10, .10, .04, .04, .02, .02, .08, .08))
  check("trim-and-fill imputes 0 studies for a symmetric funnel", edu_meta(sym, yi = "yi", vi = "vi")$publication_bias$statistic[2], 0, 0)
  # metafor documentation for dat.konstantopoulos2011 (three-level model, schools in districts):
  # estimate = 0.1847, sigma^2 (district) = 0.0651, sigma^2 (school within district) = 0.0327
  r <- edu_meta(metadat::dat.konstantopoulos2011, yi = "yi", vi = "vi", study_id = "district")$three_level
  check("three-level model (dat.konstantopoulos2011)", r$value[1:3], c(0.1847, 0.0651, 0.0327), c(1e-4, 1e-4, 1e-4))
  check("three-level variance shares sum to 100%", sum(r$variance_pct, na.rm = TRUE), 100, 1e-8)
  f <- edu_meta_plot(bcg, "RR", ai = "tpos", bi = "tneg", ci = "cpos", di = "cneg", label = "author", file = file.path(tempdir(), "meta_test"))
  check("forest and funnel plot files written", as.numeric(all(file.exists(f) & file.size(f) > 1000)), 1, 0)
}) else message("skipped: meta-analysis (needs metafor, metadat)")

if (have(c("ordinal", "MASS"))) safely("ordinal logistic regression", {
  r <- edu_ordinal(MASS::housing, "Sat", c("Infl", "Type", "Cont"), weights = "Freq")
  # Venables & Ripley (2002, MASS 4th ed., section 7.3) and ?polr, housing data:
  # coefficients 0.5664, 1.2888, -0.5724, -0.3662, -1.0910, 0.3603; thresholds -0.4961, 0.6907; residual deviance 3479.149
  check("cumulative logit coefficients (housing)", r$coefficients$B, c(0.5664, 1.2888, -0.5724, -0.3662, -1.0910, 0.3603), 1e-4)
  check("thresholds and deviance (housing)", c(r$thresholds$estimate, r$fit$deviance), c(-0.4961, 0.6907, 3479.149), c(1e-4, 1e-4, 1e-3))
  # closed-form equivalence: with two outcome categories the cumulative logit model is binary logistic regression
  m <- datasets::mtcars; ro <- edu_ordinal(m, "am", c("wt", "hp"))
  check("two-category ordinal B equals glm logistic B", ro$coefficients$B, coef(glm(am ~ wt + hp, binomial, m))[-1], 1e-4)
  # invariant: data generated under proportional odds pass the test; data whose x effect reverses across thresholds fail it
  set.seed(11); n <- 2000; x <- rnorm(n)
  ypo <- cut(0.8 * x + rlogis(n), c(-Inf, -1, 0, 1, Inf), labels = FALSE)
  u <- runif(n); ynp <- ifelse(u < plogis(-1 - 1.2 * x), 1, ifelse(u < plogis(1), 2, 3))  # slope -1.2 at threshold 1, 0 at threshold 2
  p1 <- edu_ordinal(data.frame(y = ypo, x = x), "y", "x")$proportional_odds$p[1]
  p2 <- edu_ordinal(data.frame(y = ynp, x = x), "y", "x")$proportional_odds$p[1]
  check("PO test: p > .05 under PO, p < .001 when the slope differs by threshold", as.numeric(c(p1 > .05, p2 < .001)), c(1, 1), 0)
}) else message("skipped: ordinal logistic regression (needs ordinal, MASS)")

if (have("nnet")) safely("multinomial logistic regression", {
  # closed-form equivalence: with two outcome categories, multinomial logit = binary logistic regression
  m <- datasets::mtcars; r <- edu_multinom(m, "am", c("wt", "hp"), ref = "0")
  g <- summary(glm(am ~ wt + hp, binomial, m))$coefficients
  check("two-category multinom B and SE equal glm", c(r$coefficients$B, r$coefficients$SE), c(g[, 1], g[, 2]), 1e-3)
  # closed form for a saturated model (one categorical predictor): RRR = cross-ratio of cell counts, and
  # McFadden R2 = 1 - LL/LL0 with LL = sum n_ij log(n_ij / n_i.) and LL0 = sum n_.j log(n_.j / n)
  tab <- matrix(c(30, 20, 10, 15, 25, 40), 2, byrow = TRUE, dimnames = list(c("g0", "g1"), c("A", "B", "C")))
  d <- as.data.frame(as.table(tab)); names(d) <- c("x", "y", "Freq")
  r <- edu_multinom(d, "y", "x", ref = "A", weights = "Freq")
  rrr <- r$coefficients$RRR[r$coefficients$term == "xg1"]
  want <- c((tab[2, 2] / tab[2, 1]) / (tab[1, 2] / tab[1, 1]), (tab[2, 3] / tab[2, 1]) / (tab[1, 3] / tab[1, 1]))
  ll <- sum(tab * log(tab / rowSums(tab))); ll0 <- sum(colSums(tab) * log(colSums(tab) / sum(tab)))
  check("saturated multinom: RRR = cell cross-ratios, McFadden R2 closed form", c(rrr, r$fit$McFadden_R2), c(want, 1 - ll / ll0), c(1e-4, 1e-4, 1e-6))
}) else message("skipped: multinomial logistic regression (needs nnet)")

if (have(c("MASS", "pscl"))) safely("count models", {
  bc <- pscl::bioChemists; xs <- c("fem", "mar", "kid5", "phd", "ment")
  r <- edu_count(bc, "art", xs, zero = c("zip", "zinb"))
  cf <- r$coefficients; pick <- function(m, part) cf$B[cf$model == m & grepl(part, cf$part)]
  # Zeileis, Kleiber & Jackman (2008, J Stat Softw 27(8); pscl vignette "countreg"), bioChemists:
  # Poisson: 0.3046, -0.2246, 0.1552, -0.1849, 0.0128, 0.0255; logLik -1651.1
  check("Poisson coefficients and logLik (bioChemists)", c(pick("Poisson", "count"), r$comparison$logLik[1]),
        c(0.3046, -0.2246, 0.1552, -0.1849, 0.0128, 0.0255, -1651.1), c(rep(1e-4, 6), 0.1))
  # same source: negative binomial theta = 2.264, logLik -1561.0
  check("NB theta and logLik (bioChemists)", c(r$comparison$theta[2], r$comparison$logLik[2]), c(2.264, -1561.0), c(1e-3, 0.1))
  # same source: ZIP count part 0.6408, -0.2091, 0.1038, -0.1433, -0.0062, 0.0181; logLik -1605 (12 df); ZINB logLik -1550 (13 df)
  check("ZIP count coefficients (bioChemists)", pick("zip", "count"), c(0.6408, -0.2091, 0.1038, -0.1433, -0.0062, 0.0181), 1e-4)
  check("ZIP and ZINB logLik and df", c(r$comparison$logLik[3:4], r$comparison$df[3:4]), c(-1605, -1550, 12, 13), c(0.5, 0.5, 0, 0))
  # plumbing: Vuong statistics equal those printed by pscl::vuong(glm.nb, zeroinfl negbin) (raw, AIC, BIC)
  check("Vuong NB vs ZINB equals pscl::vuong", r$vuong$z[r$vuong$model2 == "zinb"], c(-2.241831, -1.015385, 1.939690), 1e-5)
  # closed form: Poisson with one binary predictor and log-exposure offset; IRR = ratio of the two group rates
  d <- data.frame(y = c(3, 5, 2, 8, 9, 12, 7, 10), g = rep(0:1, each = 4), t = c(10, 12, 8, 15, 11, 14, 9, 13))
  irr <- with(d, (sum(y[g == 1]) / sum(t[g == 1])) / (sum(y[g == 0]) / sum(t[g == 0])))
  r <- edu_count(d, "y", "g", offset = "t")$coefficients
  check("Poisson IRR with exposure offset equals ratio of group rates", r$ratio[r$model == "Poisson" & r$term == "g"], irr, 1e-6)
  # invariant: Cameron-Trivedi test does not flag Poisson data and flags negative binomial data
  set.seed(5); n <- 1000; x <- rnorm(n); mu <- exp(0.5 + 0.4 * x)
  p0 <- edu_count(data.frame(y = rpois(n, mu), x = x), "y", "x")$overdispersion$p[2]
  p1 <- edu_count(data.frame(y = rnbinom(n, size = 1, mu = mu), x = x), "y", "x")$overdispersion$p[2]
  check("overdispersion test: p > .05 for Poisson data, p < .001 for NB data", as.numeric(c(p0 > .05, p1 < .001)), c(1, 1), 0)
}) else message("skipped: count models (needs MASS, pscl)")

if (have("BayesFactor")) safely("Bayes factors", {
  s <- datasets::sleep
  # BayesFactor documentation (?ttestBF, sleep data, paired): BF10 = 17.25888 with r = 0.707
  r <- edu_bayes(s, "paired", "extra", group = "group", id = "ID", iterations = 2000)
  check("paired JZS BF10 (sleep, BayesFactor docs)", r$bayes_factors$BF10, 17.25888, 1e-4)
  # closed form: JZS Bayes factor as a one-dimensional integral over g (Rouder et al., 2009, eq. 1)
  jzs <- function(t, N, nu, rs) {
    f <- function(g) (1 + N * g * rs^2)^(-1/2) * (1 + t^2 / ((1 + N * g * rs^2) * nu))^(-(nu + 1) / 2) * (2 * pi)^(-1/2) * g^(-3/2) * exp(-1 / (2 * g))
    integrate(f, 0, Inf)$value / (1 + t^2 / nu)^(-(nu + 1) / 2)
  }
  tt <- t.test(extra ~ group, s, var.equal = TRUE)$statistic
  r <- edu_bayes(s, "ttest", "extra", group = "group", iterations = 2000)
  check("independent JZS BF10 equals the Rouder integral", r$bayes_factors$BF10, jzs(tt, 10 * 10 / 20, 18, sqrt(2) / 2), 1e-4)
  # invariant (Rouder et al., 2012): with two groups, anovaBF (r = 1/2) equals ttestBF (r = sqrt(2)/2)
  check("two-group Bayesian ANOVA equals the t-test BF", edu_bayes(s, "anova", "extra", "group", iterations = 1000)$bayes_factors$BF10, r$bayes_factors$BF10, 1e-3)
  # closed form: Zellner-Siow BF for one predictor (Liang et al., 2008; Rouder & Morey, 2012),
  # g ~ InvGamma(1/2, r^2 N / 2), BF = int (1+g)^((N-p-1)/2) (1+g(1-R2))^(-(N-1)/2) p(g) dg
  m <- datasets::mtcars; N <- nrow(m); R2 <- summary(lm(mpg ~ wt, m))$r.squared; rs <- sqrt(2) / 4; b <- rs^2 * N / 2
  zs <- integrate(function(g) exp((N - 2) / 2 * log1p(g) - (N - 1) / 2 * log1p(g * (1 - R2)) + 0.5 * log(b) - lgamma(0.5) - 1.5 * log(g) - b / g), 0, Inf)$value
  r <- edu_bayes(m, "regression", "mpg", "wt", iterations = 2000)
  check("regression BF10 equals the Zellner-Siow integral (relative)", r$bayes_factors$BF10 / zs, 1, 1e-3)
  check("posterior slope near OLS for a single predictor", r$posterior$median[r$posterior$parameter == "wt"], coef(lm(mpg ~ wt, m))[["wt"]], 0.3)
  # invariant: with n = 500 the posterior rho sits next to the sample r and the BF is decisive
  set.seed(3); x <- rnorm(500); y <- 0.4 * x + rnorm(500)
  r <- edu_bayes(data.frame(x = x, y = y), "correlation", "y", "x", iterations = 2000)
  check("correlation posterior median near sample r, BF > 100", c(abs(r$posterior$median - cor(x, y)) < .02, r$bayes_factors$BF10 > 100), c(1, 1), 0)
  check("evidence labels (Lee & Wagenmakers, 2013)", as.numeric(edu_bf_label(c(17.26, 1 / 5, 1.5, 150)) ==
        c("strong evidence for H1", "moderate evidence for H0", "anecdotal evidence for H1", "extreme evidence for H1")), rep(1, 4), 0)
}) else message("skipped: Bayes factors (needs BayesFactor)")
