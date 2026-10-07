# How English SSCI education articles write each section: moves, paragraphs and sentence habits (n = 50, 2026-10-08)

Purpose: break down how published English empirical articles write the Introduction, the literature review and hypotheses, the Results prose, the Discussion and the closing sections (implications, limitations, conclusion), so that edu-writing can learn to write like them and a checker can flag prose that departs from them. This file measures writing only: moves, paragraph construction, use of literature and sentence habits.

It builds on, and does not repeat:
- `coding_summary_en.md`: stance and hedging, EN01–EN15;
- `sections_summary.md`: structure and lengths, EN01–EN15.

Its structure follows `writing_moves_zh.md` so the two can be compared. It replaces the 31-paper version of 2026-10-07; §7 lists every rule and threshold that changed. Papers are identified by ID only. Examples are fragments of eight words or fewer, or slot templates; no sentences are quoted. Per-paper records are in `private/writing_moves_en_coding.jsonl` (local, gitignored).

## 1. Method

**Corpus.** EN01–EN50 (`manifest_en.json`), all empirical, 2024–2026.

| Group | Papers | Designs | Journals |
|---|---|---|---|
| earlier (E) | EN01–EN15 (n = 15) | 9 quantitative, 4 qualitative, 2 mixed | IJETHE, ETR&D, EIT, C&E, BJET, TATE, L&I, IJME, MER |
| top (T) | EN16–EN50 (n = 35) | 13 quantitative, 11 qualitative, 11 mixed | AERJ, JEP, CEP, L&I, C&E, Internet & HE, Educational Researcher, npj Science of Learning, Higher Education, Studies in HE, BJET, JLS, Psychology of Music, BJME, RSME, BERJ, Science Education, Learning Media & Technology, CBE–LSE, JRST, AEHE, Teaching in HE, J Learning Analytics, Modern Language Journal, TATE, Sociology of Education, AERA Open, J Teacher Education |
| by design | 22 quantitative (Qt), 15 qualitative (Ql), 13 mixed (Mx) | | |

- "Earlier" is the label of the first acquisition batch, not an earlier period. Both tiers are 2024–2026.
- The tiers are confounded with topic and design:
  - 7 of the 15 earlier papers are about generative AI;
  - the 19 papers added in this round (EN32–EN50) are mostly qualitative or mixed.

  §3 therefore checks every tier difference within design.

**What was coded by hand**

- Every paragraph of the Introduction, review or theoretical background, present-study section, Discussion and closing sections of all 50 papers: 1,488 body paragraphs.
  - Introduction 218, review and present study 605, Discussion 354 (226 discussion points), implications and contributions 113, limitations and future research 132, conclusion 66.
  - Not counted as body paragraphs: 42 results paragraphs inside combined Results-and-Discussion sections, 149 one-line list items (RQs, hypotheses) and 67 skipped items (participant quotes, epigraphs, practitioner boxes).
- The first sentence of every Results paragraph: 1,116 openings.
- Per paragraph: function (unit), moves in order, type of the first sentence, type of the last sentence.
- Per paper: section-level fields. Hypotheses were also listed one by one with their derivation for the 19 new papers.
- Paragraphs were coded by function, not by heading.
- **Unit boundary.** The Introduction is the text before the first review subheading or review section. Ten papers carry their review inside an Introduction without subheadings.

**Coders.** Thirteen coding agents followed one written scheme (`SCHEME.md` plus a short addendum for per-hypothesis listing).
- Round 1 (EN01–EN31): 7 coders.
- Round 2 (EN32–EN50): 6 coders. Each received a mix of designs plus one already-coded anchor paper, recoded blind.

**Reliability**

| Check | Material | Paragraph endings: agreement, κ [95% CI by paper bootstrap] | Generic-closing code (GEN) |
|---|---|---|---|
| Independent second coder (2 agents) | 10 random papers: E 4, T 6; Qt 4, Ql 3, Mx 3 (EN01, EN04, EN06, EN09, EN19, EN22, EN25, EN32, EN40, EN41); 278 paragraphs | 95.3%, κ 0.95 [0.93, 0.97]. Units 98.7%, κ 0.98. By tier: E κ 0.95, T κ 0.94. By design: Qt 0.95, Ql 0.92, Mx 0.98 | Coder 1: 12 GEN, coder 2: 10, both: 10. Binary agreement 99.3%, κ 0.91 [0.79, 1.00], positive agreement 0.91 |
| Anchors: original round-1 coder vs blind round-2 coder | 6 papers: EN03, EN10, EN11, EN18, EN26, EN29 (E 3, T 3; 2 per design); 165 paragraphs | Endings 93.9%, κ 0.93 [0.90, 0.97]. Openings 91.5%, κ 0.90. Units 98.4%, κ 0.98. Paper-level categorical fields 94/102 agree (92%) | 6 vs 5 GEN, 5 shared; κ 0.91 |
| Hypothesis derivation (second coder) | The 4 hypothesis papers in the sample, 34 hypotheses | Count-level only, because round-1 coding recorded tallies, not items. EN01, EN09 and EN22 have identical tallies (31 hypotheses). EN19 differs: 3 hypotheses with one "none" vs 1 hypothesis "theory + evidence", because the coders split items a–c differently. The maximum possible item agreement is 32/32 on the hypotheses both coders listed; item-level κ cannot be computed | "none" (no argument): 1 vs 0 |

**Drift and caveats**
- **No coder drift.** On the anchors, the distribution of ending codes was nearly identical: EVID 48 vs 50, SPEC 25 vs 24, GEN 6 vs 5.
- **Count fields are noisier than codes.** Counts of synthesis versus single-study sentences differ by up to 60% on one anchor (EN03). Treat count fields as approximate.
- **Same-model agreement.** All coders are instances of the same model following one written scheme, so these κ values likely overstate human–human agreement. A blind check by the lead analyst in round 1 gave κ = 0.78 on 45 paragraph endings; that check read only each paragraph's final sentence.

**Automatic measures** (scripts kept in the session scratchpad, not in the repository)
- Paragraph = one line of the extracted text. Sentence split on terminal punctuation, protecting et al., e.g., i.e., initials and decimals.
- **Citations.** One instance is one author–year parenthesis or one narrative citation (Name (year)). "Works" counts the years. A bundle is a parenthesis with ≥3 works. EN24 (numbered citations removed in extraction) is excluded from citation measures.
- **Tense** of the verb after a narrative citation and of the first finite verb in cited sentences (approximate).
- **Passive** = sentence containing *be* + participle (approximate).
- **First person** = *we/our/us* per 1,000 words, after removing quoted participant speech.
- **Phrase lists:** 55 stock-phrase patterns per 10,000 words, a signposting list, and abbreviations (tokens with ≥2 capitals, ChatGPT excluded).
- **Results:** numbers per sentence; statistic expressions inside vs outside parentheses.
- **Main prose** = Introduction + review + present study + Discussion + implications + limitations + conclusion: median 4,353 words per paper (2,005–7,527).

**Reporting.**
- Aggregates are given pooled (n = 50), by tier (E, T) and by design (Qt, Ql, Mx).
- The pooled column shows median (range) of per-paper values; group columns show medians. Counts are numbers of papers; percentages over paragraphs or points are pooled.
- Tests:
  - Tier: Mann–Whitney or Fisher.
  - Design: Kruskal–Wallis, or a permutation χ² for counts.
  - Bootstrap CIs use 4,000 resamples of papers.

**Data-quality caveats**
- **EN48.** The extracted text lacks the untitled opening of the Introduction (several paragraphs, including the RQs and a roadmap). EN48 is excluded from every Introduction-level field.
- **Section layout in round-2 papers.**
  - EN42 has no separate Discussion (its section 6 carries it).
  - EN43 has a combined Findings-and-Discussion section (29 quote lines skipped).
  - EN47 puts limitations inside its Method.
  - EN41 ends on its Discussion.
- **Lost superscripts.** Superscript 2 is lost in EN08, EN17 and EN22; this is minor for number counts.
- **Other extraction losses.** Tables and captions are excluded everywhere. EN15 and EN31 are accepted manuscripts.
- **AI-polished prose.** The 2024–2026 corpus probably contains some AI-polished prose (§2.6), so thresholds calibrated on it are lenient toward AI-typical words.

## 2. Findings by section

### 2.1 Introduction (49 papers; 218 paragraphs)

| Measure | Pooled | E | T | Qt | Ql | Mx |
|---|---|---|---|---|---|---|
| Words (before first review subheading) | 580 (180–1,430) | 529 | 580 | 608 | 456 | 580 |
| Paragraphs (≥25 words) | 4 (1–12) | 3 | 4 | 4 | 3 | 3 |
| Paragraph length, words | 144 (78–304) | 155 | 141 | 141 | 133 | 183 |
| Sentence length, median words | 30.5 (21–44) | 31.5 | 28.8 | 29 | 31 | 30 |
| Citation instances / 1,000 words | 23.0 (8.7–36.5) | 25.1 | 22.8 | 22.1 | 23.1 | 24.1 |
| % sentences with a citation | 57.1 (27–90) | 60.0 | 55.6 | 57.1 | 60.0 | 56.2 |
| % narrative citations | 0 (0–38) | 0 | 0 | 0 | 10 | 0 |
| % parentheses with ≥3 works | 16.3 (0–62.5) | 16.7 | 14.3 | 18 | 25 | 12.5 |
| we/our/us per 1,000 | 3.0 (0–22.6) | 0 | 4.5 | 3.7 | 0 | 4.2 |

