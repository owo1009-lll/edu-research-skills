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
| chart | kind为column/bar/line；categories、series=[{name,values}]、unit；可选minimum/maximum、number_format。数值由已核实表格或数据提供，原生图表附可编辑工作簿 |
| interval | rows=[{label,estimate,low,high}]、range=[最小,最大]、unit。用原生线段/点/文本显示区间，拒绝区间颠倒或裁切；在caption说明区间类型 |
| process | steps字符串列表。原生形状与箭头；用文字区分方法流程、理论模型和已识别机制 |
| quote | text原文或准确标明的翻译、attribution。不要将翻译冒充原文逐字引语 |
| image | path（相对原plan文件位置）、caption。保留比例，独立图片可移动/缩放，内部不可编辑 |

所有visual可带caption。图表来源仍写在evidence；图表内数字和引语必须逐项回源核对。布局可以改，数据不能自行重估。

## 冻结与修改

`build.json`记录输入计划、模板、样式及产物哈希。生成器不改写文本，不新增分析。修改样式时使用同一plan原文件和新的输出目录；别直接编辑输出副本中的图片相对路径。若要移动计划，连同引用的相对图片一起移动，或先改为正确绝对路径。

验证器只能核对结构、来源ID和部分明显冲突，不能证明某句话真的由原文支持。来源完整性、概念、数字含义、前后推断一致性和讲述质量须逐页阅读。
