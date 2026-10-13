# edu-ppt 开发与验收记录

目标来源：用户2026-10-13附件，包含写作定向修复及完整edu-ppt实现。前一轮属于实际进展：完成写作修复、最终快照六案复测与本地安装；不是整体目标完成。

## 当前证据与待完成项

| 要求 | 证据或验收方式 | 状态 |
|---|---|---|
| 写作七项定向修复，最终快照对照复测 | smoke-evaluation.md最后一节；本地12份终稿与6份盲评，改善/持平/退步分别记录 | 已完成本轮修复复测，质量仍有明确局部缺陷，未宣称全通过 |
| edu-ppt统一入口，两路线两模式，无旧名冲突 | 技能、脚本和文件全树核对 | 已实现；无冲突旧入口 |
| own完成/方案/进展的内容身份 | 自有真实论文与合成进展案例，逐页来源和完成状态检查 | 已验收指定两例；方案有身份规则及验证器 |
| article全文/选题检索、多篇比较、四步走 | 真实公网检索、全文记录、选文理由与内容稿 | 已完成核心全文与较早候选阅读范围分列；不宣称遍历所有多文综合形式 |
| 逐页文案、视觉安排、讲稿、来源、时长 | schema及导出Markdown和备注往返检查 | 已完成；修复JSON表格与空正文导出 |
| 四项目当前实现、依赖、许可证核查 | 2026-10-13读取源码快照，选python-pptx | 已保存references/open-source.md |
| 原生可编辑PPTX、模板适配、复用冻结内容 | 打开OOXML、编辑往返、模板与内容哈希检查 | 指定案例通过；模板边界另记 |
| 实际渲染、遮挡/字体/符号/来源/讲稿检查 | PowerPoint渲染，逐页视觉阅读和检查记录 | 五套成品50页实际渲染，AI检查；无真人排练 |
| 路由、安装、发布、中英文说明、手册、触发测试 | 安装器和完整仓库测试 | 本机0.11.0已安装，84项通过，路由49/50；本轮未推送远端 |
| 七类场景，自动/AI/人工分开报告 | evals/edu-ppt-evaluation.md及任务目录产物 | 已完成本轮验证；人工反馈尚无，维持Beta |
| 用户资料不入技能仓库，公开示例合法或合成 | git差异/打包清单审阅；真实稿仅临时目录 | 持续遵守 |

源码快照保存在忽略目录 `edu_output/edu-ppt-dev-20261013/upstream/`。本轮不把大型Web、RAG或新模型密钥作为依赖。

## 参考源码

- HKUDS/Paper2Slides：0785051d1f52814097e94c44751e3f12b83f7c8a，MIT；已读pipeline分阶段执行及requirements。
- celestial-micha/paper2ppt：fc8a91495346d29dfb72df35fbefb5832d6d99e6，MIT（LICENSE署名HKUDS）；已读原生生成、讲稿和QA实现及requirements。
- gitbrent/PptxGenJS：3c9ec1b687c174952166f6a34b5e87ebf69fa469，package 4.0.1，MIT；已核对addNotes/addChart/addTable与依赖。
- scanny/python-pptx：278b47b1dedd5b46ee84c286e77cdfb0bf4594be，MIT；已核对notes_text_frame、add_chart、add_table、add_picture及pyproject。本机可运行版1.0.2。

实现不拷贝这些项目的代码，仅采用其分阶段、内容/版式分离、原生对象与定点复查的设计方法。

完整验收、实际缺陷、修复后复验及未覆盖范围见[edu-ppt-evaluation.md](edu-ppt-evaluation.md)。该记录已从开发待办更新为完成记录，不把写作复测的局部退步隐藏为整体通过。
