# 测试环境与失败修复

本轮在Windows、Python与PowerPoint桌面版上运行。PPT检查本身不依赖Office；实际渲染使用PowerPoint COM。

完整测试首次运行有两项失败：

1. 新增报告的相对链接指向仓库的evals目录，而单独安装技能时不包含该目录。四处技能文档链接已改为公开仓库URL，安装后链接检查恢复通过。
2. `test_modules.Analysis.test_known_answers`因环境继承`LANG/LC_ALL/LC_CTYPE=C.UTF-8`失败。Windows R 4.6.1报告无法设置该区域配置，并退回C locale；中文路径和R源码中的中文均解析失败。复制同样字节到ASCII路径后仍失败，因此问题不只在路径。

只对子进程移除LANG、LANGUAGE与LC_*覆盖值，R实际报告`Chinese (Simplified)_China.utf8`、`l10n_info()[["UTF-8"]]=TRUE`。随后在原仓库路径重跑完整测试；未修改系统设置、R分析代码或已知答案。实际命令、数量及退出状态以[test-results.txt](test-results.txt)为准。

遇到同一Windows环境问题，可从仓库根目录用下列Python入口运行；它仅改变所启动测试进程的环境：

```python
import os
import subprocess
import sys

env = {key: value for key, value in os.environ.items()
       if key not in ("LANG", "LANGUAGE") and not key.startswith("LC_")}
subprocess.run([sys.executable, "-X", "utf8", "-m", "unittest",
                "discover", "-s", "tests", "-v"], env=env, check=True)
```

这不是所有平台通用的环境修改建议，也不应把未运行的R检查记为通过。
