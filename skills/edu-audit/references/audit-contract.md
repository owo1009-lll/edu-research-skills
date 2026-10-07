# 核查合同

官方软件依据：[R sd](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/sd.html)，按 n−1 分母计算；[Rscript](https://stat.ethz.ch/R-manual/R-devel/library/utils/html/Rscript.html)。核对日2026-10-02。此说明不是期刊规定。

项目选择：不执行多层、相关推断、回归、SEM或Barnard检验。发布论文的主模型即使存在，也不能由本原型的描述性适配替代。方法意见与原模型复现分栏。

E17真实案例：Hasan & Khan (2023), doi:10.1371/journal.pone.0288844，Table 4及Measures of impact。结局阈值为最终成绩≤64；机器学习训练标签<70是另一含义。原文32干预、33对照；失败3和9，通过29和24；RR=0.34。只复算计数/RR；未复算单侧非合并方差Barnard p=0.0352，未新增置信区间。附件训练CSV没有随机组别与结局对应关系，不作为65人试验原始数据使用。

E01真实案例：Emery et al. (2021), doi:10.1371/journal.pone.0250760，Table 3、Self-efficacy及S5/S1 Data。212课程行对应80参与者；6项提供的自效能分量表在个体内不变。去重后两组各40人。原条目与未舍入计分不可核验，原模型关键变量也未全在CSV中；因此是条件性描述复算，不是整篇复现。7/24比较超出显示容差，原因未确定，不能自动改原文。

无法复核示例：Thinking about Kindergarten thinking, doi:10.3389/fpsyg.2022.933541，Data availability statement明确额外伦理许可需求。保留质性与量化论证核查；不索要或伪造受限儿童记录。
