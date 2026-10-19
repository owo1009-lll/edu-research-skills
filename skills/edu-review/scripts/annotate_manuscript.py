"""Native annotations without rewriting manuscript content.

inventory SOURCE --output anchors.json
apply SOURCE --plan annotations.json [--output NAME_审稿标注版.docx|pdf]
verify SOURCE ANNOTATED --plan annotations.json

Plans are internal working records. Deliver only the annotated manuscript.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import posixpath
import tempfile
import zipfile

from lxml import etree as ET

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/package/2006/relationships'
CT = 'http://schemas.openxmlformats.org/package/2006/content-types'
COMMENTS_REL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments'
AUTHOR = 'AI 模拟审稿'
KINDS = {
    'improvement': ('yellow', (1, 1, 0), '论证/表达建议'),
    'error': ('red', (1, 0, 0), '明确错误'),
    'verify': ('blue', (0.2, 0.55, 1), '待核实'),
}
DOC = 'word/document.xml'
RELS = 'word/_rels/document.xml.rels'


def w(name):
    return f'{{{W}}}{name}'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def xml(data):
    return ET.fromstring(data, ET.XMLParser(resolve_entities=False, no_network=True))


def serial(node):
    return ET.tostring(node, encoding='UTF-8', xml_declaration=True, standalone=True)


def canonical(node):
    return ET.tostring(node, method='c14n')


def fail(message):
    raise ValueError(message)


def package(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if len(names) != len(set(names)):
            fail('Duplicate ZIP entries are unsupported.')
        if any(n.startswith('_xmlsignatures/') for n in names):
            fail('Digitally signed DOCX is unsupported; annotation would invalidate its signature.')
        return {n: z.read(n) for n in names}


def visible_runs(paragraph):
    """Stable offsets for body/table paragraph text, including visible insertions."""
    offset = 0
    for run in paragraph.iter(w('r')):
        if next(run.iterancestors(w('p')), None) is not paragraph:
            continue  # a nested textbox has its own paragraph
        if any(a.tag in (w('del'), w('moveFrom')) for a in run.iterancestors()):
            continue
        text = ''.join((n.text or '') if n.tag == w('t') else
                       '\t' if n.tag == w('tab') else '\n'
                       for n in run if n.tag in (w('t'), w('tab'), w('br'), w('cr')))
        if text:
            yield run, offset, offset + len(text), text
            offset += len(text)


def ptext(paragraph):
    return ''.join(t for _, _, _, t in visible_runs(paragraph))


def paragraphs(root):
    return list(root.iter(w('p')))


def plain(run):
    return (len(run.findall(w('t'))) == 1 and
            all(n.tag in (w('rPr'), w('t')) for n in run))


def pdf_lines(page):
    """Text and character quads in the PDF's unrotated coordinate system."""
    import fitz
    lines = []
    for block in page.get_text('rawdict')['blocks']:
        for line in block.get('lines', []):
            chars, quads = [], []
            for span in line['spans']:
                for char in span['chars']:
                    chars.extend(char['c'])
                    quads.extend([fitz.recover_char_quad(line['dir'], span, char)] * len(char['c']))
            lines.append((''.join(chars), quads, line['dir']))
    return lines


def inventory(source):
    source = Path(source)
    result = {'schema_version': 1, 'source_sha256': digest(source.read_bytes()),
              'source_name': source.name, 'units': []}
    if source.suffix.lower() == '.docx':
        root = xml(package(source)[DOC])
        for i, p in enumerate(paragraphs(root)):
            text = ptext(p)
            result['units'].append({'part': DOC, 'paragraph': i, 'text': text,
                                    'text_sha256': digest(text.encode()),
                                    'in_table': any(a.tag == w('tc') for a in p.iterancestors())})
    elif source.suffix.lower() == '.pdf':
        import fitz
        with fitz.open(source) as doc:
            if doc.needs_pass:
                fail('Encrypted PDF requires an accessible unencrypted working copy.')
            for page in doc:
                for i, (text, _, _) in enumerate(pdf_lines(page)):
                    result['units'].append({'page': page.number + 1, 'line': i,
                                            'text': text, 'text_sha256': digest(text.encode())})
    else:
        fail('Supported source formats: DOCX and text-layer PDF.')
    return result


