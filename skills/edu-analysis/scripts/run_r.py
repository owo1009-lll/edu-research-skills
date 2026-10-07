"""Run an R analysis in a new, recorded folder under ./edu_output/analysis/.

Script mode (method cards):  python run_r.py --script analysis.R --input data.csv [--input more.csv] [--slug name]
    The script can source("edu_methods.R"), reads data from inputs/<file name>, and writes to output/.
Adapter mode (plan-driven):  python run_r.py --adapter basic|advanced --plan plan.json [--slug name]
    Runs the tested basic or advanced adapter; the plan's "data" path is copied into the run.
"""
from pathlib import Path
import argparse
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'edu-shared' / 'scripts'))
from edu_runtime import new_run_dir, run_r  # noqa: E402

ADAPTERS = {'basic': HERE / 'analyze.R', 'advanced': HERE / 'advanced.R'}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--script', type=Path)
    mode.add_argument('--adapter', choices=sorted(ADAPTERS))
    ap.add_argument('--plan', type=Path, help='adapter plan (JSON) prepared by the assistant')
    ap.add_argument('--input', type=Path, action='append', default=[])
    ap.add_argument('--slug', default='')
    ap.add_argument('--out-base', type=Path, help='default: ./edu_output')
    ap.add_argument('--rscript')
    ap.add_argument('--timeout', type=int, default=1800)
    a = ap.parse_args()
    if a.adapter:
        if not a.plan:
            ap.error('--adapter needs --plan')
        plan = json.loads(a.plan.read_text(encoding='utf-8'))
        data = (a.plan.parent / plan['data']).resolve() if not Path(plan['data']).is_absolute() else Path(plan['data'])
        run = new_run_dir('analysis', a.slug or a.adapter, a.out_base)
        plan['data'] = 'inputs/' + data.name
        (run / 'plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
        code = run_r(ADAPTERS[a.adapter], run, args=('plan.json', 'output'), inputs=[data, a.plan],
                     rscript=a.rscript, timeout=a.timeout)
    else:
        run = new_run_dir('analysis', a.slug or a.script.stem, a.out_base)
        (run / 'output').mkdir()
        code = run_r(a.script, run, inputs=a.input, helpers=[HERE / 'edu_methods.R'],
                     rscript=a.rscript, timeout=a.timeout)
    print(json.dumps({'run': str(run), 'returncode': code}, ensure_ascii=False))
    return code


if __name__ == '__main__':
    sys.exit(main())
