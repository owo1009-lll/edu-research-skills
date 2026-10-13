# 生成、模板与检查

## 依赖与命令

Python 3.9+。先用当前环境检查依赖；缺失时安装 `python -m pip install -r <本skill>/requirements.txt`。阅读、组织和内部计划由宿主AI完成，本地脚本不调用模型服务。

```bash
python <本skill>/scripts/extract_source.py --source paper.pdf --out <任务>/source
python <本skill>/scripts/build_deck.py --plan <任务>/plan.json --out <任务>/content --content-only
python <本skill>/scripts/build_deck.py --plan <任务>/plan.json --out <任务>/deck
python <本skill>/scripts/render_deck.py --pptx <任务>/deck/slides.pptx --out <任务>/preview
python <本skill>/scripts/check_deck.py --pptx <任务>/deck/slides.pptx --plan <任务>/plan.json --render <任务>/preview --out <任务>/checks.json
```

每个out使用新目录。内容模式交付content.md和speaker_notes.md；成品增加slides.pptx，预览目录有逐页PNG、PDF、联系表和render.json。用户得到这些文件，不需要自己运行内部JSON流程。

## 模板适配

先运行 `scripts/inspect_template.py 模板.pptx --out <任务>/template.json`，并渲染原模板查看实际样式。生成时加 `--template 模板.pptx --theme <任务>/theme.json`。保留模板页面尺寸、母版、布局及母版内标识；去掉示例幻灯片，生成新页面。样例页专有装饰不属于母版，不自动沿用，助理需要选择保留为独立对象或说明差别。

theme.json可指定font、accent、ink、muted、light、background（六位十六进制色值），title_size、body_size、footer_size，以及layout名称。`canvas=[左,上,宽,高]`用页面尺寸的比例表示内容区；默认`[0.055,0.235,0.89,0.64]`。模板不传background时继承背景。正文位置仍需根据标识、页眉和页脚调整并渲染查看，不能只以加载模板成功声称适配完成。

默认正文22pt、标题28pt、来源11pt；字体默认Microsoft YaHei。Linux等没有该字体的环境选已安装的中文字体，如Noto Sans CJK SC，并重新检查。脚本不打包字体。字号不足以容纳内容时先缩写、拆页或调整布局；生成器在估计超容时停止并指出页码，不自动把正文越缩越小。

## 实际渲染

Windows优先使用本机PowerPoint和pywin32，独立COM实例、不开演示文稿窗口；需要已安装可用的PowerPoint。其他环境用LibreOffice和Poppler的pdftoppm；macOS可使用这些工具。自动模式找不到可用渲染器时失败并留记录，不把python-pptx保存成功当作渲染成功。

render.json中`status=rendered`只证明文件被实际渲染，`visual_review=not_performed`提醒仍需看图。依次查看联系表和每页，放大统计表、原图和长引文：检查溢出遮挡、字体替换、中英显示、图表清晰度、单位、正负号、β/上下标/区间、来源可读性，以及页面和讲稿是否一致。原PDF表格和扫描识别结果回原图对照。

check_deck.py按稳定对象ID核对[计划格式](plan-format.md)中的原生内容、图表坐标与区间显示，并检查越界、主要对象重叠和预览哈希。每项不一致报告页码、对象、预期和实际。通过表示成品与计划一致；事实正确性需对照来源。它不能识别所有字体替换、复杂表格溢出或事实错误，不是质量总分。计划seconds是分配时间，不是实际试讲时长。

## 定点修复与交付

在visual-review.md记录检查者身份（AI自查/作者反馈）、页面与具体问题、修正、重新检查结果。不为让检查通过删除关键条件。样式修复只动theme或布局；内容修复动plan并重新核对对应来源。重新生成到新目录并渲染，旧目录保留便于对照。

交付时说明哪些对象可编辑；原文图片内部不可编辑。对无法读取的补充材料、仅摘要范围和渲染失败如实说明。用户材料不得写入公开示例；公开示例使用明确许可的材料或注明合成。
