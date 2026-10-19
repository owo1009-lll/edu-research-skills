"""Run the assigned skill checkers and preserve their actual output."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import subprocess
import sys

OUT = Path(__file__).resolve().parent
BASE = OUT.parent.parent
SKILL = BASE / "variants" / "v2" / "skills" / "edu-writing"
SOURCE = BASE / "inputs" / "D-M02" / "source-pack.md"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

draft = OUT / sys.argv[1]
stage = draft.stem
record_path = OUT / (stage + "-checks.json")
if record_path.exists():
    raise SystemExit("This stage already has a preserved run; use a new stage name.")
records = []
for name, extra in (("check_voice", ["--source", str(SOURCE)]), ("check_prose", [])):
    command = [sys.executable, str(SKILL / "scripts" / (name + ".py")), "--draft", str(draft)] + extra
    started = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(command, capture_output=True, cwd=OUT)
    stdout = OUT / (stage + "-" + name + ".stdout.txt")
    stderr = OUT / (stage + "-" + name + ".stderr.txt")
    stdout.write_bytes(result.stdout)
    stderr.write_bytes(result.stderr)
    entry = {"command_argv": command, "cwd": str(OUT), "started_utc": started,
             "finished_utc": datetime.now(timezone.utc).isoformat(), "exit_code": result.returncode,
             "draft_sha256": sha(draft), "script_sha256": sha(Path(command[1])),
             "stdout": str(stdout), "stderr": str(stderr)}
    records.append(entry)
    print(name + " (exit " + str(result.returncode) + ")")
    print(result.stdout.decode("utf-8", errors="replace"))
    if result.stderr:
        print(result.stderr.decode("utf-8", errors="replace"))
record_path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
body = "\n".join(line for line in draft.read_text(encoding="utf-8").splitlines() if not line.startswith("#"))
words = re.findall(r"\b[^\W_]+(?:['’\-][^\W_]+)*\b", body, flags=re.UNICODE)
count = {"draft": str(draft), "sha256": sha(draft), "body_word_count": len(words),
         "whitespace_word_count": len(body.split()),
         "method": "Unicode letter/number words; internal apostrophes and hyphens retained within one word; Markdown attribution heading excluded.",
         "within_350_450": 350 <= len(words) <= 450}
(OUT / (stage + "-word-count.json")).write_text(json.dumps(count, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
audit_path = OUT / "executed-commands.json"
audit = json.loads(audit_path.read_text(encoding="utf-8"))
audit["checker_commands"].extend(records)
audit.setdefault("helper_commands", []).append({"command_argv": [sys.executable, str(Path(__file__).resolve()), sys.argv[1]], "cwd": str(OUT)})
audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
resources = {}
inputs = {}
for item in audit["read_commands"]:
    path = Path(item["path"])
    target = resources if "variants" in path.parts else inputs
    target[str(path)] = {"path": str(path), "sha256": sha(path),
                         "access": ["read", "executed"] if path.name in ("check_voice.py", "check_prose.py") else ["read"]}
manifest = {"skill_snapshot": str(SKILL), "resources": list(resources.values()),
            "generated_support_resources": [{"path": str(Path(__file__).resolve()), "sha256": sha(Path(__file__)),
                                              "access": ["executed"]}]}
(OUT / "loaded-resources.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(OUT / "task-input-hashes.json").write_text(json.dumps({"inputs": list(inputs.values())}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(count, ensure_ascii=False))
sys.exit(0 if all(r["exit_code"] == 0 for r in records) else 1)