**How the Introduction opens** (first sentence; 49 papers)

| Type | Pooled | E | T | Qt | Ql | Mx |
|---|---|---|---|---|---|---|
| Trend, technology or development | 16 | 6 | 10 | 6 | 7 | 3 |
| Practical problem or puzzle | 9 | 2 | 7 | 3 | 3 | 3 |
| Broad importance claim | 7 | 2 | 5 | 2 | 1 | 4 |
| State of research | 6 | 2 | 4 | 5 | 1 | 0 |
| Definition | 5 | 2 | 3 | 2 | 1 | 2 |
| Quotation / policy / aim / theory | 2 / 2 / 1 / 1 | — | — | — | — | — |
| Statistic | 0 | 0 | 0 | 0 | 0 | 0 |
| First sentence carries a citation | 32/49 | 11/15 | 21/34 | 17/21 | 9/15 | 6/13 |
| First move is background | 31/49 | 10/15 | 21/34 | 14/21 | 10/15 | 7/13 |

**Move sequence.**
- Moves coded: BG (background), IMP (importance), DEF (definition), EVID (prior evidence), GAP, THEORY, AIM, DESIGN (preview of design), CONTRIB (contribution), ROADMAP.
- All Introductions are pruned or repeated versions of BG → IMP → EVID → GAP → AIM (→ DESIGN → CONTRIB → ROADMAP).
- Papers using each move: GAP 45, BG 45, IMP 45, AIM 45, EVID 44, DESIGN 30, DEF 28, CONTRIB 22, THEORY 19, COUNTER 11, ROADMAP 7.
- The last move is AIM in 17 papers, CONTRIB in 14, ROADMAP in 6, DESIGN in 4 and EVID in 4.

**Gap.**
- **How many.** Median of 4 gap statements per paper (1–9; Qt 5, Ql 4, Mx 3). Every paper states a gap in the Introduction. 30/49 restate it at the end of the review, and 15/49 in a present-study section.
- **Types** (papers using each):

  | Gap type | Pooled | E | T | Qt | Ql | Mx |
  |---|---|---|---|---|---|---|
  | Absence ("little is known about [X]") | 42 | 14 | 28 | 18 | 13 | 11 |
  | Focus–neglect contrast ("research has primarily focused on [A]") | 28 | 6 | 22 | 10 | 10 | 8 |
  | Practical problem rather than a research gap | 23 | 6 | 17 | 5 | 10 | 8 |
  | Weak methods of prior studies | 20 | 6 | 14 | 10 | 4 | 6 |
  | Population or context not studied | 17 | 7 | 10 | 6 | 8 | 3 |
  | Mixed findings | 9 | 3 | 6 | 6 | 1 | 2 |
  | Unclear mechanism | 8 | 3 | 5 | 6 | 1 | 1 |
  | Generalisability | 4 | 1 | 3 | 3 | 0 | 1 |

- **Gap words** ("little is known", "few studies", "remains unclear", "underexplored", "scarce", "dearth"…) appear in 35/50 papers, at a median of 2.7 per 10,000 words of main prose (p90 7.6, max 15.5).

**Aims and the "present study"** (49 papers)

| Measure | Pooled | E | T | Qt | Ql | Mx | Design test |
|---|---|---|---|---|---|---|---|
| Aims first stated at the end of the Introduction | 27 | 8 | 19 | 10 | 13 | 4 | p = .010 |
| … in a separate "present / current study" section | 17 | 5 | 12 | 10 | 0 | 7 | |
| Has a present-study section or subsection | 24 | 8 | 16 | 13 | 2 | 9 | p = .003 |
| Numbered research questions | 25 | 6 | 19 | 4 | 11 | 10 | p < .001 |
| RQs plus hypotheses / aims plus hypotheses | 12 / 4 | 6 / 2 | 6 / 2 | 12 / 4 | 0 / 0 | 0 / 0 | |
| Number of RQs (median) | 2 (0–4) | 2 | 2 | 2 | 2 | 3 | |
| Aim stated in the first person | 30 | 7 | 23 | 17 | 5 | 8 | p = .015 |
| Design previewed in the Introduction | 40 | 10 | 30 | 17 | 10 | 13 | |
| Theory named in the Introduction | 37 | 9 | 28 | 16 | 11 | 10 | |
| Explicit contribution claim | 30 | 6 | 24 | 13 | 9 | 8 | tier p = .059 |
| Novelty claim (first study, to our knowledge) | 10 | 1 | 9 | 5 | 2 | 3 | |
| Roadmap of the article | 7 | 0 | 7 | 2 | 3 | 2 | |

**Paragraph construction (218 paragraphs; % of paragraphs)**

| Measure | Pooled | E | T | Qt | Ql | Mx |
|---|---|---|---|---|---|---|
| Opens: cited claim / aim / own claim / research as subject / gap | 26 / 19 / 17 / 14 / 8 | 28 / 15 / 17 / 13 / 13 | 25 / 20 / 16 / 15 / 6 | 26 / 21 / 13 / 15 / 10 | 30 / 16 / 12 / 16 / 9 | 22 / 18 / 28 / 10 / 4 |
| Opens with a named author as subject | 2 | 0 | 3 | 2 | 2 | 4 |
| Ends: evidence / aim / gap / specific inference | 35 / 24 / 15 / 11 | 40 / 23 / 23 / 7 | 34 / 24 / 12 / 13 | 33 / 28 / 16 / 12 | 39 / 20 / 12 / 11 | 36 / 20 / 16 / 10 |
| Ends: contribution / transition | 6 / 5 | 3 / 3 | 7 / 5 | 5 / 3 | 6 / 6 | 8 / 6 |
| Ends on a generic value sentence | 1.8 (4 of 218) | 0 | 2.5 | 1.0 | 3.1 | 2.0 |

### 2.2 Literature review, theoretical background and hypotheses (50 papers; 542 review and 63 present-study paragraphs)

| Measure | Pooled | E | T | Qt | Ql | Mx |
|---|---|---|---|---|---|---|
| Review words | 1,585 (332–3,887) | 1,383 | 1,649 | 1,865 | 1,571 | 1,400 |
| Review paragraphs | 10 (2–27) | 9 | 12 | 12 | 10 | 8 |
| Subsections | 3 (0–16) | 3 | 3 | 3.5 | 3 | 2 |
| Organisation: thematic / single block / framework then evidence / by construct / by hypothesis | 20 / 9 / 9 / 7 / 5 | 4 / 2 / 2 / 4 / 3 | 16 / 7 / 7 / 3 / 2 | 6 / 2 / 3 / 6 / 5 | 10 / 3 / 2 / 0 / 0 | 4 / 4 / 4 / 1 / 0 |
| Names at least one theory or framework | 44 | 14 | 30 | 20 | 13 | 11 |
| Gap restated at the end of the review | 35 | 8 | 27 | 14 | 11 | 10 |
| Citation instances / 1,000 words | 23.8 (5.7–41.7) | 25.5 | 22.2 | 23.9 | 23.4 | 23.4 |
| % sentences with a citation | 59.5 (16–100) | 63.7 | 54.7 | 59.9 | 54.8 | 60.7 |
| % narrative citations | 13.6 (0–61.5) | 11.8 | 15.4 | 13.1 | 24.4 | 10.3 |
| % parentheses with ≥3 works | 11.8 (0–75.8) | 17.9 | 10.0 | 11.2 | 19.4 | 10.5 |
| % parentheses with ≥2 works | 33.3 (0–88) | 45.2 | 30.4 | 34.8 | 33.3 | 30.8 |
| Present-study section: words / citations per 1,000 / we per 1,000 | 249 / 5.4 / 9.5 | 178 / 0 / 0 | 264 / 6.3 / 11.6 | 392 / 6.5 / 11.8 | 89 / 0 / 0 | 201 / 6.1 / 8.8 |

**Synthesis vs listing.**
- Per paper: a median of 16.5 synthesis sentences (claims across ≥2 studies or about the field) and 8.5 single-study sentences.
- Synthesis share is 63% (22–93%; Qt 70, Ql 59, Mx 59).
- Runs of ≥3 consecutive single-study sentences:
  - once or more in 34/50 reviews;
  - twice or more in 16/50, most often in qualitative papers (Ql 9/15, Qt 6/22, Mx 1/13; p = .011).

**Citation form and verbs.**
- **Information-prominent citations dominate:** narrative citations are a median of 14% of review citations and 0% of Introduction citations. They are more common in qualitative papers (24% in reviews, 25% of all main-prose citations; design p = .06).
- **The verb right after a narrative citation** (217 identified): past 60%, present 34%, present perfect 6%. The past share is E 73%, T 55%. *Found* is the most common verb.
- **The first finite verb of a cited sentence** is past in:
  - 5–10% of Introduction and review sentences that carry a parenthetical citation;
  - 17–18% in the Discussion;
  - about half of sentences built on a narrative citation.

