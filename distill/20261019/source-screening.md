# 公网筛选、分类与读取边界

这是开发进度记录，不是优质论文排行，也不是最终语料交付。八个清单登记的是待核查候选，题目匹配、可下载、完成读取和可采用的写法分别判断。

2026-10-19 用户将本轮范围明确为**英文文献蒸馏**，取代原先兼顾中文的要求。后续只获取、分析和测试英文材料。中文条目保留为历史接触记录，均不纳入有效英文语料或后续方法依据。

## 身份与旧材料接触

[prior-exposure-check.json](prior-exposure-check.json) 对六批去重后的 39 个候选，在本轮目录以外、git 已跟踪的 `distill`、`evals` Markdown／JSON 中按所报 DOI 和完整题名作不区分大小写的字面搜索，均未命中；Q-N10 另查正式发表版 DOI，也未命中。跨批来源重试按同一来源合并；M-N09 的 DOI 登记待核实，不把字面搜索当作 DOI 有效性验证。检索另发现 Lareau 的 *Invisible Inequality* 和中文《我国中小学教师负担生成机制的质性研究》已分别作为 E10、E18 读过，不登记为新增；若深化只能算复读，中文已不在本轮范围。旧 W 标记存在身份不全，题名标点变体也可能漏检，因此不声称穷尽历史去重。

既有论文引用过某个新候选，不自动等于此前完整阅读。例如 M-R01 引用 L-N01；本次才读取后者的实际正文与七幅图。研究系列或共享样本也不能只靠 DOI 区分独立研究，后续评测选材须另核对研究关系。

第七批六篇另按相同范围核对 DOI 与完整题名，均未命中，记录已追加；本轮历史候选合计 45，其中英文 41。搜索又找到已登记为 X-N01 的联合展示方法论文，未重复新增。六篇全文均通过正常公开 PDF、出版社 HTML 或 Europe PMC XML 取得；PMC 网页验证码未绕过。L-N14 的 Crossref 请求返回 429，另由出版社全文元数据核对作者、题名、DOI、语言及 2026-06-24 在线日期，保留原失败记录。

第八批另登记两篇英文定量候选，按相同范围搜索 DOI 和完整题名均未命中；两篇的作者、题名和版本均核对，分别通过 ERIC、大学实验室网页取得全文。历史候选累计 47，其中英文 43。检索到的 Deslauriers 主动学习论文已在 E02／T1 使用，不重复登记。搜索结果中的引用命中与实际已读来源分开判断，不因某文曾被引用就自动判定已精读。

## 实际分类与获取情况

