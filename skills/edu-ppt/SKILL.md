---
name: edu-ppt
description: Prepare education research presentations with source-linked slide text and speaker notes, or editable PPTX with rendered previews. Present the user's completed paper, proposal or progress; explain supplied papers or find public literature around a topic. Use for 论文汇报、组会PPT、研究进展、答辩汇报、文章解读、四步走、逐页内容和讲稿、按模板做可编辑PPT. Use edu-writing for manuscript prose and edu-analysis or edu-qual for new analyses.
---

# 教育研究汇报与文章解读

用户提供自然语言需求与材料即可；助理阅读、组织并生成内部格式，不要求用户填写JSON。不需要额外模型API密钥。遵守[共同规则](../edu-shared/references/integrity.md)。

## 选择路线和交付

| 用户目的 | 路线 |
|---|---|
| 我的论文、研究方案、阶段进展、答辩或会议汇报 | A：[自己的研究](references/own-research.md)，先区分完成、方案、进展 |
| 解读提供的文章；围绕选题找文章做汇报 | B：[文章解读](references/article-reading.md)，以What—Why—How—Result组织 |

只在归属或目的会实质改变内容、且材料无法判断时简短询问。只要逐页文案/四步走内容/讲稿时交付**内容模式**；要求PPT、可编辑文件或指定模板时交付**成品模式**。未指定语言、时长时，按中文15分钟、约12—15页起草并简短说明；用户的时长、页数和语言优先，页数不是配额。

## 从证据到页面

1. **读取材料并定位来源。**本地PDF、Word、Markdown、文本或网页用 `scripts/extract_source.py` 提取，仍须阅读原文图表及需要的补充材料。脚本标记低文本PDF页；扫描件OCR后的数字、符号和表格要对照原图。链接和仅有选题的任务按路线B实际上网检索，不把搜索摘要当全文。
2. **建立主线。**从研究问题和贡献决定哪些证据值得讲。路线A保留作者有依据的立场和概念；路线B区分原发现、原作者解释、汇报者思考，保持他人研究归属。需要补做分析时转给edu-analysis或edu-qual，拿实际运行结果后再讲。论断需修复时采用edu-writing的[修改原则](../edu-writing/references/foundation.md)与[结果解释](../edu-writing/references/framing-results.md)，不全面降调。
3. **写实际逐页内容。**按[页面计划格式](references/plan-format.md)生成任务目录中的 `plan.json`。每页有标题、核心信息、可上屏正文、图表/案例安排、完整讲稿、关键主张的来源位置及时间。内容模式也输出完整正文和讲稿，不能只交目录。
4. **核查内容后再排版。**对照原文核实数字、引语、比较对象、正负号、区间、显著性和分析身份；重要反例及反向结果不删。不显著不转成无效、等效、排他机制或任选方案。核实后的计划作为内容快照；样式重做直接复用，改变论断则重新核查对应证据。
5. **生成。**内容模式运行 `scripts/build_deck.py --plan ... --out ... --content-only`，输出 `content.md` 与 `speaker_notes.md`。成品模式运行同一脚本而不加该开关，增加 `slides.pptx`；讲稿同时写入演讲者备注。模板、视觉布局及命令详见[生成与检查](references/production.md)。
6. **实际渲染和复查。**成品运行 `scripts/render_deck.py`，打开预览检查每页及重点局部，结合 `scripts/check_deck.py` 按对象核对表格、图表、区间、引文、流程、图片及备注。脚本验证成品与已核实计划的一致性，事实仍需回源核对。修复受影响页面后重新渲染检查。环境无法渲染须说明；几何检查不等于视觉验收，AI阅读不称人工审核，计划秒数不等于实际试讲时长。

## 讲述与页面约束

- 一页围绕一个理解任务。讲稿解释、衔接并补充细节，不逐字念屏幕；决定结论含义的条件保留在屏幕上。工作提醒、作者待办和内部推断分类留在记录，不进入观众页面；“汇报者思考”“计划”等必要的身份区分可上屏。
- 摘要式总览保留必要条件，具体结果页解释相关不确定性，局限页处理整体设计边界，结尾回答问题。不在每页复制同一免责声明，也不通过删条件减字。
- 图表优先使用清晰原图，保留图例、坐标、单位、来源。重绘统计图必须有可靠数值，不能按图形外观估计。原图是独立图片对象，内部元素不可编辑；文本、表格、模型、有可靠数值的图表使用原生对象。
- 内容太多先压缩或拆页，不持续缩小字号。默认16:9；有模板时保留模板比例和母版，检查字体、标识与内容区位置。

## 交付及复用

任务资料、计划与成品保存在用户项目的 `edu_output/ppt/<新任务名>/`，不得写入技能目录；用户另指定临时位置时服从。交付内容稿或PPTX、独立逐页讲稿、来源记录和检查结果；成品另有实际渲染预览。报告自动检查、AI自查和用户反馈各自覆盖的范围。

环境与运行命令见[生成与检查](references/production.md)，开源参考、版本及采用理由见[参考项目](references/open-source.md)。公开的[可运行示例](examples/README.md)分别标明合成材料与获许可的开放文章来源。
