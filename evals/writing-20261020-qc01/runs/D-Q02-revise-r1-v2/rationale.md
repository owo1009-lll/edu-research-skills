# Revision rationale — preparation before drafting

This is an attributed adaptation of Marsh, Pekrun, and Lüdtke (2022), Discussion, “The Juxtaposition of Results Based On CLPMs and RI-CLPMs,” opening paragraph (B132), supplied in original.md. It is an editing exercise, not a new study. Only the assigned original and source pack supply manuscript evidence. The requested deliverable is one paragraph of 140–170 English words, with a separate short account of changes and unresolved checks.

## Original argument map

The original paragraph proceeds from a dispute over CLPMs and RI-CLPMs to the authors’ position that the perspectives are complementary. Each informs the longitudinal relationship between academic self-concept and achievement. The authors then question causal interpretations of comparisons across people and distinguish interindividual from intraindividual relationships. Their equivalence is plausible only under restricted conditions, illustrated by stationarity and homogeneity. The conclusion, attributed to Voelkle et al. (2014), advocates examining commonalities together with differences.

The conceptual contribution is the joint use of distinct substantive comparisons. “Complementary” does not mean statistical interaction, interchangeable estimands, or established causality. The paragraph is a methodological argument within a substantive discussion; adding the study’s reciprocal-effects results or intervention proposal would change its purpose.

## Planned unit-to-evidence map

| Unit | Function and retained position | Evidence location | Planned revision and reason |
|---|---|---|---|
| Opening | Preserve the disagreement about model preference, including Orth et al. (2021). | Original, first sentence. | Compress “antagonistic” and the claim of universal superiority into a readable account of the debate; an expression change (a), not a new literature review. |
| Complementarity | Retain the authors’ affirmative judgment and longitudinal self-concept–achievement focus. | Original, sentences 2–4; source pack, “Authors’ conceptual position and implications.” | Merge repeated statements while retaining their substance; expression/compression (a). |
| Comparison levels | Clarify why the models offer different perspectives. | Source pack, “Design, measures and comparisons,” CLPM and RI-CLPM bullets. | Briefly explain relative standing without decomposition versus departures from usual levels; clarification of technical shorthand (a). Do not describe CLPM as a pure stable-person process or RI-CLPM as an individual causal effect. |
| Causal interpretation | Preserve the concern about cross-sectional comparisons and causal readings. | Original, sentences 5–6. | Combine into one sentence; expression/compression (a). This is part of the authors’ argument, not a generic added disclaimer. |
| Equivalence conditions | Keep interindividual/intraindividual distinction and restrictive conditions. | Original, sentence 7. | Translate stationarity and homogeneity into stable parameters over time and similar relationships across people; accessibility (a). Keep them as examples, without adding a new theorem. |
| Closing judgment | Retain commonalities alongside differences and Voelkle et al. (2014). | Original, final sentence. | Preserve the authors’ recommendation and citation while shortening its wording; expression/compression (a). |

No category (b) change is planned: no analyses have been rerun. Category (c) matters are the unresolved source checks listed below.

## Terminology

| Preferred wording | Meaning in this revision |
|---|---|
| Academic self-concept | The original paragraph’s conceptual term; no ASC abbreviation is needed in this short passage. |
| CLPMs | Conventional cross-lagged panel models; relative-standing comparisons without decomposing stable person differences from within-person variation. |
| RI-CLPMs | Random-intercept CLPMs; lagged relationships among deviations from students’ usual levels. |
| Between-person / within-person relationships | Comparisons across people / variation within a person; their equivalence is conditional. |
| Complementary | Different substantive perspectives considered together. |

## Evidence supporting and qualifying the argument

Support: the original expressly endorses complementarity; the source pack clarifies the different comparison levels and reinforces the authors’ concern with interpretation. The supplied study context reports agreement in the directional pattern across model families, but this need not be inserted into a revision of the conceptual paragraph.

Qualification: agreement does not make the estimands identical; the observational models do not by their names establish causality. The original’s restrictive equivalence conditions and criticism of inappropriate causal interpretation are retained as integral parts of the argument.

## Source checks unresolved before drafting

Orth et al. (2021) and Voelkle et al. (2014) are citations retained from the published paragraph. Their original publications have not been read or independently checked for this exercise. The original’s broad characterization of educational and psychological research is also retained as the authors’ characterization, not independently established here. The source pack reports coefficient/table correspondence problems and unread supplemental code; the revised conceptual paragraph needs no coefficients or claims of rerun analyses.

## Scope of checking

This is a local revision. The assigned workflow nevertheless requires preserving a real first draft, running the two snapshot checkers, writing an AI self-review, and completing a revision. Whole-manuscript consistency checking, new literature searches, reference-list construction, and Word export do not apply. The requested output location takes precedence over the skill’s generic output location. Word-count verification will count the paragraph separately from its attribution heading.

## Revision completed and checked

Draft 2 implements the review decisions: it states the CLPM’s conditioning on earlier measurements; describes RI-CLPMs through successive departures; restores both designs and analyses in the causal-interpretation sentence; translates the equivalence conditions into plainer language; and removes the first occurrence of “over time.” The final paragraph preserves the two original citations, the authorial “we,” complementarity, and the closing recommendation. The word “should” remains because the original makes a supported methodological recommendation.

The actual second checker runs report 160 words and one paragraph. The dedicated word-count record independently reports 160 manuscript-body words and seven words in the attribution heading. The voice checker again flags the equivalence sentence; both qualifiers remain for the substantive reasons recorded in self-review.md. The prose checker reports no prompts but continues to classify the paragraph as an Introduction; its structural classification does not change the source’s Discussion identity. These are heuristic checks supplemented by the visible-scope review, not independent source verification.

Final.md is the delivery copy of draft-2.md after these checks. Changes.md gives the requested short separate account of edits, attribution, and unresolved sources. No reference list or Word document was produced, as requested.

## Execution record notes

The first read commands successfully accessed only the assigned files, but PowerShell serialized extended string metadata, producing excessive truncated output; the orchestration then failed to parse that output. The reads were immediately repeated using System.IO.File.ReadAllText, and the readable text and hashes informed the work. Both sets of commands are retained in executed-commands.json. A later attempted no-op patch against a standalone line in this file failed because that text was part of a longer paragraph; it changed no file. The first final-verification command failed its combined equality/citation/Unicode assertion because literal Unicode in the Python script was piped through PowerShell's legacy stdin encoding; the corrected command uses ASCII Unicode escapes and passes, without changing the manuscript. The failed command and traceback remain in executed-commands.json. Drafts and reviews were saved in their actual order, with no missing writing stage reconstructed.
