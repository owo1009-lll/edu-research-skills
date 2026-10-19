"""Run the supplied checkers and retain their actual outputs and file hashes."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess
import sys

OUT = Path(__file__).resolve().parent
BASE = OUT.parent.parent
SKILLS = BASE / "variants" / "v1" / "skills"
INPUT = BASE / "inputs" / "D-Q02"


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(event):
    with (OUT / "executed-commands.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event, ensure_ascii=False) + "\n")


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


stage = sys.argv[1]
draft = OUT / stage
if not draft.is_file():
    raise FileNotFoundError(draft)
record({"time_utc": now(), "kind": "audit invocation", "argv": sys.orig_argv, "cwd": str(OUT)})

relative_resources = [
    ("edu-writing/SKILL.md", "read"),
    ("edu-writing/references/foundation.md", "read"),
    ("edu-writing/references/argument.md", "read"),
    ("edu-writing/references/voice-en.md", "read"),
    ("edu-writing/references/quantitative-discussion.md", "read"),
    ("edu-writing/references/framing-results.md", "read"),
    ("edu-shared/references/integrity.md", "read"),
    ("edu-writing/scripts/check_voice.py", "read and executed"),
    ("edu-writing/scripts/check_prose.py", "read and executed"),
]
resources = [{"path": str(SKILLS / rel), "sha256": digest(SKILLS / rel), "use": use} for rel, use in relative_resources]
resources.append({"path": str(Path(__file__).resolve()), "sha256": digest(Path(__file__)), "use": "task-local audit support, executed"})
write_json(OUT / "loaded-resources.json", {"snapshot": "v1", "resources": resources, "note": "Only this snapshot was used. Initial bulk reads had truncated display; applicable instruction files were reread in smaller batches. Checker scripts were executed in full. No linked article or external reference was opened."})
write_json(OUT / "input-file-hashes.json", [{"path": str(INPUT / name), "sha256": digest(INPUT / name)} for name in ["revise-request.md", "source-pack.md", "original.md"]])

text = draft.read_text(encoding="utf-8")
heading = "\n".join(line.lstrip("# ") for line in text.splitlines() if line.startswith("#"))
body = "\n".join(line for line in text.splitlines() if not line.startswith("#")).strip()
words = lambda value: re.findall(r"\b\w+(?:[’'-]\w+)*\b", value, flags=re.UNICODE)
counts = {
    "file": str(draft),
    "sha256": digest(draft),
    "rule": "Unicode word tokens; internal straight/curly apostrophes and hyphens remain in a word; citation names and years count. Markdown heading markers and standalone punctuation do not count.",
    "manuscript_body_words": len(words(body)),
    "attribution_heading_words": len(words(heading)),
    "body_plus_attribution_words": len(words(body)) + len(words(heading)),
    "body_whitespace_words": len(body.split()),
    "body_paragraphs": len([p for p in re.split(r"\n\s*\n", body) if p.strip()]),
    "requested_range": [140, 170],
    "body_in_range": 140 <= len(words(body)) <= 170,
}
write_json(OUT / (draft.stem + ".word-count.json"), counts)
print(json.dumps(counts, ensure_ascii=False, indent=2))

for checker in ["check_voice.py", "check_prose.py"]:
    argv = [sys.executable, str(SKILLS / "edu-writing" / "scripts" / checker), "--draft", str(draft)]
    if checker == "check_voice.py":
        argv += ["--source", str(INPUT / "source-pack.md"), str(INPUT / "original.md")]
    started = now()
    completed = subprocess.run(argv, cwd=OUT, capture_output=True, encoding="utf-8", errors="strict")
    output_file = OUT / (draft.stem + "." + checker.removesuffix(".py") + ".txt")
    output_file.write_text(completed.stdout, encoding="utf-8")
    error_file = OUT / (draft.stem + "." + checker.removesuffix(".py") + ".stderr.txt")
    error_file.write_text(completed.stderr, encoding="utf-8")
    record({"started_utc": started, "finished_utc": now(), "argv": argv, "cwd": str(OUT), "returncode": completed.returncode, "stdout": str(output_file), "stderr": str(error_file), "draft_sha256": digest(draft), "script_sha256": digest(SKILLS / "edu-writing" / "scripts" / checker)})
    print("\n" + checker + " exit=" + str(completed.returncode))
    print(completed.stdout)
    if completed.stderr:
        print(completed.stderr, file=sys.stderr)
    if completed.returncode:
        raise SystemExit(completed.returncode)
