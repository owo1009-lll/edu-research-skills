# Bibliographic-context encoding correction

The frozen `inputs/D-M02/original.md` was created by extracting the published paragraph from the UTF-8 reading file. That entire 176-word paragraph is intact, including its original punctuation. Its appended bibliographic context was composed through a Windows PowerShell pipeline, which replaced several non-ASCII characters with question marks. The defect was identified after the first two compression writers had started. The frozen input was therefore retained byte-for-byte for all four compression runs and their review; the experiment does not silently substitute an input used by only some writers.

The correct citation is:

Adl-Amini, K., Völlinger, V. A., & Eckart, A. (2024; first published online 2023). *Implementation quality of cooperative learning and teacher beliefs—a mixed methods study*. *European Journal of Psychology of Education, 39*, 2267–2281. https://doi.org/10.1007/s10212-023-00769-3

The affected context contains `V?llinger`, `beliefs?a`, `2267?2281`, `article?s` and `authors?`; these correspond to `Völlinger`, `beliefs—a`, `2267–2281`, `article’s` and `authors’`. The accompanying source-pack.md already supplies the correct author name, title, pagination and license. The source paragraph, DOI, locator, source hash and substantive task were not altered. This correction is outside the writers' permitted inputs and is not a retroactive change to their records. Public readers should use the corrected citation above while retaining the recorded frozen bytes when reproducing the experiment.

The defect is a preparation limitation. It does not establish that all possible effects on writing are absent; it is shared across the compared compression arms. The actual final headings and bodies are checked separately for propagation.
