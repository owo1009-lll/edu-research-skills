---
name: edu-research
description: Plan education research and coordinate multi-step projects - topics, research questions, theoretical frameworks, research and sampling design including sample size, and projects that chain several steps such as analyzing data and then writing the paper. Single tasks (one analysis, qualitative coding, a results or reporting check, a paper, a mock peer review, a response to reviewers or a grant application) go straight to edu-analysis, edu-qual, edu-audit, edu-writing, edu-review, edu-response or edu-proposal. Use for 选题、研究问题、研究设计、研究方案、理论框架、抽样设计、样本量估计、准实验设计、教育研究整体规划、从数据到完整论文.
---

# 教育学科研入口

用户给出材料（主题、问卷数据、访谈、文献、初稿）和一句需求即可。助理判断任务、选择模块、准备内部格式；不要求用户选版本、写配置或整理成 JSON。

## 路由

1. **判断任务，分派模块。**按下表，只读需要的模块。

   | 用户有什么、要什么 | 去哪里 |
   |---|---|
   | 只有主题或问题，要选题、研究问题、理论框架或研究设计 | [研究前期](references/research-preparation.md) |
   | 问卷、量表、实验或成绩数据，要统计分析（差异、回归、中介调节、信效度、SEM、PLS-SEM、fsQCA、NCA、多层与纵向） | edu-analysis |
   | 访谈、观察、开放题，要主题分析、内容分析或扎根理论编码 | edu-qual |
   | 已发表论文或自己稿件里的统计结果，要核对、复算或检查报告是否规范 | edu-audit |
   | 要写或改论文的某一部分、整篇论文、文献综合、讨论，或润色 | edu-writing |
   | 要写课题申报书、活页或开题报告 | edu-proposal |
   | 稿件或申报书写好了，投稿前想知道审稿人会挑什么毛病 | edu-review |
   | 收到审稿意见，要改稿、写修改说明或回复信 | edu-response |
   | 数据和成文都要（"根据这些数据写一篇论文"） | 先 edu-analysis 或 edu-qual，结果确认后再 edu-writing |

2. **确定语言和期刊。**投中文期刊（CSSCI、北大核心）写中文，投 SSCI 写英文；用户没说时按请求语言判断，判断不了问一句。目标期刊明确时，先读该刊近期的作者须知。
3. **确定范围。**只要一段、一个提纲或一章时，就只做这一部分；要完整论文时，按 edu-writing 的流程先确认一次主线，再一次做完。
4. **只在必要时提问。**材料中能找到的就不问；会改变研究判断的缺口（分析单位、分组、计分方向、目标期刊）才问，而且一次问清。

## 共同约定

- 所有产出写在用户当前项目下的 `edu_output/`，原始数据和访谈不上传、不写进 skill 文件夹。
- 统计需要 R（edu-analysis 会自检并提示安装缺少的包）；纯写作只需要 Python，不需要 R。
- 能力范围与限制见 [能力表](references/scope.md)，运行环境见 [环境](references/execution.md)，共同红线见 [共同规则](../edu-shared/references/integrity.md)。
