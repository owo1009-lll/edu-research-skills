"""Immutable delivery helper; read only assigned resources, inputs and this run."""
from pathlib import Path
import hashlib
import json
import re

OUT = Path("<EXPERIMENT_ROOT>\\runs\\D-L02-new-r2-v1")
RESOURCES = [
  {
    "path": "<EXPERIMENT_ROOT>\\variants\\v1\\skills\\edu-writing\\SKILL.md",
    "access": [
      "read"
    ]
  },
  {
    "path": "<EXPERIMENT_ROOT>\\variants\\v1\\skills\\edu-writing\\references\\argument.md",
    "access": [
      "read"
    ]
  },
  {
    "path": "<EXPERIMENT_ROOT>\\variants\\v1\\skills\\edu-writing\\references\\voice-en.md",
    "access": [
      "read"
    ]
  },
  {
    "path": "<EXPERIMENT_ROOT>\\variants\\v1\\skills\\edu-writing\\references\\qualitative-narrative.md",
    "access": [
      "read"
    ]
  },
  {
    "path": "<EXPERIMENT_ROOT>\\variants\\v1\\skills\\edu-shared\\references\\integrity.md",
    "access": [
      "read"
    ]
  },
  {
    "path": "<EXPERIMENT_ROOT>\\variants\\v1\\skills\\edu-writing\\references\\methods\\cases-develop-explanations.md",
    "access": [
      "read"
    ]
  },
  {
    "path": "<EXPERIMENT_ROOT>\\variants\\v1\\skills\\edu-writing\\references\\prose-en.md",
    "access": [
      "read"
    ]
  },
  {
    "path": "<EXPERIMENT_ROOT>\\variants\\v1\\skills\\edu-writing\\scripts\\check_voice.py",
    "access": [
      "read",
      "executed"
    ]
  },
  {
    "path": "<EXPERIMENT_ROOT>\\variants\\v1\\skills\\edu-writing\\scripts\\check_prose.py",
    "access": [
      "read",
      "executed"
    ]
  }
]
INPUTS = [
  "<EXPERIMENT_ROOT>\\inputs\\D-L02\\new-request.md",
  "<EXPERIMENT_ROOT>\\inputs\\D-L02\\source-pack.md"
]

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def write_new(name, value):
    with (OUT / name).open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

draft = OUT / "draft-02.md"
final = OUT / "final.md"
with final.open("xb") as handle:
    handle.write(draft.read_bytes())

for resource in RESOURCES:
    resource["sha256"] = digest(resource["path"])
    resource["kind"] = "assigned skill snapshot"
for name in ["run_stage_v1.py", "finalize_v1.py"]:
    path = OUT / name
    RESOURCES.append({"path": str(path), "sha256": digest(path),
                      "access": ["executed", "read for provenance hashing"],
                      "kind": "preserved task-local helper"})

write_new("loaded-resources.json", {
    "scope": "Skill and support resources actually read or executed, plus preserved task-local helpers. Standard-library runtime modules are not task resources.",
    "resources": RESOURCES
})
write_new("task-input-hashes.json", {
    "inputs": [{"path": path, "sha256": digest(path), "access": ["read"]} for path in INPUTS]
})
body = "\n".join(final.read_text(encoding="utf-8").splitlines()[1:]).strip()
count = len(re.findall(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*", body))
verification = {
    "final": str(final), "final_sha256": digest(final),
    "draft_02_sha256": digest(draft), "final_equals_draft_02": final.read_bytes() == draft.read_bytes(),
    "body_word_count": count, "initial_attribution_heading_excluded": True,
    "within_requested_350_450": 350 <= count <= 450,
    "body_paragraph_count": len(body.split("\n\n")),
    "recorded_prose_stages": ["draft-01.md", "draft-02.md"],
    "final_is_copy_of": "draft-02.md"
}
write_new("delivery-verification.json", verification)
print(json.dumps(verification, indent=2))

