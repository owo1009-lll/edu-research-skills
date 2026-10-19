# Q-C01 development comparison: useful local signals, no runtime adoption

The candidate remains outside the runtime skill. On this one English development study, all eight final passages preserve the main empirical or authorial claim. The blind new-writing reviewer slightly preferred both candidate outputs for their explanation-to-implication development. The compression reviewer gave one candidate a narrow accessibility preference, with a control close behind; this does not establish a consistent advantage across both repetitions. These are small editorial differences, not evidence that the control fails or that a broadly effective method has been established.

The exact intervention is [one positive comparison example](candidate-addition.md). The control is commit `cec4bc78fe9c240900e3c79a3097b1b96577d8fa`; the candidate changes only `skills/edu-writing/references/quantitative-discussion.md` in an external snapshot. All eight agents report loading that resource, and the reported hashes match the appropriate frozen variant. The classroom-practice article used in the example is different from this evaluation's longitudinal-model article. Both are development materials, not final independent holdouts.

## What was compared

| Operation and repetition | Control final | Candidate final | Body words: control / candidate |
|---|---|---|---:|
| New discussion, 1 | [v1](runs/D-Q02-new-r1-v1/final.md) | [v2](runs/D-Q02-new-r1-v2/final.md) | 478 / 500 |
| New discussion, 2 | [v1](runs/D-Q02-new-r2-v1/final.md) | [v2](runs/D-Q02-new-r2-v2/final.md) | 484 / 483 |
| Published-paragraph compression, 1 | [v1](runs/D-Q02-revise-r1-v1/final.md) | [v2](runs/D-Q02-revise-r1-v2/final.md) | 146 / 160 |
| Published-paragraph compression, 2 | [v1](runs/D-Q02-revise-r2-v1/final.md) | [v2](runs/D-Q02-revise-r2-v2/final.md) | 153 / 153 |

Counts here consistently use whitespace tokens and exclude attribution headings. Some writers and the new-writing reviewer split em dashes, yielding slightly different counts; every convention keeps the finals within the requested ranges. Length is a task constraint, not a writing-quality measure.

There is one study, two operations, two versions and two fresh repetitions per operation/version. Two independent agents reviewed the operations separately, seeing four anonymous manuscripts each. They did not see variants, developer notes, rationales or keys. The reviewers and writers use the same session-default model family; the exact hosted identifier, sampling settings and seed are unavailable. There was no human or cross-model review.

## Nine-dimension assessment

| Dimension | What the actual texts support |
|---|---|
| Facts and author intent | All preserve the undecomposed CLPM comparison, the RI-CLPM's within-person reference and the author's complementarity position. No final invents coefficients or an observed intervention benefit. Two candidate phrases need local attention, described below. |
| Problem and central judgment | The new passages explain reciprocal self-concept/achievement prediction and what comparison across models adds. The compressions retain the argument against automatic model ranking. |
| Reasoning and evidence | Every new output explains relative standing versus deviations from usual levels. The target comparison is already clear in the control, so that capability cannot be attributed solely to the added example. |
| Theory and literature | New passages use the proposed feedback process as interpretation and keep it unmeasured. Compressions retain Orth and Voelkle in their original roles; no cited original was independently read by these agents. |
| Explanation and contribution | The candidate new passages more smoothly connect the proposed process, classroom feedback and a trial agenda according to the reviewer. Control repetition 2 also offers a concrete feedback implication. |
| Natural, concrete prose | Control new repetition 1 repeats the joint-attention/trial point; candidate new repetition 2 has a dense mechanism-and-limits paragraph. Candidate compression repetition 2 gives the clearest construct-specific example, while the first candidate compression leaves that example more abstract. |
| Author voice | The revised paragraphs retain first-person complementarity and the final substantive recommendation. Assertive judgments and should-statements survive when supported; no preference rests on uniformly weakening language. |
| Qualification and repetition | Confounding, missingness, unmeasured process and untested intervention serve different functions. Some local repetition can be tightened; deleting distinct conditions to reduce caution would lose meaning. |
| Concrete author corrections | No unambiguous new factual error was found in the final manuscripts against the supplied material. Local attribution and interpretive-scope issues remain editorial work; source-check records are present despite blind reviewers not receiving them. |

These judgments concern the supplied, source-checked pack. They do not independently validate all statistical results or cited literature in the original article.

## Key comparisons and unresolved wording

Control new repetition 1 says that joint attention gives beliefs and performance a place in educational planning immediately after already recommending that attention. Candidate repetition 1 instead connects competence beliefs to students' interpretation of visible classroom grades, then develops the trial and process measurements. This is a concrete explanatory gain in the sample, not merely a more confident tone. The candidate's first repetition is also longer, so length allocation is a possible contributor. In repetition 2, the lengths are nearly identical, but the control already offers a substantive feedback implication.

