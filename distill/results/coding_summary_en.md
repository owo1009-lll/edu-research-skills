# How 15 English SSCI education papers write discussion, conclusion, implications and limitations

Corpus: EN01–EN15 (2024–2025; 9 quantitative, 4 qualitative, 2 mixed methods; 9 journals; see `distill/manifest_en.json`).
Coded per `distill/CODING_SCHEME.md`. Per-paper records with excerpts are in `distill/private/en/coding.jsonl` (local only).
Every sentence of the abstract and of the discussion, conclusion, implications and limitations sections was read and coded (1,114 sentence units in all, including subheading lines; 781 of them are body sentences). Results sections were read only where needed, mainly to check which null results the discussion leaves out. Sentence IDs in the `notes` of `coding.jsonl` (pNN.M) number the paragraphs of the coded sections only, starting with the abstract as p01, and M is the sentence within that paragraph.

## Definitions used for the counts

- **Discussion body**: all coded sections except the abstract and the limitations unit. EN05 and EN12 discuss their findings under headings called "implications", so those headings count as body. In EN08 and EN14 the limitations paragraph sits inside the Discussion, and it is counted as the limitations unit.
- **Finding statement**: a sentence that restates a result of the present study (statistical or thematic). Interpretations ("this means that ...") and recommendations are not counted.
  - *Direct*: no epistemic hedge on the finding ("we found", "X predicted Y", "participants described").
  - *Hedged*: the finding carries a hedge. These are split into (a) **reporting-verb hedges only** (suggest / appear / seem) and (b) **modal or adverb hedges** (may have, possibly, likely, partly, could, or a preliminary-evidence frame).
  - *Followed by disclaimer*: a disclaimer comes in the same or the next sentence (this flag overlaps with direct/hedged).
- **In-body disclaimer** (strict): a sentence in the body, outside the limitations unit, that limits what the data show or permit (generic forms: cannot show, does not establish, should be interpreted with caution, it is not possible to conclude).
  - **Design caveat** (looser): a body sentence that points to a design or scope feature as a possible artifact, without the "cannot" formula.
  - Substantive "does not mean" claims about the world (EN03, EN06) are not counted as either.
- **Explanation instance**: one proposed reason or one literature comparison, however many sentences it spans. Categories:
  - theory: a named or cited theory, or the authors' own mechanism reasoning (reported separately)
  - literature-consistent
  - literature-inconsistent
  - context
  - alternative: more than one competing explanation

  Hedge level per instance: none / one device / several devices.

## 1. Categorical fields across the 15 papers

**Opening move of the discussion**

| Code | Papers | % |
|---|---|---|
| restate_findings | 7 (EN02, 04, 06, 09, 11, 13, 14) | 47 |
| answer_rq (goes RQ/H by RQ/H) | 4 (EN03, 05, 10, 15) | 27 |
| context (returns to background first) | 3 (EN01, 07, 08) | 20 |
| other (restates approach, points to a results table) | 1 (EN12) | 7 |

First sentence: restates the aim or the RQs in 8 papers, gives background context in 3, gives an overview of the findings in 2, and states a finding in 2. In 12/15 papers the discussion opens with the study itself rather than with the field.

**Explanation moves** (instances; 157 in total)

| Move | Total | Papers using | Per-paper median (range) | Share hedged |
|---|---|---|---|---|
| theory, all | 42 | 15 | 2 (1–6) | 60% |
| … named or cited theory | 17 | 9 | 1 (0–5) | 41% |
| … authors' mechanism reasoning, no named theory | 25 | 13 | 1 (0–4) | 72% |
| literature_consistent | 82 | 14 | 6 (0–10) | 21% |
| literature_inconsistent | 11 | 8 | 1 (0–2) | 55% |
| context | 14 | 9 | 1 (0–3) | 93% |
| alternative | 8 | 6 | 0 (0–3) | 100% |
| all moves | 157 | 15 | 10 (2–20) | 44% |

