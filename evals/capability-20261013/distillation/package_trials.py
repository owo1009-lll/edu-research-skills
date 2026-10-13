"""Publish complete generated trial outputs, excluding source full texts and runtime caches.

Run after the frozen trials and rendering have finished. Originals remain in the
ignored work folder. Only workspace prefixes/newlines and manifest paths/hashes
are normalized; manuscript, slide and note content is not edited.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def package(work, dest):
    dest.mkdir(parents=True, exist_ok=False)
    manifest = {'scope': 'Original frozen trials; no post-review content revisions', 'files': []}

    def copy(src, target):
        target.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix in {'.json', '.md', '.txt', '.csv'}:
            text = src.read_text(encoding='utf-8-sig')
            for prefix in [str(ROOT) + '\\', str(ROOT).replace('\\', '\\\\') + '\\\\', ROOT.as_posix() + '/']:
                text = text.replace(prefix, '')
            text = '\n'.join(line.rstrip() for line in text.splitlines()).rstrip('\n') + '\n'
            target.write_text(text, encoding='utf-8', newline='\n')
        else:
            shutil.copyfile(src, target)
        manifest['files'].append({'file': target.relative_to(dest).as_posix(), 'original': src.relative_to(work).as_posix(),
                                  'original_sha256': sha(src), 'published_sha256': sha(target)})

    for arm in ['arm-p', 'arm-q']:
        for case in ['H1-writing', 'H2-writing', 'H1-ppt', 'H3-ppt']:
            source = work / 'runs' / arm / case
            target = dest / arm / case
            # No extracted source text, source screenshots, generator scratch
            # scripts or runtime caches are part of this public package.
            for src in source.iterdir():
                if src.is_file() and src.suffix in {'.md', '.json', '.txt', '.docx'}:
                    copy(src, target / src.name)
            if 'ppt' in case:
                for folder in ['deck', 'first-deck']:
                    for src in (source / folder).iterdir():
                        if src.is_file():
                            copy(src, target / folder / src.name)
                    build_path = target / folder / 'build.json'
                    build = json.loads(build_path.read_text(encoding='utf-8'))
                    plan_name = 'plan.json' if folder == 'deck' else 'first-plan.json'
                    build['source_plan'] = (target / plan_name).relative_to(ROOT).as_posix()
                    build['plan_sha256'] = sha(target / plan_name)
                    build['outputs'] = {name: sha(target / folder / name) for name in build['outputs']}
                    build['packaging'] = 'Portable source paths and text line endings; original hashes in package-manifest.json'
                    build_path.write_text(json.dumps(build, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
                for src in (work / 'renders' / arm / case).iterdir():
                    if src.is_file():
                        copy(src, target / 'preview' / src.name)
                render_path = target / 'preview/render.json'
                render = json.loads(render_path.read_text(encoding='utf-8'))
                render['source'] = (target / 'deck/slides.pptx').relative_to(ROOT).as_posix()
                render_path.write_text(json.dumps(render, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
    for file in (work / 'blind').rglob('*.md'):
        copy(file, dest / 'blind' / file.relative_to(work / 'blind'))
    for name in ['blind-key.json', 'blind-input-hashes.json', 'blind-review.md']:
        copy(work / name, dest / name)
    for item in manifest['files']:
        item['published_sha256'] = sha(dest / item['file'])
    (dest/'package-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
    return len(manifest['files'])


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work', type=Path, default=ROOT/'edu_output/capability-20261013')
    p.add_argument('--out', type=Path, default=HERE/'trials')
    args = p.parse_args()
    print('Published files:', package(args.work.resolve(), args.out.resolve()))
