# 开源参考与采用理由

核对日期：2026-10-13。读取默认分支的下列提交，另核对依赖和LICENSE。这里记录被读取的精确快照，不声称未来仍为最新版。

| 项目 | 核对版本/提交 | 许可 | 采用与未引入部分 |
|---|---|---|---|
| [HKUDS/Paper2Slides](https://github.com/HKUDS/Paper2Slides/tree/0785051d1f52814097e94c44751e3f12b83f7c8a) | 0785051 | MIT，HKUDS | 借鉴解析、总结、页面计划、生成分阶段和检查点复用。其依赖包含MinerU、LightRAG、OpenAI客户端、FastAPI；本技能不引入RAG/Web服务或图像生成密钥 |
| [celestial-micha/paper2ppt](https://github.com/celestial-micha/paper2ppt/tree/fc8a91495346d29dfb72df35fbefb5832d6d99e6) | fc8a914 | MIT；该快照LICENSE署名HKUDS | 借鉴内容计划与原生PPT分离、讲稿、几何检查及失败页面定点修复。其依赖含python-pptx、LangGraph、LangChain/OpenAI；不引入模型调用和大型评测框架 |
| [PptxGenJS](https://github.com/gitbrent/PptxGenJS/tree/3c9ec1b687c174952166f6a34b5e87ebf69fa469) | package 4.0.1，3c9ec1b | MIT，Brent Ely | 核对addNotes、addChart、addTable，支持原生PPT路线；现有仓库以Python为主，因此不再维护Node引擎。依赖包括jszip、image-size |
| [python-pptx](https://github.com/scanny/python-pptx/tree/278b47b1dedd5b46ee84c286e77cdfb0bf4594be) | 源码278b47b；本机验证1.0.2 | MIT，Steve Canny | 选为唯一生成引擎；使用公开的文本、表格、图表、图片与notes_text_frame接口。依赖Pillow、XlsxWriter、lxml、typing_extensions；自身不负责PowerPoint渲染 |

本技能代码独立编写，未复制以上项目的实现。python-pptx等作为外部依赖安装，各自保留原发行包中的许可证和署名。模板样例页移除使用python-pptx的底层幻灯片关系列表，属于需要往返测试的兼容点；不据此声称完整保留任意复杂模板。

## 运行依赖与许可范围

生成：python-pptx（MIT）、Pillow（HPND/MIT-CMU）、python-docx（MIT）；PDF提取：pypdf（BSD-3-Clause）；公网元数据：requests（Apache-2.0）。Windows渲染用pywin32（PSF）控制用户已有PowerPoint（专有软件，非捆绑）；可选LibreOffice（MPL/LGPL）与Poppler（GPL）作为外部命令。不随技能分发这些软件、字体或文章全文。

正常内容阅读与结构化由宿主AI完成，本地基本流程不要求新申请模型API密钥。源图和文章另按其许可及用户使用范围处理，软件MIT许可不授权转载文章。
