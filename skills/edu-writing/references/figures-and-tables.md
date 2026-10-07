# 图表

## 原则

- 图表因为能推进某个论断才做。动手前写清：目的、证据、比较对象、单位和局限。
- 统计图可以用已发表的汇总值或已成功运行的输出，不重新计算分析。
- 没有个体数据时，不编造散点、分布、个体轨迹、SD/SE/CI 或额外的模型。缺少的对比或区间就留空。四舍五入后的描述性均值不能复现调整后的推断结果。
- 表格用 Word 原生表格并附可编辑的 CSV，包括结果表和文献对比表。

## 作图脚本

`scripts/make_figures.py`（路径相对于本 skill 所在文件夹）只用 Python/matplotlib，不生成 AI 图片。输出 Word 用的 PNG、文字可编辑的 SVG、PDF、source_data.csv 和 spec.json。

```
python <本skill>/scripts/make_figures.py --spec spec.json --output <新文件夹>
```

中文图在 spec 中加 `"language": "zh"`，脚本自动使用已安装的中文字体。脚本不支持的图型，可以用其他实际可用、可复现的工具，但不要说成是这个脚本做的。

## spec 格式

统计图都需要来源字段：`source_kind`（published_summary / existing_analysis / real_data）、`source`、`locator`、`conclusion`、`units`，可选 `limits`。

| kind | 用途 | 关键字段 |
|---|---|---|
| `group_means` | 组均值 | `panels=[{title, rows:[{group, condition, mean, n（可选）}]}]`；不自动加误差线，缺失的组合留空不填 0；离散程度或区间定义和 n 写进图注 |
| `estimate_intervals` | 已算好的估计值与区间 | `rows=[{label, estimate, low, high}]`、`interval_definition`，可选 `reference_line`；区间是输入，脚本不计算 |
| `trajectory` | 模型的总体均值轨迹 | `x_units`、`trajectory_kind=model_population_mean`、`interval_definition`、`rows=[{time, mean, low, high}]`；时间严格递增、为实际经过的时间单位 |
| `prediction_curve` | 固定效应的总体均值预测曲线 | `prediction_kind=fixed_effect_population_mean`、`x_units`、`interval_definition`、`rows=[{x, group, mean, low, high}]`；记录固定的协变量和随机效应的处理 |
| `flow` / `framework` / `themes` | 流程图、框架图、主题关系图 | `evidence_status`、`nodes=[{id, label, x, y（可选，0–1）}]`、`edges=[{from, to, relation, label（可选）}]` |

**轨迹和预测曲线**：区分模型均值及其逐点置信带、观测各波次均值、个体轨迹和预测区间；置信带不自动等于个体预测区间或同时置信带。明显的拟合不良写进图注和解释。

**关系图**：
- `evidence_status` 取 procedure（流程）、conceptual（概念关系）、hypothesized（待检验假设）、reported_association（已报告的关联）、candidate_themes（候选主题）；`themes` 图必须是 candidate_themes。
- 每条边的 `relation`：`influence` 影响、`association` 关联（实线），`sequence` 过程顺序（灰色空心箭头），`hypothesized` 待检验、`candidate` 候选（虚线）。
- 这些关系都需要实际的文本或分析依据，不能暗示做过因果检验。复杂布局给出 x、y 坐标。
- 图左下角默认标注"关系性质"；`"show_status": false` 可以关闭（例如已在图注中说明）。

## 编号、图注与检查

- 打包脚本按出现顺序给图表编号。正文用 `{{table:id}}`、`{{figure:id}}`，转成"表1/图1"（英文 Table 1/Figure 1），并检查与实际图表是否对应。
- 每个图表要有标题和注释：来源引用、结果变量、单位、比较对象、样本和不确定性定义。可选的 `abbreviations` 会自动展开。图注中的来源论断同样进入引用核验记录。
- 在 Word 的实际尺寸下检查图，核对源数据、坐标轴标签和图题编号。SVG 中的文字可编辑；最权威的可编辑源是绘图代码加精确的源数据，即使有人用图形软件改过 SVG。
- 不放论证不需要的照片或期刊标志。
