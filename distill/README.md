# 写作立场提炼（2026-10-06 至 10-07）

目的：skill 写出的讨论"防御性"太强，每个发现后面都跟一句"尚不能证明……"。这里从已发表论文中提炼教育学期刊实际的写作立场，用来改写 skill 的语气规则，并用前后对照检验效果。

## 语料

| 组 | 篇数 | 来源 | 清单 |
|---|---|---|---|
| 英文 SSCI | 31 | EN01–EN15：Computers & Education、BJET、ETR&D、IJETHE、Education and Information Technologies、Teaching and Teacher Education、Learning and Instruction、IJME、Music Education Research；2024–2025。EN16–EN31（`tier: top`）：AERJ、Journal of Educational Psychology、Contemporary Educational Psychology、Learning and Instruction、Computers & Education（2）、Internet and Higher Education、Educational Researcher、npj Science of Learning、Higher Education（2）、Studies in Higher Education、BJET、Journal of the Learning Sciences、Psychology of Music（2）；2024–2026。均为合法开放获取版本 | `manifest_en.json` |
| 中文 CSSCI | 27 | 中国电化教育、电化教育研究、开放教育研究、现代远程教育研究、远程教育杂志、中国远程教育、教育研究、华东师大学报（教育科学版）、教师教育研究，各 3 篇；2025–2026；经高校图书馆数据库下载 | `manifest_zh.json` |

全文和逐篇编码只存在本地 `private/`（已在 .gitignore 中），仓库只保存书目信息、脚本和汇总。

## 方法

- `scripts/extract_cnki.py`：把知网单栏或双栏 PDF 提取为带章节标记的文本。
- `scripts/stance_metrics.py`：按 Hyland 元话语类别统计限定词、加强词、局限句、自称和免责句，结果在 `results/stance/`。
- `CODING_SCHEME.md`：逐句人工编码方案（由子任务按方案逐篇完成），汇总在 `results/coding_summary_en.md` 和 `results/coding_summary_zh.md`。

## 主要发现

| 讨论与结论部分 | 已发表 SSCI | 已发表 CSSCI | 旧版 skill |
|---|---|---|---|
| 发现句不加限定 | 86%（中位） | 99% | — |
| 推断免责句（"不能证明/不宜视为"） | 正文 1.2%，9 句 | 正文 0.25%，3 句 | 中文 8%（中位，最高 24%）；英文 6–12% |
| 不确定性放在哪里 | 解释 69% 带限定，发现 16% | 解释 28%，发现 1% | 挂在发现后面 |
| 局限 | 15/15 集中一处，中位 12 句 | 11/27 有，多在末段，中位 3 句 | 散在各段 |
| 自称（we/本研究） | 每千词约 11 | 每千字约 1.5 | 英文为 0 |

结论：已发表论文并不比 skill 更少谨慎，区别在于谨慎放在哪里——动词与设计相符、不确定性放在原因解释上、局限集中写一次并转成后续研究。skill 的旧规则明确要求"把限制放在它所修改的论断旁边"，这是免责句散布全文的直接原因。

## 对 skill 的改动

- 新增 `skills/edu-writing-research/references/voice-zh.md`、`voice-en.md` 和 `scripts/check_voice.py`。
- 改写 `SKILL.md`、`foundation.md`（3 处）、`quantitative-discussion.md`、`full-manuscript.md` 中关于限定位置的规则，并重写 M03 方法卡的示范段落。判断标准（相关不写成因果、不显著不写成等效等）没有删减。

## 改前改后对照

材料：Lechner 等（2024，Frontiers in Education，CC BY 4.0）的引言、理论、方法和结果，原讨论不提供。新旧两版 skill 各自冻结为快照，任务说明逐字相同，中文讨论各写 3 篇、英文各写 1 篇，写作者为同一模型（Claude）。用 `check_voice.py --source materials.md` 测量，并逐项核对新版用到的数字和细节。

| 版本 | 免责句占比 | 局限句在局限段内 | 材料中找不到的数字 |
|---|---|---|---|
| 旧版中文（3 篇） | 4.8%–5.4%（各 2 句） | 0%–50% | 0 |
| 新版中文（3 篇） | 0 | 100% | 0 |
| 旧版英文 | 2.6% | 0% | 0 |
| 新版英文 | 0 | 100% | 0 |

