# Known-answer self-check for edu_methods.R. Run from any folder:
#   Rscript known_answers.R            (exit status 0 = all checks passed)
# Reference values come from R's own documented examples, the lavaan tutorial, closed-form
# formulas, or a direct call to the original package where no published value exists.
here <- tryCatch(dirname(normalizePath(sys.frame(1)$ofile)), error = function(e) NULL)
if (is.null(here)) {
  a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  here <- dirname(normalizePath(sub("^--file=", "", a[1])))
}
source(file.path(here, "..", "scripts", "edu_methods.R"), encoding = "UTF-8")
results <- data.frame(check = character(), ok = logical(), detail = character())
check <- function(name, got, want, tol) {
  ok <- isTRUE(all(abs(got - want) <= tol))
  results[nrow(results) + 1, ] <<- list(name, ok, sprintf("got %s; want %s", paste(signif(got, 6), collapse = ", "), paste(signif(want, 6), collapse = ", ")))
}
safely <- function(name, expr) tryCatch(expr, error = function(e) results[nrow(results) + 1, ] <<- list(name, FALSE, conditionMessage(e)))

# group differences (R documentation examples)
safely("t tests", {
  r <- edu_compare(datasets::sleep, "extra", "group")$tests
  check("Welch t (sleep)", c(r$statistic[1], r$df[1], r$p[1]), c(-1.8608, 17.776, 0.07939), c(1e-3, 1e-2, 1e-4))
  r <- edu_compare(datasets::sleep, "extra", "group", paired = TRUE, id = "ID")$tests
  check("paired t (sleep)", c(r$statistic[1], r$p[1]), c(4.0621, 0.002833), c(1e-3, 1e-5))
})
safely("ANOVA", {
  r <- edu_compare(datasets::PlantGrowth, "weight", "group")$tests
  check("one-way ANOVA F, p, eta2 (PlantGrowth)", c(r$statistic[1], r$p[1], r$effect_size[1]), c(4.846, 0.01591, 0.2641), c(1e-3, 1e-4, 1e-3))
  r <- edu_compare(datasets::airquality, "Ozone", "Month")$tests
  check("Kruskal-Wallis (airquality)", c(r$statistic[3], r$p[3]), c(29.267, 6.901e-06), c(1e-3, 1e-8))
})
safely("chi-square", {
  M <- as.table(rbind(c(762, 327, 468), c(484, 239, 477)))
  d <- as.data.frame(M); d <- d[rep(seq_len(nrow(d)), d$Freq), 1:2]; names(d) <- c("gender", "party")
  r <- edu_chisq(d, "gender", "party")$tests
  check("Pearson chi-square and Cramer's V (?chisq.test)", c(r$statistic[1], r$p[1], r$effect_size[1]), c(30.0701, 2.954e-07, 0.10444), c(1e-3, 1e-9, 1e-4))
})
safely("correlation and regression", {
  r <- edu_cor(datasets::mtcars, c("mpg", "wt"))$pairs
  check("Pearson r (mtcars mpg-wt)", c(r$r, r$p), c(-0.86766, 1.294e-10), c(1e-4, 1e-12))
  r <- edu_regression(datasets::mtcars, "mpg", list("wt", "hp"))
  check("hierarchical R2, delta R2 (mtcars)", c(r$models$R2, r$models$delta_R2[2]), c(0.75283, 0.82679, 0.07396), c(1e-4, 1e-4, 1e-4))
  cf <- r$coefficients[r$coefficients$model == 2, ]
  check("lm coefficients wt, hp", cf$B[cf$term %in% c("wt", "hp")], c(-3.87783, -0.03177), c(1e-4, 1e-4))
  r <- edu_regression(datasets::mtcars, "am", list("wt"), family = "binomial")$coefficients
  check("logistic B (mtcars am ~ wt)", r$B, c(12.040, -4.024), c(1e-2, 1e-2))
})
safely("moderation and mediation", {
  r <- edu_moderation(datasets::mtcars, "mpg", "hp", "wt")
  raw <- stats::coef(stats::lm(mpg ~ hp * wt, datasets::mtcars))
  check("interaction coefficient equals lm", r$coefficients$B[r$coefficients$term == ".x:.w"], raw[["hp:wt"]], 1e-8)
  check("simple slope at mean equals centred main effect", r$simple_slopes$slope[2], r$coefficients$B[r$coefficients$term == ".x"], 1e-10)
  r <- edu_mediation(datasets::mtcars, "mpg", "wt", "hp", boot = 200)$effects
  a <- stats::coef(stats::lm(hp ~ wt, datasets::mtcars))[["wt"]]; b <- stats::coef(stats::lm(mpg ~ wt + hp, datasets::mtcars))[["hp"]]
  check("indirect effect equals a*b from OLS", r$est[r$effect == "ind_hp"], a * b, 1e-6)
})
safely("measurement", {
  hs <- lavaan::HolzingerSwineford1939
  r <- edu_cfa(hs, "visual =~ x1 + x2 + x3\n textual =~ x4 + x5 + x6\n speed =~ x7 + x8 + x9", estimator = "ML")$fit
  check("CFA fit (lavaan tutorial: chisq, df, CFI, TLI, RMSEA, SRMR)", c(r$chisq, r$df, r$CFI, r$TLI, r$RMSEA, r$SRMR),
        c(85.306, 24, 0.931, 0.896, 0.092, 0.065), c(1e-2, 0, 1e-3, 1e-3, 1e-3, 1e-3))
  x <- hs[, c("x1", "x2", "x3")]; k <- 3
  check("Cronbach alpha equals formula", edu_reliability(hs, list(v = c("x1", "x2", "x3")))$reliability$alpha,
        k / (k - 1) * (1 - sum(apply(x, 2, var)) / var(rowSums(x))), 1e-8)
  p <- stats::prcomp(hs[, paste0("x", 1:9)], scale. = TRUE)
  check("Harman first component equals PCA", edu_harman(hs, paste0("x", 1:9))$harman$first_factor_variance_pct, 100 * p$sdev[1]^2 / 9, 1e-8)
  pd <- "ind60 =~ x1 + x2 + x3\n dem60 =~ y1 + y2 + y3 + y4\n dem65 =~ y5 + y6 + y7 + y8\n dem60 ~ ind60\n dem65 ~ ind60 + dem60\n y1 ~~ y5\n y2 ~~ y4 + y6\n y3 ~~ y7\n y4 ~~ y8\n y6 ~~ y8"
  r <- edu_sem(lavaan::PoliticalDemocracy, pd, estimator = "ML")$fit
  check("SEM fit (lavaan tutorial: chisq, df)", c(r$chisq, r$df), c(38.125, 35), c(1e-2, 0))
})
safely("PLS-SEM", {
  mobi <- seminr::mobi
  meas <- list(Image = paste0("IMAG", 1:5), Expectation = paste0("CUEX", 1:3), Value = paste0("PERV", 1:2), Satisfaction = paste0("CUSA", 1:3))
  st <- data.frame(from = c("Image", "Image", "Expectation", "Value"), to = c("Expectation", "Satisfaction", "Value", "Satisfaction"))
  r <- edu_pls(mobi, meas, st, boot = 200)
  mm <- seminr::constructs(seminr::composite("Image", paste0("IMAG", 1:5)), seminr::composite("Expectation", paste0("CUEX", 1:3)),
                           seminr::composite("Value", paste0("PERV", 1:2)), seminr::composite("Satisfaction", paste0("CUSA", 1:3)))
  sm <- seminr::relationships(seminr::paths(from = "Image", to = c("Expectation", "Satisfaction")),
                              seminr::paths(from = "Expectation", to = "Value"), seminr::paths(from = "Value", to = "Satisfaction"))
  direct <- seminr::estimate_pls(mobi, mm, sm)$path_coef["Image", "Expectation"]
  check("PLS path equals direct seminr estimate", r$paths$`Original Est.`[r$paths$path == "Image  ->  Expectation"], direct, 1e-10)
  check("PLS reliability within (0, 1)", as.numeric(all(r$reliability$rhoC > 0 & r$reliability$rhoC < 1)), 1, 0)
})
safely("fsQCA", {
  v <- edu_calibrate(c(1, 2, 3), 1, 2, 3)
  check("direct calibration maps e, c, i to .05, .5, .95", v, c(0.05, 0.5, 0.95), c(1e-6, 1e-12, 1e-6))
  lf <- QCA::LF; conds <- c("DEV", "URB", "LIT", "IND", "STB")
  nec <- edu_necessity(lf, "SURV", conds)
  ref <- QCA::pof(lf[, "DEV"], lf[, "SURV"], relation = "necessity")$incl.cov[1, "inclN"]
  check("necessity consistency equals QCA::pof", nec$consistency[nec$condition == "DEV"], ref, 1e-6)
  r <- edu_fsqca(lf, "SURV", conds, incl.cut = 0.8, pri.cut = 0.7)
  tt <- QCA::truthTable(lf, outcome = "SURV", conditions = conds, incl.cut = 0.8, pri.cut = 0.7)
  direct <- QCA::minimize(tt, include = "?")$solution[[1]]
  got <- r$solutions$term[r$solutions$solution == "parsimonious"]
  check("parsimonious solution equals QCA::minimize", as.numeric(identical(sort(got), sort(direct))), 1, 0)
  check("configuration table has one column per configuration", ncol(r$configurations) - 1,
        sum(r$solutions$solution == "complex"), 0)
  r <- edu_fsqca(lf, "SURV", conds, incl.cut = 0.8, pri.cut = 0.7, dir.exp = conds)
  inter <- r$solutions$term[r$solutions$solution == "intermediate"]
  check("intermediate solution (LF, all conditions expected present)",
        as.numeric(identical(sort(inter), sort(c("DEV*URB*LIT*STB", "DEV*LIT*~IND*STB")))), 1, 0)
  cf <- r$configurations; col <- function(j, v) cf[cf$row == v, paste0("C", j)]
  j1 <- which(inter == "DEV*URB*LIT*STB"); j2 <- which(inter == "DEV*LIT*~IND*STB")
  check("core/peripheral marks (URB core, DEV peripheral; ~IND core, LIT peripheral)",
        as.numeric(c(col(j1, "URB") == "●", col(j1, "DEV") == "•", col(j2, "IND") == "⊗", col(j2, "LIT") == "•")), c(1, 1, 1, 1), 0)
})
safely("NCA", {
  n <- 10; d <- data.frame(x = c((0:n) / n, 1), y = c((0:n) / n, 0))
  r <- edu_nca(d, "x", "y", ceilings = "ce_fdh", test.rep = 0)$effects
  check("CE-FDH effect size on a staircase equals (n+1)/(2n)", r$effect_size, (n + 1) / (2 * n), 1e-8)
})
safely("kappa and ICC", {
  r1 <- c(rep("a", 45), rep("a", 15), rep("b", 25), rep("b", 15)); r2 <- c(rep("a", 45), rep("b", 15), rep("a", 25), rep("b", 15))
  check("Cohen's kappa (45/15/25/15 table)", edu_kappa(r1, r2)$agreement$kappa, (0.60 - 0.54) / (1 - 0.54), 1e-8)
  r <- edu_icc(lme4::sleepstudy, "Reaction", "Subject")$icc
  check("ICC within (0, 1)", as.numeric(r$ICC > 0 & r$ICC < 1), 1, 0)
})

