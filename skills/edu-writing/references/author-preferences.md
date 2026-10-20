# 作者写作偏好

用户可以直接说“记住我的讨论写法”“这次不要弱化这句话”“以后先写判断再解释”“你记住了哪些偏好”“撤销刚才记住的偏好”。由助理调用 `../scripts/author_preferences.py`，不让用户准备配置。这里只保存并在后续任务调用偏好，不称为训练模型。

## 记录与范围

只读取本次指定稿件、明确关联材料和用户授权的个人档案。项目记录在 `<项目>/edu_output/project/preferences.json`；个人档案使用用户授权的仓库外路径。用户明确要求长期记住且未指定路径时，可在其当前工作根目录旁的个人资料目录建立 `author-preferences.json`，告知保存位置；已有授权路径继续使用。不遍历其他项目寻找偏好。公开 skill 工作树及安装目录不能保存这些状态。

来源分三类：

- `explicit`：用户实际说过的话；“这次”仅为任务范围，“这篇”是项目范围，“以后都这样／记住这个习惯”是跨项目授权，不重复确认。
- `choice`：用户明确取舍之后保存原文、建议、最终选择、用户回应和已说明的理由。没有回应、下载或继续任务均不算接受；拒绝某次修改也不自动推出普遍禁令。
- `example`：用户提供的认可示范，标明 `ownership=author|other`。只提取论证、表达特点和必要短例；别人的独特措辞不迁入用户稿件。推断保留为项目候选，多次类似取舍也不冒充确认。

事实、样本量、量表含义、设计和研究结论不放入偏好。用户要求保留概念框架可以记录为表达约束；该概念在本项目的实际定义保存在[项目材料记录](../../edu-research/references/material-updates.md)，不跨论文推广定义。

## 内部请求接口

调用：`python <本skill>/scripts/author_preferences.py --project <项目> [--profile <授权的个人档案>]`，用 UTF-8 标准输入传 JSON。不要为真实偏好另存命令全文、请求副本或含例句的调试日志。

新增示例（合成用户话语）：

```json
{
  "action": "add",
  "scope": "project",
  "item": {
    "category": "expression",
    "content": "英文讨论先给出有依据的判断，再展开材料。",
    "scope": "project",
    "basis": "explicit",
    "status": "active",
    "languages": ["en"],
    "research_types": ["mixed"],
    "sections": ["discussion"],
    "tasks": ["new", "revise"],
    "conditions": ["判断得到本研究或明确的专业依据支持"],
    "exceptions": ["不把关联写成因果"],
    "source": {
      "kind": "explicit",
      "evidence": "这篇英文讨论先写我的判断，再解释。",
      "time": "2026-10-20",
      "example": "Access should be equitable; the two strands identify different barriers."
    }
  }
}
```

任务范围加 `task_id`。作者范围将两处 scope 改为 `author`，提供授权的 `--profile`，并在 source 写 `cross_project_authorization` 的实际话语。推断记录用 `basis=inferred,status=candidate,scope=project`。各筛选维度必须明确；`["*"]` 只用于实际适用的宽范围。

取舍来源另含 `decision=accept|reject|select`、`original`、`suggestion`、`selected`、`user_response`，有理由时写 `reason`。脚本核对字段和状态，不证明用户真的说过这些话；助理必须按对话原意记录。

## 加载与冲突

`action=load` 的 `context` 含 `language,research_type,section,task,task_id`。筛选只返回相关有效项；候选放在独立字段中，不自动驱动大幅改写。项目没有记录也可直接写作，不要求用户先建档。

当前明确要求优先。逐项判断具体冲突，事实和证据边界不能被偏好覆盖；项目约束与已核实期刊硬要求发生冲突时只作必要处理。可用 `current_requirements` 保留本次要求，`conflicts=[{preference_id,priority,reason}]` 排除有具体冲突的旧项；priority 为 `current_request|fact|evidence|project|verified_journal`。语义冲突由助理判断，脚本不声称自动读懂。条件和例外同样需要阅读后应用。

有效论证可不修改。写作结果仍直接交付正文，不附偏好清单；只有重要冲突、关键未确认推断或用户询问时简短说明。不要通过统一改用 could、删除反例或隐藏不确定性来模拟作者风格。

## 管理与真正删除

- 查看：`{"action":"list"}`；只查看授权的项目／个人档案。
- 暂停／恢复：`{"action":"update","id":"…","changes":{"status":"paused"}}` 或 `active`。上述是项目项；个人项的所有 update/delete/undo_add 请求都要加 `"scope":"author"`，同时传 `--profile`。指定档案路径不意味着把项目操作隐式改为个人操作。
- 修订内容、筛选条件、来源、例外：同一 update 的 changes；确认候选时补实际确认来源并改 `basis=explicit,status=active`。
- 改成只用于本项目：先按用户要求加入项目档案，成功后删除个人项；反向提升须有长期授权。不要留下两个同时有效的冲突副本。
- 项目停用个人档案：`{"action":"personal","enabled":false}`；不删除个人档案，不影响其他项目。
- 删除／撤销刚才新增：`{"action":"delete","id":"…"}` 或 `undo_add`。个人项同时指定 `scope=author` 和档案路径。脚本物理移除该项、来源和内嵌短例，不保存隐藏文本历史；反复删除仍安全。

用户说“撤销”时按实际刚执行的操作处理：撤销新增即删除；撤销停用可恢复；内容修改的旧版本不在隐藏记录中保存，有对话依据时按其恢复，否则只问必要的缺失内容。系统无法清除用户另行备份、聊天服务历史或原始示范文章；不得声称已删除这些外部副本，也不要自行删除原稿。
