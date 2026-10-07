# skills/

这里是各 skill 的源文件，也是唯一需要编辑的地方。安装副本由 `scripts/install.py` 生成，不要直接改安装目录里的文件（安装器发现被改过的副本会拒绝覆盖）。

- `release.json`：版本号和要安装的目录列表。
- 每个 `edu-*` 目录是一个 skill（`SKILL.md` 加 `references/`、`scripts/`、`tests/`、`examples/`）；`edu-shared` 没有 `SKILL.md`，供其他 skill 通过 `../edu-shared/` 引用。
- 修改后运行 `python -m unittest discover tests`，再用 `python scripts/install.py --action update` 更新安装副本。
