# quasi-experimental designs (edu_methods_causal.R): PSM, DID, event study, RDD
if (!exists("edu_psm")) source(file.path(here, "..", "scripts", "edu_methods_causal.R"), encoding = "UTF-8")
if (all(vapply(c("MatchIt", "cobalt", "sandwich"), requireNamespace, logical(1), quietly = TRUE))) safely("PSM", {
  # Published: MatchIt vignette "MatchIt: Getting Started" (Greifer), lalonde, logistic PS, 1:1 nearest neighbour
  # without replacement, no caliper: summary(m.out0) and summary(m.out1, un = FALSE).
  r <- edu_psm(MatchIt::lalonde, "treat", c("age", "educ", "race", "married", "nodegree", "re74", "re75"), "re78",
               link = "logit", caliper = NULL)
  b <- r$balance; g <- function(v, col) b[[col]][b$variable == v]
  check("lalonde SMD before (age, educ, re74, re75, race_black)", c(g("age", "smd_before"), g("educ", "smd_before"), g("re74", "smd_before"), g("re75", "smd_before"), g("race_black", "smd_before")),
        c(-0.3094, 0.0550, -0.7211, -0.2903, 1.7615), 1e-4)
  check("lalonde variance ratio before (age, re74)", c(g("age", "var_ratio_before"), g("re74", "var_ratio_before")), c(0.4400, 0.5181), 1e-4)
  check("lalonde SMD after NN matching (age, educ, re74, re75, race_black)", c(g("age", "smd_after"), g("educ", "smd_after"), g("re74", "smd_after"), g("re75", "smd_after"), g("race_black", "smd_after")),
        c(0.0718, -0.1290, -0.0505, -0.0257, 1.0259), 1e-4)
  check("lalonde variance ratio after (re74, re75)", c(g("re74", "var_ratio_after"), g("re75", "var_ratio_after")), c(1.3289, 1.4956), 1e-4)
  s <- r$sample_sizes
  check("lalonde sample sizes (matched control/treated, unmatched control)",
        c(s$control[s$sample == "Matched"], s$treated[s$sample == "Matched"], s$control[s$sample == "Unmatched"]), c(185, 185, 244), 0)
  # Plumbing: matched effect equals the weighted lm on match_data, SE equals sandwich::vcovCL by subclass
  m <- MatchIt::matchit(treat ~ age + educ + race + married + nodegree + re74 + re75, data = MatchIt::lalonde)
  md <- MatchIt::match_data(m); fit <- stats::lm(re78 ~ treat, md, weights = weights)
  e <- r$effects[2, ]
  check("matched effect and pair-clustered SE equal lm + vcovCL", c(e$estimate, e$SE),
        c(stats::coef(fit)[["treat"]], sqrt(sandwich::vcovCL(fit, cluster = md$subclass, type = "HC1")["treat", "treat"])), 1e-8)
  # Known effect: simulated confounding with constant treatment effect 2 (ATT = 2); naive difference is biased.
  set.seed(2026); n <- 3000; x1 <- stats::rnorm(n); x2 <- stats::rnorm(n)
  tr <- stats::rbinom(n, 1, stats::plogis(-0.7 + 0.8 * x1 + 0.5 * x2))
  sim <- data.frame(tr, x1, x2, y = 1 + 2 * tr + 1.5 * x1 + 1 * x2 + stats::rnorm(n))
  r <- edu_psm(sim, "tr", c("x1", "x2"), "y")
  check("simulated ATT = 2 recovered (matched; matched + covariates)", r$effects$estimate[2:3], c(2, 2), c(0.2, 0.1))
  check("naive difference biased (> 0.8 away from 2), CI of adjusted estimate covers 2",
        as.numeric(c(abs(r$effects$estimate[1] - 2) > 0.8, r$effects$ci_low[3] < 2 & r$effects$ci_high[3] > 2)), c(1, 1), 0)
  check("all covariates balanced after caliper matching", as.numeric(all(r$balance$smd_ok[-1] == "yes")), 1, 0)
}) else message("skipped: PSM (needs MatchIt, cobalt, sandwich)")

