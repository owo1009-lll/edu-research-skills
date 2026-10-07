"""Execute an assistant-prepared advanced plan with immutable, project-local R runs."""
import argparse
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workspace', required=True, type=Path)
    parser.add_argument('--plan', required=True)
    parser.add_argument('--rscript', required=True)
    parser.add_argument('--output-parent', default='round13/private/runs')
    args = parser.parse_args()
    sys.path.insert(0, str(args.workspace.resolve() / 'scripts'))
    from research_runtime import run_r
    directory, code = run_r(args.workspace, args.plan, Path(__file__).with_name('advanced.R'),
                            args.rscript, args.output_parent)
    print(directory)
    return code


if __name__ == '__main__':
    raise SystemExit(main())
