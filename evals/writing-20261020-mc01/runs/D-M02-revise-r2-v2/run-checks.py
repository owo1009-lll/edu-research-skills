from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent.parent
SKILL = BASE / "variants" / "v2" / "skills" / "edu-writing"
SOURCE = BASE / "inputs" / "D-M02" / "source-pack.md"

parser = argparse.ArgumentParser()
parser.add_argument("--draft", required=True)
args = parser.parse_args()
draft = ROOT / args.draft
text = draft.read_text(encoding="utf-8")
body = text.split("## Attribution", 1)[0]
body = "\n".join(line for line in body.splitlines() if not line.startswith("#")).strip()
check_dir = ROOT / "checks" / draft.stem
check_dir.mkdir(parents=True, exist_ok=True)
check_input = check_dir / "body.md"
check_input.write_text("# Discussion\n\n" + body + "\n", encoding="utf-8")
metrics = {
    "draft": str(draft),
    "draft_sha256": hashlib.sha256(draft.read_bytes()).hexdigest(),
    "body_words_whitespace": len(body.split()),
    "body_words_regex": len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’.-]*", body)),
    "body_paragraphs": len(re.split(r"\n\s*\n", body)),
    "count_excludes": "Discussion heading and separate Attribution heading and its contents",
}
(check_dir / "word-count.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
records = []
for name in ("check_voice", "check_prose"):
    command = [sys.executable, str(SKILL / "scripts" / (name + ".py")), "--draft", str(check_input)]
    if name == "check_voice":
        command += ["--source", str(SOURCE)]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
    (check_dir / (name + ".stdout.txt")).write_text(result.stdout, encoding="utf-8")
    (check_dir / (name + ".stderr.txt")).write_text(result.stderr, encoding="utf-8")
    records.append({"argv": command, "exit_code": result.returncode,
                    "stdout": str(check_dir / (name + ".stdout.txt")),
                    "stderr": str(check_dir / (name + ".stderr.txt"))})
    print(name + ": exit " + str(result.returncode))
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
(check_dir / "executed-commands.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
print(json.dumps(metrics, indent=2))
if any(record["exit_code"] for record in records):
    raise SystemExit(1)