| ID | 当前情况 | 使用与计数 |
|---|---|---|
| Q-N01、Q-N02 | 主文及主图表完成分析 | 两篇新增定量；Q-N02 扩展数据图表只读 XML 中相应说明，未打开图像／补充 PDF |
| L-N02、L-N04 | 主文及适用图表完成分析 | 两篇新增质性，局部限用，不能整篇当范本 |
| M-N01、M-N04、M-N06 | 主文及相关表图完成分析；M-N04 另读问卷补充 DOCX | 三篇新增混合，分别提供不同整合动作；实质错误与疑点保留 |
| L-N01 | 主文、表 1、图 1–7 完成分析；全文 Methods 明确 mixed-methods analysis | 改归同源访谈数据转换的混合分析边界案例，稳定 ID 不变，不计纯质性 |
| Q-N03 | 作者公开 PDF 主文第 1–34 页、主表 1–6、主图 1–8 已完成分析 | 新增定量，区分跨班与教师流动设计；具体修订日期未确认，附录未精读，定位使用实际 PDF 页码 |
| Q-N04 | 大学机构库标注正式 PDF，本环境请求 403 | 没有取得本地全文，未精读；搜索结果可见正文片段不算全文完成 |
| L-N07、L-N08 | 主文、表图与双栏核读完成 | 两篇新增质性；L-N08 是团队参与项目材料的跨案例分析，带明确规范立场，不算仅有理论综述；图中文字／英文译文已读，未观看原视频 |
| L-N05、L-N06、M-N05 | 已试公开 XML／PDF 未成功 | 保留失败原因，不用摘要顶替全文；仍可查找其他合法公开版本 |
| L-N03、M-N03 | 尚无已确认可取得的公开全文 | 不计取得或读取；作者主页链接与 DOI 元数据只提供检索线索 |
| M-N02 | 出版社仅确认公开摘要／引言可见 | 未确认全文，不计全文蒸馏 |
| X-N01 | 方法论文公开 HTML 已取得，尚未精读 | 方法背景；不凑入混合实证篇数，可沿其引用寻找原研究 |
| X-ZH01 | 公开中文 PDF 只筛读首页，确认为文献计量／研究范式回顾 | 已退出本轮范围，保留历史接触记录 |
| Q-N05 | 英文主文、表 1–7、图 1 完成分析；另核 PDF 表 4、5、7 页面 | 定量纵向二次分析，带方法论讨论；补充语法未读未运行，表格和模型对应疑点保留 |
| M-N07 | 英文主文及注释、表 1–6、补充观察量表完成分析 | 解释型混合；观察评分选对照案例，访谈解释评价标准与责任，自报/观察差异保留 |
| Q-ZH01、L-ZH01、M-ZH01 | 出版社公开中文 PDF 已取得；Q-ZH01 已部分读取第 1–9 页，尚未查看渲染页 | 已停止并退出本轮范围；其余两篇未精读，均不形成本轮方法或例子 |
| Q-N06、M-N08 | 大学库请求证书链验证失败、出版社请求 403 | 未取得本地全文；Q-N06 仍可寻找正常验证证书的访问方式，M-N08 尚未确认公开全文 |
| Q-N07 | 教师工作干预英文主文、附录、表 1–4、图 1–7 完成分析 | 限用理论落到活动和比较的写法；多处样本及统计报告疑点，不作数值结论范本 |
| Q-N08 | 英文主文、三图、三条显示公式及补充 A–C 的 14 表完成分析 | 限用比较层级与理论预期的解释；D–I 未精读，报告疑点保留，不把弱关系改写为无关系 |
| L-N09 | 英文主文第 1–11 页、三表完成分析；实际核看九页 PDF | 质性伙伴关系研究；四份补充附件请求 403，未读；不由会议中的提议推定实施成效 |
| L-N11 | 英文主文、四表及访谈提纲完成分析 | 相关社会政策访谈；比较同一合作的不同价值，不能拼成配对伙伴的实际互动过程 |
| L-N10 | 合作双方自我反思的英文叙事民族志主文完成分析；另看八页 PDF 核对双栏与引语 | 质性研究，原项目做过调查／聚类不等于本文就是混合设计；保留成员分歧与资助张力 |
| M-N09 | 英文主文第 1–21 页、七表及设计图完成分析；实际核看九页 PDF | 解释型混合；统计单位和表头疑点保留；出版社身份一致但所报 DOI 登记仍待确认 |
| M-N10 | 学校预防课程实施英文主文、表 1–3、图 1–3 完成分析 | 汇聚型构念层面整合；总体肯定与特定支持需求并存，保留交付量测量范围及样本／报告疑点 |
| Q-N09、M-N11 | Europe PMC XML 请求 500、出版社 PDF 请求 403 | 未取得本地全文；M-N11 与 X-N01 方法背景属于同一研究系列，不当作独立项目 |
| Q-N10 | 公开 NBER PDF 全部 63 页文字、主文和附录表图完成分析，29 页渲染已查看 | 工作稿，不称为 2021 正式版；封面修订日期与正文引用时间有差异，以文件哈希识别；限用论证动作 |
| L-N12 | 主文第 1–16 页、四表四图及公式完成分析，12 页渲染已查看 | 初次前导 CRLF 解析问题已修复；反例重新归类等问题保留，属于限用和对照案例 |
| M-N12 | 网页工具可打开 14 页 PDF，当前仅筛读开头；直接公开下载重试仍 403 | 无本地完整全文，不计取得或完成分析；实证与方法示例的分类仍待全文核实 |
| Q-N11 | 全部 41 页文字、两图、五主表及两附表完成分析，另查看 13 页渲染 | 定量主导的多地随机评价，保留嵌入质性工作的作用；工作稿报告疑点单列，不在混合组重复计数 |
| L-N13 | 全部主文、参考表、一表两图完成分析，另查看九页渲染 | 质性民族志；跟随互动和文档解释概念，不把工作压力转成已测倦怠 |
| M-N14 | B001–B151 主文、五表单元格和行列关系、两幅图完成分析 | 探索型混合；保留概念立场与未决条件关系，调查未与观察教师逐一对应；引用原作未读 |
| L-N14 | 英文主文、参考表、身份声明、出版社表 1及近期勘误完成读取和分析 | 质性对话档案再分析；四位男性、三校；保留规范立场、反例及案例对应疑点，不把法文摘要另计为语料 |
| M-N15 | B001–B051 主文、七表及全部 24 道问卷题完成分析；十页 PDF 渲染已查看 | 探索型混合；学习价值与互动体验区分，条件比较和报告疑点保留；原始日语资料未读 |
| M-N13 | 全部主文、三表一图及五页附件完成分析，另查看附件第 3–5 页渲染 | 探索型混合；按访谈类型连接课程评价，保留尺度、因果表述及报告疑点 |
| Q-N12 | 39 页 ERIC 作者稿文字、七表、两图及所附问卷完成分析，11 页渲染已查看 | 课堂集群随机试验；实际比较和实施条件保留；OSF 原始材料未读，题型顺序等报告疑点单列 |
| Q-N13 | 九页 OnlineFirst PDF 文字、一表两图完成分析，五页渲染已查看 | 两时点观察研究；保留条件问题及支持家长的立场；补充 DOC 未取得，区间和因果表述不照搬 |

历史获取运行有 34 篇不同候选取得可读全文。按当前英文范围过滤后为 **43 个新增候选、31 篇已获取、30 篇完成写作分析**，不等于三类合格范本数。Q-R01／M-R01 两篇英文旧文复读单列；四项中文接触记录不计入上述英文进度。没有最终版本独立留出测试；M-N09、Q-N08、L-N11 各两项当前版本任务，共三项开发研究、六项操作，均不是新增独立留出。

## 来源及版本检查

获取不要求用户私稿、机构登录或授权访问。来源包括出版社、大学机构库、作者网站和 ERIC 公共学术文献库。遇到访问失败保留状态，继续寻找其他公开版本，不绕过登录或验证码。

