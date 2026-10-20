"""Independent synthetic forward test. No repository writes or external services.

All recorded prose and user requests below are synthetic test material.
This runner is an observable CLI driver, not a substitute for author evaluation.
"""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

BASE = Path(__file__).resolve().parent
REPO = Path(r"@REPO@")
SCRIPT = REPO / "skills/edu-writing/scripts/author_preferences.py"
ENABLED = BASE / "project-enabled"
DISABLED = BASE / "project-no-profile"
OTHER = BASE / "project-other"
PROFILE = BASE / "private-profile/author-preferences.json"
LOG = BASE / "operations.jsonl"
STATE = BASE / "test-state.json"
USER = "以后修改我英文定性论文的 Discussion 时保留 professional discretion 这样的概念标签，先讲我的判断再给材料；有专业依据的 should 别一律弱化。这个项目存档位置由你在本测试目录内安排。"
SOURCE = "Professional discretion is not an escape from curriculum responsibility. Teachers described adapting the sequence of classroom tasks to pupils’ immediate needs while retaining shared curricular aims. Administrators should protect time for these situated judgments. The interviews illuminate how this responsibility was negotiated; they do not establish gains in attainment."
CONTEXT = dict(language="en", research_type="qualitative", section="discussion",
               task="revise", task_id="compress-01")


def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append(record):
    record["time_utc"] = datetime.now(timezone.utc).isoformat()
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def call(label, request, project=ENABLED, profile=PROFILE, user_request=None):
    command = [sys.executable, "-B", str(SCRIPT), "--project", str(project)]
    if profile is not None:
        command += ["--profile", str(profile)]
    env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    result = subprocess.run(command, input=json.dumps(request, ensure_ascii=False),
                            encoding="utf-8", capture_output=True, env=env)
    try:
        response = json.loads(result.stdout) if result.stdout.strip() else None
    except json.JSONDecodeError:
        response = None
    append(dict(label=label, synthetic_user_request=user_request, command=command,
                stdin_json=request, exit_code=result.returncode,
                stdout=result.stdout, stderr=result.stderr))
    return result.returncode, response


def load(label, context=None, project=ENABLED, profile=PROFILE):
    code, data = call(label, dict(action="load", context=context or CONTEXT),
                      project=project, profile=profile)
    if code != 0:
        raise RuntimeError(f"{label} failed: inspect operations.jsonl")
    return data


def preference(content, scope="author", basis="explicit", status="active", source=None,
               task_id=None):
    item = dict(category="expression", content=content, scope=scope, basis=basis,
                status=status, languages=["en"], research_types=["qualitative"],
                sections=["discussion"], tasks=["revise"],
                conditions=["仅用于有材料或明确专业依据的作者判断"],
                exceptions=["不覆盖当前明确要求或事实与证据边界"],
                source=source or dict(kind="explicit", evidence=USER, time="2026-10-20",
                                     cross_project_authorization=USER))
    if task_id:
        item["task_id"] = task_id
    return item


def setup():
    if STATE.exists():
        raise RuntimeError("Existing run state detected; preserve this run rather than overwriting it.")
    for project in (ENABLED, DISABLED, OTHER):
        project.mkdir(parents=True, exist_ok=True)
    materials = dict(synthetic=True, language="en", research_type="qualitative",
                     sample={"count": 24, "population": "rural teachers", "method": "interviews"},
                     project_concept={"label": "professional discretion",
                                      "definition": "教师在统一课程框架内根据学生需要判断教学顺序"},
                     findings="制度约束与教师实践判断并存", untested="未检验学习效果",
                     original=SOURCE)
    for project in (ENABLED, DISABLED):
        save(project / "edu_output/project/materials.json", materials)
    (BASE / "source.txt").write_text(json.dumps(materials, ensure_ascii=False, indent=2),
                                   encoding="utf-8")
    (BASE / "requests.txt").write_text(
        "所有内容为合成材料，未经真人评分。\n\n保存偏好请求：\n" + USER +
        "\n\n压缩任务：\n把这一段压缩到55-75英文词，保留关键认识和依据。\n",
        encoding="utf-8")
    content = [
        "修改英文定性论文的 Discussion 时保留作者采用且有材料依据的概念标签，如 professional discretion；本项目概念定义不跨项目迁移。",
        "修改英文定性论文的 Discussion 时，先给出作者有依据的判断，再给出材料与解释。",
        "修改英文定性论文的 Discussion 时，保留有专业依据的 should，不统一改成 could。"
    ]
    ids = []
    for n, text in enumerate(content, 1):
        code, data = call(f"initial-add-{n}", dict(action="add", scope="author",
                                                  item=preference(text)),
                          user_request=USER)
        if code != 0:
            raise RuntimeError(f"initial add {n} failed")
        ids.append(data["id"])
    state = dict(ids=ids, profile=str(PROFILE))
    save(STATE, state)
    enabled = load("initial-load-enabled")
    no_profile = load("initial-load-no-profile", project=DISABLED, profile=None)
    save(BASE / "initial-loads.json", dict(enabled=enabled, no_profile=no_profile))
    print(json.dumps(dict(active_enabled=enabled["active"], no_profile=no_profile,
                          profile=str(PROFILE)), ensure_ascii=False, indent=2))


