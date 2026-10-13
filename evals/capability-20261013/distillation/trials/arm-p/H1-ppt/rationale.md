# H1-ppt：主线、来源与页面依据

## 动笔前主线

路线B，文章解读，中文、教育学研究生、约8分钟、9页。What：有辅助成绩与独立学习的区别；Why：原作者回顾的生产力证据不能替代撤去工具后的测验；How：三臂、共同教学流程、课次内的无辅助主结局；Result：练习提高与考试损失并存，Tutor未显示考试收益，日志支持但不单独识别“拐杖”机制；收尾：评价AI须看独立能力，保护设计是部署条件。

## 来源范围与边界

- H1.txt与H1.xml：完整主文、两张表、图注、脚注与参考文献。以节标题和表号定位。H1-correction.txt：完整更正，仅作者单位。
- 主文提供足够核心结果，未独立阅读SI Appendix及主文引用的其他研究；不把“作者报告稳健性”写成此处重新运行或核验。
- 不使用任何原文图片。数值表、流程与对照表全为原生可编辑对象。主文数据以新表呈现，不复刻原图视觉作品。
- 按共同请求，子任务不渲染PPT、不声称视觉检查或试讲通过；主任务统一渲染。480秒是分配计划。

## 页面依据表

|页|理解任务|关键论断/素材|原文位置|角色/条件|
|---|---|---|---|---|
|1|提出问题|表现与短期独立学习区别|Significance；Abstract；Introduction|background；明确原作者与年份|
|2|解释为什么|工具在场的生产力与撤去后的能力|Introduction第1–5段|author_interpretation；其他文献为原作者回顾|
|3|解释操纵|控制、GPT Base、GPT Tutor多项保护包|Experimental Design第1段和分配段；Fig1图注|method；不将单一提示当孤立因果成分|
|4|解释测量与分组|共同复习—干预练习—教师讲解—无辅助考核|Experimental Design；Footnotes #；Main Results模型|method；普通班随机组成，课堂按特征和排课约束分臂；主结局考试|
|5|工具可用时|Base .137/.031，Tutor .361/.032，对照均值.284|Table1列1|finding；0–1归一化成绩、ITT、HC1按班级聚类；48/127为相对增幅|
|6|工具撤去后|Base −.054/.022，Tutor −.004/.013，对照均值.321|Table1列2|finding；短期、不是长期保持；非显著不是等效|
|7|解释证据|答案索取、实质求助；错误率交互|Potential Mechanism；Table2；Student Engagement|author_interpretation；观察日志与辅助分析，非机制随机操纵|
|8|实践判断及范围|保护独立尝试和评价；单校短期与组合操纵|Student Perception；Discussion|presenter_comment；明确汇报者借鉴，保留作者部署警示|
|9|一句话作答|现场试验证据将保护独立学习引入部署判断|Abstract；Table1；Discussion；Correction|presenter_comment；全文题录和更正范围|

## 统计与概念核对

Table1回归控制既往GPA、课次、评分者、年级、教师；标准误在课堂层聚类。2,848为学生—课次观测，避免放到样本人数位置。无辅助考试为预注册主要结局；主文调整后回归与预注册简单成对t检验区分，后者仅按主文称结果相似。五个班级课次未依从，主分析保留ITT身份。

术语：有辅助练习、无辅助考试、GPT Base、GPT Tutor、教学保护设计；“拐杖”只指原作者关于答案依赖的解释，非已经单独识别的中介路径。

## 取舍

保留两类结局各一页与主结果标准误，删除对主结论非必要的异质性/离散度附属分析。机制页不绘造未经给定的日志柱状数值，用准确对照表。未从显著性差别直接推断两个工具间显著不同。实践页保留应用判断力度，同时集中模型/地点/时程边界。

## 修订与检查

首稿为first-plan.json；一次内容AI自查见review.md；定稿为plan.json。后续补入实际build/check记录。

### 一轮修订记录

第6页概括语句改为“未检出”结果，保持未显著与零效应的区别；其余已核实论断、数值与讲稿保留。

具体问题、回源位置和自动检查结果见review.md。

### 实际交付与最终检查

- 9页；预计480秒，非试讲记录。
- 最终build_deck.py、check_deck.py均退出0；检查status=passed，errors/issues/warnings均空，plan_consistency=passed。
- 脚本source_fact_check=not_performed；本次AI回源核对范围见依据表和review.md。
- 未执行PPT渲染或逐页视觉复核；由主任务统一执行；不声明试讲通过。
- 完整逐页讲稿写入PPT备注，同时交付deck/speaker_notes.md；正文快照为deck/content.md。
