# 写作与汇报：预先划分材料的迁移试用

基线为`08aa933`。本轮结论是**局部收益与退步并存**，不是新版全面胜出。新写作卡暂不进入正式技能；只修复引言指南与既有原则的配额冲突。汇报组织卡缩到路线B文章解读，可选使用，不推广为阶段汇报的固定流程。

## 材料、冻结与完整输出

- [已有成果审查](audit.md)、[预先分组](split.json)、[训练来源、阅读范围和许可](training-notes.md)。训练材料包含学习感受与实测差别、学生体验的混合材料、主要结局未显著的实施评价，以及一份真实公开研究讲座。讲座只完成文字阅读，未获得可检查的页面图或录音，未据此评价视觉设计或演讲时长。
- [候选写作卡](candidate-writing.md)、[候选汇报卡](candidate-ppt.md)、[完整候选补丁](candidate.patch)、[冻结版本与逐文件哈希](freeze.json)。候选先冻结，再读取留出全文；两臂共用相同的当前PPT生成／核对代码，只比较指令。交付后复核两套快照，源文件哈希均未改变。
- [相同请求](holdout-requests.md)、[留出来源与哈希](holdout-sources.json)。H1是Bastani等高中数学实验及作者单位更正；H2是Ding等物理课体验研究，并提供两臂相同的Chan与Hu全文作直接比较；H3是明确合成的可行性进展。没有使用用户私有稿件。
- 两个新上下文分别完成四例，每例一次生成与一次自查修订。每臂的四例共用上下文；材料部分重叠，不能当作四个完全独立样本。完整[基线输出](trials/arm-p/)与[候选输出](trials/arm-q/)均含首稿、终稿、理由、检查及Word/PPTX；PPT另有逐页讲稿和渲染预览。
- [匿名输入](trials/blind/)、[盲评原文](trials/blind-review.md)、[解盲键](trials/blind-key.json)、[盲评输入哈希](trials/blind-input-hashes.json)。新评阅上下文只见匿名稿、请求与必要原始来源；未见规则、版本键、前次判断。写作者与评阅者属同一模型系列，这是AI对照评阅，不是人类专家或跨模型验证。
- [发布映射](trials/package-manifest.json)保留原文件及公开副本哈希。公开打包仅移除开发机路径前缀、统一换行和行尾空白、更新生成清单路径和哈希，未修订盲评正文；`delivery.json`与盲评输入哈希仍记录原运行文件，公开副本以发布映射核对。完整原文与原图不随仓库发布。测试稿是有已知待修正处的评估产物，不应不经来源复核直接作为投稿稿或最终示范。

## 具体比较及规则取舍

| 情境 | 基线与候选的具体差异 | 判断与取舍 |
|---|---|---|
| H1英文引言末段＋讨论 | 候选保留教师准备成本；基线对“逻辑错误率×处理”的交互说得更准确，候选先泛写为错误率与考试表现的“关系”，后句才明确交互 | 候选没有稳定改善推理或可读性；不纳入W1新卡。两稿均保留实践判断、Tutor无明确增益及短期范围 |
| H2英文引言末段＋讨论 | 候选提供14/15绘画及34/41答案变化的细节；基线明确原任务已要求解释同意／拒绝理由，再推进到教师检查理由。候选建议“要求学生解释”，没有清楚交代原任务已有这一步 | 基线在行动依据与建议推进上更好。两稿对绘画类别仍有概念伸展，不能把Human／Robot编码当作完整拟人化量表 |
| H1文章解读 | 基线把练习和考试分两页；候选在第5页同表并列，并用第7页解释自评与表现。候选清楚保留三组共有教材、笔记及教师劳动 | P1的对象／时点对应在本例有可见收益，作为文章解读的可选方法保留。候选收尾遗漏Tutor结果、核心页讲稿偏密，不能宣称整体更可讲或已通过试讲 |
| H3合成阶段进展 | 两版都保留12／9／5、两名学生困难和继续范例讨论的决定；候选把未独立双编码放在图旁，基线末页行动更集中 | 各有取舍，候选的交叉情况说明及未完成事项重复可压缩。P1不推广到路线A，不更改其现有阶段组织规则 |

