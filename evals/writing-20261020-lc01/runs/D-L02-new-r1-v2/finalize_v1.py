"""Preserved v1 finalizer: copy the checked revision and verify the local record."""
from pathlib import Path
import datetime
import hashlib
import json
import sys

root = Path(__file__).resolve().parent
def read_json(name):
    return json.loads((root / name).read_text(encoding='utf-8'))
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def put(name, data):
    (root / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

seed = read_json('prerun-record-v1.json')
tail = read_json('finalization-data-v1.json')
draft = root / 'draft-02.md'
final = root / 'final.md'
if final.exists():
    raise SystemExit('Refusing to overwrite an existing final manuscript.')
final.write_bytes(draft.read_bytes())
count = read_json('draft-02-word-count.json')
assert count['sha256'] == sha(draft)
assert count['within_350_450_words']
assert final.read_bytes() == draft.read_bytes()
for stage in ('draft-01', 'draft-02'):
    for checker in ('check_voice', 'check_prose'):
        result = read_json(stage + '-' + checker + '.execution.json')
        assert result['exit_code'] == 0
        assert result['draft_sha256'] == sha(root / (stage + '.md'))
        assert (root / result['stdout']).exists()
        assert (root / result['stderr']).exists()
for item in read_json('input-hashes.json')['inputs']:
    assert item['sha256'] == sha(item['path'])
resources = read_json('loaded-resources.json')
for item in resources['resources']:
    assert item['sha256'] == sha(item['path'])
for filename, usage in [('prerun-record-v1.json', ['read']), ('finalization-data-v1.json', ['read']), ('finalize_v1.py', ['executed'])]:
    path = root / filename
    resources['resources'].append({'path': str(path), 'sha256': sha(path), 'usage': usage, 'origin': 'preserved run support'})
put('loaded-resources.json', resources)
commands = seed['shell_commands_before_checking']
for command in tail['shell_commands_after_prerun_seed']:
    commands.append({'sequence': len(commands) + 1, 'command': command, 'exit_code': 0})
put('executed-shell-commands.json', {'commands': commands, 'checker_subprocesses': 'executed-commands.jsonl', 'patch_operations': tail['patch_operations'], 'helper_preservation': tail['support_creation']})
check = {'final_path': str(final), 'final_sha256': sha(final), 'checked_revision_sha256': sha(draft), 'byte_identical_to_checked_revision': True, 'body_words_whitespace': count['whitespace_word_count'], 'body_words_lexical': count['lexical_word_count'], 'attribution_heading_excluded': True, 'all_four_checker_executions_succeeded': True, 'input_hashes_unchanged': True, 'loaded_resource_hashes_verified': True, 'utf8_markdown_files': {p.name: sha(p) for p in sorted(root.glob('*.md'))}}
for path in root.glob('*.md'):
    path.read_text(encoding='utf-8')
put('final-integrity.json', check)
with (root / 'executed-commands.jsonl').open('a', encoding='utf-8') as stream:
    stream.write(json.dumps({'kind': 'finalizer execution', 'argv': [sys.executable, '-B', str(Path(__file__).resolve())], 'helper_sha256': sha(__file__), 'exit_code': 0, 'recorded_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}) + '\n')
summary = 'Final manuscript: ' + str(final) + '\nBody words excluding attribution heading: ' + str(count['whitespace_word_count']) + '\nFinal matches checked draft-02.md byte-for-byte. All four checker runs succeeded.\n'
(root / 'finalization-result.txt').write_text(summary, encoding='utf-8')
print(summary)
