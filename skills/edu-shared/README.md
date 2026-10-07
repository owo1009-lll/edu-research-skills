# `edu-shared` 技能

[English](README_EN.md)

其他 edu-* skill 共用的支持包，不单独处理任务。

## 适合用它做什么

- 提供运行 R 并记录每次分析的运行层（`scripts/edu_runtime.py`）
- 提供所有模块共用的诚信规则（`references/integrity.md`）

## 典型请求

- 不直接调用；由其他模块通过 `../edu-shared/` 引用

## 你需要提供

- 无

## 产出

- 运行文件夹中的 provenance.json、run_status.json、sessionInfo.txt

## 运行和依赖

- Python 3.9 及以上；运行分析时需要 R

## 边界

- 必须与其他 edu-* skill 装在同一个 skills 目录下

## 相关技能

- edu-analysis、edu-audit（运行层）；全部模块（诚信规则）

## 状态

- Stable：作者已在真实研究材料上使用；随各模块一起测试
