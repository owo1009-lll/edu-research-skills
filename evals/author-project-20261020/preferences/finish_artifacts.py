"""Preserve first attempts; finish and check synthetic writing artifacts."""
from pathlib import Path
import json
import subprocess
import sys
from run_forward import BASE, REPO, SOURCE, append, save

enabled_dir = BASE / "project-enabled/edu_output/writing/compression-01"
disabled_dir = BASE / "project-no-profile/edu_output/writing/compression-01"
changes = [
    (enabled_dir, "adjusting classroom task sequences", "adjusting the sequence of classroom tasks"),
    (disabled_dir, "exercising judgment", "exercising situated judgment"),
]
for folder, old, new in changes:
    path = folder / "final.md"
    original = path.read_text(encoding="utf-8")
    first = folder / "first-draft.md"
    if first.exists():
        raise RuntimeError("First attempt already preserved; do not overwrite it.")
    first.write_text(original, encoding="utf-8")
    revised = original.replace(old, new)
    path.write_text(revised, encoding="utf-8")
    append(dict(label="repair-initial-word-count", path=str(path),
                initial_word_count=len(original.split()), final_word_count=len(revised.split()),
                reason="The first attempt was below the explicit 55-word lower bound.",
                original=original, revised=revised))

variants = {
    "one-time-evidence-first.md":
        "Interviews with 24 rural teachers described adjustments to classroom task sequences "
        "in response to pupils’ immediate needs while retaining shared curricular aims. "
        "These accounts show professional discretion being exercised within curriculum "
        "responsibility under institutional constraints. Administrators should protect time "
        "for such situated judgments. The interviews illuminate negotiated responsibility; "
        "they do not establish gains in attainment.",
    "other-language-zh-discussion.md":
        "专业判断是在共同课程目标下履行课程责任的一种方式。24名乡村教师的访谈显示，教师根据学生即时需要调整课堂任务顺序，同时保留共同课程目标。管理者应为这种情境判断保留时间。这些材料说明了教师如何在制度约束下协商课程责任，但不能据此认定学生的学业表现得到提升。",
    "other-section-en-methods.md":
        "This qualitative study used interviews with 24 rural teachers to examine how they exercised professional discretion when sequencing classroom tasks within a shared curriculum framework.",
}
out = BASE / "project-enabled/edu_output/writing/management-scenarios"
out.mkdir(parents=True, exist_ok=True)
for name, text in variants.items():
    (out / name).write_text(text + "\n", encoding="utf-8")
save(BASE / "writing-scenarios.json", [
    dict(request="仅这一次先写访谈材料，再写判断；以后仍照旧。",
         load="load-one-time", file=str(out / "one-time-evidence-first.md"),
         reason="当前任务要求覆盖相反的作者顺序项；其余概念和语气偏好继续使用。"),
    dict(request="用中文把这段整理成讨论文字。",
         load="load-other-language", file=str(out / "other-language-zh-discussion.md"),
         reason="英文作者偏好全部不匹配；中文仍依据原材料保留判断、建议和证据边界。"),
    dict(request="将已知研究信息写成一句英文 Methods 说明。",
         load="load-other-section", file=str(out / "other-section-en-methods.md"),
         reason="discussion 偏好不匹配；方法只写已提供的研究类型、样本、访谈及研究内容，不加入 should 建议。"),
])

writing_checks = []
for project in ("project-enabled", "project-no-profile"):
    file = BASE / project / "edu_output/writing/compression-01/final.md"
    text = file.read_text("utf-8")
    writing_checks.append(dict(
        project=project, word_count=len(text.split()), within_requested_range=55 <= len(text.split()) <= 75,
        concept_label="professional discretion" in text.lower(),
        should_retained="should protect time" in text,
        attainment_boundary="do not establish gains in attainment" in text,
        source_interviews="interviews" in text.lower(),
        shared_aims="shared curricular aims" in text,
        researcher_judgment_first=text.startswith("Professional discretion")))
    for script in ("check_voice.py", "check_prose.py"):
        command = [sys.executable, "-X", "utf8", "-B", str(REPO / "skills/edu-writing/scripts" / script),
                   "--draft", str(file)]
        if script == "check_voice.py":
            command += ["--source", str(BASE / "source.txt")]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        log_name = project + "-" + script.replace(".py", ".txt")
        (BASE / log_name).write_text(result.stdout + "\nSTDERR:\n" + result.stderr, encoding="utf-8")
        append(dict(label="writing-check-" + project + "-" + script, command=command,
                    exit_code=result.returncode, stdout_file=log_name, stderr=result.stderr))
save(BASE / "writing-checks.json", dict(original_word_count=len(SOURCE.split()),
                                      final_checks=writing_checks,
                                      one_time_words=len(variants["one-time-evidence-first.md"].split()),
                                      evaluation="AI inspection of explicit synthetic instructions; no human preference score."))
print(json.dumps(writing_checks, ensure_ascii=False, indent=2))
