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
| 样本中有哪些潜在亚群（剖面） | 连续指标（量表均分、因子得分） | 潜在剖面分析（LPA，mclust）（试用） | [潜在剖面与潜在类别](methods/latent-profile.md) |
| 按作答模式把人分成类别 | 二分或类别题目 | 潜在类别分析（LCA，poLCA）（试用） | [潜在剖面与潜在类别](methods/latent-profile.md) |
| 题目难度、区分度、测验精度与能力估计 | 二分题或有序题，单维 | IRT：Rasch、2PL、等级反应模型（mirt）（试用） | [项目反应理论](methods/irt.md) |
| 非随机分组的干预效果（自愿参加、选择性进入） | 干预组 + 对照组，干预前协变量 | 倾向得分匹配（MatchIt + cobalt 平衡检验）（试用） | [准实验因果推断](methods/causal-inference.md) |
| 政策或试点在实施前后的效果 | 干预组/对照组 × 前/后；多期面板 | 双重差分；事件研究；交错实施用 Sun & Abraham（试用） | [准实验因果推断](methods/causal-inference.md) |
| 分数线、门槛决定是否受干预 | 连续运行变量 + 门槛 | 断点回归（rdrobust，稳健偏差校正）（试用） | [准实验因果推断](methods/causal-inference.md) |
| 合并多项研究的效应、异质性与调节因素 | 各研究的均值/标准差/n、相关或 2×2 表；同一研究多效应量 | 随机效应元分析、元回归/亚组、Egger 与剪补法、逐一剔除、三水平元分析（试用） | [元分析](methods/meta-analysis.md) |
| 影响有序等级结果的因素 | 有序因变量（3–5 级） | 有序 Logistic 回归 + 比例优势检验（试用） | [有序、多项与计数](methods/glm-extensions.md) |
| 影响无序多类别选择的因素 | 三类及以上无序因变量 | 多项 Logistic 回归（试用） | [有序、多项与计数](methods/glm-extensions.md) |
| 影响次数的因素 | 计数因变量（常有过度离散、零多） | Poisson / 负二项 / 零膨胀或障碍模型（试用） | [有序、多项与计数](methods/glm-extensions.md) |
| 数据支持"有差异"还是"无差异" | 连续，两组、配对、多组、回归或相关 | 贝叶斯因子检验（BayesFactor）（试用） | [贝叶斯检验](methods/bayesian.md) |
| 学生可分成哪几类（描述性类型） | 多个连续指标 | 聚类分析（k-means / Ward / PAM，轮廓系数、间隙统计量、ARI）；需要类别数检验时用 LPA（试用） | [聚类分析](methods/cluster.md) |
| 谁处在互动中心、有没有小团体 | 边列表（回帖、同伴提名、合作） | 社会网络分析（密度、互惠、中心性、社群与模块度）（试用） | [社会网络](methods/network.md) |
| 哪些行为常紧接着发生；学习轨迹有哪几种 | 行为编码日志（ID、顺序、编码）；按时间网格的状态序列 | 滞后序列分析（调整残差、Yule's Q）；序列分析（OM + 聚类）（试用） | [学习日志](methods/learning-logs.md) |
| 大量文本谈了哪些主题，主题比例是否随组别变化 | 开放题、反思、论坛帖子（中文先分词） | 结构主题模型（STM，searchK，estimateEffect）（试用） | [主题模型](methods/topic-model.md) |
| 访谈、开放题编码 | 文本 | 转到 edu-qual（主题分析、内容分析、扎根理论、编码一致性） | ../../edu-qual/SKILL.md |

标"试用"的方法已用已发表数值或解析解核对，但还没有在真实研究数据上用过，结果要多看一遍。这些方法用到的 R 包不在基础安装里，首次使用时运行 `Rscript scripts/setup_packages.R --all` 安装。

## 常见组合

- **问卷 + SEM 论文**：描述统计 → 信度与效度（α、CFA、CR/AVE、HTMT）→ 共同方法偏差（Harman）→ 相关矩阵 → 结构模型与中介或调节。
- **SEM + fsQCA + NCA**（对称与非对称互补）：SEM 检验净效应；NCA 判断哪些条件是"必要"的；fsQCA 找出导致高结果的条件组合。三者使用同一套变量，fsQCA 用校准后的隶属度，NCA 一般用原始得分或潜变量得分。
- **准实验**：前测等同性检验（t 或卡方）→ 后测比较（协方差分析可用回归实现：后测 ~ 组别 + 前测）→ 效应量。

## 不要这样做

- 不把所有检验都跑一遍再挑显著的报告；看过结果后新增的分析标为探索性。
- 学生嵌套在班级里时，不直接当独立样本做 t 检验或回归，先算 ICC。
- 横截面数据的中介、路径和组态结果，写成"关联""路径""条件组合"，不写成因果机制。
