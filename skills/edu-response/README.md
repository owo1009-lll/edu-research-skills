# `edu-response` 技能

[English](README_EN.md)

回复期刊审稿意见：拆分意见、确定处理方案、改稿，交付修改说明或回复信和标红稿。

## 适合用它做什么

- 大修、小修、退修再审
- 中文期刊的修改说明、英文期刊的 response letter 和 cover letter
- 修改稿标红

## 典型请求

- "根据这份外审意见改稿并写修改说明"
- "Write a point-by-point response to these reviewers"

## 你需要提供

- 审稿意见（编辑信和各审稿人意见）、原稿；已有的修改想法

## 产出

- 意见清单（comments.csv）、修改稿、标红稿、修改说明或回复信、cover letter、需要用户完成的事项

## 运行和依赖

- Python 3.9 及以上，python-docx；新分析由 edu-analysis 在 R 中运行

## 边界

- 只写实际做了的修改；新分析必须实际运行，新文献必须核验；不为迎合审稿人改变结论的性质

## 相关技能

- edu-writing（修改规则）、edu-analysis（补充分析）、edu-review（投稿前模拟）

## 状态

- Beta：检查脚本和标红脚本在预埋问题的样例上测试；完整流程在一组合成审稿意见上试用
