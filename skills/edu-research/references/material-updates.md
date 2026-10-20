# 材料更新后的关联核对

适用于“结果表更新了，看看全文哪里还没改”“论文改好了，PPT 有没有旧数据”“这篇参考文献换了，论断还能不能用”。默认交付简洁定位清单，**不改正文、不默认高亮全文**。用户已明确要求同步修改时直接按范围执行，保留原文件。

## 从指定材料建立记录

只读取用户指定稿件、明确关联材料、授权偏好。不要扫描同目录或其他项目；可能相关的文件可提为候选，不能仅凭名称认定关联。状态在用户项目的 `edu_output/project/`；与 `preferences.json` 分开。它是按需核对工具，没有后台监控、云同步或定时任务。

1. 运行 `scripts/project_check.py inventory --files <指定文件...> --out <项目侧清单.json>`，读取 DOCX 正文和表格、Markdown、CSV/XLSX 单元格、JSON 叶字段、PPTX 原生文字/表格/图表/讲稿、可读 PDF 文字块。阅读实际上下文，保留 `unchecked` 的对象；扫描页、图片图表、复杂 Word 对象、公式未重算等不算检查通过。
2. 用本次任务必要的对应关系准备内部 spec，再 `register --project <项目> --spec <内部记录>`。首次建立的是**当前基线**，可以发现文件间不一致，不能声称知道此前变了什么。
3. 更新后运行 `check --project <项目>`。只重复读取登记文件；相同输入不制造新提示历史。文件明确改名或搬移，用 `--relocations <文件ID到新路径的JSON>`；先比内容指纹，内容相同视作同一版本。未给新路径时报告失效，不到别的目录猜文件。
4. 将 `check.md` 中真正需要行动的位置交给作者，简短说明已检查材料和未检查范围。没有问题也不保证全文无误。未映射的读取单元必须继续由助理按当前需求检查或明确限定范围，不能把映射覆盖率当作全文核查。

## 内部记录接口

记录由助理维护，不交用户填写。spec 顶层：

- `files=[{id,path,role}]`：仅授权文件；role 如分析输出、正文、结果表、参考文献、引用 ledger、PPT／计划。
- `facts=[{id,identity,mapping_reason,sources,occurrences,authority}]`。
- `dependencies=[{id,depends_on,target,reason}]`：结果、定义、设计、计分等到解释的必要依赖，可继续连到摘要、结论和 PPT；无需建完整图。
- `citations=[{id,reference_id,reader,claim,support,source_file,ledger_file}]`：复用已有引用 ledger 和阅读文件；claim/support 是下面的位置记录。
- `decks=[{ppt:<文件ID>,plan:<文件ID>}]`：可选；对已确认对应的成品与计划运行现有 `check_deck`，同时核对图表标签、单位、原生数值及区间几何。此检查不代替来源事实检查或实际渲染。

`identity` 必须含 `outcome,comparison,timepoint,sample,statistic,unit,model,adjustments,analysis,uncertainty`。不适用的项说明“不适用”，未知项保留未决，不凭猜测形成已确认关系。同值 r 与 β、总样本与量表有效人数、调整前后、主分析与敏感性分析分别记录。没有语义依据的候选对应只作为待阅读线索，不纳入自动同步。

每个位置有稳定且唯一的 `id,file,locator,reason`；文本中的值可用 `pattern` 提取，必须有命名组 `value`，区间另用 `low,high`。没有 pattern 时读取整个字段。`value_type=text` 用于定义、设计、计分规则等。位置来自实际 inventory，不手猜段号。原生 PPT 采用已有对象 ID；改主题后仍读取真实对象，不从元数据推定值。

```json
{
  "id": "adjusted-beta-source",
  "file": "analysis",
  "locator": "json:/primary/beta",
  "reason": "同一结局、分析样本和调整模型",
  "guards": [
    {"locator": "json:/primary/outcome", "equals": "engagement"},
    {"locator": "json:/primary/model", "equals": "baseline-adjusted"}
  ]
}
```

对表格／结构化输出，应把相邻的结局、统计量、模型、单位等身份字段列入 `guards`；对应标签变化时暂停数值判断。跨格式关联仍需读取者确认，脚本不自动证明这些语义。

