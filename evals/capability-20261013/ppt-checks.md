# 逐点标签与区间错行

## 实际复现

使用上一轮公开基线08aa933、公开合成进展计划生成PPTX，在文件中作真实修改后检查。原始结果见[修改前](ppt-before.json)与[修改后](ppt-after.json)。

| 操作 | 修改前 | 修改后 |
|---|---|---|
| 原始正常成品 | passed | passed |
| 数值12不变，把该点自定义文字改成999 | passed | failed，报告逐点custom label text的预期12与实际999 |
| 只交换两行的区间线和估计点，名称/数值文字不动 | passed | failed，报告具体行对象的纵向错位 |
| 把名称、线、点、数值文字整行一起交换 | passed | passed |

从仓库根目录运行`python -X utf8 evals/capability-20261013/reproduce_ppt.py --out edu_output/new-ppt-check`。重跑基线时另检出08aa933，把`--scripts`指向该检出的`skills/edu-ppt/scripts`；输入使用同一公开合成计划。

## 修改与边界

- `chart_labels.py`核对整体、系列与逐点标签的实际设置。系列dLbls完全替代整体组设置，随后单点dLbl覆盖具体属性，不能错误地从整体继承被系列重置的格式。自定义正文根据计划中的类别/系列/数值及格式核对。
- `build_deck.py`与`plan.py`接受明确的标签内容、分隔符和逐点覆盖；百分比格式的乘100与字面百分号区分。未知引用、动态字段、外部数据标签范围和未实现的复杂格式自定义正文列为`unverified.*`并阻止通过，不把“未验证”写成“已证实篡改”。复杂格式的原生自动标签可按其显式格式核对。
- `fidelity.py`用行文本中心、高度和邻行间距核对名称、线、点与数值文字，保留原有横向比例、参考值及原始数值检查。容差相对于当前布局，不冻结绝对页坐标。
- [计划格式](../../skills/edu-ppt/references/plan-format.md)说明新字段。现有表格、类别、系列、单位、精度、截断、配色/图例、引文、图片和流程检查未移除。

格式语义参考[python-pptx的数据标签说明](https://python-pptx.readthedocs.io/en/latest/dev/analysis/cht-data-labels.html)与[Microsoft的DataLabel定义](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.charts.datalabel?view=openxml-3.0.1)，并以本次实际生成与PowerPoint渲染核对。检查不对任意Excel格式作文字猜测；外部工作簿链接及动态字段尚未实现来源解析。

## 正例、反例与渲染

[测试输出](ppt-tests.txt)包含默认值、固定小数、千位分隔、原比例转百分比、原百分数加字面百分号、纯类别标签、多内容标签、逐点格式及显隐覆盖。反例包含999文字、系列/单点格式改变、隐藏标签、类别意图改变、工作簿格式链接、引用/动态字段/扩展和非法索引；单独移名称或数值也会失败，整行移动及全图平移通过。

四页公开[计划](../../skills/edu-ppt/examples/label-row-plan.json)、[PPTX](artifacts/ppt-labels/slides.pptx)、[PDF](artifacts/ppt-labels/preview/slides.pdf)、[预览](artifacts/ppt-labels/preview/contact-01.png)、[检查结果](artifacts/ppt-labels/checks.json)均可下载。

PowerPoint COM实际渲染后逐页打开1600像素PNG（AI视觉自查）：第1页12/8与柱高一致；第2页0.12/0.08显示12.0%/8.0%，坐标明确为原始比例；第3页类别标签及“对照组: 8.00”对应各点；第4页两行名称、线点、数值、零线一致，无遮挡或截断。渲染过程中发现并修复了OOXML的delete与格式组不能并存的问题，没有把python-pptx可读当作PowerPoint可用。

这只是成品与已核实计划的一致性及本环境视觉检查，不证明原始研究事实、跨Office版本表现或实际讲述效果。归档文本统一LF并更新相应输出哈希，PPTX/PDF/PNG保持渲染时字节。