def validate_plan(source, plan):
    if plan.get('schema_version') != 1:
        fail('Plan schema_version must be 1.')
    if digest(Path(source).read_bytes()) != plan.get('source_sha256'):
        fail('Source SHA-256 changed; rebuild and review anchors against this file.')
    annotations = plan.get('annotations')
    if not isinstance(annotations, list):
        fail('annotations must be a list (it may be empty).')
    if annotations:
        try:
            created = datetime.fromisoformat(plan['created_utc'].replace('Z', '+00:00'))
            if created.utcoffset() is None or created.utcoffset().total_seconds() != 0:
                fail('created_utc must be UTC ISO 8601.')
        except (KeyError, TypeError, ValueError):
            fail('created_utc must be a real UTC ISO 8601 timestamp recorded in the working plan.')
    ids = set()
    for a in annotations:
        aid = a.get('id')
        if not isinstance(aid, str) or not aid or aid in ids:
            fail('Annotation IDs must be nonempty and unique.')
        ids.add(aid)
        if a.get('kind') not in KINDS or not str(a.get('comment', '')).strip():
            fail(f'{aid}: kind and a nonempty comment are required.')
        if a.get('severity') not in (None, 'major', 'minor'):
            fail(f'{aid}: severity must be major, minor or absent.')
        if not a.get('anchors'):
            fail(f'{aid}: at least one precise anchor is required.')
    return annotations


def comment_text(a):
    severity = {'major': '主要', 'minor': '次要'}.get(a.get('severity'))
    label = KINDS[a['kind']][2] + (f'｜{severity}' if severity else '')
    return f'[{label}｜{a["id"]}] {a["comment"].strip()}'


def check_range(anchor, text, label):
    start, end = anchor.get('start'), anchor.get('end')
    if (type(start) is not int or type(end) is not int or
            not 0 <= start < end <= len(text)):
        fail(f'{label}: invalid character range {start}:{end} for length {len(text)}.')
    if digest(text.encode()) != anchor.get('text_sha256'):
        fail(f'{label}: unit text SHA-256 differs; expected {anchor.get("quote")!r}.')
    actual = text[start:end]
    if actual != anchor.get('quote'):
        fail(f'{label}: expected {anchor.get("quote")!r}, actual {actual!r}.')
    return start, end


def check_overlaps(ranges):
    for unit, entries in ranges.items():
        ordered = sorted(entries)
        for first, second in zip(ordered, ordered[1:]):
            if second[0] < first[1]:
                fail(f'{unit}: overlapping {first[2]} and {second[2]}; combine into one dominant-color comment.')


def selected_runs(paragraph, start, end, label):
    selected = [(r, s, e, t) for r, s, e, t in visible_runs(paragraph) if s < end and e > start]
    if not selected or any(r.getparent() is not paragraph or not plain(r) for r, _, _, _ in selected):
        fail(f'{label}: anchor touches a field, hyperlink, tracked insertion, textbox or non-plain run; choose nearby plain text.')
    first, last = paragraph.index(selected[0][0]), paragraph.index(selected[-1][0])
    allowed = {w(t) for t in ['r', 'bookmarkStart', 'bookmarkEnd', 'commentRangeStart', 'commentRangeEnd']}
    for node in list(paragraph)[first:last + 1]:
        if node.tag not in allowed or (node.tag == w('r') and not plain(node)):
            fail(f'{label}: selected range crosses a non-text object; use a smaller anchor.')
    return selected


def split_run(run, text):
    new = deepcopy(run)
    new.find(w('t')).text = text
    new.find(w('t')).set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    return new


