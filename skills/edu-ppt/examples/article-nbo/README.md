# 真实开放文章：NBO中文解读

问题从“婴幼儿情绪社会性发展”收束为：帮助母亲理解婴儿信号后，自评学习与观察到的互动是否一起改善？选文过程见[selection.md](selection.md)。这不是系统综述。

[plan.json](plan.json)是15页、计划15分钟的中文四步走内容快照，包含实际上屏文案、完整讲稿、逐页来源和时间。N02解释核心概念，N10B对照最接近的澳大利亚试验；定义和比较的核实范围见[来源记录](source-notes.md)。执行：

```text
python <edu-ppt>/scripts/build_deck.py --plan <edu-ppt>/examples/article-nbo/plan.json --out <任务目录>/nbo
```

加`--content-only`仅导出内容稿和讲稿。模板或样式变化仍复用这个计划；成品要另外执行渲染和检查。本轮前后内容、成品与实际渲染记录见[定向修订验证](https://github.com/owo1009-lll/edu-research-skills/blob/main/evals/ppt-revision/README.md)，旧版记录仍保留在仓库`evals/edu-ppt-evaluation.md`。

原研究归Valla、Slinning、Wentzel-Larsen、Røsand与Arnardóttir（2025）所有：[出版社全文](https://link.springer.com/article/10.1186/s12884-024-07128-0)，BMC Pregnancy and Childbirth 25:13，DOI 10.1186/s12884-024-07128-0，许可为[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。此例是中文教学解读，非原作者背书；翻译、压缩、重组和表6、7的原生区间图属于改编。`figure1.jpg`为原文Fig.1，从出版社PDF提取，图内信息未修改；它是可移动的图片，内部元素不可编辑。全文PDF不随技能分发。

已读正文及表格；表6、7另对照PDF第9页视觉核查。主要区间与模型身份保留；未调整与调整后的非敌意结果分开讲。原文表7部分n与研究样本数不一致，保留疑点而不自行补正。纵向原图在投影时过小，因此主讲页重绘有来源人数流程，完整原图留附录供放大核对。讲述时间尚无真人排练验证。
