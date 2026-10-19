"""Create new public English review tasks; no real research or private material."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

QUANT = [
    ("Retrieval practice in lower-secondary science: manuscript excerpt", [
        "PUBLIC SYNTHETIC MANUSCRIPT. The study, people and numbers below are invented for behavioral testing. They are not evidence about an actual intervention.",
        "Abstract. We compared a weekly retrieval activity with the usual review activity in 12 classes across six schools. All 240 students remained in the reported sample. The adjusted standardized between-condition estimate was g = 0.18, 95% CI [-0.05, 0.41], p = .12. The two approaches were therefore equally effective. Teachers described the short activity as feasible within existing lessons.",
        "Methods. Classes, rather than individual pupils, were randomized within schools. Six classes received retrieval practice (118 pupils) and six received usual review (122 pupils). The intervention ran for eight weeks. Both groups received the same subject content. A curriculum-aligned test was administered before and after the intervention; the outcome was the end-of-intervention score with baseline performance included as a covariate.",
        "An ordinary individual-level regression was fitted, with pupil as the unit of analysis. Individual data, analysis code and a registration record are not included in this excerpt.",
        "Results. Posttest means were 79 in the retrieval condition and 75 in the usual-review condition. The adjusted standardized comparison and its uncertainty are reported in the abstract. A separate within-condition test found a significant change from baseline for retrieval practice (p = .02), whereas the usual-review change was not significant (p = .21). This difference in statistical significance establishes that retrieval practice outperformed usual review.",
    ]),
    ("Discussion and implementation", [
        "The intended contribution is to test whether an activity that asks students to retrieve an answer before seeing it improves performance relative to reviewing the same content. The activity changes what students do with the material, rather than simply increasing their exposure time. The primary comparison remains uncertain, with the reported interval including zero and a positive difference that could matter educationally.",
        "Eight of the 12 class teachers returned a short implementation questionnaire. Seven described the activity as manageable. Preparation involved a 40-minute training session and adapting questions to the week's content; preparation time during the intervention was not measured. These reports concern feasibility for respondents, not all teachers or effects on student motivation.",
        "Schools adopting this activity should provide preparation time and access to curriculum-aligned questions. This recommendation follows from the tasks required for implementation; it does not depend on claiming that the trial established superiority. A larger follow-up should estimate the between-condition difference with appropriate attention to the class-level assignment and a longer assessment interval.",
        "This is an excerpt supplied for review. The literature review and reference list are not included.",
    ]),
]

QUAL = [
    ("Silence and influence in teacher meetings: manuscript excerpt", [
        "PUBLIC SYNTHETIC MANUSCRIPT. All people, events and quotations below are invented for behavioral testing; this is not a report of real participants.",
        "Methods. Nine teachers from three programs took part in 12 interviews, including three follow-up interviews. The researcher also observed three team meetings. Analysis compared how speaking, waiting and written follow-up were used when teachers tried to influence team decisions. Interview accounts were considered alongside the meeting records. The supplied excerpt does not describe how the nine teachers were recruited or how the researcher entered the teams.",
        "Findings. In one observed meeting, Marta did not interrupt a senior colleague who was presenting the timetable. After the meeting she emailed an alternative arrangement. The next meeting's agenda included the alternative, and the team adopted part of it. In her interview she explained: 'I wanted the idea considered, but that moment was not going to help it.' Her account links waiting to an alternative route for influencing a decision.",
        "A contrasting case concerns Amir. He remained silent during a meeting about assessment and later said, 'I did not want the manager to think I was difficult.' The observation record contains no later written proposal from him. His account points to the anticipated consequences of disagreement, rather than a planned alternative intervention.",
    ]),
    ("Interpretation and implications", [
        "These cases make silence analytically heterogeneous. Marta's waiting formed part of a sequence that included a written proposal and a changed agenda. Amir's account instead concerned the risk of speaking against a manager. The interpretation concerns how influence becomes possible through relationships and available channels; it does not equate agency with the number of spoken turns.",
        "Every instance of silence in this study was therefore a deliberate strategy of resistance, showing that quiet teachers exercised the same influence as frequent speakers. The interviews establish how all silent teachers intended to intervene.",
        "The distinction between waiting as part of an intervention and silence under anticipated sanction matters for school leadership. Leaders should provide credible routes for raising concerns outside a fast-moving meeting and make clear how those contributions enter decisions. Providing a written channel alone does not establish that concerns will be heard; the route also needs a response. This recommendation retains the study's position that opportunities for influence depend on how contributions are received.",
        "This is an excerpt supplied for review. The author has not supplied the full transcripts, a literature section or a target-journal template.",
    ]),
]


def pdf(path, pages):
    import fitz
    doc = fitz.open()
    for number, (title, paragraphs) in enumerate(pages, 1):
        page = doc.new_page(width=595, height=842)
        if page.insert_textbox(fitz.Rect(45, 40, 550, 100), title, fontsize=15, fontname='hebo') < 0:
            raise ValueError('Title overflow')
        if page.insert_textbox(fitz.Rect(45, 110, 550, 770), '\n\n'.join(paragraphs), fontsize=11, lineheight=1.25) < 0:
            raise ValueError('Body overflow')
        page.insert_text((45, 805), f'Public synthetic review task - page {number}', fontsize=9)
    note = doc[0].add_text_annot((555, 105), 'Original author note: preserve this note in the working copy.')
    note.set_info(title='Original Author')
    note.update()
    doc.save(path)
    doc.close()


def mixed_docx(path):
    from docx import Document
    from docx.shared import Inches, Pt
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.enum.text import WD_COLOR_INDEX
    import io
    spec = importlib.util.spec_from_file_location('old_fixture', ROOT/'evals/review-annotations/create_fixture.py')
    fixture = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixture)
    doc = Document()
    doc.styles['Normal'].font.name = 'Calibri'
    doc.styles['Normal'].font.size = Pt(11)
    doc.add_heading('Access to feedback in asynchronous seminars', 0)
    doc.add_paragraph('PUBLIC SYNTHETIC MANUSCRIPT. All data, events and participants are invented for behavioral testing. This excerpt is not evidence about an actual course.')
    doc.add_heading('Abstract', 1)
    doc.add_paragraph('Survey responses from 52 students showed that feedback was useful. Interviews added an account of how students used it. The study connects reported value with the timing and accessibility of feedback, rather than assuming that a favorable rating implies an opportunity to act.')
    doc.add_heading('Methods and results', 1)
    doc.add_paragraph('The survey contained 48 completed responses from two seminar groups. It was anonymous and collected no identifier that could link a response to a later interview. Thirty-one respondents rated the feedback useful. Students were not assigned to different feedback conditions, and no test of learning gains was collected.')
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Table Grid'
    table.rows[0].cells[0].text = 'Seminar group'
    table.rows[0].cells[1].text = 'Completed responses'
    for label, value in [('A','24'),('B','24'),('Total','48')]:
        cells = table.add_row().cells
        cells[0].text, cells[1].text = label, value
    doc.add_paragraph('Table 1. Complete survey responses. The denominator for the usefulness rating is 48.')
    doc.add_paragraph('Eight students volunteered for later interviews. Whether these students had answered the survey, and which response each might have given, could not be determined. Six described receiving useful comments too close to the next submission deadline to revise their work. Two described using comments to plan a later assignment. These accounts concern reported opportunities and uses, not observed changes in attainment.')
    doc.add_paragraph('All interviewees belonged to the favorable-rating subgroup. Their accounts validate the statistical mechanism by which useful feedback improved achievement.')
    doc.add_picture(io.BytesIO(fixture.illustration()), width=Inches(3.8))
    doc.add_paragraph('Figure 1. Equal bar heights represent the two survey group sizes, not measured learning outcomes.')
    doc.add_heading('Discussion', 1)
    p = doc.add_paragraph('The analysis distinguishes perceived value from ')
    r = p.add_run('an opportunity to act on feedback')
    r.font.highlight_color = WD_COLOR_INDEX.BRIGHT_GREEN
    p.add_run('. A comment can be regarded as useful yet arrive too late for the next task. The separate samples do not show which favorable survey respondents experienced a timing constraint.')
    doc.add_comment(r, text='Original author comment: retain this distinction and check its wording with the coauthor.', author='Original Author', initials='OA')
    doc.add_paragraph('Course teams should schedule feedback early enough for students to use it before the next assessed task. This recommendation connects the reported timing problem to a concrete teaching decision; it is not a claim that changing the schedule has already improved learning.')
    p = doc.add_paragraph('Working terminology retained in tracked changes: ')
    for tag, ident, value in [('del','41','feedback effectiveness'),('ins','42','opportunity to use feedback')]:
        change = OxmlElement('w:'+tag)
        for key, val in [('id',ident),('author','Original Author'),('date','2026-10-01T00:00:00Z')]:
            change.set(qn('w:'+key),val)
        run = OxmlElement('w:r')
        text = OxmlElement('w:delText' if tag=='del' else 'w:t')
        text.text = value
        run.append(text)
        change.append(run)
        p._p.append(change)
    doc.add_paragraph('The supplied material is a methods/results/discussion excerpt. No raw survey data, interview transcripts, literature section or journal template is supplied.')
    doc.save(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    mixed_docx(args.output/'mixed_feedback.docx')
    pdf(args.output/'quant_retrieval.pdf', QUANT)
    pdf(args.output/'qual_silence.pdf', QUAL)
    request = 'Please review this English manuscript excerpt before journal submission. The research materials available for this task are limited to the supplied draft.\n'
    (args.output/'request.md').write_bytes(request.encode('utf-8'))
    records = [{'file':p.name, 'sha256':hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes':p.stat().st_size}
               for p in sorted(args.output.iterdir()) if p.is_file()]
    (args.output/'input-manifest.json').write_bytes((json.dumps(records,indent=2)+'\n').encode('utf-8'))
    print(json.dumps(records,indent=2))


if __name__ == '__main__':
    main()
