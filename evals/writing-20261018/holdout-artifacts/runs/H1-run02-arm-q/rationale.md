# Writing rationale and evidence record

## Scope and main line, recorded before the first draft

This is a new, three-section English secondary writing exercise based solely on H1-materials.md, not a manuscript claiming new research. The intended audience is education researchers interested in school policy. The requested body is 600–750 words, excluding references. The requested Markdown deliverables take precedence over the skill's default Word conversion. No target journal, external search, or author confirmation is needed for this direct, bounded request.

**Educational problem:** Changing the timetable matters if students actually obtain additional sleep and if their experiences of attending and performing at school change with it.

**What the evidence answers:** Independent tenth-grade cohorts in two Seattle high schools had longer recorded school-night sleep seven months after a district schedule change. Higher biology grades accompanied the change; school-wide first-period attendance patterns differed descriptively between schools. This is an observational comparison across years, without an unchanged-schedule concurrent group.

**Core judgment and contribution:** Seattle adds an objective observation under an implemented school policy to the prior literature as reviewed by Dunster et al. It makes sleep opportunity a concrete educational scheduling consideration. The evidence for additional recorded sleep is more direct than the evidence identifying how grades changed or who benefited most.

**Scope:** Two public high schools, independent cohorts, comparable grade level, teachers, classes and season. School-wide attendance is not the actigraphy cohort. No causal mediation, socioeconomic interaction, standardized achievement effect, or cost claim is available.

## Evidence supporting and constraining the argument

| Evidence supporting the judgment | Evidence constraining its interpretation |
|---|---|
| Two-week wrist actigraphy checked against diaries and event markers; observations seven months after implementation | Independent annual cohorts; no concurrent unchanged-schedule comparison; source inferential reporting issues unresolved |
| Median school-night sleep differed by 34 minutes; waking was 44 minutes later | Sleep-onset difference did not meet the adjusted threshold; nonschool-night nonsignificance is not equivalence |
| Lower reported sleepiness and reduced social jet lag are consistent with the sleep-opportunity interpretation | Neither is a direct biological clock-phase measure; neither identifies a causal pathway to grades |
| Biology marks were higher; Franklin's school-wide first-period attendance improved | Marks were unstandardized and teachers knew of the change; Roosevelt had no significant attendance changes; no interaction estimate |

Both the positive observations and the relevant constraints belong in the prose. Social jet lag need not be included in this short exercise because explaining the construct would displace the main educational argument.

## Writing-unit and source map

All B locators below are packet locators, not claims of direct access to the article. The only evidentiary source actually read is H1-materials.md. The original article, its cited studies, supplements and raw data were not opened.

| Unit | Function | Claim | Supplied evidence/location | Writing decision and necessary conditions |
|---|---|---|---|---|
| Introduction, paragraph 1 | Motivate the educational question | Early school mornings can conflict with adolescent sleep timing | Background; Introduction B005–B007; Discussion B020 | Attribute the physiology to the source authors' review; explain in ordinary language |
| Introduction, paragraph 2 | Specify the question and design | Ask whether a later start accompanies additional sleep and educational changes | Results B009; Participants B028; Methods | Identify independent cohorts, two schools and timing; no retrofitted hypothesis |
| Discussion, opening | Answer the sleep question and explain the pattern | More school-night sleep accompanied later waking | Results B010–B011, B015; Discussion B019 | Keep median and school-night identity; retain nonsignificance accurately |
| Discussion, literature comparison | State what this field observation adds | Seattle provides objective evidence months after a policy change | Discussion B020, as summarized in packet | Comparisons are Dunster et al.'s review; differences in design are not demonstrated causes of differences in minutes |
| Discussion, grades | Interpret the educational observation | Median biology marks differ by 4.5 percentage points | Figure 3A; B025; B045 | Percentage points, not relative percent; unstandardized marks and teacher awareness qualify the particular interpretation |
| Discussion, attendance | Keep heterogeneity and levels visible | First-period school-wide attendance changed at Franklin; Roosevelt changes were nonsignificant | Figure 3C–D; B017; B046 | No inference of income moderation or narrowed achievement gaps from different significance labels |
| Discussion, final paragraph | Consolidate design limits and practical implication | Cohort/year explanations remain; sleep opportunity warrants attention in scheduling decisions | B028; Discussion B019–B020; packet verification notes | Mention matching features and absence of a concurrent comparison together; no cost-effectiveness claim |
| Conclusion | Answer the same question and specify educational contribution | Sleep opportunity is a supported policy consideration; educational outcomes remain accompanying observations | Same evidence as above | Retain setting and timing; do not transform association into causal improvement |

