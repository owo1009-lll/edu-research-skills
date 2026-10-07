# 方法卡：组间差异（t 检验、方差分析、非参数检验）

**适用**：比较两组或多组在一个连续（或等级）变量上的差异；前后测或同一批人两种条件的配对比较。

**先检查**
- 分组是否独立：同一个学生出现在两组里就是配对数据；学生按班级分组时先算 ICC（见多层与纵向）。
- 每组人数、缺失情况、明显异常值；分布严重偏态或是等级数据时，以非参数检验为主要报告。
- 方差齐性：函数会给出 Brown-Forsythe 检验。两组比较默认报告 Welch t，方差不齐时多组比较报告 Welch 方差分析。

**调用**
```r
source("edu_methods.R")
d <- read.csv("inputs/data.csv", fileEncoding = "UTF-8")
edu_save(edu_compare(d, y = "score", group = "condition"), "score_by_condition")                 # 两组或多组
edu_save(edu_compare(d, y = "score", group = "time", paired = TRUE, id = "student_id"), "pre_post") # 配对（长格式）
```
输出：各组描述统计；检验表（统计量、df、p、效应量）；三组及以上时附 Tukey 事后比较和 Holm 校正的两两 Wilcoxon。

**效应量**：两组用 Hedges' g（0.2 小、0.5 中、0.8 大）；配对用 dz；方差分析用 η²/ω²（.01 小、.06 中、.14 大）；非参数用秩二列相关 r 或 ε²。

**报告**：见 [报告格式](../reporting.md) 的 t 检验与方差分析句式。准实验后测比较要控制前测时，用回归：`edu_regression(d, "post", list("pre", "group"))`，报告组别的系数。

**常见错误**
- 多次 t 检验代替方差分析，或不做事后比较校正。
- 只报告 p 值，不报告均值、标准差和效应量。
- 把"差异不显著"写成"两组相同"。
- 前后测数据当作独立样本处理。
