# 报告格式

## 数字

- 统计量和系数保留两位小数，p 值保留三位；p < .001 写作"p < .001"，不写"p = .000"。
- 小数位和前导 0：目标期刊没有规定时，中文稿统一保留前导 0、系数和统计量两位小数、p 值三位（如 β = 0.42，p = 0.003，p < 0.001）；英文稿按 APA 第 7 版，不能大于 1 的统计量不写前导 0（r = .32，p = .041，p < .001）。投稿前按目标期刊的样例统一。
- 每个检验同时报告统计量、自由度、p 值和效应量；有区间的报告 95% 置信区间。
- 样本量写实际进入分析的人数，与描述统计中的人数一致。

## 表格

- 中文期刊用三线表：表题在表上方（"表 2 变量的描述统计与相关系数"），只保留顶线、栏目线和底线，注释写在表下（"注：*p < .05，**p < .01，***p < .001"）。
- 英文期刊按 APA 第 7 版：表号加粗（**Table 2**），表题另起一行用斜体，注释以 *Note.* 开头。
- `edu_save()` 输出的 Markdown 表和 CSV 是数据底稿，进入 Word 前按上述格式整理。

## 常用句式

| 场景 | 中文 | English |
|---|---|---|
| t 检验 | 实验组（M = 3.82，SD = 0.61）显著高于对照组（M = 3.41，SD = 0.70），t(118) = 3.42，p < .001，Hedges' g = 0.62。 | The experimental group (M = 3.82, SD = 0.61) scored higher than the control group (M = 3.41, SD = 0.70), t(118) = 3.42, p < .001, g = 0.62. |
| 方差分析 | 三组差异显著，F(2, 147) = 5.21，p = .007，η² = .07；事后比较显示…… | Scores differed across the three groups, F(2, 147) = 5.21, p = .007, η² = .07; post hoc comparisons showed … |
| 卡方 | 性别与选课类型显著相关，χ²(2) = 30.07，p < .001，Cramér's V = .10。 | Gender was associated with course choice, χ²(2) = 30.07, p < .001, V = .10. |
| 回归 | 控制背景变量后，教师支持显著正向预测学习投入（β = .41，p < .001），解释力增加 12%（ΔR² = .12）。 | After controlling for background variables, teacher support predicted engagement (β = .41, p < .001; ΔR² = .12). |
| 中介 | 自我效能的间接效应显著，效应值为 0.18，95% Bootstrap CI [0.09, 0.29]，占总效应的 36%。 | The indirect effect through self-efficacy was 0.18, 95% bootstrap CI [0.09, 0.29], 36% of the total effect. |
| fsQCA | 共得到 3 条组态，总体一致性为 0.87，总体覆盖度为 0.64；其中…… | Three configurations emerged (solution consistency = .87, coverage = .64). |
| NCA | 教师支持是学习投入的必要条件（d = 0.32，p < .001），达到 50% 的学习投入至少需要 28.4% 的教师支持水平。 | Teacher support was necessary for engagement (d = 0.32, p < .001); 50% engagement required at least 28.4% of the support range. |

动词与设计相符：横截面数据写"预测""相关""路径系数显著"，实验或准实验才写"提升""促进"。不显著的结果照常报告并解释，不写成"没有差异"或"两者等效"。
