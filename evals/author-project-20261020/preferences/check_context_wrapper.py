"""Recheck only the discovered prose-checker context problem, without altering drafts."""
import json
import subprocess
import sys
from run_forward import BASE, REPO, append, save

results = []
for project in ("project-enabled", "project-no-profile"):
    final = BASE / project / "edu_output/writing/compression-01/final.md"
    wrapper = final.with_name("check-context-discussion.md")
    wrapper.write_text("# Discussion\n\n" + final.read_text("utf-8"), encoding="utf-8")
    command = [sys.executable, "-X", "utf8", "-B",
               str(REPO / "skills/edu-writing/scripts/check_prose.py"),
               "--draft", str(wrapper)]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    log = BASE / (project + "-check_prose-context.txt")
    log.write_text(result.stdout + "\nSTDERR:\n" + result.stderr, encoding="utf-8")
    append(dict(label="prose-context-workaround-" + project, command=command,
                exit_code=result.returncode, stdout_file=str(log)))
    results.append(dict(project=project, exit_code=result.returncode,
                        recognized_discussion="Sections found: Discussion" in result.stdout,
                        recognized_55_words="55 words" in result.stdout))
save(BASE / "prose-context-results.json", results)
print(json.dumps(results, ensure_ascii=False, indent=2))
