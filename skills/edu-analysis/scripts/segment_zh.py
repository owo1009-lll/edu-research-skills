"""Segment a Chinese text column with jieba before topic modelling (edu_topics in R).

Reads a CSV, replaces the text column (or writes --out-column) with space-separated tokens and
writes a UTF-8 CSV. Punctuation, whitespace and pure numbers are dropped; stop words are dropped
when a stop-word list is given (one word per line). Run it with the repository .venv Python:

    .venv/Scripts/python.exe segment_zh.py --input responses.csv --column answer \
        --output responses_seg.csv --userdict terms.txt --stopwords stopwords.txt
"""
import argparse
import csv
import re
import sys
from collections import Counter

import jieba

DROP = re.compile(r"^[\W_\d]+$", re.UNICODE)  # tokens made only of punctuation, symbols, digits


def read_rows(path):
    for enc in ("utf-8-sig", "gb18030"):
        try:
            with open(path, encoding=enc, newline="") as f:
                return list(csv.DictReader(f)), enc
        except UnicodeDecodeError:
            continue
    sys.exit(f"Cannot decode {path} as UTF-8 or GB18030")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True)
    ap.add_argument("--column", required=True, help="text column to segment")
    ap.add_argument("--output", help="output CSV (default: <input>_seg.csv)")
    ap.add_argument("--out-column", help="write tokens to this column instead of replacing --column")
    ap.add_argument("--userdict", help="jieba user dictionary: one term per line, optional frequency and POS")
    ap.add_argument("--stopwords", help="stop-word list, one word per line (UTF-8)")
    ap.add_argument("--min-length", type=int, default=1, help="drop tokens shorter than this (2 drops single characters)")
    a = ap.parse_args()

    jieba.setLogLevel(60)
    if a.userdict:
        jieba.load_userdict(a.userdict)
    stop = set()
    if a.stopwords:
        with open(a.stopwords, encoding="utf-8-sig") as f:
            stop = {w.strip() for w in f if w.strip()}

    rows, enc = read_rows(a.input)
    if not rows or a.column not in rows[0]:
        sys.exit(f"Column '{a.column}' not found in {a.input}")
    target = a.out_column or a.column
    vocab, n_tok, empty = Counter(), 0, 0
    for r in rows:
        toks = [t.strip().lower() for t in jieba.lcut(r[a.column] or "")]
        toks = [t for t in toks if t and not DROP.match(t) and t not in stop and len(t) >= a.min_length]
        r[target] = " ".join(toks)
        vocab.update(toks)
        n_tok += len(toks)
        empty += not toks

    out = a.output or re.sub(r"\.csv$", "", a.input, flags=re.I) + "_seg.csv"
    fields = list(rows[0].keys())
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} rows (read as {enc}); {n_tok} tokens; vocabulary {len(vocab)}; {empty} empty after cleaning -> {out}")


if __name__ == "__main__":
    main()
