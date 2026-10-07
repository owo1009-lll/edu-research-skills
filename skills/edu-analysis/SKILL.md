---
name: edu-analysis
description: Analyze education research data in R with a recorded run for every analysis - descriptives and reliability, t tests, ANOVA and nonparametric tests, chi-square, correlation, hierarchical and logistic regression, moderation and bootstrap mediation, EFA/CFA with CR/AVE/HTMT and common-method-bias checks, CB-SEM, PLS-SEM, fsQCA, NCA, multilevel and longitudinal models. Use for 问卷数据分析、量表信效度、描述统计、差异检验、t检验、方差分析、非参数检验、卡方检验、相关分析、回归分析、Logistic回归、调节效应、中介效应、结构方程、SEM、PLS-SEM、验证性因子分析、共同方法偏差、fsQCA、组态分析、NCA、必要条件分析、多层线性模型、纵向数据、准实验数据分析.
---

# 教育学数据分析

用户提供数据和一句需求即可，不需要准备配置文件。所有分析在用户当前的论文文件夹里运行，结果写入 `edu_output/analysis/`；原始数据只复制到这个文件夹，不上传。

## 步骤

1. **弄清数据和问题。** 确认分析单位、分组与时点、嵌套（班级、学校）、题项计分方向、缺失编码和研究问题。只有会改变方法选择的信息缺失时才询问用户，其余从材料中读取并在结果里写明。
2. **选方法。** 查 [选方法](references/method-selection.md)，再读对应的方法卡（`references/methods/`）。用户指定的方法与数据不符时，说明原因并给出替代。分析前写下要做哪些检验；看过结果后增加的分析标为探索性。
3. **环境自检（首次使用或换电脑时）。** 运行 `python <本skill>/../edu-shared/scripts/edu_runtime.py` 找到 Rscript（找不到时请用户安装 R，或用环境变量 `EDU_RSCRIPT` 指定），再用它运行 `tests/known_answers.R`，全部通过再继续；缺包时运行 `scripts/setup_packages.R`，它只安装缺少的包，装在 R 的用户库里，运行前告诉用户。
4. **写分析脚本并运行。** 按方法卡写 `analysis.R`：`source("edu_methods.R")`，从 `inputs/<文件名>` 读数据，用 `edu_save(结果, "名称")` 输出。然后在用户的论文文件夹里运行：
   ```
   python <本skill>/scripts/run_r.py --script analysis.R --input 数据.csv --slug 简短名称
   ```
   需要严格记录与诊断的进阶设计（测量不变性、重复测量与混合设计、线性混合模型、CLPM、RI-CLPM、增长模型）用标准适配器：`--adapter basic|advanced --plan plan.json`，方案格式见 [基础适配器](references/analysis-contract.md) 和 [进阶适配器](references/advanced-analysis.md)。
5. **检查运行结果。** 读 `run_status.json` 和 `stderr.log`。失败的运行保留不删，修正后重新运行生成新文件夹。检查模型是否收敛、有无负方差、样本量是否与预期一致。
6. **报告。** 按 [报告格式](references/reporting.md) 整理三线表和结果句子：动词与设计相符，不显著结果照常报告并解释。需要写成论文段落时交给 edu-writing，并附上 `edu_output` 中的结果文件路径。

## 文件

- `scripts/edu_methods.R`：分析函数（`edu_describe`、`edu_reliability`、`edu_harman`、`edu_cmb`（共同方法偏差三项检验）、`edu_compare`、`edu_chisq`、`edu_cor`、`edu_regression`、`edu_moderation`、`edu_mediation`、`edu_cfa`、`edu_sem`、`edu_pls`、`edu_fsqca`、`edu_fsqca_robust`、`edu_nca`、`edu_nca_plot`、`edu_kappa`、`edu_icc`）。
- `scripts/run_r.py`：运行并记录（脚本、数据指纹、R 版本与包版本、日志）。
- `tests/known_answers.R`：用 R 文档例题、lavaan 教程和解析解核对全部函数。

诚信要求见 [共同规则](../edu-shared/references/integrity.md)。
