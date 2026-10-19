"""Finalize the checked revision and record provenance without modifying prior stages."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent
BASE = Path(r"<EXPERIMENT_ROOT>")
SKILLS = BASE / "variants" / "v2" / "skills"
INPUTS = BASE / "inputs" / "D-L02"
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def write_json(name, value):
    path = ROOT / name
    if path.exists():
        raise RuntimeError(f"Refusing to overwrite {path}")
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
def body(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines[0].startswith("# ")
    return "\n".join(lines[1:]).strip()

final = ROOT / "final.md"
assert not final.exists()
final.write_bytes((ROOT / "draft-02.md").read_bytes())
resources = [
    ("edu-writing/SKILL.md", ["read"]),
    ("edu-writing/references/foundation.md", ["read"]),
    ("edu-writing/references/argument.md", ["read"]),
    ("edu-writing/references/voice-en.md", ["read"]),
    ("edu-writing/references/qualitative-narrative.md", ["read"]),
    ("edu-shared/references/integrity.md", ["read"]),
    ("edu-writing/scripts/check_voice.py", ["read", "executed for draft-01", "executed for draft-02"]),
    ("edu-writing/scripts/check_prose.py", ["read via truncated combined display", "import/file-access inspection", "executed for draft-01", "executed for draft-02"]),
]
entries = [{"path": str(SKILLS / rel), "sha256": sha(SKILLS / rel), "usage": usage}
           for rel, usage in resources]
for name in ("run_checks_v1.py", "finalize_v1.py"):
    entries.append({"path": str(ROOT / name), "sha256": sha(ROOT / name),
                    "usage": ["created in this run", "executed unchanged"],
                    "kind": "preserved local helper"})
write_json("loaded-resources.json", {
    "scope": "Skill and support resources actually read or executed; excludes task inputs, outputs and Python standard-library internals.",
    "resources": entries,
})
write_json("task-input-hashes.json", {
    "inputs": [{"path": str(INPUTS / name), "sha256": sha(INPUTS / name), "usage": "read"}
               for name in ("revise-request.md", "source-pack.md", "original.md")]
})
counts = {}
for name in ("draft-01.md", "draft-02.md", "final.md"):
    path = ROOT / name
    b = body(path)
    counts[name] = {"body_words": len(b.split()),
                    "body_paragraphs": len([p for p in b.split("\n\n") if p.strip()]),
                    "sha256": sha(path)}
original = (INPUTS / "original.md").read_text(encoding="utf-8")
original_paragraph = original.split("\n\n", 1)[1].split("\n\n## ", 1)[0].strip()
assert len(original_paragraph.split()) == 159
assert 90 <= counts["final.md"]["body_words"] <= 110
assert counts["final.md"]["body_paragraphs"] == 1
assert counts["draft-02.md"]["sha256"] == counts["final.md"]["sha256"]
for stage in ("draft-01", "draft-02"):
    record = json.loads((ROOT / f"{stage}-execution.json").read_text(encoding="utf-8"))
    assert record["draft_sha256"] == sha(ROOT / f"{stage}.md")
    assert all(c["exit_code"] == 0 for c in record["commands"])
    assert record["helper_sha256"] == sha(ROOT / "run_checks_v1.py")
write_json("word-counts.json", {
    "method": "Whitespace-delimited body words; initial attribution heading excluded; citations included.",
    "original_body_words": len(original_paragraph.split()),
    "files": counts,
})
required = ["rationale.md", "self-review.md", "source-notes.md", "workflow-notes.md",
            "executed-commands.json", "loaded-resources.json", "task-input-hashes.json",
            "word-counts.json", "draft-01.md", "draft-02.md", "final.md"]
assert all((ROOT / name).exists() for name in required)
completion = {
    "status": "complete",
    "invocation": [sys.executable, str(Path(__file__).resolve())],
    "helper_sha256": sha(Path(__file__)),
    "final": str(final),
    "body_words": counts["final.md"]["body_words"],
    "body_paragraphs": counts["final.md"]["body_paragraphs"],
    "final_matches_checked_revision": True,
    "all_four_checker_executions_succeeded": True,
    "skill_support_resource_count": len(entries),
    "task_input_count": 3,
    "output_files": sorted(p.name for p in ROOT.iterdir() if p.is_file()) + ["completion.json"],
}
write_json("completion.json", completion)
print(json.dumps(completion, ensure_ascii=False, indent=2))
