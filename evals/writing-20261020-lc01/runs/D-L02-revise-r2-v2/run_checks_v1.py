"""Run the assigned checkers once for a named saved stage; preserve all output."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SNAPSHOT = Path(r"<EXPERIMENT_ROOT>\variants\v2\skills")
INPUTS = Path(r"<EXPERIMENT_ROOT>\inputs\D-L02")

ap = argparse.ArgumentParser()
ap.add_argument("--draft", required=True)
ap.add_argument("--stage", required=True)
args = ap.parse_args()
draft = ROOT / args.draft
stage = args.stage
report_path = ROOT / f"{stage}-execution.json"
if report_path.exists():
    raise SystemExit("Refusing to overwrite an existing execution record")

text = draft.read_text(encoding="utf-8")
lines = text.splitlines()
assert lines[0].startswith("# "), "Expected separate attribution heading"
body = "\n".join(lines[1:]).strip()
paragraphs = [p for p in body.split("\n\n") if p.strip()]
report = {
    "invocation": [sys.executable, str(Path(__file__).resolve()), *sys.argv[1:]],
    "helper_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "draft": str(draft),
    "draft_sha256": hashlib.sha256(draft.read_bytes()).hexdigest(),
    "word_count_method": "Whitespace-delimited body words; initial attribution heading excluded; citations included",
    "body_word_count": len(body.split()),
    "body_paragraph_count": len(paragraphs),
    "commands": [],
}
for checker in ("check_voice", "check_prose"):
    script = SNAPSHOT / "edu-writing" / "scripts" / f"{checker}.py"
    command = [sys.executable, str(script), "--draft", str(draft)]
    if checker == "check_voice":
        command += ["--source", str(INPUTS / "source-pack.md"), str(INPUTS / "original.md")]
    completed = subprocess.run(command, capture_output=True, encoding="utf-8", errors="replace")
    stdout_path = ROOT / f"{stage}-{checker}.stdout.txt"
    stderr_path = ROOT / f"{stage}-{checker}.stderr.txt"
    stdout_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")
    report["commands"].append({
        "argv": command,
        "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        "exit_code": completed.returncode,
        "stdout": str(stdout_path),
        "stderr": str(stderr_path),
    })
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, indent=2))
for item in report["commands"]:
    print(Path(item["stdout"]).read_text(encoding="utf-8"))
    if item["exit_code"]:
        print(Path(item["stderr"]).read_text(encoding="utf-8"))
if any(item["exit_code"] for item in report["commands"]):
    raise SystemExit(1)
