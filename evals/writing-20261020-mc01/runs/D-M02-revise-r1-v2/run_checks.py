"""Run the supplied checkers on the saved paragraph and retain their exact output."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--draft", required=True)
parser.add_argument("--skill", required=True)
parser.add_argument("--source", required=True)
args = parser.parse_args()
draft = Path(args.draft)
skill = Path(args.skill)
source = Path(args.source)
out = draft.parent / "checks"
out.mkdir(exist_ok=True)
text = draft.read_text(encoding="utf-8")
body = "\n".join(line for line in text.splitlines() if not line.startswith("#")).strip()
paragraphs = [p for p in re.split(r"\n\s*\n", body) if p.strip()]
projection = out / (draft.stem + ".body.md")
projection.write_text(body + "\n", encoding="utf-8")
word_count = len(re.findall(r"\S+", body))
report = {
    "draft": str(draft),
    "draft_sha256": hashlib.sha256(draft.read_bytes()).hexdigest(),
    "body_projection": str(projection),
    "word_count_method": "Whitespace-delimited body tokens; attribution heading excluded; hyphenated forms count as one.",
    "body_words": word_count,
    "body_paragraphs": len(paragraphs),
    "within_120_to_145_words": 120 <= word_count <= 145,
    "checker_runs": [],
}
env = os.environ.copy()
env["PYTHONUTF8"] = "1"
env["PYTHONIOENCODING"] = "utf-8"
for name in ("check_voice", "check_prose"):
    checker = skill / "scripts" / (name + ".py")
    argv = [sys.executable, str(checker), "--draft", str(projection)]
    if name == "check_voice":
        argv += ["--source", str(source)]
    result = subprocess.run(argv, capture_output=True, env=env)
    stdout_path = out / (draft.stem + "." + name + ".stdout.txt")
    stderr_path = out / (draft.stem + "." + name + ".stderr.txt")
    stdout_path.write_bytes(result.stdout)
    stderr_path.write_bytes(result.stderr)
    report["checker_runs"].append({
        "argv": argv,
        "returncode": result.returncode,
        "checker_sha256": hashlib.sha256(checker.read_bytes()).hexdigest(),
        "stdout": str(stdout_path),
        "stderr": str(stderr_path),
    })
    print(name + " (exit " + str(result.returncode) + ")")
    print(result.stdout.decode("utf-8"))
    if result.stderr:
        print(result.stderr.decode("utf-8"), file=sys.stderr)
report_path = out / (draft.stem + ".checks.json")
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"body_words": word_count, "body_paragraphs": len(paragraphs), "report": str(report_path)}, ensure_ascii=False))
if any(item["returncode"] for item in report["checker_runs"]):
    raise SystemExit(1)

