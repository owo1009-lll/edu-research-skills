# 独立实际试用记录

2026-10-20。本报告来自独立生成材料后的实际操作，未阅读仓库 tests/evals，未修改仓库，未联网、访问其他用户材料或推送。仅阅读 edu-research/SKILL.md、material-updates.md 及执行所需 Python 实现。所有合成输入、脚本、内部映射、命令输出、修改后文件与真实渲染均保存在本目录。

## 实际请求与新材料

完整自然语言请求见 `requests.json`：

1. “我已重新计算课程完成率，请以我明确指定的新结果 result-current.json 中正式试验主分析为准，检查 Word 摘要、结果表、Markdown 讨论和 PPT 中还用了哪些旧内容；先别改稿。”
2. “同步修改已确定的旧内容，保留原件；歧义不要替我决定。”

独立设计的研究为同伴反馈课程两阶段研究：先导阶段 n=48，问卷有效 n=42；正式随机试验 n=240，问卷有效 n=196，干预和对照各120人。六条重复完成记录被剔除，干预组从84/120=70%改为78/120=65%，对照组维持72/120=60%。新未调整 RR=1.083333，95%CI=[0.890141,1.318456]，区间包含无效应参考值1。`participants-recounted.csv` 有240条独立合成记录；新RR和区间由实际Python计数及对数Wald公式计算。旧区间作为已有错误输出的合成材料提供，没有宣称其经过有效重算。

为了检查语义边界，材料同时保留：

- 不变的协变量调整模型 RR=1.12，[0.93,1.35]。
- 先导问卷满意率70%，不能被正式试验完成率65%替换。
- 分母和组别不明的“某子组完成率70%”，应留待作者判断。
- 加权敏感性分析区间下限1.000400，被讨论稿舍入为1.00，必须提示精度影响参考值关系。
- “排除了无效应，所以推广”的过时解释，以及“点估计仍倾向干预组，但需关注区间宽度”的仍成立解释。
- 虚构的访谈来源 SYN-01，仅支持“帮助学生理解作业要求”，不支持课程完成率因果结论。没有虚构真实书目。
- Word页眉旧70%、Excel公式、损坏DOCX附件，用来核对未检查范围。

原件位于 `materials/` 和 `deck-before/`。真实新版本位于 `updated/` 和 `deck-after/`。PPT前后均为3页，含原生柱状图和原生表格，保留实际讲稿。

## 实际结果及误报漏报

| 阶段 | 实际结果 | 证据 |
|---|---|---|
| 首次检查，开发者修复前 | 15处旧数值全部准确识别：9处完成率，6处RR/区间；19处一致；2处需判断；7处未检查 | `reports/01-first-use-check.json`、`.md` |
| 首次解释依赖 | 已登记的7条解释均未出现提示；其中6条旧解释/计划/讲稿需要处理，1条谨慎解释需阅读后保留 | 同上，`dependency_findings=[]` |
| 开发者根据反馈修复后的独立重跑 | 同一材料、同一spec、全新项目，7条依赖均提示重读 | `reports/09-fixed-first-use.json`、`09-fix-comparison.json` |
| 数值误报 | 本次已明确映射的15处旧值没有误报；调整模型4处均保持一致；四种样本口径未混淆 | 初次报告、`spec.json` |
| 数值漏报 | 本次已映射的15处目标未发现漏报；不据此推断未映射内容全部正确 | 初次报告与实际对象读回 |
| 同步后数值 | 映射范围内旧数值为0；原生图表读回[65.0,60.0]；调整模型与先导满意率仍保留 | `reports/02-readback.json` |
| 原件保留 | 首次检查后11/11文件哈希不变；同步后11/11原始材料仍不变 | `01-check-only-hashes.json`、`02-readback.json` |
| 未决解释 | 谨慎句实际重读后记录 still_supported，不强行改写 | `reports/07-still-supported.json` |

