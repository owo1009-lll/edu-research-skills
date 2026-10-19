"""Run snapshot checkers, preserve their outputs, and count the body separately."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SKILL = ROOT.parents[1] / "variants" / "v2" / "skills" / "edu-writing"
SOURCE = ROOT.parents[1] / "inputs" / "D-Q02" / "source-pack.md"


def words(text):
    # Whitespace-delimited lexical tokens; hyphenated words and numerals count once.
    return sum(any(character.isalnum() for character in token) for token in text.split())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage")
    args = parser.parse_args()
    draft = ROOT / f"{args.stage}.md"
    text = draft.read_text(encoding="utf-8")
    lines = text.splitlines()
    assert lines[0].startswith("# "), "Expected a separate attribution heading"
    heading = lines[0][2:]
    body = "\n".join(lines[1:]).strip()
    checks = ROOT / "checks"
    checks.mkdir(exist_ok=True)
    counts = {
        "file": str(draft),
        "sha256": hashlib.sha256(draft.read_bytes()).hexdigest(),
        "convention": "Whitespace-delimited tokens containing a Unicode letter or number; hyphenated words and numerals count once.",
        "body_words": words(body),
        "attribution_heading_words": words(heading),
        "body_plus_attribution_words": words(body) + words(heading),
        "body_paragraphs": len(body.split("\n\n")),
        "body_within_450_550": 450 <= words(body) <= 550,
        "unicode_replacement_character_present": "\ufffd" in text,
    }
    (checks / f"{args.stage}-word-count.json").write_text(json.dumps(counts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # This input keeps the exact body but supplies a recognisable discussion label.
    # It is a checker adapter, never a revised manuscript draft.
    adapted = checks / f"{args.stage}-discussion-input.md"
    adapted.write_text("# Discussion\n\n" + body + "\n", encoding="utf-8")
    jobs = [
        ("voice", [sys.executable, "-X", "utf8", str(SKILL / "scripts" / "check_voice.py"), "--draft", str(draft), "--source", str(SOURCE)]),
        ("prose", [sys.executable, "-X", "utf8", str(SKILL / "scripts" / "check_prose.py"), "--draft", str(draft)]),
        ("prose-discussion", [sys.executable, "-X", "utf8", str(SKILL / "scripts" / "check_prose.py"), "--draft", str(adapted)]),
    ]
    executions = []
    for name, argv in jobs:
        result = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="strict")
        stdout_path = checks / f"{args.stage}-{name}.stdout.txt"
        stderr_path = checks / f"{args.stage}-{name}.stderr.txt"
        stdout_path.write_text(result.stdout, encoding="utf-8")
        stderr_path.write_text(result.stderr, encoding="utf-8")
        executions.append({"argv": argv, "display_command": subprocess.list2cmdline(argv), "exit_code": result.returncode,
                           "stdout": str(stdout_path), "stderr": str(stderr_path)})
        print(json.dumps({"checker": name, "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}, ensure_ascii=False))
    (checks / f"{args.stage}-executed-commands.json").write_text(json.dumps(executions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(counts, ensure_ascii=False))
    if any(item["exit_code"] for item in executions):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
