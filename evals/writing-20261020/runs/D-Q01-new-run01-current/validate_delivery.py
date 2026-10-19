"""Record the actual loaded-file manifest and check this two-paragraph delivery."""
from pathlib import Path
import hashlib
import json
import re

RUN = Path(r'@runs\D-Q01-new-run01-current')
SNAPSHOT = Path(r'@snapshot')
INPUT = Path(r'@inputs\D-Q01')
LOADED = [
    'skills/edu-writing/SKILL.md',
    'skills/edu-writing/references/argument.md',
    'skills/edu-writing/references/voice-en.md',
    'skills/edu-writing/references/quantitative-discussion.md',
    'skills/edu-writing/references/framing-results.md',
    'skills/edu-shared/references/integrity.md',
    'skills/edu-writing/scripts/check_voice.py',
    'skills/edu-writing/scripts/check_prose.py',
]

def utf8_text(path):
    return path.read_text(encoding='utf-8-sig')

def body(text):
    return '\n'.join(line for line in text.splitlines() if not line.startswith('#')).strip()

def hash_record(path):
    raw = path.read_bytes()
    raw.decode('utf-8-sig')  # Confirm the loaded text is valid UTF-8; hash original bytes.
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}

manifest = {
    'snapshot_root': str(SNAPSHOT),
    'loaded_snapshot_relative_paths': LOADED,
    'snapshot_files': [dict(path=rel, **hash_record(SNAPSHOT / rel)) for rel in LOADED],
    'inputs': [dict(path=str(INPUT / name), **hash_record(INPUT / name))
               for name in ('new-request.md', 'source-pack.md')],
    'scope': 'The listed snapshot files were read; both checker scripts were executed. No original article, web source, other run, distillation file, evaluation summary or current repository skill was read.',
    'script_read_note': 'The tool display of check_prose.py was truncated; targeted searches inspected its imports, file reads and heading matcher. Its complete file was executed. Corpus values are embedded in the checker; no corpus file was loaded.'
}
(RUN / 'loads.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

final_body = body(utf8_text(RUN / 'final.md'))
paragraphs = [p for p in re.split(r'\n\s*\n', final_body) if p.strip()]
whitespace_count = len(final_body.split())
lexical_count = len(re.findall(r"[^\W_]+(?:[’'–-][^\W_]+)*(?:\.[0-9]+)*", final_body, flags=re.UNICODE))
body_matches = body(utf8_text(RUN / 'draft-01.md')) == body(utf8_text(RUN / 'draft-01-prose-input.md'))
check = {
    'final_body_paragraphs': len(paragraphs),
    'final_body_whitespace_tokens': whitespace_count,
    'final_body_lexical_words': lexical_count,
    'within_requested_230_280_by_both_counts': 230 <= whitespace_count <= 280 and 230 <= lexical_count <= 280,
    'draft_and_prose_check_copy_bodies_identical': body_matches,
    'attributed_demonstration_heading_present': utf8_text(RUN / 'final.md').startswith('# Secondary-writing demonstration based on Högberg (2023)'),
    'final_utf8_without_bom': not (RUN / 'final.md').read_bytes().startswith(b'\xef\xbb\xbf'),
    'statistical_reanalysis_performed': False,
    'note': 'These are format, encoding, count and identity checks. Claim validity was separately assessed by AI reading the source pack.'
}
(RUN / 'delivery-validation.json').write_text(json.dumps(check, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(check, ensure_ascii=False, indent=2))
assert len(paragraphs) == 2
assert check['within_requested_230_280_by_both_counts']
assert body_matches
assert check['attributed_demonstration_heading_present']
assert check['final_utf8_without_bom']