def add_docx_anchor(p, start, end, cid, color, label):
    selected = selected_runs(p, start, end, label)
    highlighted = []
    for r, s, e, text in selected:
        old = r.find('./' + w('rPr') + '/' + w('highlight'))
        if old is not None and old.get(w('val')) != 'none':
            fail(f'{label}: original text already has highlight; choose a non-overlapping anchor.')
        i = p.index(r)
        pieces = []
        lo, hi = max(start, s) - s, min(end, e) - s
        if lo:
            pieces.append(split_run(r, text[:lo]))
        middle = split_run(r, text[lo:hi])
        props = middle.find(w('rPr'))
        if props is None:
            props = ET.Element(w('rPr'))
            middle.insert(0, props)
        old = props.find(w('highlight'))
        if old is not None:
            props.remove(old)
        # python-docx's schema-ordered helper keeps w:rPr valid after color/size.
        from docx.oxml import parse_xml
        ordered = parse_xml(ET.tostring(props))
        ordered.get_or_add_highlight().set(w('val'), color)
        middle.replace(props, ordered)
        pieces.append(middle)
        highlighted.append(middle)
        if hi < len(text):
            pieces.append(split_run(r, text[hi:]))
        p.remove(r)
        for n, piece in enumerate(pieces):
            p.insert(i + n, piece)
    start_node = ET.Element(w('commentRangeStart'), {w('id'): str(cid)})
    end_node = ET.Element(w('commentRangeEnd'), {w('id'): str(cid)})
    highlighted[0].addprevious(start_node)
    highlighted[-1].addnext(end_node)
    reference = ET.Element(w('r'))
    ET.SubElement(reference, w('commentReference'), {w('id'): str(cid)})
    end_node.addnext(reference)


def build_docx(source, plan):
    annotations = validate_plan(source, plan)
    data = package(source)
    root = xml(data[DOC])
    ps = paragraphs(root)
    rels = xml(data[RELS]) if RELS in data else ET.Element(f'{{{R}}}Relationships', nsmap={None: R})
    comments_rels = [r for r in rels if r.get('Type') == COMMENTS_REL]
    if len(comments_rels) > 1:
        fail('Multiple comment parts are unsupported.')
    if comments_rels:
        target = comments_rels[0].get('Target')
        name = target.lstrip('/') if target.startswith('/') else posixpath.normpath('word/' + target)
        if name not in data:
            fail('Existing comment part is missing.')
        comments = xml(data[name])
    else:
        name = 'word/comments.xml'
        if name in data:
            fail('Orphan comment part exists; repair source relationships first.')
        comments = ET.Element(w('comments'), nsmap={'w': W})
    ranges, entries = {}, []
    for a in annotations:
        if len(a['anchors']) != 1:
            fail(f'{a["id"]}: Word supports one paragraph anchor per comment; use cross-references for other locations.')
        anchor = a['anchors'][0]
        idx = anchor.get('paragraph')
        if anchor.get('part') != DOC or type(idx) is not int or not 0 <= idx < len(ps):
            fail(f'{a["id"]}: invalid body/table paragraph address.')
        start, end = check_range(anchor, ptext(ps[idx]), f'{a["id"]}, paragraph {idx}')
        selected_runs(ps[idx], start, end, a['id'])
        ranges.setdefault(idx, []).append((start, end, a['id']))
        entries.append((a, ps[idx], start, end))
    check_overlaps(ranges)
    used = [int(e.get(w('id'))) for e in comments if e.get(w('id'), '').isdigit()]
    used += [int(e.get(w('id'))) for e in root.iter() if e.tag in
             (w('commentRangeStart'), w('commentRangeEnd'), w('commentReference')) and e.get(w('id'), '').isdigit()]
    cid = max(used, default=-1) + 1
    new_ids = []
    for a, p, start, end in entries:
        add_docx_anchor(p, start, end, cid, KINDS[a['kind']][0], a['id'])
        c = ET.SubElement(comments, w('comment'), {w('id'): str(cid), w('author'): AUTHOR,
                          w('initials'): 'AI', w('date'): plan['created_utc']})
        for line in comment_text(a).splitlines():
            t = ET.SubElement(ET.SubElement(ET.SubElement(c, w('p')), w('r')), w('t'))
            t.text = line
            t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        new_ids.append(str(cid))
        cid += 1
    if not annotations:
        return data, [], name
    if not comments_rels:
        ids = {r.get('Id') for r in rels}
        i = 1
        while f'rId{i}' in ids:
            i += 1
        ET.SubElement(rels, f'{{{R}}}Relationship', Id=f'rId{i}', Type=COMMENTS_REL, Target='comments.xml')
        data[RELS] = serial(rels)
        types = xml(data['[Content_Types].xml'])
        if not any(t.get('PartName') == '/' + name for t in types):
            ET.SubElement(types, f'{{{CT}}}Override', PartName='/' + name,
                          ContentType='application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml')
        data['[Content_Types].xml'] = serial(types)
    data[DOC] = serial(root)
    data[name] = serial(comments)
    return data, new_ids, name