Hedge level across all 157 instances: none 88, one device 51, several devices 18. Agreement with prior work is the dominant move, in 14/15 papers. EN01 has no literature comparison at all.

**Null or unexpected results**

| Handling (main mode per paper) | Papers |
|---|---|
| reported directly, then explained | 13 |
| mentioned briefly (presented as similarity between groups, not explained) | 1 (EN14) |
| treated only as a limitation | 0 |
| no null or contrary result (descriptive study) | 1 (EN04) |

Instances: 21 reported-then-explained, 2 mentioned briefly. Four papers leave at least one non-significant result from Results out of the Discussion (EN01, EN03, EN09, EN11). EN13 presents a non-significant validity correlation as support, citing its effect size. In 11 papers the unexpected result is flagged with an evaluative marker: surprisingly, unexpected, noteworthy, interestingly, contrary to, against the hypothesis, or a statement that a hypothesis was only partly supported.

**Contribution**

| Field | Count |
|---|---|
| Explicit contribution claim present | 15/15 |
| Type: theoretical / practical / methodological | 15 / 8 / 5 |
| Position: in the discussion body | 11 |
| Position: conclusion or closing sentence | 8 |
| Position: dedicated subsection (theoretical implications/contributions) | 3 (EN01, 05, 12) |
| Position: inside the limitations unit (its opening, or framed as a strength) | 3 (EN04, 08, 13) |
| Novelty claim (the first, or one of the first, to study X) | 5 (EN01, 03, 04, 08, 13) |

**Implications**

| Field | Count |
|---|---|
| Form: prose paragraphs | 11 |
| Form: numbered (First, Second ...) | 2 (EN02, EN05) |
| Form: no implications section, embedded in discussion | 2 (EN10, EN14) |
| Items per paper | median 6 (1–15) |
| Strongest modal used: must / should / need / can / seem | 5 / 6 / 1 / 2 / 1 |
| Papers using *should* or *must* at least once | 11 |
| Modal tokens across corpus | should 31, can 21, may 14, could 14, need 13, must 12, will 3, might 3, would/recommend/seem 1 each; 25 recommendation sentences use no modal (e.g. saying an action is crucial or important) |

**Limitations**

| Field | Count |
|---|---|
| Position: own section | 12 |
| Position: final paragraph (of discussion/conclusion) | 3 (EN02, 08, 14) |
| Position: scattered / absent | 0 / 0 |
| Placement: followed by conclusion, implications or a contribution claim | 11 |
| Placement: paper ends on limitations | 4 (EN01, 02, 05, 06) |
| Length of limitations unit (sentences) | median 12 (4–31) |
| Of which: limitation statements | median 6 (1–16) |
| Of which: future-research sentences | median 3 (0–20) |
| Of which: mitigation sentences (limitation answered) | median 1 (0–11); present in 9 papers |
| Content: generalisability / design / sample / measurement / other | 13 / 11 / 10 / 9 / 7 |
| Turned into future research inside the unit | 14 (EN10 puts its future-research calls elsewhere) |

**Voice**: balanced 10, assertive 5 (EN01, 02, 04, 05, 07), cautious 0.

## 2. Finding statements and disclaimers (per paper)

| Measure (per paper) | Median | Range | Corpus total |
|---|---|---|---|
| Finding statements in the body | 15 | 6–36 | 272 |
| … direct | 12 (86%) | 6–32 (54–100%) | 228 (84%) |
| … hedged | 2 (14%) | 0–8 (0–46%) | 44 (16%) |
| … followed by a disclaimer | 0 (0%) | 0–2 (0–33%) | 7 (2.6%), in 5 papers |
| In-body disclaimer sentences (strict) | 0 | 0–2 | 9 in 6 papers (1.2% of 781 body sentences) |
| In-body design caveats (looser) | 0 | 0–2 | 6 in 5 papers |
| Abstract finding statements hedged | — | — | 10 of 35 (29%) |

