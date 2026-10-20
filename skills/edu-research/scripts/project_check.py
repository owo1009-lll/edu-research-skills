"""User-triggered material update checks. Semantic mappings are reader judgments.

inventory --files FILE... --out inventory.json
register --project DIR --spec internally-prepared.json
check --project DIR [--relocations explicit-id-path-map.json]
sync --project DIR --request authorized-edits.json

The assistant prepares these records from the user's ordinary request and inspected
materials. Scripts never select an authoritative result by filename or timestamp.
"""
import argparse
from copy import deepcopy
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "edu-shared" / "scripts"))
from private_store import digest, locked, private_path, read_json, utc, write_json
from project_documents import locate, read_document, replace_docx

IDENTITY = {"outcome", "comparison", "timepoint", "sample", "statistic", "unit",
            "model", "adjustments", "analysis", "uncertainty"}
JUDGMENTS = {"consistent": "已一致", "stale": "疑似旧内容", "review": "需重新判断", "unchecked": "未能检查"}


def binding_key(item):
    return item["id"]


def confirmed_run_valid(files, authority):
    try:
        run = read_json(files[authority["run_status"]]["path"], {})
        provenance = read_json(files[authority["provenance"]]["path"], {})
        return (run.get("status") == "completed" and run.get("returncode") == 0
                and bool(provenance.get("script", {}).get("sha256"))
                and isinstance(provenance.get("inputs"), dict))
    except (KeyError, ValueError, OSError, AttributeError):
        return False


def state_path(project):
    return private_path(Path(project) / "edu_output" / "project" / "materials.json")


def report_path(project):
    return private_path(Path(project) / "edu_output" / "project" / "check.json")


def binding(document, item, previous=None):
    target, status = locate(document, item, previous)
    if target is None:
        return {"status": "unchecked", "reason": status}
    if target["kind"] == "formula":
        return {"status": "unchecked", "reason": "Spreadsheet formula has not been recalculated.", **target}
    for guard in item.get("guards", []):
        found = [u for u in document["units"] if u["locator"] == guard["locator"]]
        if len(found) != 1 or found[0]["text"] != str(guard["equals"]):
            return {"status": "review", "reason": "Context guard changed: " + guard["locator"], **target}
    if previous and previous.get("text") != target["text"] and target["kind"] in {
        "text", "paragraph", "table_paragraph", "pdf_text", "slide_text", "notes"
    }:
        # A changed prose unit may change its comparator/model, not merely its value.
        # A reader can refresh the binding after inspecting its current context.
        if item.get("reviewed_sha256") != document["sha256"]:
            return {"status": "review", "reason": "Prose changed; semantic mapping needs fresh reading.", **target}
    pattern = item.get("pattern")
    if pattern:
        matches = list(re.finditer(pattern, target["text"]))
        if len(matches) != 1 or "value" not in matches[0].groupdict():
            return {"status": "review", "reason": "Value pattern is absent or ambiguous.", **target}
        values = {k: v for k, v in matches[0].groupdict().items() if v is not None}
    else:
        values = {"value": target["text"]}
    return {**target, "status": "read", "values": values, "relocation": status}


def numeric(text):
    return Decimal(str(text).replace("−", "-").replace(",", "").strip().rstrip("%"))


