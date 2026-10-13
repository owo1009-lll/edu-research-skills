# H1-writing：论证与依据记录

## 任务、阅读与主线（动笔前）

性质：英文局部二次写作练习；引言末段约150词，Discussion约400–500词，不冒充原作者或用户研究。使用冻结的 arm-p edu-writing。实际阅读 H1 主文全部正文、表1与表2、图注、脚注、参考文献，以及更正全文；没有读取补充材料正文，也没有独立读取主文所引生产力或辅导研究。外部研究仅写成 Bastani 等的文献回顾。

主线：学习者在工具可用时完成任务的表现，是否对应撤去工具后的独立掌握？原研究在土耳其一所高中课堂实施三臂实验，按课堂分配工具、利用普通班学生原有的随机分班，比较练习成绩和紧随其后的无辅助考试。GPT Base 提高练习成绩却降低考试成绩；GPT Tutor 的考试点估计接近零、未检出收益。贡献是给出工具表现与短期独立学习分离的现场因果证据，并使教学保护设计成为部署判断的一部分。互动日志支持作者“拐杖”解释，但不能把非显著错误率交互解释为排除了误导机制。实践上应保护独立解题并用撤去工具后的测验评估部署，而不能仅以练习表现或满意度验收。

## 写作依据表与跨节对应

|单元|功能|论点|来源位置|写法/必要条件/修改理由|
|---|---|---|---|---|
|引言末段|问题与设计贡献|有辅助表现不能代表独立掌握|H1 Introduction 最后两段；Experimental Design|用第三人称指明原作者；不把短期考试写成长期保持|
|讨论1|回答主问题|Base练习收益与考试损失并存；Tutor未检出考试收益|Main Results；Table 1|保留0–1量尺、对照组、短期；不把Tutor非显著写成等效|
|讨论2|解释与反证|日志使答案依赖成为有依据的解释；错误传播尚未排除|Potential Mechanism；Table 2；Student Engagement；Fig.3图注|错误率不是单独随机化的机制；Tutor同时改变多项条件|
|讨论3|推进教育认识|独立测验与参与过程应进入部署评价|Student Perception；Discussion 第1、3段|保留作者应当保护学习的立场；区分应用判断与已验证干预|
|讨论4|范围与结尾|此证据针对短期、单校、2023年GPT-4部署|Discussion 最后段；Footnote ‡|集中一次说明设计边界；结尾返回评价标准|
|稿后|归属与更正|原作者、DOI、更正范围|H1题录；H1-correction全文|更正仅修复Osbert Bastani单位，不涉及统计值|

## 支持与约束

- 支持：按课堂分配；普通班随机分班；同一内容的练习与相似考试题；共同教师复习与课后讲解；独立评分；按课堂聚类稳健标准误；意向处理分析；日志提供过程材料。
- 约束：主分析排除非随机组成的荣誉班；预注册主要结局是无辅助考试，主文回归并非预注册的简单成对t检验；短期考试；单校数学；GPT Tutor同时提供正确解答、常见错误反馈和不直接给答案的提示；补充稳健性只按主文报告，无独立核验。
- 主文数值：Base练习0.137（SE 0.031），Tutor练习0.361（0.032）；Base考试−0.054（0.022），Tutor考试−0.004（0.013）；考试对照均值0.321。均为0–1量尺上的调整后差值，2,848为学生—课次观测数，不是人数。
- 机制表2：Base×逻辑错误率考试−0.029（SE0.040），不显著不等于错误传播为零；不以两个练习交互“都显著”证明同等大小。

## 术语

|术语|固定写法|含义|
|---|---|---|
|生成式人工智能|generative artificial intelligence (AI)|首次全称，之后AI|
|普通工具|GPT Base|原作者定制、近似ChatGPT界面的GPT-4工具，非ChatGPT所有版本|
|保护工具|GPT Tutor|提示与教师题目专用知识组成的干预包|
|辅助练习|assisted practice|允许条件指定资源的练习|
|无辅助考试|unassisted exam|同课次闭卷、关电脑、独立作答|
|学习|short-term learning / independent performance|不扩展成长时保持或广泛迁移|

## 修订记录

待首稿自动线索检查与AI自查后补入。检查不证明事实正确或专家审核。

### 一轮完整修订（已完成）

- 原文：students can complete more successfully with a tool
  终稿：students can complete tasks more successfully with a tool
- 原文：The tutor safeguards largely mitigated the observed harm, without establishing an independent-learning benefit.
  终稿：With GPT Tutor, the estimated exam penalty was much smaller; a positive independent-learning benefit was not established.
- 原文：For mathematics tasks like those studied here, teacher-designed hints and reliable problem-specific guidance are a justified safeguard to investigate and refine.
  终稿：For mathematics tasks like those studied here, schools should favor tutor designs that protect students' own attempts and provide dependable guidance, while checking independent outcomes.
- 原文：## Original research and correction
  终稿：## References

逐项理由见review.md。首稿与脚本日志均保留；终稿重新检查范围同首稿。

### 实际交付与最终检查

- 最终引言152词；Discussion 458词。
- 三个最终检查均成功执行（退出0）；所有线索已按review.md逐项判断，未把退出码或零线索当质量证明。
- final.docx由冻结md_to_docx.py实际生成；未进行Word视觉渲染。
