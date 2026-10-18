# Rationale and evidence record

## Scope and argument planned before drafting

New writing in English: Introduction, Discussion and Conclusion only, 600-750 words excluding references. This is an explicitly authorized secondary writing exercise about Kestin et al. (2025); the exercise does not claim original research or original authorship. Read only the supplied packet, request and task-relevant resources of the supplied skill snapshot. No network or raw-data analysis.

Teaching question -> Can an intentionally structured AI tutor improve immediate initial learning compared with an established active-learning class covering the same content? Evidence -> A peer-group randomized, two-week crossover in one introductory physics course favors the tutor package on immediate topic quizzes; an adjusted estimate supports the direction. Judgment -> Purpose-built tutoring merits consideration for initial learning even against a credible active comparator. Contribution -> The result gives a concrete instructional comparison and makes the implementation, learning task and comparison condition central to adoption decisions. Scope -> Two topics, one course and an instructional package; retention, complex transfer and a complete blended course remain untested.

## Evidence supporting and constraining the judgment

Supporting evidence: common content and learning objectives; experienced, highly rated instructors in an active comparator; randomized crossover; median post-test difference; positive adjusted AI coefficient; direction persists under peer-group clustering. Constraints: package changes location, pacing and peer interaction together; quizzes immediately follow lessons; no coefficient interval is supplied; condition-level score counts are not reconciled with eligible students; survey test labels/degrees of freedom need clarification; logged AI time and assumed class time are not equivalent measures; substantial development work and one setting limit implementation inference.

The manuscript will state both the learning advantage and its concrete scope. It will not substitute secondary satisfaction outcomes for the main learning result.

## Writing basis and cross-section plan

| Unit | Function and claim | Evidence/source location | Necessary conditions and location of qualification | Writing reason |
|---|---|---|---|---|
| Introduction, opening | Frame the teaching decision around structured tutoring for initial learning | H6-materials, Context and design; Interpretation and prior work | Identify structured implementation immediately | Avoid a general claim about all AI use or invented field-wide prevalence |
| Introduction, prior work | Explain why implementations deserve separate assessment | H6-materials, Interpretation and prior work, B024-B030 | Attribute Krupp/Forero descriptions to Kestin's review | Originals were not read; no independent literature claims |
| Introduction, study question | Ask about immediate topic learning against active instruction | H6-materials, Context and design, B003-B008/B025-B058 | State course, randomized peer groups, crossover, same objectives | Preserve randomized design without inventing a baseline test or hypothesis |
| Discussion, main result | Tutor package yielded higher immediate quiz performance | H6-materials, Findings, B011-B022/S1 | Medians stay medians; 0.63 stays a standardized regression coefficient | Report practical comparison without calling coefficient d or applying generic effect-size bands |
| Discussion, explanation | Feedback and pacing are candidate explanations | H6-materials, Context and design; Interpretation | Package attribution and competing features discussed here once | Evidence does not isolate tutor, pacing or recording components |
| Discussion, time and student experience | Time and perceptions add context, not a mechanism test | H6-materials, Findings | Distinguish measured/assumed time; single-item perceptions; null findings stated narrowly | No efficiency percentage, equivalence claim or validated growth-mindset claim |
| Discussion, practice and scope | Consider a carefully evaluated initial-learning use | H6-materials, Interpretation and prior work | Resources and untested course integration remain explicit | Tie action to tested package and identify development demands |
| Conclusion | Answer the teaching question and identify next decision | Same main-result and design evidence | Preserve course/topic/immediate scope; no new result | End with a specific instructional judgment |

## Terminology

| Concept | Preferred wording | Meaning/guardrail |
|---|---|---|
| Artificial intelligence | artificial intelligence (AI), then AI | Define at first substantive use |
| Intervention | structured AI tutor; tutor package when attributing effects | Includes expert solutions, prompts, sequencing, feedback, recorded introduction and home setting |
| Comparator | active-learning class / classroom condition | Experienced instructors, peer problem solving and assistance; not passive lecture |
| Learning outcome | immediate topic learning / immediate post-test score | Not long-term achievement, retention or complex transfer |
| Effect estimate | standardized AI coefficient | 0.63 is not presented as a standardized mean difference |
| Initial learning | initial engagement with new content | Does not describe a complete course or replace all in-person instruction |
| Confidence | confidence in learning difficult physics with effort | Single item; avoid calling this a validated growth-mindset scale |

## Source use and open author queries

The supplied packet is the sole factual source. It identifies a published article and paraphrases the main text, figures and supplement; the original article, original cited studies, figures and supplement were not independently opened. The reference reproduces the supplied metadata and is not labeled independently verified. Cite only Kestin et al. in the reference list; prior studies may appear only as secondary citations attributed to that review. No assertion that the source article was newly read or its data reanalyzed.

1. If preparing a full report, reconcile the condition-level post-test score counts (142 and 174) with the 194 eligible students and repeated/crossover observations. Do not represent these counts as independently randomized people. Bounded draft omits these counts.
2. Clarify Figure 3's dependent-test label against t(311) and crossover accounting before reproducing inferential survey statistics. The manuscript reports item directions and narrowly worded null findings without selecting or recomputing a test.
3. Obtain the coefficient interval before making a claim about precision; no interval is invented here.
4. The supplement's 0.63 extraction artifact is resolved by the supplied packet. Do not turn it into an unresolved publication error.
5. No target journal or external reference search is required. Markdown-only delivery is explicitly requested; no Word output.
6. This is a new writing task. The revision of its own first draft is documented in review.md; a separate change_log.md for revising a supplied author draft is not applicable.

## Checks planned

Run check_voice.py with H6-materials.md as source, check_prose.py, and check_consistency.py on first and final. Save stdout/stderr and exit codes under this task directory. Inspect every output and semantically review numeric identity, negative findings, package attribution, source scope and cross-section consistency. Automated flags are cues, not evidence of substantive correctness. Count section prose separately from headers, the exercise label and references; also check the count including the label.

## Model/runtime disclosure

The visible instructions identify this assistant as Codex, based on GPT-6. An exact deployed model identifier, reasoning effort, sampling configuration, token budget and service tier are unavailable. No inference about these settings is made.


## Completion audit

The final text follows the planned question, evidence and implication sequence. Introduction identifies the instructional comparison; Discussion states the immediate learning advantage, qualifies component attribution, distinguishes time measures, retains mixed experience outcomes, and links preparation demands to a course-level evaluation; Conclusion answers the same question within this course. The additional prompting/sequence finding comes from the supplied Context and design block and supports the implementation paragraph directly.

All requested Markdown files and the resource manifest were produced locally. First and final voice, prose and consistency checks ran with Python UTF-8 mode, with outputs inspected and dispositions recorded in review.md. Final word counts: 619 section-prose whitespace tokens (618 by the prose checker), 640 including the exercise label. References and headings are excluded.

The automatic command policy rejected one long shell write before execution. The same authorized local-file delivery was completed using the file-patch tool; no permission request or external action was needed. No other input source, run, repository report, installed skill, network source or subagent was used. No source files or skill files were edited.
