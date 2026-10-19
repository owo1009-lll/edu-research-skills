"""Check archived bytes, recorded skill resources and all three native outputs.

Run from any directory with the repository's review dependencies installed.
This verifies preservation and plan correspondence, not the truth of review advice.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', action='store_true',
                        help='Also compare all 203 current runtime files with the frozen manifest.')
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    archive = json.loads((base / 'archive-manifest.json').read_text(encoding='utf-8'))
    for row in archive['files']:
        if digest(base / row['path']) != row['published_sha256']:
            raise ValueError(f'Published artifact changed: {row["path"]}')
    snapshot = json.loads((base / 'snapshot.json').read_text(encoding='utf-8'))
    verified_resources = 0
    for row in snapshot['files']:
        copy = base / 'snapshot' / row['path']
        if copy.exists():
            assert digest(copy) == row['sha256'], row['path']
            verified_resources += 1
        if args.runtime:
            assert digest(base.parents[1] / row['path']) == row['sha256'], row['path']
    spec = importlib.util.spec_from_file_location(
        'frozen_annotator', base / 'snapshot/skills/edu-review/scripts/annotate_manuscript.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    cases = [
        ('quant', 'quant_retrieval.pdf', 'retrieval', 'annotations-v1.json',
         'quant_retrieval_审稿标注版.pdf'),
        ('qual', 'qual_silence.pdf', 'submission-review', 'annotations-v2.json',
         'qual_silence_审稿标注版.pdf'),
        ('mixed', 'mixed_feedback.docx', 'mixed-review', 'annotations-v2.json',
         'final/mixed_feedback_审稿标注版.docx'),
    ]
    results = []
    for case, source, folder, plan, output in cases:
        run = base / 'runs' / case / 'edu_output/review' / folder
        content = json.loads((run / plan).read_text(encoding='utf-8-sig'))
        result = module.verify(base / 'inputs-final' / source, run / output, content)
        results.append({'case': case, 'result': result})
    print(json.dumps({'archived_artifacts': len(archive['files']),
                      'exact_frozen_resources': verified_resources,
                      'full_runtime_checked': args.runtime,
                      'native_outputs': results}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