- Q-N02 的 PMC 页面出现验证页面，未继续尝试绕过；改用可公开读取的出版社页面寻找实际图像地址。早先猜测的八个 JPG 地址返回 404，失败记录保留；最终读取来自页面的两张 PNG。
- M-N04 和 M-N06 的主文链接表格不能由正文抽取替代，已另外请求并读取表格及脚注。图像也实际打开，不以图注代替图形读取。
- Q-N03 已核对首页、作者及主图表，但版本修订日期仍不确定；L-N07、L-N08 已按页面核对双栏与图表。L-N08 若只读文本抽取会漏掉图中的互动话轮，已补读其英文译文。所有范围分别写入笔记，不以下载成功代替这些工作。
- 第四批 Q-N04 的出版社重试仍为 403；L-N05 的 PMC PDF 地址返回 HTML 页面，抽取器拒绝把它当作全文。失败保留，未绕过验证或关闭证书检查。中文 PDF 地址来自期刊页面的 `citation_pdf_url` 元数据。
- Q-N05 表 4、7 是图片，已补读并核对 PDF；表 5 行对应问题在 PDF 也存在，不归咎于抽取。M-N07 的观察量表补充文件已读；Q-N05 补充语法仅下载未读未运行。两篇分析依据各自实际范围。
- 第五批七项取得全文，均用出版社元数据、PDF 首页或 JATS 前置信息核对题名/作者；获取时未读完正文。随后完成 Q-N07、Q-N08、L-N09、L-N10、L-N11、M-N09、M-N10 的主文及适用表图分析。M-N09 还核对出版社公开记录，但 DOI 注册不能由页面印字代替。Q-N09、M-N11 的失败保留，没有绕过验证。
- Q-N07 的四张表与七幅图另行取得并核读；M-N10 的三张表按 XML 行列核对，三幅图从公开 XML 所列图像资产取得并查看。M-N10 的 PMC 页面出现验证码，未尝试绕过；使用已经正常提供的公开 Europe PMC XML。两篇均未读取原始数据或另行复算统计。
- L-N10 读取 PDF 全部文本，主文到第 10 页；查看第 1、4–10 页，核对数据简报段的跨页衔接及引语的实际归属。未看第 2、3、11 页图像，未读原始记录或被引来源；不把阅读参考文献列表计为阅读那些原文。
- Q-N08 另取得并实际查看三图，补充 DOCX 仅 A–C 的文字、14 表与表注已读，D–I 未精读；L-N11 四表和完整访谈提纲均已读。实际范围与原始资产哈希分别保存在读取清单和两份资产 JSON；资产里的未读状态保留获取时点，不覆盖后续记录。
- 第六批的 Q-N10、L-N12 已按 PDF 前置信息核对，后者的两个前导换行曾使旧解析器误判为 HTML。修复只允许文件头前的空白，仍由 PDF 解析器验证内容，保留原始字节和哈希；不凭 MIME 类型接收摘要页或损坏文件。M-N12 的公开网页片段没有替代完整读取。另查 Hall 与 Townsend 的关键事件论文，仅找到摘要、请求全文页及机构登录指南，尚不纳入已获取队列。
- 文章所回顾的其他研究只标“原作者回顾”，除非另有完整读取记录。不能凭一篇论文的引言声称独立比较了其全部引用。

## 保持的缺口

每类约 50–100 篇是本轮首批规模参考，尚未达到，也没有用下载数量替代精读。当前英文队列中高等教育和动机主题偏多；新的学校组织、教师增值、社区、纵向与合作学习案例只改善部分覆盖。下一阶段继续扩充不同团队、主题与期刊的英文全文；不再推进中文实证全文。

本次新增笔记不改变运行规则。只有先完成组内比较、形成具体候选动作、用相同事实条件比较真实写作输出，再冻结最终实际加载版本作新材料复核，才能报告写作效果改善。文章里的同事实例子目前只是开发示范。

## 本批开发记录核验

上一批解析 16 个 JSON 文件，核对 Markdown 相对链接、分析文件与五篇新增文本 SHA-256，汇总新增分析 8 篇、复读 2 篇，检查通过。本批新增三篇分析、第四批获取记录和组内候选比较后，另按最终实际文件核验；运行结果记录在本节后续段落，不沿用旧检查作为新文件已通过的依据。

此前 `9a1be28` 批次实际解析 18 个 JSON 文件；本目录 Markdown 相对链接与清单中的分析文件均存在；Q-N03、L-N07、L-N08 的本地读取文本、清单与笔记所记 SHA-256 一致。当时汇总为 27 个新增候选、17 篇已取得全文、11 篇新增分析、2 篇复读。新增分析分为定量 3、质性 4、混合 3，另有同源转换边界案例 1；未重复计入跨批重试。差异空白检查通过。以上是历史记录完整性核验，不是新写作方法效果评测。

此前上述批次只新增或修改 `distill/20261019`，没有变更运行代码，因此没有重复执行 PPT、统计或审稿功能测试，也没有把来源完整性检查称为写作质量验证。后续若改动开发工具，单独记录其验证，不沿用这一句说明所有批次。

