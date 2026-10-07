# 方法卡：项目反应理论（IRT：Rasch、2PL、等级反应模型）

**适用**：测验或量表的题目分析与等值前分析：每道题的难度、区分度、题目拟合，测验在哪个能力段最精确，以及得到能力估计值（θ）。二分计分题（对/错）用 Rasch 或 2PL；李克特等有序题用等级反应模型（GRM）。只需要总分信度时，α/ω 就够了，见 [信度与测量](measurement.md)。

**先检查**
- 单维性：先做 EFA 或单因子 CFA（有序题用 WLSMV）确认一个主导因子；局部独立：题目之间除共同特质外没有额外关联（如同一阅读材料下的题目），可用 `mod <- mirt::mirt(x, 1, itemtype = "2PL"); mirt::residuals(mod, type = "Q3")` 查看；Q3 在题目少时整体偏负，一般以高出全部 Q3 均值 .20 以上为局部依赖的信号（Christensen et al., 2017）。
- 样本量（经验值）：Rasch 至少 100–200 人，2PL 与 GRM 至少 500 人（de Ayala, 2009）；类别回答很少的选项先合并。
- 计分方向一致；缺失作答可以保留（全信息极大似然），但缺失时 S-X² 题目拟合无法计算。

**调用**
```r
source("edu_methods.R"); source("edu_methods_latent.R")
d <- read.csv("inputs/data.csv", fileEncoding = "UTF-8")
edu_save(edu_irt(d, paste0("t", 1:20), model = "Rasch"), "irt_rasch")          # 同时给出 Rasch 对 2PL 的似然比检验
edu_save(edu_irt(d, paste0("t", 1:20), model = "2PL", scores = TRUE), "irt_2pl")
edu_save(edu_irt(d, paste0("s", 1:8), model = "graded"), "irt_grm")             # 有序题
```
输出：`item_parameters`（IRT 参数化：a = 区分度，b = 难度；GRM 为 b1…bk 各类别阈值，即 P(X ≥ k) = .5 时的 θ；均带标准误）；`item_fit`（S-X²、df、RMSEA、p）；`model_fit`（LL、AIC、BIC、SABIC，M2 或 C2 统计量及 RMSEA 90% CI、SRMSR、CFI、TLI，边际信度与 EAP 经验信度）；`model_comparison`（等区分度模型对自由区分度模型的似然比检验：二分题为 Rasch 对 2PL，GRM 为等斜率 GRM 对 GRM，多级 Rasch 为 PCM 对 GPCM）；`scores`（可选，每人的 EAP θ 与标准误）。

**判断标准**
- 整体拟合：M2 的 RMSEA ≤ .05、SRMSR ≤ .05 为拟合良好（Maydeu-Olivares & Joe, 2006；Maydeu-Olivares, 2013），RMSEA ≤ .089 尚可；题目少、df 不足时函数改用 C2 并在 `stat` 列注明。
- 题目拟合：S-X²（Orlando & Thissen, 2000）p < .01 且 RMSEA > .05 的题目需要检查；题目多时注意多重检验。
- 区分度 a（logistic 尺度，Baker, 2001）：0.65–1.34 中等，1.35–1.69 高，≥ 1.70 很高；< 0.65 的题目区分力弱。
- 难度 b 一般在 −3 到 +3；全部集中在一端说明测验对另一端能力的人测量不准。
- 信度：边际信度或 EAP 经验信度 ≥ .70（高利害用途 ≥ .80）。
- 模型选择：似然比 p < .05 且 AIC/BIC 一致更小时选择自由区分度模型；Rasch 模型的好处（总分是充分统计量、样本无关的测量）需要理论上的理由，而不是只看拟合。
- `mirt` 的 Rasch 固定 a = 1、估计 θ 的方差（`theta_var`），b 以 logit 为单位；与 SD(θ) = 1 的 1PL 对比时，b 除以 √theta_var。

**报告**
1. 题目参数表：题目、a（SE）、b 或 b1…bk（SE）、S-X²、RMSEA、p。
2. 模型比较与整体拟合："2PL 与 Rasch 模型的似然比检验显著，χ²(19) = 48.21，p < .001，BIC 由 21 456 降至 21 433，选择 2PL。2PL 模型 M2(170) = 196.4，p = .08，RMSEA = .018，SRMSR = .031，拟合良好；边际信度为 .86。"英文可写 "The 2PL fitted better than the Rasch model, LR χ²(19) = 48.21, p < .001; M2(170) = 196.4, RMSEA = .018, SRMSR = .031; marginal reliability = .86."
3. 单维性与局部独立的检验结果，以及所用软件、估计方法（mirt，边际极大似然/EM）。
4. 需要时给出测验信息曲线：`plot(mod, type = "info")`（mod 为 `mirt::mirt()` 拟合的对象）。

**常见错误**
- 不检验单维性和局部独立就做 IRT。
- 把 mirt 输出的斜率—截距参数（a1、d）当作难度报告；本函数已转换为 IRT 参数（b = −d/a）。
- 样本量不足时估计 2PL/GRM，或删去拟合差的题目却不报告删除过程。
- 用 IRT θ 做后续分析时忽略其测量误差；θ 的 SE 随能力水平变化，两端的人估计不准。
