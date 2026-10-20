# 三类语料的获取与精读

本轮已完成当前范围的提炼与验证，见[交付索引](delivery.md)。2026-10-20 用户明确每类约 50 篇只是举例，可以减少；不设篇数门槛。只有明确的论证任务、来源或评测缺口才定向补读。数量与获取成功均不证明写作质量。方法取舍见[提炼汇总](synthesis-and-decisions.md)；下文按批扩充的段落是历史记录，不代表仍按数量推进。

2026-10-19 用户明确要求从公网寻找。新增来源采用无需登录的出版社全文、大学机构库、作者公开稿和 ERIC 等公开学术文献库；不把搜索摘要当全文，不把用户私稿纳入公开语料。全文缓存保留在仓库外，仓库保存身份、公开来源链接、获取记录、读取定位和原创分析。

同日用户进一步明确：**只要英文文献蒸馏**。此后停止中文材料工作，不再执行原任务中的兼顾中文。历史中文记录保留以反映实际接触，但从本轮语料、候选方法依据和评测选材中排除；不删除原始获取记录或把部分读取改称未接触。

## 分组与接触状态

- 旧文复读：保留原 EN/ZH/E/H 标识。旧留出材料一旦用于这轮开发，就不再是独立留出。理论、方法和综述单列为背景来源。
- 新增开发：先记录候选与具体学习问题，再确认全文身份、研究设计和值得学习的实际写法。只读摘要、下载失败、已获取但未分析各自保留状态。
- 独立留出：正式规则确定、实际加载版本冻结后另选三篇英文材料，见[最终清单](../../evals/writing-final-20261020/sources.json)及[六项任务结果](../../evals/writing-final-20261020/adjudication.md)。下列开发队列没有被改标为留出，也不把新留出加入开发精读数量。

既有英文基础语料有定量 22、质性 15、混合 13 篇。这是历史清单数量，不是本轮新增数，也不能推定每篇的图表、补充文件和句段分析均已完成。历史部分 W 标记缺失完整身份，去重保留这一限制。

## 覆盖缺口

| 组别 | 要扩大比较的对象 | 选文后须确认的写作价值 |
|---|---|---|
| 定量 | 实验、准实验、横断面、纵向；不同团队与教育任务 | 让理论形成可比较预期；解释效应及模式；围绕具体对象、测量和时间比较文献；不显著或反常结果仍推进问题 |
| 质性 | 民族志、案例、主题分析；不同教育场景和知识传统 | 从互动、行动、话语发展解释；引语前后有分析；比较过程与反例；参与者意义和作者判断均清楚 |
| 混合 | 解释型、探索型、汇聚型；不同整合阶段与层级 | 实际连接样本和推理；一类材料改变另一类材料的含义；联合展示产生可说清的整合认识 |

首批英文公网队列偏重高等教育、动机与归属，团队也有交叉。这些是后续应补的缺口，不能从此归纳教育写作的普遍范式。后续扩充均限英文全文，中文分析不再属于本轮工作。

候选身份和来源见 [第一批](public-sources.json)、[第二批](public-wave2.json)、[第三批](public-wave3.json)、[第四批](public-wave4.json)、[第五批（仅英文）](public-wave5.json)、[第六批（仅英文）](public-wave6.json)、[第七批（仅英文）](public-wave7.json)、[第八批（仅英文）](public-wave8.json)、[第九批（仅英文）](public-wave9.json)、[第十批（仅英文）](public-wave10.json)、[第十一批（仅英文）](public-wave11.json)。其中 `selection_question` 是筛选问题，不是已经证实的优秀写法；候选类型也须经全文核读确认。获取状态与完成精读记录分开保存，脚本不得自动将“下载成功”升级为“精读完成”。跨批重试各自只计一篇。