def compare(expected, actual, source, occurrence):
    """Display equivalence is explicit, not evidence of semantic equivalence."""
    if expected.get("status") != "read" or actual.get("status") != "read":
        return "review", "Mapping or extraction requires review."
    if source.get("value_type", "number") == "text":
        equal = expected["values"] == actual["values"]
        return ("consistent", "Same recorded text.") if equal else ("stale", "Text differs from the confirmed source.")
    if set(expected["values"]) != set(actual["values"]):
        return "review", "Uncertainty/value fields differ."
    equivalent = True
    try:
        for name, text in expected["values"].items():
            e = numeric(text) * Decimal(str(source.get("scale", 1)))
            a = numeric(actual["values"][name]) * Decimal(str(occurrence.get("scale", 1)))
            if not e.is_finite() or not a.is_finite():
                return "unchecked", "Non-finite number cannot be compared."
            if e == a:
                continue
            # Rounding only in the display scale, and only when explicitly mapped.
            places = occurrence.get("display_decimals")
            if places is None:
                equivalent = False
                continue
            scale = Decimal(str(occurrence.get("scale", 1)))
            rendered = (e / scale).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP) * scale
            refs = source.get("reference_values", [0])
            if rendered == a and any((e - Decimal(str(r))).compare(0) != (a - Decimal(str(r))).compare(0) for r in refs):
                return "review", "Displayed precision changes sign or relation to a reference boundary."
            if rendered != a:
                equivalent = False
        return ("consistent", "Same value or explicitly permitted display rounding.") if equivalent else (
            "stale", "Value differs from the confirmed source for this analysis identity.")
    except (InvalidOperation, ValueError, TypeError, ZeroDivisionError):
        return "review", "Value is not a supported finite decimal; inspect its reporting convention."


def all_bindings(spec):
    for fact in spec.get("facts", []):
        yield from fact["sources"]
        yield from fact["occurrences"]
    for link in spec.get("dependencies", []):
        yield link["target"]
    for claim in spec.get("citations", []):
        yield claim["claim"]
        yield claim["support"]


def validate(spec, docs):
    files = {x["id"]: x for x in spec["files"]}
    if len(files) != len(spec["files"]):
        raise ValueError("Duplicate file IDs")
    for record in files.values():
        if not record.get("role"):
            raise ValueError("Each explicitly selected file needs its project role.")
    keys = [f["id"] for f in spec.get("facts", [])]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate fact IDs")
    for fact in spec.get("facts", []):
        if set(fact["identity"]) != IDENTITY or any(not str(v).strip() for v in fact["identity"].values()):
            raise ValueError("Facts require all semantic identity dimensions; mark inapplicable dimensions explicitly.")
        if not fact.get("mapping_reason"):
            raise ValueError("Record the reader's evidence for each semantic mapping.")
        source_ids = [x["id"] for x in fact["sources"]]
        if len(source_ids) != len(set(source_ids)):
            raise ValueError("Duplicate source IDs")
        authority = fact.get("authority")
        if authority:
            if authority.get("source") not in source_ids or authority.get("kind") not in {
                "user_confirmed", "confirmed_run", "project_record"
            } or not authority.get("reason"):
                raise ValueError("Authority requires explicit provenance, not recency or significance.")
            if authority["kind"] == "confirmed_run":
                run = files.get(authority.get("run_status"))
                provenance = files.get(authority.get("provenance"))
                if not run or not provenance:
                    raise ValueError("Confirmed runs require explicitly registered run_status and provenance files.")
                if not confirmed_run_valid(files, authority):
                    raise ValueError("The selected run lacks successful execution and recorded input/script provenance.")
    bindings = list(all_bindings(spec))
    ids = [x.get("id") for x in bindings]
    if len(ids) != len(set(ids)) or None in ids or "" in ids:
        raise ValueError("Every mapping needs a unique, stable binding ID.")
    for item in bindings:
        if item.get("file") not in files or not item.get("locator") or not item.get("reason"):
            raise ValueError("Every binding needs an authorized file, precise locator and semantic reason.")
        if item.get("pattern"):
            try:
                if "value" not in re.compile(item["pattern"]).groupindex:
                    raise ValueError("Value patterns need a named value group.")
            except re.error as error:
                raise ValueError(f"Invalid value pattern: {error}")
        if item.get("scale", 1) != 1 and not item.get("conversion_reason"):
            raise ValueError("Unit conversion needs an explicit dimensional justification.")
        if item.get("display_decimals") is not None and (
            not isinstance(item["display_decimals"], int) or not 0 <= item["display_decimals"] <= 15
        ):
            raise ValueError("display_decimals must be an integer from 0 to 15")
    edges = spec.get("dependencies", [])
    nodes = set(keys) | {x["id"] for x in edges}
    if len(nodes) != len(keys) + len(edges):
        raise ValueError("Dependency and fact identities must be unique.")
    for edge in edges:
        if not edge.get("reason") or not edge.get("depends_on") or not set(edge["depends_on"]) <= nodes:
            raise ValueError("Dependencies need known parents and a substantive reason.")
    visiting, visited = set(), set()
    parents = {x["id"]: x["depends_on"] for x in edges}
    def visit(key):
        if key in visiting:
            raise ValueError("Dependency cycle")
        if key in visited:
            return
        visiting.add(key)
        for parent in parents.get(key, []):
            visit(parent)
        visiting.remove(key)
        visited.add(key)
    for key in parents:
        visit(key)
    for claim in spec.get("citations", []):
        if not claim.get("reference_id") or not claim.get("reader") or claim.get("source_file") not in files:
            raise ValueError("Citation links need existing reference identity, reader and registered source.")
        if claim.get("ledger_file") not in files:
            raise ValueError("Register the existing citation support ledger.")
    for deck in spec.get("decks", []):
        if deck.get("ppt") not in files or deck.get("plan") not in files:
            raise ValueError("Deck checks require registered PPTX and plan files.")


