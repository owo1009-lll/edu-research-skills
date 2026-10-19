import hashlib
import json
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parent
results = []
for filename in sys.argv[1:]:
    path = root / filename
    text = path.read_text(encoding='utf-8')
    body = '\n'.join(line for line in text.splitlines() if not line.startswith('#')).strip()
    paragraphs = re.split(r'\n\s*\n', body)
    words = body.split()
    checker_words = re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-.]*", body)
    result = {'file': filename, 'body_words_whitespace': len(words),
              'body_words_checker_regex': len(checker_words), 'body_paragraphs': len(paragraphs),
              'word_range_pass': 120 <= len(words) <= 145,
              'single_paragraph_pass': len(paragraphs) == 1,
              'retained_citation': 'Hennessey and Dionigi (2013)' in body,
              'cl_defined': 'cooperative learning (CL)' in body,
              'utf8_decode_pass': True, 'replacement_character_present': '\ufffd' in text,
              'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'count_method': 'Split body on whitespace; remove Markdown heading lines; hyphenated words and possessives count as one word. The second count uses the supplied prose checker regex.'}
    results.append(result)
print(json.dumps(results, ensure_ascii=False, indent=2))