当前实际进度见 [reading-coverage.json](reading-coverage.json)：十五批历史清单合计 71 个不同候选、52 篇取得可读全文；其中本轮有效英文范围为 **67 个候选、49 篇取得可读全文、45 篇完成实证／边界案例分析，另有两篇方法应用分析及一篇筛选反例**。英文全文中 47 篇下载成功，M-N12 通过公开 PDF 阅读工具、L-N18 通过出版社 HTML 阅读工具完整读取并保存定位文本，均未取得原始文件字节；获取数含背景方法文与待确认类型。[M-N12](papers/M-N12.md) 和 [M-N16](papers/M-N16.md) 是带实际研究应用的方法论文章；[M-N22](papers/M-N22.md) 是完成全文分析后单列的筛选反例，均不加入下表的实证范例数。两篇英文旧文复读 Q-R01、M-R01 单列。中文 Q-ZH01 已部分读取第 1–9 页，随后按用户要求停止；L-ZH01、M-ZH01 已获取未精读，X-ZH01 仅筛读首页；四项均退出本轮范围，不计入英文进度。候选与获取记录保留当时状态，后续以实际读取清单的 `scope_status` 及读取范围为准。M-N09 的出版社身份已核对，但其所报 DOI 登记尚未确认；L-N14、M-N21 的 Crossref 请求返回 429，身份另由出版社全文元数据核对，不称所有候选 DOI 均完成登记核验。

| 完成分析的组别 | 新增开发文章 | 此阶段能比较的对象 | 尚缺的覆盖 |
|---|---|---|---|
| 定量 | Q-N01、Q-N02、Q-N03、Q-N05、Q-N07、Q-N08、Q-N10、Q-N11、Q-N12、Q-N13、Q-N15、Q-N16、Q-N17、Q-N18 | 情境适配、比较设计、主要结局、长期推算、纵向参照、理论进入活动、跨层级比较、财政调整、课堂练习、家庭参与条件、学习体验与知识表现的区别，以及结局的教育含义、未获支持预期和实施差异的解释 | 仍需扩大团队与领域覆盖；保留随机试验和观察研究的不同推断范围，不以实践方向明确为由照搬原文全部因果判断 |
| 质性 | L-N02、L-N04、L-N07、L-N08、L-N09、L-N10、L-N11、L-N12、L-N13、L-N14、L-N15、L-N17、L-N18、L-N19、L-N24 | 参与时机、身份、政策协商、话轮中的知识和责任、导师关系、合作评价、反思对象、文档流动、权力与社区关系，以及经验与新角色身份、研究者反思参与式项目的具体安排、学生经验与学校规划之间的追溯、跨文化交往中熟悉知识的重新理解 | 观察互动、回顾档案与文档流动须分别理解；L-N14 规范立场和反例并存，不能统一套用或降调，作者与场景覆盖仍不足 |
| 混合 | M-N01、M-N04、M-N06、M-N07、M-N09、M-N10、M-N13、M-N14、M-N15、M-N17、M-N19、M-N20、M-N21、M-N23、M-N24 | 解释型案例、工具修订、汇聚型功能解释、思想回应、支持需求、类型连接评价、调查检视模型、联合展示中的相反体验，以及访谈和开放回答改变分数与类别的解释；区分资源可得、合作意愿、教师实际需要及参与感与决策权 | 整合层级与不一致仍需更多跨作者证据；联合展示不自动完成解释，感受、预期、描述与关联不当作干预效果 |
| 混合分析边界案例 | L-N01 | 同一访谈的编码比例与叙述，持续就读与归属的非对应 | 不视为独立定量／质性两批资料；不替代上述混合设计覆盖 |
| 方法应用，单列 | M-N12、M-N16 | 实际项目中的联合展示迭代与参与式整合 | 不充抵实证范例数，不把同一项目的不同报告当作独立研究 |
| 筛选反例，单列 | M-N22 | 总体显著性与概念类别对应，不足以解释具体分数变化；局部反思活动描述仍可供修改示例使用 | 不计入优秀混合研究范例，保留原文的概念与统计报告疑点 |
| 旧文复读 | 定量 Q-R01；混合 M-R01 | 与新增来源比较具体解释动作 | 不计新增，更不计独立评测 |

