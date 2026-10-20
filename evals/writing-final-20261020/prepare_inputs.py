"""Build attributed, English evaluation inputs from the recorded OA downloads.

Usage: python prepare_inputs.py --cache PATH
The cache contains <source-id>/body.txt and publisher.html. See sources.json.
No private manuscript is an input. This does not score writing quality.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup
import fitz
import requests


ROOT = Path(__file__).resolve().parent


def write_frozen(path, text):
    data = text.encode("utf-8")
    if path.exists():
        if path.read_bytes() != data:
            raise ValueError(f"Reconstruction differs from frozen artifact: {path}")
    else:
        path.write_bytes(data)


SPEC = {
    "F-Q01": {
        "start": r"\nINTRODUCTION\n", "end": r"\nDISCUSSION\n",
        "author": "Rummer, Schweppe, and Schwede (2019)",
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "targets": ["These effects should be far less pronounced",
                    "Based on these considerations"],
    },
    "F-L01": {
        "start": r"\n1\u2002 Introduction\n", "end": r"\n8\u2002 \x07Discussion\n",
        "author": "Eren (2021)",
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "section": "Sec19-content",
    },
    "F-M01": {
        "start": r"\nIntroduction\n", "end": r"\nDiscussion\n",
        "author": "Rosen and Kelly (2023)",
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "targets": ["The STEM classroom laboratory traditionally",
                    "Course design choices for a remote asynchronous"],
    },
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", required=True, type=Path)
    parser.add_argument("--fetch", action="store_true",
                        help="Fetch missing public PDF and HTML files; never replace cached sources.")
    args = parser.parse_args()
    sources = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))["sources"]
    manifest = []
    for source in sources:
        sid = source["id"]
        spec = SPEC[sid]
        cache = args.cache / sid
        if args.fetch:
            cache.mkdir(parents=True, exist_ok=True)
            for name, url in [("source.pdf", source["urls"][0]),
                              ("publisher.html", source["publisher_record"])]:
                target = cache / name
                if not target.exists():
                    response = requests.get(url, timeout=60)
                    response.raise_for_status()
                    if name.endswith(".pdf"):
                        with fitz.open(stream=response.content, filetype="pdf") as pdf:
                            assert len(pdf) > 0, sid
                    else:
                        assert b"<html" in response.content.lower(), sid
                    target.write_bytes(response.content)
            body_file = cache / "body.txt"
            if not body_file.exists():
                with fitz.open(cache / "source.pdf") as pdf:
                    text = "\n\n".join(
                        f"## PDF page {i + 1}\n{p.get_text(sort=False)}"
                        for i, p in enumerate(pdf))
                body_file.write_text(text, encoding="utf-8", newline="\n")
        body = (cache / "body.txt").read_text(encoding="utf-8")
        start = re.search(spec["start"], body)
        end = re.search(spec["end"], body)
        assert start and end and end.start() > start.end(), sid
        soup = BeautifulSoup((cache / "publisher.html").read_bytes(), "html.parser")
        if "section" in spec:
            paragraphs = soup.find(id=spec["section"]).find_all("p", recursive=False)
            assert len(paragraphs) == 3, (sid, len(paragraphs))
        else:
            paragraphs = []
            for prefix in spec["targets"]:
                hits = [p for p in soup.find_all("p")
                        if p.get_text(" ", strip=True).startswith(prefix)]
                assert len(hits) == 1, (sid, prefix, len(hits))
                paragraphs.extend(hits)
        attribution = (
            f"# {source['title']}\n\n"
            f"Source: {spec['author']}. https://doi.org/{source['doi']}\n\n"
            f"Publisher: {source['publisher_record']}\n\n"
            f"Reuse: CC BY; licence link: {spec['license']} . "
            "Original author text, extracted and reformatted for a secondary-writing "
            "evaluation. Extraction can disturb line breaks and tables. "
            "Published sources cited by the article have not been independently read "
            "as part of this input pack.\n\n"
        )
        out = ROOT / "inputs" / sid
        out.mkdir(parents=True, exist_ok=True)
        files = {
            "new-evidence.md": attribution
            + "## Evidence available for new writing\n\n"
            + "Introduction, design and findings only; original abstract, discussion "
            "and conclusion withheld. PDF page markers retain source locations.\n\n"
            + body[start.start():end.start()].strip() + "\n",
            "revision-original.md": attribution
            + "## Original passage to revise\n\n"
            + "\n\n".join(p.get_text(" ", strip=True) for p in paragraphs) + "\n",
            "revision-context.md": attribution
            + "## Full article extraction for revision context\n\n" + body,
        }
        hashes = {}
        for name, content in files.items():
            path = out / name
            write_frozen(path, content)
            hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        manifest.append({
            "id": sid, "files_sha256": hashes,
            "pdf_sha256": hashlib.sha256((cache / "source.pdf").read_bytes()).hexdigest(),
            "html_sha256": hashlib.sha256((cache / "publisher.html").read_bytes()).hexdigest(),
            "new_evidence_character_count": end.start() - start.start(),
            "revision_original_words": sum(len(p.get_text(" ", strip=True).split())
                                           for p in paragraphs),
        })
    write_frozen(ROOT / "inputs-manifest.json", json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