2026-10-20 本批实际检查：22 个 JSON 均可解析；本目录 Markdown 相对链接与清单中的分析文件均存在；Q-N05、M-N07 的读取文本、清单及笔记哈希一致，第五批七个读取文件也与获取摘要哈希一致。当前英文新增候选 32、取得全文 21、完成分析 13；另有两篇英文复读，四项中文记录排除。新分析分组为定量 4、质性 4、混合 4，另有同源转换边界案例 1。差异空白检查通过；尚无本轮新方法的行为效果结论。

2026-10-20 后续三篇分析检查：24 个 JSON 均可解析，Markdown 相对链接及分析文件路径均存在；Q-N07、L-N10、M-N10 的实际读取文本、清单和笔记 SHA-256 一致，新增 14 个表图资产的缓存与公开获取记录哈希一致。汇总为英文新增候选 32、已获取 21、完成分析 16（定量 5、质性 5、混合 5、同源转换边界案例 1），另有英文复读 2；四项中文记录继续排除。实际查看 Q-N07 的七幅图、M-N10 的三幅图、L-N10 的八页 PDF。此次只修改开发目录，差异空白检查通过；未新增运行规则，也未以文献分析和记录核验替代写作效果测试。

2026-10-20 再补两篇分析及第六批来源后，实际解析 29 个 JSON，核对全部相对 Markdown 链接、分析路径及笔记所记文本哈希；Q-N08、L-N11 的两个读取文件及九项资产 SHA-256 与缓存一致，新获取 Q-N10、L-N12 的 PDF 和读取文件哈希均一致。英文新增候选 35、已获取 23、完成分析 18（定量 6、质性 6、混合 5、同源转换边界案例 1），另有英文复读 2；与提交 `ede7142` 对照，四项中文读取记录完全未变。

本批还修复[开发下载器](../20261018/fetch_sources.py)对 PDF 前导换行的识别。`python -X utf8 -m unittest discover -s tests -p test_distill_sources.py -v` 实际通过三个[回归用例](../../tests/test_distill_sources.py)：普通与带换行 PDF 产生相同文本、伪装成 PDF MIME 的摘要页仍被拒绝、只有文件标记的损坏 PDF 仍被拒绝。修复后对 L-N12 原公开地址重新获取成功，原始 732053 字节保留并记录哈希。差异空白检查通过；没有改动运行中的写作方法、PPT、统计或期刊检索，也未重复执行这些模块的无关测试。上述来源与解析核验均不代表最终写作效果已经验证。

2026-10-20 后续完成 L-N09、M-N09 后，实际解析本目录 30 个 JSON，核对相对链接、全部分析路径和所记读取哈希；两篇新笔记的读取哈希与外部缓存一致。新增英文分析为 20 篇（定量 6、质性 7、混合 6、同源转换边界案例 1）；候选 35、已获取 23、英文复读 2。与 `b89d3c5` 对照，四项历史中文读取记录完全未变。L-N09 的四份附件均为失败记录，未增加读取范围；两篇各九页实际渲染的查看范围已记入笔记。

同批公开了 M-N09 的两个英文当前版本任务及独立评阅。发布前核对 203 个冻结文件、四个任务输入、17 项声明加载记录、六项评阅输入哈希和两份匿名稿对应关系；26 个实际运行产物保留原始与发布哈希。完整结果见[开发诊断](../../evals/writing-20261020/README.md)及[记录核验](../../evals/writing-20261020/record-verification.json)。新写脚本检查的是初稿，终稿另做长度核对及独立评阅；压缩任务检查的是终稿。两项任务只涉及同一研究，没有新规则对照或独立留出效果结论。本批只更新开发分析与评测材料，没有改动运行功能。

2026-10-20 随后完成 L-N12 主文、四表四图及公式分析，另实际查看 12 页渲染。它含有可学习的案例比较，也含把异议重新归为收益和多处报告不一致，记录为限用及对照案例。英文新增分析累计 21 篇（定量 6、质性 8、混合 6、同源转换边界案例 1）；获取仍为 23 篇，候选仍为 35 项。Q-N08 的 D–I 补充表仅增加表头和前三行筛看，不称完成分析。与 `6caa407` 对照，四项历史中文读取记录未变。

同批公开 Q-N08、L-N11 的四个英文新写／压缩任务、两份独立评阅及全部实际过程文件。发布核对 203 个冻结文件、八个输入、30 项声明加载记录、12 项评阅输入哈希及四份匿名稿对应关系；64 个产物保留原始与发布哈希，其中 51 个字节不变、13 个仅替换本机路径。此前 26 个产物及四个输入也复核无改动。完整范围见[第二批记录核验](../../evals/writing-20261020/record-verification-02.json)。语料目录 30 个、评测目录另 30 个 JSON（不含新核验报告自身）均成功解析，Markdown 相对链接及读取哈希一致。这些检查证明记录相符，不证明写作质量提高。未改运行规则，未重复 PPT、统计或期刊检索的无关测试。

2026-10-20 再完成 Q-N10 与 M-N13，并取得第七批六篇英文全文。实际解析本目录 35 个 JSON（不含本次核验报告自身），核对全部相对 Markdown 链接、25 份新增或复读笔记所记哈希，以及第七批六份原文件、抽取文本和读取文本的缓存哈希。Q-N10 原 PDF、读取文本和 29 页预览，M-N13 四张图表、五页附件 PDF 及三页预览均与记录一致，见[本批记录核验](record-verification-07.json)。英文新增候选 41、取得全文 29、完成分析 23（定量 7、质性 8、混合 7、同源转换边界案例 1），英文复读 2；与 `c81ea00` 对照，四项历史中文记录完全未变。

