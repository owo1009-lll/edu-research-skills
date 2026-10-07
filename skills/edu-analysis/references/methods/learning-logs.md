# 方法卡：学习日志与行为序列（滞后序列分析 LSA、序列分析）

**适用**：平台日志、讨论帖、课堂视频的行为编码，回答"哪些行为常紧接着发生"（滞后序列分析）和"学生的学习轨迹有哪几种类型"（序列分析）。两者都要求数据是长格式：一行一个事件，含学习者（或小组）ID、时间或顺序号、行为编码。

**先检查**
- 编码方案和编码一致性先完成（Cohen's κ，见 edu-qual）；编码类别 4–10 个为宜，过多会使每格期望频数不足。
- LSA：同一编码连续出现时是否已合并？合并过则自身转换不可能，设 `self_transitions = FALSE`（准独立模型）。转换总数最好达到期望频数普遍 ≥ 5（Bakeman & Quera, 2011）。
- 序列分析：所有序列要放在同一时间网格上（周、课时、第 n 次登录），每个 ID 每个时点只有一个状态；中间缺失保留为缺失，不要用前值填补后不说明。

**调用**
```r
source("edu_methods.R"); source("edu_methods_patterns.R")
d <- read.csv("inputs/log.csv", fileEncoding = "UTF-8")      # student, seq_no, code
lsa <- edu_lsa(d, actor = "student", order = "seq_no", code = "code", lag = 1)
edu_save(lsa, "lsa")
w <- read.csv("inputs/weekly.csv", fileEncoding = "UTF-8")   # student, week, state
sq <- edu_sequence(w, id = "student", time = "week", state = "state", k = 2:6)
edu_save(sq, "sequence")   # 定 k 后可用 k_final = 3 重跑
```
LSA 输出：`summary`（转换总数、独立性卡方）、`transitions`（每个"前→后"的观察频数、期望频数、条件概率、调整残差 z、Yule's Q、符号）、`observed` / `z`（矩阵）、`significant`（z > 1.96 的显著转换）。序列分析输出：`states`（各状态平均持续时间）、`distribution`（各时点状态比例与熵，即状态分布图数据）、`transition_rates`（状态转换率）、`cluster_fit`（各 k 的平均轮廓系数）、`types`（各序列类型人数、代表序列、状态占比）、`membership`。

**判断标准**
- LSA：调整残差 z > 1.96 表示该转换显著高于随机水平（Allison & Liker, 1982; Bakeman & Quera, 2011），用 Yule's Q（-1 到 1）表示强度（Bakeman et al., 1996）：z 随转换总数增大，Q 不随样本量变化，适合跨研究比较。格子多时注意多重比较，可用 Bonferroni 校正后的临界值。
- 序列分析：最优匹配（OM）距离，替换成本按转换率设定（`sm = "TRATE"`），再做 Ward 聚类（Gabadinho et al., 2011）；平均轮廓系数 > .50 类型清晰，.25–.50 一般，< .25 结构弱。成本设定会影响分类，至少用另一种成本（如 `sm = "CONSTANT"`）检查稳健性（Studer & Ritschard, 2016）。

**报告**
1. LSA：调整残差表（显著格加粗）和行为转换图（只画 z > 1.96 的箭头，标注 z 值）；句子："共得到 1 284 次行为转换。KC1→KC2（z = 4.12，Q = .48）和 KC2→KC3（z = 3.05，Q = .39）显著，说明学生在分享观点后倾向于提出质疑……"
2. 序列分析：状态分布图、各类型的人数与代表序列、类型间状态占比比较；写明 OM 成本、聚类方法和选 k 依据。
3. 类型可作为分组变量，与成绩等外部变量做比较（见组间差异卡）。

**常见错误**
- 把不同学生的日志首尾相接算转换（函数已在学习者内部计算转换）。
- 合并了连续重复编码却仍用独立模型计算期望频数，自身转换的期望值被错估。
- 把显著转换写成因果（"A 导致 B"）；LSA 只说明先后关联。
- 只用 GSEQ 截图而不报告转换总数、期望频数和效应量。
- 序列聚类的 k 只凭直觉，不报告轮廓系数和成本设定。