def normalize_plain_runs(root):
    """Ignore harmless text-run splits; retain all other OOXML structure and style."""
    for p in paragraphs(root):
        for r in list(p):
            if r.tag != w('r') or not plain(r):
                continue
            rp = r.find(w('rPr'))
            if rp is not None and not len(rp) and not rp.attrib:
                r.remove(rp)
            r.find(w('t')).set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
            prev = r.getprevious()
            if prev is not None and prev.tag == w('r') and plain(prev):
                a, b = deepcopy(prev), deepcopy(r)
                a.find(w('t')).text = b.find(w('t')).text = ''
                if canonical(a) == canonical(b):
                    prev.find(w('t')).text = (prev.find(w('t')).text or '') + (r.find(w('t')).text or '')
                    p.remove(r)
    return root


def verify_docx(source, annotated, plan):
    expected, new_ids, comments_name = build_docx(source, plan)
    original, actual = package(source), package(annotated)
    if set(expected) != set(actual):
        fail('DOCX package parts differ from the annotation plan.')
    for name in expected:
        if expected[name] == actual[name]:
            continue
        if name.endswith(('.xml', '.rels')) and canonical(xml(expected[name])) == canonical(xml(actual[name])):
            continue
        fail(f'{name}: actual contents differ from expected annotation-only output.')
    # Independent preservation check: remove new annotations, undo highlights,
    # normalize harmless run splits, and compare the manuscript to its source.
    clean = xml(actual[DOC])
    for node in list(clean.iter()):
        if node.tag in (w('commentRangeStart'), w('commentRangeEnd')) and node.get(w('id')) in new_ids:
            node.getparent().remove(node)
        elif node.tag == w('commentReference') and node.get(w('id')) in new_ids:
            run = node.getparent()
            run.getparent().remove(run)
    ps, original_ps = paragraphs(clean), paragraphs(xml(original[DOC]))
    for a in plan['annotations']:
        anchor = a['anchors'][0]
        idx = anchor['paragraph']
        for r, s, e, _ in visible_runs(ps[idx]):
            if s < anchor['end'] and e > anchor['start']:
                rp = r.find(w('rPr'))
                highlight = rp.find(w('highlight')) if rp is not None else None
                if highlight is None or highlight.get(w('val')) != KINDS[a['kind']][0]:
                    fail(f'{a["id"]}: highlight missing or wrong color.')
                rp.remove(highlight)
                # Restore an explicit source "none" setting when present.
                old = next((x for x, lo, hi, _ in visible_runs(original_ps[idx]) if lo <= s < hi), None)
                prior = old.find('./' + w('rPr') + '/' + w('highlight'))
                if prior is not None:
                    rp.insert(old.find(w('rPr')).index(prior), deepcopy(prior))
    if canonical(normalize_plain_runs(clean)) != canonical(normalize_plain_runs(xml(original[DOC]))):
        fail('Manuscript structure/style/text changed beyond planned highlights and comments.')
    changed = [n for n in original if original[n] != actual[n]]
    return {'format': 'docx', 'annotations': len(new_ids), 'preserved_source': True,
            'changed_parts': changed, 'comments_part': comments_name,
            'scope': 'Package, text/style, fields, tables, images, existing comments and revisions; opening/rendering is separate.'}


