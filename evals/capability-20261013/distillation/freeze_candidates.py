"""Rebuild the two text-skill arms; holdout sources are deliberately not read here."""
from pathlib import Path
import datetime
import difflib
import hashlib
import json
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = '08aa93320c356b75fd0f6bfc61b5df02f98e2682'


def digest_tree(root):
    rows = [(str(p.relative_to(root)).replace('\\', '/'), hashlib.sha256(p.read_bytes()).hexdigest())
            for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
    return hashlib.sha256(json.dumps(rows).encode()).hexdigest(), rows


def freeze(out):
    out.mkdir(parents=True, exist_ok=False)
    # Both arms receive identical current PPT implementation, so this compares instructions.
    names = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE, '--',
                                     'skills/edu-writing', 'skills/edu-ppt', 'skills/edu-shared'], cwd=ROOT).decode().splitlines()
    first = out / 'arm-p'
    for name in names:
        target = first / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(subprocess.check_output(['git', 'show', BASE + ':' + name], cwd=ROOT))
    shutil.copytree(ROOT / 'skills/edu-ppt/scripts', first / 'skills/edu-ppt/scripts', dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('__pycache__'))
    second = out / 'arm-q'
    shutil.copytree(first, second)
    writing = second / 'skills/edu-writing'
    ppt = second / 'skills/edu-ppt'
    shutil.copyfile(HERE / 'candidate-writing.md', writing / 'references/methods/measurement-to-judgment.md')
    shutil.copyfile(HERE / 'candidate-ppt.md', ppt / 'references/spoken-evidence.md')
    entry = writing / 'SKILL.md'
    content = entry.read_text(encoding='utf-8')
    content = content.replace('3. **只读需要的路线：**', '   核心概念、测量或贡献容易混淆时，使用 [从关键比较形成判断](references/methods/measurement-to-judgment.md)，把已有主线落实到具体证据，不给每段添加检查标签。\n3. **只读需要的路线：**')
    entry.write_text(content, encoding='utf-8', newline='\n')
    intro = writing / 'references/introduction.md'
    content = intro.read_text(encoding='utf-8')
    substitutions = {
        '## 中文稿：四个语步': '## 中文稿：按问题组织引言',
        '写 3–4 段，800–1300 字（中位约 890 字）：': '以下语步按论证需要合并、拆分或调整。旧语料中常见3–4段、800–1300字，仅供篇幅参照，不规定段数：',
        '用"然而"转入。写成': '交代具体未决问题；需要转折时自然衔接。可写成',
        '紧接"基于此，本研究……"，写': '承接问题，写',
        '引用密度和综述相当（每千字约 7.5–9.6 处），不是无引注的背景铺陈。': '重要外部论断附对应来源；不按引用密度配额添加引文。',
        '价值句只在最后一句出现一次；前几段以证据或具体推断收尾。': '贡献在论证需要的位置说明；段落收束服务当前问题，不重复宣告研究价值。',
        '## 英文稿：四段': '## 英文稿：从问题到可检验的贡献',
        '写 3–5 段，约 450–800 词（中位 580 词、4 段，每段约 140 词）；没有单独的综述一节时可以写到 1,200–1,400 词：': '以下是可选组织方式。旧语料中位580词、4段只是观察值；篇幅随问题复杂程度及是否另设综述调整：',
        '用第一人称写目的、对象和设计：': '清楚说明目的、对象和设计，保留作者合适的人称选择。例如：',
        '一半以上的句子带引注（中位 57%，每千词 23 处），论断在前、引注在句末；引言几乎不用"Author (year) found"式引用。': '引注随需要支持的论断放置，不要求特定比例。最接近研究需要逐项比较时可以点名作者；综合领域认识时可以成组引用。',
        '段落停在证据、空白或目的上：218 个引言段落中只有 4 段以价值句收尾。': '让段落结尾推进下一项问题或判断；不因样本中某种收尾少见就禁止使用。',
    }
    for old, new in substitutions.items():
        if old not in content:
            raise ValueError('Baseline introduction changed: ' + old)
        content = content.replace(old, new)
    intro.write_text(content, encoding='utf-8', newline='\n')
    article = ppt / 'references/article-reading.md'
    article.write_text(article.read_text(encoding='utf-8') + '\n方法与结果难以串成口头讲述时，读 [让证据成为可讲述的主线](spoken-evidence.md)。\n', encoding='utf-8', newline='\n')
    entry = ppt / 'SKILL.md'
    entry.write_text(entry.read_text(encoding='utf-8') + '\n方案、阶段进展或文章解读的页面衔接需要改进时，可用 [证据主线](references/spoken-evidence.md)。\n', encoding='utf-8', newline='\n')
    report = {'frozen_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'baseline': BASE,
              'allocation': {'arm-p': 'baseline', 'arm-q': 'candidate'}, 'scope': 'instruction comparison; common current PPT code', 'arms': {}}
    for arm in [first, second]:
        digest, files = digest_tree(arm)
        report['arms'][arm.name] = {'sha256': digest, 'files': files}
    patches = []
    for p in sorted(second.rglob('*.md')):
        relative = p.relative_to(second)
        original = first / relative
        before = original.read_text(encoding='utf-8').splitlines(True) if original.exists() else []
        after = p.read_text(encoding='utf-8').splitlines(True)
        patches.extend(difflib.unified_diff(before, after, fromfile='a/' + relative.as_posix(), tofile='b/' + relative.as_posix(), n=0))
    # Reproduction must not overwrite the published original freeze record.
    (out / 'candidate.patch').write_text(''.join(patches), encoding='utf-8', newline='\n')
    (out / 'freeze.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({k: v['sha256'] for k, v in report['arms'].items()}))


if __name__ == '__main__':
    freeze(Path(sys.argv[1]).resolve())
