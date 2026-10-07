---
name: edu-response
description: Respond to journal peer review for education research papers in Chinese (CSSCI) or English (SSCI) - split reviewer and editor comments into a tracked list, decide an action for each, revise the manuscript with real analyses and verified sources, and deliver a point-by-point response letter or 修改说明, a red-marked revised manuscript and a cover letter, with checks that every comment is answered and every claimed change exists in the revised manuscript. Use for 返修、退修、修改说明、审稿意见回复、回复审稿人、外审意见、大修、小修、修改稿标红、response to reviewers, rebuttal letter, revise and resubmit, major revision, minor revision, cover letter for resubmission.
---

# 教育学论文返修回复

用户提供审稿意见（编辑信和各审稿人意见）和原稿即可，有自己的想法或已改的部分一并给。原稿最好是投稿时的 Word 文件；只有 Markdown 或文本时，先用 `<本skill>/../edu-writing/scripts/md_to_docx.py` 转成 Word 作为原稿。期刊、语言和决定类型（大修、小修、退修再审）从材料中读出；读不出时问一句。被拒稿后改投别刊不走这里，按 edu-writing 修改原稿。

## 步骤

1. **拆意见，建清单。**把每条意见原文拆成一行，存为 `comments.csv`：`id`（R1-1、R2-3；编辑意见 E-1；一条里有几个要求就拆成 R1-2a、R1-2b）、`reviewer`、`comment`（原文逐字）、`type`（major / minor / editorial）、`category`、`request`（要求做什么）、`action`（采纳 / 部分采纳 / 说明不改 / 待核实）、`needs`（新分析 / 新数据 / 用户材料 / 文献 / 改写 / 格式）。分类和处理决策见 [意见分类与处理](references/comment-actions.md)。
2. **先定处理方案，确认一次。**用一屏给用户看：每条意见打算怎么处理，重点列出三类——打算不改或部分采纳的（附理由）、需要新分析的、需要用户补材料的（新数据、伦理审批、原始问卷等）。用户确认后一次做完，不逐条确认。用户暂时给不了的材料（原始数据、量表来源、伦理批件）不等，先完成其余修改，缺的地方按第 3 步留占位。
3. **改稿。**
   - 在原稿的新副本上改，修改规则同 edu-writing 的 [修改原则](../edu-writing/references/foundation.md)：保留原有论证，只改意见涉及和由此连带需要改的地方。
   - 新分析交给 edu-analysis 实际运行，引用新文献按 edu-writing 的 [引用核验](../edu-writing/references/reference-verification.md)。结果和文献不能编造或"预估"。
   - 每处修改记下位置（章节、段落或页码）和修改后的原文，供回复引用。
   - 结果因新分析而改变时，同步改摘要、讨论和结论。
   - **缺材料时留占位，不编造**：在修改稿和回复的对应位置写 `【待补①：需要什么】`，编号与 `作者待办.md` 对应。有占位的回复不能写成"已补充"，写"待补充后填入"。
   - 实质改动按 [修改原则](../edu-writing/references/foundation.md) 分三类记入 `修改记录.md`（原稿论证图、每处改动的位置、原文、新文和理由）。
4. **写回复。**格式和语气见 [回复格式与语气](references/response-format.md)，模板见 `templates/`：
   - 中文期刊：修改说明（逐条：审稿意见—修改说明—修改位置）；
   - 英文期刊：point-by-point response letter，加一封简短的 cover letter。
   - 审稿人意见互相冲突、某项要求无法完成时，另写给编辑部的说明（中文用 `templates/editor-note-zh.md`，英文写进 cover letter）。
   - 与具体意见无关、但标红稿中能看到的改动（统一术语、改正引用编号等），在修改说明末尾的"其他修改"中列出。
   - 每条回复写清做了什么、改在哪里，引用修改后的原文；不改的给出有依据的理由。各审稿人分开回复。
5. **检查。**运行
   ```
   python <本skill>/scripts/check_response.py --comments comments.csv --response 修改说明.md --revised 修改稿.docx
   python <本skill>/scripts/redline.py --original 原稿.docx --revised 修改稿.docx --output 修改稿_标红.docx
   python <本skill>/../edu-writing/scripts/check_consistency.py --draft 修改稿.docx
   ```
   第一个脚本查：每条意见是否都有回复、回复是否给出修改位置、回复中引用的"修改后原文"是否真的在修改稿里（引用被删的原文时写明"删去……"）、回复中的数字是否能在修改稿中找到、未完成的占位、防御性措辞和"留待未来研究"式的推托；还统计回复和修改稿中剩余的占位，不为零时显示 NOT READY TO SUBMIT。第二个生成标红稿（新增内容标红，表格留在原位置；加 `--show-deletions` 同时显示删除线）和改动清单 `changes.csv`；原稿排版复杂时，也可以用 Word 的"审阅 > 比较"生成修订稿。第三个查修改稿内部是否前后一致。脚本只列线索，逐条核对后再交付。
6. **交付。**修改说明或回复信、标红稿、修改稿清洁版、cover letter 或致编辑部说明（需要时）、`comments.csv`、`修改记录.md`，以及 `作者待办.md`（补数据、用户材料、待核实的文献、作者信息、期刊系统中的填写）。还有占位时，在修改说明开头标明"待补版，请勿直接提交"，补齐后重新生成标红稿并重跑第 5 步。文件存在 `edu_output/response/<新任务文件夹>/`。中文 Word 用 `<本skill>/../edu-writing/scripts/md_to_docx.py` 生成。

## 红线

- **只写实际做了的修改。**回复中说"已补充""已重新分析"的，修改稿里必须真的有，并给出位置。
- **新分析必须实际运行，新文献必须核验。**审稿人要求的分析做不了（没有数据、设计不允许）时如实说明，作为局限写进稿件，不编造结果。
- **不为迎合审稿人改变结论的性质。**例如把相关研究写成因果、删掉不利结果，礼貌说明理由，不照改。
- **不防御，也不讨好。**不写"审稿人误解了""显然"；也不为每条意见反复致歉。不同意时用证据说明，能给出折中做法的给出。
- **各审稿人独立回复。**不把一位审稿人的意见告诉另一位，除非编辑信已经公开；审稿人意见互相冲突时，在给编辑的说明里交代取舍。

诚信要求另见 [共同规则](../edu-shared/references/integrity.md)。
