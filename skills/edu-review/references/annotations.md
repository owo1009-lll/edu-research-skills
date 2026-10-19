# 文件与锚点

在用户项目的新任务目录操作。依赖见本 skill 的 `requirements.txt`：python-docx、lxml、PyMuPDF。脚本直接编辑 Word 文件包、增量保存 PDF；不会先重排整篇稿件。原稿和已有输出不覆盖。

## 操作

```powershell
python -X utf8 <本skill>/scripts/annotate_manuscript.py inventory 原稿.docx --output anchors.json
python -X utf8 <本skill>/scripts/annotate_manuscript.py apply 原稿.docx --plan annotations.json --output 原稿_审稿标注版.docx
python -X utf8 <本skill>/scripts/annotate_manuscript.py verify 原稿.docx 原稿_审稿标注版.docx --plan annotations.json
```

PDF 用相同命令及 `.pdf` 扩展名。未给 `--output` 时自动在原稿旁输出“原稿名_审稿标注版”。实际工作优先显式放入 `edu_output/review/<新任务文件夹>/`。

`anchors.json` 只用于定位，不是审稿判断。助理读原稿和材料后整理 `annotations.json`，不让用户填写技术字段：

```json
{
  "schema_version": 1,
  "source_sha256": "从inventory复制",
  "created_utc": "填写本次实际UTC时间",
  "annotations": [{
    "id": "C1",
    "kind": "error",
    "severity": "major",
    "comment": "这里的样本量与方法部分不同。请对照原始记录核实；当前只确认稿内矛盾。",
    "anchors": [{
      "part": "word/document.xml",
      "paragraph": 3,
      "text_sha256": "该段inventory中的哈希",
      "start": 8,
      "end": 10,
      "quote": "52"
    }]
  }]
}
```

数值仅演示格式，不是可套用的原文位置。索引为 **0 起始**，字符范围左闭右开，Word 段落包含表格内段落。`quote` 必须等于该段对应范围；先核对原文再生成，不靠全文搜索第一处同名句子。

- `kind`：`improvement` 黄色、`error` 红色、`verify` 蓝色。`severity` 可省略，或 `major`/`minor`。批注自动加中文性质、可选严重程度和 ID，作者为“AI 模拟审稿”；正文内容不插入标签。
- Word 每条批注对应一个段落内范围，可跨普通文字 run（例如局部加粗）。跨章节意见在批注文字中给位置与 ID，不扩大高亮到整篇。
- PDF 锚点用 `page`（1 起始）、`line`（0 起始）、`text_sha256`、`start`、`end`、`quote`；字段从 inventory 的对应行取。一个批注可有同一页多行锚点；脚本支持旋转文字。跨页采用相关批注并互相指向。
- 同一位置的新标注重叠会拒绝生成。先合并为主要颜色的一条意见，再在评论中解释不同问题。零批注可正常输出，不需为了通过检查制造问题。

## 保留与验证范围

Word 仅增加所需原生高亮、批注及关联。检查器比较预期文件包，并在去除新增标记后归一化文字 run 的拆分，再核对正文结构和样式；其他图片、引文字段、已有批注和修订部件保留。PDF 核对原有对象及内容流，仅允许页注释列表增加；核对原有注释、新批注和字符坐标，并在隔离副本中移除注释数组后比较每页渲染。两者均可发现计划外的文本、数据或对象变动。

这些检查验证**原件保留和标注计划一致性**，不证明评论判断正确。需另读评论与来源，实际打开交付文件。Word 可用 `../edu-writing/scripts/render_word.ps1` 渲染正文及高亮；评论内容和精确范围还应在 Word 中检查，或使用带批注的导出方式。缺少 Word/LibreOffice 时明确尚未完成实际打开或视觉检查。

## 明确限制

- 当前 Word 自动锚定限主文/表格中的普通文字。已有超链接、域、图片、修订、文本框保持不变；直接锚定其内部或跨越非文字对象会拒绝，不擅自拆开。可在紧邻且能明确指认问题的普通文字处批注并注明对象；没有准确替代锚点时说明该处尚未标注。页眉、脚注、文本框和修订中的目标不宣称已覆盖。
- 已有高亮的位置不覆盖；新问题可在邻近精确位置批注关联。数字签名文档不修改，避免声称签名仍有效。
- PDF 需要可提取文字层。扫描件未实现 OCR 锚定，不把坐标猜测当作精确文字定位；加密或签名 PDF 需可处理的工作副本。PDF 高亮本身携带作者和批注内容，查看器点击高亮即可读到，不要求正文另外出现文字框。
- 生成失败会给出具体对象及位置，不交付半成品。不把普通文本报告当成已完成的原生批注。

旧 `check_review.py` 与 `report-format.md` 仅保留历史报告兼容，不属于默认流程。
