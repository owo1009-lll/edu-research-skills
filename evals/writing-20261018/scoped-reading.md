# 收窄版本的新来源读取记录

r01 在 [冻结记录](scoped-freeze.json) 的时间点固定，随后选择 H6/H7。选择时对照可恢复的旧索引、13 篇开发论文及 H1–H5；Deslauriers 2019 因已出现而排除。缺失的早期 W 清单仍限制全历史去重。H6/H7 未参与 r01 的规则修改。

| 来源 | 实际读取范围 | 用途与核对 |
|---|---|---|
| H6 Kestin et al. 2025，10.1038/s41598-025-97652-6 | 主文 B001–B058、脚注 B062–B072；Figures 1–3 实际查看；补充 DOCX 全部段落及四张表文字 | 新写任务。区分主动学习对照与普通讲授、成套教学条件与单一 AI 成分、均值图与中位数、即时成绩与长期学习。补充表 S1 的 0.63 位于内容控件中，简单 DOCX 提取漏掉 63，经 OOXML 核实；此问题是提取错误，不归为原文疑点。补充文档内嵌图未逐一查看，任务不依赖其中界面细节。 |
| H7 Otaki et al. 2023，10.1371/journal.pone.0280310 | 主文 B001–B116、Tables 1–3，Figures 1–3 实际查看；补充材料仅目录，未读数据与访谈原件 | 真实讨论压缩。图 2/3 明示 GPA 数值，故按标签转录，不从像素推算区间。保留 8A 框架及实践立场，同时区别跨队列叙述、课程成绩与个体变化。方法/结果的记录覆盖范围不一致留作来源问题。 |

读取使用与首轮相同的获取/段落定位脚本（见 [来源方法](holdout-reading.md)）。原文与图片存于仓库外；公开输入提供完成任务所需的事实及定位，不要求私人文件。H6 以事实释义供新写，不公开复制其 ND 许可文章或图；H7 的原文节选保留 CC BY 4.0 署名与许可。

从仓库根目录重建定位文件：

```powershell
python -X utf8 distill/20261018/fetch_sources.py --manifest evals/writing-20261018/scoped-sources.json --out <新的仓库外目录>
python -X utf8 distill/20261018/prepare_reading.py --manifest evals/writing-20261018/scoped-sources.json --cache <同上目录> --digest <新的记录文件>
```

图像与 H6 补充文档的具体下载 URL、字节和散列见 [获取记录](scoped-acquisition.json)。H7 原文节选取 reading.txt 的 B110–B114 和 B116，移除定位行，保留段落内容及引文编号，分别加 Discussion/Conclusion 标题；共 1,173 个空白分隔词（含这两个标题）。具体片段散列见 [输入冻结](scoped-input-freeze.json)。

只有本文回顾所述的此前研究，不冒充独立阅读全文。全部来源核对为文献层面，不是原始数据复算。H6/H7 每种规则各两次写作，使用同一任务和事实包；不因结果增跑。评阅继续采用 [八项协议](holdout-judge-request.md)。
