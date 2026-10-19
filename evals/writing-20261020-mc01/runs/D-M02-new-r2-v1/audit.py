import datetime
import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SKILL = pathlib.Path(r'<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing')
INPUTS = pathlib.Path(r'<EXPERIMENT_ROOT>\inputs\D-M02')
sys.stdout.reconfigure(encoding='utf-8')

def record(filename, item):
    path = ROOT / filename
    items = json.loads(path.read_text(encoding='utf-8')) if path.exists() else []
    items.append(item)
    path.write_text(json.dumps(items, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def resource(path, action, kind):
    path = path.resolve()
    item = {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'action': action}
    record('task-input-hashes.json' if kind == 'input' else 'loaded-resources.json', item)

def main():
    mode, *args = sys.argv[1:]
    resource(pathlib.Path(__file__), 'executed task-created audit helper', 'resource')
    command = [sys.executable, str(pathlib.Path(__file__).resolve()), *sys.argv[1:]]
    record('executed-commands.json', {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'argv': command})
    if mode == 'read':
        for arg in args:
            path = pathlib.Path(arg)
            resource(path, 'read', 'input' if path.parent == INPUTS else 'resource')
            print('\nFILE: ' + str(path) + '\n')
            print(path.read_text(encoding='utf-8'))
    elif mode == 'check':
        script, draft, *extra = args
        path = SKILL / 'scripts' / script
        resource(path, 'executed', 'resource')
        cmd = [sys.executable, str(path), '--draft', str(ROOT / draft), *extra]
        record('executed-commands.json', {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'argv': cmd})
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', env={**__import__('os').environ, 'PYTHONIOENCODING': 'utf-8'})
        log = ROOT / (path.stem + '-' + pathlib.Path(draft).stem + '.txt')
        log.write_text('COMMAND ARGV: ' + json.dumps(cmd, ensure_ascii=False) + '\nEXIT CODE: ' + str(result.returncode) + '\nSTDOUT:\n' + result.stdout + '\nSTDERR:\n' + result.stderr, encoding='utf-8')
        print(log.read_text(encoding='utf-8'))
        sys.exit(result.returncode)
    elif mode == 'prepare':
        for name in args:
            path = ROOT / name
            text = path.read_text(encoding='utf-8')
            heading, body = text.split('\n\n', 1)
            assert heading.startswith('# Secondary-writing demonstration')
            diagnostic = ROOT / (path.stem + '-checker-input.md')
            diagnostic.write_text('# Discussion\n\n' + body, encoding='utf-8')
            words = re.findall(r"\b[^\W_]+(?:['’\-][^\W_]+)*\b", body, flags=re.UNICODE)
            count = {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'body_words': len(words), 'whitespace_count': len(body.split()), 'heading_excluded': heading, 'method': 'Unicode letters/digits; internal apostrophes and hyphens stay within one word', 'diagnostic_copy': str(diagnostic), 'body_unchanged_in_diagnostic_copy': diagnostic.read_text(encoding='utf-8').split('\n\n', 1)[1] == body}
            record('word-counts.json', count)
            print(json.dumps(count, ensure_ascii=False, indent=2))
    elif mode == 'finalize':
        source = ROOT / 'second-draft.md'
        target = ROOT / 'final.md'
        assert not target.exists(), 'Do not overwrite a saved final.'
        target.write_bytes(source.read_bytes())
        print('Copied second-draft.md to final.md without changing its bytes.')
        print('Final SHA-256: ' + hashlib.sha256(target.read_bytes()).hexdigest())
    elif mode == 'verify':
        for name in ['first-draft.md', 'second-draft.md', 'final.md', 'self-review.md', 'rationale.md', 'note.md', 'loaded-resources.json', 'task-input-hashes.json', 'executed-commands.json', 'word-counts.json']:
            path = ROOT / name
            text = path.read_text(encoding='utf-8')
            assert '\ufffd' not in text, name
        assert (ROOT / 'second-draft.md').read_bytes() == (ROOT / 'final.md').read_bytes()
        body = (ROOT / 'final.md').read_text(encoding='utf-8').split('\n\n', 1)[1]
        assert not any(line.startswith('#') for line in body.splitlines())
        assert 350 <= len(body.split()) <= 450
        resources = json.loads((ROOT / 'loaded-resources.json').read_text(encoding='utf-8'))
        inputs = json.loads((ROOT / 'task-input-hashes.json').read_text(encoding='utf-8'))
        for item in resources + inputs:
            assert hashlib.sha256(pathlib.Path(item['path']).read_bytes()).hexdigest() == item['sha256'], item['path']
        result = {'final_body_words': len(body.split()), 'paragraphs': len(body.strip().split('\n\n')), 'no_internal_subheadings': True, 'utf8_validation': 'passed', 'saved_draft_equals_final': True, 'resource_hashes_verified': len(resources), 'input_hashes_verified': len(inputs)}
        (ROOT / 'verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        raise ValueError(mode)

if __name__ == '__main__':
    main()