if (all(vapply(c("sandwich"), requireNamespace, logical(1), quietly = TRUE))) safely("DID 2x2", {
  # Closed form: DID = (treated post - treated pre) - (control post - control pre). Cell means set to Card & Krueger
  # (1994, Table 3, FTE employment): NJ 20.44 -> 21.03, PA 23.33 -> 21.17; (0.59) - (-2.16) = 2.75
  # (the paper prints 2.76 from unrounded means).
  mk <- function(m, tr, po) data.frame(fte = m + c(-2, -1, 0, 1, 2), nj = tr, post = po, store = paste0(tr, "_", 1:5))
  ck <- rbind(mk(20.44, 1, 0), mk(21.03, 1, 1), mk(23.33, 0, 0), mk(21.17, 0, 1))
  r <- edu_did(ck, "fte", "nj", "post")
  check("2x2 DID equals difference of four means (Card & Krueger cell means)", c(r$did$four_mean_did, r$did$estimate), c(2.75, 2.75), 1e-8)
  # Known effect: panel of 400 units x 2 periods, group gap and common trend, true effect 3 (parallel trends hold).
  set.seed(7); u <- 400; a <- stats::rnorm(u); tr <- rep(0:1, each = u / 2)
  p <- data.frame(id = rep(1:u, 2), tr = rep(tr, 2), post = rep(0:1, each = u))
  p$y <- 10 + 2 * p$tr + rep(a, 2) + 1.5 * p$post + 3 * p$tr * p$post + stats::rnorm(2 * u)
  r <- edu_did(p, "y", "tr", "post", cluster = "id")
  check("simulated DID = 3 recovered; CI covers 3", c(r$did$estimate, as.numeric(r$did$ci_low < 3 & r$did$ci_high > 3)), c(3, 1), c(0.25, 0))
  fit <- stats::lm(y ~ tr * post, p)
  check("clustered SE equals sandwich::vcovCL (HC1)", r$did$SE, sqrt(sandwich::vcovCL(fit, cluster = p$id, type = "HC1")["tr:post", "tr:post"]), 1e-8)
}) else message("skipped: DID 2x2 (needs sandwich)")

if (all(vapply(c("fixest"), requireNamespace, logical(1), quietly = TRUE))) safely("event study", {
  # Known dynamic effects, single adoption at t = 6 (of 10) for half the units, parallel trends by construction:
  # leads are 0, lags are 1, 2, 3, 4, 5 for rel_time 0..4.
  set.seed(11); u <- 300; Tn <- 10
  p <- expand.grid(t = 1:Tn, id = 1:u); a <- stats::rnorm(u); tr <- rep(0:1, length.out = u)
  p$g <- ifelse(tr[p$id] == 1, 6, NA); rel <- p$t - p$g
  p$y <- a[p$id] + 0.3 * p$t + ifelse(!is.na(rel) & rel >= 0, rel + 1, 0) + stats::rnorm(nrow(p), sd = 0.1)
  r <- edu_did_event(p, "y", "id", "t", treat_time = "g")$event_study
  check("leads equal 0 (rel -5..-2)", r$estimate[r$rel_time %in% -5:-2], rep(0, 4), 0.05)
  check("lags equal true dynamic effects 1..5 (rel 0..4)", r$estimate[r$rel_time %in% 0:4], 1:5, 0.05)
  # Staggered adoption with cohort-specific effects (cohort 4: 2 + rel; cohort 7: 0.5 * (1 + rel)), never-treated
  # group. Sun & Abraham target at each rel_time = cohort-share-weighted mean of the true effects; overall ATT = mean
  # of the true effects over treated post-treatment observations.
  set.seed(12); u <- 600
  p <- expand.grid(t = 1:Tn, id = 1:u); a <- stats::rnorm(u); coh <- rep(c(4, 7, NA), length.out = u)
  p$g <- coh[p$id]; rel <- p$t - p$g
  tau <- ifelse(is.na(rel) | rel < 0, 0, ifelse(p$g == 4, 2 + rel, 0.5 * (1 + rel)))
  p$y <- a[p$id] + 0.2 * p$t + tau + stats::rnorm(nrow(p), sd = 0.1)
  r <- edu_did_event(p, "y", "id", "t", treat_time = "g")
  sa <- r$event_study[r$event_study$estimator == "Sun & Abraham", ]
  truth <- tapply(tau[!is.na(rel) & rel >= 0], rel[!is.na(rel) & rel >= 0], mean)
  check("Sun & Abraham lags equal the true weighted effects", sa$estimate[sa$rel_time >= 0], unname(truth[as.character(sa$rel_time[sa$rel_time >= 0])]), 0.05)
  check("Sun & Abraham leads equal 0", sa$estimate[sa$rel_time < -1], rep(0, sum(sa$rel_time < -1)), 0.05)
  tw <- r$event_study[r$event_study$estimator == "TWFE event study", ]
  check("TWFE leads are contaminated by cohort heterogeneity (max |lead| > 0.5), as Sun & Abraham (2021) show", as.numeric(max(abs(tw$estimate[tw$rel_time < -1])) > 0.5), 1, 0)
  check("Sun & Abraham overall ATT equals mean true effect", r$overall_att$estimate, mean(tau[!is.na(rel) & rel >= 0]), 0.05)
  r2 <- edu_did_event(p, "y", "id", "t", treat_time = "g", sunab = FALSE)
  check("rel_time input gives the same TWFE estimates as treat_time",
        edu_did_event(transform(p, rr = t - g), "y", "id", "t", rel_time = "rr", sunab = FALSE)$event_study$estimate,
        r2$event_study$estimate, 1e-10)
}) else message("skipped: event study (needs fixest)")

