import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

out = Path(__file__).resolve().parent
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
final_path = out / "final.md"
text = final_path.read_text(encoding="utf-8")
body = text.split("\n\n## Attribution", 1)[0].strip()
required = ["first-draft.md", "second-draft.md", "third-draft.md", "self-review.md",
            "final.md", "rationale.md", "changes-and-source-checks.md",
            "loaded-resources.json", "task-input-hashes.json", "commands.md", "executed-commands.jsonl"]
stage_reports = [json.loads((out / "checks" / (s + ".validation.json")).read_text(encoding="utf-8"))
                 for s in ["first-draft", "second-draft", "third-draft"]]
validation = {
    "at_utc": datetime.now(timezone.utc).isoformat(),
    "final_sha256": digest(final_path),
    "body_word_count": len(body.split()),
    "body_paragraphs": len(re.split(r"\n\s*\n", body)),
    "body_count_excludes": "Attribution heading and all attribution text",
    "within_120_145_words": 120 <= len(body.split()) <= 145,
    "final_identical_to_third_draft": final_path.read_bytes() == (out / "third-draft.md").read_bytes(),
    "existing_citation_preserved": "Hennessey and Dionigi (2013)" in body,
    "unicode_attribution_preserved": "Völlinger" in text,
    "no_unicode_replacement_characters_in_markdown": all("\ufffd" not in p.read_text(encoding="utf-8") for p in out.glob("*.md")),
    "all_required_files_present": all((out / p).exists() for p in required),
    "draft_history": [{"stage": x["stage"], "word_count": x["word_count"], "sha256": x["draft_sha256"],
                      "unchanged_since_checked": digest(out / (x["stage"] + ".md")) == x["draft_sha256"],
                      "checker_exit_codes": [c["exit_code"] for c in x["commands"]]} for x in stage_reports],
}
for k in ["within_120_145_words", "final_identical_to_third_draft", "existing_citation_preserved",
          "unicode_attribution_preserved", "no_unicode_replacement_characters_in_markdown", "all_required_files_present"]:
    assert validation[k], k
assert validation["body_paragraphs"] == 1
assert all(d["unchanged_since_checked"] and all(e == 0 for e in d["checker_exit_codes"]) for d in validation["draft_history"])
resources = json.loads((out / "loaded-resources.json").read_text(encoding="utf-8"))
resources["local_support_resources"] = [
    {"path": str(out / name), "sha256": digest(out / name), "actions": ["created", "executed"]}
    for name in ("audit_run.py", "finalize.py")
]
(out / "loaded-resources.json").write_text(json.dumps(resources, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(out / "final-validation.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(validation, ensure_ascii=False, indent=2))

