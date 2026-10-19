from pathlib import Path
import json
import re
import subprocess
import sys

OUT = Path(__file__).resolve().parent
SKILL = Path(r"@snapshot\skills\edu-writing")
SOURCE = Path(r"@inputs\D-L01\source-pack.md")
DRAFT = OUT / "draft-01.md"
text = DRAFT.read_text(encoding="utf-8")
prose_input = OUT / "draft-01-prose-input.md"
prose_input.write_text("# Discussion\n\n" + text, encoding="utf-8")
commands = [
    ("check-voice-draft.txt", [sys.executable, "-X", "utf8", str(SKILL / "scripts/check_voice.py"), "--draft", str(DRAFT), "--source", str(SOURCE)]),
    ("check-prose-draft.txt", [sys.executable, "-X", "utf8", str(SKILL / "scripts/check_prose.py"), "--draft", str(prose_input)]),
]
results = []
for log, command in commands:
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="strict")
    (OUT / log).write_text(result.stdout + result.stderr, encoding="utf-8")
    results.append({"command": command, "returncode": result.returncode, "log": log})
    print(log)
    print(result.stdout + result.stderr)
(OUT / "check-execution.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
counts = {"file": DRAFT.name, "paragraphs": len(re.split(r"\n\s*\n", text.strip())), "words": len(re.findall(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*", text)), "method": "Alphanumeric words; internal hyphens and apostrophes retained."}
(OUT / "draft-counts.json").write_text(json.dumps(counts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(counts, ensure_ascii=False))
if any(item["returncode"] for item in results):
    sys.exit(1)