def read_scope(spec):
    return {item["id"]: read_document(item["path"]) for item in spec["files"]}


def snapshots(spec, docs):
    result = {}
    for item in all_bindings(spec):
        key = binding_key(item)
        result[key] = binding(docs[item["file"]], item)
    return result


def register(project, spec):
    path = state_path(project)
    spec = deepcopy(spec)
    for file in spec["files"]:
        file["path"] = str(Path(file["path"]).resolve())
    docs = read_scope(spec)
    validate(spec, docs)
    with locked(path):
        prior = read_json(path)
        if prior:
            if prior["spec"] == spec:
                return {"status": "already_registered", "changed": False}
            raise ValueError("Project already registered. Use refresh to preserve its baseline.")
        state = {"schema": 1, "created_utc": utc(), "spec": spec,
                 "baseline": {key: {"sha256": d["sha256"], "status": d["status"]} for key, d in docs.items()},
                 "bindings": snapshots(spec, docs)}
        # Frozen dependency/citation content must be tied to the initial reading.
        state["citation_fingerprints"] = citation_fingerprints(spec, docs)
        write_json(path, state)
    return check(project)


def citation_fingerprints(spec, docs):
    result = {}
    files = {item["id"]: item for item in spec["files"]}
    for claim in spec.get("citations", []):
        c = binding(docs[claim["claim"]["file"]], claim["claim"])
        s = binding(docs[claim["support"]["file"]], claim["support"])
        try:
            ledger = read_json(files[claim["ledger_file"]]["path"], {})
            records = [x for x in ledger.get("claims", ledger.get("semantic_review", []))
                       if x.get("block_id") == claim.get("block_id", claim["id"])
                       and x.get("reference_id") == claim["reference_id"]]
            references = [x for x in ledger.get("references", [])
                          if x.get("id") == claim["reference_id"]]
            supported = len(records) == 1 and records[0].get("status") == "supported"
        except (OSError, ValueError, AttributeError):
            records, references, supported = [], [], False
        result[claim["id"]] = {
            "claim": digest(c.get("text")), "support": digest(s.get("text")),
            "source": docs[claim["source_file"]]["sha256"],
            "ledger": digest({"claims": records, "references": references}),
            "readable": c.get("status") == "read" and s.get("status") == "read" and supported
        }
    return result


