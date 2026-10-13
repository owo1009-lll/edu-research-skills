# 页面计划格式

这是助理内部生成的UTF-8 JSON，不是要求用户填写的表单。[合成示例](../examples/progress-plan.json)可以直接运行。

## 汇报级字段

`title`、`route`（own/article）、`stage`（自己的研究用completed/proposal/progress）、`language`、`minutes`、`sources`、`slides`。

每个来源包含唯一`id`、`title`、`access`（fulltext/abstract/title/author_material），尽可能补齐authors、year、venue、doi、url、许可信息和本地文件路径。`short`是上屏可读的短引文，如“张等，2025”，不是核验状态。来源提取不等于已经阅读；只有实际阅读后才标fulltext。

## 逐页字段

| 字段 | 内容 |
|---|---|
| id / title | 稳定页码ID与标题 |
| section | 讲述位置，如What、Why、How、Result、Close，或自己的研究阶段 |
| message | 本页核心信息，实际上屏 |
| body | 可直接上屏的字符串列表，可为空以让图表占满内容区 |
| visual_plan | 实际图表、概念、案例安排；无图时也说明文字结构 |
| notes | 完整逐页讲稿，解释、衔接、补必要细节 |
| seconds | 预计讲解时间，结合讲稿和视觉解释核对 |
| role | finding / author_interpretation / presenter_comment / plan / background / method |
| status | completed / preliminary / planned / not_applicable |
| evidence | 非空列表，每项有source（来源ID）、location（页/节/表/图/段）、supports（支持的具体内容） |
| visual | 可选，下表定义 |

role/status供工作记录判断，渲染器不自动将这些标签写进正文。需要听众辨认的计划、初步结果和汇报者思考，必须在title/message/body自然表达。背景和汇报者思考也写其根据，不能用一个引用笼统担保全页。

## 原生视觉对象

| type | 字段与注意事项 |
|---|---|
| table | columns列表、rows二维列表；可选widths相对列宽、font_size（至少18）。单位、区间和分析身份保留在表内或caption |
| chart | kind为column/bar/line；categories、series=[{name,values}]、unit；可选minimum/maximum、major_unit、number_format（数据标签的Excel格式，默认General）、labels。数值轴刻度目前使用General格式，只支持线性轴；数值由已核实表格或数据提供，原生图表附可编辑工作簿 |
| interval | rows=[{label,estimate,low,high}]、range=[最小,最大]、unit；reference默认0，比值指标可设1；scale仅支持linear。原生线段/点/文本显示区间，拒绝区间颠倒或裁切，参考值须在范围内；caption说明区间类型 |
| process | steps字符串列表，语义是依次从前一节点指向下一节点；生成真正连接节点的有向连接线。支持顺序流程，分支模型须另作有来源的图片或明确标注的表达，不声称本格式能表示任意图 |
| quote | text原文或准确标明的翻译、attribution。不要将翻译冒充原文逐字引语 |
| image | path（相对原plan文件位置）、caption。保留比例，独立图片可移动/缩放，内部不可编辑 |

所有visual可带caption。图表来源仍写在evidence；图表内数字和引语必须逐项回源核对。布局可以改，数据不能自行重估。

### 数值显示与坐标

区间原值保留在estimate/low/high中，默认按输入数值显示，不统一补两位小数。可选`number_format=".3f"`或`".2e"`等Python数值格式；也可逐行提供`display={"estimate":"0.90","low":"0.57","high":"1.23"}`以保留原文已有的显示精度。display必须与原值相等，不用于追加解释文字。格式导致符号、相对参考值的关系改变或不同边界合并时拒绝生成。数值与显示标签分别输出并核对；增加小数位须有原文依据，格式不代表新的测量精度。

例如0.009 [0.004, 0.014]默认保持原样；`.2f`会把下限变为0，因而被拒绝。比值区间用`reference=1`与线性坐标；当前不支持对数轴。

普通图表检查有限坐标值、最小值小于最大值和数据是否超出显式范围。确需截断时同时设置`allow_truncation=true`和具体`truncation_note`，说明会实际显示在图旁。柱形/条形的非零基线也需说明；折线图只要覆盖数据便可使用非零范围，不一律要求从零开始。

多系列默认按计划顺序使用稳定的不同颜色，图例与系列一致；折线另有不同标记。theme可用`series_colors`提供每系列的六位RGB颜色，不能重复。默认六色，更多系列需显式提供可区分的配色或拆图。自动检查颜色不同不等于通过色觉或投影可读性验收，必要时配合直接标签。

## 冻结与修改

`build.json`记录输入计划、模板、样式及产物哈希，以及对象ID、区间原值和图片资产哈希。对象ID由页id与字段位置组成，保存在OOXML对象的替代说明中，换主题或布局后仍对应同一字段；手工改可见对象名称不影响对应，删除标识则报告缺失，不退回整页搜句子。生成器不改写文本，不新增分析。修改样式时使用同一plan原文件和新的输出目录；别直接编辑输出副本中的图片相对路径。若要移动计划，连同引用的相对图片一起移动，或先改为正确绝对路径。

成品检查器按对象核对文本与备注、表格结构和单元格、图表类别/系列/数值/单位/显式坐标、区间原值/显示/相对位置/参考值、引文归属、流程连接、图片字节与生成记录。失败项列页码、对象ID、字段、预期和实际。图片核对需原始资产与成品旁的build.json。旧版无对象ID的成品需重新生成。

“与已核实计划一致”由这些检查支持；“原始材料中的事实正确”仍须阅读来源。脚本报告source_fact_check=not_performed，不能证明某句话由原文支持，也不替代视觉或讲述检查。