Most hedges on findings are reporting verbs: 33 of 44 use only suggest/appear/seem, and 11 use a modal or an adverb. If "suggest" is read as neutral, 96% of finding statements are direct. Two papers (EN02, EN08) hedge no finding at all. The most hedged papers are EN01 (46%, all reporting-verb hedges), EN12 (36%) and EN09 and EN15 (31% each). In EN15 the hedges sit on claims about individual interviewees in a nine-person study.

Per paper:

| ID | Design | Opening | Findings: total / direct / hedged / +disclaimer | In-body disclaimers | Design caveats | Explanations th / lc / li / cx / alt | Null handling | Limitations: position, sentences (statements) | → future | Implications form, strongest modal | Voice |
|---|---|---|---|---|---|---|---|---|---|---|---|
| EN01 | quant | context | 13 / 7 / 6 / 0 | 0 | 0 | 1/0/0/0/1 | reported then explained | own section, 13 (3) | yes | paragraphs, must | assertive |
| EN02 | qual | restate | 17 / 17 / 0 / 0 | 0 | 0 | 2/8/1/0/0 | reported then explained | final paragraph, 4 (1) | yes | numbered, should | assertive |
| EN03 | quant | RQ | 20 / 18 / 2 / 0 | 0 | 0 | 2/4/1/1/0 | reported then explained | own section, 13 (11) | yes | paragraphs, must | balanced |
| EN04 | mixed | restate | 14 / 12 / 2 / 0 | 0 | 0 | 1/7/0/0/0 | absent | own section, 10 (3) | yes | paragraphs, need | assertive |
| EN05 | quant | RQ | 7 / 6 / 1 / 0 | 0 | 0 | 2/4/0/1/0 | reported then explained | own section, 7 (4) | yes | numbered, should | assertive |
| EN06 | qual | restate | 32 / 27 / 5 / 0 | 0 | 0 | 1/8/2/1/1 | reported then explained | own section, 16 (10) | yes | paragraphs, must | balanced |
| EN07 | quant | context | 12 / 10 / 2 / 0 | 1 | 0 | 6/2/2/0/0 | reported then explained | own section, 16 (8) | yes | paragraphs, must | assertive |
| EN08 | quant | context | 6 / 6 / 0 / 2 | 2 | 0 | 2/7/1/2/3 | reported then explained | final paragraph, 10 (7) | yes | paragraphs, should | balanced |
| EN09 | quant | restate | 13 / 9 / 4 / 1 | 1 | 0 | 6/9/1/3/1 | reported then explained | own section, 31 (11) | yes | paragraphs, should | balanced |
| EN10 | qual | RQ | 34 / 32 / 2 / 1 | 1 | 1 | 1/10/0/2/1 | reported then explained | own section, 8 (6) | no | embedded, must | balanced |
| EN11 | mixed | restate | 36 / 32 / 4 / 0 | 0 | 0 | 3/6/2/0/0 | reported then explained | own section, 20 (16) | yes | paragraphs, should | balanced |
| EN12 | quant | other | 11 / 7 / 4 / 0 | 0 | 1 | 6/3/0/1/0 | reported then explained | own section, 12 (4) | yes | paragraphs, can | balanced |
| EN13 | quant | restate | 16 / 15 / 1 / 1 | 2 | 1 | 2/4/0/2/1 | reported then explained | own section, 27 (12) | yes | paragraphs, seem | balanced |
| EN14 | quant | restate | 15 / 12 / 3 / 2 | 2 | 2 | 2/3/0/1/0 | mentioned briefly | final paragraph, 5 (3) | yes | embedded, can | balanced |
| EN15 | qual | RQ | 26 / 18 / 8 / 0 | 0 | 1 | 5/7/1/0/0 | reported then explained | own section, 4 (3) | yes | paragraphs, should | balanced |

## 3. How uncertainty is expressed, and where it sits

