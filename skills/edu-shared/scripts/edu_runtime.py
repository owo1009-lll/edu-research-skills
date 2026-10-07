"""Shared runtime for the edu-* skills: locate R, create output folders, run R with a provenance record.

Outputs go to <current project>/edu_output/<kind>/<UTC stamp>-<slug>/, never into the skill folder.
"""
from pathlib import Path
import datetime
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import uuid

WRAPPER = r'''
script <- Sys.getenv("EDU_SCRIPT")
status <- tryCatch({ source(script, echo = FALSE, encoding = "UTF-8"); 0 },
                   error = function(e) { message("ERROR: ", conditionMessage(e)); 1 })
writeLines(capture.output(sessionInfo()), "sessionInfo.txt")
writeLines(.libPaths(), "library_paths.txt")
quit(save = "no", status = status)
'''


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def find_rscript(explicit=None):
    """Explicit path, then EDU_RSCRIPT, PATH, and the usual install locations."""
    candidates = [explicit, os.environ.get('EDU_RSCRIPT'), shutil.which('Rscript')]
    if os.name == 'nt':
        for root in (os.environ.get('ProgramFiles', r'C:\Program Files'), os.environ.get('LOCALAPPDATA', '')):
            found = sorted(glob.glob(os.path.join(root, 'R', 'R-*', 'bin', 'Rscript.exe')),
                           key=lambda p: [int(x) for x in re.findall(r'\d+', Path(p).parents[1].name)])
            candidates += found[::-1]
    else:
        candidates += ['/usr/local/bin/Rscript', '/opt/homebrew/bin/Rscript',
                       '/Library/Frameworks/R.framework/Resources/bin/Rscript', '/usr/bin/Rscript']
    for c in candidates:
        if c and Path(c).is_file():
            return str(Path(c))
    return None


def new_run_dir(kind, slug, base=None):
    base = Path(base) if base else Path.cwd() / 'edu_output'
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    slug = re.sub(r'[^\w-]+', '-', slug or 'run', flags=re.UNICODE).strip('-')[:40] or 'run'
    run = base / kind / f'{stamp}-{slug}-{uuid.uuid4().hex[:6]}'
    run.mkdir(parents=True)
    return run


def run_r(script, run_dir, args=(), inputs=(), helpers=(), rscript=None, timeout=1800):
    """Copy script/inputs/helpers into run_dir, run it there, and record what happened.

    The script runs through a wrapper that always saves sessionInfo.txt, even after an error.
    Returns the R exit code (0 = success). Failed runs are kept, not overwritten.
    """
    run_dir = Path(run_dir)
    (run_dir / 'inputs').mkdir(exist_ok=True)
    shutil.copy2(script, run_dir / 'analysis.R')
    for h in helpers:
        shutil.copy2(h, run_dir / Path(h).name)
    provenance = {'script': {'source': str(Path(script).resolve()), 'sha256': sha256(script)},
                  'helpers': {Path(h).name: sha256(h) for h in helpers}, 'inputs': {}}
    for i in inputs:
        target = run_dir / 'inputs' / Path(i).name
        shutil.copy2(i, target)
        provenance['inputs'][Path(i).name] = {'source': str(Path(i).resolve()), 'sha256': sha256(i)}
    (run_dir / '_wrapper.R').write_text(WRAPPER, encoding='utf-8')
    executable = find_rscript(rscript)
    status = {'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'rscript': executable,
              'args': list(args)}
    if not executable:
        status.update(status='not_executed', reason='Rscript not found; install R or set EDU_RSCRIPT', returncode=2)
    else:
        env = os.environ.copy()
        env['EDU_SCRIPT'] = 'analysis.R'
        if os.name == 'nt':
            for name in ('LANG', 'LC_ALL', 'LC_CTYPE'):
                env[name] = 'English_United States.utf8'
        command = [executable, '--vanilla', '_wrapper.R', *map(str, args)]
        try:
            proc = subprocess.run(command, cwd=run_dir, env=env, capture_output=True, timeout=timeout)
            (run_dir / 'stdout.log').write_bytes(proc.stdout)
            (run_dir / 'stderr.log').write_bytes(proc.stderr)
            status.update(status='completed' if proc.returncode == 0 else 'failed', returncode=proc.returncode)
        except (OSError, subprocess.TimeoutExpired) as error:
            (run_dir / 'stderr.log').write_text(str(error), encoding='utf-8')
            status.update(status='failed', reason=str(error), returncode=2)
    status['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    (run_dir / 'provenance.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2), encoding='utf-8')
    (run_dir / 'run_status.json').write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding='utf-8')
    return status['returncode']


if __name__ == '__main__':
    # `python edu_runtime.py` prints the Rscript that the skills will use (or explains how to set it).
    found = find_rscript()
    print(found or 'Rscript not found: install R (https://cran.r-project.org) or set EDU_RSCRIPT to Rscript.exe')
