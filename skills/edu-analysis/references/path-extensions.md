# 观测变量线性路径扩展 · 0.2.0-dev.1

用户提供数据、变量说明及问题；助理建立内部JSON方案。本批只接受连续数值结果、一行一个独立分析单位（`one_per_unit`）。重复测量、已识别的班级/学校/场次聚类、复杂抽样不能通过唯一ID强行忽略。

## 参数、编码与样本

三方法共有：`x,outcome,covariates,center,inference,time_order,path_rationale`，并声明`missing=complete_case`。同一方法所有模型使用所有角色变量的共同完整案例；不逐路径换样本。解释变量、结果、调节/中介、协变量角色必须不同。时间顺序和路径理由不能为空；书写理由不等于识别因果。

- `moderation`另需`w,moderator_values`。X可为非恒定数值或明确参照组的多类别因子；W可为非恒定数值或两类别因子。模型为Y~X*W+协变量。数值X还需原尺度的`plot_x_values`；数值W的条件值及数值X图示值限于观察范围。
- `simple_mediation`的`mediators`恰有一个非恒定数值中介；X为数值或两类别因子。类别X按第一声明参照组=0、另一组=1转换。
- `serial_mediation`的`mediators`恰有两个非恒定数值中介，顺序由问题先行指定；X范围同上。不自动重排变量或筛选显著路径。

协变量可用已声明的数值或类别编码。`center`为显式列表；只接受指定的数值X（及调节时的数值W），允许空列表。不中心化因子、中介或协变量。中心化均值与完整案例数保存于encoding记录；中心化不是强制步骤，也不是因果修正。

## 估计、区间与图

系数为原单位。`inference=OLS`使用lm协方差及残差df的t参考；`HC3`使用异方差稳健协方差及残差df的近似t参考。秩不足、系数非有限或残差自由度少于3则停止。HC3不解决非线性、聚类或混杂。

调节：保存交互系数及区间。数值X输出在指定W值的一单位X简单斜率；类别X输出各非参照组对参照组的条件差。通过模型矩阵差L计算估计Lβ、SE=sqrt(LVL')。图为条件均值及点态置信带，非个体预测区间；数值协变量固定于完整案例均值，类别协变量固定于声明参照组。未做多重比较校正，也未实现Johnson–Neyman区间；条件显著不等于交互显著。

简单路径：M=aX+C；Y=c'X+bM+C；另拟合Y=cX+C；间接关联ab。链式：M1=a1X+C；M2=a2X+d21M1+C；Y=c'X+b1M1+b2M2+C。具体路径a1b1、a2b2、a1d21b2；每次拟合均核对总效应=直接+总间接。

Bootstrap按完整独立单位抽整行，每次重拟合全部路径，在每次重抽样内求具体和总间接量。总间接区间来自总量的分布，不把各路径区间端点相加。记录seed、RNG、请求次数、有效次数、失败原因、区间方法；索引和逐次结果留私有目录。至少200次且联合有效次数达到80%才输出百分位区间，R quantile type7；未实现BC/BCa或聚类Bootstrap。

不设置总效应显著性门槛。横断面间接关联不能写成已发现的因果机制；即使时间在前，也仍需相应识别条件。模型中不包含X×中介交互、非线性结果、潜变量、测量模型、SEM、纵向或多层路径。

## 检查与使用

程序用独立NumPy/SciPy实现核对点估计、OLS/HC3区间、条件效应、每次整组路径重抽样和百分位算法。明确标为模拟的测试检验程序；开发期的真实案例已归档到 archive/dev-history 分支，复算一致不认证数据真实或模型质量。

R原始说明：[lm](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/lm.html)、[quantile](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/quantile.html)、[predict.lm](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/predict.lm.html)。本项目样本、Bootstrap和输出策略是方法选择，不是R官方统一要求。
