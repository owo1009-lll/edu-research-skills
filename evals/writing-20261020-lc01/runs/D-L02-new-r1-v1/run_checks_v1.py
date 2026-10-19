"""Preserved helper version 1: run supplied checkers and record provenance."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
SKILL = ROOT / "variants/v1/skills/edu-writing"
INPUTS = ROOT / "inputs/D-L02"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_new(name, content):
    with (OUT / name).open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(content)


def json_new(name, value):
    write_new(name, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", required=True)
    parser.add_argument("--stage", required=True)
    args = parser.parse_args()
    draft = (OUT / args.draft).resolve()
    if draft.parent != OUT:
        raise ValueError("Draft must be directly inside this run directory")

    if not (OUT / "loaded-resources.json").exists():
        resources = [
            (SKILL / "SKILL.md", ["read"]),
            (SKILL / "references/argument.md", ["read"]),
            (SKILL / "references/voice-en.md", ["read"]),
            (SKILL / "references/qualitative-narrative.md", ["read"]),
            (SKILL.parent / "edu-shared/references/integrity.md", ["read"]),
            (SKILL / "references/methods/cases-develop-explanations.md", ["read"]),
            (SKILL / "references/prose-en.md", ["read"]),
            (SKILL / "scripts/check_voice.py", ["inspected (combined display truncated)", "dependency scan", "executed"]),
            (SKILL / "scripts/check_prose.py", ["inspected (combined display truncated)", "dependency scan", "executed"]),
            (Path(__file__).resolve(), ["authored in this run", "executed"]),
        ]
        json_new("loaded-resources.json", {
            "scope": "Only assigned v1 snapshot resources and this run's helper; Python standard-library modules are not task support resources.",
            "resources": [{"path": str(p), "sha256": digest(p), "access": access} for p, access in resources],
        })
        json_new("task-inputs.json", {
            "inputs": [{"path": str(INPUTS / name), "sha256": digest(INPUTS / name)}
                       for name in ["new-request.md", "source-pack.md"]]
        })

    executions = []
    for checker in ["check_voice", "check_prose"]:
        command = [sys.executable, "-B", str(SKILL / "scripts" / (checker + ".py")), "--draft", str(draft)]
        if checker == "check_voice":
            command += ["--source", str(INPUTS / "source-pack.md")]
        started = datetime.now(timezone.utc).isoformat()
        result = subprocess.run(command, capture_output=True)
        stdout = result.stdout.decode("utf-8", errors="replace")
        stderr = result.stderr.decode("utf-8", errors="replace")
        write_new(args.stage + "-" + checker + ".stdout.txt", stdout)
        write_new(args.stage + "-" + checker + ".stderr.txt", stderr)
        executions.append({"command_argv": command, "started_utc": started,
                           "exit_code": result.returncode, "draft_sha256": digest(draft),
                           "stdout_file": args.stage + "-" + checker + ".stdout.txt",
                           "stderr_file": args.stage + "-" + checker + ".stderr.txt"})
        print(f"{checker}: exit {result.returncode}\n{stdout}")
    json_new(args.stage + "-checker-executions.json", executions)

    text = draft.read_text(encoding="utf-8")
    heading, body = text.split("\n", 1)
    if not heading.startswith("# Attribution:"):
        raise ValueError("Expected initial attribution heading")
    words = re.findall(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*", body)
    summary = {"draft": str(draft), "draft_sha256": digest(draft),
               "excluded": "Initial attribution heading only",
               "word_definition": "Alphanumeric words; internal apostrophes and hyphens stay within a word",
               "body_word_count": len(words), "required_range": [350, 450],
               "in_range": 350 <= len(words) <= 450}
    json_new(args.stage + "-word-count.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if any(item["exit_code"] for item in executions):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
