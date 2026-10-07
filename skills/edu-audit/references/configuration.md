# 配置

完整可运行示例位于此技能的 `examples/`。复制到自己的项目文件夹后在该文件夹运行（`--workspace` 默认为当前目录）。JSON 路径均相对工作目录，结果写入 `edu_output/audit/`。

`case_id`, `mode`, `evidence_status`, `input`, `source_results` 必填。`summary_counts` 要求 `outcome_definition`，输入表为group,failed,passed且组为intervention/control。原结果表为key,original,digits,comparison,source_location；comparison仅exact或rounded。

`descriptive_repeated` 要求id_column,group_column,groups,variables,na_strings,scale_min,scale_max,missing_policy,collapse,sd_denominator,scoring,standardization,sample_selection,interval_algorithm。可执行选项仅 available_case_per_variable / require_invariant_then_unique / n-1；其他设置应先开发适配，不能悄然回退。

0.2补充：配置中的说明不能为空，尺度上下限须明确，standardization仅支持none。可选expected_participants_by_group为组名到正整数人数的映射，必须覆盖全部配置组别；不一致则停止并保存失败。它是来源声明的校核，不是自动证明样本正确。每次成功描述复算输出逐组逐变量missingness.csv；空source_results拒绝运行。

每次运行新建时间戳目录；可在该目录用 `Rscript --vanilla recheck.R --config analysis_config.json --out second_output` 重跑，已有目录拒绝覆盖。未安装R保存not_executed；运行失败保存failed，保留stderr。