if (all(vapply(c("rdrobust"), requireNamespace, logical(1), quietly = TRUE))) safely("RDD", {
  e <- new.env(); utils::data("rdrobust_RDsenate", package = "rdrobust", envir = e); sen <- e$rdrobust_RDsenate
  # Published: rdrobust vignette "rdrobust-new-features" (v4.0.0), U.S. Senate data: default rdrobust(vote, margin)
  # conventional 7.414, bias-corrected 7.507.
  r <- edu_rdd(sen, "vote", "margin", 0)$estimate
  check("Senate RD (conventional, bias-corrected)", c(r$estimate, r$bias_corrected), c(7.414, 7.507), 5e-4)
  # Same vignette, cluster = state, vce = "cr3": estimate 7.386, robust CI [3.916, 11.072], h = 18.259, eff. N 369 / 328.
  r <- edu_rdd(sen, "vote", "margin", 0, cluster = "state", vce = "cr3")$estimate
  check("Senate RD, CR3 by state (estimate, robust CI, h)", c(r$estimate, r$robust_ci_low, r$robust_ci_high, r$h_left), c(7.386, 3.916, 11.072, 18.259), 5e-4)
  check("Senate RD, CR3 effective N left/right", c(r$eff_n_left, r$eff_n_right), c(369, 328), 0)
  # Closed form: uniform kernel, p = 1, fixed h -> conventional estimate = difference of the intercepts of
  # separate OLS lines fitted within h on each side.
  set.seed(5); n <- 4000; x <- stats::runif(n, -1, 1); z <- stats::rnorm(n)
  y <- 0.5 + 0.8 * x + 0.5 * (x >= 0) + 0.3 * x^2 + stats::rnorm(n, sd = 0.3)
  s <- data.frame(y, x, z); hh <- 0.4
  r <- edu_rdd(s, "y", "x", 0, kernel = "uniform", h = hh)$estimate
  L <- stats::coef(stats::lm(y ~ x, s, subset = x < 0 & x >= -hh))[1]; R <- stats::coef(stats::lm(y ~ x, s, subset = x >= 0 & x <= hh))[1]
  check("uniform-kernel RD equals difference of local OLS intercepts", r$estimate, unname(R - L), 1e-6)
  # Known jump 0.5 with data-driven bandwidth; covariate z continuous at the cutoff; uniform running variable.
  r <- edu_rdd(s, "y", "x", 0, covariates = "z")
  check("simulated jump 0.5 recovered; robust CI covers 0.5", c(r$estimate$estimate, as.numeric(r$estimate$robust_ci_low < 0.5 & r$estimate$robust_ci_high > 0.5)), c(0.5, 1), c(0.1, 0))
  check("balanced covariate: robust CI covers 0", as.numeric(r$covariate_balance$robust_ci_low < 0 & r$covariate_balance$robust_ci_high > 0), 1, 0)
  check("no manipulation: binomial p > .05 in every window", as.numeric(all(r$density_windows$p > .05)), 1, 0)
  # Heaping: move 40% of units just below the cutoff to just above it -> the count test must flag it.
  m <- s; j <- which(m$x < 0 & m$x > -0.05); j <- j[seq_len(round(0.4 * length(j)))]; m$x[j] <- -m$x[j]
  r <- edu_rdd(m, "y", "x", 0)
  check("manipulated density flagged (smallest window p < .001)", as.numeric(min(r$density_windows$p) < .001), 1, 0)
}) else message("skipped: RDD (needs rdrobust)")
