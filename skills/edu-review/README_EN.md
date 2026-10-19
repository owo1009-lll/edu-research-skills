# `edu-review` Skill

[中文说明](README.md)

Review the original manuscript with precisely anchored native highlights and comments, preserving its prose, existing comments and tracked changes.

## What To Use It For

- Find what reviewers will criticize before you submit
- Check a grant application from a panel reviewer's view

## Typical Requests

- "Review this manuscript as a reviewer would and tell me where it may be rejected"
- "Simulate two external reviewers for this application"

## What You Need To Provide

- The manuscript or application; the target journal or fund if known

## Outputs

- An annotated copy named `original-name_审稿标注版.docx` or `.pdf`: yellow for argument/expression suggestions, red for definite errors and blue for verification needs. Comments give grounds and next steps. No prose rewriting or separate review report by default.

## Runtime and Dependencies

- Python 3.9 or later; dependencies in `requirements.txt`. Uses edu-writing and edu-audit checks when relevant; actual Word opening/rendering requires Word or a compatible reader.

## Boundaries

- Simulated by AI, not expert review; no acceptance probabilities; no guessing at author identity
- Automated anchors cover plain body/table text in Word and text-layer PDFs. Existing fields, links and revisions are preserved; internal anchors, scanned PDFs and signed files have documented limits in [file handling](references/annotations.md). Explicitly requested revision follows the user's authorization.

## Related Skills

- edu-writing (revise from comments and author decisions), edu-response (answer real reviews), edu-audit (reporting review)

## Status

- Beta: native annotations tested with public synthetic manuscripts and deliberate file mutations. Earlier report-workflow usage does not establish human validation of this annotation workflow.
