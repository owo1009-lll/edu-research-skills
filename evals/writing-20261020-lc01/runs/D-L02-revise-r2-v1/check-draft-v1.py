"""Run the assigned skill checkers and preserve their actual output."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SKILL = Path(r"<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing")
SOURCE = Path(r"<EXPERIMENT_ROOT>\inputs\D-L02\source-pack.md")
draft = ROOT / sys.argv[1]
stage = sys.argv[2]
text = draft.read_text(encoding="utf-8")
heading, body = text.split("\n", 1)
body = body.strip()
word_report = {
    "file": str(draft),
    "sha256": hashlib.sha256(draft.read_bytes()).hexdigest(),
    "method": "Whitespace-delimited body words; initial attribution heading excluded",
    "body_words": len(body.split()),
    "body_paragraphs": len([p for p in body.split("\n\n") if p.strip()]),
    "within_90_110": 90 <= len(body.split()) <= 110,
}
(ROOT / f"{stage}-word-count.json").write_text(json.dumps(word_report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(word_report, indent=2))
records = []
for name, extra in (("check_voice", ["--source", str(SOURCE)]), ("check_prose", [])):
    command = [sys.executable, str(SKILL / "scripts" / f"{name}.py"), "--draft", str(draft), *extra]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    out = ROOT / f"{stage}-{name}.stdout.txt"
    err = ROOT / f"{stage}-{name}.stderr.txt"
    out.write_text(result.stdout, encoding="utf-8")
    err.write_text(result.stderr, encoding="utf-8")
    records.append({"argv": command, "returncode": result.returncode, "stdout": str(out), "stderr": str(err)})
    print(f"\n{name}: exit {result.returncode}\n{result.stdout}")
(ROOT / f"{stage}-checker-commands.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
if any(record["returncode"] for record in records):
    raise SystemExit(1)
