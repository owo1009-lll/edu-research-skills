# 材料关联核对

只核对登记材料和明确对应的位置；未映射及未解析内容不作一致性保证。
已一致 0 处；疑似旧内容 1 处；需重新判断 1 处；未能检查 0 处。完整明细在 check.json。

| 文件及位置 | 当前内容 | 对应材料 | 判断 | 处理依据 |
|---|---|---|---|---|
| discussion.md / line:1 | 正式试验干预组课程完成率70.0%；某子组课程完成率70.0%，分母和组别待确认。 | result-current.json / json:/phase2/rate_treated: {'value': '0.65'} | 疑似旧内容 | Value differs from the confirmed source for this analysis identity. 核对本处归属后同步；不要全局替换同一数字。 |
| discussion.md / line:1 | 正式试验干预组课程完成率70.0%；某子组课程完成率70.0%，分母和组别待确认。 | — | 需重新判断 | Authoritative version is not established; alternative results were retained. 重新阅读相关材料并判断，不自动选结果或改写。 |

## 检查范围

- new: 读取 17 个单元，映射 1 个；解析状态 read。其余单元需结合正文判断。
- md: 读取 1 个单元，映射 1 个；解析状态 read。其余单元需结合正文判断。