2026-10-20 随后完成 Q-N11、L-N13、M-N14 的英文全文分析及英文同事实改写。实际解析 39 个 JSON（不含本次报告自身），核对相对 Markdown 链接、28 份新增或复读笔记所记读取哈希；三篇原文件、抽取文本、读取文本，以及 Q-N11 的 13 页预览、L-N13 的九页预览、M-N14 的两张图和五份表格片段均与缓存一致，见[本批记录核验](record-verification-08.json)。图像均已实际查看，M-N14 表格按 XML 单元格及行列读取。Q-N11 图 1基线标签合计 104.41%，只核算印刷数字并保留疑点，未替作者更正或重跑模型。英文新增分析为 26 篇（定量 8、质性 9、混合 8、边界案例 1）；候选 41、取得全文 29、英文复读 2。与 `abc6e88` 对照，四项历史中文记录及其余所有读取条目均未变。变更仅在开发目录，未修改运行规则；新编英文例子不算模型行为测试或最终独立留出结果。

2026-10-20 随后完成 L-N14、M-N15，并取得第八批两篇英文定量全文。实际解析 44 个 JSON（不含本次报告自身），核对本目录相对 Markdown 链接、30 份新增或复读笔记所记读取哈希，以及四篇原文件、抽取文本、读取文本的哈希。L-N14 的出版社表格与近期勘误、M-N15 的出版社 PDF 及十页实际查看的预览均与缓存一致；HTML 获取失败和渲染结构树警告保留，见[本批记录核验](record-verification-09.json)。英文新增分析累计 28 篇（定量 8、质性 10、混合 9、边界案例 1），候选 43、取得全文 31，另有英文复读 2；Q-N12、Q-N13 尚未完成全文分析。与 `7033cb3` 对照，四项历史中文记录及另外 41 项旧读取条目均未变。

2026-10-20 随后完成 Q-N12、Q-N13 的英文主文、表图及同事实改写分析。实际解析 47 个 JSON（不含本次报告自身），核对相对 Markdown 链接、32 份新增或复读笔记所记哈希；两篇原文件、抽取文本、读取文本，以及 11 页和五页实际查看的渲染均与缓存一致。Q-N13 补充 DOC 的 403 响应留存并核对哈希，未误计为已取得附件，见[本批记录核验](record-verification-10.json)。英文新增分析累计 30 篇（定量 10、质性 10、混合 9、边界案例 1），候选 43、取得全文 31、英文复读 2。与 `0b6b220` 对照，四项历史中文记录及另外 43 项读取条目均未变。

本批只更新 `distill/20261019` 的英文来源、原创分析和进度记录。没有新运行规则、行为比较或独立留出结果，未重复运行 PPT、统计、审稿或期刊检索测试。表图核读和文件一致性检查用于保证分析记录可追溯，不当作写作能力改善的证明。

## 第九批：英文复现研究、教师身份与转化型混合方法

登记前三个 DOI 在现有 `distill` 和 `evals` 中均未检出；它们是新增开发候选，不是留出材料。检索时另发现的联合展示理论化论文和混合 EdTech 方法论文分别已是 M-N05、X-N01，未重复登记。Frontline Learning Research 的教师身份候选只筛看了落地页，下载链接失败，尚未列为已获取或已分析。

[第九批清单](public-wave9.json)中，L-N15 从出版社取得 HTML 全文，M-N16 从大学机构库取得开放 PDF；Q-N14 的 Europe PMC XML 请求返回 500。Q-N14 已核对 PMC 身份和开头，但浏览器可见正文不等于完成全文精读。L-N15 也仍处于身份和开头筛看阶段。

[M-N16](papers/M-N16.md) 已读全部 11 页文字、表 1、图 1，并实际查看七页渲染。其真实研究应用涵盖取样、解释和参与式建议，但本文主要承担方法论说明，分项估计与参与者材料较少。因此单列为“方法应用与对照来源”，不把它加入实证范例数量。保留局部正面动作及英文同事实改写，不采纳广泛的方法优越性断言，也不把共同制定建议写成已经改善辍学。

当前英文候选 46、取得全文 33，完成实证／边界案例分析 30，另有方法应用分析 1、英文复读 2。没有新增中文材料工作；历史中文记录保持原状。

发布前已核对两篇新取得原文件及抽取文本、七页实际查看的渲染、33 份分析笔记中的读取哈希；与 `cec4bc7` 相比，全部 49 项旧读取记录（含四项历史中文记录）未变，见[第九批核验](record-verification-11.json)。同批 [Q-C01 英文对照的核验](../../evals/writing-20261020-qc01/record-verification.json)确认两套各 203 文件快照、四项冻结输入、八份匿名稿对应、13 项评阅输入哈希及 221 个实际产物；其中 60 个过程文件只替换本机实验根路径，其余 161 个字节不变。正式运行规则未改变，候选不因局部偏好直接采用。