def pdf_targets(doc, plan):
    import fitz
    ranges, targets = {}, []
    for a in plan['annotations']:
        quads, pages = [], set()
        for anchor in a['anchors']:
            page, line = anchor.get('page'), anchor.get('line')
            if type(page) is not int or not 1 <= page <= len(doc):
                fail(f'{a["id"]}: invalid page {page}.')
            lines = pdf_lines(doc[page - 1])
            if type(line) is not int or not 0 <= line < len(lines):
                fail(f'{a["id"]}: invalid line {line} on page {page}.')
            text, chars, direction = lines[line]
            lo, hi = check_range(anchor, text, f'{a["id"]}, page {page}, line {line}')
            ranges.setdefault((page, line), []).append((lo, hi, a['id']))
            # One quad per glyph handles horizontal and rotated text precisely.
            # Merge horizontal adjacent glyphs for the usual clean highlight.
            if direction == (1, 0):
                rect = fitz.Rect(chars[lo].rect)
                for char in chars[lo + 1:hi]:
                    rect |= char.rect
                quads.append(rect.quad)
            else:
                quads.extend(chars[lo:hi])
            pages.add(page)
        if len(pages) != 1:
            fail(f'{a["id"]}: use one comment per PDF page and cross-reference related locations.')
        targets.append((pages.pop() - 1, a, quads))
    check_overlaps(ranges)
    return targets


def verify_pdf(source, annotated, plan):
    import fitz
    validate_plan(source, plan)
    with fitz.open(source) as before, fitz.open(annotated) as after:
        targets = pdf_targets(before, plan)
        if len(before) != len(after):
            fail('PDF page count changed.')
        page_xrefs = {p.xref for p in before}
        for xref in range(1, before.xref_length()):
            if xref in page_xrefs:
                old_keys = set(before.xref_get_keys(xref)) - {'Annots'}
                new_keys = set(after.xref_get_keys(xref)) - {'Annots'}
                if old_keys != new_keys or any(before.xref_get_key(xref, k) != after.xref_get_key(xref, k) for k in old_keys):
                    fail(f'PDF page object {xref} changed outside its annotation list.')
            elif before.xref_object(xref) != after.xref_object(xref):
                fail(f'Existing PDF object {xref} changed.')
            if before.xref_is_stream(xref) and before.xref_stream_raw(xref) != after.xref_stream_raw(xref):
                fail(f'Existing PDF stream {xref} changed.')
        for i in range(len(before)):
            b, a = before[i], after[i]
            if b.get_text() != a.get_text() or b.rotation != a.rotation or b.mediabox != a.mediabox:
                fail(f'Page {i + 1}: source text or page geometry changed.')
            old = list(b.annots() or [])
            found = list(a.annots() or [])
            # Incremental saving retains original annotation xrefs and dictionaries.
            for annot in old:
                if before.xref_object(annot.xref) != after.xref_object(annot.xref):
                    fail(f'Page {i + 1}: existing annotation {annot.xref} changed.')
            added = [x for x in found if x.xref not in {o.xref for o in old}]
            wanted = [(entry, qs) for page, entry, qs in targets if page == i]
            if len(added) != len(wanted):
                fail(f'Page {i + 1}: expected {len(wanted)} added annotations, found {len(added)}.')
            for annot, (entry, qs) in zip(added, wanted):
                expected_vertices = [v for q in qs for pt in q for v in pt]
                actual_vertices = [v for pt in annot.vertices for v in pt]
                if len(actual_vertices) != len(expected_vertices) or any(abs(a-b) > .02 for a, b in zip(actual_vertices, expected_vertices)):
                    fail(f'{entry["id"]}: highlight location differs from the exact text range.')
                if annot.type[0] != fitz.PDF_ANNOT_HIGHLIGHT or annot.info['title'] != AUTHOR or annot.info['content'] != comment_text(entry):
                    fail(f'{entry["id"]}: highlight type, comment or author mismatch.')
                stroke = annot.colors['stroke']
                if len(stroke) != 3 or any(abs(a-b) > .001 for a,b in zip(stroke, KINDS[entry['kind']][1])):
                    fail(f'{entry["id"]}: highlight color mismatch.')
                if abs(annot.opacity - .3) > .001:
                    fail(f'{entry["id"]}: highlight opacity changed.')
        # Transparent annotations can change antialiasing by 1-2 levels even
        # with annots=False. Render isolated copies with annotation arrays
        # removed, while the object/stream checks above enforce exact fidelity.
        for i in range(len(before)):
            samples = []
            for path in (source, annotated):
                with fitz.open(path) as render:
                    render.xref_set_key(render[i].xref, 'Annots', 'null')
                    samples.append(render[i].get_pixmap(annots=False).samples)
            if samples[0] != samples[1]:
                fail(f'Page {i + 1}: isolated unannotated page rendering changed.')
    return {'format': 'pdf', 'annotations': len(targets), 'preserved_source': True,
            'scope': 'Every page rendered without annotations matches; exact anchors/comments/colors and existing annotations checked.'}


