# 方法卡：调节与中介

**适用**：调节——X 对 Y 的作用是否随 W 的水平而变；中介——X 是否通过 M 与 Y 相联系（并行中介或两个中介的链式中介）。

**先检查**
- 中介要有理论上的先后顺序；横截面数据只能说明"统计意义上的间接效应"，不能证明因果机制。三波及以上数据更合适时，转到多层与纵向方法卡。
- 调节变量是连续还是类别：连续变量自动取均值 ±1 个标准差做简单斜率；类别变量给出各组内的斜率。
- 中介的 Bootstrap 次数正式报告用 5000 次，并写明随机种子。

**调用**
```r
source("edu_methods.R")
d <- read.csv("inputs/data.csv", fileEncoding = "UTF-8")
edu_save(edu_moderation(d, y = "engagement", x = "support", w = "efficacy", covariates = c("gender")), "moderation")
edu_save(edu_mediation(d, y = "engagement", x = "support", m = c("efficacy", "belonging")), "parallel_mediation")
edu_save(edu_mediation(d, y = "engagement", x = "support", m = c("efficacy", "belonging"), serial = TRUE), "serial_mediation")
```
输出：调节给出系数表、交互项的 ΔR² 和 F 检验、简单斜率（斜率、SE、t、p、95% CI）；中介给出各路径系数（含标准化系数）、各间接效应、总间接效应、直接效应和总效应，以及百分位 Bootstrap 95% CI 和占总效应的比例。

**报告**
- 调节："交互项显著（B = 0.15，p = .004，ΔR² = .03）。简单斜率分析表明，自我效能较高时（+1 SD），教师支持与学习投入的关系更强（B = 0.52，p < .001）；较低时（−1 SD）关系较弱（B = 0.21，p = .012）。"
- 中介：间接效应的 95% CI 不包含 0 即为显著；报告效应值、CI 和占比。直接效应仍显著写"部分中介"，不显著写"完全中介"时要谨慎，样本量会影响直接效应是否显著。

**常见错误**
- 用逐步法（Baron & Kenny）的"X→Y 必须显著"作为中介前提；现在以间接效应的 Bootstrap 区间为准。
- 交互项不中心化导致主效应难以解释（函数默认中心化）。
- 潜变量之间的中介和调节：写进 lavaan 模型用 `edu_sem()`，见结构方程方法卡。
