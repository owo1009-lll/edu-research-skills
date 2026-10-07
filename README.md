# 教育学科研 Skill

面向教育学研究者的一组 Skill，可在 Claude Code、Codex 和 WorkBuddy 中使用。覆盖从选题与研究设计、数据分析、访谈编码、结果复核，到中英文论文写作、投稿前外审模拟、返修回复和课题申报书的全过程。统计分析实际运行 R，每次运行都留下脚本、数据指纹和日志；写作按已发表的 CSSCI 与 SSCI 论文校准语气。

当前版本 **0.7.0**。

## 可以用来做什么

在你的论文文件夹里打开 Claude Code 或 Codex，把材料放进去，直接说需求。Claude Code 会按需求自动调用相应 skill；Codex 中可以用 `$edu-research` 点名入口。

| 你有什么 | 直接这样说 | 得到什么 |
|---|---|---|
| 问卷数据 | "检验这份量表的信效度，做共同方法偏差检验和结构方程模型" | α、CFA、CR/AVE、HTMT、共同方法偏差检验、路径与中介结果，三线表和结果段落 |
| 问卷数据，SEM + 组态 | "在 SEM 之外再做 fsQCA 和 NCA，看哪些条件组合导致高学习投入" | 校准表、必要性分析、核心/边缘组态表、稳健性检验；NCA 效应量与瓶颈表 |
| 实验或准实验数据 | "比较实验组和对照组的后测成绩，控制前测" | 描述统计、t 检验或协方差回归、效应量 |
| 调查数据，类别变量 | "看性别和年级与是否使用 AI 工具有没有关系" | 卡方或 Fisher 检验、Cramér's V、调整残差 |
| 班级嵌套或多时点数据 | "学生嵌在班级里，做多层模型" / "三次测量，做增长模型" | ICC、多层或纵向模型结果 |
| 访谈记录 | "用扎根理论做三级编码，建一个形成机理模型" / "做主题分析" | 编码表、范畴、饱和检验、带引文的结果叙述 |
| 背景、方法、结果 | "写一篇投《电化教育研究》的完整论文" / "写英文 Discussion" / "写中英文摘要" | 先确认一次主线，再交付含三线表、图和核验引用的 Word 稿 |
| 已有初稿 | "修改讨论部分，保留我的论点和结构" / "检查全文数字和术语是否前后一致" | 修改稿与改动理由；一致性检查结果 |
| 写好的稿件，准备投稿 | "从审稿人角度看看这篇稿子哪里会被拒" | 两三位独立的模拟审稿人报告、综合报告和按优先级的修改清单 |
| 收到审稿意见 | "根据外审意见改稿并写修改说明" / "写英文 response letter" | 意见清单、修改稿、标红稿、修改说明或回复信、cover letter |
| 稿件的结果部分 | "看看我的统计报告规不规范" | 缺自由度、效应量、区间等问题的审查表和建议写法 |
| 已发表论文的数据 | "核对这篇论文表 4 的计数和风险比" | 原值与复算值对照 |
| 申报课题 | "按今年全国教育科学规划的活页，写一份申报书" | 论证地图和证据表，确认主线后交付活页正文；字数、匿名和"首次""填补空白"等说法的检查 |
| 只有选题 | "围绕生成式 AI 与大学生自主学习，提出可做的研究问题和设计" | 文献核对、候选问题、框架与研究设计 |

所有结果写在论文文件夹下的 `edu_output/`，原始数据不上传。

## 安装

需要 Python 3.9 及以上；做统计分析还需要 R 4.1 及以上。

**推荐：安装脚本**（同时装到 Claude Code 和 Codex，可更新、可卸载，不会覆盖你自己的同名目录）

```bash
git clone https://github.com/owo1009-lll/edu-research-skills.git
cd edu-research-skills
python scripts/install.py                  # 同时安装到 Claude Code 和 Codex
python scripts/install.py --host claude    # 只装 Claude Code（--host codex 只装 Codex）
```

装好后开一个新会话即可使用。更新：`git pull` 后运行 `python scripts/install.py --action update`；卸载：`--action uninstall`（只删除本安装器装的目录）；查看状态：`--action status`。

**Claude Code 插件**（需要能访问本仓库的 git 权限）

```
/plugin marketplace add owo1009-lll/edu-research-skills
/plugin install edu-research-skills@edu-research-skills
```

插件方式下 skill 名带前缀（如 `edu-research-skills:edu-writing`）。两种方式选一种，不要同时装。

**WorkBuddy（腾讯）**

有 Python 时，在仓库文件夹里运行：

