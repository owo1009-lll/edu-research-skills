# 开发对照记录（评阅完成后解盲）

本记录不替代最终留出检验。D1/D2 为规则开发时已知的合成材料；没有真人稿件或参与者数据。源文精读与候选方法见 `../../distill/20261018/`。

## 固定输入

- 基线提交：`a4020c41a4f3d8ab180a4e2818955d90e40f6f3b`，公开 0.12.0。
- 基线技能字节：[dev-p01.json](snapshots/dev-p01.json)，200 个技能文件，整体摘要 `1d00faafb6eb42a90d32170c7960fa9f2023b029beb264d382c0902ecea7a194`。
- 候选开发快照：[dev-q01.json](snapshots/dev-q01.json)，203 个文件，整体摘要 `e69aead044e120a1359c15cf41a56b54808d7c1120e696de85d5b83f8e9087d7`。它是开发比较的固定输入，尚不是最终留出之前的冻结记录。
- [D1 请求](inputs/D1-request.md) / [材料](inputs/D1-materials.md)：英文新写引言、讨论、结论，定量主次结局与文献比较。
- [D2 请求](inputs/D2-request.md) / [材料](inputs/D2-materials.md)：合成作者稿压缩修改，保留 answerability 的作者定义、should 与章节，核对日志和访谈的含义。
- 每个任务每个版本两次独立生成，均使用上述相同任务文件；原始输出另存，禁止事后编辑样稿以改善得分。

## 执行范围与限制

写作者使用新上下文、继承宿主模型配置，不显式换模型；精确后端版本、温度与随机种子在工具中不可获得，不能声称这些参数受控。写作者只获给定技能、其必要引用及任务文件，无网络、无其他运行或开发评审记录。各自保存实际读取清单和检查输出。

早期三个基线运行使用原基线工作树；其后检查工作树无修改，并保存该树实际技能字节。D2 第二次与候选运行使用相同的文件式任务包装，仅替换技能路径、任务编号及输出目录。早期运行没有单独导出完整派发包装，因此不将整轮包装称为逐字一致。基线路径含 baseline 字样，也不能声称写作者完全不知道版本身份；评阅者通过另建 A/B 文件隔离版本与工作记录。最终留出将采用统一包装和中性快照路径。

首稿、检查器提示、自查与修订属于各版本实际工作流。检查器阈值未修改，脚本成功或提示较少不计为质量证据。

## 匿名评阅

[make_blind.py](make_blind.py) 对四组分别随机排列 A/B，原样复制 final.md，包括教学模拟说明；键与评阅输入分开保存。[judge-request.md](judge-request.md) 在评阅前固定八个比较维度，要求具体文本依据并单列严重错误。评阅者只读本组材料、请求、两稿及评阅说明，不读规则、其他组或键。

四组匿名稿均已评阅，保存原记录后解盲；结果见 [development-results.md](development-results.md)。评阅不称作者或专家验收。全部原始样稿、过程记录的公开副本及实际技能快照见 [development-artifacts](development-artifacts/README.md)。

## 已完成的机械检查

2026-10-18，工作树候选实施后：

| 命令或检查 | 结果 | 能说明什么 |
|---|---|---|
| skill-creator 的 `quick_validate.py skills/edu-writing` | Skill is valid | 技能元数据格式有效 |
| `python -X utf8 -m unittest discover -s tests -p test_contracts.py` | 10 项通过 | 现有结构、规则保留和链接约束 |
| `python -X utf8 -m unittest discover -s tests -p test_ppt*.py` | 25 项通过 | 原有 PPT 功能回归；本轮没有视觉渲染验收 |
| `python -X utf8 -m unittest discover -s tests -p test_journal_search.py` | 8 项通过 | 原有检索来源与身份逻辑；使用测试夹具，不代表一次在线搜索 |
| `git diff --check`（允许 CRLF） | 无问题 | 改动无空白错误 |
| 受保护路径差异 | 空 | `edu-ppt`、写作脚本、目标期刊指南、release.json 未变 |

这些结果不证明候选的论证、语言或迁移能力优于基线。

## 复现准备

从对应基线提交和候选工作树分别运行 `snapshot.py --source <仓库> --out <仓库外新目录> --manifest <新记录.json> --label <名称>`，核对清单中的技能文件字节。最终公开提交确定后将补入候选提交标识。将同一请求和材料交给同一可用模型配置的独立写作上下文，再按匿名评阅说明比较；后端或采样不同会产生不同文本，不能保证生成逐字复现。
