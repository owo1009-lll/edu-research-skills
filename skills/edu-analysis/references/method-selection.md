# 选方法

先确认四件事，再查下表：分析单位（学生、班级、学校）、因变量类型（连续、二分类、有序、类别、隶属度）、设计（独立组、配对或重复、嵌套、多时点）、研究问题的形式（差异、关系、路径、组态、必要条件）。用户已指定方法时，核对它与数据是否相符；不相符时说明原因并给出替代方法。

| 研究问题 | 数据 | 方法 | 方法卡 |
|---|---|---|---|
| 样本特征、量表得分分布 | 任意 | 描述统计 | [信度与测量](methods/measurement.md) |
| 量表是否可靠、结构是否成立 | 多题项量表 | Cronbach's α / ω、EFA、CFA、CR/AVE、HTMT、Harman 单因素检验 | [信度与测量](methods/measurement.md) |
| 两组有没有差异 | 连续因变量，独立两组 | Welch t（默认）；非正态或等级数据用 Mann-Whitney U | [组间差异](methods/group-differences.md) |
| 前后测、同一人两种条件 | 连续，配对 | 配对 t；Wilcoxon 符号秩 | [组间差异](methods/group-differences.md) |
| 三组及以上差异 | 连续，独立多组 | 单因素方差分析或 Welch 方差分析；Kruskal-Wallis；事后比较 | [组间差异](methods/group-differences.md) |
| 两个类别变量是否相关 | 类别 × 类别 | 卡方检验；期望频数过小时用 Fisher 精确检验 | [类别数据](methods/categorical.md) |
| 两个变量相关程度 | 连续或等级 | Pearson / Spearman 相关 | [相关与回归](methods/correlation-regression.md) |
| 多个因素对结果的影响，控制背景变量 | 连续因变量 | 分层线性回归 | [相关与回归](methods/correlation-regression.md) |
| 影响"是否"发生 | 二分类因变量 | Logistic 回归 | [相关与回归](methods/correlation-regression.md) |
| 影响是否随条件而变 | 连续因变量 + 调节变量 | 调节效应（交互项、简单斜率） | [调节与中介](methods/moderation-mediation.md) |
| X 通过 M 影响 Y | 连续变量 | Bootstrap 中介（并行或链式） | [调节与中介](methods/moderation-mediation.md) |
| 多个潜变量之间的路径 | 多题项量表，样本较大 | CB-SEM（lavaan） | [结构方程](methods/sem.md) |
| 预测导向、小样本、形成性构念 | 多题项量表 | PLS-SEM（seminr） | [PLS-SEM](methods/pls-sem.md) |
| 哪些条件组合导致结果（多重并发、非对称） | 案例数 10–500，条件 3–7 个 | fsQCA | [fsQCA](methods/fsqca.md) |
| 某条件是否是结果的必要条件、需要到什么水平 | 连续或有序 | NCA | [NCA](methods/nca.md) |
| 学生嵌套在班级或学校中 | 多层数据 | ICC 判断，多层线性模型 | [多层与纵向](methods/multilevel-longitudinal.md) |
| 多次测量的变化 | 三个及以上时点 | 重复测量方差分析、增长模型、CLPM / RI-CLPM | [多层与纵向](methods/multilevel-longitudinal.md) |
| 访谈、开放题编码 | 文本 | 转到 edu-qual（主题分析、内容分析、扎根理论、编码一致性） | ../../edu-qual/SKILL.md |

## 常见组合

- **问卷 + SEM 论文**：描述统计 → 信度与效度（α、CFA、CR/AVE、HTMT）→ 共同方法偏差（Harman）→ 相关矩阵 → 结构模型与中介或调节。
- **SEM + fsQCA + NCA**（对称与非对称互补）：SEM 检验净效应；NCA 判断哪些条件是"必要"的；fsQCA 找出导致高结果的条件组合。三者使用同一套变量，fsQCA 用校准后的隶属度，NCA 一般用原始得分或潜变量得分。
- **准实验**：前测等同性检验（t 或卡方）→ 后测比较（协方差分析可用回归实现：后测 ~ 组别 + 前测）→ 效应量。

## 不要这样做

- 不把所有检验都跑一遍再挑显著的报告；看过结果后新增的分析标为探索性。
- 学生嵌套在班级里时，不直接当独立样本做 t 检验或回归，先算 ICC。
- 横截面数据的中介、路径和组态结果，写成"关联""路径""条件组合"，不写成因果机制。
