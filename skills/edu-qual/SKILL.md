---
name: edu-qual
description: Analyze education interviews, observations and open-ended responses with source-linked records - AI-assisted reflexive thematic analysis, inductive or theory-guided codebook content analysis, grounded-theory three-level coding with saturation checks, and inter-coder agreement. Use for 访谈分析、质性研究、主题分析、内容分析、扎根理论、三级编码、开放式编码、主轴编码、选择性编码、编码一致性、开放题分析、课堂观察记录分析.
---

# 教育学定性分析

用户提供访谈、观察记录或开放题答案和研究问题即可。助理把材料整理成内部表格和编码记录，不要求用户准备格式。原始材料和匿名映射放在用户项目的 `edu_output/private/`，只导出检查过的必要摘录。

## 步骤

1. **选取向。**按研究问题选一种，并在方法部分写明，三者的编码单位、目标和审核方式不同，不要混用：
   - **反思性主题分析**（Braun & Clarke）：解释参与者经验与意义，主题是分析者建构的解释。见 [主题分析流程](references/thematic-workflow.md)。
   - **代码本内容分析**（归纳或理论指导）：按类别系统编码、可以计数和计算一致性。见 [内容分析流程](references/content-workflow.md)。
   - **扎根理论三级编码**：从材料中归纳过程或机理模型。见 [扎根理论](references/grounded-theory.md)。
2. **整理与匿名化。**整理成 `document_id, speaker, text, source_locator` 四列的内部表；说话人区分受访者、观察者、访谈者和归属不明。观察笔记是观察者的记录，不能当作受访者原话。匿名化只做显式替换，替换后仍要检查可识别的细节。
3. **全读材料并写熟悉备忘录，**然后编码。每个代码有定义和纳入、排除条件；每次赋码保留原文精确摘录和位置。
4. **回到原文检验。**为每个主题或范畴找支持证据，主动查找反例和替代解释，写明适用边界。
5. **保存版本。**三种取向各用各的提交脚本：主题分析用 `scripts/theme_analysis.py commit`，内容分析用 `scripts/content_analysis.py`，扎根理论用 `scripts/grounded_coding.py`（输入编码表 CSV，导出开放式编码表、主轴编码表和逐份新增与饱和表）。三者都先用 `theme_analysis.py prepare` 把材料切成带编号的片段；没有需要匿名替换的内容时，替换文件写 `{}`。每次修改生成新版本并引用上一版本。AI 做的修改标 `AI_assistant`，研究者实际提交的修改才标 `researcher`。
6. **报告。**交付编码本、来源表、候选主题或范畴、反例与替代解释、修订记录，以及带引文的结果叙述。需要写成论文段落时交给 edu-writing（[分析衔接](../edu-writing/references/analysis-bridge.md)）。

## 编码一致性

代码本内容分析和扎根理论有两位编码者独立编码时，用 edu-analysis 的 `edu_kappa(编码者1, 编码者2)` 计算 Cohen's κ 并报告分歧处理。反思性主题分析不以一致性系数作为质量标准。只有一位研究者或由 AI 辅助编码时如实写明，不虚构独立编码者、成员核查或理论饱和。

## 示例

`examples/` 里是一组虚构的教师访谈示例（访谈表、匿名映射、标注记录），可以直接跑通主题分析脚本的 prepare 和 commit；`grounded_coding_template.csv` 是扎根理论编码表的列格式。

诚信要求见 [共同规则](../edu-shared/references/integrity.md)。
