"""Immutable helper for this isolated run; all outputs stay beside this file."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys

OUT = Path(__file__).resolve().parent
BASE = OUT.parent.parent
SKILLS = BASE / "variants" / "v2" / "skills"
INPUTS = BASE / "inputs" / "D-L02"

RESOURCE_FILES = [
    "edu-writing/SKILL.md",
    "edu-writing/references/foundation.md",
    "edu-writing/references/argument.md",
    "edu-writing/references/voice-en.md",
    "edu-writing/references/qualitative-narrative.md",
    "edu-shared/references/integrity.md",
    "edu-writing/scripts/check_voice.py",
    "edu-writing/scripts/check_prose.py",
]

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_json(name, data):
    path = OUT / name
    if path.exists():
        raise FileExistsError(str(path))
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def log(record):
    with (OUT / "executed-commands.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")

def bootstrap_reads():
    start = [SKILLS / RESOURCE_FILES[0], INPUTS / "revise-request.md", INPUTS / "source-pack.md", INPUTS / "original.md"]
    records = []
    for encoding in ["", " -Encoding UTF8"]:
        for path in start:
            records.append({"command": "Get-Content -LiteralPath '" + str(path) + "'" + encoding + " -Raw", "exit_code": 0})
    for rel in RESOURCE_FILES[1:]:
        records.append({"command": "Get-Content -LiteralPath '" + str(SKILLS / rel) + "' -Encoding UTF8 -Raw", "exit_code": 0})
    for rel in RESOURCE_FILES[3:6]:
        records.append({"command": "Get-Content -LiteralPath '" + str(SKILLS / rel) + "' -Encoding UTF8 -Raw", "exit_code": 0})
    records.append({"command": "Get-Content -LiteralPath '" + str(SKILLS / RESOURCE_FILES[6]) + "' -Encoding UTF8 -Raw", "exit_code": 0})
    records.append({"command": "Get-Content -LiteralPath '" + str(SKILLS / RESOURCE_FILES[7]) + "' -Encoding UTF8 -TotalCount 90", "exit_code": 0})
    records.append({"command": "rg -n '^(import|from)|read_text|read_bytes|open\\(|Path\\(|load\\(' '" + str(SKILLS / RESOURCE_FILES[7]) + "' '" + str(SKILLS / RESOURCE_FILES[6]) + "'", "exit_code": 0})
    write_json("initial-read-commands.json", {
        "record_type": "Exact shell commands already executed before the helper was created; timestamps were not captured.",
        "notes": "The initial four PowerShell reads used the default encoding and produced mojibake; explicit UTF-8 reads followed. A large combined result was truncated, followed by focused rereads. These are command records, not reconstructed drafting stages.",
        "commands": records,
        "edits_before_helper": [
            {"tool": "tools.apply_patch", "created": ["rationale.md", "draft-01.md", "notes.md"]},
            {"tool": "tools.apply_patch", "created": ["audit-run-v1.py"]},
        ],
    })

def initialize():
    bootstrap_reads()
    write_json("loaded-resources.json", {
        "scope": "Assigned v2 skill/support files actually read, plus the immutable helper executed for this run. Standard-library implementation files are not task resources.",
        "resources": [{"path": str(SKILLS / rel), "sha256": digest(SKILLS / rel), "access": "read"} for rel in RESOURCE_FILES],
        "generated_helpers": [{"path": str(Path(__file__).resolve()), "sha256": digest(Path(__file__).resolve()), "access": "executed", "version": "v1"}],
        "execution_records": "executed-commands.jsonl records actual checker invocations separately from resource loading.",
    })
    write_json("task-input-hashes.json", {
        "inputs": [{"path": str(INPUTS / name), "sha256": digest(INPUTS / name)} for name in ["revise-request.md", "source-pack.md", "original.md"]]
    })

def metrics(draft_name):
    path = OUT / draft_name
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    assert lines and lines[0].startswith("# "), "Initial attribution heading is required"
    body = "\n".join(lines[1:]).strip()
    paragraphs = [p for p in body.split("\n\n") if p.strip()]
    result = {"path": str(path), "sha256": digest(path), "method": "Whitespace-delimited body words; the separate initial attribution heading is excluded.", "body_words": len(body.split()), "body_paragraphs": len(paragraphs), "within_90_110_words": 90 <= len(body.split()) <= 110, "initial_heading": lines[0]}
    write_json(path.stem + "-metrics.json", result)
    print(json.dumps(result, ensure_ascii=False))
    return result

def check(draft_name):
    metrics(draft_name)
    checks = OUT / "checks"
    checks.mkdir(exist_ok=True)
    for script in ["check_voice.py", "check_prose.py"]:
        argv = [sys.executable, "-B", str(SKILLS / "edu-writing" / "scripts" / script), "--draft", str(OUT / draft_name)]
        if script == "check_voice.py":
            argv += ["--source", str(INPUTS / "source-pack.md"), str(INPUTS / "original.md")]
        prefix = checks / (Path(draft_name).stem + "-" + Path(script).stem)
        stdout_path = prefix.with_suffix(".stdout.txt")
        stderr_path = prefix.with_suffix(".stderr.txt")
        if stdout_path.exists() or stderr_path.exists():
            raise FileExistsError(str(prefix))
        start = now()
        completed = subprocess.run(argv, cwd=OUT, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8"}, capture_output=True)
        stdout_path.write_bytes(completed.stdout)
        stderr_path.write_bytes(completed.stderr)
        log({"kind": "checker", "started_utc": start, "finished_utc": now(), "argv": argv, "windows_command": subprocess.list2cmdline(argv), "cwd": str(OUT), "exit_code": completed.returncode, "script_sha256": digest(Path(argv[2])), "draft_sha256": digest(OUT / draft_name), "stdout": str(stdout_path), "stderr": str(stderr_path)})
        print(script + ": exit " + str(completed.returncode))
        print(completed.stdout.decode("utf-8", errors="replace"))
        if completed.stderr:
            print(completed.stderr.decode("utf-8", errors="replace"))
        if completed.returncode:
            raise RuntimeError("Checker failed")

def validate():
    final = metrics("final.md")
    assert final["within_90_110_words"] and final["body_paragraphs"] == 1
    assert (OUT / "draft-02.md").read_bytes() == (OUT / "final.md").read_bytes()
    loaded = json.loads((OUT / "loaded-resources.json").read_text(encoding="utf-8"))
    inputs = json.loads((OUT / "task-input-hashes.json").read_text(encoding="utf-8"))
    for item in loaded["resources"] + loaded["generated_helpers"] + inputs["inputs"]:
        assert digest(Path(item["path"])) == item["sha256"], "Resource or input changed"
    report = {"validated_utc": now(), "final_body_words": final["body_words"], "single_body_paragraph": True, "final_matches_actual_second_draft": True, "resource_input_and_helper_hashes_unchanged": True, "required_records_present": all((OUT / name).exists() for name in ["draft-01.md", "draft-02.md", "self-review.md", "rationale.md", "notes.md", "loaded-resources.json", "task-input-hashes.json", "executed-commands.jsonl"])}
    write_json("validation.json", report)
    print(json.dumps(report, ensure_ascii=False))

if __name__ == "__main__":
    log({"kind": "helper", "time_utc": now(), "argv": [sys.executable] + sys.argv, "invoked_shell_command": "python -B '" + str(Path(__file__).resolve()) + "' " + " ".join(sys.argv[1:]), "helper_sha256": digest(Path(__file__).resolve()), "cwd": str(OUT)})
    mode = sys.argv[1]
    if mode == "initialize":
        initialize()
    elif mode == "check":
        check(sys.argv[2])
    elif mode == "validate":
        validate()
    else:
        raise ValueError(mode)
