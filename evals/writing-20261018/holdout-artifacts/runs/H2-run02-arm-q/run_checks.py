from pathlib import Path
import concurrent.futures
import json
import subprocess
import sys

OUT = Path(__file__).resolve().parent
SKILL = Path(r"C:/Users/Administrator/Downloads/edu-writing-snapshot-q01-20261018/skills/edu-writing")
SOURCE = Path(r"C:/Users/Administrator/Downloads/edu-research-skills-work/evals/writing-20261018/inputs/H2-materials.md")
stage = sys.argv[1]
if stage not in {"first", "final"}:
    raise SystemExit("stage must be first or final")
commands = {
    "voice": [sys.executable, "-X", "utf8", str(SKILL / "scripts/check_voice.py"), "--draft", str(OUT / f"{stage}.md"), "--source", str(SOURCE)],
    "prose": [sys.executable, "-X", "utf8", str(SKILL / "scripts/check_prose.py"), "--draft", str(OUT / f"{stage}.md")],
    "consistency": [sys.executable, "-X", "utf8", str(SKILL / "scripts/check_consistency.py"), "--draft", str(OUT / f"{stage}.md"), "--term-group", "written evidence=written survey accounts|interviews", "--term-group", "housing state=housing insecurity|housing instability"],
}
def run(item):
    name, command = item
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    log = result.stdout + ("\nSTDERR:\n" + result.stderr if result.stderr else "")
    path = OUT / f"{stage}_{name}.txt"
    path.write_text(log, encoding="utf-8")
    return {"check": name, "exit_code": result.returncode, "command": command, "output": path.name}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(run, commands.items()))
(OUT / f"{stage}_checks.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(results, ensure_ascii=False, indent=2))
if any(item["exit_code"] for item in results):
    raise SystemExit(1)
