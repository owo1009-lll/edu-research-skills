# 收窄组合的原始运行

`runs/` 已保存 H6/H7 的两次 p/r 运行，共八份原始运行，包括首稿、自查、终稿、修改理由、读取记录与检查输出。归档不改写正文，按字节核对并列入 [manifest.json](manifest.json)。

重做相同任务时，解压 [p01 基线](../development-artifacts/dev-p01-skills.zip) 和 [r01 候选](../development-artifacts/scoped-r01-skills.zip) 到两个独立目录，使用 [公开任务材料](../inputs) 及 [派发原文](../scoped-dispatch.json)。替换记录中的本机根目录即可，不需要作者私有稿件；模型输出不保证相同。`edu-writing-snapshot-p01-20261018`/`edu-writing-snapshot-r01-20261018` 对应技能解压根，`edu_output/writing-20261018/scoped-runs/<运行>` 对应本目录的 `runs/<运行>`。

匿名比较使用 `make_blind.py --stage holdout --arms p r`，并指定新输出目录、目录外的键、H6 或 H7 和重复序号。正文逐字节复制，键在评阅保存前不向评阅者提供。评阅者仅见 [评阅协议](../holdout-judge-request.md)、本组请求、材料和 A/B。实际协议、快照散列与冻结先后关系见 [输入冻结](../scoped-input-freeze.json) 和 [规则冻结](../scoped-freeze.json)。

H7 的真实原文及其改写遵循材料中的 CC BY 4.0 署名与许可，不代表 Otaki 等作者认可。H6 为事实包基础上的新写练习。所有稿件均为 AI 产出，检查脚本不证明写作质量或原始数据正确；没有真人评价。