def check(project, relocations=None):
    path = state_path(project)
    with locked(path):
        state = read_json(path)
        if not state:
            raise ValueError("No project record. Inventory selected materials and establish the current baseline first.")
        spec = state["spec"]
        if relocations:
            known = {x["id"]: x for x in spec["files"]}
            if not set(relocations) <= known.keys():
                raise ValueError("Relocations can only address explicitly registered file IDs.")
            for key, new_path in relocations.items():
                known[key]["path"] = str(Path(new_path).resolve())
            write_json(path, state)
        docs = read_scope(spec)
        rows, changes, affected = [], {}, set()
        file_by_id = {x["id"]: x for x in spec["files"]}
        for key, d in docs.items():
            old = state["baseline"][key]
            changes[key] = "missing" if d["status"] == "missing" else (
                "unchanged" if old["sha256"] == d["sha256"] else "changed")

        def read(item):
            return binding(docs[item["file"]], item, state["bindings"].get(binding_key(item)))

        def row(item, status, reason, actual=None, expected=None, **extra):
            rows.append({
                "file_id": item["file"], "file": file_by_id[item["file"]]["path"],
                "binding_id": item.get("id"),
                "location": (actual or {}).get("locator", item["locator"]),
                "current": (actual or {}).get("text"), "new_material": expected,
                "status": status, "judgment": JUDGMENTS[status], "reason": reason,
                "suggestion": {"consistent": "保留；对应值一致，语义解释仍按上下文判断。",
                               "stale": "核对本处归属后同步；不要全局替换同一数字。",
                               "review": "重新阅读相关材料并判断，不自动选结果或改写。",
                               "unchecked": "补足可读材料或重新定位后检查。"}[status],
                **extra
            })

        for fact in spec.get("facts", []):
            authority = fact.get("authority")
            invalid_run = authority and authority["kind"] == "confirmed_run" and not confirmed_run_valid(file_by_id, authority)
            if not authority or invalid_run:
                affected.add(fact["id"])
                for target in fact["occurrences"] or fact["sources"]:
                    reason = ("Confirmed analysis run is no longer readable/successful with provenance." if invalid_run else
                              "Authoritative version is not established; alternative results were retained.")
                    row(target, "review", reason,
                        read(target), fact_id=fact["id"])
                continue
            source = next(x for x in fact["sources"] if x["id"] == authority["source"])
            expected = read(source)
            prior = state["bindings"].get(binding_key(source), {})
            changed = expected.get("values") != prior.get("values")
            if changed or expected["status"] != "read":
                affected.add(fact["id"])
            if expected["status"] != "read":
                row(source, expected["status"], expected["reason"], expected, fact_id=fact["id"])
            for target in fact["occurrences"]:
                actual = read(target)
                if expected["status"] != "read":
                    status, reason = "review", "Confirmed source is unavailable or its context changed."
                elif actual["status"] != "read":
                    status, reason = actual["status"], actual["reason"]
                else:
                    status, reason = compare(expected, actual, source, target)
                if status != "consistent":
                    # On first use, source history is unknown but a current mismatch
                    # still makes dependent interpretations worth re-reading.
                    affected.add(fact["id"])
                row(target, status, reason, actual, {
                    "file": file_by_id[source["file"]]["path"], "location": source["locator"],
                    "values": expected.get("values"), "authority": authority,
                    "identity": fact["identity"]
                }, fact_id=fact["id"], source_changed_since_baseline=changed)
        # Dependency propagation is independent of the order of declared edges.
        pending = list(spec.get("dependencies", []))
        while pending:
            ready = [x for x in pending if not any(y["id"] in x["depends_on"] for y in pending)]
            for edge in ready:
                target = edge["target"]
                actual = read(target)
                previous = state["bindings"].get(binding_key(target), {})
                changed_text = actual.get("text") != previous.get("text")
                triggered = bool(set(edge["depends_on"]) & affected) or changed_text
                if triggered or actual["status"] != "read":
                    affected.add(edge["id"])
                    decision = edge.get("decision", {})
                    fingerprint = digest({"files": {k: d["sha256"] for k, d in docs.items()},
                                          "target": actual.get("text")})
                    if (decision.get("fingerprint") == fingerprint and decision.get("reader")
                            and decision.get("reason") and decision.get("status") == "still_supported"):
                        row(target, "consistent", "Reader judged this interpretation still supported: " + decision["reason"],
                            actual, dependency_id=edge["id"])
                    else:
                        row(target, "unchecked" if actual["status"] == "unchecked" else "review",
                            "Related material or wording changed: " + edge["reason"], actual,
                            dependency_id=edge["id"], review_fingerprint=fingerprint)
            pending = [x for x in pending if x not in ready]
        now_citations = citation_fingerprints(spec, docs)
        for claim in spec.get("citations", []):
            now = now_citations[claim["id"]]
            old = state["citation_fingerprints"].get(claim["id"])
            valid = now == old and now["readable"]
            row(claim["claim"], "consistent" if valid else "review",
                "Recorded support unchanged (reader judgment)." if valid else
                "Claim, source version, support passage or citation ledger changed; old support is pending re-review.",
                read(claim["claim"]), citation_id=claim["id"], support_status="recorded" if valid else "pending")
        deck_checks = []
        checked_decks = set()
        if spec.get("decks"):
            sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "edu-ppt" / "scripts"))
            from check_deck import check as check_native_deck
            for deck in spec["decks"]:
                try:
                    result = check_native_deck(file_by_id[deck["ppt"]]["path"], file_by_id[deck["plan"]]["path"])
                    deck_checks.append(dict(deck, result=result))
                    checked_decks.add(deck["ppt"])
                    for error in result["errors"]:
                        row({"file": deck["ppt"], "locator": "native deck objects"}, "review", error)
                except Exception as error:
                    deck_checks.append(dict(deck, status="unchecked", reason=str(error)))
                    row({"file": deck["ppt"], "locator": "native deck objects"}, "unchecked", str(error))
        for key, doc in docs.items():
            for gap in doc["unchecked"]:
                if key in checked_decks and gap["reason"].startswith("Chart label formatting/geometry"):
                    continue
                row({"file": key, "locator": gap["location"]}, "unchecked", gap["reason"])
        bound = {(x["file"], x["locator"]) for x in all_bindings(spec)}
        coverage = {key: {"read_units": len(d["units"]),
                          "mapped_units": sum((key, u["locator"]) in bound for u in d["units"]),
                          "unmapped_locations": [u["locator"] for u in d["units"] if (key, u["locator"]) not in bound],
                          "parser_status": d["status"]} for key, d in docs.items()}
        report = {
            "schema": 1, "input_fingerprint": digest({"spec": spec, "hashes": {k: d["sha256"] for k, d in docs.items()}}),
            "files": {key: {"path": d["path"], "sha256": d["sha256"], "baseline_state": changes[key]} for key, d in docs.items()},
            "findings": rows, "coverage": coverage, "deck_checks": deck_checks,
            "scope": "Only explicitly registered semantic mappings. Unmapped units and unreadable objects are not certified. "
                     "First use establishes a current baseline, not historical change. Scripts verify bytes/locations/values; "
                     "the reader establishes analysis identity and interpretation.",
        }
        previous_report = read_json(report_path(project))
        if report != previous_report:
            write_json(report_path(project), report)
            write_report(project, report)
        return report