safely("method bias, bootstrap sample, formatting", {
  hs <- lavaan::HolzingerSwineford1939
  model <- "visual =~ x1 + x2 + x3\n textual =~ x4 + x5 + x6\n speed =~ x7 + x8 + x9"
  r <- edu_cmb(hs, model, estimator = "ML")
  check("single-factor CFA fits worse (delta chi2 > 0, p < .001)", as.numeric(c(r$single_factor_test$delta_chisq > 0, r$single_factor_test$p < .001)), c(1, 1), 0)
  check("CMB Harman equals edu_harman", r$harman$first_factor_variance_pct, edu_harman(hs, paste0("x", 1:9))$harman$first_factor_variance_pct, 1e-10)
  hm <- hs; hm$x2[1:10] <- NA
  pd <- paste(model, "textual ~ a*visual\n speed ~ b*textual + visual\n ind := a*b", sep = "\n")
  set.seed(1); s <- edu_sem(hm, pd, boot = 100)
  check("bootstrap SEM keeps all cases with missing data (FIML)", as.numeric(grepl("n = 301", s$notes[1])), 1, 0)
  check("standardized indirect effect has a CI", as.numeric(!is.na(s$defined$std_ci_low[1])), 1, 0)
  md <- edu_md(data.frame(p = c(0.00001, 0.0412)))
  check("p values print as '< .001' and '.041'", as.numeric(c(grepl("< .001", md[3], fixed = TRUE), grepl(".041", md[4], fixed = TRUE))), c(1, 1), 0)
  f <- edu_nca_plot(data.frame(x = c(0, .5, 1, .2), y = c(0, .5, 1, .1)), "x", "y", file.path(tempdir(), "nca_test.png"))
  check("NCA plot file written", as.numeric(file.exists(f) && file.size(f) > 1000), 1, 0)
})

# method groups added in 0.9.0; each block is skipped when its packages are missing
for (f in sort(list.files(here, "^ka_[a-z]+\\.R$", full.names = TRUE))) source(f, encoding = "UTF-8")

print(results, right = FALSE)
cat(sprintf("\n%d of %d checks passed.\n", sum(results$ok), nrow(results)))
if (!all(results$ok)) quit(status = 1)
