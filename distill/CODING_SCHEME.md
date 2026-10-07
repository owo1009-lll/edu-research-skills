# 写作立场编码方案（讨论、结论、局限、启示）

目的：看已发表教育学论文如何陈述发现、解释原因、处理不显著结果、声明贡献、写启示和局限，为 skill 的语气规则提供依据。只编码 `## DISCUSSION`、`## CONCLUSION`、`## LIMITATIONS`、`## IMPLICATIONS` 及摘要；没有这些标记的论文读最后两个一级标题下的内容。

每篇输出一个 JSON 对象，字段如下。摘录只用于本地分析，每条不超过 60 个汉字或 40 个英文词。

| 字段 | 内容 |
|---|---|
| `id` | 语料编号 |
| `opening_move` | 讨论第一段做什么：`restate_findings`（复述主要发现）/ `answer_rq`（逐个回答研究问题）/ `context`（先回到背景）/ `other`；附第一句摘录 |
| `finding_statements` | 讨论中复述发现的句子：总数，直接陈述数（"研究发现X显著影响Y""results showed"），带限定词数，紧跟免责句数（"但不能说明……"）；各附 1–2 条摘录 |
| `explanation_moves` | 解释发现的方式及次数：`theory`（用理论解释机制）、`literature_consistent`（与已有研究一致）、`literature_inconsistent`（与已有研究不一致并解释原因）、`context`（用研究情境解释）、`alternative`（并列多种解释）；记录解释句里用了什么程度的限定（无 / 一个限定词 / 多个） |
| `null_or_unexpected` | 不显著或与假设相反的结果怎么写：直接报告后解释原因 / 一笔带过 / 作为局限 / 未出现；附摘录 |
| `contribution` | 是否明确声明贡献（理论 / 实践 / 方法），位置（讨论开头、结论、单独小节），句式摘录 |
| `implications` | 启示的形式：编号条目（一是、二是 / First, Second）还是段落；祈使强度（应当、需要、可以 / should, could, may）；条目数 |
| `limitations` | 位置（`own_section` 单独小节 / `final_paragraph` 末段 / `scattered` 散在各段 / `absent`），句数，内容类型（样本、设计、测量、推广、其他），是否转成后续研究方向；讨论正文里出现的"不能证明/不能推断"类免责句数 |
| `voice` | 整体立场：`assertive` / `balanced` / `cautious`，一句理由 |
| `patterns` | 2–4 个最有代表性的句式，改写成带槽位的模板（如"X对Y具有显著正向影响（β=__），H1得到支持。这与__的研究结论一致，说明__。"），不照抄原句 |

汇总时报告各类别的篇数和比例，按中文 CSSCI 与英文 SSCI 分开，并各给 3 条最能体现差异的规律。
