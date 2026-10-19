# Run note

## Scope

Completed D-Q01/new-request.md using source-pack.md as the sole substantive source. The requested deliverable is two connected English discussion paragraphs of 230–280 words, plus a short separate explanation. final.md contains only the manuscript, including a heading identifying it as a secondary-writing demonstration. rationale.md is the separate note. No reference list, table or Word file was produced.

The writing instructions came exclusively from the frozen snapshot at @snapshot. The actual loaded snapshot-relative paths and SHA-256 hashes of both input files are in loads.json. No browser, original.md, other run, repository distillation notes, evaluation summary or current repository skill was accessed. No subagent was spawned. All writes were confined to this run directory.

## Actual workflow

1. Read the frozen skill, request and source pack with explicit UTF-8 decoding. Read the argument, English voice, quantitative discussion, framing-results and shared integrity resources. No optional example card or additional writing route was needed for this short discussion task.
2. Wrote rationale.md before drafting. Its original planning text is preserved as rationale-plan.md. The plan recorded the core argument and both supporting and restricting evidence.
3. Saved the complete first draft as draft-01.md. Read the two frozen checker scripts; the tool display of check_prose.py was truncated, so targeted searches inspected its imports, file reads and heading matcher. Neither checker loads external corpus files.
4. Made draft-01-prose-input.md with an explicitly recognisable “Discussion:” heading and identical body. Ran check_voice.py on draft-01.md with source-pack.md, and check_prose.py on the check-only copy, using `python -X utf8 -B`.
5. Initial PowerShell UTF-8 writes included a byte-order mark. This made the voice checker count the heading as a paragraph and prevented useful prose section recognition. Rewrote the two draft files as UTF-8 without a byte-order mark and repeated both checks. Both initial outputs and retry outputs are preserved as check-voice-draft-01*.txt and check-prose-draft-01*.txt. No checker error was concealed or represented as a successful prose assessment.
6. Saved local-self-review.md, including judgments on the prompts and a source-based semantic review. Made one substantive revision, producing final.md. A subsequent minor edit labelled the 0.069 coefficient as standardised and the interval as wild-cluster-bootstrap. Replaced the planning version of rationale.md with the concise delivery explanation.
7. Ran the local validate_delivery.py script and inspected final.md and loads.json. delivery-validation.json confirms two body paragraphs, 259 lexical words (261 whitespace-delimited tokens), matching bodies in the draft and check-only copy, an attribution heading and UTF-8 without a byte-order mark. The earlier length-check-initial.txt records the count before the minor coefficient/interval edit. The final script output is preserved in delivery-validation.json.

## Checks and limits

AI reading checked the direction, object, scale and analysis identity of the reported coefficient and interval against the supplied text. It also checked the within-country versus single-wave comparisons, the bounded belonging interaction, the absence of an equivalence or no-harm conclusion, and the grounding of the practical recommendation. The first-draft voice retry found no unsupported number strings and one semantic cue; the latter was assessed and its sentence replaced for clarity. The prose retry missed the accented author name in its citation matcher, so its two zero-citation prompts were treated as a tool limitation. Corpus medians were not treated as quality scores.

The final body was reread against the source pack. The two frozen style scripts were run on the first draft, not rerun on the final text. The local validation script performs format, identity, encoding and count checks only. A full-manuscript consistency run was not applicable to this single discussion passage. The original article, cited originals and supplementary D–I were not examined independently; no statistical reanalysis or external citation verification was performed. All review here is AI self-review, not expert review.
