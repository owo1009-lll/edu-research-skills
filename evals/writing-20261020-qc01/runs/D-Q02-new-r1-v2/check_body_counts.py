"""Count the attribution heading separately from the manuscript body."""
from pathlib import Path
import argparse
import json
import re

parser = argparse.ArgumentParser()
parser.add_argument("draft", type=Path)
args = parser.parse_args()
text = args.draft.read_text(encoding="utf-8-sig")
heading, separator, body = text.partition("\n\n")
assert heading.startswith("# ") and separator, "Expected one attribution heading."
assert not any(line.startswith("#") for line in body.splitlines()), "Unexpected body subheading."
count = lambda value: len(re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+(?:[’'.,–-][A-Za-zÀ-ÖØ-öø-ÿ0-9]+)*", value))
result = {
    "file": str(args.draft.resolve()),
    "method": "Letter/number tokens; internal apostrophes, commas, periods, hyphens and en dashes stay within a word.",
    "body_words": count(body),
    "attribution_heading_words": count(heading.removeprefix("# ")),
    "body_whitespace_tokens": len(body.split()),
    "attribution_heading_whitespace_tokens": len(heading.removeprefix("# ").split()),
    "body_paragraphs": len([paragraph for paragraph in body.split("\n\n") if paragraph.strip()]),
    "body_within_450_550": 450 <= count(body) <= 550,
}
print(json.dumps(result, ensure_ascii=False, indent=2))
