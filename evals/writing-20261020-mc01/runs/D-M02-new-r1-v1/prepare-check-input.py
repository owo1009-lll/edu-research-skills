"""Prepare a checker-only heading and count body words without attribution."""
from pathlib import Path
import hashlib
import json
import re
import sys

draft = Path(sys.argv[1])
text = draft.read_text(encoding="utf-8")
heading, body = text.split("\n", 1)
assert heading.startswith("# Secondary-writing demonstration"), heading
body = body.lstrip("\n")
check_input = draft.with_name(draft.stem + ".check-input.md")
check_input.write_text("# Discussion\n\n" + body, encoding="utf-8")
record = {
    "draft": str(draft.resolve()),
    "excluded_attribution_heading": heading,
    "body_word_count": len(body.split()),
    "count_method": "Whitespace-delimited body words; hyphenated forms count as one; attribution heading excluded.",
    "unicode_lexical_token_count": len(re.findall(r"[^\W_]+(?:[’'-][^\W_]+)*", body)),
    "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
    "checker_input": str(check_input.resolve()),
    "checker_input_transformation": "Replace attribution heading with Discussion; preserve body exactly.",
}
record_path = draft.with_name(draft.stem + ".word-count.json")
record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
print(json.dumps(record, ensure_ascii=False, indent=2))
