"""Verify archived bytes and reported loads; this does not score prose quality."""
import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]


def read(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime", action="store_true")
    parser.add_argument("--inputs", action="store_true",
                        help="Also check locally reconstructed long source extracts.")
    args = parser.parse_args()
    manifest = read("publication-manifest.json")
    originals = {}
    for record in manifest["records"]:
        assert sha(ROOT / record["path"]) == record["published_sha256"], record["path"]
        originals[record["path"]] = record["original_sha256"]
        if record["path"].endswith("/final.md"):
            assert record["original_sha256"] == record["published_sha256"]
    snapshot = read("snapshot.json")
    frozen = {r["path"]: r["sha256"] for r in snapshot["files"]}
    if args.runtime:
        for path, digest in frozen.items():
            assert sha(REPO / path) == digest, path
    inputs = {}
    for record in read("inputs-manifest.json"):
        for name, digest in record["files_sha256"].items():
            path = f"{record['id']}/{name}"
            inputs[path] = digest
            if args.inputs or name == "revision-original.md":
                assert sha(ROOT / "inputs" / path) == digest, path
    loads = {}
    for sid in ["F-Q01", "F-L01", "F-M01"]:
        rows = read(f"runs/{sid}/read-log.json")
        assert isinstance(rows, list)
        assert [r["order"] for r in rows] == list(range(1, len(rows) + 1))
        for row in rows:
            path = row["path"].replace("\\", "/")
            if path.startswith("@snapshot/"):
                expected = frozen[path.removeprefix("@snapshot/")]
            elif path.startswith("@inputs/"):
                expected = inputs[path.removeprefix("@inputs/")]
            elif path.startswith("@experiment/"):
                expected = originals[path.removeprefix("@experiment/")]
            elif path.startswith("@repository/"):
                expected = sha(REPO / path.removeprefix("@repository/"))
            else:
                raise AssertionError(f"Unresolved recorded path: {path}")
            assert row["sha256"].lower() == expected, path
        loads[sid] = len(rows)
        key = read(f"blind/{sid}/key.json")
        for label, item in key.items():
            assert sha(ROOT / f"blind/{sid}/{label}.md") == item["sha256"]
            assert sha(ROOT / item["run"]) == item["sha256"]
    print(json.dumps({
        "archived_artifacts": len(manifest["records"]),
        "reported_access_records_hash_checked": loads,
        "anonymous_finals": 6,
        "full_runtime_checked": args.runtime,
        "reconstructed_long_inputs_checked": args.inputs,
        "limits": "Hash identity and reported accesses are not an instrumented execution trace or writing-quality verdict.",
    }, indent=2))


if __name__ == "__main__":
    main()
