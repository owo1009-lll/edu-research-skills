# 目标期刊检索：AJET公开端到端示例

日期：2026-10-13。请求：为一项**尚未采集数据的合成研究构想**寻找AJET及其编辑团队的相关研究，补充必要理论和竞争证据，并修改引言的问题定位。原始构想与完整角色记录在 [brief.json](brief.json)。无用户私有数据。

## 实际检索与身份核验

期刊是 *Australasian Journal of Educational Technology*，官网说明由ASCILITE出版，定位于高等教育中的技术研究。[官网](https://ajet.org.au/index.php/AJET)、[作者须知](https://ajet.org.au/index.php/AJET/about/submissions)、[编辑团队](https://ajet.org.au/index.php/AJET/about/editorialTeam)。官方历史出版物列出电子ISSN1449-5554，API亦按该号返回本刊记录。

查询当日官网列出的Lead Editorial team为Linda Corrin、Chris Deneen、Feifei Han、Henk Huijser；本题相关Associate Editors包括Seyyed Kazem Banihashem和Omid Noroozi。Michael Henderson明确列为Past AJET Lead Editor；Antonina Petrolito是Copyeditor，未作为当前学术编辑检索。没有推断处理本稿的人选。

Banihashem的完整姓名、当前机构和研究方向由[Maastricht个人页](https://www.maastrichtuniversity.nl/nl/k-banihashem)核实，旧机构及ORCID由[WUR机构存档PDF第12页](https://edepot.wur.nl/658826)交叉核对。2026年C&E论文的作者ORCID与之相符；2024年论文在Crossref没有作者ORCID，使用出版社署名和Open Universiteit出版记录对应，未把缺失字段标成自动匹配。

实际遇到的身份风险：

- 查询Chris Deneen得到的`10.37237/110306`实际作者是Chris Harwood与Dennis Koyama，已记为different_person，未据此称为编辑成果。
- [2024年社论网页](https://ajet.org.au/index.php/AJET/article/view/10258)给Feifei Han与Chris Deneen显示同一ORCID，不能直接同时采信。本例不用该冲突ORCID确认Deneen，也不根据旧社论推定当前角色。
- [AI反馈特刊征稿页](https://ajet.org.au/index.php/AJET/AJETSI2026AIFeedback)列出Shen Ba、Lan Yang、Zi Yan、Chee Kit Looi、Dragan Gašević为客座编辑，投稿截止2026-06-30，早于本次查询。本例按常规投稿，不推定特刊仍开放。测试另外检查只有明确目标特刊匹配时才纳入客座编辑查询。

第一次API检索保存为[discovery.json](discovery.json)，两项B查询遭遇429，记录为partial；随后仅重试失败查询，保存[discovery-retried.json](discovery-retried.json)，11项查询全部完成，取得52篇去重候选。C的前五条未包含反馈素养原始概念文，另经HKU机构记录补充，最终53篇见[discovery-final.json](discovery-final.json)。查询词、返回范围和补充来源均保留；不是系统综述。脚本已加入有限的429/503重试，失败仍明确报告。

## 取舍和实际改稿

[decisions.json](decisions.json)保存8项重点筛选的阅读范围、对应论断、位置与理由；其余45篇仍标未评阅，不伪称全文筛完。完整书目信息在最终检索记录与[引用建议表](recommendations.md)。

| 来源 | 用途与实际阅读范围 |
|---|---|
| Li & Kim, 2024，AJET | A：自动反馈的批判性参与；摘要。保留工具差异，不当作ChatGPT效果研究 |
| Banihashem et al., 2024，IJETHE | B：论证文反馈的功能差异；方法、结果、讨论、局限及身份信息。保留互补作为设计理由，未宣称组合成效已证实 |
| Pozdniakov et al., 2026，C&E | B：学生提供反馈时对AI修订建议的采用；机构/出版社摘要。不是收到反馈后修改作文的采用率 |
| Carless & Boud, 2018，AEHE | C：反馈素养概念；HKU摘要。不虚构量表或干预效果 |
| Weidlich et al., 2025，CAEO | C：感受与作品改善可能不同；机构存档的出版社PDF第1页摘要及署名。未补写效应系数或机制 |
| Lodge et al., 2023，AJET社论 | 办刊方向备查；来源片段。未作为实证证据或强制引用 |
| Huijser, 2009，书章 | 题名/元数据筛除：泛网页学习对象设计，未显示本例的直接用途 |
| Harwood & Koyama, 2020 | 身份误命中；出版者题录与摘要核对后仍作备查，未放正文 |

[修改前](manuscript-before.md)把迅速、个性化反馈直接连到写作提高，并仅凭本地研究少立论。[修改后](manuscript-after.md)实际写出质量—采用—修订之间的问题，保留“学生应对反馈判断负责”的立场，并清楚说研究尚属计划。正文没有编辑身份、引用配额或录用承诺。这是主任务做的来源整合示范，不冒充盲评中的技能迁移输出。

最终来源复核将“修订反馈”和“修订作文”分开，避免把不同教育活动当成同一个结局。Weidlich等的[机构PDF](https://www.ife.uzh.ch/dam/jcr%3A240d1fe5-81a5-4670-8e0d-b8ab9548d498/Weidlich%20et%20al_2025_Teacher%20peer%20or%20AI_Comparing%20effects%20of%20feedback%20sources%20in%20higher%20education.pdf)第1页另确认作者拼写Bütler、Maag Merki。最终纳入的五条文献已实际运行既有`verify_references.py`，全部身份字段核对通过：[依据表](ledger.json)、[在线核验结果](identity-verification/verified.json)。来源语义支持由阅读判断，不由该脚本认证。

## 复现

从仓库根目录运行，选择不存在的新输出路径：

```text
python skills/edu-writing/scripts/search_journal.py search --brief evals/capability-20261013/journal/brief.json --limit 5 --out edu_output/journal-new-search.json
python skills/edu-writing/scripts/search_journal.py check --record evals/capability-20261013/journal/discovery-final.json --decisions evals/capability-20261013/journal/decisions.json --out edu_output/journal-new-check.json
python -m unittest discover -s tests -p test_journal_search.py -v
```

重新查询可能改变候选排序、身份和数量，需重查官网；保存记录的核对可离线复现。[最终记录检查](decision-check-final.json)只证明记录及标识关系符合设计，`source_truth_check`和`claim_semantics_check`均为`not_performed`。正文支持关系由实际阅读另行判断；摘要支持仅用于当前概括。外部论文版权仍归原权利人，仓库未复制全文或原图。
