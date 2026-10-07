"""Installer lifecycle checks in disposable destinations; never touches real skill folders."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import install as installer


class InstallLifecycle(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.dest = Path(self.temp.name) / 'skills'
        self.release = json.loads((installer.ROOT / 'skills/release.json').read_text(encoding='utf-8'))
        self.names = list(self.release['packages'])

    def tearDown(self):
        self.temp.cleanup()

    def action(self, action, release=None):
        return installer.operate(self.dest, action, release=release or self.release)

    def install(self):
        return self.action('install')

    def test_idempotency_and_stable_sibling_preserved(self):
        stable = self.dest / 'edu-writing-old/SKILL.md'
        stable.parent.mkdir(parents=True)
        stable.write_bytes(b'foreign stable content')
        first = self.install()
        self.assertTrue(all(p['status'] == 'installed' for p in first['packages']))
        second = self.install()
        self.assertTrue(all(p['status'] == 'already_identical' for p in second['packages']))
        self.action('uninstall')
        self.assertEqual(stable.read_bytes(), b'foreign stable content')
        self.assertFalse(any((self.dest / n).exists() for n in self.names))
        self.assertTrue(all(p['status'] == 'absent' for p in self.action('uninstall')['packages']))

    def test_foreign_target_preflight_no_partial_install(self):
        foreign = self.dest / self.names[-1] / 'research.txt'
        foreign.parent.mkdir(parents=True)
        foreign.write_bytes(b'keep')
        with self.assertRaisesRegex(RuntimeError, 'Foreign'):
            self.install()
        self.assertEqual(foreign.read_bytes(), b'keep')
        self.assertFalse((self.dest / self.names[0]).exists())

    def test_identical_without_receipt_is_foreign(self):
        self.install()
        marker = self.dest / self.names[0] / installer.MARKER
        marker.unlink()
        with self.assertRaisesRegex(RuntimeError, 'Foreign'):
            self.action('uninstall')
        self.assertTrue(all((self.dest / n).exists() for n in self.names))

    def test_changed_and_extra_files_preserved(self):
        self.install()
        extra = self.dest / self.names[-1] / 'user_note.txt'
        extra.write_bytes(b'user edit')
        before = {n: installer.inspect_tree(self.dest / n) for n in self.names}
        for action in ['install', 'update', 'uninstall']:
            with self.assertRaisesRegex(RuntimeError, 'Modified or additional'):
                self.action(action)
            self.assertEqual(before, {n: installer.inspect_tree(self.dest / n) for n in self.names})
        extra.unlink()
        skill = self.dest / self.names[0] / 'SKILL.md'
        skill.write_bytes(skill.read_bytes() + b'\nlocal change\n')
        with self.assertRaises(RuntimeError):
            self.action('update')
        self.assertTrue(skill.read_bytes().endswith(b'local change\n'))

    def test_bytecode_cache_from_running_scripts_does_not_block_update(self):
        self.install()
        cache = self.dest / 'edu-writing/scripts/__pycache__/x.cpython-311.pyc'
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_bytes(b'bytecode')
        release = copy.deepcopy(self.release)
        release['version'] = '0.1.0-test-update'
        self.action('update', release)
        self.assertFalse(cache.exists())
        self.action('uninstall', release)
        self.assertFalse(any((self.dest / n).exists() for n in self.names))

    def test_host_destinations_include_workbuddy_and_codebuddy(self):
        import os
        from unittest import mock
        with mock.patch.dict(os.environ, {'WORKBUDDY_HOME': str(self.dest / 'wb'), 'CODEBUDDY_HOME': str(self.dest / 'cb')}):
            self.assertEqual(installer.host_destinations('workbuddy'), [self.dest / 'wb' / 'skills'])
            self.assertEqual(installer.host_destinations('codebuddy'), [self.dest / 'cb' / 'skills'])
        self.assertEqual(len(installer.host_destinations('both')), 2)  # both still means Claude Code and Codex

    def test_extra_empty_directory_preserved(self):
        self.install()
        extra = self.dest / self.names[0] / 'my_folder'
        extra.mkdir()
        with self.assertRaises(RuntimeError):
            self.action('uninstall')
        self.assertTrue(extra.is_dir())

    def test_real_version_update_and_repeat(self):
        self.install()
        release = copy.deepcopy(self.release)
        release['version'] = '0.1.0-test-update'
        with self.assertRaisesRegex(RuntimeError, 'use --action update'):
            self.action('install', release)
        updated = self.action('update', release)
        self.assertTrue(all(p['receipt']['version'] == release['version'] for p in updated['packages']))
        self.assertTrue(all(p['status'] == 'already_identical' for p in self.action('update', release)['packages']))
        self.action('uninstall', release)

    def test_partial_failure_rolls_back_all_packages(self):
        self.install()
        before = {n: installer.inspect_tree(self.dest / n) for n in self.names}
        release = copy.deepcopy(self.release)
        release['version'] = '0.1.0-test-update'
        original = Path.rename
        def injected(path, target):
            if path.parent.name == 'new' and path.name == self.names[1]:
                raise OSError('injected promotion failure')
            return original(path, target)
        with patch.object(Path, 'rename', injected):
            with self.assertRaisesRegex(OSError, 'injected'):
                self.action('update', release)
        self.assertEqual(before, {n: installer.inspect_tree(self.dest / n) for n in self.names})
        self.assertFalse((self.dest / installer.LOCK).exists())
        self.assertFalse(list(self.dest.glob(installer.STAGE + '*')))

    def test_installed_links_and_unchanged_analysis_code(self):
        self.install()
        import re
        for name in self.names:
            for p in (self.dest / name).rglob('*.md'):
                for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', p.read_text(encoding='utf-8')):
                    if '://' not in link and not link.startswith('#'):
                        self.assertTrue((p.parent / link.split('#')[0]).exists(), (p, link))
        for name in self.names:
            for p in (installer.ROOT / 'skills' / name).rglob('*'):
                if p.is_file() and '__pycache__' not in p.parts:
                    rel = p.relative_to(installer.ROOT / 'skills' / name)
                    self.assertEqual(p.read_bytes(), (self.dest / name / rel).read_bytes(), rel)

if __name__ == '__main__':
    unittest.main()