def verify(source, annotated, plan):
    if Path(source).suffix.lower() == '.docx':
        return verify_docx(source, annotated, plan)
    return verify_pdf(source, annotated, plan)


def apply(source, plan, output=None):
    source = Path(source).resolve()
    output = Path(output).resolve() if output else source.with_name(source.stem + '_审稿标注版' + source.suffix)
    if source == output or output.exists():
        fail('Output already exists or equals source; choose a new output path.')
    if output.suffix.lower() != source.suffix.lower():
        fail('Output must retain the source format.')
    validate_plan(source, plan)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='edu-review-', dir=output.parent) as temp:
        target = Path(temp) / output.name
        if source.suffix.lower() == '.docx':
            data, _, _ = build_docx(source, plan)
            with zipfile.ZipFile(source) as original, zipfile.ZipFile(target, 'w') as z:
                for info in original.infolist():
                    z.writestr(info, data.pop(info.filename))
                for name, content in data.items():
                    z.writestr(name, content, compress_type=zipfile.ZIP_DEFLATED)
        elif source.suffix.lower() == '.pdf':
            import fitz
            target.write_bytes(source.read_bytes())
            with fitz.open(target) as doc:
                if doc.needs_pass or doc.get_sigflags() > 0:
                    fail('Encrypted or signed PDF requires a suitable unsigned, accessible working copy.')
                for page, entry, quads in pdf_targets(doc, plan):
                    page_object = doc[page]
                    annot = page_object.add_highlight_annot(quads)
                    annot.set_info(title=AUTHOR, content=comment_text(entry), subject=entry['id'])
                    annot.set_colors(stroke=KINDS[entry['kind']][1])
                    annot.set_opacity(.3)
                    annot.update()
                doc.saveIncr()
        else:
            fail('Supported source formats: DOCX and text-layer PDF.')
        result = verify(source, target, plan)
        # Exclusive create avoids accidentally overwriting a concurrently created file.
        with output.open('xb') as f:
            f.write(target.read_bytes())
    return result | {'output': str(output), 'output_sha256': digest(output.read_bytes())}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = ap.add_subparsers(dest='command', required=True)
    inv = commands.add_parser('inventory')
    inv.add_argument('source', type=Path)
    inv.add_argument('--output', type=Path, required=True)
    for name in ('apply', 'verify'):
        sub = commands.add_parser(name)
        sub.add_argument('source', type=Path)
        sub.add_argument('--plan', type=Path, required=True)
        if name == 'verify':
            sub.add_argument('annotated', type=Path)
        else:
            sub.add_argument('--output', type=Path)
    args = ap.parse_args()
    try:
        if args.command == 'inventory':
            result = inventory(args.source)
            with args.output.open('x', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(json.dumps({'units': len(result['units']), 'output': str(args.output)}, ensure_ascii=False))
        else:
            plan = json.loads(args.plan.read_text(encoding='utf-8'))
            if args.command == 'apply':
                result = apply(args.source, plan, args.output)
            else:
                result = verify(args.source, args.annotated, plan)
            print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, KeyError, OSError, zipfile.BadZipFile) as e:
        ap.exit(1, f'{e}\n')


if __name__ == '__main__':
    main()