**Counter-evidence.**
- 36/50 reviews present at least one contrary or mixed finding (median 1, 0–9).
- This is now clearly design-dependent: Qt 21/22, Ql 8/15, Mx 7/13 (p = .006). The E 14/15 vs T 22/35 difference (p = .04) is mostly this design mix.
- Devices, as in the 31-paper version:
  - an adversative turn to a named study ("However, [Author] reported …");
  - pairing ("while [A] found …, [B] …");
  - labelling the evidence as "mixed / inconsistent";
  - concession ("although [consensus], [exception]").

**Paragraph construction (605 review and present-study paragraphs; %)**

| Measure | Pooled | E | T | Qt | Ql | Mx |
|---|---|---|---|---|---|---|
| Opens: cited claim / own claim / research as subject / definition / theory | 21 / 19 / 13 / 12 / 9 | 28 / 11 / 14 / 18 / 7 | 19 / 22 / 13 / 10 / 9 | 21 / 20 / 11 / 17 / 6 | 21 / 14 / 18 / 9 / 11 | 21 / 21 / 12 / 3 / 11 |
| Opens with a named author as subject | 6 | 6 | 7 | 4 | 10 | 7 |
| Ends: evidence / specific inference / aim / gap | 44 / 19 / 11 / 8 | 45 / 14 / 10 / 10 | 44 / 21 / 11 / 8 | 42 / 18 / 10 / 8 | 45 / 20 / 9 / 9 | 49 / 20 / 17 / 8 |
| Ends: hypothesis / transition | 8 / 6 | 12 / 4 | 6 / 8 | 15 / 6 | 0 / 9 | 0 / 4 |
| Ends on a generic value sentence | 1.3 (8 of 605) | 1.8 | 1.1 | 0.3 | 4.1 | 0 |

**Hypotheses.** 20/50 papers state hypotheses: 19 of 22 quantitative, 1 mixed, no qualitative paper (E 9, T 11).

| Measure (n = 20) | Pooled | E (9) | T (11) |
|---|---|---|---|
| Hypotheses per paper | median 3 (1–17) | 2 | 3 |
| Labels: prose / H1–H1a / "Hypothesis 1" | 11 / 6 / 3 | 4 / 3 / 2 | 7 / 3 / 1 |
| Placement: present-study section (prose 9, list 2) / end of each review subsection / mixed / Introduction | 11 / 6 / 2 / 1 | 4 / 3 / 1 / 1 | 7 / 3 / 1 / 0 |
| Derivation of 96 hypotheses: theory + evidence / theory only / evidence only / none | 64% / 24% / 9% / 3% | 58 / 32 / 8 / 3% | 67 / 19 / 10 / 3% |

Lead-ins are short and formulaic: "Based on [X], we hypothesize that"; "we expected [X] to …".

### 2.3 Results prose (brief)

| Measure | Pooled | E | T | Qt | Ql | Mx |
|---|---|---|---|---|---|---|
| Results words | 1,538 (597–7,317) | 1,401 | 1,548 | 1,130 | 2,989 | 1,701 |
| Sentence length, median words | 22 (15–30) | 22 | 22 | 23.2 | 22 | 22 |
| % sentences with a number | 41 (0–81) | 56 | 40 | 56 | 12 | 42 |
| Numbers per number-bearing sentence (Qt/Mx) | 2 (1–5) | 2 | 1.8 | 2 | — | 1 |
| % statistic expressions inside parentheses (25 papers with ≥10 statistics) | 100 (0–100) | 100 | 100 | 97 | — | 100 |

**Paragraph openings** (1,116; % within design)

| Opening | Qt (256) | Ql (604) | Mx (256) |
|---|---|---|---|
| Aim or procedure ("To test H1, we …") | 32 | 1 | 14 |
| Finding stated in words first | 27 | 3 | 14 |
| Table or figure pointer | 18 | 1 | 3 |
| Checks (fit, assumptions, descriptives) | 12 | 0 | 1 |
| Theme claim | — | 62 | 45 |
| Participant quote | — | 21 | 15 |
| Opens with a number or statistic | 3 | 1 | 1 |

- Within design, the earlier and top tiers are alike, e.g. quantitative procedure-first openings 29% (E) vs 34% (T).
- Mixed papers differ by tier because the round-2 mixed papers are more quantitative: top-tier mixed papers open 38% theme, 19% procedure, 17% finding.
- Statistics follow the verbal claim. Five of 25 papers (EN12, EN14, EN18, EN49, EN50) mostly set them off with commas, which APA allows.

### 2.4 Discussion (49 papers with a discussion; 354 paragraphs; 226 points)

| Measure | Pooled | E | T | Qt | Ql | Mx |
|---|---|---|---|---|---|---|
| Words | 1,024 (169–2,843) | 858 | 1,128 | 975 | 1,097 | 908 |
| Paragraphs | 6 (2–19) | 5 | 8 | 6 | 8 | 6 |
| Paragraph length, words | 156 (84–251) | 146 | 158 | 155 | 160 | 146 |
| Points per paper | 4 (1–13) | 4 | 4 | 4 | 5 | 4 |
| Citation instances / 1,000 words | 11.4 (0–25.9) | 13.7 | 11.0 | 10.8 | 13.9 | 11.0 |
| % sentences with a citation | 27 (0–54.5) | 30.4 | 24.3 | 27.3 | 34.1 | 24.3 |
| % narrative citations | 16.7 (0–90) | 20 | 14.6 | 2.5 | 33.3 | 16.2 |
| Citations per point | median 2 (IQR 1–4); 29/218 points have none | 2 | 2 | 2 | 2 | 2 |
| % sentences with a number | 2.9 (0–31) | 2.4 | 3.1 | 4.4 | 3.5 | 2.4 |
| we/our/us per 1,000 | 6.1 (0–23.5) | 6.1 | 6.2 | 9.7 | 3.5 | 5.5 |

**Opening and subheadings.**
- **Opening move:** aim plus a summary of the findings 19; aim restated 15; straight into the first point 9; summary of all findings 6.
  - Quantitative papers prefer to restate the aim (12/22).
  - Qualitative and mixed papers more often go straight to the first point (9/28).
- 29/50 open with a separate summary paragraph.
- **Subheadings:** none 23, topic labels 21, claim headings 4, RQ or hypothesis labels 2.

**Inside a point (226 points; %)**

| Feature | Pooled | E | T | Qt | Ql | Mx |
|---|---|---|---|---|---|---|
| Opens by restating the finding | 98 | 98 | 98 | 98 | 97 | 98 |
| … with a statistic | 9 | 7 | 10 | 9 | 4 | 15 |
| Restated finding carries a modal or adverb hedge | 4 | 3 | 4 | 5 | 4 | 2 |
| Compared with cited prior work | 73 | 78 | 71 | 69 | 75 | 75 |
| … consistent only / both / inconsistent only | 53 / 15 / 4 | 59 / 15 / 3 | 50 / 16 / 5 | 43 / 20 / 6 | 62 / 10 / 3 | 54 / 15 / 5 |
| Explained (any explanation) | 75 | 58 | 81 | 81 | 70 | 73 |
| … mechanism / context / named theory / method | 32 / 18 / 17 / 8 | 29 / 14 / 5 / 10 | 33 / 19 / 21 / 8 | 40 / 12 / 15 / 14 | 23 / 20 / 19 / 8 | 32 / 22 / 17 / 2 |
| Names a theory or framework | 32 | 17 | 38 | 33 | 34 | 29 |
| Restate + compare + explain | 51 | 41 | 55 | 53 | 47 | 54 |
| Explanation hedged (of explained points) | 73 | 74 | 73 | 80 | 67 | 67 |
| Null, contrary or unexpected result | 30 | 29 | 30 | 50 | 15 | 19 |
| … stated, then explained (of these) | 69 | 65 | 70 | 68 | 83 | 55 |
| Implication given inside the point | 27 | 19 | 31 | 16 | 41 | 27 |
| Ends: specific interpretation / finding / evidence / implication / future / generic | 36 / 15 / 16 / 12 / 11 / 4 | 36 / 17 / 17 / 3 / 12 / 5 | 36 / 14 / 16 / 16 / 10 / 3 | 40 / 12 / 16 / 8 / 16 / 2 | 32 / 14 / 18 / 18 / 8 / 6 | 36 / 19 / 15 / 12 / 7 / 2 |

**Tier difference.** At paper level, points with an explanation are E 67% vs T 84% (p = .008), and points naming a theory E 0% vs T 35% (p = .011). The direction holds within each design: within quantitative papers, explanation runs E 67% vs T 100% (p = .02).

**Design differences.** At paper level:
- null or contrary points are a median of 46% in quantitative papers, 6% in qualitative and 0% in mixed (p < .001);
- implications inside a point are Qt 0%, Ql 29%, Mx 20% (p = .03).

