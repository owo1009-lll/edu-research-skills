# 文件式写作任务包装

以下为开发后段运行与最终留出可复用的派发格式。仅替换 `{SKILL_ROOT}`、`{TASK}`、`{INPUTS}` 和 `{OUT}`；同一任务各版本使用同一份请求和材料。最终留出使用中性技能目录名，不把 baseline/candidate 或预期胜负写给写作者。

```text
Complete one independent writing task. Read only the supplied skill at {SKILL_ROOT}/skills/edu-writing/SKILL.md and its task-relevant referenced resources, plus {INPUTS}/{TASK}-request.md and {TASK}-materials.md. Execute that request directly. Save outputs ONLY in a new directory {OUT}/. Use UTF-8 for all reads/writes and python -X utf8 for checks. Do not inspect other runs, repository evaluation/development reports, or any other installed skill. No network, no subagents, no edits to skills or inputs. Read relevant skill instructions, write first/review/final/rationale/loads.json as requested, plus change_log.md for revision tasks. Run applicable check scripts on first and final and inspect outputs. Maintain a list of actual file reads and reasons; model identity/settings only if genuinely visible, otherwise report unavailable. Report files completed and limitations. You are a writer, not a comparative evaluator.
```

模型继承同一宿主配置，不显式覆盖；记录能看见的配置，无法获知的后端版本、温度或随机种子不猜测。模板不保证跨时刻的模型实现完全一致或输出确定。
