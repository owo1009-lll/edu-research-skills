"""Count the attribution separately from the manuscript body."""
import json
import re
import sys
from pathlib import Path


def count(text):
    return len(re.findall(r"\b\w+(?:[’'-]\w+|,\d+)*\b", text, re.UNICODE))


reports = []
for filename in sys.argv[1:]:
    text = Path(filename).read_text(encoding="utf-8-sig")
    heading, separator, body = text.partition("\n\n")
    if not separator or not heading.startswith("# "):
        raise ValueError(f"Expected a separate attribution heading: {filename}")
    body_count = count(body)
    reports.append({
        "file": filename,
        "attribution_heading_words": count(heading),
        "manuscript_body_words": body_count,
        "total_words": count(text),
        "body_within_450_550": 450 <= body_count <= 550,
        "method": "Unicode word tokens; internal apostrophes, hyphens, and numeral commas stay joined",
    })
print(json.dumps(reports, ensure_ascii=False, indent=2))
