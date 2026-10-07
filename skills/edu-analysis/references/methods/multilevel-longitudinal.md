# 方法卡：多层与纵向数据（ICC、多层线性模型、重复测量、增长模型、CLPM / RI-CLPM）

**适用**：学生嵌套在班级或学校；同一批学生多次测量。

**先检查**
- 嵌套：先算 ICC 和设计效应。ICC ≥ .05 或设计效应 > 2 时，用多层模型或聚类稳健标准误，不能当作独立样本。
  ```r
  source("edu_methods.R")
  edu_save(edu_icc(d, y = "score", cluster = "class_id"), "icc")
  ```
- 纵向：时点数、各时点的实际间隔、流失情况。两个时点只能做前后比较；增长模型和 RI-CLPM 至少需要三个时点。
- 自变量的层次（学生层还是班级层），以及是否需要组均值中心化。

**怎么做**
- 简单的多层模型（随机截距）可以直接写：
  ```r
  m <- lmerTest::lmer(score ~ support + class_size + (1 | class_id), data = d)
  summary(m)
  ```
- 需要完整记录和诊断的分析，用标准适配器：重复测量与混合设计方差分析、带中心化与跨层交互的线性混合模型、CLPM、RI-CLPM、线性增长模型。适配器的方案格式和每种模型需要写明的设置见 [进阶分析](../advanced-analysis.md)，运行方式：
  ```
  python scripts/run_r.py --adapter advanced --plan plan.json
  ```
  适配器需要的 R 包（lme4、lmerTest、afex、emmeans、lavaan）缺失时，运行 `Rscript scripts/setup_packages.R` 安装到 R 的用户库。

**报告**：多层模型报告 ICC、固定效应（系数、SE、df、p）、随机效应方差和模型比较；纵向模型说明各时点人数、缺失处理、模型拟合，并区分个体间稳定差异和个体内变化。

**常见错误**
- 忽略班级嵌套导致显著性被高估。
- 把 CLPM 的交叉滞后路径解释为个体内的因果作用（这需要 RI-CLPM）。
- 两个时点的数据宣称"发展趋势"。
