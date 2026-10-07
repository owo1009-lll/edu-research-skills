# 方法卡：PLS-SEM（seminr）

**适用**：以预测为导向的模型、样本较小（约 100–200）、含形成性构念或模型较复杂的探索性研究。理论检验和需要整体拟合指标时优先用 CB-SEM。在方法部分说明选择 PLS-SEM 的理由。

**先检查**
- 各构念的题项归属；反映性构念用默认的 Mode A。形成性构念需要在 seminr 中用 `weights = mode_B` 单独写，不能用本函数的默认设置。
- 样本量至少满足"10 倍规则"，更好的做法是做功效分析（逆平方根法）。

**调用**
```r
source("edu_methods.R")
d <- read.csv("inputs/data.csv", fileEncoding = "UTF-8")
measurement <- list(Support = paste0("s", 1:5), Efficacy = paste0("e", 1:4), Engagement = paste0("g", 1:6))
structural  <- data.frame(from = c("Support", "Support", "Efficacy"), to = c("Efficacy", "Engagement", "Engagement"))
edu_save(edu_pls(d, measurement, structural, boot = 5000), "pls")
```
输出：外部载荷；信度（α、rhoC、AVE、rhoA）；HTMT；路径系数的 Bootstrap 结果（原估计、均值、标准差、t、95% CI、p）；R²。间接效应可在 seminr 中用 `specific_effect_significance()` 计算。

**常用标准**（Hair et al., 2022）：外部载荷 ≥ .708；rhoA 和 rhoC 在 .70–.95 之间；AVE ≥ .50；HTMT < .85（概念相近时 < .90）；路径显著性看 Bootstrap 区间是否包含 0；报告 R²（.25、.50、.75 分别为弱、中、强）。

**报告**：先报告测量模型（信度、收敛效度、区分效度），再报告结构模型（路径系数、t、p、95% CI，以及 R²），需要时报告 f² 和 Q²。

**常见错误**
- 把 PLS-SEM 的 GoF 当作模型拟合依据。
- 用 lavaan 的 CB-SEM 结果冒充 PLS-SEM 结果，或反过来。
