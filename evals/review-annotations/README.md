# 原稿高亮与原生批注验证

基线 `684f5e435b76daf8d0109c9c6a93297542c59889`。本目录只含新编公开软件测试稿，没有真实研究数据、用户私稿或真实受访者材料。测试稿的引文字段和图表也是功能样例，不能引用为研究发现。这里的开发记录不属于日常审稿交付；日常只交付原稿标注版。

## 实际文件

- Word：[原稿](examples/synthetic_manuscript.docx)、[审稿标注版](examples/synthetic_manuscript_审稿标注版.docx)、[内部标注计划](examples/docx-plan.json)。新增 4 条批注，正文和表格均有精确锚点。
- PDF：[原稿](examples/synthetic_manuscript.pdf)、[审稿标注版](examples/synthetic_manuscript_审稿标注版.pdf)、[内部标注计划](examples/pdf-plan.json)。新增 3 个携带评论正文的高亮注释。
- [文件保留核对](examples/verification.json)；[Word 16.0 实际打开记录](word-checked/word-open.json)包含逐条评论作者、原文范围、内容和颜色，以及原有对象数量。
- Word 的[高亮预览](word-checked/synthetic_manuscript_审稿标注版_highlights.pdf)与[批注气泡预览](word-checked/synthetic_manuscript_审稿标注版_word-preview.pdf)来自实际 Word 导出，原件对应预览也在同目录。每份均一页，已经查看。

Word 打开前后都识别到：原有批注 1 条、修订 2 处、引文字段 1 个、表格 1 张、内嵌图片 1 张。新增评论的作者为“AI 模拟审稿”，原作者评论及绿色高亮保留。正文最终视图的文字一致，文件包中的删除/插入修订和域未接受、拒绝或展开。

## 针对性验证

| 场景 | 核对方式及结果 |
|---|---|
| 原稿正文、表格、格式、图、引文、原批注与修订保留 | Word 文件包比较＋去除新增标记后核对结构/样式＋实际 Word 打开；通过 |
| 同文多处出现数字，跨格式文字 run | 用段落/行地址、范围、原文及文件/单元哈希定位；批注落在指定位置，没有取全文首次匹配 |
| 计划与稿件不一致 | 错误 quote 或来源哈希拒绝，且不留下半成品 |
| 新批注相互重叠 | 拒绝生成，要求合并成主要颜色的一条评论 |
| 域内部等尚不支持的锚点 | 明确拒绝，不拆坏字段；域及修订位于其他位置时完整保留 |
| 故意改坏 Word 的表格数值、删除修订内容、旧评论或图片字节 | 核对失败；正常稿通过 |
| PDF 重复文字、旋转文字及跨行范围 | 原生高亮坐标逐项对应原文字形；通过 |
| 故意改 PDF 评论、正文或把高亮变为不可见 | 核对失败；原页面对象/内容流和已有注释需保持 |
| 无问题稿件、已有输出 | 零条批注正常通过；原稿及已有文件均拒绝覆盖 |

测试输出：[契约与链接](check-1.txt)、[原生标注及既有审稿/回复检查](check-2.txt)、[PPT 回归](check-3.txt)、[期刊检索回归](check-4.txt)。统计分析代码未修改，尚未在本轮重跑全部 R 分析；这些功能测试也不证明 AI 审稿判断已达到真人水平。

## 发现并修复的问题

1. PDF 透明高亮会影响渲染器的抗锯齿路径，即使设置不画注释，部分像素也出现 1–2 级变化。未放宽为任意像素容差：检查器先严格比对原有对象/流，再在隔离副本移除注释数组比较原页面渲染。输出 PDF 保留原生注释。
2. 最初的 Word 自动检查停滞；实际 Word 实例可响应并识别源文件，停止该检查后改用带进度输出的 Python COM 调用。原稿与标注稿的修订视图需显式一致，否则 Range.Text 会随当前视图变化。现在两个文件按相同最终视图读取，不接受/拒绝修订。
3. Word 导出会刷新未锁定域，使测试稿的占位 REF 变成错误提示。最终预览在只读且不保存的打开副本中临时锁域，保留原有显示值；实际 DOCX 不变。带批注导出的结构标签还触发过 MuPDF 警告，最终开发预览关闭这项标签，未修改源文档。
4. 人工读取功能样例时发现一条“分析计划时间”评论原先锚到同段人数。现改为精确锚到计划时间短语并重新生成、实际打开及渲染。脚本能核对计划一致性，不能代替这项语义判断。

Word 在批注气泡视图可能按评论作者覆盖范围底色，因此同时导出高亮与气泡两种视图检查；原生红/黄/蓝颜色通过 Word 的 HighlightColorIndex 再核对。原生蓝色较深，批注开头仍有文字性质标识，颜色不是唯一辨识方式。未声称跨所有 Office/PDF 查看器均完成视觉验证。

## 复现

```powershell
python -m pip install -r evals/review-annotations/requirements.txt
python -X utf8 evals/review-annotations/create_fixture.py --output <新的示例目录>
python -X utf8 -m unittest discover -s tests -p 'test_review*.py' -v
```

Windows 安装 Word 和 pywin32 时，另运行：

```powershell
python -X utf8 evals/review-annotations/check_word.py --examples <示例目录> --output <新的预览目录>
```

核心标注不依赖 Word COM。手工打开原生文件后，可逐一点击高亮查看评论。实际能力边界见 [锚点说明](../../skills/edu-review/references/annotations.md)：尚未支持 Word 页眉/脚注/域/修订内部的自动精确锚定、扫描 PDF OCR 锚定或签名文档修改。

实现参考：[python-docx 原生评论说明](https://python-docx.readthedocs.io/en/latest/user/comments.html)、[PyMuPDF 页面注释接口](https://pymupdf.readthedocs.io/en/latest/page.html#Page.add_highlight_annot)、[Word 高亮显示设置](https://learn.microsoft.com/office/vba/api/word.view.showhighlight)。这些接口文档不构成审稿质量依据。