原值和显示值分开：`.210` 与 `.21` 本身等价；需要舍入时在出现位置声明 `display_decimals`，不可掩盖符号或与参考值的关系。比值指标可用 `reference_values=[1]`。比例/百分数换算仅在同一统计含义得到确认后使用 `scale=0.01,conversion_reason=...`；不是所有 21% 都等于系数 .21。

authority 使用 `{source:<来源位置ID>,kind:user_confirmed|confirmed_run|project_record,reason:<实际依据>}`。已确认运行还要求登记 `run_status` 和 `provenance` 文件ID，并由实际运行记录与输出关系支持。**不能凭修改时间、final/new 文件名或显著性选来源。**不同分析的有效结果并存；权威不明时不填 authority，报告需判断，继续其他可判断部分。

## 变化、重新阅读和来源支撑

脚本把数值变化沿显式依赖传播。变的是区间、计分规则、模型、排除标准、设计、概念定义时，也应登记为事实并连接到依赖解释。结果变了但解释仍成立，可记录一次实际阅读判断，而非强制重写。

`refresh --project <项目> --request <更新请求>` 接受：

```text
reader, reason,
replace: {facts（可选完整替换）,dependencies（可选）,citations（可选）},
reverified_citations（可选引用关系ID列表）
```

位置被重新阅读时填当前 `reviewed_sha256`，保留稳定 binding id；旧基线不因改定位就被抹掉。文字改变、段落移动、对象删除或重复位置时先重新定位；脚本只对唯一的整段旧文本作自动重定位，其余需重新阅读。

解释仍成立的判断存到依赖项 `decision={status:still_supported,reader,reason,fingerprint}`，fingerprint 使用本轮报告的 `review_fingerprint`；材料再变后该判断失效。不要为消除提示编造判断。

引用支撑绑定论断文本、阅读文件、支撑段落和 ledger。任一改变，旧支撑在核对结果中为 `pending`，不能拿旧“supported”证明扩写成立。重新阅读受影响部分后更新既有 ledger，在对应 citation 记录新 `review_reason` 并显式 reverify。脚本不联网读取文件中的 URL，也不把文献身份核验当作语义支撑。

ledger 使用 [既有引用格式](../../edu-writing/references/reference-verification.md)：`claims=[{block_id,reference_id,status:"supported",locator,support,reader}]`，或核验输出中的 `semantic_review` 同形数组。关联项可用 `block_id` 指定对应论断，省略时取其 `id`。只有唯一对应且实际状态为 supported 的记录才保留原支撑状态；任意自定义 `support:"supported"` 字典不会冒充核验。只比较该论断及文献的相关 ledger 条目，无关参考文献修订不触发本条待核实。

## 授权同步与复核

用户仅要检查时，原稿、结果和 PPT 字节保持不变。用户要求写入原稿批注时复用 [edu-review 原生批注](../../edu-review/references/annotations.md)，不自行生成改写稿。

明确“同步修改这些位置”后：

1. 按本轮报告逐处准备修改，保留新材料归属、单位、比较方向和解释依据。需要作者实质判断的歧义保留待核实。
2. `sync --project <项目> --request <内部修改请求>` 含用户实际 `authorization`、当前 `report_fingerprint`、`edits=[{file,output,replacements:[{locator,before,old,new,reason}]}]`。它只在当前、已检查且不含歧义的位置执行，生成新 Markdown/TXT、普通 DOCX 正文/表格文本或 JSON 文件。先合并同一段落的多个改动；复杂域、修订内部等转到副本手工处理并说明未自动处理的部分。
3. PPT 改计划，通过既有 `build_deck.py` 重建原生图表，再运行 `check_deck.py` 核对类别、系列、数值、标签和单位。检查源事实与计划是否一致另用本流程；不在旧图上覆盖数字。实际渲染后检查各页，生成成功不是视觉验收。
4. 明确登记新路径，重新阅读改动位置并 refresh，再 check。未授权改变的原文件保持。脚本不自动把解释或引用标为通过；阅读者核实后才能作支持判断。

本轮不是自动理解全文的事实数据库。解析器、已明确的语义对应和实际阅读各有边界；公开完整示例及失败记录见仓库的 `evals/author-project-20261020/`。
