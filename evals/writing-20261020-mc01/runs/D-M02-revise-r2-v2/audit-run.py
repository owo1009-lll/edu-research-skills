from pathlib import Path
import hashlib
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent.parent
spec = json.loads((ROOT / "audit-spec.json").read_text(encoding="utf-8"))

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

resources = []
for relative in spec["resources"]:
    path = BASE / relative
    activities = ["read"]
    if path.name in ("check_voice.py", "check_prose.py"):
        activities.append("executed")
    resources.append({"path": str(path), "sha256": digest(path), "activities": activities})
generated = []
for name in ("run-checks.py", "audit-run.py"):
    path = ROOT / name
    generated.append({"path": str(path), "sha256": digest(path), "activities": ["executed"],
                      "origin": "Created within this run, not part of the skill snapshot."})
(ROOT / "loaded-resources.json").write_text(
    json.dumps({"hash_algorithm": "SHA-256", "resources": resources, "generated_support": generated},
               ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
inputs = [{"path": str(BASE / relative), "sha256": digest(BASE / relative)}
          for relative in spec["task_inputs"]]
(ROOT / "task-input-hashes.json").write_text(
    json.dumps({"hash_algorithm": "SHA-256", "inputs": inputs}, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8")

prose_names = ["draft-01.md", "draft-02.md", "self-review.md", "final.md", "rationale.md",
               "changes-and-source-checks.md"]
for name in prose_names:
    content = (ROOT / name).read_text(encoding="utf-8", errors="strict")
    assert "\ufffd" not in content, name + ": replacement character found"
text = (ROOT / "final.md").read_text(encoding="utf-8")
body = text.split("## Attribution", 1)[0]
body = "\n".join(line for line in body.splitlines() if not line.startswith("#")).strip()
words = len(body.split())
paragraphs = len(re.split(r"\n\s*\n", body))
assert 120 <= words <= 145, words
assert paragraphs == 1, paragraphs
assert "Hennessey and Dionigi (2013)" in body
assert (ROOT / "draft-02.md").read_bytes() == (ROOT / "final.md").read_bytes()
assert (ROOT / "draft-01.md").read_bytes() != (ROOT / "final.md").read_bytes()
for draft in ("draft-01", "draft-02"):
    records = json.loads((ROOT / "checks" / draft / "executed-commands.json").read_text(encoding="utf-8"))
    assert len(records) == 2 and all(record["exit_code"] == 0 for record in records)
verification = {
    "status": "passed",
    "final_body_words": words,
    "body_paragraphs": paragraphs,
    "counting_method": "Whitespace-separated body words; headings and attribution excluded.",
    "final_equals_checked_draft_02": True,
    "first_draft_preserved_and_distinct": True,
    "prose_decodes_as_utf8_without_replacement_characters": True,
    "original_citation_retained": True,
    "checker_runs": "Two successful skill checker runs per saved draft; see checks/*/executed-commands.json.",
    "files": [{"path": str(ROOT / name), "sha256": digest(ROOT / name)} for name in prose_names]
}
(ROOT / "final-verification.json").write_text(
    json.dumps(verification, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(verification, ensure_ascii=False, indent=2))