L-N15 has now been read in full in English, including both linked tables and the actual Figure 1 image. Its [analysis](papers/L-N15.md) distinguishes a useful relation between teaching experience and emerging identity from unsupported claims about achievement and reduced conflict. The English same-fact edits retain that conceptual relation. No PDF layout check is claimed. [Verification](record-verification-12.json) confirms the source/extraction hashes, all four additional assets and 34 analysis-note hash references; only L-N15 changed among the 52 previous reading entries, and all four historical Chinese entries remain unchanged. Current English counts are 46 candidates, 33 acquired full texts and 31 empirical/boundary analyses: quantitative 10, qualitative 11, mixed 9 and one same-source transformation boundary case. One methodological application and two rereads remain separate.

### Q-N14 public HTML retry

A later direct request to the public PMC article URL returned HTTP 200 but no article element; the 21,315-byte response was not accepted as full text. The original Europe PMC XML HTTP 500 remains recorded. Browser access verified identity and opening material, not a completed source analysis. The new [retry record](acquisition-Q-N14-retry-01.json) preserves status, size and response hash. No acquisition or full-reading count changes; no source text is republished.

## Wave 10: English experimental and mixed-methods sources

The [new manifest](public-wave10.json) contains five English development candidates found through public search and checked against publisher and Crossref identities. Their DOIs were not found in the earlier indexed source records; the historical incomplete W identities still limit deduplication beyond known records. All five remain development material. Sources were selected for specific writing questions, not on the assumption that published papers are uniformly excellent.

| ID | Acquisition and actual reading | Selection and classification |
|---|---|---|
| Q-N15 | Publisher PDF acquired; identity and first page only | LEIP cluster-trial subgroup report on negative/null findings. A later reading of the main trial report would not create an independent intervention. |
| Q-N16 | Publisher PDF acquired; all 20 pages read; four page images checked | Randomized comparison of explanation activities. Positive theory-to-comparison moves, the distinction between learning experience and knowledge outcomes, and limitations of a presence indicator. [Complete English analysis](papers/Q-N16.md). |
| M-N17 | Publisher PDF acquired; all 19 pages and 16 supplement pages read; ten main and six supplement images checked | Interviews demonstrably inform the final survey and change how scores are interpreted. Counted as empirical mixed methods, with separate samples and no formal joint display. [Complete English analysis](papers/M-N17.md). |
| M-N18 | Publisher identity/abstract only; attempted PDF failed with SSL EOF | Candidate joint-display study of autistic students' classroom experience. Full-text acquisition, license and actual integration remain to be verified. Not counted as acquired or analyzed. |
| M-N19 | All 16 PDF pages and Tables 1–4 read; rendered pp. 5–9 and 12–14 inspected | Convergent mixed-methods development analysis completed subsequently. Open responses distinguish meanings of no reported change; unmatched strands, counterexamples and numerical reporting conflicts retained. |

Q-N16's SAV and preregistration were not read. For M-N17, all five PDF supplements were acquired and read; S1 Fig, the preregistration, raw data and original cited works were not read. Six supplement renderings emitted MuPDF structure-tree warnings, but their actual images were inspected and the relevant content was legible. Source tables preserve unresolved coefficient-scope and interaction-reporting issues; these have not been silently corrected. Full texts, figures and interview extracts are not republished in the repository.

Current English totals: 51 candidates, 37 acquired full texts, 33 empirical/boundary analyses (quantitative 11, qualitative 11, mixed 10, same-source boundary 1), one methodological application and two separate rereads. [Record verification](record-verification-14.json) checks the source/asset hashes, all 52 unchanged prior reading entries, four unchanged historical Chinese entries and the unchanged runtime tree. These checks establish record consistency, not writing quality. This batch contains original English editing illustrations but no new model comparison or final holdout result. [Reproduction instructions](wave10-reproduction.md) use public URLs and a reader-chosen cache.

M-N19 subsequently completed full English reading and analysis. The family-interaction paragraph explains three unchanged responses through role and established practice; the note retains two interview counterexamples, the unlinked-strand boundary and two table/text reporting conflicts. The [reading manifest](reading-mn19-assets.json) records eight actually inspected PDF pages. Current totals are 34 new empirical/boundary analyses: quantitative 11, qualitative 11, mixed 11 and boundary 1; candidate/acquisition counts remain 51/37. One methodological application and two rereads stay separate. This is source analysis, not a behavioral writing-effect finding.

[Verification 15](record-verification-15.json) checks the M-N19 record, the other 56 unchanged records, four unchanged historical Chinese records and the actual runtime freeze. The only runtime changes are the review annotation script and language-field instructions. Separate public English synthetic review tasks validate that workflow's default delivery, not the broader writing-distillation objective.

## Wave 11: English organizational and practitioner perspectives

The three DOIs in [this manifest](public-wave11.json) were not found in earlier registered source records. Selection targets collaborative autoethnography, early-childhood professional learning and implementation in inclusive elementary classrooms. All are development candidates. A search also returned Lareau's *Invisible Inequality*, already registered as E10 in the previous corpus; it was not counted again. Historical entries with incomplete identities still limit deduplication.