def write_report(project, report):
    out = private_path(Path(project) / "edu_output" / "project" / "check.md")
    def cell(value):
        return str(value if value is not None else "—").replace("|", "\\|").replace("\n", " ")
    counts = {label: sum(x["status"] == key for x in report["findings"]) for key, label in JUDGMENTS.items()}
    lines = ["# 材料关联核对", "", "只核对登记材料和明确对应的位置；未映射及未解析内容不作一致性保证。",
             "；".join(f"{label} {count} 处" for label, count in counts.items()) + "。完整明细在 check.json。",
             "", "| 文件及位置 | 当前内容 | 对应材料 | 判断 | 处理依据 |", "|---|---|---|---|---|"]
    for item in report["findings"]:
        if item["status"] == "consistent":
            continue
        source = item["new_material"]
        if isinstance(source, dict) and "file" in source:
            source = Path(source["file"]).name + " / " + source["location"] + ": " + str(source.get("values", ""))
        lines.append("| " + " | ".join(cell(x) for x in (
            Path(item["file"]).name + " / " + item["location"], item["current"],
            source, item["judgment"], item["reason"] + " " + item["suggestion"])) + " |")
    lines += ["", "## 检查范围", ""]
    for key, scope in report["coverage"].items():
        lines.append(f"- {key}: 读取 {scope['read_units']} 个单元，映射 {scope['mapped_units']} 个；"
                     f"解析状态 {scope['parser_status']}。其余单元需结合正文判断。")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def refresh(project, request):
    """Refresh inspected mappings without resetting historical facts or citation support."""
    path = state_path(project)
    with locked(path):
        state = read_json(path)
        if not request.get("reader") or not request.get("reason"):
            raise ValueError("Refresh requires an actual reader and rationale.")
        spec = deepcopy(state["spec"])
        allowed = {"facts", "dependencies", "citations"}
        if not set(request.get("replace", {})) <= allowed:
            raise ValueError("Refresh only explicit facts, dependencies or citation mappings.")
        spec.update(deepcopy(request.get("replace", {})))
        docs = read_scope(spec)
        validate(spec, docs)
        for item in all_bindings(spec):
            if item.get("reviewed_sha256") and item["reviewed_sha256"] != docs[item["file"]]["sha256"]:
                raise ValueError("Refreshed locator targets an obsolete file.")
        state["spec"] = spec
        # New mappings start with current content; existing mapping keys retain old baseline.
        for key, value in snapshots(spec, docs).items():
            state["bindings"].setdefault(key, value)
        for claim_id in request.get("reverified_citations", []):
            claims = {x["id"]: x for x in spec.get("citations", [])}
            if claim_id not in claims or not claims[claim_id].get("review_reason"):
                raise ValueError("Citation re-verification requires a new substantive support rationale.")
            state["citation_fingerprints"][claim_id] = citation_fingerprints(spec, docs)[claim_id]
        write_json(path, state)
    return check(project)