完整成对终稿：[H1写作基线](trials/arm-p/H1-writing/final.md)／[候选](trials/arm-q/H1-writing/final.md)；[H2写作基线](trials/arm-p/H2-writing/final.md)／[候选](trials/arm-q/H2-writing/final.md)；[H1汇报基线](trials/arm-p/H1-ppt/deck/content.md)／[候选](trials/arm-q/H1-ppt/deck/content.md)；[H3汇报基线](trials/arm-p/H3-ppt/deck/content.md)／[候选](trials/arm-q/H3-ppt/deck/content.md)。每个`content.md`包含页面、表格、讲稿和来源，独立讲稿另在同目录。

典型对照不是“少用几个否定词”：

- H2基线先交代“The assignment already requested reasons”，再建议教师审查理由；候选只说“educators should require students to justify…”。前者更清楚地区分已经做过的事与下一步行动。
- H1汇报候选用同一组名、同一张表并列有辅助／无辅助成绩，再说明自评为何不能替代独立表现；这是证据关系的改善。
- H3两版均保留“继续范例讨论、改进提示语、再检验效果”，没有因当前无对照就删除有根据的团队决定。

正式保留的**配额修复**来自[审查](audit.md)中已查明的内部冲突：旧引言规定段数、固定连接词及一半以上句子带引注，入口又明确这些统计仅供参照。将其改为按论证需要选择，是一致性修复；两篇引言末段试用不能证明完整引言质量提升，W1又是组合条件，不能分离估计取消配额的独立效果。新写作卡继续留在本目录作为未采用候选，不从技能入口调用。

正式保留的**P1**只通过文章解读路线调用，删除了候选卡中的路线A段落。这是根据结果缩小适用范围，未重新调参、重写留出稿后宣称第二次独立验证。质性／理论汇报的替代组织方式仍是可选建议，本轮未验证其迁移效果。未增加新的禁用词或统一弱化建议。

## 渲染、成品核对与实际范围

四套PPTX均用Windows PowerPoint COM真实渲染：两套H1各9页，两套H3各4页，共26页。查看四张联系表中的每一页，并放大检查基线H1第4／6页、候选H1第5页、候选H3第2页。未发现可见的对象缺失、文字遮挡或表格错行；基础版式仍以表格为主，核心证据页口头负担及长标题留待真实听众反馈。AI看图不是投影现场可读性或美学优越性证明。

预览：[H1基线](trials/arm-p/H1-ppt/preview/contact-01.png)、[H1候选](trials/arm-q/H1-ppt/preview/contact-01.png)、[H3基线](trials/arm-p/H3-ppt/preview/contact-01.png)、[H3候选](trials/arm-q/H3-ppt/preview/contact-01.png)。各`preview/`保存逐页PNG、PDF及带哈希的`render.json`；其中自动字段`visual_review=not_performed`表示渲染脚本本身不评审图片，人工式AI图像检查记录在本段。

每套计划、生成和结构核对成功。来源事实核对另见盲评；脚本不认证原研究事实。480／240秒是计划，不是实际演讲计时。写作只测试了英文引言末段与讨论，未覆盖完整论文、真人修稿、中文新写、所有学科及长期迁移。

## 复现

从仓库根目录运行；输出路径必须是新目录：

```text
python evals/capability-20261013/distillation/fetch_holdout.py --out edu_output/new-holdout-sources
python evals/capability-20261013/distillation/freeze_candidates.py edu_output/new-frozen-arms
python skills/edu-ppt/scripts/build_deck.py --plan evals/capability-20261013/distillation/trials/arm-q/H1-ppt/plan.json --out edu_output/rebuilt-h1
python skills/edu-ppt/scripts/check_deck.py --pptx edu_output/rebuilt-h1/slides.pptx --plan evals/capability-20261013/distillation/trials/arm-q/H1-ppt/plan.json --out edu_output/rebuilt-h1/checks.json
python skills/edu-ppt/scripts/render_deck.py --pptx edu_output/rebuilt-h1/slides.pptx --out edu_output/rebuilt-h1-preview
```

脚本生成和核对可复现；重新让模型按相同请求生成不会保证逐字或评分相同。恢复基线指令需要git中保留`08aa933`，不是只下载源代码ZIP。来源获取保留真实状态与哈希；服务器响应改变时不覆盖旧输入、不把HTML验证页当论文。PDF文字抽取布局随工具版本可能变化，盲评的行号对应原次抽取，章节／表号可用于回查。完整论文仍仅下载到本地忽略目录。
