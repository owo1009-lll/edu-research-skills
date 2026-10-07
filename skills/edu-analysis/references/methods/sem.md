# 方法卡：结构方程模型（CB-SEM，lavaan）

**适用**：多个潜变量之间的路径关系，以及潜变量层面的中介和调节；样本量一般在 200 以上，或每个自由参数至少 10 个样本。

**先检查**
- 测量模型（CFA）先过关，再估计结构模型（两步法）。
- 模型要有理论依据，在看数据之前写好；不要比较大量候选模型挑最好的一个。
- 估计方法：连续或 5 点以上题项用 MLR；等级题项用 WLSMV。有缺失时 ML/MLR 自动使用 FIML。

**调用**
```r
source("edu_methods.R")
d <- read.csv("inputs/data.csv", fileEncoding = "UTF-8")
model <- "
  support    =~ s1 + s2 + s3 + s4 + s5
  efficacy   =~ e1 + e2 + e3 + e4
  engagement =~ g1 + g2 + g3 + g4 + g5 + g6
  efficacy   ~ a*support
  engagement ~ c*support + b*efficacy
  indirect := a*b
  total    := c + a*b
"
edu_save(edu_sem(d, model, estimator = "MLR"), "sem")              # 路径、R²、拟合
edu_save(edu_sem(d, model, boot = 5000), "sem_boot")              # 间接效应的 Bootstrap 区间（ML；有缺失时自动用 FIML，样本与主模型一致）
```
输出：拟合指标、路径系数（B、SE、z、p、95% CI、标准化 β）、内生变量的 R²、定义参数（间接效应、总效应）。潜变量交互、多组比较和带约束的复杂模型，用标准适配器，见 [进阶分析](../advanced-analysis.md)。

**报告**：先报告测量模型，再报告结构模型的拟合，然后逐条报告假设路径（β、p）和间接效应（效应值与 Bootstrap 95% CI），最后报告 R²。路径图用 `edu-writing` 的作图工具绘制，标出标准化系数和显著性。

输出中的 `std` 及其区间是标准化效应（delta 法 95% CI）；显著性以非标准化间接效应的 Bootstrap 区间为准。路径图用 edu-writing 的 `make_figures.py`（`kind: "framework"`，中文图加 `"language": "zh"`，每条边写 `relation`：`influence` 实线、`hypothesized` 虚线）。

**常见错误**
- 根据修正指数不断添加路径直到拟合达标。
- 横截面模型的箭头写成因果机制。
- 间接效应只看 Sobel 检验；以 Bootstrap 区间为准。
