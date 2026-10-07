# 运行环境

- **Python 3.9 及以上**：所有脚本只用标准库；生成 Word 和图表需要 python-docx 与 matplotlib（见 edu-writing 的 `requirements.txt`，安装前先征得用户同意）。
- **R 4.1 及以上**：只有统计分析和结果复核需要。`edu-shared/scripts/edu_runtime.py` 依次查找参数 `--rscript`、环境变量 `EDU_RSCRIPT`、PATH 和常见安装位置。缺少的 R 包用 `Rscript edu-analysis/scripts/setup_packages.R` 安装到 R 的用户库。
- **工作目录**：在用户的论文或项目文件夹里运行。产出写入 `./edu_output/`，每次运行新建子文件夹，失败的运行也保留；不同任务互不覆盖。
- **恢复任务**：中断后读取 `edu_output/` 里最近的任务文件夹（`run_status.json`、写作任务的 `rationale.md` 和首稿）继续，不需要用户重复材料。
- **安装位置**：Claude Code 为 `~/.claude/skills/`，Codex 为 `~/.codex/skills/`。各 skill 与 `edu-shared` 放在同一目录下，互相用相对路径引用。
