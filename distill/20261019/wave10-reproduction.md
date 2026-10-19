# Reproduce the wave 10 source records

This batch uses public English papers only. [The manifest](public-wave10.json) records the source identities, public URLs and selection questions. [Acquisition](acquisition-public-wave10.json) records the original request outcomes, including the failed M-N18 PDF. [The reading ledger](reading-coverage.json) separately records later reading; downloading or extracting the text does not complete that work.

From a checkout of the repository, choose a **new cache directory outside the checkout** and run the existing acquisition tools. Replace `<cache>` and `<new-digest.json>` with paths you choose; do not overwrite the committed historical digest.

```powershell
python -X utf8 distill/20261018/fetch_sources.py --manifest distill/20261019/public-wave10.json --out <cache>
python -X utf8 distill/20261018/prepare_reading.py --manifest distill/20261019/public-wave10.json --cache <cache> --digest <new-digest.json>
```

The expected acquired files at the recorded access time are Q-N15, Q-N16, M-N17 and M-N19. Publisher access or file versions may subsequently change; preserve a changed outcome rather than rewriting the original record. Each acquired source folder contains `source.pdf`, `body.txt`, `reading.txt`, `crossref.json` and `acquisition.json`. Compare actual file SHA-256 values with the corresponding fields in the committed digest. Reading block B001 corresponds to PDF page 1 for these four sources.

[The asset record](acquisition-wave10-assets.json) gives every supplementary PDF URL, its hash and page count, plus the pages actually rendered and viewed. M-N17's five supplementary PDFs are S1–S4 File and S1 Table, publisher asset suffixes `.s002`–`.s006`. Download each URL with an ordinary HTTPS GET into `M-N17/supplements/<label>.pdf`; accept an actual PDF response, not an HTML page with a successful HTTP status. No login, private paper or developer-machine path is needed.

For the recorded text extraction and page previews, the operations were:

```python
from pathlib import Path
import fitz

pdf_path = Path("REPLACE_WITH_YOUR_PUBLIC_SOURCE_PDF")
document = fitz.open(pdf_path)
# For supplement text; the main reading.txt is produced by prepare_reading.py.
text = "\n\n".join(
    f"## PDF page {index + 1}\n" + page.get_text()
    for index, page in enumerate(document)
)
pdf_path.with_suffix(".txt").write_bytes(text.encode("utf-8"))

page_number = 2  # Substitute a page listed in acquisition-wave10-assets.json.
document[page_number - 1].get_pixmap(
    matrix=fitz.Matrix(1.5, 1.5)
).save(pdf_path.with_name(f"{pdf_path.stem}-p{page_number}.png"))
```

Preview filenames and hashes in the record refer to the original run. The engine version is recorded with the assets; a different PyMuPDF version may change rendered image bytes. Inspect the actual figures and tables even when hashes agree. Main pages viewed: Q-N16 5, 11, 12, 13; M-N17 3, 6, 7, 8, 9, 10, 12, 13, 14, 15. Supplement pages viewed: S1 File 2; S3 File 2; S4 File 2 and 4; S1 Table 1 and 2. The remaining supplement text and table cells were read from extraction. Six structure-tree warnings occurred during supplement rendering; the output pages were legible. S1 Fig and OSF datasets were not acquired or analyzed.

The public analyses are [Q-N16](papers/Q-N16.md) and [M-N17](papers/M-N17.md). They contain original sentence/paragraph/article analyses and newly authored English editing examples. Full source PDFs, text extracts and page images remain in the reader's external cache. The before/after examples are not experimental arms and do not establish improved model behavior.

Before publication, the actual checks recorded in [verification 14](record-verification-14.json) compared the original cached bytes with the acquisition and asset records, resolved local Markdown links, parsed the development JSON files, compared all old ledger entries with commit `4398fffa278d9f9baa4b5007827e22b05d8cd43b`, and compared the complete skill-file tree with that commit. No runtime skill changed, so no new PPT, statistics, journal-search or annotation behavior test was claimed for this batch.
