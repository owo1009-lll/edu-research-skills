"""Install, update, check or remove the edu-* skills for Claude Code, Codex or WorkBuddy.

    python scripts/install.py                         # install for Claude Code and Codex
    python scripts/install.py --host workbuddy        # WorkBuddy (personal edition: ~/.workbuddy/skills)
    python scripts/install.py --host codebuddy        # CodeBuddy / WorkBuddy Enterprise: ~/.codebuddy/skills
    python scripts/install.py --host claude --action update
    python scripts/install.py --action status
    python scripts/install.py --action uninstall      # removes only directories this installer owns

Foreign or locally modified directories are never overwritten; every package is staged first and the
whole operation rolls back if any step fails.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import uuid
from contextlib import contextmanager

ROOT = Path(__file__).resolve().parents[1]
OWNER = 'owo1009-lll/edu-research-skills'
MARKER = '.edu-owner.json'
LOCK = '.edu-operation.lock'
STAGE = '.edu-stage-'


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')


def reject_link(path):
    if path.is_symlink() or (path.exists() and getattr(path.stat(), 'st_file_attributes', 0) & 0x400):
        raise RuntimeError('Link/reparse point is not an owned directory: ' + str(path))


def bytecode(rel):
    # Python writes __pycache__ beside installed scripts the first time they run; it is not user content.
    return '__pycache__' in rel.parts or rel.suffix == '.pyc'


def inspect_tree(root):
    reject_link(root)
    files, directories = {}, []
    for directory, dirs, names in os.walk(root, followlinks=False):
        for name in dirs:
            p = Path(directory) / name
            reject_link(p)
            if not bytecode(p.relative_to(root)):
                directories.append(p.relative_to(root).as_posix())
        for name in names:
            p = Path(directory) / name
            reject_link(p)
            if not bytecode(p.relative_to(root)):
                files[p.relative_to(root).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return files, sorted(directories)


def contained_target(base, name):
    reject_link(base)
    path = base / name
    reject_link(path)
    if path.resolve().parent != base.resolve():
        raise RuntimeError('Target is outside the installation root: ' + str(path))
    return path


def remove_owned_stage(base, stage):
    # Deletes only a fresh staging directory created by this installer, never a skill path.
    stage = contained_target(base, stage.name)
    if not stage.name.startswith(STAGE):
        raise RuntimeError('Invalid staging path')
    inspect_tree(stage)  # reject any link before recursive deletion
    shutil.rmtree(stage)


def source_payloads(root=ROOT, release=None):
    release = release or json.loads((root / 'skills/release.json').read_text(encoding='utf-8'))
    payloads = {}
    for name in release['packages']:
        src = root / 'skills' / name
        inspect_tree(src)
        files = {p.relative_to(src).as_posix(): p.read_bytes() for p in sorted(src.rglob('*'))
                 if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}
        hashes = {k: hashlib.sha256(v).hexdigest() for k, v in files.items()}
        directories = sorted({str(parent).replace('\\', '/') for k in files for parent in Path(k).parents if str(parent) != '.'})
        files[MARKER] = encode({'owner': OWNER, 'schema': 2, 'package': name, 'version': release['version'],
                                'files': hashes, 'directories': directories})
        payloads[name] = files
    return release, payloads


def verify_owned(path, name):
    if not path.is_dir() or not (path / MARKER).is_file():
        raise RuntimeError('Foreign target preserved: ' + str(path))
    receipt = json.loads((path / MARKER).read_text(encoding='utf-8'))
    if receipt.get('owner') != OWNER or receipt.get('package') != name or receipt.get('schema') != 2:
        raise RuntimeError('Foreign ownership preserved: ' + str(path))
    files, directories = inspect_tree(path)
    files.pop(MARKER, None)
    if files != receipt.get('files') or directories != receipt.get('directories'):
        raise RuntimeError('Modified or additional files preserved; no action: ' + str(path))
    return receipt


@contextmanager
def operation_lock(path):
    # A pre-existing lock belongs to another or interrupted operation; never remove it here.
    handle = path.open('x', encoding='utf-8')
    try:
        handle.write(OWNER)
        handle.flush()
        yield
    finally:
        handle.close()
        path.unlink()


def operate(destination, action, root=ROOT, release=None):
    destination = Path(destination).absolute()
    for ancestor in [destination, *destination.parents]:
        reject_link(ancestor)
    destination = destination.resolve()
    release, payloads = source_payloads(root, release)
    existing, changes = {}, []
    for name, payload in payloads.items():
        path = contained_target(destination, name)
        if path.exists():
            existing[name] = verify_owned(path, name)
            actual, _ = inspect_tree(path)
            identical = actual == {k: hashlib.sha256(v).hexdigest() for k, v in payload.items()}
            if action == 'install' and not identical:
                raise RuntimeError('Owned older snapshot; use --action update: ' + name)
            if action == 'uninstall' or (action == 'update' and not identical):
                changes.append(name)
        elif action in ('install', 'update'):
            changes.append(name)
    report = {'action': action, 'version': release['version'], 'destination': str(destination), 'packages': []}
    if action == 'status':
        for name in payloads:
            receipt = existing.get(name)
            report['packages'].append({'name': name, 'status': 'owned_verified' if receipt else 'absent', 'receipt': receipt})
        return report
    if changes:
        destination.mkdir(parents=True, exist_ok=True)
        with operation_lock(destination / LOCK):
            stage = contained_target(destination, STAGE + uuid.uuid4().hex)
            stage.mkdir()
            promoted, backed_up = [], []
            safe_to_remove = False
            try:
                if action != 'uninstall':  # build every package before touching an installed one
                    for name in changes:
                        for rel, data in payloads[name].items():
                            p = stage / 'new' / name / rel
                            p.parent.mkdir(parents=True, exist_ok=True)
                            p.write_bytes(data)
                        verify_owned(stage / 'new' / name, name)
                for name in changes:
                    path = contained_target(destination, name)
                    if name in existing:
                        verify_owned(path, name)  # recheck immediately before moving
                        backup = stage / 'old' / name
                        backup.parent.mkdir(parents=True, exist_ok=True)
                        path.rename(backup)
                        backed_up.append(name)
                    elif path.exists():
                        raise RuntimeError('Concurrent target appeared; preserved: ' + str(path))
                    if action != 'uninstall':
                        (stage / 'new' / name).rename(path)
                        promoted.append(name)
                        verify_owned(path, name)
                safe_to_remove = True
            except BaseException:
                for name in reversed(promoted):
                    path = contained_target(destination, name)
                    verify_owned(path, name)
                    path.rename(stage / 'new' / name)
                for name in reversed(backed_up):
                    (stage / 'old' / name).rename(contained_target(destination, name))
                safe_to_remove = True
                raise
            finally:
                if safe_to_remove:
                    remove_owned_stage(destination, stage)
    for name in payloads:
        if action == 'uninstall':
            report['packages'].append({'name': name, 'status': 'removed_owned' if name in changes else 'absent',
                                       'previous_receipt': existing.get(name)})
        else:
            receipt = verify_owned(contained_target(destination, name), name)
            report['packages'].append({'name': name, 'status': 'updated' if name in changes and name in existing
                                       else 'installed' if name in changes else 'already_identical', 'receipt': receipt})
    return report


def host_destinations(host):
    claude = Path(os.environ.get('CLAUDE_CONFIG_DIR', str(Path.home() / '.claude'))) / 'skills'
    codex = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'skills'
    workbuddy = Path(os.environ.get('WORKBUDDY_HOME', str(Path.home() / '.workbuddy'))) / 'skills'
    codebuddy = Path(os.environ.get('CODEBUDDY_HOME', str(Path.home() / '.codebuddy'))) / 'skills'
    return {'claude': [claude], 'codex': [codex], 'workbuddy': [workbuddy], 'codebuddy': [codebuddy],
            'both': [claude, codex]}[host]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--host', choices=['claude', 'codex', 'workbuddy', 'codebuddy', 'both'], default='both',
                    help='both = Claude Code and Codex')
    ap.add_argument('--action', choices=['install', 'update', 'status', 'uninstall'], default='install')
    ap.add_argument('--destination', type=Path, help='install into this folder instead of the host defaults')
    a = ap.parse_args()
    for dest in [a.destination] if a.destination else host_destinations(a.host):
        report = operate(dest, a.action)
        print(json.dumps({'destination': report['destination'], 'action': report['action'], 'version': report['version'],
                          'packages': {p['name']: p['status'] for p in report['packages']}}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
