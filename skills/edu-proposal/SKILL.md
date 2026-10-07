---
name: edu-proposal
description: Draft and check education research grant applications and proposals in Chinese - National Social Science Fund (including the National Education Science Planning projects), Ministry of Education humanities and social sciences projects, provincial social science funds, and thesis or project opening reports - from topic and evidence to the anonymous review sheet, with word counts, anonymity and overclaim checks. Use for 课题申报、申报书、活页、国家社科基金、全国教育科学规划、教育部人文社科、省社科基金、社科规划课题、开题报告、课题论证、选题依据、研究内容、创新之处、预期成果、研究基础.
---

# 教育学课题申报书

用户提供选题想法、前期成果、已有材料和目标基金（以及当年的申报公告或模板）即可。申报书的结构、字数和匿名要求每年会调整，**以用户提供或从官方网站核实的当年公告和模板为准**；下面的栏目只是常见结构。

## 步骤

1. **确认基金类别和当年要求。**问清（或从材料中读出）：基金类别与项目类型（重点、一般、青年等）、学科分类、是否有匿名活页、活页字数上限、成果形式要求。用户没有提供当年模板时，到官方网站下载当年的申报公告、活页模板和答疑（全国教育科学规划见全国教育科学规划领导小组办公室网站 onsgep.moe.edu.cn，一般 5 月下旬至 6 月初发布、6 月下旬截止，附件多为 .doc；国家社科基金见全国哲学社会科学工作办公室网站；省级见本省规划办网站）。当年已经截止时，按下一年度准备，以最近一年的模板起草并标明待新公告核对。[申报书结构](references/structures.md) 里的全国教育科学规划活页已按 2026 年模板原文核对。
2. **先定主线，再动笔。**先在任务文件夹里填 [论证地图](templates/argument-map.md) 和 [证据表](templates/evidence-table.md)：核心问题—已有研究做到哪一步—缺口—研究板块—方法—创新点—预期成果，每个缺口和创新点都要有登记过的文献依据。再用一屏内容给用户确认：课题名称（一般不超过 40 字）、要解决的核心问题、两三条创新点、研究内容的几个板块、主要方法、预期成果。确认后按栏目一次写完，不逐节确认。
3. **按栏目写。**写法见 [写作要点](references/writing-guide.md)；全国教育科学规划活页按 [栏目计划](templates/section-plan-qgjk.md) 分配篇幅。学术史梳理只引用核实过的真实文献（核验流程同 edu-writing 的引用核验）；即使用户只要创新之处，也先简要梳理相关研究，让每条创新点都有对照的已有研究；研究设计和方法可以调用 edu-research 的研究设计和样本量估计；语气按 edu-writing 的 [中文语气规则](../edu-writing/references/voice-zh.md)，把价值和可行性讲清楚，不堆限定。
4. **检查。**运行
   ```
   python <本skill>/scripts/check_proposal.py --draft 活页.docx --preset qgjk --identity "张三,某某大学"
   ```
   `--identity` 填申请人和成员的真实姓名、单位。脚本统计总字数和各栏目字数（`qgjk` 预设按 2026 年全规活页：总字数 7000，选题说明和研究基础各 300），查出活页中可能暴露身份的表述，列出"填补空白""首次""首创"等需要文献依据的说法。论文用的 `check_voice.py` 不适合申报书（研究设计里的计划样本量、"推广"等会被误报）。再按 [交付前自查](references/self-review.md) 逐项检查；用户要评审视角的意见时，用 edu-review 的申报书模式。
5. **交付。**先给活页正文，再给需要用户补充或核实的事项（当年模板差异、前期成果情况、经费预算等）。文件存在 `edu_output/proposal/<新任务文件夹>/`。Word 用 `python <本skill>/../edu-writing/scripts/md_to_docx.py --input 活页.md --output 活页.docx --lang zh --superscript-citations` 生成（`manuscript_package.py` 只用于论文）；参考文献用 GB/T 7714 著录。中文文献在知网等数据库的核实由用户完成或提供条目，`verify_references.py` 只能核对有 DOI 的文献。

## 红线

- **研究基础只写真实成果。**已发表、已录用和已完成的成果照实写明状态；未发表的实验、模拟数据、虚拟实验或预研如实写明性质，不能写成已验证的实证成果，也不能编造发表信息。
- **匿名活页不出现可识别信息，否则取消参评资格。**包括申请人和成员的姓名、单位，以及"本人主持的""我校""我院"等表述。全国教育科学规划活页（2026 年模板）的研究基础只综述前期研究的核心观点（300 字以内），**不得出现成果名称或项目名称、作者、单位、刊物或出版社、发表时间或刊期**；申请人的前期成果不列入参考文献。其他基金按当年模板说明逐条核对。
- **创新和价值要有依据。**"填补空白""国内首次""国际领先"只在学术史梳理确实能支持时使用，否则写具体的推进之处。

诚信要求另见 [共同规则](../edu-shared/references/integrity.md)。
