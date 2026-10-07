# How English SSCI education articles write each section: moves, paragraphs and sentence habits (2026-10-07)

Purpose: break down how published English empirical articles write the Introduction, the literature review and hypotheses, the Results prose, the Discussion and the closing sections (implications, limitations, conclusion), so that edu-writing can learn to write like them and a checker can flag prose that departs from them. This file measures writing only: moves, paragraph construction, use of literature and sentence habits. It builds on, and does not repeat, `coding_summary_en.md` (stance and hedging, EN01–EN15) and `sections_summary.md` (structure and lengths, EN01–EN15). Its structure follows `writing_moves_zh.md` so the two can be compared. Papers are identified by ID only. Examples are fragments of eight words or fewer, or slot templates; no sentences are quoted. Per-paper records are in `private/writing_moves_en_coding.jsonl` (local, gitignored).

## 1. Method

**Corpus.** EN01–EN31 (`manifest_en.json`), all empirical, 2024–2026.

| Tier | Papers | Designs | Journals |
|---|---|---|---|
| earlier (E) | EN01–EN15 | 9 quantitative, 4 qualitative, 2 mixed | IJETHE, ETR&D, EIT, C&E, BJET, TATE, L&I, IJME, MER |
| top (T) | EN16–EN31 | 9 quantitative, 4 qualitative, 3 mixed | AERJ, JEP, CEP, L&I, C&E, Internet & HE, Educational Researcher, npj Science of Learning, Higher Education, Studies in HE, BJET, JLS, Psychology of Music |

"Earlier" is the label of the first acquisition batch, not of an earlier period: both tiers are 2024–2026. The tiers differ in journal standing and in topic, since 7 of the 15 earlier papers are about generative AI and the top tier was chosen to keep that topic rare.

**What was read and coded by hand**

- Every paragraph of the Introduction, the review or theoretical-background sections, the present-study sections, the Discussion and the closing sections of all 31 papers: 924 body paragraphs coded, plus 22 results paragraphs inside combined Results-and-Discussion sections, 99 one-line list items (RQs, hypotheses) and 47 skipped items (participant quotes, epigraphs, practitioner boxes).
  - By unit: Introduction 132 paragraphs, review 345, present study 43, Discussion 200 (in 120 discussion points), implications and contributions 82, limitations and future research 85, conclusion 37.
- The first sentence of every Results paragraph: 632 openings.
- For each paragraph the coders recorded its function (unit), its moves in order, the type of its first sentence and the type of its last sentence. For each paper they recorded section-level fields: Introduction opening, gap statements, aims, review organisation, synthesis and counter-evidence, hypotheses, discussion points, implications, limitations, conclusion and the last sentence of the paper.
- Paragraphs were coded by function, not by heading. For example, EN05's and EN12's "implications" sections that discuss findings were coded as Discussion, and EN16's "Conclusion" was coded paragraph by paragraph.
- **Unit boundary.** The Introduction is the text before the first review subheading or review section. Coders flagged five papers whose Introduction also carries the review (EN14, EN15, EN24, EN26, EN30). EN16, EN21 and EN23 have long Introductions before a separate review or context section.

**Who coded.** Seven coding agents followed one written scheme. Each coder received papers from both tiers, so coder differences do not line up with the tier comparison. Reliability:
- I re-coded the paragraph endings of a random 45 paragraphs blind: 82% agreement, Cohen's κ = 0.78. Agreement on the "generic closing sentence" code was 45/45.
- I independently read EN19's Discussion and closing sections: 9 of 10 paragraph endings matched.
- Disagreements were near-misses between neighbouring codes (FIND/SPEC, AIM/TRANS).
- Every paper was coded once. The rare-code counts (generic closings) are therefore conservative, coder-dependent estimates.

