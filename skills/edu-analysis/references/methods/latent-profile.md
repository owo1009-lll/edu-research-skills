# 方法卡：潜在剖面分析（LPA）与潜在类别分析（LCA）

**适用**：以人为中心，找出样本中未被观察到的亚群（如"高投入—低焦虑型"学习者）。指标为连续得分（量表均分、因子得分）时用 LPA；指标为类别或二分题目（是/否、选项）时用 LCA。研究问题是"变量之间的关系"时，用回归或 SEM，不用 LPA/LCA。

**先检查**
- 样本量：一般至少 300–500；类别分得越细，最小类所需的人数越多。
- 指标 3–10 个，方向一致；LPA 的指标量纲不同时保留 `scale = TRUE`（默认），剖面均值仍按原始单位报告。
- LCA 的题目类别不宜太多（稀疏表会让 G² 失效）；字符型选项按字母排序，想按原顺序显示就先转成有序 factor。
- 两种方法都只用完整个案，缺失比例高时先报告缺失情况。

**调用**
```r
source("edu_methods.R"); source("edu_methods_latent.R")
d <- read.csv("inputs/data.csv", fileEncoding = "UTF-8")
vars <- c("motivation", "anxiety", "selfreg", "engagement")
lpa <- edu_lpa(d, vars, k = 1:6, models = c("EEI", "VVI"), nboot = 100)
edu_save(lpa, "lpa_enumeration")                      # 先看 fit 表，确定类别数
edu_save(edu_lpa(d, vars, k = 1:6, choose_k = 3, choose_model = "EEI"), "lpa_3profiles")
lca <- edu_lca(d, paste0("q", 1:8), k = 1:5, nrep = 20)  # 题目为类别变量
edu_save(edu_lca(d, paste0("q", 1:8), k = 1:5, choose_k = 3), "lca_3classes")
```
输出：`fit`（每个解的 LL、参数数、AIC、BIC、SABIC、熵、最小类占比与人数；LPA 另有 BLRT 的 LRTS 与 p，第 k 行检验 k−1 类对 k 类；LCA 另有 G²、X²、df 及最优对数似然被多少个随机起点重复得到）；`profile_sizes`/`class_sizes`（模型估计比例、按最大后验归类的人数、各类平均后验概率 AvePP）；`profile_means`（原始单位）与 `profile_means_z`，或 `item_probabilities`（各类在每个选项上的条件概率）；`membership`（每人的所属类别与后验概率）。未指定 `choose_k` 时，函数暂按"最小类 ≥ 5% 中 BIC 最小"给出剖面表，这只是起点，不是结论。

**判断标准**（Nylund, Asparouhov & Muthén, 2007；Masyn, 2013；Weller, Bowen & Faubert, 2020）
- 信息准则：BIC 与 SABIC 越小越好，BIC 在模拟中最可靠；AIC 倾向于过多分类，只作参考。BIC 持续下降时看下降幅度（"肘部"）。
- BLRT：k 类对 k−1 类 p < .05，说明 k 类优于 k−1 类；第一次不显著时，通常取前一个 k。
- 熵 ≥ .80 表示分类清晰（Clark & Muthén, 2009），AvePP ≥ .70（Nagin, 2005）；熵不是选 k 的依据，只说明分类精度。
- 最小类占比 ≥ 5%（或至少约 25–50 人），太小的类难以重复、难以解释。
- 可解释性：每一类在理论上有意义、彼此在形状上（而不只是高低水平上）有区别。
- LCA 的 `best_ll_replicated` 只有 1/nrep 时，说明可能是局部最优，增大 `nrep` 重跑。
- 模型（LPA）：EEI 是 Mplus 默认的等方差模型；VVI 允许各剖面方差不同。两个模型的结论一致时更可信。

**报告**
1. 类别数比较表：k、LL、参数数、AIC、BIC、SABIC、熵、BLRT p、最小类比例。
2. 决策句："综合 BIC 与 SABIC 的拐点、BLRT（3 类对 2 类 p < .01，4 类对 3 类 p = .43）、熵（.89）与最小类比例（14.2%），并考虑各剖面的可解释性，选择三剖面模型。"英文可写 "Following Nylund et al. (2007), we retained the three-profile solution: BIC and SABIC flattened after three profiles, the BLRT favoured three over two profiles (p < .01) but not four over three (p = .43), entropy was .89, and the smallest profile held 14.2% of the sample."
3. 剖面均值图（原始或标准化均值折线图）或条件概率表，给出各类命名、人数和比例。
4. 注明软件与设定：mclust 模型（如 EEI）、BLRT 重复次数、LCA 随机起点数。

**类别与结果变量的关系（三步法/BCH）**：不要把 `membership` 中的类别当作没有误差的观测变量直接做方差分析或回归，这会低估效应、低估标准误（熵越低偏差越大）。前因变量用 R3STEP（Vermunt, 2010），结果变量用 BCH（Bolck, Croon & Hagenaars, 2004；Asparouhov & Muthén, 2014），可在 Mplus、Latent GOLD 或 R 的 tidySEM 中实现；本函数不提供。只能用归类变量时，在熵 ≥ .80 的前提下，把结果写为描述性比较，并说明这一局限。协变量也不要直接加进类别模型，否则会改变类别本身。

**常见错误**
- 只凭某一个指标（如熵最高、AIC 最小）选类别数，或选了一个不到 5% 的小类。
- 把熵当作模型拟合指标。
- 不报告未选择的解，只报告最终模型。
- 用类别解释因果（"属于高投入型导致成绩更好"）；横截面类别只是描述。
- LCA 不检查局部最优（只用一个随机起点）。