每篇笔记包含正面动作与不采纳的推断。整体语料仍显著不足，这 45 篇用于集中提炼，不以是否达到每类 50 篇验收；方法的适用范围仍需具体依据和实际输出支持。尚无本轮最终版本独立留出评测；阅读次数不代表验证情境数量。来源失败、版本待核对和去重范围见 [筛选说明](source-screening.md)。[组内候选比较](candidate-methods.md) 将具体动作与旧输出、旧规则和适用情境连接，仍不作为正式方法或效果结论。M-N09、Q-N08、L-N11 各用于一次当前版本的英文新写和一次真实段落压缩，共三项开发研究、六项操作；没有重复生成或新规则对照，见[英文开发诊断](../../evals/writing-20261020/README.md)。

## 可复现获取

[Wave 12](public-wave12.json) adds the English collaborative-autoethnography source L-N17. Q-N15 from wave 10 is now also fully analyzed. [M-N20's HTML retry](public-mn20-html-retry.json) is a second acquisition of the same registered article, not a new source; its [English full-text analysis](papers/M-N20.md) is now complete. Details and reproduction commands are in [source screening](source-screening.md#later-reading-and-wave-12).

[Wave 13](public-wave13.json) adds Q-N17, Q-N18, L-N18, M-N22 and M-N23. Four full texts were acquired; Q-N17, Q-N18, M-N22 and M-N23 now have complete analyses within their recorded reading scope, with M-N22 kept as a separate screening counterexample. Q-N17's supplement remains unread. L-N18's original PDF request failed; its later complete publisher-web reading is recorded below. Q-N18 required the [observed replacement repository link](public-qn18-repository-retry.json). M-N12's complete web reading and source-image inspection are documented separately in [its provenance record](reading-mn12-web-assets.json); this is an access upgrade of an existing candidate, not a sixth new source. See [wave-13 screening](source-screening.md#english-wave-13-and-completed-m-n12-reading), [Q-N18 reading](source-screening.md#q-n18-complete-english-reading) and [the mixed-source selection increment](source-screening.md#full-reading-and-selection-of-m-n22-and-m-n23), and [Q-N17 reading](source-screening.md#q-n17-complete-english-main-article-reading).

复用上一轮的公开获取和定位脚本，不在本轮重复建立下载框架。输出目录须新建且位于仓库之外；示例路径为用户自行选择的 `<cache>`。

```powershell
python distill/20261018/fetch_sources.py --manifest distill/20261019/public-sources.json --ids Q-N01 Q-N02 L-N01 L-N02 M-N01 --out <cache>
python distill/20261018/prepare_reading.py --manifest distill/20261019/public-sources.json --cache <cache> --digest distill/20261019/acquisition-public-wave1.json
```

第二批使用 `public-wave2.json`，当时实际获取 ID 为 `Q-N03 L-N04 L-N05 L-N06 M-N04 M-N05 X-N01`；X-ZH01 为历史单独首页筛读。第三、四批历史运行分别读取 `public-wave3.json`、`public-wave4.json` 的全部 ID。**现在复现第四批英文获取时使用 `--ids Q-N05 Q-N06 M-N07 M-N08 Q-N04 L-N05`，不再获取其中中文条目。** 各批使用不同的新缓存目录，保留失败与重试记录。相应摘要文件为 `acquisition-public-wave2.json`、`acquisition-public-wave3.json`、`acquisition-public-wave4.json`。表图链接来自已取得的出版社主文 HTML，实际请求地址及哈希另存各篇资产 JSON；不依赖开发者本机路径即可寻找同一来源。

获取脚本可拒绝只有摘要的落地页；失败记录保留。PDF 另核对页面及栏序，HTML 的链接表格按分析需要单独读取。读取范围只按实际完成记录，不把补充材料的链接当作已读取内容。

第五批使用 `public-wave5.json` 全部九项，缓存另选新目录，再用同一 `prepare_reading.py` 生成 `acquisition-public-wave5.json`。取得七项全文、两项访问失败，获取时完成题名/作者筛核。随后 Q-N07、Q-N08、L-N09、L-N10、L-N11、M-N09、M-N10 均完成主文和适用表图分析；获取摘要保留原状态，实际进度见读取清单。L-N09 的四份补充附件请求失败，不计为已读。

第六批使用 `public-wave6.json` 全部三项。首次记录见 [获取摘要](acquisition-public-wave6.json)：Q-N10 成功，L-N12 遇到 PDF 前导换行解析失败，M-N12 返回 403。修复下载器后以 `--ids L-N12` 和另一新缓存目录重跑，见[重试摘要](acquisition-public-wave6-retry.json)。复现时可直接用当前脚本及同一公开地址，不依赖本机缓存。Q-N10 的 NBER 工作稿与 2021 正式发表版只计一个候选；现已读全部 63 页文字并查看 29 页渲染。封面标 2019 年 8 月修订，正文又引用 2020 年文献，故以实际文件和哈希识别版本，不推定整份内容更新时间。L-N12 完成主文第 1–16 页、全部四表四图及公式分析，另查看 12 页渲染；记录为对照案例，不将其整体认定为优秀范本。M-N12 后来可通过网页工具打开 14 页 PDF，但只筛看开头，未完成全文分析；直接下载重试仍为 403，见[重试记录](acquisition-M-N12-retry.json)。

第七批使用 `public-wave7.json` 六项和新的外部缓存目录，取得全部六篇，见[获取摘要](acquisition-public-wave7.json)。六篇均已完成主文与相关表图分析，M-N13 另读五页附件，M-N15 另核读问卷附录；L-N14 的近期勘误也已读取。PDF、XML、HTML 和附件继续留在仓库外，公开记录提供来源与定位。L-N14 是英文正文，附带法文摘要不另算语料；其 DOI 含 2025 字样，实际出版社标 2026-06-24 在线发表。

第八批使用 `public-wave8.json` 两项和新的外部缓存目录，取得 Q-N12 的 ERIC 作者稿及 Q-N13 的大学实验室公开 PDF，见[获取摘要](acquisition-public-wave8.json)。两篇现均已完成全文及主表图分析，分别实际查看 11 页和五页渲染。Q-N12 在线年份为 2019、卷期为 2020；Q-N13 为 2015 年 OnlineFirst 排版，按实际文件定位。Q-N12 的 OSF 原始材料未读，Q-N13 补充 DOC 未取得，均不把主文分析当作全部附件已核验。另检索到的 Deslauriers 等主动学习论文已作为 E02／T1 使用，未重复登记为新增。

[Wave 14](public-wave14.json) registers six further English qualitative candidates, with [two PDF acquisitions and four failed PDF requests](acquisition-public-wave14.json). L-N19 and L-N24 now have complete analyses within their recorded scope. The existing candidate [L-N18](papers/L-N18.md) is now analyzed as a qualitative reflexive implementation case, with [complete web-text provenance](reading-ln18-web-assets.json); this access upgrade adds no new candidate. Its student-led surveys are embedded activities and do not establish a separately evaluated mixed-methods intervention. Current totals above include this distinction.

[L-N19](papers/L-N19.md) adds institutional ethnography to the completed qualitative set, with [17-page reading and six-page visual provenance](reading-ln19-assets.json). The English paragraph analysis and same-fact edits follow classroom accounts into an organizational provision, while keeping reported experience distinct from evaluated effects. No new source was registered in this reading increment; current candidate and acquisition totals are unchanged.

[L-N24](papers/L-N24.md) adds the classroom environmental-literacy project to the completed qualitative set. [Reading provenance](reading-ln24-assets.json) covers all 25 pages, Table 1, four figures and 14 actual page-image inspections, including correction of page-2 extraction order. The approximate project participation count is not recast as a quantitative strand or an exact interview sample. No new candidate or acquisition is added by this completed analysis.

[第十五批英文来源](public-wave15.json)新增 M-N24；[获取记录](acquisition-public-wave15.json)保留下载时状态。该文现已完成全部 22 页及四表三图分析，十二页实际看图核对，详见[英文笔记](papers/M-N24.md)和[读取定位](reading-mn24-assets.json)。它补充中学课堂管理中的解释型设计：调查刻画学生心目中的有效教师，焦点小组细化责任、秩序与参与的含义。实际整合以连接样本、共同概念和主题解释为主，不将尚未逐项解释的组间差异写成已获解释。当前混合实证分析增至 15 篇；本篇来自开发阅读中已接触的文献线索，不是独立留出。
