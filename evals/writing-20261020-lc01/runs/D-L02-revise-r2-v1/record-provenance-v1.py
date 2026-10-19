"""Record actually loaded resources, assigned inputs, and final draft identity."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
BASE = Path(r"<EXPERIMENT_ROOT>")
SKILLS = BASE / "variants" / "v1" / "skills"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

resources = []
for relative in (
    "edu-writing/SKILL.md",
    "edu-writing/references/foundation.md",
    "edu-writing/references/argument.md",
    "edu-writing/references/voice-en.md",
    "edu-writing/references/qualitative-narrative.md",
    "edu-shared/references/integrity.md",
    "edu-writing/scripts/check_voice.py",
    "edu-writing/scripts/check_prose.py",
):
    path = SKILLS / relative
    resources.append({"path": str(path), "sha256": sha(path), "activity": ["read", "executed"] if path.suffix == ".py" else ["read"], "resource_type": "assigned_skill_snapshot"})
for name in ("check-draft-v1.py", "record-provenance-v1.py"):
    path = ROOT / name
    resources.append({"path": str(path), "sha256": sha(path), "activity": ["created", "executed"], "resource_type": "preserved_generated_helper"})
(ROOT / "loaded-resources.json").write_text(json.dumps({"resources": resources, "input_hashes_file": "task-input-hashes.json", "scope": "Only actual skill/support files read or executed; standard-library runtime dependencies are not skill resources."}, indent=2) + "\n", encoding="utf-8")
inputs = []
for name in ("revise-request.md", "source-pack.md", "original.md"):
    path = BASE / "inputs" / "D-L02" / name
    inputs.append({"path": str(path), "sha256": sha(path), "activity": "read"})
(ROOT / "task-input-hashes.json").write_text(json.dumps({"inputs": inputs}, indent=2) + "\n", encoding="utf-8")
drafts = []
for name in ("draft-01.md", "draft-02.md", "draft-03.md", "final.md"):
    path = ROOT / name
    text = path.read_text(encoding="utf-8")
    heading, body = text.split("\n", 1)
    body = body.strip()
    drafts.append({"file": name, "sha256": sha(path), "body_words": len(body.split()), "body_paragraphs": len([p for p in body.split("\n\n") if p.strip()]), "initial_heading_excluded": heading})
summary = {"drafts": drafts, "final_equals_draft_03": (ROOT / "final.md").read_bytes() == (ROOT / "draft-03.md").read_bytes(), "final_matches_checked_sha256": sha(ROOT / "final.md") == json.loads((ROOT / "final-verified-word-count.json").read_text(encoding="utf-8"))["sha256"]}
(ROOT / "draft-manifest.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=2))
assert summary["final_equals_draft_03"] and summary["final_matches_checked_sha256"]
assert 90 <= drafts[-1]["body_words"] <= 110 and drafts[-1]["body_paragraphs"] == 1
