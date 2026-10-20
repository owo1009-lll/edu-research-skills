"""Archive only the three named synthetic trials, with explicit path aliases.

This is a development evidence exporter, never a user-data backup or preference logger.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
NAMES = {"public-example-final": "example", "independent-preferences": "preferences",
         "independent-links": "linked-materials"}
TEXT = {".md", ".txt", ".json", ".jsonl", ".py", ".log", ".ps1", ".csv"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def archive(source_root):
    source_root = Path(source_root).resolve()
    records = []
    for name, destination in NAMES.items():
        source = source_root / name
        if not source.is_dir():
            raise ValueError(f"Missing synthetic trial: {name}")
        for path in sorted(source.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts or path.suffix in {".pyc", ".lock"}:
                continue
            relative = path.relative_to(source)
            target = ROOT / destination / relative
            if target.exists():
                raise ValueError("Archive destination already exists: " + str(target))
            raw = path.read_bytes()
            output = raw
            transformation = "byte-identical"
            if path.suffix in TEXT:
                text = raw.decode("utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig")
                aliases = [(str(source), "@RUN@"), (str(REPO), "@REPO@"), (str(source_root), "@EVAL@")]
                for old, new in aliases:
                    for form in (old, old.replace("\\", "/"), json.dumps(old, ensure_ascii=False)[1:-1],
                                 json.dumps(old, ensure_ascii=True)[1:-1]):
                        text = text.replace(form, new)
                output = text.encode("utf-8")
                if output != raw:
                    transformation = "UTF-8/path-alias normalization"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(output)
            records.append(dict(path=target.relative_to(ROOT).as_posix(), source_sha256=sha(raw),
                                archived_sha256=sha(output), transformation=transformation))
    manifest = dict(synthetic=True, records=records,
                    aliases={"@RUN@": "the containing example/preferences/linked-materials trial root",
                             "@REPO@": "the repository root", "@EVAL@": "the developer's external evaluation root"},
                    limits="Original binary files and prose preserved; paths normalized in text evidence. "
                           "Archived operations are historical, not automatically replayed.")
    (ROOT / "archive-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                                               encoding="utf-8")
    return {"files": len(records), "synthetic": True}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--synthetic-trial-root", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(archive(args.synthetic_trial_root)))
