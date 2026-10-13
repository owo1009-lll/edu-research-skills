# H2-writing：论证与依据记录

## 任务、阅读与主线（动笔前）

新写英文二次写作练习；约150词引言末段、400–500词讨论。以 Ding 等（2023）为原研究，直接阅读 Chan 与 Hu（2023）全文作为最接近比较来源，不把文献数量不足写成全领域空白。不联网。已读两篇全部正文与题录；H2参考文献仅作其回顾范围，不外推为独立阅读。

主线：一般问卷已经显示学生承认GenAI风险且愿意使用，教育上还需知道学生在真实学科任务中是否拒绝错误答案。Ding等把答复正确性、接受行为、使用感知和绘画表征放到一次物理补做任务中。增量不是又证明“态度复杂”，而是呈现知道/被告知AI可能出错、手头有答案，却仍接受错误答复的任务情境，并提出对信任来源的具体追问。绘画为这种追问提供表征线索，不能独自诊断参与者内在信念。

## 写作依据与跨节位置

|单元|功能|论点|证据与位置|理由与关键限定|
|---|---|---|---|---|
|引言末段|提出增量问题|总体态度与对具体答复的判断有区别|T2 pp.6–9,11–15；H2 pp.5–8|两篇设计/样本不同，不能当同一群体先后变化|
|讨论1|回答问题、直接比较|多数答复正确仍伴有错答接受|H2 p.7，307/362正确、55错答中30被接受；p.5答案与警告|分母是答复/问题提交记录，非独立学生；不称85%所有物理题准确率|
|讨论2|解释定量|信任按接受比例定义，与易用感知有关；不能确定因果方向|H2 pp.7–9 Tables2–3；p.10–11原讨论|19人全部接受；易用性Trust与Partial Trust的p=.026；使用意愿p=.059未达到常规.05，修复原文正向定论|
|讨论3|绘画解释|机器形象可能承载高能力期待；人形与信任非简单正关系|H2 pp.9–10 Table4, Fig4；pp.11–14|27幅可读；Trust绘画15幅中的14幅机器/机器人；稀疏分组、无访谈；向导帽也可能装饰|
|讨论4|教育判断与范围|应教授有依据的核验而非仅泛泛警告|H2 Implications pp.12–13；T2 Implications pp.14–15|具体教学建议有观察依据，干预效果未验证；不把减拟人化设计当已证明方案|

## 支持与约束

- 支持核心判断：真实课程任务；学生有答案且被告知AI可能出错；收集正确性与同意行为；量表和绘画提供不同证据；没有将意见调查冒充学习成绩。
- 约束：单班40人、36名女性、仅3人有少量先前使用经验；每人可提交不同错题，输入题目难度可不同；信任群体是观察后聚类不是随机组；Distrust仅3人；绘画未全员提交；图像编码一致不证明内在意图；无AI素养或学习效果干预检验。
- 与T2对照：香港六校399名本科及研究生，便利抽样，26项量表和3道开放题；对不准确输出的认识平均4.10/5（Table2），总体使用意愿积极。它提供一般认识和自述期待，没有同样的学科作答准确性与接受记录。
- 原文数字不一致：H2结果p.7额外问题209，启示p.12写206；本稿不用该数字，不擅自选择。Table3 Intention均值Trust4.07、Partial3.22、Distrust4.33，不能称Trust高于其他所有组。

## 术语

|固定写法|含义|
|---|---|
|generative artificial intelligence (GenAI)|引言首次定义|
|trust / agreement-based trust|原研究以同意答复比例操作化，非独立心理信任量表|
|Trust / Partial Trust / Distrust group|事后聚类分组，不是实验条件|
|answer accuracy|提交任务中答复正确率，非跨领域模型能力|
|perceived ease of use / intention to use|感知易用性/使用意愿，非实际未来使用|
|drawings / representations|绘画表征，非自动等同于认知错误|

## 修订记录

待首稿自动线索检查与AI自查后补入。

### 一轮完整修订（已完成）

- 原文：ChatGPT answered 307 of 362 submitted questions correctly, yet students accepted 30 of the 55 incorrect answers
  终稿：Across submissions covering 46 distinct questions, ChatGPT answered 307 of 362 submissions correctly, yet students accepted 30 of the 55 incorrect answers
- 原文：The reported test for intention to use yielded p = .059, leaving the original claim about greater future-use intention less secure than the ease-of-use finding.
  终稿：The reported test for intention to use yielded p = .059 and does not establish greater future-use intention; the Distrust group contained only three students.
- 原文：The authors interpret some depictions as attributing exceptional knowledge or magical capabilities to ChatGPT.
  终稿：One drawing explicitly labels a machine as knowing everything; the authors interpret other imagery, such as a wizard's hat, as attributing magical capabilities to ChatGPT.
- 原文：In comparable physics tasks, instructors should require students to explain why they accept or reject an answer, making verification part of the work rather than relying on a general warning.
  终稿：The assignment already requested reasons for accepting or rejecting answers. In comparable tasks, instructors should review these justifications, resolve disagreements through physics reasoning, and demonstrate checking against reliable sources.

逐项理由见review.md。首稿与脚本日志均保留；终稿重新检查范围同首稿。

### 实际交付与最终检查

- 最终引言153词；Discussion 465词。
- 三个最终检查均成功执行（退出0）；所有线索已按review.md逐项判断，未把退出码或零线索当质量证明。
- final.docx由冻结md_to_docx.py实际生成；未进行Word视觉渲染。
- 初次读取H2分段时，Python默认GBK终端输出遇到NBSP发生UnicodeEncodeError；改用python -X utf8后同一读取成功。没有据此改动原材料。
