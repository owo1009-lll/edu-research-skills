# Recorded advanced analysis

Use only for the requested analysis, from documented research questions and design. The assistant prepares internal plans; users supply ordinary data and research descriptions. Existing results can go directly to writing. Standard adapters below were checked on real cases during development (archived on the archive/dev-history branch); that is bounded execution evidence, not universal method or measurement validation.

## Three execution states

- `verified_standard`: documented adapter plus relevant actual runs, diagnostics and checks for the stated design/options.
- `task_specific_executed`: a documented dedicated script was executed and checked for this task; its scope does not become generic support.
- `blocked`: identify the actual missing material, inadmissible solution, unidentified structure, or environment problem. Keep failed runs and finish independent tasks.

For a method outside the adapters, inspect official current documentation and original method sources, assess design/identification, and construct a task-specific reproducible workflow if feasible. Do not reply with a blanket unsupported-method refusal or bypass a substantive decision. A supported adapter can still fail for a particular dataset.

## Run and evidence

Run from the user's project folder; results go to `edu_output/analysis/`. Preserve input bytes and conversion decisions, including any derived IDs. Install missing statistical dependencies with `Rscript scripts/setup_packages.R` (R user library); record versions and the process exit. Environment failure must not become a successful run claim.

```powershell
python <skill>/scripts/run_r.py --adapter advanced --plan <assistant-created plan.json> [--rscript <path>]
```

The runner saves immutable input/plan/script hashes, actual R/session/library paths, stdout/stderr, exit status, structured estimates and diagnoses. Microdata/IDs/model objects stay private. An R exit0 can mean `awaiting_constraint_review`, not a completed comparison sequence. Follow `analysis_record.json` and diagnostics, not exit code alone. Failed runs remain separate; create a new plan/run after a justified correction.

Common plan: data CSV path; real question/selection reason; unit, ID, row structure, actual cluster columns, independence basis; documented variable meanings/sources/types and special missing values; explicit seed/confidence; method, missing strategy/assumption. No user JSON requirement.

## Measurement

EFA (`efa`): items, chosen factors and source/theory rationale, extraction `minres|ml|pa`, rotation `oblimin|promax|varimax|none`, Pearson or polychoric correlation, listwise/pairwise missingness, parallel replicates. Continuous PA uses psych documented reference. Ordinal PA requires listwise and `parallel_design=permutation_without_replacement`: independently permute columns preserving actual response marginals, use mature psych polychoric/globalFALSE/no smoothing/zero continuity correction and psych fa reduced eigenvalues. Save 95th null reference. Rare/invalid correlations stop rather than collapse categories or replace estimates silently. Pairwise EFA inference needs review of varying pair counts; nrow is not a universal effective N. Factor counts and loading thresholds do not certify validity. EFA/CFA on identical observations are not independent validation.

CFA (`cfa`): located model and measurement rationale; continuous ML/MLR or declared ordered indicators WLSMV; marker or std.lv identification; delta/theta parameterization; explicit listwise, continuous FIML, or ordered pairwise handling. WLSMV FIML is prohibited. Save loadings, covariance/variance, fitted measures, parameter and standardized tables separately. Fit indices alone never certify a model. Review convergence/postcheck, negative variances, covariance definiteness, finite SEs, gradient and instability; equality constraints require constrained interpretation of gradients and singular full covariance matrices.

Composite reliability is requested only for an admissible CFA, with `reliability=true` and explicit `reliability_denominator=observed|model_implied`. semTools congeneric reliability uses fitted loadings/latent variances; observed versus implied covariance denominators differ. Ordered-scale estimates use Green–Yang correction. Do not call these raw alpha, validity or universal reliability of every score.

Invariance (`invariance`): actual groups or `long_factors` repeated-factor map, substantive comparison basis, located configural model and prespecified same-item residual correlations where warranted. Each named step has equal constraint types, reason and any justified partial release. Use semTools measEq.syntax, Wu–Estabrook ordered identification, then actual lavaan fits/scaled LRT. Ordered thresholds precede loading comparisons; continuous metric/scalar constraints are a different sequence. Save generated syntax. Review each actual contrast before setting `continue_after_review=true`; a nonsignificant contrast does not prove equivalence. Scalar failure forbids unqualified latent mean comparison. No automatic freeing of intercepts/items/residuals to pass thresholds. Partial constraints need located substantive reasons and dedicated identification review.

## Paths and SEM

`sem` uses explicit lavaan model syntax, documented estimand and model rationale, identification/estimator/missing settings as above. Fixed-X is explicitly FALSE for the adapted joint covariance/FIML model. Observed and latent paths, selected parallel/serial indirect paths and prespecified observed interactions are represented in the planned model; never enumerate models. Labels and `:=` definitions state direct, indirect and total estimands. Contemporaneous decomposition, products of coefficients and time precedence do not establish causal mechanisms.

