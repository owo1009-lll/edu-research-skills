"""Copy the current release into a clone of the public repository and commit it there.

    python scripts/sync_public.py --public <path to a clone of the public repository> --message "Release 0.6.0"

Only the files tracked at HEAD of this repository are copied: no history, no other branches, nothing ignored.
The public clone must be clean; everything in it except .git is replaced. Push from the public clone afterwards.
"""
from pathlib import Path
import argparse
import io
import shutil
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def git(*args, cwd):
    return subprocess.run(['git', *args], cwd=cwd, check=True, capture_output=True).stdout


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--public', required=True, type=Path)
    ap.add_argument('--message', required=True)
    a = ap.parse_args()
    public = a.public.resolve()
    if public == ROOT or not (public / '.git').is_dir():
        sys.exit('--public must be a separate git clone')
    if git('status', '--porcelain', cwd=public).strip():
        sys.exit('the public clone has uncommitted changes')
    if git('status', '--porcelain', '--untracked-files=no', cwd=ROOT).strip():
        sys.exit('commit the release in this repository first')
    for item in public.iterdir():
        if item.name != '.git':
            shutil.rmtree(item) if item.is_dir() else item.unlink()
    with tarfile.open(fileobj=io.BytesIO(git('archive', '--format=tar', 'HEAD', cwd=ROOT))) as tar:
        tar.extractall(public, filter='data')
    git('add', '-A', '--force', cwd=public)  # every extracted file is a tracked release file
    if not git('status', '--porcelain', cwd=public).strip():
        print('nothing changed')
        return
    git('commit', '-q', '-m', a.message, cwd=public)
    print(git('log', '-1', '--format=%h %s', cwd=public).decode().strip())


if __name__ == '__main__':
    main()
