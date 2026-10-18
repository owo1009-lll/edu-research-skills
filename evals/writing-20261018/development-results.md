# 开发对照结果：局部收益，尚无稳定整体优势

2026-10-18。比较基线 `a4020c4` 与固定开发快照 q01；两项合成任务，每版本各两次独立生成。四位独立上下文的 AI 评阅者分别只读一组匿名 A/B、任务和材料，先保存评阅，再解盲。没有真人评价，精确后端模型与采样参数不可获取。

**结论：两组略倾向候选、两组无稳定优势；每项任务均是一次局部占优、一次相当，不能据此声称稳定提升。** 四组评阅都未发现确定的严重事实、推理或作者原意错误，这只覆盖所给材料和已读文本，不证明普遍可靠。下面依据原评阅与稿件说明差异，不按总分或规则数量验收。

## 对照与证据

| 任务 | 解盲后结论 | 具体依据与剩余问题 |
|---|---|---|
| D1 新写第 1 次 | 候选有限优势 | 两版均保留延迟主结局与即时次结局、区间、未检验时间差及成本信息身份。候选把已包含的例题核对与教师讲解接到解释质量这一后续观察对象；基线设计介绍更集中、当前研究未做中介分析更明确。候选把分析单位放在局限标题下，仍需局部调整。[原评阅](judges/D1-pair01/review.md) |
| D1 新写第 2 次 | 无稳定优势 | 基线更直接说明为何相同完成指标可包含不同质量的尝试；候选的后续研究问题更具体。但候选反驳“再增加例题核对”这一文中未提出的建议，存在编辑提醒进入正文的问题；基线结论以 estimate 简称区间，需小幅修正。[原评阅](judges/D1-pair02/review.md) |
| D2 压缩修改第 1 次 | 无稳定优势 | 两版均保留作者的 answerability、should 与标题，修复打开等于阅读、修订等于效果、自动/教师绝对化对立。候选区分修订效应与未测成绩更明确；基线更清楚解释教师自己的建议也须可质询。候选对四人时段冲突的概括还可收紧。[原评阅](judges/D2-pair01/review.md) |
| D2 压缩修改第 2 次 | 候选有限优势 | 候选在引言更早连接学生说明责任与取得理由的规范性要求，也更直接说明未证实任一渠道改善学习。基线对同一修订可能包含理解、无批判接受或有理由保留原稿的解释更充分。两版都没有严重错误。[原评阅](judges/D2-pair02/review.md) |

上述“有限优势”是每位评阅者对本组文本的判断，不是独立统计重复、总体胜率或实际读者效果。尤其 D2 第二组的部分优势来自更显式的效果限制，不能据此认为增加否定句就是提高解释力。开发者知道版本身份的补充阅读记录另存 [developer-reading.md](developer-reading.md)，不覆盖匿名原评阅。

## 代表性前后对照

### 将下一步研究连到实际过程：有局部收益，也有过度执行

D1 第一次基线的下一步主要是处理缺失、扩大延迟观察并保留尝试与有效重构的区别。候选写：

> Because retrieval already included example checking and the subsequent teacher explanation, development work should examine the quality of pupils' explanations within that supported sequence.

这把下一步落到了资料实际缺少的观察上，没有声称质量已经解释了效果。相应 [基线终稿](development-artifacts/runs/D1-run01-arm-p/final.md) 与 [候选终稿](development-artifacts/runs/D1-run01-arm-q/final.md) 都保留主要结果的不确定性。

但第二次候选写：

> simply adding example checking would repeat a step already built into its design.

事实虽正确，文中并没有人提出要加这一环节。内部核对已有实施的动作不应自动变成面向读者的反驳。此处是候选剩余风险；未修改原始稿件以消除它。[第二次候选](development-artifacts/runs/D1-run02-arm-q/final.md)

### 保留作者立场：两版都做到，不能归功于候选

D2 两次两版都保留：

> Institutions should protect a route for questioning feedback in assessed work.

候选第二次较早写出：

> Students' obligation to justify academic decisions gives them a corresponding claim to reasons for consequential judgements.

基线第二次的引言只先说区分与学生责任相连接，互惠理由到结论才充分展开。候选的局部收益是推理位置与清晰度，不是恢复了基线丢失的 should；基线并未丢失这一立场。[基线](development-artifacts/runs/D2-run02-arm-p/final.md) / [候选](development-artifacts/runs/D2-run02-arm-q/final.md)

### 基线的优点应保留

D1 第二次基线写：

> Attempts of different quality could meet the same completion criterion.

它用一句具体推理说明为何 81% 不等于有效重构。候选具有相同概念区分，但并非处处更清楚。D2 第一次基线也更显式地从教师评论被学生纠正的案例，推进到教师自己的判断须可质询。后续评估应允许基线在某些论证动作上更好，而不是将旧稿只作为错误示例。

## 方法取舍与下一阶段

- **M1/M2/M3/M6/M7**：两项任务触及问题、比较、推进、规范判断和压缩，但改动作为一组实施，无法因果归属到单条规则。当前仅有局部收益与局部退步，尚不满足稳定整体收益的采纳标准。
- **M4**：D2 包含计数与访谈的衔接，但它是为修改任务构造的记录，不能代替正式混合研究的迁移检验。新路线仍需在真实混合设计材料中检验样本对应、整合判断与不一致处理。
- **M5、中文任务、理论/综述任务与翻译**：尚未由本批开发任务充分覆盖，不能声称已通过。
- 本轮不继续因每处轻微编辑意见追加规则；先保留 q01 的实际字节作为最终留出前的候选输入。冻结是实验安排，不是批准发布或证明有效。
- 最终候选冻结后才选择并读取新材料，采用统一包装、中性技能目录及相同任务文件，关键新写与修改任务重复生成。未达稳定收益的方法继续保留候选或限定范围；若读过留出后改规则，相应材料转为开发材料。

## 可复核材料与限制

完整样稿、过程记录及两份技能 ZIP 见 [development-artifacts](development-artifacts/README.md)；输入、匿名稿、原评阅及 [解盲键](blinding-key.json) 均保存在本目录。[留出前冻结记录](candidate-freeze.json) 固定下一阶段输入。快照清单记录实际字节，结果不能仅由检查器通过或句式统计推出。

机械检查：技能格式有效；结构测试 10 项、PPT 测试 25 项、期刊检索测试 8 项通过。实际快照差异共 22 个 edu-writing 文件，其他技能字节相同。本轮没有重新视觉验收 PPT，也没有把夹具检索测试当在线检索。

早期基线的完整派发包装没有单独导出，其文件路径带 baseline；详见 [执行记录](development-record.md)。这些局限进一步限制本次结果的外推。新真实留出尚未完成，当前不能作为本轮总任务的最终成果。