```bash
python scripts/install.py --host workbuddy     # 个人版，装到 %USERPROFILE%\.workbuddy\skills
python scripts/install.py --host codebuddy     # 企业版或 CodeBuddy，装到 %USERPROFILE%\.codebuddy\skills
```

不想用命令行时，手动安装：

1. 在本仓库页面点 Code → Download ZIP，解压。
2. 打开解压后的 `skills` 文件夹，把里面的 9 个文件夹（`edu-research`、`edu-analysis`……`edu-shared`）全部复制到 `C:\Users\你的用户名\.workbuddy\skills\`（Mac 是 `~/.workbuddy/skills/`；文件夹不存在就新建）。`edu-shared` 不能漏，其他模块要用它。
3. 重启 WorkBuddy，在技能列表里能看到 edu-research 等模块即可。

WorkBuddy 用的是同一套 SKILL.md 格式，写作、审稿、申报书等文字类功能直接可用；统计分析和生成 Word 需要电脑上装有 R 和 Python（见下文），并允许 WorkBuddy 运行本地命令。本仓库在 Claude Code 和 Codex 中测试过，WorkBuddy 中没有实测。

**其他支持 SKILL.md 的 Agent**：把 `skills/` 下的所有文件夹（包括 `edu-shared`）复制到该 Agent 的 skills 目录，保持目录结构不变。

首次做统计分析时，助理会运行自检（`edu-analysis/tests/known_answers.R`），缺少的 R 包用 `Rscript edu-analysis/scripts/setup_packages.R` 安装到 R 的用户库。生成 Word 稿需要 python-docx 和 matplotlib（`edu-writing/requirements.txt`）。

## 模块

| Skill | 负责 | 状态 |
|---|---|---|
| [`edu-research`](skills/edu-research/README.md) | 入口：判断任务、分派模块；选题、研究问题与研究设计 | Beta |
| [`edu-analysis`](skills/edu-analysis/README.md) | 统计分析：描述与信效度、差异检验、卡方、相关与回归、调节与中介、CFA、共同方法偏差、CB-SEM、PLS-SEM、fsQCA、NCA、多层与纵向 | Beta |
| [`edu-qual`](skills/edu-qual/README.md) | 定性分析：反思性主题分析、代码本内容分析、扎根理论三级编码、编码一致性 | Beta |
| [`edu-audit`](skills/edu-audit/README.md) | 结果复核：已报告统计值的复算；统计报告审查 | Beta |
| [`edu-writing`](skills/edu-writing/README.md) | 中英文论文写作与修改（标题摘要到结论与建议）、三线表与图、引用核验、Word 交付（英文 APA，中文 GB/T 7714）、语气检查、全文一致性检查 | Beta |
| [`edu-review`](skills/edu-review/README.md) | 投稿前外审模拟：独立的模拟审稿人、编号的问题与解决标准、综合与修改清单；申报书评审视角 | Beta |
| [`edu-response`](skills/edu-response/README.md) | 返修回复：意见清单、处理方案、改稿、修改说明或回复信、标红稿、一致性检查 | Beta |
| [`edu-proposal`](skills/edu-proposal/README.md) | 课题申报书与开题报告：论证地图、证据表、栏目计划；字数、匿名和措辞检查 | Beta |
| [`edu-shared`](skills/edu-shared/README.md) | 共用的运行层（查找 R、记录运行）和诚信规则，不单独处理任务 | Beta |

状态的含义：Draft 规则已定义，只在样例上测过脚本；Beta 已在示例任务上试用，仍可能有边界问题；Stable 已在真实研究材料上验证。目前所有模块都只在合成数据或公开示例上试用过，没有标为 Stable 的。

## 质量检查

- **分析函数**：33 项已知答案检查，标准答案来自 R 文档例题、lavaan 教程的拟合值，以及可以手算的解析解；fsQCA 和 PLS 逐项对照原始包的输出。
- **写作语气与写法**：
  - **语气**：依据 27 篇 CSSCI 与 15 篇 SSCI 实证论文的逐句编码校准。
  - **段落写法**：统计内容包括引言语步、引用方式与密度、讨论要点的构成、句长与套话。中文稿按 27 篇 CSSCI 论文逐段统计；英文稿按 31 篇 SSCI 论文统计，其中 16 篇来自 AERJ、JEP、Computers & Education 等顶刊。
  - **写法检查脚本**：中英文的阈值分别在这两批论文上校准。
  - **验证**：中英文各做过一次改前改后的对照，由独立子任务各写一次同一份稿子，再盲评。

  见 `distill/` 和 `evals/smoke-evaluation.md`。
- **检查脚本**：语气、全文一致性、统计报告、返修回复、标红、审稿报告结构等脚本都用预埋问题的样例测试。
- **试用记录**：各使用场景的试用请求和观察到的结果见 [evals/smoke-evaluation.md](evals/smoke-evaluation.md)，路由测试见 [evals/README.md](evals/README.md)。
- **测试**：在仓库根目录运行 `python -m unittest discover tests`，覆盖安装、各模块的端到端运行、检查脚本，以及红线条款、链接、元数据和中英文说明的一致性。

这些检验范围有限，不等于对所有数据和研究类型都有效；AI 的评阅和模拟审稿是自查，不能替代导师或审稿人。

## 版本

- **0.7.0（2026-10-07）**：改进英文论文的写法。
  - **语料**：英文语料补充 16 篇顶刊论文（AERJ、Journal of Educational Psychology、Learning and Instruction、Computers & Education、Higher Education 等），共 31 篇，并逐段统计写法。
  - **新增英文写法规范**：
    - 引言和综述一半以上的句子带引注，点名作者式引用约十分之一；
    - 综述先综合、再举一两项研究；
    - 讨论要点按"复述发现→对照 2–4 项研究→解释并点名理论"展开；
    - 讨论不用论断式小标题，启示写成段落；
    - 规定了句长、we、被动语态和 AI 常用词的用量。
  - **路线**：重写引言、综述与假设、讨论、结论、结果段的英文部分。
  - **检查脚本**：`check_prose.py` 支持英文，阈值在 31 篇上校准。
  - **盲评**：改后版本五部分赢四个，摘要略逊；评审指出的退步（表述绝对化、为凑引用密度误挂文献等）已写进规则。
- **0.6.0（2026-10-07）**：改进中文论文的写法。新增中文写法规范（论证在段内完成、论断在前引注在后、段末停在证据上、价值句只在引言末句和结语、讨论不重复统计量、不在正文提"还可以做的分析"、句长和套话），按 27 篇 CSSCI 论文重写引言、综述与假设、讨论、结论与建议的写法；新增 `check_prose.py` 按章节对照已发表论文检查写法；用已发表研究写作而用户要投稿时明确提示属于抄袭；盲评中改后版本在五个部分中赢了四个。另含 WorkBuddy 安装、CC BY-NC 4.0 许可和公开发布脚本。
- **0.5.1（2026-10-07）**：用一篇真实中文稿件跑通外审模拟后修正检查脚本：统计报告与一致性检查识别全角的＝＜＞（此前对中文稿基本失效）；小数位比较只比同一统计量；段首"表1列出……"算作正文提及；RQ1、H3、M (SD) 等不再当作缩写定义；读 Word 时保留标题层级，语气检查在声明和参考文献处停止；审稿与回复检查识别"3.7节""声明"等位置写法。
- **0.5.0（2026-10-07）**：新增投稿前外审模拟（edu-review）和返修回复（edu-response，含修改说明、回复信、标红稿）；edu-audit 增加统计报告审查；edu-writing 增加全文一致性检查，以及摘要与标题、研究方法、结论与建议三条写作路线，参考文件改为分节的中文说明；edu-proposal 增加论证地图、证据表、栏目计划和交付前自查；每个 skill 增加中英文说明页、Codex 界面信息和成熟度标签；增加 Claude Code 插件清单；安装器不再被运行脚本产生的缓存文件阻挡；增加红线条款和链接一致性测试。
- **0.4.1（2026-10-07）**：新增课题申报书模块（全国教育科学规划活页按 2026 年模板核对）；中文稿按 GB/T 7714 著录和排版；任意 Markdown 转 Word；扎根理论编码的提交与版本记录脚本；SEM 的 bootstrap 置信区间改用标准化估计、共同方法偏差增加单因子 CFA 和潜在方法因子；中文图表字体；按四个使用场景的试用结果修正。
- **0.4.0（2026-10-07）**：按独立 skill 重构，不再绑定仓库路径，产出写入用户的项目文件夹；同时支持 Claude Code 和 Codex。新增卡方与非参数检验、Logistic 回归、调节与中介、CR/AVE/HTMT、Harman 检验、PLS-SEM、fsQCA、NCA、ICC、扎根理论编码和编码一致性，并配有已知答案测试。写作模块在全文写作前确认一次主线，并使用写作依据表。
- **0.3.2（2026-10-07）**：写作语气按已发表论文校准，新增语气检查脚本。
- 更早的开发记录（13 轮试验、语料与案例）保存在未公开的开发仓库中。

## 许可

采用 [CC BY-NC 4.0](LICENSE)（署名—非商业性使用）：可以自由使用、修改和分享，需注明出处，不得用于商业目的；商业使用请先联系作者。`distill/` 只保存书目信息和统计汇总，不包含论文全文。
