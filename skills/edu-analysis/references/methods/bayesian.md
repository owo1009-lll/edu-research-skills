# 方法卡：贝叶斯因子检验（t 检验、方差分析、回归、相关）

**适用**
- 需要回答"数据更支持有差异还是无差异"：频率学派的不显著结果不能说明"没有差异"，贝叶斯因子（BF01）可以量化支持零假设的证据。
- 小样本研究、重复验证研究，或审稿人要求补充贝叶斯分析时，与频率学派结果并列报告。

**先检查**
- 与对应频率学派方法的前提相同：独立组 t 检验要求组内近似正态；回归要求线性与同方差；方差分析的因子为组间因素。
- 先确定先验尺度并在方法部分写明。默认用 BayesFactor 的 "medium"：t 检验 r = √2/2 ≈ 0.707（Cauchy 先验），方差分析固定效应 r = 1/2，回归连续变量 r = √2/4，相关 r = 1/3。
- 有理论依据预期效应较大时可用 "wide" 或 "ultrawide"，但要事先确定，不能看结果再换。

**调用**
```r
source("edu_methods.R"); source("edu_methods_models.R")
d <- read.csv("inputs/data.csv", fileEncoding = "UTF-8")
edu_save(edu_bayes(d, "ttest", "score", group = "condition"), "bayes_t")
edu_save(edu_bayes(d, "paired", "score", group = "time", id = "id"), "bayes_paired")
edu_save(edu_bayes(d, "anova", "score", x = c("method", "grade")), "bayes_anova")
edu_save(edu_bayes(d, "regression", "engagement", x = c("support", "efficacy")), "bayes_reg")
edu_save(edu_bayes(d, "correlation", "engagement", x = "support"), "bayes_cor")
# 先验稳健性：再用 rscale = "wide"、"ultrawide" 各跑一次
```

输出：BF10、BF01、数值误差（%）、所用先验尺度、证据等级；后验估计（中位数、均值、SD、95% 可信区间：t 检验为标准化效应 δ 和均值差，相关为 ρ，回归与方差分析为 BF 最大模型的参数）；多预测变量回归另给每个变量的 BF（全模型对去掉该变量的模型）。

**判断标准**（Jeffreys, 1961；Lee & Wagenmakers, 2013 的分级）
- BF10：1–3 弱（anecdotal），3–10 中等（moderate），10–30 强（strong），30–100 很强（very strong），> 100 极强（extreme）；BF10 < 1 时看 BF01 = 1/BF10，按同一标准表示支持 H0 的程度。
- BF 依赖先验：同一数据在不同先验尺度下 BF 可能跨过 3 或 1/3，必须报告先验稳健性检验（Rouder et al., 2009；Wagenmakers et al., 2018）。
- BF 在 1/3 与 3 之间说明数据不足以区分两种假设，不能写成"支持零假设"。
- 可信区间是参数的后验不确定性，不等于假设检验；判断"有无效应"看 BF。

**报告**
- 方法部分：使用 R 包 BayesFactor（Morey & Rouder），JZS 先验，Cauchy 尺度 r = 0.707；后验抽样 10,000 次。
- 结果句："贝叶斯独立样本 t 检验显示，BF10 = 0.21，即数据支持两组无差异的程度约为有差异的 4.8 倍（中等证据支持 H0）；δ 的后验中位数为 0.05，95% 可信区间 [−0.31, 0.40]。在宽（r = 1）与超宽（r = √2）先验下 BF01 分别为 6.6 与 9.2，结论稳定。"
- 与频率学派结果并列时一张表同时给 t/F、p、效应量和 BF10。

**常见错误**
- 只报告 BF，不报告先验尺度和稳健性检验。
- 把 BF10 = 2 写成"支持备择假设"，或把不显著的 p 值直接写成"证实无差异"。
- 把 BF 当作效应大小；BF 大说明证据强，不说明效应大。
- 用后验可信区间是否包含 0 代替 BF 来下"有无效应"的结论，或看完数据后挑选能得到显著结果的先验。
