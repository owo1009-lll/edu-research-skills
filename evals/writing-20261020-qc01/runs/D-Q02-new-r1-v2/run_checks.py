"""Preserve checker output and normalize resource records for this isolated run."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys

OUT = Path(__file__).resolve().parent
SKILLS = Path("<EXPERIMENT_ROOT>/variants/v2/skills")
SOURCE = Path("<EXPERIMENT_ROOT>/inputs/D-Q02/source-pack.md")
MANIFEST = OUT / "loaded-resources.json"

def flatten(value):
    if isinstance(value, list):
        for item in value:
            yield from flatten(item)
    elif isinstance(value, dict):
        if "path" in value:
            yield value
        elif "value" in value:
            yield from flatten(value["value"])

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

records = {}
raw = json.loads(MANIFEST.read_text(encoding="utf-8-sig"))
if any("value" in item for item in raw) and not (OUT / "loaded-resources-before-normalization.json").exists():
    shutil.copyfile(MANIFEST, OUT / "loaded-resources-before-normalization.json")
for item in flatten(raw):
    path = Path(item["path"]).as_posix()
    item["path"] = path
    if path in records:
        records[path]["actions"] = sorted(set(records[path]["actions"] + item["actions"]))
    else:
        records[path] = item
    assert item["sha256"] == digest(path), f"Resource hash mismatch: {path}"

def resource(path, action, purpose):
    path = Path(path).as_posix()
    if path not in records:
        records[path] = {"path": path, "sha256": digest(path), "actions": [], "purpose": purpose}
    records[path]["actions"] = sorted(set(records[path]["actions"] + [action]))
    records[path]["purpose"] = purpose

def log(value):
    with (OUT / "commands.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, ensure_ascii=False) + "\n")

def run(script, arguments, output):
    command = [sys.executable, str(script), *map(str, arguments)]
    process = subprocess.run(command, capture_output=True)
    (OUT / output).write_bytes(process.stdout)
    (OUT / (output + ".stderr.txt")).write_bytes(process.stderr)
    log({"stage": sys.argv[1], "program": command[0], "arguments": command[1:], "exit_code": process.returncode, "output": output, "stderr": output + ".stderr.txt"})
    resource(script, "executed", "Required checker or body/heading count helper")
    print(f"OUTPUT: {output}; exit={process.returncode}")
    print(process.stdout.decode("utf-8"))
    if process.stderr:
        print(process.stderr.decode("utf-8"), file=sys.stderr)
    if process.returncode:
        raise SystemExit(process.returncode)

resource(__file__, "executed", "Checker runner and resource-record normalization")
log({"stage": sys.argv[1], "program": sys.executable, "arguments": [str(Path(__file__).resolve()), *sys.argv[1:]], "role": "orchestrator"})
stage = sys.argv[1]
draft = OUT / ("draft-01.md" if stage == "first-draft-diagnostic" else "final.md")
heading, separator, body = draft.read_text(encoding="utf-8-sig").partition("\n\n")
assert separator and heading.startswith("# ")
view = OUT / (draft.stem + "-checker-view.md")
view.write_text("# Discussion\n\n" + body, encoding="utf-8")
assert view.read_text(encoding="utf-8").partition("\n\n")[2] == body
log({"stage": stage, "operation": "create-checker-view", "source": str(draft), "destination": str(view), "body_identical": True, "only_change": "Replace attribution heading with # Discussion for section recognition"})
if stage == "first-draft-diagnostic":
    run(SKILLS / "edu-writing/scripts/check_prose.py", ["--draft", view], "draft-01-check-prose-discussion.txt")
elif stage == "final-verification":
    run(SKILLS / "edu-writing/scripts/check_voice.py", ["--draft", draft, "--source", SOURCE], "final-check-voice.txt")
    run(SKILLS / "edu-writing/scripts/check_prose.py", ["--draft", draft], "final-check-prose.txt")
    run(SKILLS / "edu-writing/scripts/check_prose.py", ["--draft", view], "final-check-prose-discussion.txt")
    run(OUT / "check_body_counts.py", [draft], "final-word-count.json")
else:
    raise SystemExit(f"Unknown stage: {stage}")
MANIFEST.write_text(json.dumps(list(records.values()), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