“7个未检查”包括Word页眉1个、PPT装饰线和图形/标签几何4个、Excel公式1个、损坏附件1个。PPT的四个范围项随后另经实际渲染和 `check_deck` 验证；Word页眉、Excel公式和损坏附件没有被伪称通过。

未映射单元也已按内容阅读：CSV中先导满意率70%及问卷有效196、Word表格标签和先导42、PPT类别/系列/轴单位、计划中的样本说明等均保留。`coverage` 统计不是语义核对通过率；结构标签被 guard 使用时，仍可能计入未映射单元。

## 同步方式与真实对象验收

`sync-request.json` 为实际授权请求，工具直接生成新DOCX、Markdown和计划JSON。同一段的完成率与RR变化合并为一次替换。CSV不在内置同步格式内，因此按已核对行写新CSV，记录于 `manual-copy-edits.json`。

解释依赖仅有 review、没有数值stale/consistent时，`sync` 会拒绝自动替换，见 `logs/03-dependency-only-sync.json`。这不是本文声称已修复的功能：实际只在副本中修正新95%CI包含1这个确定事实，把原推广建议标为“需作者重新判断”。没有替作者选择未知子组或选择不同分析结果。

PPT按新计划重新构建；`render-before/`、`render-after/` 均由真实 PowerPoint COM 渲染。实际查看两套3页联系表及新版第2、3页原尺寸图：类别、单位、柱高、65.0/60.0标签、未调整RR/CI和保留的调整模型文字可见，无截断或覆盖。`reports/08-deck-check.json` 的对象一致性和渲染检查均通过。该工具输出仍明确说 `source_fact_check=not_performed`、`visual_review=not_performed`，本报告把独立来源核对和目视阅读另行记录，未把工具通过当成语义正确。

首次调用 `check_deck` 的试用脚本漏传必需 `--out`，得到明确参数错误；随后补齐参数，实际成功结果在 `08-deck-check.json`。这是试用者命令错误，不计产品缺陷。

## 自然异常的实际结果

1. **检查后重新编辑原Word。** 在隔离副本顶部插入一段作者说明。旧同步请求退出2，“Materials changed after inspection”，不产生预期输出。正文数值按唯一完整旧段落重定位；表格值也找到新段号，但其 guard 仍指向旧标签段号，故保守进入 review，必须重读刷新。见 `reports/03-original-reedited.json`、`exceptions/readedit-safety.json`、`logs/12-original-reedited-stale-sync.json`。这没有错误地改到下一段。
2. **模型标签变化。** CSV的“未调整风险比”改为“基线协变量调整”，对应值停止被直接判为旧值，进入 Context guard changed。见 `reports/05-model-label-changed.json`。
3. **无法解析附件与未重算公式。** 其余文件继续检查；损坏DOCX标failed/unchecked，公式标未重算。没有把整个项目静默标为通过。
4. **引用扩写。** 明确结构化ledger基线支持原访谈论断。添加无关条目不会使其失效；扩写“并显著提高了课程完成率”后变为pending。真实来源明说没有测量完成率，因此应拒绝为扩写恢复supported。见 `reports/10-citation-baseline.json`、`11-citation-unrelated.json`、`12-citation-expansion.json`。
5. **结果改变、谨慎解释仍成立。** 另建有真实先前登记的历史项目，切换明确指定的新结果，相关解释均触发阅读；“点估计倾向干预组，需关注区间宽度”经过实际核实后允许保留。见 `history/decision.json` 和 `reports/07-still-supported.json`。

## 已发现并独立确认修复的缺陷：同段歧义未被阻断

最小材料 `mixed-probe/discussion.md`：

> 正式试验干预组课程完成率70.0%；某子组课程完成率70.0%，分母和组别待确认。

对第一项建立明确来源，对第二项不填写authority。`mixed-probe/spec.json` 登记后，`reports/13-mixed-location-before.json` 在同一个 `line:1` 同时给出 stale 和 review，符合语义预期。

