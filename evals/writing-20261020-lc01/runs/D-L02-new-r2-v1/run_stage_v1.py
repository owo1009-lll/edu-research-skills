"""Immutable helper: execute supplied checkers and record actual stage outputs."""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import re
import subprocess
import sys

BASE = Path(r"<EXPERIMENT_ROOT>")
OUT = BASE / "runs" / "D-L02-new-r2-v1"
SKILL = BASE / "variants" / "v1" / "skills" / "edu-writing"
SOURCE = BASE / "inputs" / "D-L02" / "source-pack.md"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_new(path, content):
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(content)

parser = argparse.ArgumentParser()
parser.add_argument("stage", choices=["draft-01", "draft-02", "final"])
args = parser.parse_args()
draft = OUT / (args.stage + ".md")
raw = draft.read_text(encoding="utf-8-sig")
lines = raw.splitlines()
if not lines or not lines[0].startswith("# "):
    raise ValueError("Expected the separate initial attribution heading")
body = "\n".join(lines[1:]).strip()
pattern = r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*"
words = re.findall(pattern, body)
count = {"stage": args.stage, "draft_sha256": sha(draft),
         "excluded": "First line: initial attribution heading", "body_word_count": len(words),
         "word_pattern": pattern, "within_requested_350_450": 350 <= len(words) <= 450}
write_new(OUT / (args.stage + "-word-count.json"), json.dumps(count, indent=2) + "\n")
records = []
for name, extra in [("check_voice", ["--source", str(SOURCE)]), ("check_prose", [])]:
    script = SKILL / "scripts" / (name + ".py")
    command = [sys.executable, "-B", str(script), "--draft", str(draft)] + extra
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = subprocess.run(command, capture_output=True, encoding="utf-8", errors="replace")
    stem = args.stage + "-" + name
    write_new(OUT / (stem + ".stdout.txt"), result.stdout)
    write_new(OUT / (stem + ".stderr.txt"), result.stderr)
    records.append({"argv": command, "started_utc": started, "exit_code": result.returncode,
                    "script_sha256": sha(script), "stdout": stem + ".stdout.txt",
                    "stderr": stem + ".stderr.txt"})
write_new(OUT / (args.stage + "-checker-commands.json"), json.dumps(records, indent=2) + "\n")
print(json.dumps(count, indent=2))
for record in records:
    print(record["stdout"] + ": exit " + str(record["exit_code"]))
if any(record["exit_code"] != 0 for record in records):
    sys.exit(1)
