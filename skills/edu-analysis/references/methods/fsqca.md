# 方法卡：模糊集定性比较分析（fsQCA，QCA 包）

**适用**：哪些条件的组合会导致某个结果（多重并发因果、等效路径、因果非对称）。案例数一般 10–500，条件 3–7 个；问卷研究常和 SEM、NCA 配合使用。

**先检查**
- 条件和结果的选择有理论依据，条件数与案例数相称（条件越多，有限多样性越严重）。
- 校准锚点：完全不隶属、交叉点、完全隶属。问卷数据常用样本的 95%、50%、5% 分位数，或量表的有意义取值（如 5 点量表的 4、3、2）。锚点和依据要在文中写明。
- 隶属度恰为 0.5 的案例会被自动改为 0.501，函数注释会写明人数。量表均分取值离散时，大量案例会正好落在中位数锚点上（超过约 10% 时应在文中说明），可把交叉点设在相邻的非取值点（如 3.01）并说明理由。
- 条件只有 3 个左右时，真值表往往没有逻辑余项，复杂解、简约解和中间解会完全相同，核心和边缘条件无法区分；这时在文中说明，并以复杂解报告组态。

**调用**
```r
source("edu_methods.R")
d <- read.csv("inputs/data.csv", fileEncoding = "UTF-8")
q <- function(v) unname(quantile(d[[v]], c(.05, .50, .95), na.rm = TRUE))   # 5%、50%、95% 分位数作锚点
vars <- c("engagement", "support", "efficacy", "belonging", "ai_use")
anchors <- setNames(lapply(vars, q), vars)
res <- edu_fsqca(d, outcome = "engagement", conditions = vars[-1], anchors = anchors,
                 incl.cut = 0.8, n.cut = 1, pri.cut = 0.7,
                 dir.exp = c("support", "efficacy", "belonging", "ai_use"))   # 方向性预期：都预期"存在"有利于结果
edu_save(res, "fsqca_high_engagement")
edu_save(edu_fsqca(d, "engagement", vars[-1], anchors, neg.out = TRUE, dir.exp = c("~support", "~efficacy", "~belonging", "~ai_use")), "fsqca_low_engagement")
edu_save(edu_fsqca_robust(d, "engagement", vars[-1], anchors,
                          variants = list(base = list(), incl_085 = list(incl.cut = 0.85), pri_075 = list(pri.cut = 0.75),
                                          anchors_alt = list(anchors = anchors_alt))), "fsqca_robustness")
```
`anchors_alt` 是另一套有依据的锚点（如 90%、50%、10% 分位数），稳健性检验前先定义好。

输出：校准后隶属度；单个条件的必要性分析（一致性、覆盖度）；真值表；复杂解、简约解、中间解（各组态的一致性、PRI、原始覆盖度、唯一覆盖度）及总体一致性、覆盖度；Fiss 式组态表（● 核心存在，• 边缘存在，⊗ 核心缺失，⊘ 边缘缺失）。

**常用标准**：必要条件一致性 ≥ .90；真值表一致性阈值 ≥ .80（常用 .80–.85），PRI ≥ .70（常用 .65–.75），频数阈值 1–3；组态和总体一致性 ≥ .75–.80。核心条件是同时出现在简约解和中间解中的条件，只出现在中间解中的为边缘条件。

**报告**
1. 校准锚点表（各变量的三个锚点及依据）。
2. 必要性分析表：没有条件的一致性超过 .90，说明单个条件都不构成必要条件。
3. 组态表（核心、边缘），写明总体一致性和覆盖度。按组态命名（如"支持驱动型""效能主导型"），逐条解释条件之间如何组合。
4. 非高结果的组态分析，说明因果非对称性。
5. 稳健性检验：改变一致性阈值、PRI 阈值或校准锚点后，组态基本一致（子集或超集关系）。

**常见错误**
- 用中间解的全部条件当作核心条件。
- 校准锚点按结果反复调整。
- 只报告高结果的组态，不做非高结果分析和稳健性检验。
- 把组态写成"因果机制已被证实"；fsQCA 揭示的是集合关系。
