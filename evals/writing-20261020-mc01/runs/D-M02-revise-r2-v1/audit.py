import hashlib
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent

def append(name, record):
    path = ROOT / name
    data = json.loads(path.read_text(encoding='utf-8')) if path.exists() else []
    data.append(record)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def register(path, kind, action):
    path = Path(path).resolve()
    record = {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'action': action, 'recorded_utc': datetime.now(timezone.utc).isoformat()}
    append('task-input-hashes.json' if kind == 'input' else 'loaded-resources.json', record)

def main():
    append('executed-commands.json', {'argv': sys.argv, 'rendered': subprocess.list2cmdline([sys.executable] + sys.argv),
                                    'started_utc': datetime.now(timezone.utc).isoformat()})
    mode, *args = sys.argv[1:]
    if mode == 'register':
        kind, action, *paths = args
        for path in paths:
            register(path, kind, action)
    elif mode == 'read':
        for path in args:
            register(path, 'resource', 'read')
            print('\nRESOURCE: ' + path)
            print(Path(path).read_text(encoding='utf-8'))
    elif mode in ('check', 'command'):
        label, target, *arguments = args
        if mode == 'check':
            register(target, 'resource', 'executed')
            command = [sys.executable, '-B', target] + arguments
        else:
            command = [target] + arguments
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
        (ROOT / (label + '.stdout.txt')).write_text(result.stdout, encoding='utf-8')
        (ROOT / (label + '.stderr.txt')).write_text(result.stderr, encoding='utf-8')
        append('executed-commands.json', {'argv': command, 'rendered': subprocess.list2cmdline(command),
                                        'exit_code': result.returncode, 'stdout_file': label + '.stdout.txt',
                                        'stderr_file': label + '.stderr.txt'})
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)
    else:
        raise ValueError(mode)

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    main()
