# 本轮全文写作蒸馏

基线是公开库 0.12.0 的 `a4020c41a4f3d8ab180a4e2818955d90e40f6f3b`。本轮完成 13 篇新增开发全文的精读，另选 7 个真实来源分两批验证。**定量比较与有依据的解释正式保留；混合整合仍为候选，其他广泛增补撤回。** 数量仅说明工作范围，取舍依据是原始文本和比较结果，见 [最终实施](implementation.md) 与 [验证结果](../../evals/writing-20261018/scoped-results.md)。

## 当前证据

- [既有来源索引及候选去重](prior-index.json)：77 篇原语料、当前来源卡、此前训练/留出来源及可恢复的历史身份。部分 W 系列原始清单已无法在两个仓库当前树中找到，因此“新增”目前指未见于可用既有记录，不能证明丢失会话从未读过。Yeager 2019（W07）及已确认复读来源排除在新增数外。
- [候选新增清单](new-sources.json)：12 篇文件已经获取；[补充清单](sources.json) 中 E06 Rohrer 2018 是另 1 篇新增候选，E01–E05/E07 为复读。英语为主，含定量、质性、混合、理论、综述及 2 篇中文论文。选文理由先作为具体阅读问题，不能以名刊或已发表身份推定整篇优秀。
- [获取记录](acquisition-new.json)：身份元数据、链接、成功或失败尝试、字节与文本校验值。E16 是整期下载中的一篇，仅 PDF 52–60 页计为目标文章；其他文章没有计入语料。
- [实际阅读范围](reading-coverage.json)：首批 13 篇主文精读已完成，各篇图表、附录、脚注与未读范围分别登记。E10 下载阶段的 DOI 未检出，经首页视觉核对及题名、作者、期刊卷页对应确认身份；文件名的 2003 不替代实际出版年 2002。获取成功与实际阅读仍分别记录。
- 逐篇分析：[E06 方法论教程](papers/E06.md)、[E08 定量观察研究](papers/E08.md)、[E09 质性访谈](papers/E09.md)、[E10 家庭民族志](papers/E10.md)、[E11 数学归属感混合研究](papers/E11.md)、[E12 反馈使用混合研究](papers/E12.md)、[E13 阅读反馈批判综述](papers/E13.md)、[E14 学习与表现整合综述](papers/E14.md)、[E15 主动学习元分析](papers/E15.md)、[E16 理论论证](papers/E16.md)、[E17 中文研究项目与概念建构](papers/E17.md)、[E18 中文教师负担质性研究](papers/E18.md)、[E19 实地干预](papers/E19.md)。包含可定位的写作动作及不应照搬的反例，尚不是正式规则。
- [跨文章比较](cross-article.md)：7 项候选方法，每项包括待解决问题、具体动作、多篇定位、条件、例外及同事实改写；明确与已有方法卡的合并关系。[候选实施状态](candidate-status.md) 区分已改文件与尚待完成部分。
- [现行规则与旧输出审计](audit.md)、[对照验证协议](../../evals/writing-20261018/protocol.md)。D1/D2 合成开发任务完成八份样稿及四组匿名评阅：[开发结果](../../evals/writing-20261018/development-results.md) 为两组候选有限优势、两组无稳定优势，各任务均未显示重复稳定提升。[候选冻结记录](../../evals/writing-20261018/candidate-freeze.json) 固定后续留出输入；未将候选发布为有效成果。

## 重建阅读材料

从仓库根目录运行；需要 Python、requests、beautifulsoup4、lxml、PyMuPDF、python-docx。全文放在仓库外的全新目录，脚本拒绝覆盖旧获取记录。

```powershell
python -X utf8 distill/20261018/index_prior.py
$readingCache = Join-Path $env:TEMP 'edu-writing-new-fulltexts-20261018'
python -X utf8 distill/20261018/fetch_sources.py --manifest distill/20261018/new-sources.json --out $readingCache
python -X utf8 distill/20261018/prepare_reading.py --cache $readingCache --digest (Join-Path $readingCache 'reproduced-digest.json')
```

E06 可用 `fetch_sources.py --manifest distill/20261018/sources.json --ids E06 --out <另一全新目录>` 获取。HTML 表格如为另页链接，需单独打开；E11 的 4 个表格链接和校验值在阅读记录中。网页字节可能更新，校验值用于识别本次具体读取的文件，不要求未来网页永久相同。PDF 文本顺序需逐篇检查，页码按收到文件的实际页数，不以 DOI 出现在任意页就认定整份文件均为目标文章。

## 验证与最终范围

广泛候选 q01 在五类真实任务中，定量/混合各两次有局部优势，中文质性、理论翻译和综述的单次比较略偏基线；因此收窄为 r01，再冻结并选择两个新来源。r01 的定量任务两次局部占优，混合一次局部占优、一次相当。最终只采用定量部分的原文字节；最终子集未另外重跑整树，不宣称每条规则的独立效果或全类型提升。完整首稿、自查、终稿、理由、技能快照及原评阅均在 [验证目录](../../evals/writing-20261018/README.md)。

原始全文存于仓库外，公开记录提供合法获取方式、原创分析、事实包，以及有署名和许可的 CC BY 节选。没有读取或发布用户私有稿件。逐篇笔记中的“候选”“尚待验证”记录其形成时点，最终状态以本页及实施记录为准。全部评阅为 AI，没有真人验证；材料范围和历史去重缺口分别明示。开发笔记不加入日常技能加载路径。