**Automatic measures** (scripts kept in the session scratchpad, not in the repository):
- **Paragraphs and sentences.** Paragraph = one line of the extracted text. Sentence split on terminal punctuation, protecting et al., e.g., i.e., initials and decimals.
- **Citations.** A citation instance is one author–year parenthesis, or one narrative citation (Name (year), Name et al. (year), Name's (year)). "Works" counts the years inside each parenthesis. A bundle is a parenthesis with three or more works. Narrative share = narrative instances / all instances.
  - EN24 used numbered citations that were removed in extraction, so it is excluded from every citation measure.
- **Tense.** Coded from the verb right after a narrative citation, and from the first finite verb of each cited sentence (both approximate).
- **Passive.** A sentence counts as passive if it contains a form of *be* followed by a participle (approximate; *is related to*, *is based on* count).
- **First person.** *we/our/us* per 1,000 words, after removing quoted participant speech of four or more words.
- **Stock phrases.** Rates per 10,000 words of main prose, from a fixed list of 55 patterns, plus a separate signposting list. **Abbreviations**: tokens with two or more capitals, e.g. SDT, GenAI (ChatGPT excluded).
- **Signposting.** e.g. *in this section*, *the remainder of this paper*, *as noted above*.
- **Results.** Numbers per sentence; statistic expressions (β, r, t, F, p, M, SD, d, CI …) inside vs outside parentheses.
- **"Main prose"** = Introduction + review + present study + Discussion + implications + limitations + conclusion. This is a median of 4,067 words per paper (2,441–7,189).

**Reporting.** Every aggregate is given pooled (n = 31), then E (n = 15) and T (n = 16), as median (range) of per-paper values unless stated. Counts are numbers of papers. Percentages over paragraphs or points are pooled across papers.

**Caveats**
- 31 papers. Education technology, teacher education, educational psychology and music education dominate, and there are only 8 qualitative and 5 mixed-methods papers.
- Tables, captions and footnotes were removed in extraction, so statistics that appear only in tables are invisible.
- EN15 and EN31 are accepted manuscripts.
- The 2024–2026 corpus probably contains AI-polished prose: several AI-typical words are already common (§2.6). Thresholds calibrated on it are therefore lenient toward such words.

## 2. Findings by section

### 2.1 Introduction (31 papers; 132 paragraphs)

| Measure | Pooled | E | T |
|---|---|---|---|
| Words (before first review subheading) | 529 (180–1,430) | 529 (180–1,430) | 518 (181–1,265) |
| Paragraphs (≥25 words) | 4 (1–9) | 3 (1–9) | 4 (1–9) |
| Paragraph length, words | 144 (81–304) | 155 | 139 |
| Citation instances / 1,000 words | 23.4 (11.3–36.5) | 25.1 | 22.1 |
| Works cited / 1,000 words | 39.2 (15.5–69.5) | 44.7 | 36.2 |
| % sentences with a citation | 56.7 (32–90) | 60.0 | 51.1 |
| % narrative (author-prominent) citations | 0 (0–31) | 0 | 0 |
| % parentheses with ≥3 works | 15.5 (0–62.5) | 16.7 | 13.6 |

**How the Introduction opens** (first sentence)

| Type | Pooled | E | T |
|---|---|---|---|
| Trend, technology or development ("[X] is increasingly used") | 11 | 6 | 5 |
| Practical problem or puzzle | 5 | 2 | 3 |
| What research has established | 4 | 2 | 2 |
| Definition | 4 | 2 | 2 |
| Broad importance claim | 4 | 2 | 2 |
| Policy / quotation / aim | 1 / 1 / 1 | 0 / 1 / 0 | 1 / 0 / 1 |
| Statistic | 0 | 0 | 0 |
| First sentence carries a citation | 23 | 11 | 12 |

The first move is background (trend, context) in 20/31 papers. Other first moves are importance in 4, definition in 3, prior evidence in 3, and a contribution statement in 1 (EN25).

**Move sequence.** Coded moves were BG (background), IMP (importance), DEF (definition), EVID (prior evidence), GAP, THEORY, AIM, DESIGN (preview of design), CONTRIB (contribution) and ROADMAP. Every Introduction can be read as a pruned or repeated version of BG → IMP → EVID → GAP → AIM (→ DESIGN → CONTRIB).

Papers using each move:

| Move | Papers |
|---|---|
| GAP | 29 |
| BG | 28 |
| IMP | 28 |
| AIM | 27 |
| EVID | 26 |
| DESIGN | 18 |
| DEF | 16 |
| CONTRIB | 13 |
| THEORY | 12 |
| COUNTER | 6 |
| ROADMAP | 4 |

The Introduction's last move is AIM in 10 papers, CONTRIB in 7, ROADMAP in 4 and EVID in 4. Three of the four EVID endings (EN06, EN11, EN28) are short Introductions that hand over to a review and a present-study section where the aims are stated.

**Gap.**
- **How many.** Papers make a median of 5 gap statements (2–8; E 4, T 5). Every paper states a gap in the Introduction (31/31). 18 restate it at the end of the review, and 10 again in the present-study section.
- **Types** (papers using each):

  | Gap type | Pooled | E | T |
  |---|---|---|---|
  | Absence ("little is known about [X]", "few studies have [examined X]") | 28 | 14 | 14 |
  | Focus–neglect contrast ("research has primarily focused on [A]") | 18 | 6 | 12 |
  | Practical problem rather than a research gap | 14 | 6 | 8 |
  | Population or context not studied | 13 | 7 | 6 |
  | Weak methods of prior studies ("[studies] typically relied on [self-report]") | 13 | 6 | 7 |
  | Mixed findings | 6 | 3 | 3 |
  | Unclear mechanism ("the underlying mechanisms remain unclear") | 6 | 3 | 3 |
  | Generalisability | 3 | 1 | 2 |

  Most papers combine an absence statement with one specific contrast or design weakness, rather than resting on "few studies" alone.
- **Gap words.** Gap words ("little is known", "few studies", "limited research", "remains unclear", "underexplored", "scarce") appear in 24/31 papers, at a median of 3.6 per 10,000 words of main prose (p90 9.4, max 15.5).

**Aims and the "present study"**

| Measure | Pooled | E | T |
|---|---|---|---|
| Aims or RQs first stated at the end of the Introduction | 18 | 8 | 10 |
| … in a separate "present / current study" section | 10 | 5 | 5 |
| … mid-Introduction / end of review | 2 / 1 | 1 / 1 | 1 / 0 |
| Has a "present / current study" section or subsection | 16 | 8 | 8 |
| Numbered research questions | 15 | 6 | 9 |
| RQs plus hypotheses | 10 | 6 | 4 |
| Aims plus hypotheses | 3 | 2 | 1 |
| RQs in prose / hypotheses only / aims only | 1 / 1 / 1 | 1 / 0 / 0 | 0 / 1 / 1 |
| Number of RQs | median 2 (0–4) | 2 | 2 |
| Aim stated in the first person ("In this study, we …") | 19 | 7 | 12 |
| Design previewed in the Introduction | 24 | 10 | 14 |
| Theory named in the Introduction | 23 | 9 | 14 |
| Explicit contribution claim in the Introduction or present-study section | 19 | 6 | 13 |
| Novelty claim (first study, to our knowledge) | 7 | 1 | 6 |
| Roadmap of the article | 4 | 0 | 4 |

**Paragraph construction (132 paragraphs)**

- **First sentence:**

  | Type | Pooled | E | T |
  |---|---|---|---|
  | Cited claim | 28% | 28% | 28% |
  | Aim | 17% | 15% | 18% |
  | Writer's own uncited claim | 14% | 17% | 13% |
  | Research or studies as the subject | 13% | 13% | 13% |
  | Gap | 12% | 13% | 11% |
  | Definition | 5% | 5% | 6% |
  | Named author as the subject | 1 paragraph of 132 | — | — |

- **Last sentence:**

  | Type | Pooled | E | T |
  |---|---|---|---|
  | Evidence (cited claim or a study result) | 35% | 40% | 31% |
  | Aim | 23% | 23% | 22% |
  | Gap | 18% | 23% | 14% |
  | Specific inference | 10% | 7% | 13% |
  | Transition | 6% | 3% | 8% |
  | Contribution | 5% | 3% | 7% |
  | Generic value sentence | 1.5% (2 paragraphs) | 0 | 2 paragraphs |

- English Introductions almost never end a paragraph on an evaluative flourish (2 of 132 paragraphs). They stop on the evidence, the gap or the aim.

### 2.2 Literature review, theoretical background and hypotheses (31 papers; 345 review and 43 present-study paragraphs)

| Measure | Pooled | E | T |
|---|---|---|---|
| Review words (LIT units) | 1,601 (332–3,641) | 1,383 | 2,016 |
| Review paragraphs | 11 (2–25) | 9 | 15 |
| Subsections | 3 (0–16) | 3 | 4 |
| Organisation | thematic 10, by construct 6, by hypothesis 5, framework first then evidence 5, single block 5 | 4 / 4 / 3 / 2 / 2 | 6 / 2 / 2 / 3 / 3 |
| Names at least one theory or framework | 28 | 14 | 14 |
| Gap restated at the end of the review | 20 | 8 | 12 |
| Citation instances / 1,000 words | 25.5 (15.2–41.7) | 25.5 | 24.5 |
| Works / 1,000 words | 38.4 (20.1–78.9) | 44.6 | 34.6 |
| % sentences with a citation | 59.9 (37–100) | 63.7 | 53.5 |
| % narrative citations | 11.8 (0–61.5) | 11.8 | 12.1 |
| % parentheses with ≥3 works | 10.3 (0–40) | 17.9 | 8.1 |
| % parentheses with ≥2 works | 35.6 (13–70) | 45.2 | 29.4 |
| Present-study section: words / citations per 1,000 / we per 1,000 | 255 / 4.8 / 9.7 | 178 / 0 / 0 | 340 / 6.5 / 13.1 |

**Synthesis vs listing.**
- Coders counted synthesis sentences (claims across two or more studies, or about the state of the field) and single-study sentences (the design or result of one study).
- Per paper there are a median of 17 synthesis and 9 single-study sentences. Synthesis is 61% of the two (p90 82%; E 63%, T 59%).
- A "listing run" is three or more consecutive single-study sentences. These occur at least once in 22/31 reviews (E 10, T 12), and twice or more in 10/31.
- Single-study sentences are used, but in short bursts that illustrate a synthesis claim. Reviews rarely proceed study by study.

**Citation form and verbs.**
- **Information-prominent citations dominate.** The claim comes first and the citation sits at the end of the clause; narrative citations are a median of 12% of review citations and about 0% of Introduction citations.
- **Narrative citations cluster** in a few papers: EN23 62%, EN02 48%, EN25 40%, EN13 37%, EN19 31%, EN31 30%.
- **The verb after a narrative citation:** *found* is by far the most common (37 of about 120 identified verbs), followed by *showed*, *highlighted*, *argued*, *demonstrated*, *proposed* and *reported*.
  - Tense of the identified verbs: past 67%, present 26%, present perfect 7% (E 73% past, T 61%).
- **Cited sentences overall** use the present tense, present perfect included. The first finite verb is past in only 9–10% of review sentences that carry a parenthetical citation, against about 50% of sentences built on a narrative citation.

So established claims go in the present with a parenthetical citation, and specific studies go in the past with the author named.

**Counter-evidence.**
- 23/31 reviews present at least one contrary or mixed finding (median 2, 0–9). This holds in E 14/15 but only T 9/16, and the top-tier papers without counter-evidence are mostly qualitative (EN25, EN26, EN29, EN30) or descriptive (EN23, EN28).
- Devices:
  1. Adversative turn to a named study or finding: "However / In contrast, [Author] (year) reported …" (about 18 papers).
  2. Pair contrasting studies: "while [A] found X, [B] found Y", "some studies … others …" (9 papers).
  3. Label the state of evidence, then give both sides: "findings on [X] are mixed / inconsistent / conflicting" (8 papers).
  4. Concession that limits a consensus: "although evidence suggests [A], [B]", "even so", "nevertheless" (8 papers).

  Device counts come from the coders' slot templates and overlap.

**Paragraph construction (388 review and present-study paragraphs)**

- **First sentence:**

  | Type | Pooled | E | T |
  |---|---|---|---|
  | Cited claim | 21% | 29% | 16% |
  | Writer's own uncited claim | 17% | 11% | 22% |
  | Definition | 16.5% | 18% | 16% |
  | Research as the subject | 12% | — | — |
  | Theory as the subject | 8% | — | — |
  | Aim | 7.5% | — | — |
  | Gap | 6% | — | — |
  | Named author as the subject | 5% | — | — |
  | Metadiscourse ("This section reviews …") | 2.6% | — | — |

- **Last sentence:**

  | Type | Pooled | E | T |
  |---|---|---|---|
  | Evidence | 41% | 45.5% | 38% |
  | Specific inference | 18% | 14% | 21% |
  | Aim | 11% | — | — |
  | Hypothesis | 11% | — | — |
  | Gap | 9% | — | — |
  | Transition | 6% | — | — |
  | Generic value sentence | 2.1% (8 paragraphs in 7 papers) | — | — |

**Hypotheses** (16/31 papers, all quantitative except EN11 (mixed); E 9, T 7). Three quantitative papers (EN07, EN20, EN31) use RQs only.

| Measure | Pooled (n = 16) | E (9) | T (7) |
|---|---|---|---|
| Hypotheses per paper | median 3.5 (1–17) | — | — |
| Labels: H1/H1a / "Hypothesis 1" / prose | 6 / 3 / 7 | 3 / 2 / 4 | 3 / 1 / 3 |
| Placement: end of each review subsection | 5 | 3 | 2 |
| Placement: present-study section (prose 6, list 2) | 8 | 4 | 4 |
| Placement: mixed / Introduction | 2 / 1 | 1 / 1 | 1 / 0 |
| Also has RQs | 12 | — | — |
| Directional | 14 | 9 | 5 |
| Preregistered | 1 (EN19) | 0 | 1 |

Derivation of the 87 hypotheses (what the text right before each one does):

| Derivation | Pooled | E | T |
|---|---|---|---|
| Theory and empirical evidence | 55 (63%) | 22/38 | 33/49 |
| Theory only | 22 (25%) | — | — |
| Evidence only | 7 (8%) | — | — |
| None | 3 (3%) | — | — |

Lead-ins are formulaic and short: "Based on [this], we hypothesize that", "Consistent with [framework], we expected", "the following hypotheses are proposed:".

### 2.3 Results prose (brief; 632 paragraph openings, automatic measures on all Results text)

| Measure | Pooled | E | T |
|---|---|---|---|
| Results words | 1,398 (597–5,948) | 1,401 | 1,230 |
| Sentence length, median words | 22 (15–30) | 22 | 21.5 |
| % sentences with a number (quantitative and mixed papers, n = 23) | 55 (11–81) | 59 | 50 |
| Numbers per number-bearing sentence, median | 2 (1–5) | 2 | 2 |
| % statistic expressions inside parentheses (19 papers with ≥10 statistics) | median 100 (0–100) | 100 | 100 |
| Citation instances / 1,000 words | 1.3 (0–16.8) | 1.2 | 1.5 |

- **Paragraph openings, quantitative papers (197 openings):**

  | Opening | Pooled | E | T |
  |---|---|---|---|
  | Aim or procedure ("To test H1, we …") | 30% | 29% | 31% |
  | Finding stated in words first | 27% | 27% | 27% |
  | Table or figure pointer | 17% | — | — |
  | Checks: model fit, assumptions, descriptives | 14% | — | — |
  | Opens with a number or statistic | 4% | — | — |

- **Paragraph openings, qualitative papers (304 openings):**

  | Opening | Pooled | E | T |
  |---|---|---|---|
  | Theme claim | 59% | 61% | 57% |
  | Participant quote | 21% | 25% | 16% |

  Mixed-methods papers sit between the two: theme 54%, quote 15%, finding 12%, procedure 10%.
- **Where the statistics go.** Statistics follow the verbal claim. Most papers put them in parentheses. Four papers (EN12, EN14, EN17, EN18) mostly set them off with commas, which APA also allows.

### 2.4 Discussion (30 papers with a discussion; 200 paragraphs; 120 points)

| Measure | Pooled | E | T |
|---|---|---|---|
| Words | 905 (451–2,185) | 858 | 1,077 |
| Paragraphs | 6 (3–19) | 5 | 7 |
| Paragraph length, words | 152 (96–240) | 146 | 152 |
| Points per paper | 4 (2–8) | 4 (2–8) | 4 (2–8) |
| Citation instances / 1,000 words | 13.5 (3.8–25.9) | 13.7 | 12.1 |
| % sentences with a citation | 30.4 (10–54.5) | 30.4 | 29.6 |
| % narrative citations | 9.5 (0–64) | 20 | 5.3 |
| Citations per point (EN24 excluded) | median 3 (IQR 1–5); 12/112 points have none | 2 | 3 |
| % sentences with a number | 3.9 (0–31) | 2.4 | 4.0 |

**Opening.**
- The opening move is: restating the aim (13 papers); aim plus a summary of the findings (9); straight into the first point (5); a summary of all findings (3).
- 14/31 papers give a separate opening summary paragraph. Almost all open with the present study rather than with the field, as `coding_summary_en.md` found for the earlier tier (12/15).

**Subheadings.**
- None: 15 papers (E 5, T 10).
- Topic labels such as "Effects of [X] on [Y]": 13 papers (E 8, T 5).
- Claim headings: 1 (EN09). RQ as heading: 1 (EN15). Hypothesis labels: 1 (EN22).

**Inside a point (120 points)**

| Feature | Pooled | E (59) | T (61) |
|---|---|---|---|
| Opens by restating the finding | 98% | 98% | 98% |
| … restated in words only / with a statistic | 88% / 10% | 92% / 7% | 85% / 13% |
| Restated finding carries a modal or adverb hedge | 2.5% | 3% | 2% |
| Compared with cited prior work | 76% | 78% | 74% |
| … consistent only / both / inconsistent only | 50% / 20% / 6% | 59% / 15% / 3% | 41% / 25% / 8% |
| Explained (any explanation) | 75% | 58% | 92% |
| … mechanism reasoning / named theory / method or measurement / context | 37.5% / 14% / 12.5% / 11% | 29 / 5 / 10 / 14% | 46 / 23 / 15 / 8% |
| Names a theory or framework anywhere in the point | 29% | 17% | 41% |
| Restate + compare + explain all present | 52.5% | 41% | 64% |
| Explanation hedged (of explained points) | 69% | 74% | 66% |
| Point concerns a null, contrary or unexpected result | 35% | 29% | 41% |
| … stated, then explained / mentioned briefly | 67% / 33% | 11 of 17 / 6 of 17 | 17 of 25 / 8 of 25 |
| Implication given inside the point | 20% | 19% | 21% |

- **How points end:**

  | Ending | Pooled | E | T |
  |---|---|---|---|
  | Specific interpretation | 36% | 36% | 36% |
  | The finding or a hypothesis verdict | 19% | 17% | 21% |
  | Evidence | 15% | 17% | 13% |
  | Specific future direction | 12% | 12% | 12% |
  | Implication | 7.5% | 3% | 11.5% |
  | Contribution claim | 2.5% | — | — |
  | Generic value sentence | 4% | 5% | 3% |

- **Paragraph construction (200 paragraphs).**
  - First sentences restate a finding in 56.5% of paragraphs, make the writer's own claim in 16% and restate the aim in 11.5%.
  - Last sentences: specific inference 28.5%, finding 27%, evidence 12%, future direction 9%, transition 6%, implication 6%, aim 4%, generic value sentence 3% (6 paragraphs in 3 papers; EN19 alone has 3).
- **The tier difference** is in explanation, not in comparison. Both tiers compare about three-quarters of points with prior work. Top-tier points add an explanation far more often: points with no explanation are E 42% vs T 8%, and points naming a theory are E 17% vs T 41%.
  - This holds within coders: every coder had papers from both tiers, and each coded more unexplained points in the earlier papers.
- **Hedging.** The stance coding of EN01–EN15 found the same location of hedging: findings 16% hedged against explanations 69% hedged (`coding_summary_en.md`). The new point-level coding replicates it in the top tier: findings 2% hedged against explanations 66% hedged.
- **Null and contrary results** are introduced with a flag phrase ("Contrary to [H2]", "unexpectedly", "did not find the expected"). The writers then give measurement or design reasons (method-based explanations appear in 12.5% of all points) and usually a concrete test for future work.

### 2.5 Implications, limitations and conclusion

| Measure | Pooled | E | T |
|---|---|---|---|
| Implications present | 31 | 15 | 16 |
| … own section / mixed / in conclusion / in discussion | 15 / 7 / 5 / 4 | 7 / 4 / 2 / 2 | 8 / 3 / 3 / 2 |
| Implication items | median 5 (1–11) | 5 | 5 |
| Numbered items / subheaded items | 3 / 6 | 2 / 3 | 1 / 3 |
| Item anchored to a finding: explicit / implicit / generic (158 items) | 39% / 42% / 19% | 35 / 42 / 23% | 43 / 42 / 15% |
| Strongest directive: should / must / can / need to / other | 13 / 6 / 3 / 2 / 7 | 6 / 5 / 2 / 1 / 1 | 7 / 1 / 1 / 1 / 6 |
| Separate theoretical-contribution section | 6 | 3 | 3 |
| Implication words (IMPL + CONTRIB units) | 328 (136–1,190) | 314 | 404 |
| Implication paragraphs ending on a concrete action / contribution / specific claim / generic value | 55% / 12% / 10% / 7% | — | — |
| Limitations present | 31 | 15 | 16 |
| … own section / end of conclusion / final paragraph of discussion / scattered | 22 / 4 / 4 / 1 | 12 / 1 / 2 / 0 | 10 / 3 / 2 / 1 |
| Distinct limitations | median 4 (1–8) | 4 | 4 |
| Limitations paired with a future-research direction | 78 of 136 (57%); none paired in 6 papers | 62% | 53% |
| Papers answering at least one limitation with a mitigating fact | 25 | 10 | 15 |
| Limitations words | 310 (75–1,032) | 297 | 405 |
| Limitations paragraphs ending on future direction / limitation / mitigation / generic | 60% / 19% / 11% / 3.5% | — | — |
| Conclusion present | 24 | 11 | 13 |
| Conclusion words | 148 (28–801) | 208 | 135 |
| Conclusion moves (papers): summary / implication / contribution / future / closing message | 20 / 17 / 13 / 11 / 11 | — | — |
| Conclusion final sentence: future / generic / implication / contribution / other | 7 / 7 / 6 / 2 / 2 | 3 / 3 / 3 / 1 / 1 | 4 / 4 / 3 / 1 / 1 |
| Last sentence of the paper: future / implication / generic / contribution / limitation / other | 10 / 8 / 7 / 2 / 2 / 2 | 5 / 4 / 3 / 1 / 1 / 1 | 5 / 4 / 4 / 1 / 1 / 1 |

**Actors.** Implications most often address teachers (14 papers) and "educators" (9), then researchers, policy makers, school leaders, teacher education and institutions (2–4 papers each).

**Limitations sections.**
- They open with a formula of the type "This study has several limitations" or "Despite [its strengths], several limitations warrant consideration" (about two-thirds of papers).
- 11/31 number the limitations (First, Second …).

**Generic value sentences in the conclusion.**
- The conclusion is the one unit where they are common: 27% of conclusion paragraphs (10 of 37, in 8 papers).
- The paper's final sentence is generic in 7/31 papers.
- In every other unit they stay at or below 7%.

### 2.6 Sentence level

**By section** (median of per-paper values)

| Unit | Sentence length, words | % >40 words | % passive (be + participle) | we/our/us per 1,000 | Abbreviations per 1,000 |
|---|---|---|---|---|---|
| Introduction | 29.5 (21–44); E 31.5, T 27.8 | 20 (0–60); E 25, T 17 | 26 | 3.3; E 0, T 5.2 | 16.8 |
| Review | 27 (16.5–36); E 27, T 25 | 14 | 28 | 1.3 | 11.9 |
| Present study | 23 | 4 | 21 | 9.7; E 0, T 13.1 | 25.2 |
| Results | 22 (15–30) | 7 | 21 | 4.6 | 23.5; E 33, T 7 |
| Discussion | 26 (19.5–33.5) | 13.6; E 16, T 12 | 23 | 6.4; E 6.1, T 8.9 | 12.7; E 27, T 8 |
| Implications | 27 | 12.5 | 18.5 | 3.8 | 12.2 |
| Limitations | 24 | 8 | 32; E 40, T 29 | 8.9 | 13.1 |
| Conclusion | 26 | 0 | 15 | 6.5; E 0, T 13.8 | 16 |
| **All main prose** | **26.5 (22–32); E 27, T 25.2** | **14.6 (2.7–28.2); E 16.9, T 11.8** | **24.2 (10–45.5); E 29, T 24** | **4.8 (0–13.9); E 3.4, T 6.9** | **15.1 (1.1–63.5); E 17.9, T 9.2** |

**Other sentence-level measures**
- **Short sentences.** Sentences under 10 words are 2.6% of main prose.
- **Paragraph length.** Paragraphs in main prose run a median of 130 words (94–207).
- **Paragraph-initial connectives.** 21% of main-prose paragraphs start with one (0–43%; E 23, T 17). The most frequent are *while*, *although*, *moreover*, *furthermore*, *despite*, *however*, *second*, *finally*.
- **First person.**
  - *I* is used only by single authors (EN16 5.5 per 1,000; EN15 2.5).
  - 3 papers stay below 1 *we* per 1,000 words (EN10 0; EN16 0.3; EN11 0.8), so impersonal prose is also within the published range.

**Stock phrases and AI-typical words** (per 10,000 words of main prose; total 132,642 words; one occurrence in a 4,000-word main text = 2.5 per 10,000)

| Phrase | Pooled rate | Per-paper median (E / T) | p90 | Max | Papers using (E / T) |
|---|---|---|---|---|---|
| however | 16.1 | 13.3 (14.3 / 12.7) | 34.4 | 43.3 | 31 (15/16) |
| therefore | 6.9 | 6.2 (6.2 / 6.4) | 12.8 | 20.0 | 30 |
| thus | 5.9 | 2.1 | 20.4 | 24.1 | 19 |
| moreover | 5.7 | 4.2 (5.3 / 3.9) | 12.5 | 20.5 | 23 (12/11) |
| furthermore | 4.5 | 2.5 (3.1 / 2.4) | 11.0 | 19.7 | 20 (10/10) |
| additionally | 3.8 | 2.1 (0 / 2.7) | 9.5 | 15.8 | 16 (6/10) |
| in addition | 3.3 | 2.7 | 8.5 | 13.3 | 19 |
| highlight(s/ed) | 6.8 | 3.2 | 17.9 | 32.4 | 22 |
| foster(s/ed) | 5.5 | 3.9 | 12.5 | 19.9 | 27 |
| essential | 4.7 | 3.6 (2.1 / 5.2) | 8.9 | 15.9 | 21 (8/13) |
| crucial | 4.1 | 2.5 (2.1 / 3.1) | 7.9 | 20.0 | 21 (9/12) |
| "[valuable/new] insights", "provide insights" | 3.6 | 2.7 (3.3 / 0) | 10.7 | 14.3 | 19 (12/7) |
| it is important to / it should be noted | 3.3 | 2.8 | 6.7 | 11.3 | 23 |
| comprehensive | 2.8 | 1.8 | 6.7 | 9.4 | 17 |
| play a [crucial/key/vital …] role | 1.7 | 0 | 4.1 | 9.8 | 15 |
| notably | 1.7 | 0 (0 / 0.7) | 4.4 | 7.3 | 11 (3/8) |
| robust | 1.6 | 0 | 3.6 | 8.3 | 12 |
| nuanced | 1.4 | 0 | 3.9 | 7.0 | 14 |
| navigate | 1.4 | 0 | 3.9 | 6.7 | 12 |
| fill / address / bridge a gap | 1.4 | 0 | 4.4 | 8.0 | 9 |
| underscore(s) | 1.2 | 0 | 3.9 | 5.6 | 11 |
| novel | 1.2 | 0 | 4.5 | 7.8 | 11 |
| leverage | 1.1 | 0 | 4.4 | 6.4 | 8 |
| the first (study) to / to the best of our knowledge | 0.9 / 0.7 | 0 / 0 | 2.8 / 2.0 | 5.0 / 5.0 | 8 / 7 |
| pivotal / multifaceted / importantly / interestingly | 0.8 each | 0 | 2.3–3.6 | 5.6–8.2 | 6–8 |
| shed light on | 0.7 | 0 | 2.5 | 9.6 | 7 |
| intricate / holistic / vital / landscape | 0.5–0.6 | 0 | 1.6–2.5 | 4.7–11.6 | 4–6 |
| it is worth noting / delve / a growing body of | 0.4 / 0.4 / 0.3 | 0 | 0 / 2.2 / 0 | 6.7 / 2.8 / 4.1 | 3 / 4 / 3 |
| in conclusion / pave the way / in today's / paramount / noteworthy / realm | 0.1–0.2 | 0 | 0 | 2.1–4.4 | 1–3 each |
| garnered / gained attention | 0 | 0 | 0 | 0 | 0 |
| Signposting (in this section, the remainder of the paper, as noted above …) | — | 0 (E 0 / T 1.5) | 5.9 | 8.0 | 12 |

Composite indices per paper (per 10,000 words):
- **AI-typical words** (24 items from *notably* to *in conclusion*): median 20.3 (5.6–82.3; E 20.0, T 24.3). Highest: EN07 82, EN22 65, EN04 55, EN29 54, EN30 47, so the high values occur in both tiers.
- **Additive connectors** (*furthermore*, *moreover*, *additionally*, *in addition*): median 14.6 (0–41).
- **Rare phrases** (*delve*, *in today's*, *pave the way*, *a growing body of*, *it is worth noting*, *noteworthy*, *realm*, *in conclusion*, *paramount*, *garnered attention*): median 1 occurrence per paper, max 3.

## 3. Stability check: is 31 enough?

Medians are per paper. CIs are 4,000-sample bootstrap 95% intervals. δ is Cliff's delta (E vs T; positive means E is higher), and p comes from a permutation test of the difference in medians.

| Measure | E median (range) | T median (range) | Pooled median [95% CI] | Pooled p90 [95% CI] | δ (p) | Verdict |
|---|---|---|---|---|---|---|
| Sentence length, main prose | 27.0 (23–32) | 25.2 (22–29) | 26.5 [25.0, 28.0] | 29.0 [28.0, 30.5] | +.25 (.35) | Stable; CI ±6%. 31 is ample |
| % sentences >40 words | 16.9 (5.9–28.2) | 11.8 (2.7–18.3) | 14.6 [12.0, 15.8] | 19.7 [16.9, 26.1] | **+.53 (.01)** | Real tier difference: set the target from T (≈12%) and the flag from the pooled max |
| Introduction citations / 1,000 | 25.1 (14.6–33.6) | 22.1 (11.3–36.5) | 23.4 [20.7, 27.9] | 33.2 [29.9, 36.1] | +.09 (.40) | Stable |
| Review citations / 1,000 | 25.5 (15.2–38.1) | 24.5 (16.7–41.7) | 25.5 [23.2, 30.2] | 35.3 [30.6, 39.2] | +.12 (.68) | Stable |
| Review % sentences cited | 63.7 (37–90) | 53.5 (37.5–100) | 59.9 [52.4, 66.7] | 87.5 [73.8, 92.8] | +.30 (.12) | Median stable; T somewhat lower |
| Review % narrative citations | 11.8 (1.7–48) | 12.1 (0–61.5) | 11.8 [8.6, 23.4] | 37.8 [26.0, 52.2] | +.04 (.96) | Tiers agree, but a few papers drive the tail; the upper threshold is unstable |
| Review % parentheses with ≥3 works | 17.9 (0–40) | 8.1 (0–31) | 10.3 [6.0, 18.0] | 31.0 [21.0, 37.3] | +.27 (.06) | Tier-sensitive and noisy (CI ±58%) |
| Discussion citations / 1,000 | 13.7 (4.4–21.6) | 12.1 (3.8–25.9) | 13.5 [10.4, 15.2] | 21.7 [17.4, 24.0] | +.01 (.71) | Stable |
| Discussion citations per point | 2.0 (0–8) | 3.2 (0–9) | 2.5 [2.0, 3.5] | 6.8 [4.0, 8.2] | −.36 (.11) | T higher; moderately stable |
| Points restating the finding (%) | 100 (67–100) | 100 (75–100) | 100 [100, 100] | 100 | 0 (1.0) | Stable (ceiling) |
| Points compared with cited work (%) | 83 (0–100) | 75 (33–100) | 75 [67, 100] | 100 | +.03 (.74) | Stable |
| Points with any explanation (%) | 58 (pooled over points) | 92 | — | — | (see §2.4) | Large tier difference that holds within coders; use T as the target |
| Generic closing sentences, % of paragraphs | 4.2 (0–14.3) | 1.5 (0–12.5) | 3.6 [0, 4.5] | 10.8 [5.7, 12.5] | +.13 (.37) | Rare event coded once: the median is stable near 0–5%, the tail is not |
| we/our/us per 1,000 | 3.4 (0–11.8) | 6.9 (0.3–13.9) | 4.8 [3.1, 7.8] | 11.8 [9.6, 12.2] | −.38 (.10) | Tier- and design-dependent; CI ±49% |
| % passive sentences | 29.1 (10–45.5) | 23.6 (13.5–41) | 24.2 [23.4, 31.3] | 36.4 [32.8, 41.1] | +.27 (.16) | Fairly stable |
| AI-typical word index / 10,000 | 20.0 (5.6–82) | 24.3 (5.7–65) | 20.3 [16.1, 29.5] | 53.7 [34.1, 65.4] | −.06 (.48) | Tiers agree; tail unstable |
| Additive connectors / 10,000 | 17.8 (0–39) | 13.0 (0–41) | 14.6 [10.0, 21.0] | 30.6 [23.3, 39.4] | +.05 (.52) | Tail unstable |
| Abbreviations / 1,000 | 17.9 (1.1–63.5) | 9.2 (1.2–37) | 15.1 [7.4, 22.2] | 37.2 [32.8, 57.3] | +.18 (.40) | Topic-driven (GenAI-heavy E); unstable |

**Verdict**
- **Enough for:** all central tendencies of density and length measures, and the categorical move patterns. The rules in §4 are supported by both tiers unless marked.
  - Sentence length, citation densities by section, discussion point structure (restate, compare), passive share.
  - Gap types, aim placement, paragraph-ending distributions.
  - For these measures the medians agree across tiers (|δ| < .30, p > .10) and the bootstrap CIs are within about ±15% of the median.
  - The bootstrap projection suggests that 10–90 papers would bring their medians within ±10%. Most are already close, and sentence length needs only about 10.
- **Tier-dependent:** for these, the writing target should follow the top tier, while the flag thresholds can use the pooled range.
  - Long sentences (δ = .53, p = .01).
  - Explanation in discussion points (unexplained points E 42% vs T 8%; named theory 17% vs 41%).
  - Explicit contribution claims in the Introduction (6/15 vs 13/16).
  - Counter-evidence in the review (14/15 vs 9/16, the difference driven by qualitative top-tier papers).
  - Citation bundles of ≥3 works (18% vs 8%).
  - First person (3.4 vs 6.9 per 1,000).
- **Not enough for upper-tail thresholds** of skewed measures: narrative-citation share, bundle share, first person, abbreviations, connector and AI-word indices, single stock phrases, generic closings.
  - With 31 papers, p90 rests on about three papers, and its bootstrap CI spans roughly ±10–35%, mostly ±25–35% (e.g., narrative share p90 26–52%, AI-word index p90 34–65).
  - Halving that width needs about four times as many papers, so 100–150 papers are needed for p90/p95 thresholds you can defend.
  - For now, the thresholds in §6 are set at or just above the published maximum. A flag then means "outside everything we have seen", not "unusual".
- **Not enough for design-specific rules.** There are only 8 qualitative and 5 mixed-methods papers. Results openings, citation density in the Discussion and first-person rates differ by design, so 15–20 papers per design would be needed for design-stratified thresholds.
- **Coding reliability.** Single coding is adequate for the common codes (κ = 0.78 on paragraph endings). Rare codes (generic closings, hypothesis derivation "none") should be double-coded before they are used as hard gates.

## 4. Writing rules

Each rule gives its supporting numbers first (pooled; E/T where they differ), then what to do. Slots are in [brackets].

### Introduction

1. **Write 3–5 paragraphs, about 400–800 words, before the first review heading.** Published: median 529 words (180–1,430), 4 paragraphs of about 140 words. If there is no separate review section, the Introduction can run to about 1,200–1,400 words (EN14, EN16, EN30).
2. **Open with the phenomenon, trend or practical problem, and cite it.** Published:
   - first sentence is a trend or development 11/31, a practical problem 5, the state of research 4, a definition 4, a broad importance claim 4, and a statistic 0;
   - 23/31 first sentences carry a citation;
   - the first move is background in 20/31.

   Do not open with a quotation, "In today's [world]", or an uncited sweeping claim.
3. **Cite in more than half the sentences, information-prominently.** Published:
   - 23 citations per 1,000 words (11–37) and 57% of sentences cited (32–90);
   - narrative citations median 0% in the Introduction;
   - one parenthesis in six carries three or more works.

   Write "[claim] ([Author], [year]; [Author], [year])". Use bundles for consensus claims, not for every sentence.
4. **State the gap more than once, as a specific absence plus a contrast or design weakness.** Published:
   - median 5 gap statements;
   - a gap in the Introduction 31/31, restated at the end of the review in 18 and in the present-study section in 10;
   - types: absence 28, focus–neglect 18 (E 6, T 12), practical problem 14, population or context 13, method 13.

   Templates:
   - "Most studies have [examined A in B]; [C] remains [unexamined]."
   - "Prior studies relied on [design or measure], which cannot [show X]."
   - "Little is known about whether [X] holds for [population]."
5. **End on the study: aim, design and contribution, in the first person.** Published:
   - aims end the Introduction in 18/31 or open a present-study section in 10/31;
   - a design preview in 24/31; a theory named in 23/31; first-person aim in 19/31 (T 12/16);
   - an explicit contribution claim in 19/31 (E 6/15, T 13/16).

   Template: "In this study, we [examine X] among [population] using [design]. [We address two RQs: …]. In doing so, we contribute to [literature] by [specific addition]." A roadmap is optional (4/31, all in the top tier). A novelty claim ("to our knowledge, no study") appears in 7/31: use it only if it is true and checkable.
6. **Paragraphs stop on evidence, the gap or the aim, not on a value sentence.** Published:
   - endings: evidence 35%, aim 23%, gap 18%, specific inference 10%; generic value sentence 1.5% (2 of 132);
   - first sentences: cited claim 28%, aim 17%, own claim 14%, research as subject 13%, gap 12%; a named author as subject only once in 132 paragraphs.

### Literature review and hypotheses

7. **Organise the review by construct or theme in 2–5 subsections, and name a theory.** Published: median 3 subsections; thematic 10, by construct 6, by hypothesis 5, framework then evidence 5, single block 5; a theory named in 28/31.
8. **Synthesise first; illustrate with single studies.** Published:
   - 25.5 citations per 1,000 words (15–42) and 60% of sentences cited (37–100);
   - synthesis sentences outnumber single-study sentences about 2:1 (median 17 vs 9; 61% synthesis);
   - runs of three or more single-study sentences occur once in most reviews (22/31) and twice or more in 10/31.

   Do this:
   - Open the paragraph with a synthesis claim ("Studies consistently show [X] (A; B; C)").
   - Then give one or two specific studies whose design matters, in the past tense with the author named ("[Author] ([year]) found that [result] in [sample]").
   - Then state what follows for this study.
9. **Keep author-prominent citations to about one in eight.** Published: narrative citations median 12% of review citations (0–62; only EN23 is above 50%). The verb after a narrative citation is past in 67% of cases, and *found* is the most frequent verb. Claims with parenthetical citations are in the present or present perfect about 90% of the time.
10. **Include at least one piece of contrary or mixed evidence.** Published: 23/31 reviews, median 2. Devices:
    - "findings on [X] are mixed: [A] reported …, whereas [B] …";
    - "although [consensus] (cites), [study] found [exception]";
    - "However, [Author] ([year]) showed …".
11. **Derive each hypothesis from theory plus evidence, then state it in one labelled sentence.** Published:
    - 16/31 papers state hypotheses (all quantitative or mixed), a median of 3.5 per paper;
    - derivation: theory and evidence 63%, theory only 25%, evidence only 8%, none 3%;
    - placement: at the end of each review subsection 5, in a present-study section 8;
    - labels: H1/H1a 6, "Hypothesis 1" 3, prose 7;
    - 12/16 pair hypotheses with RQs, and 14/16 are directional.

    Template: "[Theory] holds that [mechanism] ([cites]). Consistent with this, [studies] found [pattern] ([cites]). We therefore expected that [X] would be positively related to [Y] (H1)."
12. **Review paragraphs end on evidence, a specific inference or the hypothesis.** Published: evidence 41%, specific inference 18%, aim 11%, hypothesis 11%, gap 9%, transition 6%; generic value sentence 2%. Close the review by restating the gap (20/31).

### Results

13. **Start each paragraph with the analysis step or the finding in words; put statistics after the claim.** Published:
    - quantitative openings: procedure 30%, finding in words 27%, table pointer 17%, checks 14%; opening with a number 4%;
    - statistics sit inside parentheses (median 100% of statistic expressions), or are set off by commas in 4 of 19 papers;
    - 55% of sentences carry numbers, with a median of 2 numbers per numeric sentence.

    Template: "To test H1, we [estimated …]. [X] was positively related to [Y] (β = __, p = __), supporting H1." Qualitative paragraphs open with the theme claim (59%) and then the quote (21% open with the quote).

### Discussion

14. **Open by restating the aim and, optionally, summarising the findings in one paragraph; then discuss about 4 points.** Published:
    - opening move: aim 13, aim plus summary 9, first point 5, summary of all findings 3;
    - a separate summary paragraph in 14/31;
    - median 4 points (2–8);
    - subheadings: none in 15/31, topic labels in 13/31, claim headings in 1.
15. **Each point opens by restating the finding in words, unhedged.** Published: 98% of points restate the finding; 88% do so in words only and 10% repeat a statistic; 2.5% put a modal hedge on the finding. Only 3.9% of Discussion sentences carry a number.
16. **Compare the finding with 2–4 cited studies, including disagreements.** Published:
    - 76% of points compare: consistent 50%, both 20%, inconsistent 6%;
    - median 3 citations per point (IQR 1–5), with T higher than E (3.2 vs 2.0);
    - 13.5 citations per 1,000 Discussion words (3.8–26); 30% of sentences cited.
17. **Explain each finding, name the theory where you can, and hedge the explanation rather than the finding.** Published:
    - 75% of points explain: mechanism 37.5%, named theory 14%, method or measurement 12.5%, context 11%;
    - top-tier points explain 92% of the time and name a theory 41% of the time (E 58% and 17%);
    - 69% of explanations are hedged (*may*, *one possible explanation is*), against 2.5% of findings;
    - restate, compare and explain together in 52.5% of points (T 64%).
18. **Report null and contrary results in the Discussion and explain them.** Published: 35% of points concern a null or contrary result; 67% of these are explained, often by measurement or design reasons, and are followed by a concrete future test. Template: "Contrary to H2, [X] was not related to [Y]. This differs from [cites]. One possible reason is [measurement feature]; [design] could test this."
19. **End points on a specific interpretation, the finding's verdict or a specific next step.** Published: specific interpretation 36%, finding 19%, evidence 15%, future direction 12%, implication 7.5%; generic value sentence 4%. Only 3% of Discussion paragraphs end on a generic sentence.

### Implications, limitations, conclusion

20. **Write about 5 implications, each tied to a finding and addressed to a named actor.** Published:
    - median 5 items (1–11), in prose rather than numbered lists (28/31);
    - explicit anchoring 39%, implicit 42%, generic 19% (T 15%);
    - teachers named in 14 papers and educators in 9;
    - the strongest directive is *should* in 13 papers and *must* in 6;
    - 55% of implication paragraphs end on a concrete action, 7% on a generic sentence.

    Template: "Because [finding], [actor] should [action], for example by [concrete practice]."
21. **Put the limitations in one place, name each one concretely, and turn most into a design for future work.** Published:
    - a single unit in 30/31 (own section in 22);
    - median 4 distinct limitations (1–8); 57% paired with a future-research direction;
    - 25/31 answer at least one limitation with a mitigating fact;
    - 60% of limitation paragraphs end on a future direction.

    Template: "[First], [design feature] limits [specific inference]; [mitigating fact]. Future studies using [design] could test whether [question]."
22. **Keep the conclusion short and end on substance.** Published:
    - a conclusion in 24/31, median 148 words (28–801), usually one paragraph;
    - moves: summary 20, implication 17, contribution 13, future direction 11;
    - the final sentence of the paper is a future direction (10), an implication (8), a generic value sentence (7) or a contribution (2).

    End on the main implication or a specific next step. If a closing message is wanted, allow one evaluative sentence, as the last sentence of the paper only.

### Sentences

23. **Aim for a median of about 25 words per sentence, with no more than about 1 sentence in 7 over 40 words.** Published:
    - median 26.5 (22–32), T 25.2; over 40 words 14.6% (T 11.8%);
    - Results run shortest (22) and the Introduction longest (29.5).
24. **Use *we* for the study's actions and decisions, mostly in the present-study, Discussion and limitations sections.** Published:
    - 4.8 per 1,000 words (0–13.9; T 6.9);
    - present study 9.7, limitations 8.9, Discussion 6.4, review 1.3 per 1,000.
25. **Keep the passive to about a quarter of sentences.** Published: 24% of sentences (10–45.5); highest in limitations (32%) and the review (28%).
26. **Use connectors sparingly and vary them; drop AI-typical words.** Published:
    - *however* is the workhorse (median 13 per 10,000);
    - *furthermore*, *moreover*, *additionally* and *in addition* together run at a median of 14.6 per 10,000 (max 41), i.e. about 6 in a 4,000-word main text;
    - 21% of paragraphs start with a connective;
    - AI-typical words are present but thin (index median 20 per 10,000);
    - *delve*, *in today's*, *pave the way*, *a growing body of*, *it is worth noting*, *realm*, *paramount* and *in conclusion* are rare (median 1 occurrence in total per paper, max 3).
27. **Abbreviate only recurring core constructs and define them once.** Published: 15 abbreviation tokens per 1,000 words (1–63.5; T 9.2).
28. **Little signposting.** Published: no signposting in 19/31 papers (max 8 per 10,000); a roadmap in 4/31.

### Structural templates

- **Introduction (4 paragraphs)**
  1. [Trend or problem, cited] → [why it matters for (actor/outcome), cited].
  2. [What research has established, synthesis with bundled citations] → [one or two specific findings].
  3. [However, most studies have (focused on A / used design D); (B / mechanism / population) remains (unexamined), cited] → [why that matters for this question].
  4. [In this study, we (aim) in (context) using (design)] → [RQs, or "see Present study"] → [We contribute to (literature) by (specific addition)].
- **Review subsection that builds a hypothesis:** [definition or theory claim, cited] → [mechanism: According to (theory), X … because …] → [evidence: studies show (A; B; C); (Author) (year) found …] → [counter-evidence: however, findings are mixed …] → [Based on (theory and evidence), we hypothesize that … (H1)].
- **Present-study section:** gap recap (1–2 sentences) → aim and design in the first person → RQs and hypotheses, labelled → exploratory question if any.
- **Results paragraph:** [To test H1, we …] → [X was (positively) related to Y (statistics)] → [robustness or moderator check] → [H1 was supported / not supported].
- **Discussion point:** [finding restated in words, unhedged] → [comparison: consistent with A (year) and B (year); unlike C (year), who found …] → [explanation, hedged: one possible explanation is …, in line with (theory)] → [specific inference or implication].
- **Null or contrary point:** [Contrary to H2, X was not related to Y] → [differs from (cites)] → [one or two reasons: measurement, design, context] → [what study would test this].
- **Implication item:** [Because (finding)] → [(actor) should (action)] → [for example, (concrete practice)].
- **Limitation:** [design or sample feature] → [the specific inference it limits] → ([mitigating fact]) → [Future studies using (design) could test whether (question)].
- **Conclusion (1 paragraph):** [aim and main finding in one sentence] → [contribution] → [main implication] → [specific future direction or implication as the final sentence].

## 5. Automatically checkable measures and flag thresholds

Thresholds sit at or just beyond the published extremes, so published papers rarely trigger them. The last column shows how many of the 31 published papers trigger each flag. Rates per 10,000 words are noisy in short texts: at 4,000 words of main prose, one occurrence equals 2.5 per 10,000. For single phrases, use counts when the text is short. Measures marked † need paragraph-level judgment (an LLM classifier or a human), not regular expressions.

| Measure | Published: pooled median (range); E / T | Flag when | Published papers flagged |
|---|---|---|---|
| Sentence length, median words (main prose) | 26.5 (22–32); 27 / 25.2 | < 20 or > 33 | 0/31 |
| % sentences > 40 words (main prose) | 14.6 (2.7–28.2); 16.9 / 11.8 | > 30 | 0/31 |
| Paragraph length, median words (main prose) | 130 (94–207) | < 75 or > 230 | 0/31 |
| Introduction citations / 1,000 words | 23.4 (11.3–36.5) | < 10 | 0/30 |
| Introduction % sentences cited | 56.7 (32–90) | < 25 | 0/30 |
| Review citations / 1,000 words | 25.5 (15.2–41.7) | < 12 | 0/28 |
| Review % sentences cited | 59.9 (37–100) | < 30 | 0/28 |
| Review % narrative (author-prominent) citations | 11.8 (0–61.5) | > 65 | 0/28 (> 50 flags 1) |
| Review % parentheses with ≥ 3 works | 10.3 (0–40) | > 45 | 0/28 |
| Discussion citations / 1,000 words | 13.5 (3.8–25.9) | < 3, or no citation at all | 0/29 |
| Discussion % sentences containing a number | 3.9 (0–30.8) | > 35 | 0/30 |
| † Discussion points opening with the restated finding | 100% (67–100) | < 60% of points | 0/30 |
| † Discussion points compared with cited work | 75% (0–100) | < 25% of points | 1/30 |
| † Hedge on a restated finding (modal or adverb) | 2.5% of points; per paper 0 (0–25) | > 30% of points | 0/30 |
| † Generic value sentence as paragraph ending (all main units) | 3.6% (0–14.3) | > 15% of paragraphs, or 3 or more consecutive paragraphs | 0/31 (2 consecutive: 3/31) |
| Value-phrase paragraph endings (regex proxy†) | 5.9% (0–20) | > 25% of paragraph-final sentences | 0/31 |
| we/our/us per 1,000 words | 4.8 (0–13.9) | > 16 | 0/31 |
| % sentences with be + participle | 24.2 (10–45.5) | < 8 or > 50 | 0/31 |
| Abbreviation tokens / 1,000 words | 15.1 (1.1–63.5) | > 60 | 1/31 |
| Signposting / 10,000 words | 0 (0–8) | > 10 | 0/31 |
| % paragraphs opening with a connective | 21 (0–43) | > 45 | 0/31 |
| furthermore + moreover + additionally + in addition / 10,000 | 14.6 (0–41) | > 45 | 0/31 |
| AI-typical word index / 10,000 (24 items) | 20.3 (5.6–82.3) | > 70 | 1/31 |
| Rare phrases (delve, in today's, pave the way, a growing body of, it is worth noting, noteworthy, realm, in conclusion, paramount, garnered attention): total count | 1 (0–3) | ≥ 4 | 0/31 |
| Single words / 10,000 words (published max in brackets) | crucial (20), highlight (32), foster (20), essential (16), insights (14), notably (7.3), underscore (5.6), pivotal (5.6), nuanced (7.0), multifaceted (7.8), leverage (6.4), navigate (6.7), robust (8.3), comprehensive (9.4), shed light on (9.6), play a [adj] role (9.8), it is important to / it should be noted (11.3) | above the published max, i.e. crucial > 21, highlight > 35, foster > 21, notably > 8, underscore > 6, pivotal > 6, nuanced > 8, multifaceted > 8, leverage > 7, navigate > 7, robust > 9, comprehensive > 10, shed light on > 10, play a role > 10, it is important to > 12 | 0/31 each |
| Results: paragraphs opening with a number or statistic (quantitative and mixed) | 4%; per paper 0 (0–16) | > 20% | 0/23 |
| Results: numbers per number-bearing sentence (median) | 2 (1–5) | > 6 | 0/23 |
| † Implication items with no traceable finding | 17% per paper (0–83) | > 2/3 of items | 1/31 |
| † Hypotheses with no theoretical or empirical argument before them | 3% of hypotheses (3 papers have one each) | more than half of a paper's hypotheses | 1/16 (EN23: a single null hypothesis) |
| † Gap statement in the Introduction | 31/31 | absent | 0/31 |
| † Aims or RQs stated before Method | 31/31 | absent | 0/31 |
| † Limitations in one unit | 30/31 | absent, or spread over ≥ 3 sections | 0/31 |

Use the flags as prompts to revise, not as hard rejections. Several flags fire only on extreme values (abbreviations, the AI-word index), so a manuscript can be unlike published prose and still pass. The writing rules in §4 target the medians, not the thresholds.

## 6. Interpretation (not a direct corpus result)

- **English articles carry their argument with citations and comparisons.** About 60% of sentences in the review and the Introduction carry a citation, and three-quarters of discussion points are set against named prior studies. AI drafts tend to do the opposite: few citations, much uncited generalisation, and a closing evaluation in each paragraph. Rules 3, 8, 16 and 19 target this.
- **Generic value closings are rarer in English than in Chinese articles.** The English rate is 1.5–7% of paragraphs outside the conclusion, against 8% in Chinese discussions and 27% in Chinese recommendations (`writing_moves_zh.md`). The conclusion is the only place where English papers allow one, and usually as the final sentence (7/31). A checker can be strict everywhere else.
- **Caution sits on explanations, not on findings.** This matches `coding_summary_en.md`. The top tier differs from the earlier batch mainly in doing more interpretive work: it explains, names theories, states contributions, uses *we* and writes shorter sentences. The skill should aim at the top-tier profile.
- **AI-typical vocabulary already appears in published 2024–2026 papers,** sometimes densely (EN07, EN22). Single occurrences therefore prove nothing. The useful signals are density and clustering: many rare phrases, connectors stacked at paragraph starts, value-phrase endings.
- **Hypothesis sections are formulaic and easy to template.** The most consistent pattern is derivation from theory plus evidence (63%) followed by a labelled one-sentence prediction.

**Comparison with the Chinese corpus** (`writing_moves_zh.md`; where measures are comparable)

| Measure | English (31) | Chinese CSSCI (27) |
|---|---|---|
| Discussion points per paper | 4 | 3 |
| Points restating the finding | 98% | 87% |
| Points compared with prior work (cited) | 76% | 33% (25%) |
| Points naming a theory | 29% (T 41%) | 37% |
| Citations per point | 3 | 1.25 |
| Generic paragraph endings: Introduction / review / Discussion / recommendations or implications | 1.5% / 2.1% / 3% / 7% | 13% / 3% / 8% / 27% |
| Introduction ends on aims, RQs, design, contribution or roadmap (EN) / aims, value or RQs (ZH) | 23/31 | 25/27 |
| Narrative ("Author (year) found") citations in the review | 12% of citations | 8% of cited sentences |

## 7. Files

- Summary: this file.
- Per-paper records: `private/writing_moves_en_coding.jsonl` (local, gitignored). One line per paper with:
  - every paragraph's unit, moves, opening and closing codes;
  - Introduction, review, hypothesis, discussion-point, implication, limitation and conclusion fields;
  - Results opening codes;
  - automatic measures by section;
  - excerpts only as fragments of eight words or fewer, or slot templates.
