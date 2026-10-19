"""Close the local provenance record using actual file hashes."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
RESOURCE_SPEC = [
  {
    "path": "<EXPERIMENT_ROOT>\\variants\\v2\\skills\\edu-writing\\SKILL.md",
    "access": [
      "read"
    ]
  },
  {
    "path": "<EXPERIMENT_ROOT>\\variants\\v2\\skills\\edu-writing\\references\\argument.md",
    "access": [
      "read"
    ]
  },
  {
    "path": "<EXPERIMENT_ROOT>\\variants\\v2\\skills\\edu-writing\\references\\voice-en.md",
    "access": [
      "read"
    ]
  },
  {
    "path": "<EXPERIMENT_ROOT>\\variants\\v2\\skills\\edu-writing\\references\\framing-results.md",
    "access": [
      "read"
    ]
  },
  {
    "path": "<EXPERIMENT_ROOT>\\variants\\v2\\skills\\edu-writing\\references\\quantitative-discussion.md",
    "access": [
      "read"
    ]
  },
  {
    "path": "<EXPERIMENT_ROOT>\\variants\\v2\\skills\\edu-writing\\references\\conclusion-implications.md",
    "access": [
      "read"
    ]
  },
  {
    "path": "<EXPERIMENT_ROOT>\\variants\\v2\\skills\\edu-shared\\references\\integrity.md",
    "access": [
      "read"
    ]
  },
  {
    "path": "<EXPERIMENT_ROOT>\\variants\\v2\\skills\\edu-writing\\scripts\\check_voice.py",
    "access": [
      "read",
      "executed"
    ]
  },
  {
    "path": "<EXPERIMENT_ROOT>\\variants\\v2\\skills\\edu-writing\\scripts\\check_prose.py",
    "access": [
      "read",
      "executed"
    ]
  },
  {
    "path": "<EXPERIMENT_ROOT>\\runs\\D-Q02-new-r2-v2\\run-checks.py",
    "access": [
      "authored",
      "executed"
    ]
  },
  {
    "path": "<EXPERIMENT_ROOT>\\runs\\D-Q02-new-r2-v2\\finalize-audit.py",
    "access": [
      "authored",
      "executed"
    ]
  }
]
INPUTS = [
    ROOT.parents[1] / "inputs" / "D-Q02" / "new-request.md",
    ROOT.parents[1] / "inputs" / "D-Q02" / "source-pack.md",
]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


resources = []
for item in RESOURCE_SPEC:
    path = Path(item["path"])
    resources.append({**item, "sha256": digest(path), "bytes": path.stat().st_size})
(ROOT / "loaded-resources.json").write_text(json.dumps({
    "scope": "Only the specified v2 snapshot skill resources and locally authored execution helpers; standard-library modules are not skill resources.",
    "hash_timing": "SHA-256 calculated at audit closure on the files actually read or executed.",
    "resources": resources,
    "external_reading": "None. No browsing, installed skill copies, other runs, developer notes or comparison records were read.",
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "input-file-hashes.json").write_text(json.dumps({
    "algorithm": "SHA-256",
    "inputs": [{"path": str(path), "sha256": digest(path), "bytes": path.stat().st_size} for path in INPUTS],
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
required = ["draft-01.md", "draft-02.md", "draft-03.md", "final.md", "self-review.md", "rationale.md", "note.md",
            "executed-commands.json", "loaded-resources.json", "input-file-hashes.json"]
assert all((ROOT / item).is_file() for item in required)
assert (ROOT / "draft-03.md").read_bytes() == (ROOT / "final.md").read_bytes()
counts = json.loads((ROOT / "checks" / "final-word-count.json").read_text(encoding="utf-8"))
assert counts["body_within_450_550"]
assert counts["sha256"] == digest(ROOT / "final.md")
for stage in ["draft-01", "draft-02", "final"]:
    commands = json.loads((ROOT / "checks" / f"{stage}-executed-commands.json").read_text(encoding="utf-8"))
    assert len(commands) == 3 and all(item["exit_code"] == 0 for item in commands)
    for item in commands:
        assert Path(item["stdout"]).is_file() and Path(item["stderr"]).is_file()
for name in ["draft-01.md", "draft-02.md", "draft-03.md", "final.md", "self-review.md", "rationale.md", "note.md"]:
    text = (ROOT / name).read_text(encoding="utf-8", errors="strict")
    assert "\ufffd" not in text
summary = {
    "required_artifacts_present": True,
    "final_equals_draft_03": True,
    "body_words": counts["body_words"],
    "attribution_heading_words": counts["attribution_heading_words"],
    "all_nine_checker_invocations_exit_zero": True,
    "utf8_validation": "passed",
    "loaded_resource_count": len(resources),
    "final_sha256": digest(ROOT / "final.md"),
}
(ROOT / "audit-validation.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False))