## Terms

| Preferred term | Meaning and use |
|---|---|
| later school start times / later starts | The timetable change, not a measured biological intervention |
| school-night sleep | Sleep before a school day; keep separate from nonschool-night sleep |
| wrist actigraphy | Wrist recordings used to estimate sleep; explain at first use |
| independent cohorts | Different students sampled in the two years, not repeated measures of the same students |
| biology grades / biology marks | Teachers' unstandardized second-semester marks; never standardized achievement |
| first-period attendance | School-wide absences and tardies during the first period, not all-day or cohort-specific attendance |
| percentage points | Absolute difference between the two grade percentages |

No acronyms are needed. “Dunster et al.” and “the Seattle study” identify the original study. The exercise will not use “we collected” or “our students.”

## Checking and author-query notes

- The packet flags a signed-rank label applied to independent cohorts, differences between Figure 1 and the results text, and inconsistent descriptions of the year-prediction model. These remain unresolved; no test corrections, missing p values, confidence intervals, or reanalysis will be invented. The short prose will emphasize checked descriptive quantities and identify reported significance as such where needed.
- Original studies mentioned in Dunster et al.'s discussion have not been separately read or independently cited. One full supplied reference is sufficient for this exercise. This is not a field-wide literature review.
- No author query blocks this exercise. Any future empirical reanalysis or submission would need the original reporting issues, raw-data access, and source literature checked under a newly authorized task.
- Required checks: check_voice.py with the packet as source, check_prose.py, and check_consistency.py for both drafts. Corpus medians and flag counts are prompts for judgment, not success criteria.
- New writing was requested. The first-to-final revision belongs in review.md and this rationale; a separate change_log.md for revision of a user manuscript is not applicable.

## Final alignment after revision

| Unit | Final action and rationale |
|---|---|
| Introduction | Explained the practical sleep-timing problem without specialist terminology; made different students across years explicit; added the source authors' objective-versus-survey distinction |
| Discussion: sleep | Preserved the main medians and waking shift; retained nonsignificance without inferring unchanged or equivalent sleep; kept the explanatory interpretation attributed |
| Discussion: comparison | Used the two comparisons to distinguish scheduled delay from observed sleep gain; retained unresolved explanations for differences across studies |
| Discussion: grades | Retained 4.5 percentage points and unstandardized biology marks; expressed the measurement scope directly; identified rather than implied the causal-pathway limit |
| Discussion: attendance | Retained school-wide first-period records, both schools and reported significance; connected monitoring to school-specific patterns without an income-effect claim |
| Discussion: overall limits and action | Grouped cohort/year confounding and the absence of a concurrent comparison; identified protecting adolescent sleep as the premise for policy deliberation; left the evening-advice proposal untested |
| Conclusion | Answered the same question with association language; named separate sleep, classroom-mark and first-period attendance outcomes for district evaluation |

The final body is 652 words using whitespace separation, excluding the note, headings and references (654 using the prose checker's tokenizer). All six required draft/check combinations ran successfully and their saved outputs were inspected. The self-review documents decisions on each substantive cue. Final claim scope and source attribution were checked manually; the scripts cannot establish either.
