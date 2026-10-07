# 写作立场提炼（2026-10-06 至 10-07）

目的：skill 写出的讨论"防御性"太强，每个发现后面都跟一句"尚不能证明……"。这里从已发表论文中提炼教育学期刊实际的写作立场，用来改写 skill 的语气规则，并用前后对照检验效果。

## 语料

| 组 | 篇数 | 来源 | 清单 |
|---|---|---|---|
| 英文 SSCI | 50 | EN01–EN15：Computers & Education、BJET、ETR&D、IJETHE、Education and Information Technologies、Teaching and Teacher Education、Learning and Instruction、IJME、Music Education Research；2024–2025。EN16–EN31（`tier: top`）：AERJ、Journal of Educational Psychology、Contemporary Educational Psychology、Learning and Instruction、Computers & Education（2）、Internet and Higher Education、Educational Researcher、npj Science of Learning、Higher Education（2）、Studies in Higher Education、BJET、Journal of the Learning Sciences、Psychology of Music（2）；2024–2026。EN32–EN50（`tier: top`，2026-10-08 补充）：BJME（2）、Research Studies in Music Education、BERJ、Science Education、Learning, Media and Technology、CBE—LSE（2）、JRST（2）、AEHE、Teaching in Higher Education、Journal of Learning Analytics、Modern Language Journal、TATE（2）、Sociology of Education、AERA Open、Journal of Teacher Education。均为合法开放获取版本 | `manifest_en.json` |
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

## 英文写法统计（2026-10-07 至 10-08）

**31 篇（0.7.0）**：英文语料补充 16 篇顶刊论文（EN16–EN31），逐段编码引言、综述、present study、讨论和结尾单元，引用方式与密度、句长、被动语态、we、套话和 AI 常用词由脚本统计。两组（原 15 篇、顶刊 16 篇）的中位数一致，但偏态指标的上尾和按研究设计的差异看不清，当时只有 8 篇定性、5 篇混合研究。

**50 篇（0.8.0）**：再补 19 篇顶刊（EN32–EN50，以定性和混合研究为主，含 BERJ、Science Education、JRST、CBE—LSE、AERA Open、Sociology of Education、Journal of Teacher Education、British Journal of Music Education 等）。语料现为定量 22 篇、定性 15 篇、混合 13 篇；顶刊 35 篇，其余 15 篇。
- **编码**：六个编码子任务按同一方案编码新增论文，每个子任务分到不同设计的论文和一篇已编过的锚定论文。锚定论文前后两次编码 κ = 0.90–0.98，没有编码漂移。
- **信度**：另一位编码者盲重编随机 10 篇的 278 个段末收尾，一致率 95.3%，κ = 0.95；泛化收尾句这一罕见编码 κ = 0.91。编码者都是同一模型，按同一方案编码，所以这些 κ 可能高估人与人之间的一致；第一轮人工抽查的 κ 为 0.78。
- **稳定性**：
  - 中位数和 p90 都稳定（bootstrap 区间在 ±15% 以内）：句长、段长、引言和综述的引用密度与带引注句比例、被动语态、缩写。
  - 只有中位数稳定、上尾仍不稳定的：长句比例、讨论引用密度、we、点名作者式引用、成组引注、AI 常用词。这些的报警线仍设在已发表论文的最大值附近，要把区间再缩一半需约 200 篇。
- **组间差异**：31 篇时看到的长句、we 的组间差异，到 50 篇已不成立。顶刊讨论更常解释发现、更常点名理论，这一差异在三种设计中都成立。
- **设计差异**（写进 `prose-en.md` 第 7 节）：
  - 研究问题与假设：定量研究几乎都写假设（19/22），定性研究不写，用编号研究问题（11/15）。
  - 结果段开头：定量以分析步骤或发现开头，定性以主题论断开头（62%）。
  - 讨论中点名作者式引用：定量中位 2.5%，定性 33%。
  - 相反证据：定量综述几乎都写（21/22），定性 8/15。
  - 局限：定量中位 5 条，定性 2 条。
- **检验**：用按 31 篇定的阈值去查新增 19 篇，有 9 篇触发提示，说明上尾阈值确实不稳。`check_prose.py` 已按 50 篇重定阈值：
  - 讨论中点名作者式引用的提示只用于写了假设的稿件；
  - 修正了题目含"methods"时整篇被识别成方法部分的问题，章节识别与人工标记的一致率为 94%；
  - 除 EN24（数字编号引用在提取时丢失）外，已发表论文都不再触发提示。
- **结果文件**：汇总在 `results/writing_moves_en.md`，第 7 节列出与 31 篇版本相比的全部变化；逐篇记录在 `private/writing_moves_en_coding.jsonl`。

## 已知局限

- 词表指标只是近似。中文"并非……而是"多为实质判断，所以中文免责句改用严格词表；人工编码结果以 `results/coding_summary_*.md` 为准。
- 中文提取有少量缺失：ZH20 结语、ZH27 总结与展望为空，ZH21 讨论缺第一小节，ZH10–12 摘要不全。表格碎片混入段落，编码时已忽略。
- 中文 27 篇、英文 50 篇，以教育技术、教师教育、教育心理、科学教育和音乐教育为主。JRME、JCAL、EEPA 没有拿到合法的开放获取全文；EN48 的引言开头在提取时缺失，不计入引言相关的统计。
