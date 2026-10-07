# 方法卡：主题模型（结构主题模型 STM）

**适用**：大量开放题回答、学习反思、论坛帖子、政策文本，归纳"文本里谈了哪些主题"，并检验主题比例是否随年级、组别、时间等协变量变化。文本少于约 100 篇或研究者需要逐句解释时，改用 edu-qual 的人工编码；主题模型适合作为大样本文本的探索与补充。

**先检查**
- 中文必须先分词（两步流程，见下）。准备领域用户词典（如"翻转课堂""核心素养"），避免专有名词被切开；准备停用词表（虚词、"老师""觉得"等没有区分力的高频词）。
- 去掉模板化文本（如"无""没有意见"）和重复提交；每篇文档至少几个有效词。
- 协变量没有缺失（含缺失的文档会被删除，结果中写明）。

**调用**

第一步，用仓库的 .venv Python 分词（jieba），把文本列替换为空格分隔的词：
```
.venv/Scripts/python.exe <本skill>/scripts/segment_zh.py --input 数据.csv --column answer \
    --output 数据_seg.csv --userdict 用户词典.txt --stopwords 停用词.txt
```
用户词典一行一个词（可加词频和词性），停用词表一行一个词（UTF-8）；`--min-length 2` 可去掉单字词。停用词表可由 R 生成：`writeLines(stopwords::stopwords("zh", source = "misc"), "停用词.txt")`，再补充本研究的无意义高频词。

第二步，在 R 中建模（英文文本用 `segmented = FALSE`，`stopwords = stopwords::stopwords("en")`）：
```r
source("edu_methods.R"); source("edu_methods_patterns.R")
d <- read.csv("inputs/数据_seg.csv", fileEncoding = "UTF-8")
res <- edu_topics(d, "answer", k = 3:10, segmented = TRUE, covariates = c("grade", "group"), id_col = "id")
edu_save(res, "topics")      # 读过相邻 k 的主题后，用 k_final = 6 重跑并保存
```
输出：`corpus`（文档数、词表大小、词数）；`search`（各 k 的语义一致性、排他性、留出似然、残差）；`topics`（各主题平均比例、主导文档数、语义一致性、排他性、最高概率词、FREX 词）；`representative_docs`（各主题最典型文档的 ID 与比例，只给 ID，原文自己去读）；`theta`（每篇文档的主题比例）；`effects`（有协变量时，estimateEffect 的系数、SE、t、p）。

**判断标准**
- k 没有唯一正确值：在语义一致性（Mimno et al., 2011）与排他性的权衡前沿上选几个候选 k，读各候选的 FREX 词和代表文档，选主题可解释、互不重叠的那个（Roberts et al., 2014, 2019）。未指定 `k_final` 时函数按两指标标准化之和取一个起点，不能直接当结论。
- 每个主题由研究者结合 FREX 词与代表文档命名；无法命名或混杂的主题如实报告。
- 协变量效应：estimateEffect 系数表示协变量变化时预期主题比例的变化，p < .05 视为显著，属于关联。

**报告**
1. 方法：语料来源与规模、分词工具（jieba，用户词典 n 词、停用词 n 词）、预处理、选 k 依据（附 searchK 图或表）。
2. 主题表：主题名、平均比例、FREX 前 10 词、代表性文本摘录（脱敏）。
3. 句子："STM 结果表明，学生反思文本可归纳为 6 个主题，其中'同伴互评'主题比例最高（21.4%）。与对照班相比，实验班讨论'元认知调节'主题的比例更高（b = .062，SE = .015，p < .001）……"

**常见错误**
- 中文不分词或不去停用词就建模，主题被"的、了、我们"占据。
- 只报告一个 k、不给选择依据；或只看指标不读原文就命名主题。
- 把主题比例当作经过验证的测量变量直接进入回归，而不说明其局限。
- 报告 LDA/STM 结果却不写随机种子、初始化方法和预处理细节，结果无法复现。