def synchronize(project, request):
    """Apply explicitly authorized, current, unambiguous text replacements to new files."""
    if not request.get("authorization") or not request.get("edits"):
        raise ValueError("Explicit user authorization and individually scoped edits are required.")
    report = check(project)
    if request.get("report_fingerprint") != report["input_fingerprint"]:
        raise ValueError("Materials changed after inspection. Review fresh findings before synchronizing.")
    state = read_json(state_path(project))
    files = {x["id"]: x for x in state["spec"]["files"]}
    facts = {x["id"]: x for x in state["spec"]["facts"]}
    bindings = {binding_key(x): x for x in all_bindings(state["spec"])}
    current_docs = read_scope(state["spec"])
    prepared = []
    for group in request["edits"]:
        source = Path(files[group["file"]]["path"])
        output = private_path(group["output"])
        if output == source.resolve() or output.exists():
            raise ValueError("Synchronization must preserve originals and use a new output path.")
        if output.suffix.lower() != source.suffix.lower():
            raise ValueError("Output extension must match source.")
        doc = read_document(source)
        if doc["sha256"] != report["files"][group["file"]]["sha256"]:
            raise ValueError("Source changed during synchronization.")
        changes = group["replacements"]
        used = set()
        for edit in changes:
            unresolved = [f for f in report["findings"] if f["file_id"] == group["file"]
                          and f["location"] == edit["locator"] and f["status"] in {"review", "unchecked"}]
            if unresolved:
                raise ValueError("This location also contains unresolved evidence; re-read and narrow the edit before synchronization.")
            matching = [f for f in report["findings"] if f["file_id"] == group["file"]
                        and f["location"] == edit["locator"] and f["status"] in {"stale", "consistent"}]
            if not matching or not edit.get("reason"):
                raise ValueError("Only inspected, unambiguous locations can be synchronized automatically.")
            actual = [u for u in doc["units"] if u["locator"] == edit["locator"]]
            if len(actual) != 1 or actual[0]["text"] != edit["before"] or not edit.get("old"):
                raise ValueError("Stale edit location.")
            if edit["before"].count(edit["old"]) != 1 or edit["locator"] in used:
                raise ValueError("Ambiguous/repeated edit; combine changes in one reviewed replacement.")
            if actual[0].get("editable") is False:
                raise ValueError("Complex Word object requires editing on a copy.")
            proposed = deepcopy(doc)
            new_text = edit["before"].replace(edit["old"], edit["new"], 1)
            for obj in proposed["units"]:
                if obj["locator"] == edit["locator"]:
                    obj["text"] = new_text
            for finding in matching:
                if "fact_id" not in finding:
                    continue
                fact = facts[finding["fact_id"]]
                source_binding = next(x for x in fact["sources"] if x["id"] == fact["authority"]["source"])
                target_binding = deepcopy(bindings[finding["binding_id"]])
                target_binding["locator"] = edit["locator"]
                expected = binding(current_docs[source_binding["file"]], source_binding)
                proposed_value = binding(proposed, target_binding)
                status, reason = compare(expected, proposed_value, source_binding, target_binding)
                if status != "consistent":
                    raise ValueError("Proposed replacement does not match the authoritative material: " + reason)
            used.add(edit["locator"])
        if source.suffix.lower() not in {".md", ".txt", ".docx", ".json"}:
            raise ValueError("For PPTX/charts, update the verified plan and rebuild with edu-ppt; other formats require a reviewed new copy.")
        prepared.append((source, output, changes))
    if len({output for _, output, _ in prepared}) != len(prepared):
        raise ValueError("Duplicate output destinations")
    results = []
    for source, output, changes in prepared:
        output.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix.lower() == ".docx":
            replace_docx(source, changes, output)
        elif source.suffix.lower() == ".json":
            value = read_json(source)
            for edit in changes:
                keys = edit["locator"].removeprefix("json:").split("/")[1:]
                keys = [k.replace("~1", "/").replace("~0", "~") for k in keys]
                target = value
                for key in keys[:-1]:
                    target = target[int(key)] if isinstance(target, list) else target[key]
                key = int(keys[-1]) if isinstance(target, list) else keys[-1]
                old = target[key]
                replacement = edit["before"].replace(edit["old"], edit["new"], 1)
                target[key] = type(old)(replacement) if isinstance(old, (int, float)) and not isinstance(old, bool) else replacement
            with output.open("x", encoding="utf-8") as stream:
                json.dump(value, stream, ensure_ascii=False, indent=2)
                stream.write("\n")
        else:
            lines = source.read_text(encoding="utf-8-sig").splitlines(keepends=True)
            for edit in changes:
                idx = int(edit["locator"].split(":")[-1]) - 1
                lines[idx] = lines[idx].replace(edit["old"], edit["new"], 1)
            with output.open("x", encoding="utf-8", newline="") as stream:
                stream.write("".join(lines))
        results.append({"source": str(source), "output": str(output),
                        "sha256": digest(output.read_bytes())})
    return {"files": results, "next": "Register explicit new paths, refresh changed semantic mappings, and check again. "
            "For changed PPT plans, rebuild_deck, check_deck and render all affected slides."}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    inv = sub.add_parser("inventory")
    inv.add_argument("--files", nargs="+", type=Path, required=True)
    inv.add_argument("--out", type=Path, required=True)
    for name in ("register", "check", "refresh", "sync"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--project", type=Path, required=True)
        if name == "register":
            cmd.add_argument("--spec", type=Path, required=True)
        if name in {"refresh", "sync"}:
            cmd.add_argument("--request", type=Path, required=True)
        if name == "check":
            cmd.add_argument("--relocations", type=Path)
    args = p.parse_args()
    try:
        if args.command == "inventory":
            result = [read_document(x) for x in args.files]
            write_json(args.out, result)
        elif args.command == "register":
            result = register(args.project, read_json(args.spec))
        elif args.command == "refresh":
            result = refresh(args.project, read_json(args.request))
        elif args.command == "sync":
            result = synchronize(args.project, read_json(args.request))
        else:
            result = check(args.project, read_json(args.relocations) if args.relocations else None)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, KeyError, OSError) as error:
        p.exit(2, str(error) + "\n")


if __name__ == "__main__":
    main()
