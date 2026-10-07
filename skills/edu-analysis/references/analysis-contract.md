# 内部方案与计算语义

方案由助理根据问题和材料制作。参考 `tests/fixtures/paths_plan.json`（合成数据）；不要猜测变量含义。执行代码为基础 R + jsonlite，用 `python scripts/run_r.py --adapter basic --plan <plan.json>` 运行，结果写入 `edu_output/analysis/`。

## 必须显式保存的设置

- `data`：项目内UTF-8 CSV；`question`及每项`purpose`；`na_strings`。
- `design`：`unit,id,row_structure,cluster_columns,independence_basis`。行结构只接受`one_per_unit`或`paired_wide`；配对列按同一行唯一ID对齐。ID可以按冻结行序生成，但必须注明不是原始身份编号。字段名扫描仅辅助识别嵌套，不能替代研究设计说明。已观察多个班级/学校等簇时，本批拒绝独立推断；也不支持仅因个体ID唯一就把重复测量视为独立。
- `variables`字典：数值`type,meaning,source`及已知`min,max,allowed`；类别另需`levels,labels,reference`。原始代码与参照组不可由字母排序决定。
- `scales`：每项`name,items,min,max,reverse,aggregation,min_items,source,missing_rule`。反向=min+max−原值；均值或总分，不覆盖原列。部分题目总分只接受显式`sum_method: prorated`，不得默默把缺题记零。各题异质范围或权重未适配。
- `seed,bootstrap_replicates,confidence`；运行记录区间算法、有效重抽次数与种子。固定种子不代表区间覆盖率已认证。
- `analyses`：唯一安全`id`、`method,purpose,missing`，可选`filters`仅支持`operator: in`的明确取值。推断为选定变量完整案例；描述按每变量可用案例。每项保存总数、资格数、完整数、缺失数与实际ID（私有）。

## 方法参数与区间

| method | 额外参数 | 估计与不确定性 |
|---|---|---|
| descriptive | variables，可选group | n、均值、SD、中位数、范围；均值Student t区间 |
| alpha | scale | 原始Cronbach α，完整计分题；行Bootstrap百分位区间 |
| pearson / spearman | x,y | Pearson r的Fisher z区间；Spearman用有并列值的渐近t检验p及成对行Bootstrap区间 |
| independent_t | outcome,group,groups,variance=welch/pooled | 明确第一组−第二组均值差及t区间；精确gamma校正的Hedges g与分组Bootstrap区间；g仍用合并SD |
| paired_t | x,y；paired_wide | x−y差与t区间；缺失整对剔除；Cohen dz与成对Bootstrap区间 |
| anova | outcome,group,variance=classical/welch | 总体F、两个df与p；组间平方和/总平方和η²及分组Bootstrap区间，无自动多重比较 |
| regression | outcome,predictors,inference=OLS/HC3 | 加性普通线性模型、原单位系数、OLS及HC3区间/p、R²/调整R²；明确选用哪一种推断 |

η²在Welch旁是经典平方和构成的描述性效应，不冒称Welch专属校正效应；小样本百分位区间与参数边界仍有偏差。Bootstrap使用百分位法、R quantile type7；至少200次，仅>=80%有效时计算并报告有效数。正式高风险推断可另评估更适合的区间，本批不宣称已有BCa。

HC3协方差为 `(X'X)^-1 X' diag(e²/(1-h)²) X (X'X)^-1`；以残差df的t分布计算近似区间/p。本批不输出虚构的标准化系数；回归的条件关联使用原单位说明。

检查包括计分范围、缺失/唯一单位、散点图、差值/残差正态性、ANOVA中位数中心方差诊断、回归残差图、辅助nR²异方差诊断、Cook距离、杠杆和设计列VIF（不是因子GVIF）。不把诊断p>.05称为满足全部假设；不根据诊断p自动切换到最显著检验。秩不足、非数值、未说明类别、超范围和重复单位均报错。

R原始说明：[cor.test](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/cor.test.html)、[t.test](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/t.test.html)、[oneway.test](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/oneway.test.html)。本项目的Bootstrap、报告与样本策略是明确的方法选择，不是R的统一官方要求。

## 线性路径扩展

新增`moderation`、`simple_mediation`、`serial_mediation`，参数与支持类型见[path-extensions.md](path-extensions.md)。助理从材料生成完整内部方案，保留同一样本、时间/路径理由与实际R运行；不是要求用户提供JSON。未支持设计须停止推断并交付缺口。