逐篇阅读：新版明确声明贡献，与假设不符的结果用"与预期不同的是……可能的原因在于……"处理，建议编号并给出材料中已有的做法，局限集中一段并转成后续设计；没有发现把相关写成因果、把不显著写成等效或补造细节。旧版内容同样准确，但每段带"尚不能区分""有待检验""不能解读为"一类收尾。

两点说明：一是同样的旧版规则，在 Codex 历史产出中的免责句高达 8%–24%（中文）、6%–12%（英文），本次用 Claude 写只有 3%–5%，说明防御腔有相当部分来自 Codex 所用模型本身，新规则需要在 Codex 中再验证一次；二是每组样本少，结论是方向性的，不是盲评。

## 结构统计（2026-10-07）

在同一批 42 篇论文上测量摘要（长度、语步、发现条数、收尾方式）、标题与关键词、方法部分（小节顺序、信效度位置、共同方法偏差、伦理、软件版本、篇幅占比）和结尾单元（结论、建议、局限的组织方式，每条建议是否回扣具体发现）。汇总和由此得出的写作规则见 `results/sections_summary.md`，逐篇记录在 `private/sections_coding.jsonl`。据此新增 edu-writing 的 `abstract-title.md`、`methods-section.md`、`conclusion-implications.md` 三条路线。Codex 中的语气复测已在 0.4.1 完成（免责句 0%），见 `evals/smoke-evaluation.md`。

## 写法统计（2026-10-07）

在 27 篇 CSSCI 论文上逐段编码引言、综述、讨论、建议的语步与段末收尾，并统计引用方式与密度、句长、套话和自称（`results/writing_moves_zh.md`，逐篇记录在 `private/writing_moves_coding.jsonl`）。据此新增 edu-writing 的 `prose-zh.md`，重写引言、综述、讨论、结论各路线，并写出 `check_prose.py`（阈值在这 27 篇上校准）。

## 英文写法统计（2026-10-07）

**语料**：英文语料补充 16 篇顶刊论文（EN16–EN31）。在 31 篇上逐段编码引言、综述、present study、讨论和结尾单元，共 924 段、120 个讨论要点、632 个结果段开头；引用方式与密度、句长、被动语态、we、套话和 AI 常用词由脚本统计。
- **编码**：七个编码子任务按同一方案编码，每个子任务都分到两组论文，所以编码者差异不会和组别差异重合。
- **信度**：随机抽 45 段盲重编段末收尾，一致率 82%（κ = 0.78）。
- **结果文件**：汇总在 `results/writing_moves_en.md`，逐篇记录在 `private/writing_moves_en_coding.jsonl`。

**两组对照**（原 15 篇与顶刊 16 篇）：
- **一致**：句长、各部分引用密度、讨论要点的构成（复述、对照）、空白类型、研究目的的位置和段末收尾两组一致，bootstrap 区间在中位数 ±15% 以内，31 篇足以支撑这些规则。
- **组间差异**：顶刊长句更少（12% 对 17%），讨论要点更常解释（92% 对 58%）、更常点名理论（41% 对 17%），引言更常写明贡献（13/16 对 6/15）。写作目标按顶刊定。
- **还不够的地方**：偏态指标的上尾阈值（点名作者式引用占比、成组引注、we、缩写、AI 常用词）还不稳定，要 100–150 篇才能定 p90 阈值。按研究设计分开定阈值，每种设计需 15–20 篇；现在只有 8 篇定性、5 篇混合研究。

**对 skill 的改动**：
- 新增 `prose-en.md`；
- 重写引言、综述、讨论、结论和结果段各路线的英文部分；
- `check_prose.py` 增加英文模式，阈值设在 31 篇的极值附近：用脚本检查这 31 篇，除 EN24（数字编号引用在提取时丢失）外，只有 EN07 一篇因 AI 常用词偏多而触发提示。

## 已知局限

- 词表指标只是近似。中文"并非……而是"多为实质判断，所以中文免责句改用严格词表；人工编码结果以 `results/coding_summary_*.md` 为准。
- 中文提取有少量缺失：ZH20 结语、ZH27 总结与展望为空，ZH21 讨论缺第一小节，ZH10–12 摘要不全。表格碎片混入段落，编码时已忽略。
- 中文 27 篇、英文 31 篇，以教育技术、教师教育、教育心理和音乐教育为主。JRME、JCAL 没有拿到合法的开放获取全文。英文写法编码每篇只编一次，罕见编码（泛化收尾句）在用作硬性门槛前需要第二位编码者。
