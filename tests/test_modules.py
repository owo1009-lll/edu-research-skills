"""End-to-end checks of the analysis, audit, qualitative and voice scripts in disposable project folders."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'skills'
sys.path.insert(0, str(SKILLS / 'edu-shared' / 'scripts'))
from edu_runtime import find_rscript  # noqa: E402

RSCRIPT = find_rscript()


def run(args, cwd):
    return subprocess.run([sys.executable, '-X', 'utf8', *map(str, args)], cwd=cwd, capture_output=True, text=True, encoding='utf-8')


class Project(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()


@unittest.skipUnless(RSCRIPT, 'R is not installed')
class Analysis(Project):
    def test_known_answers(self):
        proc = subprocess.run([RSCRIPT, '--vanilla', str(SKILLS / 'edu-analysis/tests/known_answers.R')],
                              capture_output=True, text=True, encoding='utf-8', errors='replace')
        self.assertEqual(proc.returncode, 0, proc.stdout[-3000:] + proc.stderr[-2000:])

    def test_script_and_adapter_runs_write_to_project(self):
        fixtures = SKILLS / 'edu-analysis/tests/fixtures'
        (self.dir / 'analysis.R').write_text('source("edu_methods.R")\nx <- read.csv("inputs/paths_synthetic.csv")\n'
                                             'edu_save(edu_chisq(x, "xb", "wb"), "chisq")\n', encoding='utf-8')
        p = run([SKILLS / 'edu-analysis/scripts/run_r.py', '--script', 'analysis.R', '--input', fixtures / 'paths_synthetic.csv'], self.dir)
        self.assertEqual(p.returncode, 0, p.stderr)
        out = Path(json.loads(p.stdout)['run'])
        self.assertTrue((out / 'output/chisq_tests.csv').is_file())
        self.assertEqual(json.loads((out / 'run_status.json').read_text(encoding='utf-8'))['status'], 'completed')
        self.assertTrue((out / 'sessionInfo.txt').is_file())
        self.assertTrue(out.is_relative_to(self.dir / 'edu_output' / 'analysis'))
        p = run([SKILLS / 'edu-analysis/scripts/run_r.py', '--adapter', 'basic', '--plan', fixtures / 'paths_plan.json'], self.dir)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertTrue((Path(json.loads(p.stdout)['run']) / 'output/results.csv').is_file())

    def test_failed_script_is_kept_and_reported(self):
        (self.dir / 'bad.R').write_text('stop("deliberate failure")\n', encoding='utf-8')
        p = run([SKILLS / 'edu-analysis/scripts/run_r.py', '--script', 'bad.R'], self.dir)
        self.assertNotEqual(p.returncode, 0)
        out = Path(json.loads(p.stdout)['run'])
        self.assertEqual(json.loads((out / 'run_status.json').read_text(encoding='utf-8'))['status'], 'failed')
        self.assertTrue((out / 'sessionInfo.txt').is_file())

    def test_audit_example(self):
        for f in (SKILLS / 'edu-audit/examples').glob('E17_*'):
            shutil.copy(f, self.dir)
        p = run([SKILLS / 'edu-audit/scripts/run_audit.py', '--config', 'E17_config.json'], self.dir)
        self.assertEqual(p.returncode, 0, p.stderr)
        rows = next((self.dir / 'edu_output/audit').iterdir()) / 'output/comparison.csv'
        self.assertNotIn('"discrepant"', rows.read_text(encoding='utf-8'))


class Qualitative(Project):
    def test_synthetic_thematic_cycle(self):
        private = self.dir / 'edu_output/private'
        private.mkdir(parents=True)
        for f in ['synthetic_interviews.csv', 'synthetic_redactions.json', 'synthetic_annotation.json']:
            shutil.copy(SKILLS / 'edu-qual/examples' / f, private)
        script = SKILLS / 'edu-qual/scripts/theme_analysis.py'
        p = run([script, 'prepare', '--input', 'edu_output/private/synthetic_interviews.csv',
                 '--redactions', 'edu_output/private/synthetic_redactions.json', '--output', 'edu_output/private/prep'], self.dir)
        self.assertEqual(p.returncode, 0, p.stderr)
        p = run([script, 'commit', '--prepared', 'edu_output/private/prep',
                 '--annotation', 'edu_output/private/synthetic_annotation.json', '--actor', 'AI_assistant'], self.dir)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn('[同事A]', (private / 'prep/segments.json').read_text(encoding='utf-8'))

    def test_transcripts_outside_private_are_refused(self):
        shutil.copy(SKILLS / 'edu-qual/examples/synthetic_interviews.csv', self.dir)
        p = run([SKILLS / 'edu-qual/scripts/theme_analysis.py', 'prepare', '--input', 'synthetic_interviews.csv',
                 '--redactions', 'x.json', '--output', 'prep'], self.dir)
        self.assertNotEqual(p.returncode, 0)


class Voice(Project):
    CHECK = SKILLS / 'edu-writing/scripts/check_voice.py'

    def test_disclaimers_and_invented_numbers_are_flagged(self):
        (self.dir / 'src.md').write_text('Each video lasted about 4 min; 60 students took part.', encoding='utf-8')
        (self.dir / 'draft.md').write_text('# 讨论\n\n研究发现样例提升了应用表现，但尚不能证明其提升了迁移能力。'
                                          '这一结果不宜视为普遍规律。教师可采用每段约6分钟的视频。\n', encoding='utf-8')
        p = run([self.CHECK, '--draft', 'draft.md', '--source', 'src.md'], self.dir)
        self.assertIn('Disclaimer sentences in the discussion body: 2', p.stdout)
        self.assertIn('Numbers not found in the sources (derived values are fine; invented details are not): 1', p.stdout)

    def test_published_style_passes(self):
        (self.dir / 'draft.md').write_text('# 讨论\n\n研究发现，教师支持显著正向预测学习投入。可能的原因在于，支持提高了学生的胜任感。'
                                          '这与已有研究的结论一致。\n\n# 研究局限与展望\n\n本研究为横截面设计，后续研究可采用纵向设计检验因果方向。\n', encoding='utf-8')
        p = run([self.CHECK, '--draft', 'draft.md'], self.dir)
        self.assertIn('Disclaimer sentences (%): 0.0', p.stdout)
        self.assertIn('Limitation sentences outside the limitations unit: 0', p.stdout)


class Proposal(Project):
    def test_counts_identity_and_overclaims(self):
        lines = ['一、选题依据', '本课题填补了国内空白。我校前期开展了预调查。', '二、研究内容', '研究对象为农村教师。']
        (self.dir / 'draft.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
        p = run([SKILLS / 'edu-proposal/scripts/check_proposal.py', '--draft', 'draft.md', '--limit', '20', '--identity', '张三,某某大学'], self.dir)
        self.assertIn('OVER by', p.stdout)
        self.assertIn('选题依据:', p.stdout)
        self.assertIn('Possible identity leaks: 1', p.stdout)
        self.assertIn('Claims that need support from the literature review: 1', p.stdout)


if __name__ == '__main__':
    unittest.main()
