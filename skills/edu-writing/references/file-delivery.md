# 文件交付

## 环境

- 在用户的项目文件夹里工作；首稿、评阅和交付文件放在 `edu_output/writing/<新任务文件夹>/`。
- 纯写作不需要统计环境，也不需要 R。
- Word 和图需要 Python 的 python-docx 和 matplotlib（本 skill 的 `requirements.txt`）；缺少时先问用户，再运行 `python -m pip install -r <本skill>/requirements.txt`。
- 脚本路径相对于本 skill 所在文件夹（也可用绝对路径）。

## 选哪个工具

| 交付什么 | 用什么 |
|---|---|
| 新写的完整论文，引用已核验 | `manuscript_package.py`（下文） |
| 已有作者原稿的修改 | 在用户 Word 的新副本上改，或保留原稿实际提纲另行导出；不把原稿塞进打包流程的提纲 |
| 一部分正文、结果、报告、编码表、申报书 | `md_to_docx.py --input x.md --output x.docx [--lang zh] [--superscript-citations]` |
| 图 | `make_figures.py`，见 [图表](figures-and-tables.md) |

修改原稿时，必要的原始文献仍待查的，按 [引用核验](reference-verification.md) 处理：保留有限定的论证和引文，另附外部来源记录，用普通 Word 修订交付，不为了通过核验关卡而谎报已核验。原稿的表格和有依据的图尽量保留，替换的要说明。下面的渲染、数值、引用和版面检查同样适用。

## 完整论文打包

**1. 准备内部的稿件 JSON**（助理整理，不是让用户填的表）：

- 顶层：`scope=full_paper`、`research_type`（quantitative / qualitative / mixed / theoretical / narrative_review）、`title`、`abstract`、`keywords`、`reference_ids`、`pending`，可选 `disclosure`（二次写作说明）、`language`（`zh` 为中文稿）、`citation_style`。
- `sections=[{heading, role, blocks}]`。实证论文的 role：introduction、methods、results、discussion、conclusion；理论或综述用 introduction、conclusion 和相应的论证章节。
- 每个 block 有唯一 `id` 和类型：
  - `paragraph`：`text`；
  - `table`：`title`、`columns`、`rows`、`note`，可选 `abbreviations`；
  - `figure`：`title`、`caption`、`spec`，可选 `abbreviations`。
- 正文引用写 `[@id]`，提到图表写 `{{figure:id}}`、`{{table:id}}`。

**2. 核验引用，再打包**：

```powershell
python -X utf8 <本skill>/scripts/verify_references.py --ledger <ledger.json> --output <新的核验文件夹>
python -X utf8 <本skill>/scripts/manuscript_package.py --manuscript <final.json> --verification <verified.json> --output <新的交付文件夹>
```

打包脚本拒绝：未核验的文献、未完成的支撑记录、不完整的实证章节、正文没有提到的图表。它不补全缺失事实，也不证明内容正确。用户要 Markdown 时加 `--format markdown`；其他格式需要真实可用的导出工具，不能只改扩展名。不覆盖用户文件和已保存的首稿。

**3. 输出**：manuscript.docx 和可读的 manuscript.md；editable_tables.docx 和 CSV；图（可编辑 SVG、PDF、PNG，以及精确的输入 spec 和数据）；code/；citation_check.csv；PENDING.md；输入与核验快照；带哈希的 package_receipt.json。

## 渲染检查

ZIP/OOXML 生成成功不等于版面没问题。用实际可用的 Word 或 LibreOffice 打开或渲染，检查分页、表格断行、图是否清晰、图题位置和参考文献位置。本 skill 的 `scripts/render_word.ps1` 在后台调用本机 Word 导出一份新 PDF，不改动 docx。没有渲染工具时，如实说明哪些视觉检查没做，不声称通过。

## 终审与回复

- 终审时用 `check_consistency.py` 比对摘要、结果、图表和结论中的关键数值与术语，再读渲染后的页面，修正重叠、截断、过小的字、孤立的标题或图题、别扭的分页。
- 默认回复给出终稿 Word 和必要的简短说明，可编辑文件包和引用核查表放在同一文件夹；首稿、评阅和来源细节留在任务记录里。

## 中文期刊与 GB/T 7714

- 稿件 JSON 设 `"language": "zh"`：使用摘要、关键词、参考文献，图表编号为表1、图1，正文宋体、标题黑体，表格为三线表，引用按 GB/T 7714-2015 顺序编码制——按首次引用编号，相邻引用合并（[1,2]、[3-5]），上标显示。
- `"citation_style": "apa"` 或 `--style apa|gbt7714` 可以覆盖默认。
- 文献元数据可带 `type`（J 期刊、M 图书、D 学位论文、C 会议论文、R 报告、EB/OL 网络文献）；图书和学位论文还需要 `publisher`、`place`，网络文献需要 `published`、`accessed`、`url`。
- 投稿前核对目标期刊的作者须知（有的刊要求中文文献附英文译名，有的用著者-出版年制或脚注），按要求调整。
