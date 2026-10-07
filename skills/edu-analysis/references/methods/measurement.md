# 方法卡：描述统计、信度与测量（α/ω、EFA、CFA、CR/AVE、HTMT、共同方法偏差）

**适用**：问卷研究的"研究工具"和"信效度检验"部分；改编或自编量表的结构检验。

**先检查**
- 反向题已转换，缺失编码（如 99、-1）已设为缺失。
- 自编或改编量表：先在一半样本或预调查中做 EFA，再在另一半或正式样本中做 CFA；同一批数据先 EFA 再 CFA，不能称作交叉验证。
- 估计方法：题项为 4 点及以下，或 5 点但分布明显偏斜（多数回答集中在一两个选项）时，CFA 用 `estimator = "WLSMV", ordered = c(题项)`；5 点及以上、分布大致对称时用 MLR（教育学问卷最常见的情形）。在方法部分写明选择理由。

**调用**
```r
source("edu_methods.R")
d <- read.csv("inputs/data.csv", fileEncoding = "UTF-8")
edu_save(edu_describe(d, c("support", "efficacy", "engagement")), "descriptives")
edu_save(edu_reliability(d, list(support = paste0("s", 1:5), efficacy = paste0("e", 1:4))), "reliability")
edu_save(edu_harman(d, c(paste0("s", 1:5), paste0("e", 1:4), paste0("g", 1:6))), "harman")
edu_save(edu_cmb(d, model), "common_method_bias")   # Harman + 单因子 CFA 比较 + 潜在方法因子（ULMC），三项一起报告
model <- "support =~ s1 + s2 + s3 + s4 + s5\n efficacy =~ e1 + e2 + e3 + e4\n engagement =~ g1 + g2 + g3 + g4 + g5 + g6"
edu_save(edu_cfa(d, model, estimator = "MLR"), "cfa")
```
EFA 用 psych：`psych::fa.parallel(x)` 定因子数，`psych::fa(x, nfactors = k, rotate = "oblimin", fm = "minres")` 看载荷。需要严格记录的 EFA、测量不变性（跨组、跨时间）用标准适配器，见 [进阶分析](../advanced-analysis.md)。

输出：CFA 拟合指标（χ²、df、χ²/df、CFI、TLI、RMSEA 及 90% CI、SRMR；MLR 时为稳健版本）；标准化载荷；各因子 CR 与 AVE；Fornell-Larcker 矩阵（对角线为 √AVE）；HTMT 矩阵。

**常用标准**（惯例，不是证明）：α 和 CR ≥ .70；AVE ≥ .50；标准化载荷 ≥ .50（较严格为 .70）；CFI、TLI ≥ .90（较严格为 .95）；RMSEA、SRMR ≤ .08；√AVE 大于该因子与其他因子的相关、HTMT < .85（或 .90）说明区分效度。Harman 单因素检验中第一个因子解释的方差低于 40%，一般表示共同方法偏差不严重。

**报告**："CFA 结果显示三因子模型拟合良好，χ²/df = 2.13，CFI = .96，TLI = .95，RMSEA = .052（90% CI [.041, .063]），SRMR = .041。各题项标准化载荷为 .62～.88，各维度 CR 为 .82～.91，AVE 为 .54～.67，均达到标准；各维度 √AVE 均大于其与其他维度的相关系数，HTMT 均小于 .85，区分效度良好。"

**常见错误**
- 为了达到拟合标准反复删题或加残差相关，却不报告修改过程和理由。
- 把 α 当作效度证据。
- 只做 Harman 检验就宣称"不存在共同方法偏差"。用 `edu_cmb()` 同时报告单因子 CFA 比较和潜在方法因子检验，结论写"共同方法偏差不严重"。
