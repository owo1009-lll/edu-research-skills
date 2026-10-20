"""Verify archived bytes and concrete outputs, not general writing quality."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    archive = read("archive-manifest.json")
    for item in archive["records"]:
        assert sha(ROOT / item["path"]) == item["archived_sha256"], item["path"]
    final = read("example/final-check.json")
    assert not [x for x in final["findings"] if x["status"] in {"stale", "review"}]
    intermediate = read("example/numeric-only-check.json")
    assert any(x.get("dependency_id") == "direction-reading" and x["status"] == "review"
               for x in intermediate["findings"])
    before = read("example/baseline-check.json")
    original_paths = {"paper": "paper.docx", "plan": "plan.json", "ppt": "before/slides.pptx"}
    for key, path in original_paths.items():
        assert sha(ROOT / "example" / path) == before["files"][key]["sha256"], path
    sys.path.insert(0, str(REPO / "skills/edu-ppt/scripts"))
    from check_deck import check
    deck = check(ROOT / "example/after/slides.pptx", ROOT / "example/plan-updated.json",
                 ROOT / "example/after/render")
    assert deck["status"] == "passed", deck
    fixed = read("linked-materials/reports/15-mixed-location-fixed.json")
    assert fixed["returncode"] == 2 and not fixed["output_exists"] and fixed["prior_failure_preserved"]
    assert read("linked-materials/reports/16-known-location-fixed.json")["returncode"] == 0
    prefs = read("preferences/final-audit.json")
    assert not prefs["project_facts_in_author_profile"]
    assert all(not x for x in prefs["deleted_short_example_storage_residuals"].values())
    for path, expected in read("validation.json")["runtime_sha256"].items():
        assert sha(REPO / path) == expected, path
    print(json.dumps({"archived_files": len(archive["records"]), "originals_unchanged": True,
                      "reviewed_example_consistent": True, "native_deck_and_preview_freshness": "passed",
                      "known_failed_examples_preserved": True,
                      "limits": "Hash/object checks do not establish semantic mapping, writing quality or human time savings."},
                     indent=2))


if __name__ == "__main__":
    main()
