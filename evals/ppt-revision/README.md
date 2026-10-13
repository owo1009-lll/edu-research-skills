# edu-ppt定向修订与验证

日期：2026-10-13。修订基线：[`3830434`](https://github.com/owo1009-lll/edu-research-skills/tree/383043466f067f71e2ce94e89ba5f4e0e61472c8)。本轮验收成品与来源，不以新增规则或测试数量作质量评分。名称、两条路线、四步走、两种交付模式、逐页讲稿与编辑能力保持原定位。

## 修改文件与原因

| 文件 | 修改及理由 |
|---|---|
| [check_deck.py](../../skills/edu-ppt/scripts/check_deck.py)、[fidelity.py](../../skills/edu-ppt/scripts/fidelity.py)、[objects.py](../../skills/edu-ppt/scripts/objects.py) | 用稳定ID读取原生对象，补齐内容、关系和资产核对；失败报告页码、对象、字段、预期与实际，不用整页文字命中证明忠实 |
| [build_deck.py](../../skills/edu-ppt/scripts/build_deck.py)、[plan.py](../../skills/edu-ppt/scripts/plan.py) | 分开保留区间原值和显示文字，支持参考值；检查坐标；系列使用不同颜色，折线另有不同标记；流程使用真正连接节点的箭头 |
| [计划格式](../../skills/edu-ppt/references/plan-format.md)、[生成与检查](../../skills/edu-ppt/references/production.md)、SKILL.md及中英文模块README | 说明实现范围、对象标识、精度与截断配置，区分计划一致性、来源核实和视觉查看 |
| [article-reading.md](../../skills/edu-ppt/references/article-reading.md) | 补实概念、最接近研究、方法解释和贡献比较；限定按理解需要安排，编辑过程不进入讲稿 |
| [NBO计划](../../skills/edu-ppt/examples/article-nbo/plan.json)、[来源记录](../../skills/edu-ppt/examples/article-nbo/source-notes.md)及示例README | 实际重写概念、干预、研究比较与讲稿；原文区间、主要结果、时间项和分母疑点保留 |
| [图表验证计划](../../skills/edu-ppt/examples/chart-fidelity-plan.json)、[回归测试](../../tests/test_ppt_fidelity.py)、[复现脚本](reproduce.py) | 用可编辑成品上的真实修改、删除和换标记来检验漏检，兼顾正常输出正例 |

## 反例：修改前与修改后

原始观察记录：[修改前](before-observations.json)、[修改后](after-observations.json)。没有原始来源支持的“显著提升”仅作为篡改字符串，未进入任何研究示例。

| 问题与复现方式 | 基线实际行为 | 修订后实际行为 |
|---|---|---|
| 将阶段表中“尚未实施”改成“显著提升，p < .001” | 检查通过 | 指出S04/visual/table的cell[3,1]预期与实际不同 |
| 删除整张阶段表 | 检查通过 | 报告表格对象缺失 |
| 保留数值，只替换类别或系列名称 | 检查通过 | 分别报告类别/顺序、系列名/顺序不同；另测了反转顺序 |
| 将图表单位改为另一单位 | 检查通过 | 指出unit不同；坐标百分比格式及反转方向也有回归测试 |
| 0.009 [0.004, 0.014] | 成品显示0.01 [0.00, 0.01]且检查通过 | 默认完整显示；显式请求`.2f`会因改变下限与零的关系被拒绝；负值、接近参考值1另测 |
| 数值12、8而纵轴最大5 | 生成、检查均通过 | 默认生成前拒绝；明确允许截断且有上屏说明才生成，删除说明则检查失败 |
| 两系列柱形图 | 两个系列均为176B76 | 实验/对照使用176B76与C46B16，图例对应；把颜色改相同会失败 |
| 比值区间参考值1 | 只实现参考零线，范围不含零便无参考线 | 真正绘制参考线1并显示文字；改线位置、估计点、上下限或标签可检出 |
| 引文/归属、流程文字/连接、图片 | 缺少逐对象内容核对 | 正常对象通过；改引文归属、改节点、接错连接线、删图、替换图片字节或缺生成记录会失败 |

已经具备且保留的检查：区间颠倒和超出范围、过密文字停止生成、备注改动、模板尺寸、换主题内容不变、输出目录防覆盖。原生表格本来可编辑，问题是编辑后未校验，故没有替换生成引擎。

## NBO写作前后对照

完整文本：[修改前](before-nbo-content.md)、[修改后](artifacts/nbo/content.md)、[最终讲稿](artifacts/nbo/speaker_notes.md)。逐项判断见[内容与视觉自查](review.md)。这些判断来自AI阅读，未经真实听众理解测试。

| 位置 | 原写法/缺口 | 最终处理 |
|---|---|---|
| N02概念 | 主要按报告者和测量分类，用“EAS评分”替代概念解释 | 解释情绪可得性框架、敏感性与非敌意两个维度，给出可观察表现例子，并接到录像评分；标明例子是概念说明 |
| N03动机与新增N10B比较 | 笼统提到互动研究少，缺少最接近研究的对应 | 独立读取Nicolson 2022相关正文，比较人群、照护、四个月EAS、分析与发现；说明本文补充了同次数常规访视中的自评与观察证据 |
| N06干预页 | “共同观察是干预内容，尚不是已证实的作用机制” | “护士与母亲共同观察婴儿信号，并讨论相应的回应方式。”机制限定放在N11具体解释旁 |
| N12讲稿 | 含“把这些问题集中说明……不是在每页反复否定研究” | 删除编辑过程评论，直接讲小样本、实施记录、问卷验证及表7分母疑点对解释的影响 |
| N08—N10及结尾 | 有必要限定，也有重复自我审查 | 保留自评/观察区别、全部六维区间、未调整/调整结果、问卷验证和时间项；结尾回答问题并给出“同时测量理解、信心与表现”的研究建议 |

## 运行与实际成品

可直接下载或查看：

- NBO：[PPTX](artifacts/nbo/slides.pptx)、[PDF](artifacts/nbo/preview/slides.pdf)、[联系表1](artifacts/nbo/preview/contact-01.png)、[联系表2](artifacts/nbo/preview/contact-02.png)、[检查记录](artifacts/nbo/checks.json)。15页，计划秒数合计900；不是实测15分钟。
- 路线A阶段进展：[PPTX](artifacts/progress/slides.pptx)、[PDF](artifacts/progress/preview/slides.pdf)、[联系表](artifacts/progress/preview/contact-01.png)、[检查记录](artifacts/progress/checks.json)。5页；已完成工具准备、合成试填、待实施课堂比较区分清楚。
- 图表边界：[PPTX](artifacts/charts/slides.pptx)、[PDF](artifacts/charts/preview/slides.pdf)、[联系表](artifacts/charts/preview/contact-01.png)、[检查记录](artifacts/charts/checks.json)。5页；双系列、微小区间、参考值1、非零起点折线、显式截断说明均实际生成。

三个成品共25页，均使用本机PowerPoint COM实际渲染，逐页查看PNG，并放大检查表格、区间和双系列图。修订前的14页NBO也实际渲染，作为改前内容对照；不把它计入修订后验收。render.json仍将visual_review标为not_performed，因为渲染脚本本身没有看图；AI查看记录在[review.md](review.md)，未冒充作者验收。

最终全库95项测试通过，其中PPT的21项测试也在原仓库单独重跑通过；skill-creator格式校验通过，三套已渲染成品检查通过。测试命令和完整输出：[test-results.txt](test-results.txt)。安装链接及Windows R区域设置的失败、排查与修复见[环境记录](environment-check.md)。这些数量只标明实际运行范围，不作为写作质量评分。从仓库根目录复现：

```bash
python -X utf8 -m unittest discover -s tests -p "test_ppt*.py" -v
python -X utf8 evals/ppt-revision/reproduce.py --out edu_output/ppt-revision-new
python -X utf8 skills/edu-ppt/scripts/build_deck.py --plan skills/edu-ppt/examples/article-nbo/plan.json --out edu_output/nbo-new
python -X utf8 skills/edu-ppt/scripts/render_deck.py --pptx edu_output/nbo-new/slides.pptx --out edu_output/nbo-new-preview
python -X utf8 skills/edu-ppt/scripts/check_deck.py --pptx edu_output/nbo-new/slides.pptx --plan skills/edu-ppt/examples/article-nbo/plan.json --render edu_output/nbo-new-preview --out edu_output/nbo-new-checks.json
```

要重跑基线，在另一目录检出3830434，再把`reproduce.py --scripts`指向该检出的skills/edu-ppt/scripts。复现脚本是公共合成输入，不依赖开发者本机文件。已存成品可直接用其旁plan.json、build.json和preview核对；NBO图片资产亦随成品附上，许可与归属见[示例README](../../skills/edu-ppt/examples/article-nbo/README.md)。归档文本统一LF换行，build.json中的输出哈希对应归档文件；PPTX、PDF和PNG字节未改动。生成日期等元数据可能使重新生成的PPTX二进制哈希不同，应核对对应计划和本次渲染记录。

## 范围与剩余限制

- 自动通过证明与已核实计划一致；报告中的source_fact_check仍是not_performed。事实核实依据在公开来源记录，不能靠脚本对计划的一致性代替。
- 仅支持当前六类visual对象；普通图为column/bar/line，区间仅线性尺度，参考值必须在显示范围内。流程只表达顺序关系，不声称能检查任意分支网络。
- 新检查依赖生成对象ID，旧成品应按旧计划重新生成。它不是对任意手制PPT或故意同步篡改计划、记录和成品的防伪工具。
- 本轮视觉检查环境为Windows PowerPoint。其他Office/LibreOffice版本、缺字环境、灰度投影和真实观众可读性尚未验收；颜色不同的自动判定不等于色觉无障碍认证。
- NBO附录原图的内部文字较小，用于会后放大核对，主讲人数已经重画为可读流程。原文表7分母疑点仍未解决；没有擅自修正原文或移除相关结果。
- 没有真实听众测试、作者审定或实际计时排练，不能声称讲述效果已被实证验证。全部公开材料来自许可文章或明确合成材料，未加入用户私有稿件。
