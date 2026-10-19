"""Promote the checked revision unchanged and verify the audit files."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import sys

out = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
revision = out / "revised-draft.md"
final = out / "final.md"
if final.exists():
    raise FileExistsError("Final already exists; this promotion is single-use.")
final.write_bytes(revision.read_bytes())
assert sha(final) == sha(revision)
text = final.read_text(encoding="utf-8")
body = "\n".join(line for line in text.splitlines() if not line.startswith("#")).strip()
assert "\ufffd" not in text
assert len([p for p in re.split(r"\n\s*\n", body) if p.strip()]) == 1
assert 140 <= len(re.findall(r"\b\w+(?:[’'-]\w+)*\b", body)) <= 170
assert "Orth et al., 2021" in body and "Voelkle et al. (2014)" in body
assert "Lüdtke" in text
count = json.loads((out / "revised-draft.word-count.json").read_text(encoding="utf-8"))
assert count["sha256"] == sha(final)
count["file"] = str(final)
(out / "final.word-count.json").write_text(json.dumps(count, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
manifest_path = out / "loaded-resources.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["resources"].append({"path": str(Path(__file__).resolve()), "sha256": sha(Path(__file__)), "use": "task-local finalization support, executed"})
for resource in manifest["resources"]:
    assert sha(Path(resource["path"])) == resource["sha256"]
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for item in json.loads((out / "input-file-hashes.json").read_text(encoding="utf-8")):
    assert sha(Path(item["path"])) == item["sha256"]
events = [json.loads(line) for line in (out / "executed-commands.jsonl").read_text(encoding="utf-8").splitlines()]
checks = [item for item in events if "returncode" in item]
assert len(checks) == 4 and all(item["returncode"] == 0 for item in checks)
for item in checks:
    assert Path(item["stdout"]).is_file() and Path(item["stderr"]).is_file()
    assert Path(item["stderr"]).read_text(encoding="utf-8") == ""
event = {"time_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "kind": "final promotion and verification", "argv": sys.orig_argv, "source": str(revision), "destination": str(final), "final_sha256": sha(final), "body_words": count["manuscript_body_words"], "heading_words": count["attribution_heading_words"], "checks_executed_successfully": len(checks), "resource_hashes_verified": len(manifest["resources"]), "input_hashes_verified": 3}
with (out / "executed-commands.jsonl").open("a", encoding="utf-8") as stream:
    stream.write(json.dumps(event, ensure_ascii=False) + "\n")
report = json.dumps(event, ensure_ascii=False, indent=2) + "\n"
(out / "final-verification.json").write_text(report, encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
print(report)
