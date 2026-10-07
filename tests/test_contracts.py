"""Instruction contracts and repository structure: red lines stay in place, links resolve, metadata agrees."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'skills'
RELEASE = json.loads((SKILLS / 'release.json').read_text(encoding='utf-8'))
TASK_SKILLS = [p for p in RELEASE['packages'] if p != 'edu-shared']


def text(rel):
    return (SKILLS / rel).read_text(encoding='utf-8')


def frontmatter(rel):
    m = re.match(r'---\n(.*?)\n---\n', text(rel).replace('\r\n', '\n'), re.S)
    return dict(re.findall(r'^(\w+):\s*(.*)$', m.group(1), re.M)) if m else {}


class RedLines(unittest.TestCase):
    """Rules that past failures showed must not be lost when the instructions are edited."""
    CONTRACTS = {
        'edu-shared/references/integrity.md': ['不编造', '报告实际运行过的分析', '结论强度与设计相符', '保留作者的论证', '数据留在本地',
                                               '不把他人的研究写成用户的论文', '属于抄袭', '区分 AI 自查和专家审阅'],
        'edu-writing/SKILL.md': ['voice-zh', 'prose-zh', 'prose-en', '不称为专家审阅', 'check_voice.py', 'check_prose.py',
                                 'check_consistency.py', '先确认一次主线', '属于抄袭'],
        'edu-writing/references/prose-zh.md': ['不编造', '待补', '还可以做的分析'],
        'edu-writing/references/prose-en.md': ['never invent citations', 'Proposed analyses', 'check_prose.py'],
        'edu-writing/references/foundation.md': ['不加免责句', '只在局限部分写一次', '不编造引文'],
        'edu-writing/references/full-manuscript.md': ['写作语言跟随目标期刊', '不编造'],
        'edu-proposal/SKILL.md': ['取消参评资格', '前期成果不列入参考文献', '研究基础只写真实成果', '--identity'],
        'edu-response/SKILL.md': ['只写实际做了的修改', '新分析必须实际运行', '不为迎合审稿人改变结论的性质', '各审稿人独立回复'],
        'edu-review/SKILL.md': ['不是真实的专家评审', '不预测录用概率', '独立性'],
        'edu-audit/SKILL.md': ['不能混称为完整复现', '不凭已报告的值估算'],
        'edu-qual/SKILL.md': ['不虚构独立编码者'],
        'edu-analysis/SKILL.md': ['看过结果后增加的分析标为探索性', 'known_answers.R'],
    }

    def test_contracts_present(self):
        for rel, phrases in self.CONTRACTS.items():
            body = text(rel)
            for phrase in phrases:
                self.assertIn(phrase, body, f'{rel} lost: {phrase}')

    def test_writing_language_follows_journal(self):
        self.assertNotIn('defaulting to English', text('edu-writing/references/full-manuscript.md'))


class Structure(unittest.TestCase):
    def test_packages_match_folders(self):
        folders = sorted(p.name for p in SKILLS.iterdir() if (p / 'SKILL.md').is_file())
        self.assertEqual(folders, sorted(RELEASE['packages']))

    def test_frontmatter(self):
        for name in RELEASE['packages']:
            fm = frontmatter(f'{name}/SKILL.md')
            self.assertEqual(fm.get('name'), name)
            desc = fm.get('description', '')
            self.assertTrue(0 < len(desc) <= 1024, f'{name}: description length {len(desc)}')
            if name in TASK_SKILLS:
                self.assertRegex(desc, r'[一-鿿]', f'{name}: no Chinese trigger words')

    def test_codex_interface(self):
        for name in TASK_SKILLS:
            y = text(f'{name}/agents/openai.yaml')
            self.assertIn('display_name:', y)
            self.assertIn(f'${name}', y)

    def test_relative_links_resolve(self):
        broken = []
        for md in SKILLS.rglob('*.md'):
            for target in re.findall(r'\]\(([^)\s]+)\)', md.read_text(encoding='utf-8')):
                if re.match(r'(https?:|mailto:|#)', target):
                    continue
                if not (md.parent / target.split('#')[0]).exists():
                    broken.append(f'{md.relative_to(SKILLS)} -> {target}')
        self.assertEqual(broken, [])

    def test_root_document_links_resolve(self):
        broken = []
        for md in [ROOT / 'README.md', ROOT / '使用手册.md']:
            for target in re.findall(r'\]\(([^)\s]+)\)', md.read_text(encoding='utf-8')):
                if not re.match(r'(https?:|mailto:|#)', target) and not (ROOT / target.split('#')[0]).exists():
                    broken.append(f'{md.name} -> {target}')
        self.assertEqual(broken, [])

    def test_scripts_named_in_skills_exist(self):
        missing = []
        for name in RELEASE['packages']:
            body = text(f'{name}/SKILL.md')
            for rel in re.findall(r'(?:<本skill>/|(?<![\w/.\-]))(scripts/[\w-]+\.(?:py|R|ps1))', body):
                if not (SKILLS / name / rel).is_file():
                    missing.append(f'{name}: {rel}')
            for other, rel in re.findall(r'\.\./(edu-[\w-]+)/(scripts/[\w-]+\.py)', body):
                if not (SKILLS / other / rel).is_file():
                    missing.append(f'{name}: ../{other}/{rel}')
        self.assertEqual(missing, [])

    def test_readmes_mirror(self):
        for name in RELEASE['packages']:
            zh, en = text(f'{name}/README.md'), text(f'{name}/README_EN.md')
            self.assertIn('[English](README_EN.md)', zh)
            self.assertIn('[中文说明](README.md)', en)
            self.assertEqual(len(re.findall(r'^## ', zh, re.M)), len(re.findall(r'^## ', en, re.M)), name)
            self.assertRegex(zh, r'## 状态\n\n- (Draft|Beta|Stable)')

    def test_plugin_manifests_match_release(self):
        for rel in ['.claude-plugin/plugin.json', '.codex-plugin/plugin.json']:
            self.assertEqual(json.loads((ROOT / rel).read_text(encoding='utf-8'))['version'], RELEASE['version'], rel)
        market = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text(encoding='utf-8'))
        self.assertEqual(market['plugins'][0]['version'], RELEASE['version'])
        self.assertIn(RELEASE['version'], (ROOT / 'README.md').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
