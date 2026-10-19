"""Check an attributed paragraph with a section heading for the prose checker."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
parser = argparse.ArgumentParser()
parser.add_argument("--draft", required=True)
parser.add_argument("--skill", required=True)
parser.add_argument("--source", required=True)
parser.add_argument("--tag", required=True)
args = parser.parse_args()
draft, skill, source = Path(args.draft), Path(args.skill), Path(args.source)
out = draft.parent / "checks"
out.mkdir(exist_ok=True)
body = "\n".join(line for line in draft.read_text(encoding="utf-8").splitlines() if not line.startswith("#")).strip()
projection = out / (args.tag + ".discussion.md")
projection.write_text("# Discussion\n\n" + body + "\n", encoding="utf-8")
word_count = len(re.findall(r"\S+", body))
report = {
    "draft": str(draft),
    "draft_sha256": hashlib.sha256(draft.read_bytes()).hexdigest(),
    "checker_input": str(projection),
    "projection_note": "The exact saved body with a Discussion heading; attribution omitted.",
    "word_count_method": "Whitespace-delimited body tokens; attribution heading excluded; hyphenated forms count as one.",
    "body_words": word_count,
    "body_paragraphs": len([p for p in re.split(r"\n\s*\n", body) if p.strip()]),
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
    stdout_path = out / (args.tag + "." + name + ".stdout.txt")
    stderr_path = out / (args.tag + "." + name + ".stderr.txt")
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
report_path = out / (args.tag + ".checks.json")
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"body_words": word_count, "body_paragraphs": report["body_paragraphs"], "report": str(report_path)}, ensure_ascii=False))
if any(item["returncode"] for item in report["checker_runs"]):
    raise SystemExit(1)