| ID | Acquisition and actual reading | Current use |
|---|---|---|
| L-N16 | Crossref identity and indexed excerpts checked; publisher PDF returned 403 | Collaborative-autoethnography candidate. No full reading or analysis claim. |
| M-N20 | Crossref and PMC identity checked; PDF endpoint returned HTML challenge content; accessible HTML was only partly screened | Head Start professional-learning candidate. Complete extraction and full reading remain pending. An accessible page is not counted as acquired-and-read full text. |
| M-N21 | Publisher PDF acquired and all 15 pages read; Tables 1–4 and eight page images inspected | Sequential explanatory mixed-methods analysis. Availability, preferences and specific work arrangements contribute different information; the table's convergence labels are examined rather than automatically adopted. |

M-N21's Crossref request returned 429; the publisher record and PDF establish the identity used here. Its references identify a larger research programme and related reports. Those reports were not read or counted as additional independent studies. Both supplementary files remain unread. The [English analysis](papers/M-N21.md) includes sentence, paragraph and whole-article work, a newly composed before/after/compressed example, and unresolved source discrepancies. Source text and images stay outside the repository.

To reproduce acquisition with a new reader-chosen external cache, use the existing tools:

```powershell
python -X utf8 distill/20261018/fetch_sources.py --manifest distill/20261019/public-wave11.json --out <cache>
python -X utf8 distill/20261018/prepare_reading.py --manifest distill/20261019/public-wave11.json --cache <cache> --digest <new-digest.json>
```

The [original acquisition digest](acquisition-public-wave11.json) retains the two failures; a future successful retry should preserve them. [Reading assets](reading-mn21-assets.json) list the exact M-N21 pages and rendering scale. [Verification 16](record-verification-16.json) checks this increment against `fac7429c426696ff3deeb4baf1122497cda4c6fd`: 57 previous reading records, including four excluded historical Chinese records, remain unchanged. The 203 runtime files are unchanged. Source analysis is not a behavioral improvement result, and the overall objective remains unfinished.

## Later reading and wave 12

[Q-N15](papers/Q-N15.md), previously acquired in wave 10, is now read through all 21 PDF pages, including the flowchart and seven tables. Twelve rendered pages were inspected. Its local positive moves connect competing expectations to subgroup questions and develop explanations of adverse findings. The article also contains unresolved population, threshold and scoring descriptions and overextended interpretations. These remain explicit rather than becoming runtime guidance. The protocol, power supplement, registration, main trial report and cited originals remain unread; this subgroup report is not an independent trial from them.

[L-N17](papers/L-N17.md) was registered in [wave 12](public-wave12.json), after checking its DOI and author names against the indexed corpus. It was obtained from the journal's public PDF endpoint, with successful Crossref identity retrieval. All 12 PDF pages, including references and contributor information, were read; six actual page images cover the narratives and their embedded teaching artifacts. Its concept-to-action sequence is a reason for selecting particular writing moves, not certification of every claim about learning communities. The journal's current open-access policy states CC BY 4.0; the original PDF bears a 2021 journal copyright notice. Original emails and collaborative notes were not independently inspected.

[M-N20](public-mn20-html-retry.json) is now acquired as complete public PMC HTML. The earlier PDF challenge remains in wave 11's digest. A small addition to the existing development downloader recognizes the PMC main-body container while rejecting challenge and abstract-only pages. The first extraction included all three tables but omitted the 103 reference entries. An [actual content-preservation check](pmc-extraction-checks.json) reproduced that failure; after including reference citations and removing navigation text, all 103 entries and all three tables are retained. A 12-page public PDF still extracts successfully. The [initial extraction](acquisition-mn20-html-retry.json) and [corrected extraction of the same received bytes](acquisition-mn20-html-retry-final.json) are both recorded. The corrected reading file has 200 blocks. This is acquisition progress only: remaining full reading and analysis are pending.

Reproduce the new acquisitions using separate, new external caches:

```powershell
python -X utf8 distill/20261018/fetch_sources.py --manifest distill/20261019/public-wave12.json --out <pdf-cache>
python -X utf8 distill/20261018/prepare_reading.py --manifest distill/20261019/public-wave12.json --cache <pdf-cache> --digest <new-pdf-digest.json>
python -X utf8 distill/20261018/fetch_sources.py --manifest distill/20261019/public-mn20-html-retry.json --out <html-cache>
python -X utf8 distill/20261018/prepare_reading.py --manifest distill/20261019/public-mn20-html-retry.json --cache <html-cache> --digest <new-html-digest.json>
python -X utf8 distill/20261019/verify_pmc_extraction.py --source <html-cache>/M-N20/source.html --pdf <pdf-cache>/L-N17/source.pdf
```

Q-N15 can be acquired separately with `public-wave10.json --ids Q-N15`. The [reading-assets manifest](reading-qn15-ln17-assets.json) identifies all 18 actually inspected page images and the rendering scale. No source PDFs, full HTML, images or private manuscript content are republished. Current English totals are 55 candidates, 40 acquired full texts, 37 empirical/boundary analyses, one methodological application and two rereads. [Verification 17](record-verification-17.json) records two changed older reading entries (Q-N15 and M-N20), 58 unchanged entries including all four historical Chinese records, and one new entry. Runtime skills remain unchanged. No new behavioral comparison or final holdout result is claimed.

## M-N20 completed English reading

