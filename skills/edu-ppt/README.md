# edu-ppt

[English](README_EN.md)

把自己的研究或阅读的文章整理成可讲清的学术汇报。

## 用法

- “把我的论文做成15分钟组会汇报。”
- “根据我的研究进展做PPT，保留未完成事项。”
- “解读这篇英文论文，生成中文汇报PPT。”
- “围绕婴幼儿情绪社会性发展找文章，按四步走生成逐页内容和讲稿。”
- “按这个模板生成可编辑PPT。”

## 产出

内容模式：实际逐页文字、图表安排、逐页讲稿、来源位置和时间。成品模式另有可编辑PPTX、演讲者备注、PNG/PDF预览及检查记录。自己的研究区分完成、方案与进展；他人文章按问题、动机、设计、发现组织。

## 依赖与边界

Python依赖见requirements.txt；生成引擎python-pptx，不需要额外模型API密钥。渲染需Windows PowerPoint，或LibreOffice与pdftoppm。没有渲染器不宣称完成视觉验收。文本、表格、模型和重建图表为原生对象；文章图片内部不可编辑。只见摘要时不假装全文阅读，不新增分析，不补造研究进度。

详见[入口](SKILL.md)、[生成命令](references/production.md)、[参考项目](references/open-source.md)及[合成与开放文章示例](examples/README.md)。任务材料存用户项目edu_output/ppt，不能放进技能目录。

## 状态

- Beta：新模块；具体自动检查、AI自查及场景验证范围由开发仓库evals记录，不视为作者或专家验收。
