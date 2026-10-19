"""Run the snapshot checkers and preserve their actual output and provenance."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SKILLS = Path('<EXPERIMENT_ROOT>/variants/v2/skills')
INPUTS = Path('<EXPERIMENT_ROOT>/inputs/D-Q02')
CHECKS = ROOT / 'checks'
CHECKS.mkdir(exist_ok=True)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_json(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

resource_paths = [
    ('edu-writing/SKILL.md', ['read']),
    ('edu-writing/references/foundation.md', ['read']),
    ('edu-writing/references/argument.md', ['read']),
    ('edu-writing/references/voice-en.md', ['read']),
    ('edu-writing/references/quantitative-discussion.md', ['read']),
    ('edu-writing/references/framing-results.md', ['read']),
    ('edu-shared/references/integrity.md', ['read']),
    ('edu-writing/scripts/check_voice.py', ['read', 'executed']),
    ('edu-writing/scripts/check_prose.py', ['read', 'executed']),
]
resources = [dict(path=str(SKILLS / p), sha256=digest(SKILLS / p), actions=a)
             for p, a in resource_paths]
resources.append(dict(path=str(Path(__file__).resolve()), sha256=digest(Path(__file__)),
                      actions=['executed'], role='run-local logging and validation helper'))
write_json(ROOT / 'loaded-resources.json', {
    'hash_algorithm': 'SHA-256',
    'scope': 'Only specified v2 skill snapshot and this output directory; no installed skill copies.',
    'note': 'Read means opened by the tool. Long script displays were truncated; imports and external reads were separately inspected with rg. Both checkers use standard-library modules and embedded reference data for Markdown input.',
    'resources': resources,
})
write_json(ROOT / 'input-hashes.json', {
    'hash_algorithm': 'SHA-256',
    'inputs': [dict(path=str(INPUTS / name), sha256=digest(INPUTS / name))
               for name in ['revise-request.md', 'source-pack.md', 'original.md']],
})

stage = sys.argv[1]
draft = ROOT / f'{stage}.md'
text = draft.read_text(encoding='utf-8')
lines = text.splitlines()
heading = lines[0]
body = '\n'.join(lines[1:]).strip()
paragraphs = [p for p in re.split(r'\n\s*\n', body) if p.strip()]
word_counts = {
    'stage': stage,
    'file': str(draft),
    'sha256': digest(draft),
    'convention': 'Whitespace-delimited words; hyphenated words and contractions count as one. In-text citations count; the attribution heading and Markdown marker do not count toward the manuscript limit.',
    'body_words': len(body.split()),
    'attribution_heading_words': len(heading.lstrip('# ').split()),
    'total_words_without_markdown_marker': len(body.split()) + len(heading.lstrip('# ').split()),
    'body_paragraphs': len(paragraphs),
    'within_140_170_words': 140 <= len(body.split()) <= 170,
    'replacement_characters': text.count('\ufffd'),
    'contains_cjk': bool(re.search(r'[\u4e00-\u9fff]', text)),
    'both_original_citations_present': 'Orth et al., 2021' in body and 'Voelkle et al. (2014)' in body,
}
write_json(CHECKS / f'{stage}-word-count.json', word_counts)
print(json.dumps(word_counts, ensure_ascii=False, indent=2))

checker_input = CHECKS / f'{stage}-body.md'
checker_input.write_text('# Discussion\n\n' + body + '\n', encoding='utf-8')
write_json(CHECKS / f'{stage}-checker-input.json', {
    'source_draft': str(draft),
    'source_sha256': digest(draft),
    'checker_input': str(checker_input),
    'checker_input_sha256': digest(checker_input),
    'transformation': 'Replace only the attribution heading with Discussion so section recognition and prose metrics describe the manuscript body.',
    'body_identical': checker_input.read_text(encoding='utf-8').split('\n\n', 1)[1].strip() == body,
})
commands = [
    ('voice', [sys.executable, str(SKILLS / 'edu-writing/scripts/check_voice.py'), '--draft', str(checker_input), '--source', str(INPUTS / 'source-pack.md'), str(INPUTS / 'original.md')]),
    ('prose', [sys.executable, str(SKILLS / 'edu-writing/scripts/check_prose.py'), '--draft', str(checker_input)]),
]
for label, argv in commands:
    started = datetime.now(timezone.utc).isoformat()
    completed = subprocess.run(argv, cwd=ROOT, capture_output=True)
    stdout_path = CHECKS / f'{stage}-{label}.stdout.txt'
    stderr_path = CHECKS / f'{stage}-{label}.stderr.txt'
    stdout_path.write_bytes(completed.stdout)
    stderr_path.write_bytes(completed.stderr)
    record = dict(stage=stage, check=label, started_utc=started,
                  finished_utc=datetime.now(timezone.utc).isoformat(), argv=argv,
                  command_line=subprocess.list2cmdline(argv), cwd=str(ROOT),
                  returncode=completed.returncode,
                  stdout=str(stdout_path), stderr=str(stderr_path),
                  draft_sha256=digest(draft), checker_input_sha256=digest(checker_input))
    with (ROOT / 'executed-commands.jsonl').open('a', encoding='utf-8') as log:
        log.write(json.dumps(record, ensure_ascii=False) + '\n')
    print(completed.stdout.decode('utf-8'))
    if completed.stderr:
        print(completed.stderr.decode('utf-8'), file=sys.stderr)
    if completed.returncode:
        raise SystemExit(completed.returncode)