**Paragraph construction (354 paragraphs; %).**
- First sentences restate a finding in 60% of paragraphs (Ql 70, Qt 51), make the writer's own claim in 14% and restate the aim in 10%.
- Last sentences:

  | Ending | Pooled | Ql | Qt |
  |---|---|---|---|
  | Specific inference | 30 | — | — |
  | Finding | 23 | — | — |
  | Evidence | 14 | — | — |
  | Implication | 10 | 15 | 6 |
  | Future direction | 8 | — | — |
  | Transition | 5 | — | — |
  | Generic value sentence | 3.1 (11 paragraphs in 8 papers) | 5.2 | 1.9 |

### 2.5 Implications, limitations and conclusion

| Measure | Pooled | E | T | Qt | Ql | Mx |
|---|---|---|---|---|---|---|
| Implications in their own section (papers) | 17 | 7 | 10 | 8 | 4 | 5 |
| Implication items | 5 (1–12) | 5 | 5 | 4 | 5 | 6 |
| Numbered items / separate theory-contribution section | 4 / 7 | 2 / 3 | 2 / 4 | 2 / 5 | 1 / 1 | 1 / 1 |
| Items anchored to a finding: explicit / implicit / generic (251 items) | 43 / 43 / 14% | 35 / 42 / 23 | 47 / 44 / 10 | 44 / 38 / 18 | 42 / 47 / 11 | 43 / 46 / 11 |
| Strongest directive: should / must / can / need to / other | 21 / 6 / 4 / 3 / 16 | 6 / 5 / 2 / 1 / 1 | 15 / 1 / 2 / 2 / 15 | 8 / 3 / 2 / 2 / 7 | 5 / 3 / 1 / 0 / 6 | 8 / 0 / 1 / 1 / 3 |
| Implication paragraphs ending on a concrete action / contribution / specific claim / future / generic (%) | 52 / 12 / 10 / 8 / 6 | 58 / 15 / 8 / 8 / 10 | 49 / 10 / 11 / 8 / 4 | 50 / 17 / 8 / 4 / 13 | 49 / 5 / 14 / 14 / 0 | 62 / 8 / 8 / 8 / 0 |
| Limitations: own section / in conclusion / final paragraph of discussion / scattered / absent | 31 / 8 / 7 / 3 / 1 | 12 / 1 / 2 / 0 / 0 | 19 / 7 / 5 / 3 / 1 | 15 / 1 / 5 / 1 / 0 | 9 / 4 / 1 / 1 / 0 | 7 / 3 / 1 / 1 / 1 |
| Distinct limitations | 4 (0–8) | 4 | 4 | 5 | 2 | 4 |
| Limitations paired with a future direction (pooled) | 107/208 = 51% | 62% | 47% | 60% | 45% | 40% |
| Papers answering ≥1 limitation with a mitigating fact | 39/50 | 10/15 | 29/35 | 19/22 | 12/15 | 8/13 |
| Limitations numbered First, Second … | 17/50 | 7 | 10 | 12 | 2 | 3 |
| Limitations words | 283 (75–1,430) | 297 | 277 | 491 | 175 | 277 |
| Limitation paragraphs ending on future / limitation / mitigation / generic (%) | 55 / 18 / 14 / 5 | 59 / 15 / 12 / 6 | 54 / 19 / 14 / 5 | 59 / 20 / 10 / 3 | 49 / 14 / 20 / 9 | 54 / 19 / 15 / 8 |
| Conclusion present | 39/50 | 11/15 | 28/35 | 15/22 | 15/15 | 9/13 |
| Conclusion words | 154 (28–1,089) | 208 | 147 | 141 | 230 | 160 |
| Conclusion's final sentence: generic / implication / future / contribution / finding (of 39) | 12 / 11 / 8 / 4 / 3 | 3 / 3 / 3 / 1 / 1 | 9 / 8 / 5 / 3 / 2 | 4 / 6 / 2 / 2 / 0 | 6 / 4 / 4 / 1 / 0 | 2 / 1 / 2 / 1 / 3 |
| Last sentence of the paper: implication / future / generic / contribution / other | 15 / 14 / 13 / 3 / 5 | 4 / 5 / 3 / 1 / 2 | 11 / 9 / 10 / 2 / 3 | 10 / 5 / 4 / 2 / 1 | 3 / 4 / 6 / 0 / 2 | 2 / 5 / 3 / 1 / 2 |

- **Design test for limitation numbering:** p = .02.
- **Design test for conclusion present:** p = .054.
- **Limitation formula.** Most limitation units open with a formula of the type "This study has several limitations".
- **Actors.** Implications address teachers and educators most often, then researchers, institutions and policy makers.
- **Generic value sentences in the conclusion.**
  - They are common only in the conclusion: 26% of conclusion paragraphs (17 of 66, in 14 papers).
  - In every other unit they stay at or below 6%.
  - The last sentence of the paper is generic in 13/50 (Ql 6/15, Qt 4/22).

### 2.6 Sentence level

**By section** (median of per-paper values)

| Unit | Sentence length | % >40 words | % passive | we/our/us per 1,000 | Abbreviations per 1,000 |
|---|---|---|---|---|---|
| Introduction | 30.5; E 31.5, T 28.8 | 20 | 24 | 3.0; Qt 3.7, Ql 0, Mx 4.2 | 14.6 |
| Review | 27.2 | 15.7 | 27; Mx 42 | 1.2 | 9.7 |
| Present study | 22.5 | 8 | 20 | 9.5 | 21 |
| Results | 22; Qt 23.2 | 10.5 | 20.5 | 5.2; Qt 7.7 | 11.4 |
| Discussion | 26.5 | 12.7 | 22 | 6.1; Qt 9.7, Ql 3.5 | 10 |
| Implications | 25.5 | 12.5 | 16 | 4.0 | 7.5 |
| Limitations | 24 | 10 | 32 | 9.3 | 9.9 |
| Conclusion | 26 | 11 | 12.5 | 6.2 | 9.8 |

**All main prose** (pooled median (range); then E, T, Qt, Ql, Mx medians)

| Measure | Pooled | E | T | Qt | Ql | Mx |
|---|---|---|---|---|---|---|
| Sentence length | 27 (22–33) | 27 | 27 | 26.5 | 27 | 27 |
| % sentences > 40 words | 15.3 (2.7–31.6) | 16.9 | 14.9 | 14.1 | 15.4 | 18.3 |
| % passive | 24.2 (10–45.6) | 29.1 | 23.4 | 25.3 | 22.0 | 31.9 |
| we/our/us per 1,000 | 4.8 (0–18.1) | 3.4 | 5.7 | 6.2 | 3.9 | 3.1 |
| Abbreviations per 1,000 | 10.1 (1.1–63.5) | 17.9 | 8.8 | 9.2 | 20.0 | 8.6 |

**Other measures**
- **Paragraph length.** Median 138 words (83–228).
- **Paragraph-initial connectives.** 17% of paragraphs (0–43; Qt 22, Ql 11, Mx 20) start with one, most often *while, although, moreover, furthermore, despite, however*.
- **First person.**
  - *I* appears only in single-author papers (EN16, EN15).
  - Eight papers stay below 1 *we* per 1,000 words (3 qualitative, 3 mixed, 2 quantitative).

**Stock phrases and AI-typical words** (per 10,000 words of main prose; 218,675 words; at 4,000 words, one occurrence = 2.5 per 10,000)

| Phrase | Pooled rate | Per-paper median (E / T) | p90 | Max | Papers using (E/T) |
|---|---|---|---|---|---|
| however | 15.3 | 13.8 (14.3 / 13.1) | 29.7 | 43.3 | 50 (15/35) |
| thus | 7.3 | 5.0 (3.6 / 5.0) | 21.4 | 40.6 | 37 |
| therefore | 6.6 | 5.1 (6.2 / 4.6) | 13.1 | 30.6 | 47 |
| highlight(s/ed) | 6.6 | 4.5 (3.3 / 5.6) | 17.3 | 34.5 | 37 |
| foster | 4.8 | 3.1 | 12.6 | 19.9 | 39 |
| moreover | 4.3 | 2.6 (5.3 / 2.0) | 11.6 | 20.5 | 31 (12/19) |
| furthermore | 3.8 | 2.4 | 11.0 | 19.7 | 32 |
| essential | 3.8 | 2.5 | 9.2 | 15.9 | 30 |
| crucial | 3.7 | 2.4 | 8.0 | 20.0 | 34 |
| additionally | 3.3 | 2.2 (0 / 2.9) | 8.1 | 15.8 | 27 (6/21) |
| "[valuable/new] insights", "provide insights" | 3.3 | 2.1 | 10.0 | 25.9 | 29 |
| in addition | 3.2 | 2.6 | 8.7 | 24.9 | 33 |
| it is important to / it should be noted | 2.9 | 2.8 | 6.3 | 11.3 | 34 |
| comprehensive | 2.1 | 0 | 6.7 | 10.0 | 23 |
| navigate | 1.7 | 0 | 4.3 | 16.2 | 19 |
| play a [crucial/key …] role | 1.6 | 0 | 4.1 | 9.8 | 21 |
| nuanced | 1.6 | 0 | 4.1 | 9.5 | 23 |
| notably | 1.5 | 0 | 4.0 | 8.6 | 17 (3/14) |
| underscore(s) | 1.4 | 0 | 3.9 | 8.6 | 19 |
| robust | 1.4 | 0 | 3.6 | 25.9 | 15 |
| fill / address / bridge a gap | 1.4 | 0 | 4.5 | 18.8 | 16 |
| novel / importantly | 1.0 / 1.0 | 0 | 4.1 / 4.3 | 7.8 / 8.2 | 15 / 14 |
| holistic / multifaceted | 0.9 / 0.8 | 0 | 3.2 / 3.6 | 9.4 / 7.8 | 10 / 10 |
| to the best of our knowledge / the first (study) to | 0.7 / 0.7 | 0 | 1.8 / 2.8 | 6.1 / 5.0 | 11 / 12 |
| interestingly / landscape / leverage / vital / pivotal / intricate / shed light on | 0.5–0.6 | 0 | 2.0–2.9 | 4.7–11.6 | 8–9 each |
| a growing body of / noteworthy / it is worth noting / delve | 0.3–0.4 | 0 | 0–1.8 | 3.4–6.7 | 4–7 |
| in conclusion / pave the way / in today's / paramount / realm / garnered attention | 0.1–0.2 | 0 | 0 | 2.1–4.4 | 2–4 each |
| Signposting (in this section, the remainder of the paper …) | — | 0 | 3.5 | 8.0 | 18 |

