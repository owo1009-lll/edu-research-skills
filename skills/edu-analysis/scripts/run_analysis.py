"""Run a task-specific, internally prepared plan; accepts no arbitrary R expressions."""
from pathlib import Path
import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--plan', required=True, help='Internal plan generated from the request and source dictionary')
    parser.add_argument('--rscript', required=True)
    parser.add_argument('--output-parent', default='round7/private/runs')
    args = parser.parse_args()
    root = Path(args.workspace).resolve()
    sys.path.insert(0, str(root / 'scripts'))
    from research_runtime import run_r
    run, code = run_r(root, args.plan, Path(__file__).with_name('analyze.R'), args.rscript, args.output_parent)
    print(run)
    return code


if __name__ == '__main__':
    sys.exit(main())