| Location | What carries it | Frequency |
|---|---|---|
| **On findings** | Reporting verb (the findings suggest / appear to / seem to) | 33 hedges, 12 papers |
| | Modal or adverb (may have led, possibly moderated, likely, partly) | 11 hedges, 4 papers |
| | Provisional label on a whole result set (preliminary, initial, exploratory, tentative) | 4 papers in the body (EN01, 03, 12, 13); EN03's "initial and preliminary evidence" frames its headline claim in both the abstract and the conclusion |
| **On explanations** | may / might / could on the proposed cause | 52 of 75 non-literature explanations hedged (69%), against 16% of findings |
| | Formula that introduces a candidate reason (one possible explanation is ...; one reason ... might be; there are several potential reasons) | 6 papers (e.g. EN05 "One possible explanation is") |
| | Attribution formulas (*may be attributed to*, *may be due to*, *may be explained by*) | 4 papers (EN06, 08, 09, 10) |
| | First-person epistemic framing (we suspect / we assume / we propose / the authors suggest) | 3 papers (EN08, 10, 13) |
| | Rhetorical question before the explanation | 1 paper (EN09) |
| **On literature comparisons** | Mostly unhedged ("consistent with", "in line with", "echoes") | 65 of 82 unhedged |
| **In the body, about the design** | Strict disclaimer | 9 sentences, 6 papers. Targets: an explanation (3, e.g. EN08 "we cannot provide explanations for this result based on our data"); a causal or comparison inference (4, e.g. EN13 "causal inferences must be made with caution"); a measure's meaning (1); the scope of outcomes (1) |
| | Design caveat (scope or measure noted as a possible artifact) | 6 sentences, 5 papers |
| **In the limitations unit** | Design, sample, measure and generalisability statements | 102 limitation statements; about 87% of all caveat sentences (102 of 117) sit here. Causal-design caveats (correlational or cross-sectional design, reciprocal effects, self-selection) are named here, once each, in EN01, 08, 09 and 11. In the body, only EN13 states one |

Two patterns hold for every in-body disclaimer. First, each one is tied to a single, named inference; none is a general warning attached to a list of findings. Second, all 9 are followed at once by a substantive move: a hedged explanation or interpretation (5), an alternative reading (1), a decision about what to focus on (1), or a next step or data source (2). None ends a paragraph on the disclaimer.

## 4. Reusable sentence templates (paraphrased, with slots)

**Restating a finding**
1. [Predictor] was [positively/negatively] related to [outcome] ([statistic]); [group high on X] reported [more/less Y] than [comparison group], supporting H[n].
2. On RQ[n], [participants] most often described [theme], especially when [condition]; [less frequent theme] appeared only in [subset].

**Explaining with theory**
3. This pattern fits [theory]'s account of [mechanism]: because [premise from theory] ([citation]), [condition in this study] may have [effect on outcome].

**Relating to prior studies**
4. *Consistent*: This agrees with [Author, year], who found [result] among [population]; our data show the same pattern in [new context].
5. *Inconsistent*: Unlike [Author, year], who reported [opposite result], we found [result]. One possible reason is that [their sample/setting/measure] differed from ours in [feature], which would [effect on outcome].

**Handling a null or unexpected result**
6. Contrary to H[n], [X] was not related to [Y]. A plausible reason is [contextual or theoretical reason]; alternatively, [second reason], which [future design] could separate.
7. [X] did not show the expected [effect]. Because [measure] captures [trait] rather than [actual use/process], the null may reflect [this gap]; [process or log data] would test it directly.

**Stating a contribution**
8. This study adds to research on [topic] by showing that [core finding] in [context not studied before], and it offers [instrument/concept] for [use].

**Implications**
9. [Actor] should [action], because [finding]. In practice, this could mean [concrete example]. (When there are two or three items, number them: First ... Second ...)

**Limitations → future research**
10. Because [design feature], we cannot settle [one specific inference, e.g. direction of the effect]; a [longitudinal / experimental / multi-site] study could test whether [specific question].
11. Although [limitation], [mitigating fact or check], so [bounded claim] still holds; future work with [improvement] could [extend the claim].

## 5. Five regularities that separate these papers from disclaimer-first prose

