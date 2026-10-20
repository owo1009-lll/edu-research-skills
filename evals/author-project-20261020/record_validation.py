"""Record actual local logs and code identity for this development evaluation."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
RUNTIME = [
    "skills/edu-writing/scripts/author_preferences.py",
    "skills/edu-writing/references/author-preferences.md",
    "skills/edu-shared/scripts/private_store.py",
    "skills/edu-shared/scripts/project_documents.py",
    "skills/edu-research/scripts/project_check.py",
    "skills/edu-research/references/material-updates.md",
    "skills/edu-writing/SKILL.md", "skills/edu-research/SKILL.md", "skills/edu-ppt/SKILL.md",
    "skills/edu-writing/references/reference-verification.md",
    "skills/edu-research/requirements.txt",
]


def main(trial):
    for name in ("tests-01.log", "tests-final.log"):
        data = (trial / name).read_bytes()
        text = data.decode("utf-16" if data.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig")
        text = text.replace(str(REPO), "@REPO@").replace(str(trial), "@EVAL@")
        (ROOT / name).write_text(text, encoding="utf-8")
    final = (ROOT / "tests-final.log").read_text(encoding="utf-8")
    if "Ran 146 tests" not in final or "\nOK" not in final:
        raise ValueError("Expected actual successful complete local run not found.")
    record = {
        "baseline_commit": "f3e2066a181cbda90b75bd71296c49a9ac5f6007",
        "release": "0.14.0",
        "runtime_sha256": {name: hashlib.sha256((REPO / name).read_bytes()).hexdigest() for name in RUNTIME},
        "local_complete_suite": {"command": "python -X utf8 -m unittest discover -s tests -v",
                                 "tests": 146, "status": "passed", "log": "tests-final.log",
                                 "locale": "English_United States.utf8 (Windows R)", "R_tests_skipped": False},
        "subsequent_integration_check": {
            "command": "python -X utf8 -m unittest discover -s tests -p test_project_check.py -v",
            "tests": 16, "status": "passed",
            "scope": "Includes the added native deck integration regression: same values with changed category, series and unit fail."
        },
        "initial_failure": {"log": "tests-01.log", "status": "failed",
                            "reason": "Host C.UTF-8 locale caused Windows R to misread a Chinese source path.",
                            "repair": "R-compatible locale in the invoking environment; no statistics-code edits or skipped test."},
        "skill_validation": {"edu-writing": "passed", "edu-research": "passed"},
        "visual": {"example": "example/visual-review.json",
                   "independent": "linked-materials/independent-report.md",
                   "scope": "Actual PowerPoint and Word rendering, followed by AI image inspection."},
        "ci_gate": "Check Python and R jobs for the final commit; the final response links the exact completed run.",
        "limits": ["All new public materials are synthetic.", "No measured author time savings or human preference scores.",
                   "Independent trials preceded some localized fixes; failures and actual retests are retained.",
                   "Artifact and structural validation do not prove semantic correctness."]
    }
    (ROOT / "validation.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--trial-root", type=Path, required=True)
    main(p.parse_args().trial_root)
