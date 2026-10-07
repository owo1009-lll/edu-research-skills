# `edu-analysis` Skill

[中文说明](README.md)

Statistical analysis for education research in R, with the script, data fingerprint, R session and log saved for every run.

## What To Use It For

- Survey data: reliability and validity, CFA, common-method bias, SEM, PLS-SEM
- Configurations and necessity: fsQCA, NCA
- Experiments and surveys: t tests, ANOVA, nonparametric tests, chi-square, regression, moderation and mediation
- Nested or longitudinal data: multilevel, growth and cross-lagged models

## Typical Requests

- "Check the reliability and validity of this scale, test common-method bias and fit a structural model"
- "Add fsQCA and NCA to the SEM"
- "Compare post-test scores of the two groups controlling for the pre-test"

## What You Need To Provide

- A data file (CSV, Excel) and variable notes (item-to-scale mapping, reverse items, groups)

## Outputs

- Result tables (CSV and Markdown), three-line tables and run records (`edu_output/analysis/`)

## Runtime and Dependencies

- R 4.1 or later; missing packages install into the user library with `scripts/setup_packages.R`; run `tests/known_answers.R` once as a self-check

## Boundaries

- Fit indices and cut-offs are conventions, not proof of a model; cross-sectional data are not written up as causal; no repeated respecification by modification indices

## Related Skills

- edu-writing (turn results into prose), edu-audit (check reported results)

## Status

- Beta: 33 known-answer checks (R documentation examples, lavaan tutorial values, analytic solutions); tried on synthetic data
