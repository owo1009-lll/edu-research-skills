---
name: edu-shared
description: Support files shared by the other edu-* skills (the R runner that records every analysis, and the common integrity rules). Not a task skill - do not select it for a user request; the edu-* skills read it through ../edu-shared/ when they need it.
---

# 共用支持包

这个包不单独处理任务，供其他 edu-* skill 引用：

- `scripts/edu_runtime.py`：查找 Rscript，在 `./edu_output/` 下新建运行文件夹，运行 R 并记录脚本、输入指纹、R 环境和日志（edu-analysis、edu-audit 使用）。
- `references/integrity.md`：所有模块共用的红线和输出位置约定。

安装任何 edu-* skill 时都要把这个文件夹一起装在同一个 skills 目录下。
