import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

RUN = Path(r"<EXPERIMENT_ROOT>\runs\D-L02-revise-r1-v1")
SKILL = Path(r"<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing")
INPUT = Path(r"<EXPERIMENT_ROOT>\inputs\D-L02")
RESOURCES = [
    r"<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\SKILL.md",
    r"<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\references\foundation.md",
    r"<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\references\argument.md",
    r"<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\references\voice-en.md",
    r"<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\references\qualitative-narrative.md",
    r"<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\..\edu-shared\references\integrity.md",
    r"<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\scripts\check_voice.py",
    r"<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\scripts\check_prose.py",
]
INPUT_NAMES = ["revise-request.md", "source-pack.md", "original.md"]

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def save_json(path, value):
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite audit artifact: {path}")
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", required=True)
    parser.add_argument("--stage", required=True, choices=["first", "final", "corrected"])
    args = parser.parse_args()
    draft = (RUN / args.draft).resolve()
    if draft.parent != RUN.resolve():
        raise ValueError("Draft must be directly inside this run directory.")
    checks = RUN / "checks"
    checks.mkdir(exist_ok=True)
    resource_records = [
        {
            "path": str(Path(p).resolve()),
            "sha256": sha(p),
            "access": ["read", "executed"] if Path(p).name in ("check_voice.py", "check_prose.py") else ["read"],
            "kind": "skill" if Path(p).name == "SKILL.md" else "support",
        }
        for p in RESOURCES
    ]
    resource_records.append({
        "path": str((RUN / "audit-runner-v1.py").resolve()),
        "sha256": sha(RUN / "audit-runner-v1.py"),
        "access": ["created", "executed"],
        "kind": "local_helper",
    })
    resource_records.append({
        "path": str(Path(__file__).resolve()),
        "sha256": sha(__file__),
        "access": ["created", "executed"],
        "kind": "local_helper",
    })
    input_records = [{"path": str(INPUT / name), "sha256": sha(INPUT / name)} for name in INPUT_NAMES]
    if args.stage == "first":
        save_json(RUN / "loaded-resources.json", {"algorithm": "SHA-256", "resources": resource_records})
        save_json(RUN / "task-input-hashes.json", {"algorithm": "SHA-256", "inputs": input_records})
    else:
        original_resources = json.loads((RUN / "loaded-resources.json").read_text(encoding="utf-8"))
        original_inputs = json.loads((RUN / "task-input-hashes.json").read_text(encoding="utf-8"))
        current_by_path = {r["path"]: r for r in resource_records}
        save_json(checks / f"{args.stage}-manifest-check.json", {
            "previous_resource_hashes_unchanged": all(current_by_path[r["path"]]["sha256"] == r["sha256"] for r in original_resources["resources"]),
            "inputs_unchanged": original_inputs["inputs"] == input_records,
            "added_helper": str(Path(__file__).resolve()),
        })
        (RUN / "loaded-resources.json").write_text(json.dumps({"algorithm": "SHA-256", "resources": resource_records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    commands = [
        [sys.executable, "-B", str(SKILL / "scripts" / "check_voice.py"), "--draft", str(draft),
         "--source", str(INPUT / "source-pack.md"), str(INPUT / "original.md")],
        [sys.executable, "-B", str(SKILL / "scripts" / "check_prose.py"), "--draft", str(draft)],
    ]
    entries = []
    for command in commands:
        script_name = Path(command[2]).stem
        started = datetime.now(timezone.utc).isoformat()
        result = subprocess.run(command, cwd=str(RUN), capture_output=True, text=True, encoding="utf-8")
        stdout_path = checks / f"{args.stage}-{script_name}.stdout.txt"
        stderr_path = checks / f"{args.stage}-{script_name}.stderr.txt"
        for path, value in [(stdout_path, result.stdout), (stderr_path, result.stderr)]:
            if path.exists():
                raise FileExistsError(path)
            path.write_text(value, encoding="utf-8")
        entries.append({
            "argv": command, "cwd": str(RUN), "started_utc": started,
            "exit_code": result.returncode, "script_sha256": sha(command[2]),
            "draft_sha256": sha(draft), "stdout_path": str(stdout_path), "stderr_path": str(stderr_path),
        })
        print(script_name + ":")
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
    save_json(checks / f"{args.stage}-executed-commands.json", {
        "helper_argv": sys.argv,
        "helper_path": str(Path(__file__).resolve()),
        "helper_sha256": sha(__file__),
        "commands": entries,
    })
    text = draft.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        raise ValueError("Expected separate initial attribution heading.")
    body = "\n".join(lines[1:]).strip()
    paragraphs = [p for p in body.split("\n\n") if p.strip()]
    word_count = len(body.split())
    counts = {
        "draft": str(draft), "draft_sha256": sha(draft),
        "method": "Whitespace-delimited body words; initial attribution heading excluded.",
        "body_words": word_count, "body_paragraphs": len(paragraphs),
        "within_90_to_110": 90 <= word_count <= 110,
        "single_body_paragraph": len(paragraphs) == 1,
    }
    save_json(checks / f"{args.stage}-word-count.json", counts)
    print(json.dumps(counts, indent=2))
    if any(e["exit_code"] != 0 for e in entries):
        raise SystemExit(1)
    if not counts["within_90_to_110"] or not counts["single_body_paragraph"]:
        raise SystemExit(2)

if __name__ == "__main__":
    main()

