"""Final checks limited to the changed draft and storage, with synthetic provenance."""
import json
from pathlib import Path
import subprocess
import sys
from run_forward import BASE, REPO, PROFILE, append, save

final = BASE / "project-enabled/edu_output/writing/compression-01/final.md"
text = final.read_text("utf-8")
append(dict(label="semantic-review-revision", path=str(final),
            reason="将24人明确写为访谈样本，而不暗示24人都报告了同一种实践；不改样本量或添加出现频次。",
            previous="In interviews, 24 rural teachers described adjusting the sequence of classroom tasks",
            revised="In interviews with 24 rural teachers, participants described adjusting classroom task sequences",
            final_word_count=len(text.split())))
wrapper = final.with_name("check-context-discussion.md")
wrapper.write_text("# Discussion\n\n" + text, encoding="utf-8")
for name, draft in (("check_voice.py", final), ("check_prose.py", wrapper)):
    command = [sys.executable, "-X", "utf8", "-B",
               str(REPO / "skills/edu-writing/scripts" / name), "--draft", str(draft)]
    if name == "check_voice.py":
        command += ["--source", str(BASE / "source.txt")]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    filename = "enabled-final-" + name.replace(".py", ".txt")
    (BASE / filename).write_text(result.stdout + "\nSTDERR:\n" + result.stderr, encoding="utf-8")
    append(dict(label="final-writing-check-" + name, command=command,
                exit_code=result.returncode, stdout_file=filename))

profile = json.loads(PROFILE.read_text("utf-8"))
storage_paths = [
    path
    for root in (BASE / "private-profile",
                 BASE / "project-enabled/edu_output/project",
                 BASE / "project-no-profile/edu_output/project",
                 BASE / "project-other/edu_output/project")
    for path in root.rglob("*") if path.is_file()
]
examples = [
    "Within shared aims, teachers judge the next classroom step.",
    "Judgment remains answerable to shared curricular purposes.",
]
residuals = {example: [str(path.relative_to(BASE)) for path in storage_paths
                       if example in path.read_text("utf-8", errors="replace")]
             for example in examples}
checks = json.loads((BASE / "management-results.json").read_text("utf-8"))["checks"]
logs = [json.loads(line) for line in (BASE / "operations.jsonl").read_text("utf-8").splitlines()]
report = dict(
    synthetic_only=True, repository_writes_performed=False, external_services_used=False,
    test_log_records=len(logs), management_checks=len(checks),
    management_passed=sum(item["passed"] for item in checks),
    historical_management_failure="documentation omitted scope=author on an author-item update; explicit scope fixed it",
    documentation_fix_observed=True,
    active_author_items=sum(item["status"] == "active" for item in profile["items"]),
    project_facts_in_author_profile=any(token in PROFILE.read_text("utf-8")
                                       for token in ("24", "乡村教师", "统一课程框架内根据学生需要判断教学顺序")),
    deleted_short_example_storage_residuals=residuals,
    storage_files=[str(path.relative_to(BASE)) for path in storage_paths],
    lock_or_temporary_files=[str(path.relative_to(BASE)) for path in storage_paths
                             if path.suffix == ".lock" or path.name.startswith(".edu-write-")],
    final_words={project: len((BASE / project / "edu_output/writing/compression-01/final.md")
                             .read_text("utf-8").split())
                 for project in ("project-enabled", "project-no-profile")},
    limits=["Same evaluator authored both variants; no model-context blinding.",
            "No real author preference scores or time measurements.",
            "Deleted synthetic examples remain in deliberately retained test driver/logs, not live preference storage.",
            "The original is 49 words; strict shortening conflicts with the 55–75-word request."])
save(BASE / "final-audit.json", report)
print(json.dumps(report, ensure_ascii=False, indent=2))
