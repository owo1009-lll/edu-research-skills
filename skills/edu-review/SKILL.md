---
name: edu-review
description: Simulate peer review of an education research manuscript or grant application before submission - two or three independent reviewer reports (methods, field and theory, and optionally an editor's view) with numbered major and minor concerns, each tied to a location in the manuscript and a test for when it is resolved, then a synthesis of consensus problems and a prioritized revision list, for Chinese (CSSCI) or English (SSCI) journals. Use for 模拟审稿、投稿前自审、外审模拟、审稿人视角、预审、帮我挑毛病、论文哪里会被拒、申报书评审视角、mock peer review, pre-submission review, reviewer report.
---

# 教育学论文外审模拟

用户提供稿件（或申报书）即可，目标期刊或基金类别有就一并说明。这是 AI 模拟的审稿，用来在投稿前找出问题；不是真实的专家评审，不预测录用概率。要写回复真实审稿意见时用 edu-response。

## 步骤

1. **读稿，定范围。**确认是全文还是部分章节、目标期刊（中文或英文）或基金类别、研究类型（定量、定性、混合、理论）。只给了部分章节时，审稿范围限于这部分，并写明哪些判断因缺少材料而无法做出。
2. **先跑脚本，作为审稿材料。**在用户的项目文件夹中运行（`<本skill>` 是本 skill 所在的文件夹），输出存到任务文件夹的 `script_outputs/`，供各审稿人读取：
   ```
   python <本skill>/../edu-writing/scripts/check_consistency.py --draft 稿件.docx --term-group 学习投入=学习投入|学业投入
   python <本skill>/../edu-audit/scripts/check_reporting.py --draft 稿件.docx
   ```
   前者查摘要与正文、样本量、数值精度、术语、图表和引用编号是否前后一致；它会自动比对关键词的一字之差写法，其他核心构念先通读稿件，把同一构念的不同写法用 `--term-group 名称=写法1|写法2` 传入。后者查统计报告是否完整。脚本输出只是线索（例如数值相同的两个量可能是不同的统计量），审稿人回到原文核实后才写进意见。
3. **独立写审稿报告。**设两到三位审稿人，每人负责的维度见 [审稿维度](references/review-criteria.md) 的"审稿人分工"：
   - R1 方法与数据；
   - R2 领域与理论；
   - R3（可选）编辑视角。

   先按"审稿人分工"为每人写一份审稿要求（负责的维度、目标期刊、语言、报告格式），存到任务文件夹的 `briefs/`。

   **独立性**：宿主支持子任务（如 Claude Code 的子代理、Codex 的子任务）时，每位审稿人在单独的子任务中审稿，只拿到稿件、`script_outputs/` 和自己的审稿要求，看不到其他人的报告。不支持时依次写，每份报告定稿后再写下一份，写后面的报告时不回头修改前面的。
4. **按格式写意见。**格式见 [报告格式](references/report-format.md)。每条主要问题都有编号（R1-M1）、是否阻断、维度、论断位置、证据位置、问题、为什么重要、怎样算解决；次要问题（R1-m1）写位置和问题与建议。字段内容较长时可以在字段下分条缩进。语言与稿件一致。
5. **综合。**所有报告定稿后再综合：共识的优点；阻断性问题（每条注明由哪几位审稿人提出，只有一位提出的也列入）；其他主要问题；审稿人之间的分歧（包括同一问题严重程度判断不同）；一致性和报告规范问题；最后给出按优先级排列的修改清单，每项注明对应的问题编号和由谁处理（重新分析交 edu-analysis，需要原始数据；改写交 edu-writing）。每条主要问题都要在综合中出现。
6. **检查并交付。**在任务文件夹中运行
   ```
   python <本skill>/scripts/check_review.py --reports R1.md R2.md R3.md --synthesis synthesis.md
   ```
   它检查每条问题的必填字段、阻断标记、证据位置、编号是否重复、综合中引用的编号是否存在、主要问题是否都进入了综合，以及是否出现录用预测（说明"不预测录用概率"的句子不算）。交付 `synthesis.md` 和各审稿报告 `R1.md`……；用户要一个文件时，用 `<本skill>/../edu-writing/scripts/md_to_docx.py` 合成 Word，综合报告在前、各审稿报告在后。文件存在 `edu_output/review/<新任务文件夹>/`。用户要按清单修改时，转到 edu-writing（修改原稿流程）。

## 审稿立场

- **对稿件，不对人。**意见针对稿件中可以指出位置的内容；每条主要问题都给出原文位置和依据。
- **具体可改。**"怎样算解决"写成可检验的标准（例如"报告 HTMT 且均低于 0.85"），不写"需要进一步完善"。
- **分清严重程度。**阻断性问题是不解决就无法支持主要结论的问题；表述和格式问题归为次要。不为显得严格而罗列问题，也不为显得友好而略过致命问题。
- **不越界。**不臆测作者身份，不要求引用与本文无关的文献，不预测录用概率，不称为专家评审。
- **申报书模式**：评审维度换成选题价值、论证、研究设计与可行性、创新、研究基础与预期成果（见 [审稿维度](references/review-criteria.md) 的申报书部分），同时检查活页匿名要求；字数、身份信息和"首次""填补空白"等措辞用 `python <本skill>/../edu-proposal/scripts/check_proposal.py --draft 活页.docx --preset qgjk` 检查（其他基金用 `--limit` 和 `--section-limit` 按当年模板设置）。

诚信要求另见 [共同规则](../edu-shared/references/integrity.md)。
