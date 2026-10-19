import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
SKILL = Path(r"<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing")
SOURCE = Path(r"<EXPERIMENT_ROOT>\inputs\D-M02\source-pack.md")
utc = lambda: datetime.now(timezone.utc).isoformat()
digest = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

stage = sys.argv[1]
draft = OUT / (stage + ".md")
text = draft.read_text(encoding="utf-8")
body = text.split("\n\n## Attribution", 1)[0].strip()
checks = OUT / "checks"
checks.mkdir(exist_ok=True)
checker_input = checks / (stage + ".body.md")
checker_input.write_text("# Discussion\n\n" + body + "\n", encoding="utf-8")
count = len(body.split())
results = {"stage": stage, "at_utc": utc(), "draft_sha256": digest(draft), "word_count": count,
           "count_rule": "Whitespace-delimited body tokens, including the in-text citation and excluding Attribution heading and all attribution content.",
           "body_paragraphs": len(re.split(r"\n\s*\n", body)),
           "within_120_145_words": 120 <= count <= 145,
           "checker_input": str(checker_input), "commands": []}
for script in ("check_voice.py", "check_prose.py"):
    command = [sys.executable, str(SKILL / "scripts" / script), "--draft", str(checker_input)]
    if script == "check_voice.py":
        command += ["--source", str(SOURCE)]
    result = subprocess.run(command, capture_output=True, encoding="utf-8")
    stem = stage + "." + script.removesuffix(".py")
    (checks / (stem + ".stdout.txt")).write_text(result.stdout, encoding="utf-8")
    (checks / (stem + ".stderr.txt")).write_text(result.stderr, encoding="utf-8")
    entry = {"at_utc": utc(), "argv": command, "exit_code": result.returncode,
             "script_sha256": digest(SKILL / "scripts" / script),
             "stdout": str(checks / (stem + ".stdout.txt")), "stderr": str(checks / (stem + ".stderr.txt"))}
    results["commands"].append(entry)
    with (OUT / "executed-commands.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(script + ":\n" + result.stdout)
save(checks / (stage + ".validation.json"), results)

manifest = json.loads((OUT / "resource-read-record.json").read_text(encoding="utf-8"))
resources = []
for entry in manifest["resources"]:
    entry = dict(entry)
    entry["sha256"] = digest(entry["path"])
    if entry["path"].endswith(("check_voice.py", "check_prose.py")):
        entry["actions"] = ["read", "executed"]
    resources.append(entry)
save(OUT / "loaded-resources.json", {"hash_algorithm": "SHA-256", "resources": resources,
     "scope_note": "Only listed skill snapshot resources were loaded. Checkers use standard-library imports and no additional skill files."})
save(OUT / "task-input-hashes.json", {"hash_algorithm": "SHA-256", "inputs":
     [dict(entry, sha256=digest(entry["path"])) for entry in manifest["inputs"]]})
print(json.dumps({k: v for k, v in results.items() if k != "commands"}, ensure_ascii=False, indent=2))

