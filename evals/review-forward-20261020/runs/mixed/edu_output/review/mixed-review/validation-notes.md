# Final validation notes

The final deliverable is final/mixed_feedback_审稿标注版.docx, generated from annotations-v2.json. It contains five new native comments: C1, C4, and C5 are definite errors/contradictions (red); C2 and C3 request missing evidence or reporting details (blue). No unsupported weakness or color-count quota was imposed.

Structural validation: the frozen annotate_manuscript.py verify command passed for the final file. Only word/document.xml and word/comments.xml changed. Original body text, formatting except planned highlights, table, figure, original author comment, and tracked insertion/deletion were preserved. No prose was rewritten.

Actual application opening: Microsoft Word 16.0 opened the first annotated copy read-only and reported six comments, two revisions, one table, and one inline shape. All five new comment scopes and full texts matched the first annotation plan. The final shortened version subsequently opened and exported successfully through two fresh Word COM sessions.

Visual inspection: both pages of the original source, first annotated body, first marked-up export, final body, and final marked-up export were viewed. Final body highlights match their intended text; table and figure retain layout; the existing green highlight is preserved. Final marked-up pages display all five complete new comments, the original comment, and the tracked terminology. The first marked-up preview clipped the end of C5; comments were shortened in annotations-v2.json, and final previews show the complete comments without clipping.

Rendering incident: the first combined native-comment-inspection/PDF-export helper stalled after completing Word inspection. A live export retry also stalled. Only the identified run-owned Word process was stopped, and both waiting shell sessions were interrupted. The frozen renderer then exported successfully. All attempts and helper versions are retained. MuPDF emitted a structure-tree warning while rasterizing marked-up Word exports, but all page images and extracted text were produced successfully; visual checks found no resulting loss or clipping in final previews. Preview PDFs are internal validation artifacts, not user deliverables.

Research scope: this is an AI review of a synthetic supplied excerpt. No raw-data authenticity, literature completeness/novelty, or journal-specific compliance determination was made. The source explicitly lacked raw data, transcripts, literature section, and a journal template. No external research was performed.
