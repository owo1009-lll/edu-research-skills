# 方法卡：相关与回归（相关、分层回归、Logistic 回归）

**适用**：变量之间的相关；控制背景变量后，某些因素对连续结果的预测（分层回归）；对"是否"类结果的预测（Logistic 回归）。

**先检查**
- 题项计分方向（反向题是否已转换）、量表得分是均分还是总分。
- 各分层的模型必须用同一批样本，函数会自动取全部变量都完整的个案并在注释中写明人数。
- 共线性：函数输出 VIF，大于 5（严格时 3）需要说明或处理。
- 类别预测变量（如年级、学校类型）保持为因子，回归自动生成虚拟变量；参照组要在文中写明。

**调用**
```r
source("edu_methods.R")
d <- read.csv("inputs/data.csv", fileEncoding = "UTF-8")
edu_save(edu_cor(d, c("support", "efficacy", "engagement")), "correlations")              # 相关矩阵（带星号）
edu_save(edu_regression(d, "engagement", list(c("gender", "grade"), c("support", "efficacy"))), "hier_reg")
edu_save(edu_regression(d, "passed", list(c("gender"), c("support")), family = "binomial"), "logit")
```
输出：线性回归给出各模型的 R²、调整 R²、ΔR²、F 变化检验，系数表（B、SE、β、t、p、95% CI）和 VIF；Logistic 回归给出 OR 及 95% CI、似然比检验、Nagelkerke R²、分类准确率。

**报告**：分层回归先报告每一步的 ΔR² 和 F 变化，再报告最终模型中关键变量的 β 和 p；Logistic 回归报告 OR（如"教师支持每增加 1 分，通过的几率增加 1.85 倍，OR = 1.85，95% CI [1.32, 2.59]"）。

**常见错误**
- 横截面数据写"影响""导致""提升"；用"预测""与……相关"。
- 只报告标准化系数，不报告 B 和置信区间。
- 各分层模型样本量不同，导致 ΔR² 不可比。
- 把 Logistic 回归的 B 当作概率变化来解释。
