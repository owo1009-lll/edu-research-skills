"""Open the public DOCX fixtures in hidden Windows Word and render comment balloons."""
import argparse
import gc
import json
from pathlib import Path


def main():
    import win32com.client
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--examples', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    folder = args.examples.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    receipt = output / 'word-open.json'
    files = sorted(folder.glob('*.docx'))
    if len(files) != 2:
        raise ValueError('Expected source and annotated DOCX.')
    app = win32com.client.DispatchEx('Word.Application')
    app.Visible = False
    app.DisplayAlerts = 0
    update_links = app.Options.UpdateLinksAtOpen
    app.Options.UpdateLinksAtOpen = False
    doc, records = None, []
    try:
        for file in files:
            pdf = output / (file.stem + '_word-preview.pdf')
            if pdf.exists():
                raise FileExistsError(pdf)
            print('Opening', file.name, flush=True)
            doc = app.Documents.Open(str(file), False, True, False)
            # Word's Range.Text follows revision-view settings. Set the same
            # view before reading either file; never accept/reject revisions.
            doc.ActiveWindow.View.RevisionsView = 0
            doc.ActiveWindow.View.ShowRevisionsAndComments = True
            doc.ActiveWindow.View.RevisionsMode = 0
            doc.ActiveWindow.View.ShowHighlight = True
            comments = []
            for i in range(1, doc.Comments.Count + 1):
                comment = doc.Comments.Item(i)
                comments.append({'author': comment.Author, 'anchor': comment.Scope.Text,
                                 'text': comment.Range.Text, 'color': comment.Scope.HighlightColorIndex})
            records.append({'file': file.name, 'word_version': app.Version, 'comments': comments,
                            'revisions': doc.Revisions.Count, 'fields': doc.Fields.Count,
                            'tables': doc.Tables.Count, 'inline_shapes': doc.InlineShapes.Count,
                            'body_text': doc.Content.Text})
            print('Read native comments, revisions and object counts; exporting', flush=True)
            # Read-only, unsaved rendering copy: prevent Word's print-time
            # field refresh from changing the cached citation display.
            doc.Fields.Locked = True
            # Word overlays reviewer colors on highlight marks in markup view.
            # Export both views to inspect native colors and comment balloons.
            # Preview PDFs omit Word's problematic markup structure tags;
            # the source/annotated DOCX packages remain untouched.
            doc.ActiveWindow.View.ShowRevisionsAndComments = False
            content_pdf = output / (file.stem + '_highlights.pdf')
            doc.ExportAsFixedFormat(str(content_pdf), 17, False, 0, 0, 1, 1, 0, True, True, 0, False)
            doc.ActiveWindow.View.ShowRevisionsAndComments = True
            doc.ExportAsFixedFormat(str(pdf), 17, False, 0, 0, 1, 1, 7, True, True, 0, False)
            doc.Close(0)
            doc = None
            print('Rendered', pdf.name, flush=True)
        before, after = records
        for key in ('body_text', 'revisions', 'fields', 'tables', 'inline_shapes'):
            if before[key] != after[key]:
                raise ValueError(f'Opened document changed: {key}')
        plan = json.loads((folder / 'docx-plan.json').read_text(encoding='utf-8'))
        additions = [c for c in after['comments'] if c not in before['comments']]
        if len(additions) != len(plan['annotations']) or any(c not in after['comments'] for c in before['comments']):
            raise ValueError('Native existing/new comments differ from the plan.')
        for entry in plan['annotations']:
            found = [c for c in additions if f'｜{entry["id"]}]' in c['text']]
            if len(found) != 1 or found[0]['author'] != 'AI 模拟审稿' or found[0]['anchor'] != entry['anchors'][0]['quote']:
                raise ValueError(f'Wrong native comment anchor/author: {entry["id"]}')
            if found[0]['color'] != {'error': 6, 'improvement': 7, 'verify': 2}[entry['kind']]:
                raise ValueError(f'Wrong native highlight color: {entry["id"]}')
        with receipt.open('x', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        import fitz
        for pdf in output.glob('*.pdf'):
            with fitz.open(pdf) as rendered:
                for i, page in enumerate(rendered):
                    page.get_pixmap(matrix=fitz.Matrix(1.3, 1.3)).save(
                        str(pdf.with_name(pdf.stem + f'-page-{i+1}.png')))
        print('Opened and rendered both files; original content and objects preserved.', flush=True)
    finally:
        if doc is not None:
            doc.Close(0)
        app.Options.UpdateLinksAtOpen = update_links
        app.Quit()
        del app
        gc.collect()


if __name__ == '__main__':
    main()