Composite indices per paper (per 10,000 words):
- **AI-typical words** (24 items): median 17.9 (5.0–86.3; E 20.0, T 16.9; Qt 20.2, Ql 16.1, Mx 16.9). Highest: EN42 86, EN07 82, EN22 65.
- **Additive connectors** (*furthermore, moreover, additionally, in addition*): median 13.4 (0–41). This differs by design: Qt 14.3, Ql 8.4, Mx 15.3 (p = .037).
- **Rare phrases** (*delve, in today's, pave the way, a growing body of, it is worth noting, noteworthy, realm, in conclusion, paramount, garnered attention*): median 1 occurrence in total per paper, max 3.

## 3. Stability check (n = 50)

How to read the table:
- Medians are per paper, with 95% bootstrap CIs. "±" is the CI half-width as a share of the estimate; the column v31 gives the same quantity for the 31-paper sample.
- δ is Cliff's delta for E vs T (positive means E higher), with its Mann–Whitney p.
- The design column gives the Qt / Ql / Mx medians and the Kruskal–Wallis p.

| Measure | Pooled median [95% CI] | p90 [95% CI] (±; v31 ±) | E vs T: medians, δ (p) | Qt / Ql / Mx (p) | Verdict |
|---|---|---|---|---|---|
| Sentence length, main | 27.0 [25.8, 28.0] | 30.1 [29.0, 32.0] (±5%; v31 ±4%) | 27.0 vs 27.0, +.06 (.77) | 26.5 / 27 / 27 (.60) | Stable in centre and tail |
| % sentences > 40 words | 15.3 [13.9, 17.3] | 21.1 [19.2, 28.2] (±21%; ±24%) | 16.9 vs 14.9, +.18 (.33) | 14.1 / 15.4 / 18.3 (.14) | Median stable; the 31-paper tier difference disappeared; tail not yet stable |
| Paragraph length, main | 138 [125, 146.5] | 188 [163, 196] (±9%) | 141 vs 136, +.15 (.41) | 133 / 136 / 144 (.82) | Stable |
| Introduction citations / 1,000 | 23.0 [22.1, 24.6] | 33.3 [28.9, 36.0] (±11%; ±9%) | 25.1 vs 22.8, +.13 (.49) | 22.1 / 23.1 / 24.1 (.44) | Stable |
| Review citations / 1,000 | 23.8 [21.5, 25.8] | 32.9 [30.2, 37.3] (±11%; ±12%) | 25.5 vs 22.2, +.31 (.10) | 23.9 / 23.4 / 23.4 (.96) | Stable; T slightly lower |
| Review % sentences cited | 59.5 [53.6, 63.5] | 81.3 [71.6, 89.6] (±11%; ±11%) | 63.7 vs 54.7, +.30 (.12) | 59.9 / 54.8 / 60.7 (.62) | Stable |
| Review % narrative citations | 13.6 [10.6, 21.9] | 39.2 [30.7, 51.6] (±27%; ±35%) | 11.8 vs 15.4, −.10 (.60) | 13.1 / 24.4 / 10.3 (.06) | Tail improving but unstable; higher in qualitative papers |
| Review % parentheses with ≥3 works | 11.8 [8.8, 19.4] | 34.1 [26.7, 61.0] (±50%; ±26%) | 17.9 vs 10.0, +.11 (.56) | 11.2 / 19.4 / 10.5 (.65) | Unstable (two papers at 75%) |
| Discussion citations / 1,000 | 11.4 [9.4, 13.9] | 19.5 [15.6, 22.7] (±18%; ±15%) | 13.7 vs 11.0, +.20 (.27) | 10.8 / 13.9 / 11.0 (.41) | Median stable; tail borderline |
| Discussion citations per point | 2.0 [2.0, 3.0] | 5.3 [4.0, 8.0] (±38%; ±31%) | 2.0 vs 2.0, −.14 (.46) | 2 / 3 / 2 (.34) | Median stable; tail unstable |
| Points compared with cited work (%) | 75 [66.7, 85.7] | 100 | 83 vs 75, +.14 (.44) | 69 / 85 / 80 (.43) | Stable |
| Points explained (%) | 75 [66.7, 92.3] | 100 | 67 vs 84, −.47 (.008) | 75 / 73 / 78 (.56) | Robust tier difference |
| Points naming a theory (%) | 33 [20, 37.5] | 76 [56, 100] | 0 vs 35, −.45 (.011) | 29 / 38 / 20 (.55) | Robust tier difference |
| Generic closings, % of paragraphs | 3.5 [0, 4.5] | 9.2 [6.2, 12.5] (±34%; ±31%) | 4.2 vs 3.2, +.12 (.50) | 1.6 / 5.0 / 0 (.008) | Design-dependent; tail unstable |
| we/our/us per 1,000 | 4.8 [3.0, 6.5] | 12.3 [10.2, 14.8] (±19%; ±11%) | 3.4 vs 5.7, −.23 (.21) | 6.2 / 3.9 / 3.1 (.29) | Tier difference no longer significant; tail ±19% |
| % passive sentences | 24.2 [21.9, 28.1] | 38.2 [34.0, 41.6] (±10%; ±11%) | 29.1 vs 23.4, +.24 (.18) | 25.3 / 22.0 / 31.9 (.09) | Stable |
| AI-typical word index / 10,000 | 17.9 [14.5, 24.3] | 50.8 [37.2, 67.1] (±29%; ±29%) | 20.0 vs 16.9, +.06 (.74) | 20.2 / 16.1 / 16.9 (.84) | Tail unstable |
| Additive connectors / 10,000 | 13.4 [9.7, 16.2] | 26.0 [21.3, 39.3] (±35%; ±26%) | 17.8 vs 13.1, +.18 (.31) | 14.3 / 8.4 / 15.3 (.037) | Design-dependent; tail unstable |
| Abbreviations / 1,000 | 10.1 [7.5, 17.9] | 35.8 [29.5, 39.3] (±14%; ±33%) | 17.9 vs 8.8, +.23 (.21) | 9.2 / 20.0 / 8.6 (.21) | p90 now stable; median topic-driven |
| Results: % sentences with a number | 41 [34.5, 51.8] | 68 [58.6, 75.6] (±12%) | 55.6 vs 40.4, +.33 (.07) | 56 / 12 / 42 (< .001) | Design-specific |
| Results openings: finding or theme (%) | 48 [33, 56.5] | 83 | 50 vs 47 | 25 / 65 / 53 (< .001) | Design-specific |
| Results openings: procedure / pointer / check (%) | 41 [12, 56] | 84 | 45.5 vs 40 | 61 / 2 / 25 (< .001) | Design-specific |

**Verdict**
- **Stable at n = 50 for both the median and the upper tail** (p90 CI within about ±15%):
  - sentence length;
  - paragraph length;
  - Introduction and review citation density and share of cited sentences;
  - passive share;
  - abbreviation density (newly stable);
  - Results sentence length and numeric density, within design.

  Thresholds for these can be set near the published extremes with confidence.
- **Medians stable, tails not:**
  - long sentences (±21%);
  - Discussion citation density (±18%);
  - first person (±19%);
  - narrative-citation share (±27%; improved from ±35%);
  - citations per discussion point (±38%);
  - generic closings (±34%);
  - the AI-word index (±29%);
  - additive connectors (±35%);
  - bundles of three or more works (±50%, worse because two new papers reach 75%);
  - signposting.

  For these, the 50 papers fix the typical value but not where "unusual" begins. Halving these tail intervals would take roughly four times as many papers (about 200), or a stratified design sample. Their flags stay at "beyond the published maximum".
- **Tier differences that survive n = 50.** Top-tier discussions explain their findings and name theories more often (p = .008 and .011, consistent within each design). Contribution claims in the Introduction (E 6/15 vs T 24/34, p = .06) and a roadmap (0/15 vs 7/34, p = .08) lean the same way.
- **Tier differences from the 31-paper version that did not survive:**
  - long sentences (δ .53 → .18) and first person (p .10 → .21), because the new top-tier papers (social-science and qualitative journals) write longer sentences and use less *we*;
  - counter-evidence in the review, which is now explained by design.
- **Design differences large enough to need design-specific guidance** (p < .05 unless noted):

  | Difference | Qt | Ql | Mx |
  |---|---|---|---|
  | Results openings: procedure, pointer or check | 61% | — | — |
  | Results openings: theme or quote | — | 83% | 60% |
  | Results sentences carrying numbers | 56% | 12% | 42% |
  | Research questions and hypotheses | Hypotheses 19/22, numbered RQs 4/21 | Hypotheses 0/15, numbered RQs 11/15 | Hypotheses 1/13, numbered RQs 10/13 |
  | Present-study section | 13/21 | 2/15 | 9/13 |
  | First-person aim | 17/21 | 5/15 | 8/13 |
  | Counter-evidence in the review | 21/22 | 8/15 | 7/13 |
  | Repeated single-study listing (2+ runs) | 6/22 | 9/15 | 1/13 |
  | Narrative citations (p = .06) | 13% | 24% | 10% |
  | Null or contrary results as discussion points (paper median) | 46% | 6% | 0% |
  | Implications inside discussion points (paper median) | 0% | 29% | 20% |
  | Numbered limitations | 12/22 | 2/15 | 3/13 |
  | Distinct limitations (median) | 5 | 2 | 4 |
  | Conclusion section (p = .054) | 15/22 | 15/15 | 9/13 |
  | Generic paragraph endings (share of paragraphs) | 2.8% | 5.8% | 2.5% |
  | Additive connectors per 10,000 | 14.3 | 8.4 | 15.3 |

- **Not design-dependent:** citation density in every section, sentence and paragraph length, restating and comparing in discussion points, explanation rate, hedging location, and *we/our* in main prose (Qt 6.2, Ql 3.9, Mx 3.1 per 1,000; p = .29).
  - First person is design-dependent only in where it appears: the aim statement (above) and the Discussion (Qt 9.7 vs Ql 3.5 per 1,000; p = .18).
  - So it needs design-specific advice, but not a design-specific threshold.

## 4. Writing rules

Each rule gives its supporting numbers first (pooled n = 50 unless stated), then what to do. Slots are in [brackets]. Design-specific variants follow the general rules.

### Introduction

1. **Write 3–5 paragraphs, about 450–800 words, before the first review heading.** Published: median 580 words (180–1,430), 4 paragraphs of about 140 words. Without a separate review section, run to about 1,200–1,400 words.
2. **Open with the phenomenon, trend or practical problem, and usually cite it.** Published:
   - first sentence: trend 16/49, practical problem 9, broad importance 7, state of research 6, definition 5, statistic 0;
   - 32/49 first sentences are cited, and the first move is background in 31/49.

   Do not open with "In today's [world]" or an uncited sweeping claim.
3. **Cite in more than half the sentences, information-prominently.** Published:
   - 23 citations per 1,000 words (8.7–36.5) and 57% of sentences cited;
   - narrative citations 0% (median);
   - one parenthesis in six with three or more works.
4. **State the gap as a specific absence plus a contrast, design weakness or practical problem, and restate it before the aims.** Published:
   - median 4 gap statements (1–9);
   - restated at the end of the review in 30/49;
   - types: absence 42, focus–neglect 28, practical problem 23, method 20, population 17.

   Templates:
   - "Most studies have [examined A]; [B] remains [unexamined]."
   - "Prior work relied on [design], which cannot [show X]."
5. **End on the study: aim, design and contribution.** Published:
   - aims end the Introduction in 27/49 or open a present-study section in 17/49;
   - design preview 40/49; theory named 37/49; first-person aim 30/49;
   - contribution claim 30/49 (T 24/34, E 6/15);
   - roadmap 7/49 (all top tier); novelty claim 10/49.

   Template: "In this study, we [examine X] among [population] using [design] … In doing so, we contribute to [literature] by [specific addition]."
6. **Paragraphs stop on evidence, the aim, the gap or a specific inference, not on a value sentence.** Published:
   - endings: evidence 35%, aim 24%, gap 15%, specific inference 11%; generic 1.8% (4 of 218);
   - a named author as the subject of the first sentence in 2% of paragraphs.

### Literature review and hypotheses

7. **Organise by theme, construct or framework in 2–5 subsections, and name a theory.** Published: median 3 subsections; thematic 20, single block 9, framework then evidence 9, by construct 7, by hypothesis 5; a theory named in 44/50.
8. **Synthesise first; illustrate with single studies; avoid study-by-study listing.** Published:
   - 23.8 citations per 1,000 words and 60% of sentences cited;
   - synthesis to single-study sentences about 2:1 (median 16.5 vs 8.5; 63% synthesis);
   - repeated listing runs in 16/50 papers, mostly qualitative.
9. **Keep author-prominent citations to about one in seven** (qualitative papers up to one in four). Published: median 14% of review citations (Ql 24%). The verb after a narrative citation is past in 60% of cases (*found* most often). Claims with parenthetical citations are in the present or present perfect about 90% of the time.
10. **Quantitative papers: include contrary or mixed evidence; qualitative and mixed papers: include it where the literature is contested.** Published: 36/50 overall; Qt 21/22, Ql 8/15, Mx 7/13. Devices: "However, [Author] reported …", "while [A] found …, [B] …", "findings on [X] are mixed".
11. **Derive each hypothesis from theory plus evidence, then state it in one sentence.** Published:
    - 20/50 papers (19/22 quantitative), median 3 hypotheses;
    - derivation: theory and evidence 64%, theory only 24%, evidence only 9%, none 3%;
    - placement: present-study section 11, end of each review subsection 6;
    - labels: prose 11, H1/H1a 6, "Hypothesis 1" 3.

    Template: "[Theory] holds that [mechanism] ([cites]); [studies] found [pattern] ([cites]). We therefore expected [X] to be positively related to [Y] (H1)."
12. **Review paragraphs end on evidence, a specific inference, the aim or the hypothesis.** Published: evidence 44%, specific inference 19%, aim 11%, gap 8%, hypothesis 8% (Qt 15%); generic 1.3%. Close the review by restating the gap (35/50).

### Results

13. **Lead with the step or the claim; statistics follow it.** Published:
    - quantitative openings: procedure 32%, finding in words 27%, table pointer 18%, checks 12%; a number first 3%;
    - statistics in parentheses (median 100%) or set off by commas (5/25 papers);
    - 56% of quantitative Results sentences carry numbers, median 2 per sentence.

    For qualitative and mixed Results, see the design-specific rules below.

### Discussion

14. **Open by restating the aim, optionally with a one-paragraph summary of findings; then discuss about 4 points.** Published:
    - aim plus summary 19, aim 15, first point 9, summary 6;
    - a summary paragraph in 29/50;
    - median 4 points (1–13);
    - subheadings: none 23/50, topic labels 21/50, claim headings 4/50.
15. **Each point opens by restating the finding in words, unhedged.** Published: 98% of points restate the finding, 9% with a statistic; 4% hedge it; 2.9% of Discussion sentences carry numbers.
16. **Compare each finding with cited studies, including disagreements.** Published:
    - 73% of points compare: consistent 53%, both 15%, inconsistent 4%;
    - median 2 citations per point (IQR 1–4);
    - 11.4 citations per 1,000 words.
17. **Explain each finding, name the theory where possible, and hedge the explanation rather than the finding.** Published:
    - 75% of points explain (top tier 81% of points; per paper E 67% vs T 84%);
    - 32% name a theory (T 38%, E 17%);
    - 73% of explanations are hedged, against 4% of findings;
    - restate, compare and explain together in 51% of points.
18. **Report null and contrary results and give reasons.** Published: 30% of points (Qt 50%); 69% of these are explained, typically by measurement, design or context, and followed by a concrete test.
19. **End points on a specific interpretation, the finding, evidence, an implication or a specific next step.** Published: endings 36 / 15 / 16 / 12 / 11%; generic value sentence 4%. Discussion paragraphs end generic in 3.1%.

### Implications, limitations, conclusion

20. **Write about 5 implications, each tied to a finding and addressed to a named actor.** Published:
    - median 5 items (1–12), rarely numbered (4/50);
    - explicit anchoring 43%, implicit 43%, generic 14% (T 10%);
    - strongest directive *should* in 21/50;
    - 52% of implication paragraphs end on a concrete action, 6% on a generic sentence.

    Template: "Because [finding], [actor] should [action], for example [practice]."
21. **Put the limitations in one place, name each concretely, answer what you can, and pair most with a future design.** Published:
    - a single unit in 46/50 (own section 31);
    - median 4 limitations (Ql 2, Qt 5); 51% paired with a future direction;
    - 39/50 answer at least one limitation with a mitigating fact;
    - 55% of limitation paragraphs end on a future direction.
22. **Keep the conclusion short and end on substance.** Published:
    - conclusion present 39/50, median 154 words;
    - last sentence of the paper: implication 15, future direction 14, generic 13, contribution 3.

    End on an implication or a specific next step. If a closing evaluative sentence is wanted, allow one, as the last sentence of the paper (26% of papers do this).

### Sentences

23. **Median sentence about 27 words; no more than about 1 sentence in 6 over 40 words.** Published: 27 (22–33); 15.3% over 40 words (2.7–31.6). Results run shortest (22) and the Introduction longest (30.5).
24. **Use *we* for the study's actions and decisions, mainly in the present-study, Discussion and limitations sections.** Published: 4.8 per 1,000 words (0–18.1); present study 9.5, limitations 9.3, Discussion 6.1, review 1.2 per 1,000. Impersonal prose is also within range: 8 papers stay below 1 per 1,000.
25. **Keep the passive to about a quarter of sentences.** Published: 24% (10–46); limitations 32%; mixed-methods reviews higher.
26. **Use connectors sparingly; drop AI-typical words.** Published:
    - *however* about 14 per 10,000 words;
    - additive connectors together median 13 per 10,000 (Ql 8);
    - 17% of paragraphs start with a connective;
    - AI-typical words median 18 per 10,000;
    - the rare phrases total 0–3 per paper.
27. **Abbreviate only recurring core constructs.** Published: 10 per 1,000 words (1–63.5).
28. **Little signposting.** Published: none in 32/50 papers; roadmap in 7/49.

### Design-specific rules

- **Quantitative**
  - State hypotheses (19/22), usually in prose in a present-study section, each derived from theory and evidence.
  - Write the aim in the first person (17/21).
  - Include counter-evidence in the review (21/22).
  - Open Results paragraphs with the procedure, the finding, a table pointer or a check.
  - Give null or contrary results their own discussion points (median 46% of points).
  - Number the limitations if there are several (12/22; median 5).
- **Qualitative**
  - Use numbered RQs (11/15) at the end of the Introduction (13/15). No present-study section is needed (2/15), and no hypotheses.
  - Results paragraphs open with a theme claim (62%), then evidence and quotes (21% open with a quote). Numbers are rare (12% of sentences).
  - Discussion points may end on an implication (41% of points contain one).
  - Narrative citations may run to about a quarter of citations.
  - The limitations unit is usually short (median 2 limitations).
  - Always write a conclusion (15/15).
  - Keep generic closings rare (they are already more frequent here: 5.8% of paragraphs).
- **Mixed**
  - Use numbered RQs (10/13) in a present-study section (9/13).
  - Results alternate theme-led and procedure- or finding-led paragraphs (theme 45%, procedure 14%, finding 14%, quote 15%).
  - Discussion as for qualitative papers, with implications inside points (median 20%).

### Structural templates

- **Introduction (4 paragraphs)**
  1. [Trend or problem, cited] → [why it matters, cited].
  2. [What research has established, synthesis] → [one or two specific findings].
  3. [However, most studies have (A); (B) remains (unexamined), cited] → [why that matters here].
  4. [In this study, we (aim) in (context) using (design)] → [RQs or hypotheses, or "see Present study"] → [We contribute to (literature) by (specific addition)].
- **Review subsection that builds a hypothesis (quantitative):** [definition or theory, cited] → [mechanism: According to (theory) …] → [evidence: studies show (A; B; C); (Author) (year) found …] → [counter-evidence] → [Based on (theory and evidence), we hypothesize that … (H1)].
- **Present-study section (quantitative and mixed):** gap recap → aim and design in the first person → RQs and hypotheses → exploratory question if any.
- **Results paragraph, quantitative:** [To test H1, we …] → [X was related to Y (statistics)] → [robustness check] → [H1 was supported].
- **Results paragraph, qualitative:** [theme claim: Participants described (X) as (Y)] → [one or two quotes with participant codes] → [one interpretive sentence that links the theme to the RQ].
- **Discussion point:** [finding restated in words, unhedged] → [comparison: consistent with A (year); unlike C (year) …] → [hedged explanation, theory named] → [specific inference or implication].
- **Null or contrary point:** [Contrary to H2, X was not related to Y] → [differs from (cites)] → [measurement, design or context reasons] → [the study that would test this].
- **Implication item:** [Because (finding)] → [(actor) should (action)] → [for example, (practice)].
- **Limitation:** [feature] → [inference it limits] → ([mitigating fact]) → [Future studies using (design) could test (question)].
- **Conclusion (1 paragraph):** [aim and main finding] → [contribution] → [main implication] → [specific next step or implication as the final sentence].

## 5. Automatically checkable measures and flag thresholds (n = 50)

How the thresholds were set:
- A threshold from the 31-paper version was kept if it flags at most one of the 50 published papers. Otherwise it was moved to just above the second-highest published value.
- "Flagged" shows how many published papers trigger the flag (denominator = papers to which the measure applies).
- Rates per 10,000 words are noisy in short texts: at 4,000 words of main prose, one occurrence equals 2.5 per 10,000.
- † = needs paragraph-level judgment (an LLM classifier or a human).
- Under these thresholds, 41 of 50 published papers trigger no flag and 3 trigger two or more: EN42 8 flags, EN35 2, EN48 2. EN42 has low citation density, no comparison with prior work and dense AI-typical vocabulary.

| Measure | Published: pooled median (range); E / T; Qt / Ql / Mx | Flag when | Flagged (n = 50) |
|---|---|---|---|
| Sentence length, median words (main) | 27 (22–33); 27 / 27; 26.5 / 27 / 27 | < 20 or > 33 | 0/50 |
| % sentences > 40 words | 15.3 (2.7–31.6); 16.9 / 14.9 | > 30 | 1/50 |
| Paragraph length, median words | 138 (83–228) | < 75 or > 230 | 0/50 |
| Introduction citations / 1,000 words | 23.0 (8.7–36.5) | < 10 | 1/48 |
| Introduction % sentences cited | 57.1 (27–90) | < 25 | 0/48 |
| Review citations / 1,000 words | 23.8 (5.7–41.7) | < 12 | 1/45 |
| Review % sentences cited | 59.5 (16–100) | < 30 | 1/45 |
| Review % narrative citations | 13.6 (0–61.5); Ql 24.4 | > 65 | 0/45 |
| Review % parentheses with ≥ 3 works | 11.8 (0–75.8) | > 75 (was > 45) | 1/45 |
| Discussion citations / 1,000 words | 11.4 (0–25.9) | < 3 | 1/48 |
| Discussion % sentences with a number | 2.9 (0–30.8) | > 35 | 0/49 |
| † Discussion points opening with the restated finding | 100% (67–100) | < 60% of points | 0/49 |
| † Points compared with cited work (papers with ≥ 3 points) | 75% (25–100) | < 25% | 0/45 |
| † Points whose restated finding is hedged | 0% (0–25) | > 30% | 0/49 |
| † Generic value sentence as paragraph ending | 3.5% (0–14.3); Qt 1.6 / Ql 5.0 / Mx 0 | > 15% of paragraphs, or ≥ 3 consecutive | 0/50 |
| Value-phrase paragraph endings (regex proxy) | 5.4% (0–20) | > 25% | 0/50 |
| we/our/us per 1,000 words | 4.8 (0–18.1) | > 17 (was > 16) | 1/50 |
| % sentences with be + participle | 24.2 (10–45.6) | < 8 or > 50 | 0/50 |
| Abbreviation tokens / 1,000 words | 10.1 (1.1–63.5) | > 60 | 1/50 |
| Signposting / 10,000 words | 0 (0–8) | > 10 | 0/50 |
| % paragraphs opening with a connective | 17 (0–43) | > 45 | 0/50 |
| furthermore + moreover + additionally + in addition / 10,000 | 13.4 (0–41) | > 45 | 0/50 |
| AI-typical word index / 10,000 (24 items) | 17.9 (5.0–86.3) | > 85 (was > 70) | 1/50 |
| Rare phrases (delve, in today's, pave the way, a growing body of, it is worth noting, noteworthy, realm, in conclusion, paramount, garnered attention): total count | 1 (0–3) | ≥ 4 | 0/50 |
| Single words per 10,000 (published max) | crucial (20), highlight (34.5), foster (19.9), essential (15.9), insights (25.9), notably (8.6), underscore (8.6), pivotal (5.6), nuanced (9.5), multifaceted (7.8), leverage (6.4), navigate (16.2), robust (25.9), comprehensive (10.0), shed light on (9.6), play a role (9.8), it is important to (11.3) | crucial > 21, highlight > 35, foster > 21, essential > 16, insights > 15, notably > 8, underscore > 8 (was > 6), pivotal > 6, nuanced > 8, multifaceted > 8, leverage > 7, navigate > 8 (was > 7), robust > 9, comprehensive > 10, shed light on > 10, play a role > 10, it is important to > 12 | 1/50 each for insights, notably, underscore, nuanced, navigate and robust; 0/50 for the rest |
| Results: paragraphs opening with a number (Qt and Mx papers) | 0% (0–16) | > 20% | 0/35 |
| Results: numbers per number-bearing sentence (Qt and Mx) | 2 (1–5) | > 6 | 0/35 |
| Results: sentences with a number, qualitative papers | 12% (Ql median) | design check: > 40% in a qualitative paper | — |
| † Implication items with no traceable finding | 0% per paper (0–83) | > 2/3 of items | 1/50 |
| † Hypotheses with no theoretical or empirical argument before them | 3% of hypotheses | more than half of a paper's hypotheses | 1/20 |
| † Gap statement in the Introduction | 50/50 | absent | 0/50 |
| † Aims or RQs stated before Method | 50/50 | absent | 0/50 |
| † Limitations present | 49/50 | absent | 1/50 |
| † Limitations in one unit (advisory) | 46/50 | spread over several sections | 3/50 (advisory, not a flag) |

Use the flags as prompts to revise, not as hard rejections. The writing rules in §4 target the medians, not the thresholds. For measures marked unstable in §3, a flag means "beyond anything published in this corpus", not "unusual".

## 6. Interpretation (not a direct corpus result)

- **English articles carry the argument with citations and comparisons.** About 60% of review sentences carry a citation, and about three-quarters of discussion points are set against named prior studies. AI drafts tend to under-cite and to close paragraphs with evaluations. Rules 3, 8, 16 and 19 target this.
- **Generic value closings are rare outside the conclusion.** They end 1.3–6% of paragraphs elsewhere, against 26% of conclusion paragraphs. Qualitative papers allow a little more (5.8% overall), but a checker can be strict everywhere except the paper's last sentence.
- **Caution sits on explanations, not on findings.** This holds in all designs and both tiers.
- **The tier difference is in interpretive work, not in style.** At n = 50, top-tier papers differ mainly in explaining findings and naming theories, and somewhat in claiming contributions. Sentence length and first person do not separate the tiers once qualitative and social-science journals are included.
- **Design matters more than tier for the shape of the paper:** RQs versus hypotheses, the present-study section, Results paragraphs, null results, and how much limitation and conclusion text there is. The skill should pick the template by design.
- **AI-typical vocabulary already appears in published 2024–2026 papers,** sometimes densely (EN42, EN07, EN22). Single occurrences prove nothing; density and clustering are the signal.

**Comparison with the Chinese corpus** (`writing_moves_zh.md`; comparable measures only)

| Measure | English (50) | Chinese CSSCI (27) |
|---|---|---|
| Discussion points per paper | 4 | 3 |
| Points restating the finding | 98% | 87% |
| Points compared with cited prior work | 73% | 25% (33% including uncited comparisons) |
| Points naming a theory | 32% (T 38%) | 37% |
| Citations per point | 2 | 1.25 |
| Generic paragraph endings: Introduction / review / Discussion / implications or recommendations | 1.8% / 1.3% / 3.1% / 6.2% | 13% / 3% / 8% / 27% |
| Introduction ends on aims, RQs, design, contribution or roadmap (EN) / aims, value or RQs (ZH) | 41/49 | 25/27 |
| Narrative ("Author (year) found") citations in the review | 14% of citations | 8% of cited sentences |

## 7. Changes from the 31-paper version

**Corpus and method**
- 50 papers instead of 31: T 16 → 35; qualitative 8 → 15; mixed 5 → 13.
- Design columns were added throughout.
- A second coder recoded paragraph endings for 10 papers: κ 0.95, GEN κ 0.91.
- Six anchor papers were recoded blind: κ 0.93.
- EN48's Introduction is excluded (extraction gap).

**Rules whose numbers changed (31 → 50)**
- **Introduction.**
  - Median length 529 → 580 words; paragraph range 1–9 → 1–12.
  - Cited first sentence 23/31 (74%) → 32/49 (65%); practical-problem openings 5/31 → 9/49.
  - Gap statements median 5 → 4.
  - Contribution claim tier contrast E 6/15 vs T 13/16 → T 24/34 (p = .06, weaker).
  - Roadmap 4/31 → 7/49, still top tier only.
  - Aims at Introduction end vs present-study section is now design-specific (Ql 13/15 at the end; Qt 13/21 with a present-study section).
  - Generic paragraph endings 1.5% → 1.8%.
- **Review.**
  - Citation density 25.5 → 23.8 per 1,000 words (T 22.2).
  - Narrative share 12% → 14% (Ql 24%).
  - Bundles of three or more works 10% → 12%, maximum 40% → 76%.
  - Verb after a narrative citation: past 67% → 60%.
  - Counter-evidence 23/31 → 36/50 and now design-specific (Qt 21/22, Ql 8/15); rule 10 rewritten.
  - Repeated listing runs 10/31 → 16/50, concentrated in qualitative papers.
  - Generic endings 2.1% → 1.3%.
- **Hypotheses.**
  - 16/31 → 20/50 papers (19/22 quantitative); median 3.5 → 3 per paper.
  - Placement now mostly in a present-study section (11 vs 6 at the end of subsections).
  - Prose labels most common (11/20).
  - Derivation shares unchanged: 63/25/8/3% → 64/24/9/3%.
- **Results.** Mixed-methods openings shift: theme 54% → 45%, procedure 10% → 14%, finding 12% → 14%. Quantitative and qualitative patterns are unchanged. Comma-style statistics 4/19 → 5/25.
- **Discussion.**
  - Words 905 → 1,024; points per paper range 2–8 → 1–13.
  - Citations per point 3 → 2; citations per 1,000 words 13.5 → 11.4.
  - Points compared 76% → 73%.
  - Points explained in the top tier 92% → 81% (E unchanged at 58%); named theory in the top tier 41% → 38%; full restate–compare–explain in the top tier 64% → 55%.
  - Hedged explanations 69% → 73%; hedged findings 2.5% → 4%.
  - Null or contrary points 35% → 30% (now Qt 50%, Ql 15%).
  - Implication inside the point 20% → 27%; points ending on an implication 7.5% → 12%.
  - Most common opening move: aim only → aim plus summary; summary paragraph 14/31 → 29/50.
  - Generic endings 3.0% → 3.1%.
- **Implications.** Explicit anchoring 39% → 43%; generic 19% → 14%; own section 48% → 34% of papers.
- **Limitations.**
  - Own section 71% → 62%; scattered or absent 1 → 4 papers.
  - Paired with a future direction 57% → 51%.
  - Mitigation 25/31 → 39/50.
  - Generic endings 3.5% → 5.3%.
- **Conclusion.**
  - Present 24/31 → 39/50 (Ql 15/15).
  - Generic final sentence 7/24 → 12/39.
  - Paper ends generic 7/31 → 13/50 (26%).
  - Rule 22 now cites implication 15 / future 14 / generic 13.
- **Sentences.**
  - Median sentence 26.5 → 27 words.
  - Long sentences: the tier difference disappeared (T 11.8% → 14.9%; δ .53 → .18). Rule 23 now aims at "1 in 6" instead of "1 in 7".
  - *we* tier difference weakened (T 6.9 → 5.7; p .10 → .21); maximum 13.9 → 18.1.
  - Abbreviations median 15.1 → 10.1.
  - Paragraph-initial connectives 21% → 17%.
  - AI-word index median 20.3 → 17.9 (maximum 82 → 86).

**Stability verdict changes**
- Abbreviation p90 is now stable (±33% → ±14%).
- Narrative-share tail improved (±35% → ±27%), but bundles (±26% → ±50%) and connectors (±26% → ±35%) got worse.
- The "long sentences" and "first person" tier differences are withdrawn.
- The "counter-evidence" tier difference is re-attributed to design.
- The explanation and theory tier differences are confirmed.

**Thresholds changed**
- Review bundles of three or more works: > 45 → > 75.
- *we/our/us*: > 16 → > 17.
- AI-typical word index: > 70 → > 85.
- *underscore*: > 6 → > 8.
- *navigate*: > 7 → > 8.
- "Points compared with cited work" now applies only to papers with three or more points.
- "Limitations in one unit" split into a flag (limitations absent, 1/50) and an advisory (scattered, 3/50). The 31-paper table wrongly reported 0/31 for this flag; EN28 was already scattered.
- Added: a design check for numbers in qualitative Results.
- All other thresholds unchanged.
- Papers that trigger at least one flag under the revised thresholds: EN42 (8), EN35 (2), EN48 (2), and EN03, EN04, EN23, EN37, EN40, EN46 (1 each); the other 41 trigger none.

## 8. Files

- **Summary:** this file.
- **Per-paper records:** `private/writing_moves_en_coding.jsonl` (local, gitignored), 50 lines. EN32–EN50 were appended with `"coding_round": 2` and include per-hypothesis derivations. Each record holds:
  - paragraph codes;
  - section-level fields;
  - discussion points with their citation counts;
  - Results openings;
  - automatic measures by section;
  - excerpts only as fragments of eight words or fewer, or slot templates.
- **Reliability and anchor codings** (second-coder files, anchor recodings, agreement tables) are kept in the session scratchpad with the scripts, not in the repository.