实际提交 `mixed-probe/request.json`，授权仍明确说“歧义不要替我决定”，但内部替换错误地把两个70%都写成65%。`sync` 退出0并生成 `mixed-probe/unsafe-attempt.md`，未知子组被实际改变。见 `reports/14-mixed-location-result.json`、`logs/23-mixed-paragraph-sync.json`。

实现检查只选择同位置的 stale/consistent findings，验证已确认事实能通过后，没有阻断同位置review的未知事实。因此文档所承诺“只在当前、已检查且不含歧义的位置执行”在这个实际场景不成立。建议在改动涉及未决绑定的提取值或文字时拒绝，或者保守拒绝同位置所有含review的编辑。保留此错误输出作为试验样本，绝未交作正式同步结果。

本试用没有改实现；将缺陷和复现文件报告给父代理后，父代理修改实现。独立使用完全相同的错误替换请求、仅更换新输出文件名复跑：退出2，提示该位置含未决证据，`after-fix-attempt.md`没有生成；旧失败样本保留。见 `reports/15-mixed-location-fixed.json`、`logs/24-mixed-paragraph-fixed-recheck.json`。

另将正式稿中独立的、已确认的完成率段落提交同步，退出0并成功生成新副本，证明保守拒绝未决混合位置没有阻断其他明确位置。见 `reports/16-known-location-fixed.json`、`logs/25-known-location-still-works.json`。现有策略拒绝同位置所有含review/unchecked的自动编辑；需重读并缩小位置或在副本中审慎处理。

## 文档契约问题及适用边界

- 初始material-updates.md只说复用已有引用ledger，没有给出其最小结构。试用自行构造的 `{"SYN-01": {"claim":..., "support":"supported",...}}` 在旧实现被视作记录一致。开发者改进后必须有 `claims`/`semantic_review` 数组和 `block_id/reference_id/status` 字段；原结构会变成pending。随后采用显式结构化副本才进行上述引用验证。父代理已补充引用ledger最小结构及既有规范链接，本代理实际重读确认；不能把历史自定义结构的“支持未确认”误述为真实论文内容已经变化。
- `sync` 的自动格式为DOCX普通段落/表格、Markdown/TXT、JSON；CSV需要新副本，PPT需要计划重建。解释的语义改写仍是助理阅读任务。工具不应被描述为自动同步全部文件。
- 本次映射由助理根据实际单位和上下文建立，没有自动发现全部语义的证据。原稿页眉旧值仍存在且未解析范围明确列出；损坏附件需可读版本，Excel公式需实际计算后再校核。
- 本次未测试PDF、复杂修订Word、合并Excel单元格、图像内数值识别、受密码保护文件、跨目录自动搜寻或后台同步，不对其下结论。
- 结束前新增可选 `decks=[{ppt,plan}]` 统一入口，本次未再单独试验该新入口；已单独完成同一成品的实际 `check_deck`、渲染与来源核对。不能用此记录宣称新增入口已经独立验收。

## 可复核入口

- 输入与生成：`forward_trial.py`、`materials/`、`requests.json`
- 初次映射与检查：`run_check.py`、`inventory-before.json`、`spec.json`
- 实际授权修改与异常：`run_sync_and_exceptions.py`、`sync-request.json`、`manual-copy-edits.json`
- 修复重跑、引用与同段歧义：`finish_probes.py`
- 原件：`materials/manuscript.docx`、`materials/results.csv`、`materials/discussion.md`、`deck-before/slides.pptx`
- 新稿：`updated/manuscript.docx`、`updated/results.csv`、`updated/discussion.md`、`deck-after/slides.pptx`
- 真实预览：`render-before/contact-01.png`、`render-after/contact-01.png`及各页PNG/PDF
- 机器可读输出：`reports/`、`logs/`

脚本会生成新文件并拒绝复用已存在输出，复跑应使用新的试验根目录。不得删除既有失败证据来追求全绿。
