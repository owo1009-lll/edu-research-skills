---
name: edu-review
description: Review education research manuscripts or grant applications in Chinese or English. Return the original DOCX or PDF with precisely anchored native highlights and comments, preserving prose, figures, citations, existing comments and tracked changes. Distinguish definite errors, items needing verification and argument or expression suggestions. Do not rewrite the manuscript or attach separate reviewer reports unless the user explicitly requests that work. Use for 模拟审稿、审阅、检查论文、指出问题、投稿前自审、外审模拟、审稿人视角、预审、帮我挑毛病、论文哪里会被拒、申报书评审视角、mock peer review, manuscript review, pre-submission review.
---

# 教育学原稿审阅

默认交付**原稿对应位置高亮＋原生批注**，保留正文，不自动改写，不另生成审稿报告或意见单。这是 AI 模拟审稿，不是真实的专家评审，不预测录用概率。用户已明确要求改稿时按授权执行，转到 edu-writing 的原稿修改流程，不再次询问已经明确的事项；回复真实外审意见用 edu-response。

## 审阅与标注

1. **读原稿，确定可判断的范围。**根据全文或所给章节、研究类型、语言及已有目标期刊/基金要求审阅。按 [审阅维度](references/review-criteria.md) 同时看贡献、设计、证据、概念、文献、解释与表达，不把定量标准套到质性研究或把混合研究拆成互不相干的两份检查。
2. **核实问题。**需要时运行 `../edu-writing/scripts/check_consistency.py`、`../edu-audit/scripts/check_reporting.py`；它们只提供线索，回到原文和实际材料判断。缺原始数据不能据此断言统计错误，未检索核实不能宣称没有创新或遗漏关键研究。保留有依据的强判断和有效表达，不机械替换动词或每段增加局限。
3. **把意见锚定到必要文字。**一句有多类问题时用主要问题的颜色，在同一批注中分清各项；不要叠加高亮。同一问题在关键位置写主批注，其他位置简短关联。跨章节问题点明相关位置；全文层面的判断可在标题处写总评批注。没有问题的段落无需标注，不设数量配额。

   | 高亮 | 批注性质 | 依据 |
   |---|---|---|
   | 黄色 | 论证、解释或表达建议 | 说明哪项理解或推理需要改善；可选风格偏好不能写成必须遵守的规范 |
   | 红色 | 明确错误或实质矛盾 | 有可核查依据，指出来源及矛盾；稿内数字不一致不等于已确定哪个值真实 |
   | 蓝色 | 待核实、需补材料 | 明确缺什么及它影响哪项判断，不把“未提供”写成“没有做” |

   批注开头标明性质，必要时注明主要/次要；根据问题说明是什么、为何影响理解或结论、怎样处理。备选表达放在批注内，不替换正文。批注语言跟随稿件；新作者标识统一为 **AI 模拟审稿**。
4. **生成原生标注。**读 [文件与锚点](references/annotations.md)，先用 `scripts/annotate_manuscript.py inventory` 建立原文位置，再根据已核实的问题整理内部标注计划，用 `apply` 输出新文件。Word 用原生文字高亮与批注；PDF 用高亮注释及其关联批注，不强行转换格式。已有正文、图表、引文、格式、批注和修订均保留；不在正文插入“【批注】”冒充原生功能。
5. **检查实际文件后交付。**运行 `scripts/annotate_manuscript.py verify`，核对标注与原文对应、保留情况及计划外变动；实际用 Word/可用阅读器打开并检查。条件允许时渲染检查每页的高亮范围、批注、表格和图。结构通过不等于视觉验收。不能可靠定位或生成时，说明具体受限对象，不伪装完成。

仅交付 `原稿名_审稿标注版.docx` 或 `原稿名_审稿标注版.pdf` 与必要的简短说明；原上传文件保持不动。锚点清单、计划及检查日志留在用户项目 `edu_output/review/<新任务文件夹>/`，不作为独立审稿报告附送。没有实质问题时原样保留并如实说明，不制造批注。

## 可选审阅范围

- **独立性**：用户要求多位独立审阅时，使用可用的独立子任务；每位只读原稿、必要材料和自己的任务，内部记录合并去重后仍交付同一份原稿标注版。没有独立运行时不声称已完成独立评阅。
- **申报书**：按 [审阅维度](references/review-criteria.md) 的申报书部分检查选题、论证、设计、基础和可行性；匿名及格式按当年实际模板核对，可调用 `../edu-proposal/scripts/check_proposal.py`。意见仍写入原稿批注。
- **纯文本或无法原生标注的文件**：说明现有文件格式的具体限制。用户提供 DOCX/PDF 后可在原件副本标注；不把重排后的普通文字称为原稿原生批注。

诚信要求见 [共同规则](../edu-shared/references/integrity.md)。只有用户明确要求修改才按其取舍改正文；不能为完成意见补造数据、分析、文献或研究过程。
