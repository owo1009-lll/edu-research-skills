---
name: edu-audit
description: Check the statistics in education papers or drafts - recompute reported values against their tables and data with recorded R runs (counts, percentages, risk ratios, means and standard deviations), and review how statistics are reported (degrees of freedom, effect sizes, confidence intervals, p values, fit indices, reliability and validity, common-method bias, assumptions, multiple-comparison corrections). Use for 结果复核、复算、核对论文数据、核对均值标准差、核查统计结果、检查报告值、统计报告审查、统计规范检查、审稿前自查数据.
---

# 教育学结果复核

两种任务，可以同时做：

| 用户要什么 | 做什么 |
|---|---|
| 核对论文或稿件里的数字对不对（"表 4 的计数和风险比对吗""均值标准差能复算出来吗"） | **A. 复算核对**：用数据或表格重新计算，比较原值与复算值 |
| 检查统计结果报告得规不规范（"看看我的结果部分统计报告有没有问题"） | **B. 统计报告审查**：不复算，检查报告是否完整、格式是否规范 |

## A. 复算核对

先读 [核查合同](references/audit-contract.md)，确定层级：A 一致性核查、B 汇总复算、C 原始数据条件性复算、D 方法意见。可同时输出多个层级，但不能混称为完整复现。

1. **记录设置。**对照全文和数据字典，记下分析单位、组别、样本筛选、计分、缺失、标准化、估计和区间设置，每项写出来源位置或"未知"；不凭列名推断。时间、学校、班级嵌套和重复测量不能忽略。
2. **选适配器。**
   - `summary_counts`：两组失败/通过计数及失败风险比。
   - `descriptive_repeated`：同一参与者的重复行中数值不变时去重，按变量可用个案计算均值和 n−1 标准差；必须标明是条件性复算。条目计分无法从总分恢复；随时间变化的重复测量直接拒绝，不默认求平均。
3. **配置并运行。**按 [配置示例](references/configuration.md) 建 JSON 和带来源的原值 CSV，在用户的项目文件夹中运行：
   ```
   python <本skill>/scripts/run_audit.py --config <项目内相对配置路径>
   ```
   需要 Python 标准库和 R 的 jsonlite。脚本只读项目内输入，复制到新运行目录，保存配置、哈希、代码、输出日志、sessionInfo 和比较 CSV。它限制路径，但不是安全沙箱；不执行论文附带的未知代码。Rscript 由 `../edu-shared/scripts/edu_runtime.py` 自动查找，也可用 `--rscript` 或环境变量 `EDU_RSCRIPT` 指定。
4. **比较。**人数精确比较；连续值按原文显示位数的半个单位容差比较，不因结果不通过而改容差。阈值 p、区间、多重插补、回归、SEM、Bootstrap 目前没有适配器，不用类似算法冒充复现。
5. **报告。**展示差异和设置缺口，说明各统计量的含义；计算一致不证明数据真实，设置不一致不能直接归为论文错误。

**停止条件和限制**：
- 描述统计必须明确提供量表范围、缺失编码、计分和样本说明；缺少时先停下，不用默认值补全。原值表为空不算成功核查。
- 原文给出各组人数时，在配置中填写有出处的 `expected_participants_by_group`，核对去重后的人数；按变量的缺失和有效样本存入 `missingness.csv`。被错误声明但内部一致的样本口径，脚本发现不了，仍需回原文。
- 公开分量表没有缺失，不证明条目没有缺失；参与者组别不变，不证明配对关系随时间不变。

**输出**：比较表、核查报告、未决事项和可引用的结果键，写入 `edu_output/audit/`。写作只使用已标明范围的结果；描述统计核对通过，不代表主模型也核对过。

## B. 统计报告审查

1. 读用户的稿件（结果部分为主，方法部分一起看），运行：
   ```
   python <本skill>/scripts/check_reporting.py --draft 稿件.docx
   ```
   脚本逐句列出：t、F、χ² 缺自由度，检验缺效应量，p 写成 0.000，p 值没有对应的检验统计量，声称显著却没有统计量或图表依据，间接效应缺置信区间，系数缺标准误或区间；并按稿件中出现的分析类型，列出全文都没有找到的内容（拟合指标、CR/AVE、区分效度、共同方法偏差、前提检验、多重比较校正、缺失处理、软件、样本量依据、伦理与知情同意）。
2. 脚本只给线索：统计量可能报告在表格里，"显著"可能是在转述文献。逐条回到原文核对，再按 [统计报告清单](references/reporting-checklist.md) 判断哪些确实需要补充。
3. 交付一份审查表：位置、问题、为什么重要、建议的写法（给出改后的示范句，数字只用稿件或分析结果中已有的值）。需要重新计算的项（缺效应量、缺置信区间）交给 edu-analysis 用原始数据计算，不凭已报告的值估算后当作结果写入。
4. 审查表写入 `edu_output/audit/<新任务文件夹>/`。

诚信要求见 [共同规则](../edu-shared/references/integrity.md)。