The candidate's final sentence in new repetition 1 refers to “the sequence suggested by the observational findings.” Its previous paragraph correctly says that the intervening steps were unmeasured, so this is not a clear claim of observed mediation. Still, the ending should identify the authors' proposed process explicitly if used as a polished exemplar. A possible local replacement is “whether changes follow the authors' proposed feedback–belief–effort process.” The archived final is unchanged, preserving the actual outcome.

In compression repetition 2, the candidate explains that deviations in self-concept predict later deviations in achievement, and the reverse. The control describes deviations predicting later deviations more generally. The candidate's explicit pair helps readers see the comparison. However, it also combines the original's broad causal-inference criticism with its separate cross-level concern, saying cross-student associations are frequently interpreted as causal processes within students. That is a plausible reading, but it sharpens the author's proposition without documenting this specific shift in the change note. For strict preservation, restore the broader warning about causal interpretations unsupported by design or analysis, while leaving the following between/within distinction intact. This is a localized fidelity concern, not proof that the original source makes the narrower empirical frequency claim false.

Control compression repetition 1 has a different tradeoff: it turns the original criticism of actual research practice into a general inferential rule. It preserves the central argument but softens that rhetorical emphasis. Neither version should be called perfectly equivalent at every level of wording. The task's demand to preserve the author's argument requires attention to these choices, even when the central position survives.

## Correcting the blind reviewers' package-completeness finding

Both raw reviews say accompanying notes are missing, and the compression reviewer also notes absent adaptation attribution. The review packages intentionally contained manuscript bodies only; headings were removed uniformly, and process/change notes were withheld to protect blinding. Those observations therefore do **not** establish missing deliverables in the actual runs.

All four new-writing runs contain a separate note: three use `writing-note.md`, and candidate r2 uses [note.md](runs/D-Q02-new-r2-v2/note.md). Revision notes are [control r1](runs/D-Q02-revise-r1-v1/changes-and-source-checks.md), [candidate r1](runs/D-Q02-revise-r1-v2/changes.md), [control r2](runs/D-Q02-revise-r2-v1/changes.md), and [candidate r2](runs/D-Q02-revise-r2-v2/changes-and-source-checks.md); the original final files also retain attribution headings. The notes state their source limits. The candidate r2 note does not identify the particular causal-scope sharpening discussed above, so presence alone does not establish complete explanation of every interpretive change.

Preserve the [new-writing review](reviews/new/review.md), [compression review](reviews/revise/review.md) and their JSON records as received. Do not count their conditional completeness concern as eight writer failures, and do not rewrite the raw reviews to match this adjudication. Future review instructions should explicitly distinguish body-only assessment from delivery-package checks.

## Actual checks and negative records

- All eight agents saved real first drafts, self-review, final text and separate rationale. Both supplied checkers were executed in each run; their actual outputs and command records are archived. An exit code of zero is not a semantic quality verdict.
- Control compression repetition 1 initially fell below the requested minimum, then revised into range. Its failed PowerShell word-count command and successful Python fallback remain in the record.
- Self-review caught imprecise reciprocal phrasing and overly decisive future-trial wording in candidate new repetition 1. These earlier drafts remain visible; final evaluation does not erase them.
- Existing checkers sometimes classified attribution-headed discussion text as Introduction, missed a Unicode narrative citation or flagged source-supported qualifications. Writers assessed those prompts individually. A correctly sourced weak-confounding-test judgment or the distinct equivalence conditions was not deleted merely to clear a lexical flag.
- Record verification checks two 203-file snapshots, four frozen inputs, 84 reported resource entries, 20 reported input entries, the eight anonymous-final correspondences and 221 archived artifacts. Resource entries include generated helper scripts; they are not 84 independent skill resources. These are reported reading/execution records with verified hashes, not an independent execution trace.
- The archive helper initially rejected a valid BOM-prefixed JSON input. It was corrected to parse UTF-8 with an optional BOM and rerun successfully. Source bytes and original hashes were preserved.
- The staged whitespace check passes for authored files. Five whitespace warnings in three raw checker outputs and two raw review files are retained with their original bytes and hashes; the full archive is not described as whitespace-clean.

The public archive replaces only the external experiment-root path with `<EXPERIMENT_ROOT>` in affected process files and records original/published hashes. Final manuscripts and blind body wording remain unchanged. The helper scripts prepare variants, anonymous packages and the archive; they do not reproduce hosted model sampling or establish behavioral benefit. No PPT, statistics or journal-search runtime file changed, so their unrelated tests were not rerun here.

## Decision and next evidence needed

Q-C01 has a limited positive signal in new writing and one accessible compression, alongside a capable control and small fidelity tradeoffs. Retain it as a candidate for another English development study rather than load it into `edu-writing` now. The next comparison should require a materially different kind of comparison, preserve the author's proposition during compression, and use the same fixed intervention. This study cannot establish cross-design transfer or final-version performance. Qualitative and mixed-methods candidate comparisons and the final frozen-version independent review also remain unfinished.
