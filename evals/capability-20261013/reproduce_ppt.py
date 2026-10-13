"""Run two object-correspondence mutations with current or archived scripts."""
from pathlib import Path
import argparse
import copy
import json
import sys


def run(scripts, out):
    sys.path.insert(0, str(Path(scripts).resolve()))
    from build_deck import build
    from check_deck import check
    from objects import identity
    from pptx import Presentation
    root = Path(__file__).resolve().parents[2]
    plan = json.loads((root / 'skills/edu-ppt/examples/progress-plan.json').read_text(encoding='utf-8'))
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    reports = {}
    for case in ('normal', 'custom_label_999', 'interval_partial_swap', 'interval_whole_row_swap'):
        source = out / (case + '.json')
        source.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
        folder = out / case
        build(source, folder)
        path = folder / 'slides.pptx'
        prs = Presentation(path)
        if case == 'custom_label_999':
            chart = next(s.chart for s in prs.slides[1].shapes if s.has_chart)
            chart.series[0].points[0].data_label.text_frame.text = '999'
        elif case.startswith('interval_'):
            shapes = {identity(s).get('id', '').split('/row/')[-1]: s for s in prs.slides[-1].shapes}
            parts = ('interval', 'estimate', 'label', 'display') if case.endswith('whole_row_swap') else ('interval', 'estimate')
            for part in parts:
                one, two = shapes['0/' + part], shapes['1/' + part]
                one.top, two.top = two.top, one.top
        prs.save(path)
        reports[case] = check(path, source)
    (out / 'observations.json').write_text(json.dumps(reports, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return {case: result['status'] for case, result in reports.items()}


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--scripts', default='skills/edu-ppt/scripts')
    cli.add_argument('--out', required=True)
    args = cli.parse_args()
    print(json.dumps(run(args.scripts, args.out), indent=2))
