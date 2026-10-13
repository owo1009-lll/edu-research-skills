# 教育学能力定向修订：2026-10-13

本轮基线：[08aa933](https://github.com/owo1009-lll/edu-research-skills/tree/08aa93320c356b75fd0f6bfc61b5df02f98e2682)。三项任务分别保存证据，功能验证与写作质量判断分开报告。

| 任务 | 当前记录 |
|---|---|
| PPT逐点标签与区间错行 | [复现与验证](ppt-checks.md) |
| 写作与汇报蒸馏及留出迁移 | [完整对照、盲评和取舍](distillation/README.md)；新写作卡不采用，汇报卡缩到文章解读 |
| 目标期刊与编辑团队检索 | [AJET端到端示例](journal/README.md)、[引用建议](journal/recommendations.md)、[实际改稿](journal/manuscript-after.md) |

公开材料只使用公开许可材料的合法摘述和明确合成示例，不包含用户私有稿件。发布版本为0.12.0。没有把测试数量当作写作质量证明。

## 修改文件与理由

| 文件／组 | 实际修改及原因 |
|---|---|
| `skills/edu-ppt/scripts/chart_labels.py`、`build_deck.py`、`plan.py` | 将逐点正文、格式、显隐及对整体／系列设置的覆盖纳入生成和核对，支持合法百分比和类别意图；未支持来源明确报告未验证 |
| `skills/edu-ppt/scripts/fidelity.py` | 区间名称、线、点、数值文字按相对位置关联，捕捉只移动部分对象的错行，允许整行移动与整体布局变化 |
| `tests/test_ppt_fidelity.py`、PPT计划格式与`examples/label-row-plan.json` | 两个真实修改反例及正常格式／移动正例；保留既有对象检查，公开四页可运行计划和渲染 |
| `skills/edu-writing/references/introduction.md`、使用手册对应段落 | 取消段数、固定连接词和引用比例配额，修复与既有“语料统计仅供参照”原则的冲突；不是新的固定结构 |
| `skills/edu-ppt/references/spoken-evidence.md`、`article-reading.md` | 仅为文章解读加入可选证据组织办法；路线A规则不按候选卡扩展，四步走与两种交付模式保留 |
| `skills/edu-writing/scripts/search_journal.py`、`references/target-journal.md`、`tests/test_journal_search.py` | 实际交叉检索与来源记录；验证角色、身份冲突、阅读范围和取舍信息，复用既有引用身份核验 |
| `edu-writing`入口及中英文说明、`edu-research`入口、`edu-ppt`入口 | 写作中识别目标期刊请求并路由；自有研究定位贡献时可复用已核实文献；文章解读不默认查编辑团队 |
| 本目录、根说明、插件清单与`skills/release.json` | 保存完整公开证据及复现命令，同步0.12.0版本和实际适用范围 |

## 实际验证

- [完整单元／端到端测试日志](all-tests.txt)：`python -B -X utf8 -m unittest discover tests -v`，107项通过、无跳过。包括新增8项期刊检索测试，以及原有表格、类别、系列、单位、坐标、图例、图片、流程、引文、模板、内容模式和讲稿检查。
- [其他验证](additional-validation.txt)：R已知答案154／154通过；三个修改技能的`quick_validate.py`均通过。Windows子进程移除了宿主遗留的`LANG`、`LANGUAGE`及`LC_*`变量，避免R误用`C.UTF-8`；未修改用户环境或R实现。
- PPT两处漏洞的[修改前](ppt-before.json)与[修改后](ppt-after.json)都来自实际PPTX修改；正常成品与完整行移动可通过。新四页示例全部实际渲染并逐页看图；留出四套共26页的查看范围见[渲染记录](distillation/README.md)。
- 留出公开打包后的四套PPT再次核对，均通过：[结果](distillation/published-deck-checks.json)。从公开计划重新生成H1也通过；两个冻结指令目录按公开脚本重建后哈希完全一致：[复现检查](distillation/reproduction-check.json)。
- [再次获取来源](distillation/source-refetch.json)：H1主文、更正及H2的原文件哈希与试用一致；T2原文件哈希也与训练下载记录一致。HTML响应不得作为PDF被接收；文字抽取行号可能随工具变化。
- 期刊检索实际运行11个A/B/C查询，遇到的429及重试保留；52篇API候选加1篇有记录的理论补充。8篇重点取舍、45篇明确未评阅；正文使用5篇，已完成[在线身份核验](journal/identity-verification/verified.json)与[最终记录核对](journal/decision-check-final.json)。真实姓名误命中与合成的同名不同ORCID测试分开报告。
- 公开文件链接、190个试用发布副本哈希和Office文件中的本机路径检查完成。未发布原始全文、私人文件或运行缓存。

## 仍需区分的范围

自动PPT检查验证成品与已核实计划的对应，不能认证原材料事实。外部工作簿、动态字段及未实现的复杂自定义标签来源仍报告未验证；不保证任意Office版本渲染一致。实际渲染不等于真实试讲。

写作迁移未显示稳定全面提升，W1新卡没有进入正式版本。当前有价值的汇报组织办法仅在一篇新文章中观察到局部收益；完整英文论文、中文新写、理论／质性汇报及真人试讲仍未在本轮验证。完整评估输出保留已识别的待改处，未事后重写成胜出的测试稿。

期刊检索是有界候选发现；编辑身份和作者身份需要官方来源核对，不能据姓名命中自动认定。部分引用只读摘要，支持范围据此限定；身份字段通过不等于语义正确或保证没有更正。查编辑成果不设引用比例，也不预测录用或审稿人。
