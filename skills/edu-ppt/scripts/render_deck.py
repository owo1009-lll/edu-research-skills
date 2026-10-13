"""Render actual PPTX with PowerPoint (Windows) or LibreOffice + pdftoppm.

No screenshot-based substitute renderer is used. Failure is recorded explicitly.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from PIL import Image, ImageOps, ImageDraw


def powerpoint(source, out):
    import pythoncom
    import win32com.client
    pythoncom.CoInitialize()
    app = deck = None
    try:
        # A dedicated instance and WithWindow=False avoid changing the user's open deck.
        app = win32com.client.DispatchEx('PowerPoint.Application')
        deck = app.Presentations.Open(str(source), ReadOnly=True, Untitled=False, WithWindow=False)
        width = 1600
        height = round(width * deck.PageSetup.SlideHeight / deck.PageSetup.SlideWidth)
        for i in range(1, deck.Slides.Count + 1):
            deck.Slides.Item(i).Export(str(out / f'slide-{i:03d}.png'), 'PNG', width, height)
        deck.SaveAs(str(out / 'slides.pdf'), 32)
        return 'PowerPoint COM'
    finally:
        if deck is not None:
            deck.Close()
        if app is not None:
            app.Quit()
        pythoncom.CoUninitialize()


def libreoffice(source, out):
    office = shutil.which('soffice') or shutil.which('libreoffice')
    ppm = shutil.which('pdftoppm')
    if not office or not ppm:
        raise RuntimeError('Rendering requires PowerPoint on Windows, or LibreOffice and pdftoppm on PATH')
    with tempfile.TemporaryDirectory(prefix='edu-ppt-lo-') as profile:
        subprocess.run([office, '-env:UserInstallation=' + Path(profile).as_uri(), '--headless', '--convert-to', 'pdf', '--outdir', str(out), str(source)], check=True, capture_output=True, timeout=120)
    pdf = out / (source.stem + '.pdf')
    if not pdf.exists():
        raise RuntimeError('LibreOffice returned without producing a PDF')
    subprocess.run([ppm, '-png', '-r', '120', str(pdf), str(out / 'page')], check=True, capture_output=True, timeout=120)
    pages = sorted(out.glob('page-*.png'), key=lambda p: int(p.stem.split('-')[-1]))
    for i, page in enumerate(pages, 1):
        page.rename(out / f'slide-{i:03d}.png')
    if pdf.name != 'slides.pdf':
        pdf.rename(out / 'slides.pdf')
    return 'LibreOffice + pdftoppm'


def contact_sheets(out):
    pages = sorted(out.glob('slide-*.png'))
    outputs = []
    for batch in range(0, len(pages), 12):
        group = pages[batch:batch + 12]
        tile_w, tile_h = 480, 305
        sheet = Image.new('RGB', (tile_w * 3, tile_h * ((len(group) + 2) // 3)), '#dce3e7')
        draw = ImageDraw.Draw(sheet)
        for i, page in enumerate(group):
            with Image.open(page) as image:
                tile = ImageOps.contain(image.convert('RGB'), (tile_w - 16, tile_h - 30))
                xx, yy = i % 3 * tile_w, i // 3 * tile_h
                sheet.paste(tile, (xx + 8, yy + 22))
                draw.text((xx + 8, yy + 5), f'Slide {batch + i + 1}', fill='#172d3a')
        name = f'contact-{batch // 12 + 1:02d}.png'
        sheet.save(out / name)
        outputs.append(name)
    return outputs


def render(source, out, engine='auto'):
    source, out = Path(source).resolve(), Path(out).resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError('Render to a fresh directory; stale previews must not imply success')
    out.mkdir(parents=True, exist_ok=True)
    result = {'source': str(source), 'pptx_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'status': 'failed', 'visual_review': 'not_performed', 'errors': []}
    try:
        chosen = engine
        if chosen == 'auto':
            chosen = 'powerpoint' if os.name == 'nt' else 'libreoffice'
        try:
            result['engine'] = powerpoint(source, out) if chosen == 'powerpoint' else libreoffice(source, out)
        except Exception as exc:
            if engine != 'auto' or chosen != 'powerpoint' or not (shutil.which('soffice') or shutil.which('libreoffice')):
                raise
            result['errors'].append('PowerPoint unavailable: ' + str(exc))
            # No successful preview is claimed until the alternate renderer returns.
            result['engine'] = libreoffice(source, out)
        pages = sorted(out.glob('slide-*.png'))
        from pptx import Presentation
        expected = len(Presentation(source).slides)
        if len(pages) != expected:
            raise RuntimeError(f'Rendered {len(pages)} pages, expected {expected}')
        result.update(status='rendered', slides=expected, contact_sheets=contact_sheets(out))
        result['images'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in pages}
    except Exception as exc:
        result['errors'].append(str(exc))
    (out / 'render.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pptx', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--engine', choices=['auto', 'powerpoint', 'libreoffice'], default='auto')
    args = parser.parse_args()
    report = render(args.pptx, args.out, args.engine)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report['status'] != 'rendered':
        sys.exit(1)
