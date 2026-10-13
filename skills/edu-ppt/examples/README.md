# 可运行示例

进展材料和数据为合成，仅演示页面计划和原生对象，不是真实研究或实证证据。源说明见[source.md](source.md)，计划见[progress-plan.json](progress-plan.json)。

另有真实开放文章的[NBO四步走中文解读](article-nbo/README.md)，包含公开检索选文记录、来源说明、已核对计划与获许可原图；不包含用户稿件。

[图表边界计划](chart-fidelity-plan.json)使用合成值展示双系列、微小区间、参考值1、非零起点折线和显式截断说明。三套示例的实际PPTX、PNG/PDF及前后检查记录见[定向修订验证](https://github.com/owo1009-lll/edu-research-skills/blob/main/evals/ppt-revision/README.md)。

运行：`python <本skill>/scripts/build_deck.py --plan <本skill>/examples/progress-plan.json --out <任务>/demo`。加`--content-only`仅导出完整文案和讲稿。实际渲染仍需PowerPoint或LibreOffice；不要把生成文件保存进本技能目录。

自然语言调用：

- “把我的论文做成15分钟组会汇报。” → 路线A、完成论文、成品。
- “根据我的研究进展做PPT，哪些已完成哪些待做要分开。” → 路线A、进展、成品。
- “解读这篇英文论文，生成中文汇报PPT。” → 路线B、四步走、成品。
- “围绕婴幼儿情绪社会性发展找文献，做组会汇报。” → 路线B、先实际检索并说明选文，再生成。
- “按四步走生成这篇文章的PPT内容，只要逐页内容和讲稿。” → 路线B、内容模式。
- “按这个模板生成可编辑PPT。” → 从材料判断路线，检查模板后生成和渲染。
