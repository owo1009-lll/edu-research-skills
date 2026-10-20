"""User-side author preferences. The assistant translates natural language to requests.

python author_preferences.py --project PROJECT [--profile AUTHORIZED_FILE] < request.json
No implicit discovery of personal profiles. JSON is an internal interface, not a user form.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "edu-shared" / "scripts"))
from private_store import digest, locked, private_path, read_json, utc, write_json

FILTERS = ("languages", "research_types", "sections", "tasks")
STATUSES = {"candidate", "active", "paused", "superseded"}


def empty():
    return {"schema": 1, "use_personal": True, "items": []}


def validate(item):
    if item.get("category") != "expression":
        raise ValueError("Only expression preferences belong here; facts/definitions go in project evidence.")
    if not str(item.get("content", "")).strip():
        raise ValueError("Preference content is required.")
    if item.get("scope") not in {"task", "project", "author"}:
        raise ValueError("scope must be task, project or author")
    if item["scope"] == "task" and not item.get("task_id"):
        raise ValueError("Task preferences need task_id.")
    source = item.get("source", {})
    kind = source.get("kind")
    if kind not in {"explicit", "choice", "example"} or not source.get("evidence"):
        raise ValueError("Provide an actual user statement/choice/example with provenance.")
    if kind == "choice":
        if source.get("decision") not in {"accept", "reject", "select"}:
            raise ValueError("Silence, downloads or continuation are not acceptance.")
        if not all(k in source for k in ("original", "suggestion", "selected", "user_response")):
            raise ValueError("Record the original, suggestion, actual choice and user response.")
        if not source["user_response"]:
            raise ValueError("An actual user choice is required.")
    if kind == "example" and source.get("ownership") not in {"author", "other"}:
        raise ValueError("Identify whether example prose is the author's or another person's.")
    if item.get("basis") not in {"explicit", "inferred"}:
        raise ValueError("basis must distinguish explicit from inferred")
    if item.get("status") not in STATUSES:
        raise ValueError("Invalid preference status.")
    if item["basis"] == "inferred":
        if item["scope"] != "project" or item["status"] not in {"candidate", "paused", "superseded"}:
            raise ValueError("Inferred preferences remain project candidates until explicitly confirmed.")
    if item["scope"] == "author" and not source.get("cross_project_authorization"):
        raise ValueError("Author scope requires the user's explicit cross-project authorization.")
    for key in FILTERS:
        if not isinstance(item.get(key), list) or not item[key] or not all(isinstance(x, str) for x in item[key]):
            raise ValueError(f"{key}: provide explicit selectors (use ['*'] for an authorized broad scope).")
    if not isinstance(item.get("conditions", []), list) or not isinstance(item.get("exceptions", []), list):
        raise ValueError("conditions and exceptions must be lists")


def location(project, scope, profile):
    if scope == "author":
        if not profile:
            raise ValueError("No authorized personal-profile path supplied.")
        return private_path(profile)
    return private_path(Path(project) / "edu_output" / "project" / "preferences.json")


def load_store(path):
    data = read_json(path, empty())
    if data.get("schema") != 1:
        raise ValueError("Unsupported preference schema.")
    return data


def select(project, context, profile=None):
    project_store = load_store(location(project, "project", None))
    stores = [("project", project_store)]
    if profile and project_store["use_personal"] and context.get("use_personal", True):
        stores.append(("author", load_store(location(project, "author", profile))))
    active, candidates, skipped = [], [], []
    required_context = {"language", "research_type", "section", "task"}
    if not required_context <= context.keys():
        raise ValueError("Loading needs language, research_type, section and task.")
    dimensions = dict(zip(FILTERS, ("language", "research_type", "section", "task")))
    current = context.get("current_requirements", [])
    conflicts = {x["preference_id"]: x for x in context.get("conflicts", [])}
    for origin, data in stores:
        for item in data["items"]:
            if item["status"] not in {"active", "candidate"}:
                continue
            if item["scope"] == "task" and item["task_id"] != context.get("task_id"):
                continue
            if any("*" not in item[key] and context[dim] not in item[key] for key, dim in dimensions.items()):
                continue
            view = dict(item, storage=origin)
            if item["id"] in conflicts:
                conflict = conflicts[item["id"]]
                if not conflict.get("reason") or conflict.get("priority") not in {
                    "current_request", "fact", "evidence", "project", "verified_journal"
                }:
                    raise ValueError("Conflict requires a concrete reason and higher-priority requirement.")
                skipped.append({"id": item["id"], "reason": conflict["reason"],
                                "priority": conflict["priority"]})
                continue
            (active if item["status"] == "active" else candidates).append(view)
    active.sort(key=lambda x: {"task": 0, "project": 1, "author": 2}[x["scope"]])
    return {
        "active": active, "candidates_for_review_only": candidates, "skipped": skipped,
        "current_requirements": current,
        "application_order": ["facts_and_evidence", "current_request", "project_and_verified_journal",
                              "task_preference", "project_preference", "author_preference"],
        "limits": "Selectors do not judge semantic conflicts. Apply current requirements first; check "
                  "conditions and exceptions; candidates never authorize rewriting; unchanged prose is valid."
    }


def operate(project, request, profile=None):
    action = request["action"]
    if action == "load":
        return select(project, request["context"], profile)
    if action == "list":
        result = {"project": load_store(location(project, "project", None))}
        if profile:
            result["author"] = load_store(location(project, "author", profile))
        return result
    if action == "personal":
        path = location(project, "project", None)
        with locked(path):
            data = load_store(path)
            if not isinstance(request.get("enabled"), bool):
                raise ValueError("enabled must be true or false")
            data["use_personal"] = request["enabled"]
            write_json(path, data)
        return {"use_personal": data["use_personal"]}
    scope = request.get("scope", "project")
    path = location(project, scope, profile)
    with locked(path):
        data = load_store(path)
        if action == "add":
            item = deepcopy(request["item"])
            if item["scope"] == "author" and scope != "author":
                raise ValueError("Author preferences require the authorized personal store.")
            if item["scope"] != "author" and scope == "author":
                raise ValueError("Task/project preferences stay in the project store.")
            validate(item)
            # A stable evidence-derived ID makes retrying the same request idempotent.
            key = digest({k: v for k, v in item.items() if k not in {"id", "created_utc", "updated_utc"}})[:20]
            item["id"] = "pref-" + key
            old = next((x for x in data["items"] if x["id"] == item["id"]), None)
            if old:
                return {"id": old["id"], "status": old["status"], "changed": False}
            item["created_utc"] = utc()
            data["items"].append(item)
        else:
            item = next((x for x in data["items"] if x["id"] == request.get("id")), None)
            if item is None:
                if action in {"delete", "undo_add"}:
                    return {"deleted": request.get("id"), "changed": False}
                raise ValueError("Preference not found in this authorized store.")
            if action in {"delete", "undo_add"}:
                data["items"] = [x for x in data["items"] if x["id"] != item["id"]]
                write_json(path, data)
                return {"deleted": item["id"], "changed": True}
            if action != "update":
                raise ValueError("Use add/list/load/update/delete/undo_add/personal.")
            patch = request["changes"]
            if {"id", "created_utc", "updated_utc"} & patch.keys():
                raise ValueError("Identity and audit times cannot be edited.")
            if patch.get("scope", item["scope"]) == "author" and scope != "author":
                raise ValueError("Promotion: add with explicit authorization to the personal store, then delete project item.")
            if scope == "author" and patch.get("scope", item["scope"]) != "author":
                raise ValueError("Narrowing: add to the project store, then delete the personal item.")
            if all(item.get(key) == value for key, value in patch.items()):
                return {"id": item["id"], "status": item["status"], "changed": False}
            item.update(deepcopy(patch))
            validate(item)
            item["updated_utc"] = utc()
        write_json(path, data)
        return {"id": item["id"], "status": item["status"], "changed": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--profile", type=Path, help="Only an explicitly authorized personal archive")
    args = parser.parse_args()
    try:
        result = operate(args.project, json.load(sys.stdin), args.profile)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, KeyError, OSError) as error:
        parser.exit(2, str(error) + "\n")


if __name__ == "__main__":
    main()