ML `bootstrap_percentile` requires at least200 replicates and preserves actual failed/nonadmissible resamples; small500 case runs are software checks, not a universal precision recommendation. Delta intervals are explicitly different. The parameter table CI belongs to unstandardized est; standardized CIs are exported separately with their delta approximation, never relabeled bootstrap-percentile intervals. Defined conditional indirect products must use actual moderator coding/centering and actual sampled units. No fake observed latent interaction adaptation.

Multi-group SEM needs group_reason and measurement_comparability. Different vector labels (`c(a1,a2)`) allow genuine group differences; repeated labels constrain them. Joint planned contrasts can be supplied as named `hypotheses` with located reasons; actual lavaan Wald tests are saved. Do not infer a group difference from one significant coefficient and another nonsignificant coefficient. Comparability limits remain in interpretation.

## Repeated/multilevel

`rm_anova`: long participant IDs, documented within/between factors and exact factor levels, outcome, complete-cell missing assumption, explicit `cell_handling=mean`, sum/poly contrasts and `correction=GG|HF|none`. Check between factors constant within person. Save actual trial selection, aggregated cells and excluded persons. TypeIII afex tests, applicable sphericity correction and prespecified emmeans contrasts/multiplicity are saved. Cell means condition on sampled stimuli; generalization to new items may need crossed item random effects in a dedicated workflow. Two-level within factors do not require sphericity corrections; more levels do.

`lmm`: actual cluster structure, formula, ML/REML, Satterthwaite/KenwardRoger df, centering decisions, random-structure and residual rationale. Grand centering or within-group decomposition creates explicitly named within/between columns with saved reason. Distinguish within-person from between-person and cross-level interactions. Save cluster counts, fixed effects/intervals, random variance/covariance, singularity and optimizer/Hessian checks. Small cluster counts or singularity require review, not automatic term deletion. ML/REML and df rules are not interchangeable. Missing outcome rows are excluded while other observations may remain; disclose ignorable/MAR assumptions, not universal complete-person deletion.

Optional prediction.rows is an assistant-prepared column mapping, with meaning. Saved fixed-effect population mean curves have pointwise asymptotic Wald intervals, not individual prediction bands. Repeated-person time coding must come from actual elapsed intervals; school/class IDs must come from source, not synthetic memberships. Complex survey weights, AR residuals and generalized mixed outcomes need dedicated documented workflows.

Optional planned_contrasts supplies name, named coefficient weights and reason. lmerTest contest1D uses the full coefficient covariance and selected df rule for the joint contrast. Conditional slopes must not sum separate coefficient CI endpoints. Prespecified contrast intervals are unadjusted unless a separately recorded family adjustment is justified.

## Longitudinal

`clpm|ri_clpm`: wide one row per participant, at least3 increasing times, two distinct continuous documented outcome series, explicit comparability basis, `lag_constraints=free|equal` and constraint_reason. Equality is never automatic, and unequal interval lengths do not justify equal discrete-lag coefficients. CLPM combines between/within sources. Genuine RI-CLPM generates fixed-unit RI loadings, separate within factors, zero observed residual variance, explicit RI/within orthogonality and wave means; it uses lavaan::lavaan with automatic variance/covariance defaults disabled. It is not CLPM renamed. State single-indicator measurement-error and stable-component assumptions. Improper latent/innovation covariances stop interpretation; preserve them and choose a separately justified source/example, not a hidden wave deletion.

`growth`: documented continuous waves, actual elapsed times and origin_reason, at least3 occasions, explicit linear trajectory question. Latent intercept loadings1 and slope loadings are actual time units; free wave residual variances are saved. Source item comparability may be untestable with score-only data. Save model-implied population means and estimator-specific pointwise mean intervals; distinguish observed wave means, individual trajectories and mean trends. An admissible optimizer solution can still have severe substantive misfit: retain that limit, do not present a linear curve as established development.

## Writing/figures

Pass actual aggregate outputs and design/diagnostic limits to the existing writing/full-manuscript workflow. Generate located loadings/reliability, fit/comparison, path/effect, fixed/random, repeated-condition and longitudinal tables from actual CSVs. Use existing Python make_figures for estimated intervals, model population trajectories and explicitly classified model diagrams. Manuscript paragraphs state actual N/retention, coding/time, estimator, missing assumptions and interval meaning. Keep detailed diagnostics/run logs outside prose, with consequential model/selection limits in the claims they constrain.

The existing project scripts/build_analysis_evidence.py now accepts completed advanced --quant-run directories and validated --content-version directories, retaining method choices, aggregate hashes and source roles. Content excerpts stay in private packets. Inadmissible diagnoses and incomplete review statuses cannot become unrestricted empirical prose. No user-created configuration is needed.

Bounded execution evidence includes continuous minres/oblimin, ML/promax, PA/varimax; ordinal minres/none permutation PA is a task-specific workflow. Unexecuted variants (including Kenward–Roger, alternate correction, partial constraints and equal-lag options) require actual dedicated execution and checks before a task claims them as validated. Accepting an option in code is not evidence that this release has tested every combination.
