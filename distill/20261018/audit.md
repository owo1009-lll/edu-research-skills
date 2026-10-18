# 写作体系审计（进行中）

基线：`a4020c41a4f3d8ab180a4e2818955d90e40f6f3b`。日期：2026-10-18。公开库重新克隆；此前本地开发目录与全文缓存目前不可用。不得把旧汇总等同于本轮已经重读全文。未读取用户私有稿件。

## 已核对的依据

已读当前 `edu-writing/SKILL.md`、共享 integrity、foundation、argument、voice-en/zh、prose-en/zh、introduction、synthesis、methods-section、analysis-bridge、quantitative-discussion、qualitative-narrative、conceptual-argument、conclusion-implications、abstract-title、full-manuscript、framing-results；旧 distill README、来源清单与统计汇总；0.10.0 复测概要；20261013 蒸馏的候选、取舍报告、来源记录和匿名评审。当前读取清单及哈希另存 `audit-inventory.json`。下表区分规则缺陷、已观察输出和待检验风险。

| 问题 | 当前证据 | 状态与下一步 |
|---|---|---|
| 统一弱化作者判断 | foundation §1 明确保护 should 与有依据框架；0.10.0 复测的英文修改稿保留了教师个别反馈立场，但漏改工具能力的无依据概括 | 保护原则已有局部收益；不能声称作者声音完全解决。用带鲜明立场及局部错误的修改任务分别评估保留和纠错 |
| 把不显著写成没有作用 | framing-results §4–5 与 argument §10 已覆盖；0.10.0 复测前三案两臂均达标 | 保留规则；本轮重复检测执行，不重建另一套统计解释流程 |
| 规范判断的边界冲突 | voice-en “Factors … did not manipulate or measure … not … basis for recommendations”；voice-zh 对应禁令，与同页保留有依据专业/规范判断及 foundation §2 冲突 | 是可定位的规则冲突；需要区分未测机制不能冒充发现与规范前提可参与论证 |
| 过程标签泄漏 | voice-en/zh 要求贡献“say what kind it is/说清属于哪一类”；argument §10、结论指南又要求分类仅用于内部判断。prose-zh 的待补占位例外与 foundation 的工作记录分离有冲突 | 规则存在执行歧义；旧 0.10.0 测试曾出现“这是一条应用推论”，不能当作当前版本必然复现 |
| 数量与形式配额 | prose-en 每要点至多一个效应量、长句比例、启示不编号；prose-zh 点名引用次数、冒号/“的”/套话配额；voice-zh 局限 2–4 条；qualitative-narrative 结论必须写 | 与统计仅供参照矛盾。检测它们是否导致删信息、改作者结构或剪碎推理；不以消除某个词为目标 |
| 解释需要与材料支持不匹配 | quantitative-discussion 和 voice 的不显著段落要求给原因；argument §5 允许材料不足时简洁未决。voice 对跨研究差异要求指出样本/测量原因 | 容易将可比较的差异直接包装为原因。检查实际是否编造解释；保留有材料支持的解释 |
| 结果模板与设计边界冲突 | analysis-bridge 中文通用模板使用“显著正向影响”，同页要求相关不写因果 | 模板本身与规则矛盾，需修复为与设计相符的正面示例 |
| 概念、理论、比较缺少执行收益 | 当前已有问题区分、解释轴、案例差异、规范前提方法卡；卡内多数明确仍待独立验证 | 不因“方法卡存在”认定能力已获得；本轮从实际稿件检查概念是否做推理工作 |
| 旧候选无稳定收益 | 20261013 W1 在两项英文任务未稳定改善，H2 行动建议遗漏作业本已有要求；W1 未入正式技能 | 不直接重新纳入 W1，不把旧 H1/H2 再称留出。相关材料只用作开发或既有失败证据 |
| 任务边界与上下文负担 | 入口有新写/修改，却缺压缩/翻译独立选择；入口重复 argument 多段。各章节互相链接且有“先读”及条件性卡片 | 静态链接数量不等于实际加载；在独立运行中记录真正读取的文件、顺序与用途，比较是否误读其他语言规则 |

## 已有输出的具体证据

- 20261013 H2：基线写 “The assignment already requested reasons”，候选建议 “educators should require students to justify…” 却未交代既有步骤。此处问题是实践推论没有接上实际程序，不是 should 太强。出处：`evals/capability-20261013/distillation/README.md` 与 `trials/blind-review.md` H2。
- 同轮 H1：候选先将处理 × 逻辑错误率交互泛写成错误率与考试表现的“关系”，下一句才收窄；基线更准确。不能用概念贡献或流畅度掩盖估计对象漂移。
- 0.10.0 最终复测概要：一份真实稿修复版把缺少事前界值记录写成确定未事先设定。原始私有稿未在本轮读取，故本轮只将它作为历史记录中的失败类别，不作新的原文审定。

## 采用原则

先完成语料定位与候选说明，再冻结候选和运行条件。新写、修改、压缩、翻译分别检验；正常作者结构不是缺陷。分类、工作记录和脚本线索不应成为正文内容。共享统计分析、PPT 和目标期刊检索实现保持兼容。对照结果决定采用、限用或撤回；未证实收益的旧卡不因本轮标题重新获得“已验证”身份。
