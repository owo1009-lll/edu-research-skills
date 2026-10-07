# 反思性主题分析与可恢复记录

选择语义与情境层面、问题导向的反思性主题分析，允许研究问题和解释视角影响编码，反思其选择偏向。原文与主题之间是解释关系，追溯校验能防错引，不能证明解释唯一正确。阶段可以递归返工，参考[Braun与Clarke原始团队的流程说明](https://www.thematicanalysis.net/doing-reflexive-ta/)。

## 材料准备

助理从原格式提取到内部CSV，字段`document_id,speaker,text,source_locator`。speaker为participant/observer/interviewer/context/ambiguous。受访者原话使用participant；观察者描述使用observer，赋码必须显式evidence_kind=observation_note，导出始终保留观察者身份，不作为受访者直接引语。观察时间、地点、观察者位置依原材料记录，缺失不补造。其他说话人保留情境；含糊归属不得猜定。脚本支持访谈、开放回答及明确来源的观察笔记。

定位可以是原PDF页/段、逐字稿行或解析TXT行；说清是哪种定位。保存原始与解析哈希、转换版本、阅读顺序检查及未核对音频状态。不要为了匿名化改写观点；映射置私有目录，保留哪些字符被替换。

```powershell
python <本skill>/scripts/theme_analysis.py prepare --input edu_output/private/<内部CSV> --redactions edu_output/private/<映射JSON> --output edu_output/private/<新准备目录>
```

显式替换只实现所列字符串替换，不承诺自动发现全部隐私。段ID按输入哈希与行序生成，保留原文本哈希与准确定位。修改原材料需重新prepare，不能在已有准备目录中覆写。

## 熟悉、编码与原文复查

先全读所选文档并写`document_memos`，说明样本/视角、反向材料、疑义、分析者偏向，不能仅看摘录再宣称全读。大型库可先选范围，说明为什么、哪些未读。

内部 annotation 的格式见本 skill 的虚构示例 `examples/synthetic_annotation.json`（配套 `examples/synthetic_interviews.csv`、`examples/synthetic_redactions.json`，可以直接跑通 prepare 和 commit）：

- question、approach（精确值见例）、memo、document_memos、change_reason、unresolved。
- codes：id,label,definition,include,exclude,category。
- assignments：唯一id、code、segment、excerpt、role（support/counterexample/context/alternative）、interpretation；观察笔记另需evidence_kind=observation_note，受访者为participant_statement。excerpt必须为匿名后原段精确子串；翻译另存，不能拿意译冒充直接引文。
- themes：id,name,central_idea,status=candidate_AI_assisted、support/counterexamples赋码ID、counterexample_review、alternative_explanation、boundary。没有找到明确反例可保存空列表，但必须说明检查范围与结果；不得凑造反例。

脚本不强迫所有文本赋码；coverage分别列出参与者与观察笔记段、已编码段与未编码ID，区分“全文熟悉”与“赋码覆盖”。编码本不是预先固定的普遍测量工具，类别与主题可以合并、拆分或重新命名。

## 修订后继续

```powershell
python <本skill>/scripts/theme_analysis.py commit --prepared edu_output/private/<准备目录> --annotation edu_output/private/<内部分析JSON> --actor AI_assistant
# 下一次使用latest.json中的revision为parent；研究者实际编辑才选researcher
python <本skill>/scripts/theme_analysis.py commit --prepared edu_output/private/<准备目录> --annotation edu_output/private/<修改后JSON> --parent <前版本ID> --actor researcher
```

每次新建不可覆写revision：analysis/history/evidence/coverage/themes，父版本与前后内容哈希并存。旧parent拒绝，伪造引文拒绝，来源或准备后文本变更拒绝。脚本不能认证actor的人类身份；记录应依实际来源选择。模拟研究者编辑只用于独立测试。

主题以中心解释组织，引用必要短片段和位置，用反例说明边界、用替代解释暴露未决部分；不按编码次数排重要性，不宣称人工双盲、一致性或饱和。结果正文与追溯附录分开，分析者可以提出新解释，但要说明如何从材料推到解释。
