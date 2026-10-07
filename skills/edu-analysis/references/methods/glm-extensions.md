# 方法卡：有序、多项与计数回归（Logistic 回归的扩展）

**适用**
- **有序 Logistic**：因变量是有序等级，且不宜当连续变量（如学业等级 A/B/C/D、"从不—偶尔—经常"、3 级及以下的满意度单题）。
- **多项 Logistic**：因变量是三类及以上、无顺序的类别（如升学去向、选课类型、学习策略类型）。
- **计数模型**：因变量是次数（缺勤天数、提问次数、发表篇数、违纪次数），非负整数、常右偏且零多。

**先检查**
- 各类别都要有足够样本：每个参数约 10 例以上；稀疏类别先合并（有理论依据）。
- 有序模型的比例优势假设：每个预测变量在各切点的效应相同。
- 多项模型的无关选项独立性（IIA）：去掉某一类不应改变其余类别之间的比较。
- 计数：均值与方差是否接近（过度离散）；零的比例；观测时长不同（如课时数不同）时用暴露量作偏移项。

**调用**
```r
source("edu_methods.R"); source("edu_methods_models.R")
d <- read.csv("inputs/data.csv", fileEncoding = "UTF-8")
edu_save(edu_ordinal(d, "grade_level", c("support", "efficacy", "gender"), levels = c("D", "C", "B", "A")), "ordinal")
edu_save(edu_multinom(d, "pathway", c("ses", "achievement", "gender"), ref = "就业"), "multinom")
edu_save(edu_count(d, "absences", c("ses", "engagement"), offset = "school_days", zero = c("zinb", "hurdle_nb")), "count")
```
`offset` 是暴露量列名（函数取对数）；`zero` 可选 `"zip"`、`"zinb"`、`"hurdle_poisson"`、`"hurdle_nb"`，`zero_x` 指定零部分的预测变量。

输出：有序——系数 B、OR 及剖面似然 95% CI、切点、模型拟合（LR χ²、AIC、McFadden R²、Hessian 条件数）、逐变量与整体的比例优势似然比检验。多项——每一类相对参照类的 B、RRR、Wald CI 与 p；偏差、AIC、McFadden R²、命中率；各预测变量的整体 LR 检验。计数——Poisson、负二项及所选零膨胀/障碍模型的 logLik、AIC、BIC、θ、观测与预测零个数；过度离散检验（Pearson χ²/df、Cameron-Trivedi、Poisson 对负二项 LR）；IRR（计数部分）和 OR（零部分）及 CI；Vuong 检验。

**判断标准**
- 比例优势检验 p < .05 说明该变量违背假设（Brant, 1990 的似然比版本）；大样本下轻微违背也会显著，可报告部分比例优势模型或改用多项模型作敏感性分析。
- 系数方向：有序模型中 OR > 1 表示更可能处于更高等级。
- 过度离散：Pearson χ²/df 明显大于 1、Cameron-Trivedi 检验显著（Cameron & Trivedi, 1990）时用负二项，Poisson 的标准误会偏小。
- 零膨胀/障碍模型要有理论理由（存在"结构性零"的人群，或"是否发生"与"发生几次"是两个过程）；用 AIC/BIC 和零的拟合比较，Vuong 检验不能单独证明零膨胀（Wilson, 2015）。
- McFadden R² 在 .2–.4 已属拟合很好（McFadden, 1979），不要按 OLS 的 R² 解读。

**报告**
1. 有序："控制性别后，自我效能每提高 1 分，学生处于更高学业等级的优势提高 1.84 倍，OR = 1.84，95% CI [1.52, 2.23]，p < .001；比例优势假设检验未见违背，χ²(3) = 4.12，p = .249。"
2. 多项：先报告各预测变量的整体 LR 检验，再按"相对于参照类"报告 RRR。
3. 计数：说明选择模型的依据（过度离散检验、AIC、零的拟合），报告 IRR："每多 1 分学习投入，缺勤天数的期望值降低 12%，IRR = 0.88，95% CI [0.83, 0.93]。"

**常见错误**
- 把 5 级以下的有序结果当连续变量做 OLS，或把有序结果拆成多个二分类回归。
- 不检验比例优势假设；把 polr/clm 系数的方向读反。
- 多项模型参照类不说明，或只报告显著的那一类比较。
- 计数数据直接用 OLS 或对数变换后 OLS；有过度离散仍用 Poisson；暴露时长不同却不加偏移项。
