"""Count manuscript body and attribution heading separately."""
import argparse
import json
import re
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--draft", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
parser.add_argument("--enforce", action="store_true")
args = parser.parse_args()
text = args.draft.read_text(encoding="utf-8")
lines = text.splitlines()
heading = "\n".join(line for line in lines if line.startswith("# "))
body = "\n".join(line for line in lines if not line.startswith("# ")).strip()
words = re.compile(r"[^\W_]+(?:['’-][^\W_]+)*", re.UNICODE)
body_words = len(words.findall(body))
report = {
    "file": str(args.draft.resolve()),
    "method": "Unicode alphanumeric words; internal hyphens/apostrophes retained; em dashes split; citation years counted",
    "body_words": body_words,
    "attribution_heading_words": len(words.findall(heading)),
    "body_whitespace_tokens": len(body.split()),
    "body_paragraphs": len(re.split(r"\n\s*\n", body)),
    "required_body_range": [140, 170],
    "body_in_range": 140 <= body_words <= 170,
    "one_body_paragraph": len(re.split(r"\n\s*\n", body)) == 1,
}
serialized = json.dumps(report, ensure_ascii=False, indent=2)
args.output.write_text(serialized + "\n", encoding="utf-8")
print(serialized)
if args.enforce and not (report["body_in_range"] and report["one_body_paragraph"]):
    raise SystemExit(1)