The subsequent reading covers all 200 corrected M-N20 HTML blocks, the three tables both in extraction and as separate HTML cells, and both original figure images. [The analysis](papers/M-N20.md) identifies the actual topic-level integration and distinguishes teachers' anticipated uses from reported experiences. There is no joint display in this article; Figure 1 shows the design and Figure 2 maps the participants. [Image provenance](reading-mn20-assets.json) gives the public image URLs and hashes. Reproduce acquisition with the HTML command above, then use the figure image links in the acquired source. No successful PDF retrieval or PDF inspection is claimed.

The new same-fact English revisions preserve item denominators, the linked volunteer sample, uncertainty about the reason for neutral survey responses and the untested external-support proposal. The article's own declaration reports AI-assisted surface editing. Its inclusion rests on specific argument moves, not a claim that its prose was unaided or uniformly exemplary. Related programme reports and cited original studies remain unread.

An additional public search for L-N03 confirmed the title and DOI on the publisher and [author research page](https://jessica-calarco.squarespace.com/research). The author page links to the restricted publisher record, without an accessible full-text copy located in this search. The record therefore remains awaiting full text; this search adds neither an acquired article nor a completed reading. The separately found 2011 help-seeking article was not registered or read as another source.

English totals are now 55 candidates, 40 acquired full texts and 38 empirical/boundary analyses: 12 quantitative, 12 qualitative, 13 mixed and one separately counted transformation boundary case. One methodological application and two rereads remain separate. [Verification 18](record-verification-18.json) compares the increment with `b1c1cd8e3f2a6f07d14f285c1b3463ec5589950c`. Only the M-N20 reading record changes; the other 60 records, including four excluded historical Chinese records, and all 203 runtime files remain unchanged. This is English source-analysis progress, not a new behavioral evaluation or completion of the overall objective.

## English wave 13 and completed M-N12 reading

M-N12's direct-download failures remain in the earlier acquisition records. The public web PDF reader provided the full 14-page text. Four overlapping responses were retained outside the repository; merging by the reader's numbered lines covers all 1,036 lines without gaps or conflicting overlaps. Table 1, references and declarations were read. URL-based screenshot calls failed; a later reader-reference response supplied no inspectable image here. Instead, all six original figure images were downloaded successfully from links observed on the publisher HTML and actually viewed. The [provenance record](reading-mn12-web-assets.json) gives public URLs and hashes, and distinguishes this reading from possession or rendering of the PDF bytes. The [English analysis](papers/M-N12.md) is a methodological application, separate from empirical exemplars. The same project's other publications are not additional independent studies.

The [Q-N14 HTML retry](public-qn14-html-retry.json) returned HTTP 200 but no full-article body. The existing extractor rejected it, and the [failure record](acquisition-qn14-html-retry.json) remains visible. There is no additional full-text reading for Q-N14.

[Wave 13](public-wave13.json) adds five English development candidates after checking the indexed corpus for DOI/title/author matches. Historical records with incomplete identities still limit perfect deduplication. [The original acquisition digest](acquisition-public-wave13.json) records three successful acquisitions, Q-N18's obsolete repository URL returning 404, and L-N18's publisher PDF returning 403. The actual University of Chicago landing page redirects to a new record and supplies replacement links for Q-N18. Its [retry manifest](public-qn18-repository-retry.json) and [successful digest](acquisition-qn18-repository-retry.json) retain that distinction. The [26-page supplement](acquisition-qn18-supplement.json) was also acquired, but remains unread. The existing PDF parser correctly accepted the repository's application/octet-stream response after validating PDF bytes; no parser change was needed.

Current screening is deliberately limited: Q-N17's title/authors and search excerpts; the opening title/authors/abstract excerpts of Q-N18 and M-N22; and M-N23's publisher cover. These checks verify candidate identities, not complete reading or writing quality. Q-N17 has 240 extracted HTML blocks, Q-N18 a six-page article, M-N22 an 11-page article and M-N23 a 25-page file including its cover. M-N22/M-N23 still require confirmation of the actual integration. L-N18 remains pending access. Earlier double-dose algebra reports concern the same policy and cohorts as Q-N17 and cannot automatically be counted as independent replications.

Reproduce acquisition using new external caches:

```powershell
python -X utf8 distill/20261018/fetch_sources.py --manifest distill/20261019/public-wave13.json --out <wave13-cache>
python -X utf8 distill/20261018/prepare_reading.py --manifest distill/20261019/public-wave13.json --cache <wave13-cache> --digest <wave13-digest.json>
python -X utf8 distill/20261018/fetch_sources.py --manifest distill/20261019/public-qn18-repository-retry.json --out <qn18-cache>
python -X utf8 distill/20261018/prepare_reading.py --manifest distill/20261019/public-qn18-repository-retry.json --cache <qn18-cache> --digest <qn18-digest.json>
```

The Q-N18 supplement link is in the retry manifest. M-N12's public PDF/HTML and all six figure links are in its provenance record; inspect the article in a reader capable of opening it. Do not interpret a fresh access failure as absence of the article or claim a complete reading from an abstract.

English totals are 60 candidates, 45 acquired/readable full texts (44 downloaded, one complete public web reading), 38 empirical/boundary analyses, two methodological applications and two rereads. [Verification 19](record-verification-19.json) compares this increment with `2be9dbf09085826319b677c9b36c6c1ac3de1d33`. The four historical Chinese records and all 203 runtime files remain unchanged. Source reading and acquisition are progress toward the corpus objective, not evidence of a new writing-quality effect or completion of the overall goal.