1. **Findings are restated as plain declaratives.** In 13/15 papers at least two-thirds of finding statements are direct (median 86%, range 54–100%; 228 of 272 overall). When a finding is hedged, the hedge is usually just the reporting verb ("suggest", "appear"; 33 of 44 hedges), not a stack of modals.
2. **Disclaimers are rare, local and followed by something useful.** 9/15 papers contain no "cannot show / cannot establish / should not be interpreted as" sentence in the body, and 10/15 never attach one to a finding. Across the corpus there are 9 such sentences (1.2% of body sentences), and only 7 of 272 finding statements are followed by one. Each one targets a single inference, and all 9 lead straight into an explanation, an alternative or a next step.
3. **Uncertainty is placed on explanations, not on results.** In 15/15 papers a larger share of the authors' own explanations is hedged than of their finding statements (pooled: 69% vs 16%). The usual devices are may/might/could and a candidate-reason formula such as *one possible explanation is* (6 papers). Agreement with prior studies, the most common move (14 papers), is mostly stated without hedges (65 of 82).
4. **Limitations are kept in one place, bounded, and turned into future work.** 15/15 papers have a single limitations unit (12 own sections, 3 final paragraphs), with a median of 12 sentences and 6 limitation statements. Of these papers, 14 convert limitations into future-research designs and 9 answer at least one limitation with a mitigating fact. Only 4 end the paper on limitations; the other 11 close on a conclusion, implications or a contribution claim. Of the 5 papers that state a causal-design caveat, 4 do so once, in the limitations unit, rather than after each finding.
5. **Null and unexpected results are reported plainly and then explained.** 13/15 papers state at least one null or contrary result directly and then give reasons (21 instances). 11 papers flag it as interesting rather than as a problem (surprisingly, unexpected, noteworthy, only partly supported). No paper handles a null only as a limitation. One reopens a discussed null as a future-research question (EN01).

## 6. Where these papers are cautious, and where they over-reach

- **Cautious**:
  - EN08 hedges almost every explanation and twice says the data cannot explain a difference.
  - EN13 ends its Discussion with a correlational and reverse-causality caveat, and calls its practical implications tentative.
  - EN09 puts a two-sample caution clause inside a finding sentence.
  - EN14 has two body disclaimers about measures and comparison norms.
  - EN03 frames its headline claim as provisional evidence in both the abstract and the conclusion.
  - EN12 labels its subgroup effects as exploratory and restates practical implications with appear/seem.
  - Abstracts hedge more than discussions (29% of abstract finding statements), usually in the closing sentence, where the findings "suggest" something.
- **Over-reach**. These features should not be copied into the skill.
  - Causal verbs on survey or correlational data (EN01, EN09).
  - Unmeasured mechanisms narrated as observed (EN07, EN09).
  - One abstract that turns a null into a comparative claim (EN05).
  - Some Results nulls left out of the Discussion (4 papers).

  The skill should copy *where* these papers put caution, not the over-claiming. "Direct" here means unhedged, not causal.

## 7. Coding difficulties

- **Finding vs interpretation.** The boundary between a finding and an interpretation ("This indicates that ...") is a judgement call. Inferences beyond the data were coded as explanations or implications, not as findings.
- **"Suggest".** Treating "suggest" as a hedge raises the hedged count. With a stricter rule, 96% of findings would count as direct.
- **Which caveats count.** Strict disclaimers, looser design caveats and substantive "does not mean" claims were separated. The EN14 and EN10 cases were the hardest calls (see `notes` in `coding.jsonl`).
- **Explanation instances.** Boundaries were set by judgement. Parenthetical citations attached to a finding were counted as literature-consistent.
- **Section structure varies.**
  - Findings are discussed under "implications" headings in EN05 and EN12.
  - EN08 and EN14 have no limitations heading.
  - EN13 merges limitations and implications.
  - EN15 quotes participants inside the Discussion (quotes excluded).
  - EN12's results summary is a table excluded from the text.
- **Source quirks.** Sentences were split automatically and checked by hand (one merged sentence in EN06 was split during coding). EN05 contains an apparent typo that restates its null as "significant". EN15 is an accepted manuscript.
