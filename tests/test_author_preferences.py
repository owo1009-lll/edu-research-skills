"""Behavioral storage contracts using synthetic user statements, never private prose."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/edu-writing/scripts"))
from author_preferences import operate


def preference(**changes):
    item = {
        "content": "State the judgment before the supporting evidence.",
        "category": "expression", "basis": "explicit", "scope": "project", "status": "active",
        "languages": ["en"], "research_types": ["mixed"], "sections": ["discussion"],
        "tasks": ["revise"], "conditions": ["The judgment has evidence."],
        "exceptions": ["Do not turn association into causation."],
        "source": {"kind": "explicit", "evidence": "For this paper, state my judgment first.",
                   "time": "2026-10-20", "example": "Participation is uneven; the two strands explain why."}
    }
    item.update(changes)
    return item


def context(**changes):
    c = {"language": "en", "research_type": "mixed", "section": "discussion", "task": "revise",
         "task_id": "task-one"}
    c.update(changes)
    return c


class Preferences(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "paper"
        self.profile = Path(self.temp.name) / "author.json"

    def call(self, action, **args):
        return operate(self.project, dict(action=action, **args), self.profile)

    def test_task_requirement_does_not_leak(self):
        self.call("add", item=preference(scope="task", task_id="task-one"))
        self.assertEqual(len(self.call("load", context=context())["active"]), 1)
        self.assertFalse(self.call("load", context=context(task_id="task-two"))["active"])
        self.assertFalse(self.profile.exists())

    def test_explicit_long_term_memory_is_available_in_another_project(self):
        item = preference(scope="author")
        item["source"]["cross_project_authorization"] = "Remember this for future papers."
        self.call("add", scope="author", item=item)
        other = Path(self.temp.name) / "other"
        result = operate(other, {"action": "load", "context": context()}, self.profile)
        self.assertEqual(len(result["active"]), 1)
        self.assertFalse(operate(other, {"action": "load", "context": context()})["active"])

    def test_inference_remains_local_candidate(self):
        item = preference(basis="inferred", status="candidate")
        item["source"] = {"kind": "example", "ownership": "other",
                          "evidence": "User supplied a public style example.", "example": "A short synthetic example."}
        self.call("add", item=item)
        result = self.call("load", context=context())
        self.assertFalse(result["active"])
        self.assertEqual(len(result["candidates_for_review_only"]), 1)
        item["scope"] = "author"
        with self.assertRaises(ValueError):
            self.call("add", scope="author", item=item)

    def test_silence_is_not_acceptance(self):
        for decision in ["silence", "download", "continue", ""]:
            item = preference()
            item["source"] = {"kind": "choice", "evidence": "No response.", "decision": decision}
            with self.subTest(decision=decision), self.assertRaises(ValueError):
                self.call("add", item=item)

    def test_actual_rejection_records_choice_and_reason(self):
        item = preference()
        item["source"] = {"kind": "choice", "evidence": "User rejected weakened verb.",
                          "decision": "reject", "original": "Schools should provide access.",
                          "suggestion": "Schools could consider providing access.",
                          "selected": "Schools should provide access.", "user_response": "Keep should; this is an access obligation.",
                          "reason": "Normative obligation remains justified."}
        self.call("add", item=item)
        loaded = self.call("load", context=context())["active"][0]
        self.assertEqual(loaded["source"]["selected"], item["source"]["original"])

    def test_language_section_and_research_type_are_filtered(self):
        self.call("add", item=preference())
        for options in [{"language": "zh"}, {"section": "methods"}, {"research_type": "quantitative"},
                        {"task": "new"}]:
            self.assertFalse(self.call("load", context=context(**options))["active"])

    def test_current_request_and_fact_conflicts_override_saved_preference(self):
        key = self.call("add", item=preference())["id"]
        for priority in ["current_request", "fact", "verified_journal"]:
            result = self.call("load", context=context(
                current_requirements=["This paragraph should first present the interview evidence."],
                conflicts=[{"preference_id": key, "priority": priority,
                            "reason": "This specific comparison needs its evidence before the qualified judgment."}]))
            self.assertFalse(result["active"])
            self.assertEqual(result["skipped"][0]["id"], key)

    def test_pause_delete_and_undo_remove_examples_from_all_owned_files(self):
        item = preference()
        item["source"]["example"] = "PRIVATE_SYNTHETIC_EXAMPLE_9271"
        key = self.call("add", item=item)["id"]
        self.call("update", id=key, changes={"status": "paused"})
        self.assertFalse(self.call("load", context=context())["active"])
        self.call("update", id=key, changes={"status": "active"})
        self.assertTrue(self.call("load", context=context())["active"])
        self.call("delete", id=key)
        for p in Path(self.temp.name).rglob("*"):
            if p.is_file():
                self.assertNotIn(b"PRIVATE_SYNTHETIC_EXAMPLE_9271", p.read_bytes())
        key = self.call("add", item=item)["id"]
        self.call("undo_add", id=key)
        self.assertFalse(self.call("load", context=context())["active"])

    def test_project_opt_out_and_idempotent_add(self):
        item = preference(scope="author")
        item["source"]["cross_project_authorization"] = "Use in future projects."
        first = self.call("add", scope="author", item=item)
        second = self.call("add", scope="author", item=item)
        self.assertEqual(first["id"], second["id"])
        self.assertFalse(second["changed"])
        self.call("personal", enabled=False)
        self.assertFalse(self.call("load", context=context())["active"])
        self.call("personal", enabled=True)
        self.assertTrue(self.call("load", context=context())["active"])

    def test_project_facts_and_public_repository_storage_are_rejected(self):
        with self.assertRaises(ValueError):
            self.call("add", item=preference(category="sample_size"))
        with self.assertRaises(ValueError):
            operate(ROOT, {"action": "add", "item": preference()})


if __name__ == "__main__":
    unittest.main()