def manage():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    ids = state["ids"]
    checks = []

    def check(name, condition, detail):
        checks.append(dict(name=name, passed=bool(condition), detail=detail))

    user_once = "仅这一次先写访谈材料，再写判断；以后仍照旧。"
    once = preference("这次先给访谈材料，再给作者判断。", scope="task",
                      source=dict(kind="explicit", evidence=user_once, time="2026-10-20"),
                      task_id="one-time-evidence-first")
    code, result = call("add-one-time", dict(action="add", scope="task", item=once),
                        user_request=user_once)
    check("one-time-saved", code == 0, result)
    one_id = result["id"]
    one_context = dict(CONTEXT, task_id="one-time-evidence-first",
                       current_requirements=[user_once],
                       conflicts=[dict(preference_id=ids[1], priority="current_request",
                                       reason="本次明确要求材料先行，仅排除相反的作者顺序偏好。")])
    one_load = load("load-one-time", one_context)
    check("one-time-priority", one_load["active"][0]["id"] == one_id
          and ids[1] not in [x["id"] for x in one_load["active"]]
          and len(one_load["skipped"]) == 1, one_load)
    later = load("load-new-task", dict(CONTEXT, task_id="compress-02"))
    check("one-time-does-not-leak", one_id not in [x["id"] for x in later["active"]]
          and ids[1] in [x["id"] for x in later["active"]], later)

    chinese = load("load-other-language", dict(CONTEXT, language="zh"))
    method = load("load-other-section", dict(CONTEXT, section="methods"))
    quantitative = load("load-other-research-type", dict(CONTEXT, research_type="quantitative"))
    new_task = load("load-other-task-kind", dict(CONTEXT, task="new"))
    for label, data in (("language", chinese), ("section", method),
                        ("research-type", quantitative), ("task-kind", new_task)):
        check("filter-" + label, not data["active"], data)

    # The simulated user has not answered this suggestion. Do not claim acceptance.
    unanswered_source = dict(kind="choice", evidence="助理提出改用 could；合成用户尚未回应。",
                              decision="accept", original="Administrators should protect time.",
                              suggestion="Administrators could protect time.",
                              selected="Administrators could protect time.", user_response="")
    unanswered = preference("把 should 改成 could。", scope="project", source=unanswered_source)
    project_store = ENABLED / "edu_output/project/preferences.json"
    before = project_store.read_bytes()
    code, response = call("unanswered-choice-rejected", dict(action="add", scope="project",
                                                            item=unanswered),
                          user_request="（用户未答复助理的修改建议；测试不能将沉默当同意。）")
    check("silence-is-not-acceptance", code == 2 and project_store.read_bytes() == before, response)

    inferred = preference("作者可能偏好将建议与概念判断放在同一句，待确认。",
                          scope="project", basis="inferred", status="candidate",
                          source=dict(kind="example", evidence="合成原段只有一条实践建议；不能推出稳定句式偏好。",
                                      ownership="author", time="2026-10-20"))
    code, candidate = call("add-project-candidate", dict(action="add", scope="project",
                                                        item=inferred))
    candidate_load = load("load-candidate")
    check("candidate-separated", code == 0
          and candidate["id"] in [x["id"] for x in candidate_load["candidates_for_review_only"]]
          and candidate["id"] not in [x["id"] for x in candidate_load["active"]], candidate_load)

    profile_before = PROFILE.read_bytes()
    code, result = call("disable-profile-for-project", dict(action="personal", enabled=False),
                        user_request="这个项目暂停使用个人偏好档案，其他项目照旧。")
    disabled = load("load-project-with-profile-disabled")
    other = load("load-other-project-still-enabled", project=OTHER)
    check("project-disable-only", code == 0 and not disabled["active"]
          and len(other["active"]) == 3 and PROFILE.read_bytes() == profile_before,
          dict(disabled=disabled, other=other))
    call("undo-project-disable", dict(action="personal", enabled=True),
         user_request="撤销刚才这个项目的停用。")
    restored = load("load-after-undo-disable")
    check("undo-disable-restores", len(restored["active"]) == 3, restored)

    call("pause-author-item", dict(action="update", scope="author", id=ids[2],
                                   changes={"status": "paused"}),
         user_request="暂停 should 这条偏好，其他偏好继续。")
    paused = load("load-after-pause")
    check("pause-removes-from-active", ids[2] not in [x["id"] for x in paused["active"]]
          and len(paused["active"]) == 2, paused)
    call("resume-author-item", dict(action="update", scope="author", id=ids[2],
                                    changes={"status": "active"}),
         user_request="恢复刚才暂停的 should 偏好。")
    resumed = load("load-after-resume")
    check("resume-restores", len(resumed["active"]) == 3, resumed)

    # Explicit synthetic request authorizes this example-bearing record.
    short_example = "Within shared aims, teachers judge the next classroom step."
    example_item = preference("保留判断与课程框架的简短连接。", source=dict(
        kind="example", ownership="author",
        evidence="我认可这个短例，以后英文定性 Discussion 修改可参考其论证连接。",
        cross_project_authorization="以后英文定性 Discussion 修改可参考其论证连接。",
        example=short_example, time="2026-10-20"))
    code, example_result = call("add-example-for-delete", dict(action="add", scope="author",
                                                               item=example_item),
                               user_request="我认可这个短例，以后英文定性 Discussion 修改可参考其论证连接。")
    example_id = example_result["id"]
    check("example-actually-saved", code == 0 and short_example in PROFILE.read_text("utf-8"),
          dict(id=example_id))
    call("delete-example", dict(action="delete", scope="author", id=example_id),
         user_request="删除刚才的短例偏好，连同来源和短例一起删除。")
    profile_content = PROFILE.read_text("utf-8")
    residual = [str(p.relative_to(BASE)) for root in (BASE / "private-profile", ENABLED / "edu_output/project")
                for p in root.rglob("*") if p.is_file()
                and short_example in p.read_text("utf-8", errors="replace")]
    check("delete-physically-removes-example", example_id not in profile_content
          and short_example not in profile_content and not residual,
          dict(storage_residual_files=residual,
               scope="Only actual profile/project storage scanned; synthetic test logs intentionally retained."))
    code, delete_again = call("delete-example-again", dict(action="delete", scope="author", id=example_id))
    check("delete-idempotent", code == 0 and delete_again["changed"] is False, delete_again)

    undo_example = "Judgment remains answerable to shared curricular purposes."
    undo_item = deepcopy(example_item)
    undo_item["content"] = "保留判断与共同目标的联系。"
    undo_item["source"]["example"] = undo_example
    code, undo_result = call("add-example-for-undo", dict(action="add", scope="author",
                                                         item=undo_item))
    undo_id = undo_result["id"]
    check("undo-example-actually-saved", code == 0 and undo_example in PROFILE.read_text("utf-8"),
          dict(id=undo_id))
    call("undo-last-add", dict(action="undo_add", scope="author", id=undo_id),
         user_request="撤销刚才记住的这一条。")
    check("undo-removes-example", undo_id not in PROFILE.read_text("utf-8")
          and undo_example not in PROFILE.read_text("utf-8"),
          dict(removed_id=undo_id))

    # This test exercises the documented management example literally, then repairs locally.
    before = PROFILE.read_bytes()
    code, response = call("documented-pause-form-on-author-item",
                          dict(action="update", id=ids[0], changes={"status": "paused"}),
                          user_request="暂停概念标签那条个人偏好。")
    check("documented-pause-example-handles-author-item", code == 0,
          dict(profile_unchanged=before == PROFILE.read_bytes(),
               expected_behavior="Pause selected author item with supplied profile."))
    if code != 0:
        call("repair-pause-with-explicit-author-scope",
             dict(action="update", scope="author", id=ids[0], changes={"status": "paused"}))
        fixed = load("load-after-repaired-pause")
        check("explicit-author-scope-fixes-pause",
              ids[0] not in [x["id"] for x in fixed["active"]], fixed)
        call("restore-after-pause-documentation-test",
             dict(action="update", scope="author", id=ids[0], changes={"status": "active"}))

    # Inspect all current records without reading any unrelated profile or project.
    call("list-final-author-and-project", dict(action="list"),
         user_request="查看目前记住了哪些条目。")
    final = load("final-load")
    save(BASE / "management-results.json", dict(checks=checks, final=final,
                                                one_time_load=one_load))
    print(json.dumps(dict(checks=[dict(name=x["name"], passed=x["passed"]) for x in checks],
                          failures=[x for x in checks if not x["passed"]]),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    {"setup": setup, "manage": manage}[sys.argv[1]]()
