from pathlib import Path
import hashlib
import json
import re
import sys

OUT = Path(__file__).resolve().parent
SNAPSHOT = Path(r"@snapshot")
INPUT = Path(r"@inputs\D-L01")
loaded = [
    ("skills/edu-writing/SKILL.md", "Workflow instructions"),
    ("skills/edu-writing/references/argument.md", "Argument and evidentiary scope"),
    ("skills/edu-writing/references/voice-en.md", "English authorial stance"),
    ("skills/edu-writing/references/qualitative-narrative.md", "Qualitative discussion route"),
    ("skills/edu-shared/references/integrity.md", "Shared integrity rules"),
    ("skills/edu-writing/references/methods/cases-develop-explanations.md", "Using differences and counterexamples without invented trajectories"),
    ("skills/edu-writing/scripts/check_voice.py", "Read and executed on first draft"),
    ("skills/edu-writing/scripts/check_prose.py", "Read and executed on heading-labeled first draft copy"),
]
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
manifest = {
    "snapshot_root": str(SNAPSHOT),
    "snapshot_relative_base": "current-01",
    "loaded_snapshot_files": [{"path": path, "sha256": sha(SNAPSHOT / path), "purpose": purpose} for path, purpose in loaded],
    "inputs": [{"path": str(INPUT / name), "sha256": sha(INPUT / name), "role": role} for name, role in [("new-request.md", "Task instructions"), ("source-pack.md", "Sole substantive source")]],
    "encoding": "UTF-8 for text; raw bytes for hashes",
    "browsed": False,
    "spawned_agents": False,
}
(OUT / "loads.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
final = (OUT / "final.md").read_text(encoding="utf-8")
paragraphs = re.split(r"\n\s*\n", final.strip())
words = re.findall(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*", final)
assert len(paragraphs) == 2, len(paragraphs)
assert 230 <= len(words) <= 280, len(words)
assert "Williamson et al.'s (2019)" in final
assert not re.search(r"(?m)^\s*(?:#|\|)", final)
required = ["final.md", "rationale.md", "loads.json", "run-note.md", "draft-01.md", "self-review.md", "check-voice-draft.txt", "check-prose-draft.txt"]
for name in required:
    assert (OUT / name).is_file(), name
validation = {
    "file": "final.md", "sha256": sha(OUT / "final.md"), "paragraphs": len(paragraphs), "words": len(words),
    "word_count_rule": "Alphanumeric words; internal hyphens and apostrophes retained.",
    "requested_word_range": [230, 280], "attribution_present": True, "headings_or_tables_present": False,
    "required_files_present": required, "validation_passed": True,
    "python": sys.version,
    "limits": "These assertions check format, count, attribution presence and file existence; substantive review is recorded in self-review.md. Frozen checkers were run only on the draft."
}
(OUT / "final-validation.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(validation, ensure_ascii=False, indent=2))
