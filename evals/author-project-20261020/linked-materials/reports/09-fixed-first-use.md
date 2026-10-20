# 材料关联核对

只核对登记材料和明确对应的位置；未映射及未解析内容不作一致性保证。
已一致 18 处；疑似旧内容 15 处；需重新判断 10 处；未能检查 7 处。完整明细在 check.json。

| 文件及位置 | 当前内容 | 对应材料 | 判断 | 处理依据 |
|---|---|---|---|---|
| manuscript.docx / docx:p:2 | 正式试验8周课程完成率：干预组70.0%，对照组60.0%；未调整风险比RR=1.166667; 95%CI=[1.001200,1.359400]。 | result-current.json / json:/phase2/rate_treated: {'value': '0.65'} | 疑似旧内容 | Value differs from the confirmed source for this analysis identity. 核对本处归属后同步；不要全局替换同一数字。 |
| results.csv / csv:2:6 | 70.0 | result-current.json / json:/phase2/rate_treated: {'value': '0.65'} | 疑似旧内容 | Value differs from the confirmed source for this analysis identity. 核对本处归属后同步；不要全局替换同一数字。 |
| discussion.md / line:2 | 正式试验干预组课程完成率70.0%，对照组为60.0%。 | result-current.json / json:/phase2/rate_treated: {'value': '0.65'} | 疑似旧内容 | Value differs from the confirmed source for this analysis identity. 核对本处归属后同步；不要全局替换同一数字。 |
| slides.pptx / ppt:2:completion/body/0:text | 干预组70.0%；对照组60.0% | result-current.json / json:/phase2/rate_treated: {'value': '0.65'} | 疑似旧内容 | Value differs from the confirmed source for this analysis identity. 核对本处归属后同步；不要全局替换同一数字。 |
| slides.pptx / ppt:2:completion/visual/chart:series:0:value:0 | 70.0 | result-current.json / json:/phase2/rate_treated: {'value': '0.65'} | 疑似旧内容 | Value differs from the confirmed source for this analysis identity. 核对本处归属后同步；不要全局替换同一数字。 |
| slides.pptx / ppt:2:notes | 干预组70.0%，对照组60.0%。  来源：合成材料 · completion 预计讲解：40秒 | result-current.json / json:/phase2/rate_treated: {'value': '0.65'} | 疑似旧内容 | Value differs from the confirmed source for this analysis identity. 核对本处归属后同步；不要全局替换同一数字。 |
| deck-plan.json / json:/slides/1/body/0 | 干预组70.0%；对照组60.0% | result-current.json / json:/phase2/rate_treated: {'value': '0.65'} | 疑似旧内容 | Value differs from the confirmed source for this analysis identity. 核对本处归属后同步；不要全局替换同一数字。 |
| deck-plan.json / json:/slides/1/visual/series/0/values/0 | 70 | result-current.json / json:/phase2/rate_treated: {'value': '0.65'} | 疑似旧内容 | Value differs from the confirmed source for this analysis identity. 核对本处归属后同步；不要全局替换同一数字。 |
| deck-plan.json / json:/slides/1/notes | 干预组70.0%，对照组60.0%。 | result-current.json / json:/phase2/rate_treated: {'value': '0.65'} | 疑似旧内容 | Value differs from the confirmed source for this analysis identity. 核对本处归属后同步；不要全局替换同一数字。 |
| manuscript.docx / docx:p:2 | 正式试验8周课程完成率：干预组70.0%，对照组60.0%；未调整风险比RR=1.166667; 95%CI=[1.001200,1.359400]。 | result-current.json / json:/phase2/rr: {'value': '1.083333', 'low': '0.890141', 'high': '1.318456'} | 疑似旧内容 | Value differs from the confirmed source for this analysis identity. 核对本处归属后同步；不要全局替换同一数字。 |
| manuscript.docx / docx:p:9 | RR=1.166667; 95%CI=[1.001200,1.359400] | result-current.json / json:/phase2/rr: {'value': '1.083333', 'low': '0.890141', 'high': '1.318456'} | 疑似旧内容 | Value differs from the confirmed source for this analysis identity. 核对本处归属后同步；不要全局替换同一数字。 |
| results.csv / csv:4:6 | RR=1.166667; 95%CI=[1.001200,1.359400] | result-current.json / json:/phase2/rr: {'value': '1.083333', 'low': '0.890141', 'high': '1.318456'} | 疑似旧内容 | Value differs from the confirmed source for this analysis identity. 核对本处归属后同步；不要全局替换同一数字。 |
| discussion.md / line:3 | 未调整风险比RR=1.166667; 95%CI=[1.001200,1.359400]。 | result-current.json / json:/phase2/rr: {'value': '1.083333', 'low': '0.890141', 'high': '1.318456'} | 疑似旧内容 | Value differs from the confirmed source for this analysis identity. 核对本处归属后同步；不要全局替换同一数字。 |
| slides.pptx / ppt:3:effect/body/0:text | RR=1.166667; 95%CI=[1.001200,1.359400] | result-current.json / json:/phase2/rr: {'value': '1.083333', 'low': '0.890141', 'high': '1.318456'} | 疑似旧内容 | Value differs from the confirmed source for this analysis identity. 核对本处归属后同步；不要全局替换同一数字。 |
| deck-plan.json / json:/slides/2/body/0 | RR=1.166667; 95%CI=[1.001200,1.359400] | result-current.json / json:/phase2/rr: {'value': '1.083333', 'low': '0.890141', 'high': '1.318456'} | 疑似旧内容 | Value differs from the confirmed source for this analysis identity. 核对本处归属后同步；不要全局替换同一数字。 |
| discussion.md / line:10 | 加权敏感性分析RR=1.02; 95%CI=[1.00,1.04]。 | result-current.json / json:/phase2/sensitivity: {'value': '1.020000', 'low': '1.000400', 'high': '1.039984'} | 需重新判断 | Displayed precision changes sign or relation to a reference boundary. 重新阅读相关材料并判断，不自动选结果或改写。 |
| discussion.md / line:7 | 某子组课程完成率70.0%，分母和组别仍待作者确认。 | — | 需重新判断 | Authoritative version is not established; alternative results were retained. 重新阅读相关材料并判断，不自动选结果或改写。 |
| manuscript.docx / docx:p:3 | 完成率优势排除了无效应，说明课程适合推广。 | — | 需重新判断 | Related material or wording changed: 解释依赖未调整风险比及区间是否覆盖无效应参考值1 重新阅读相关材料并判断，不自动选结果或改写。 |
| discussion.md / line:4 | 完成率优势排除了无效应，因此推荐立即普遍推广。 | — | 需重新判断 | Related material or wording changed: 解释依赖未调整风险比及区间是否覆盖无效应参考值1 重新阅读相关材料并判断，不自动选结果或改写。 |
| discussion.md / line:8 | 从新材料看，完成率的点估计仍向干预组倾斜，但需要关注区间宽度。 | — | 需重新判断 | Related material or wording changed: 解释依赖未调整风险比及区间是否覆盖无效应参考值1 重新阅读相关材料并判断，不自动选结果或改写。 |
| slides.pptx / ppt:3:effect/message:text | 区间下限高于1 | — | 需重新判断 | Related material or wording changed: 解释依赖未调整风险比及区间是否覆盖无效应参考值1 重新阅读相关材料并判断，不自动选结果或改写。 |
| slides.pptx / ppt:3:notes | 未调整模型排除了无效应；调整模型仍不精确。  来源：合成材料 · effect 预计讲解：40秒 | — | 需重新判断 | Related material or wording changed: 解释依赖未调整风险比及区间是否覆盖无效应参考值1 重新阅读相关材料并判断，不自动选结果或改写。 |
| deck-plan.json / json:/slides/2/message | 区间下限高于1 | — | 需重新判断 | Related material or wording changed: 解释依赖未调整风险比及区间是否覆盖无效应参考值1 重新阅读相关材料并判断，不自动选结果或改写。 |
| deck-plan.json / json:/slides/2/notes | 未调整模型排除了无效应；调整模型仍不精确。 | — | 需重新判断 | Related material or wording changed: 解释依赖未调整风险比及区间是否覆盖无效应参考值1 重新阅读相关材料并判断，不自动选结果或改写。 |
| discussion.md / line:9 | 引用论断：同伴反馈帮助受访学生解释作业要求。[SYN-01] | — | 需重新判断 | Claim, source version, support passage or citation ledger changed; old support is pending re-review. 重新阅读相关材料并判断，不自动选结果或改写。 |
| manuscript.docx / word/header1.xml | — | — | 未能检查 | Ancillary Word part not checked. 补足可读材料或重新定位后检查。 |
| slides.pptx / ppt:1:3 | — | — | 未能检查 | Nontext drawing: geometry/meaning not checked. 补足可读材料或重新定位后检查。 |
| slides.pptx / ppt:2:3 | — | — | 未能检查 | Nontext drawing: geometry/meaning not checked. 补足可读材料或重新定位后检查。 |
| slides.pptx / ppt:2:completion/visual/chart | — | — | 未能检查 | Chart label formatting/geometry require edu-ppt check_deck and rendering. 补足可读材料或重新定位后检查。 |
| slides.pptx / ppt:3:3 | — | — | 未能检查 | Nontext drawing: geometry/meaning not checked. 补足可读材料或重新定位后检查。 |
| formula-supplement.xlsx / 辅助计算!D2 | — | — | 未能检查 | Formula not recalculated; cached value is not authoritative. 补足可读材料或重新定位后检查。 |
| broken-supplement.docx / @RUN@\materials\broken-supplement.docx | — | — | 未能检查 | BadZipFile: File is not a zip file 补足可读材料或重新定位后检查。 |

## 检查范围

- new: 读取 17 个单元，映射 9 个；解析状态 read。其余单元需结合正文判断。
- old: 读取 16 个单元，映射 0 个；解析状态 read。其余单元需结合正文判断。
- doc: 读取 16 个单元，映射 5 个；解析状态 read。其余单元需结合正文判断。
- csv: 读取 42 个单元，映射 4 个；解析状态 read。其余单元需结合正文判断。
- md: 读取 10 个单元，映射 9 个；解析状态 read。其余单元需结合正文判断。
- plan: 读取 61 个单元，映射 6 个；解析状态 read。其余单元需结合正文判断。
- ppt: 读取 32 个单元，映射 10 个；解析状态 read。其余单元需结合正文判断。
- reading: 读取 2 个单元，映射 1 个；解析状态 read。其余单元需结合正文判断。
- ledger: 读取 4 个单元，映射 0 个；解析状态 read。其余单元需结合正文判断。
- formula: 读取 8 个单元，映射 0 个；解析状态 read。其余单元需结合正文判断。
- broken: 读取 0 个单元，映射 0 个；解析状态 failed。其余单元需结合正文判断。
