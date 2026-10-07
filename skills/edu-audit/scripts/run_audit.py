"""Run inspected R adapter with contained read paths and a fresh output directory under ./edu_output/audit/."""
import argparse,datetime,hashlib,json,math,os,re,shutil,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'edu-shared'/'scripts'))
from edu_runtime import find_rscript

def contained(root,value):
    p=(root/value).resolve()
    if not p.is_relative_to(root):raise ValueError('Path leaves workspace')
    if not p.is_file():raise ValueError('Input file does not exist: '+str(p))
    return p

def run(root,config,rscript,out_parent=None):
    root=Path(root).resolve();cpath=contained(root,config)
    cfg=json.loads(cpath.read_text(encoding='utf-8'))
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}',cfg.get('case_id','')):raise ValueError('case_id must be a safe local identifier')
    if cfg.get('evidence_status') not in ['source_verified_summary','conditional_raw_descriptives','synthetic_test']:raise ValueError('Evidence status required')
    provenance={}
    for field in ['input','source_results']:
        p=contained(root,cfg[field]);provenance[field]={'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};cfg[field]=str(p)
    if cfg['mode']=='summary_counts' and not cfg.get('outcome_definition'):raise ValueError('Outcome definition required')
    if cfg['mode']=='descriptive_repeated':
        required=['id_column','group_column','groups','variables','na_strings','scale_min','scale_max','missing_policy','collapse','sd_denominator','scoring','standardization','sample_selection','interval_algorithm']
        if not all(k in cfg for k in required):raise ValueError('Required settings missing')
        for key in ['id_column','group_column','missing_policy','collapse','sd_denominator','scoring','standardization','sample_selection','interval_algorithm']:
            if not isinstance(cfg[key],str) or not cfg[key].strip():raise ValueError('Nonempty setting required: '+key)
        for key in ['groups','variables']:
            if not isinstance(cfg[key],list) or not cfg[key] or not all(isinstance(x,str) and x.strip() for x in cfg[key]) or len(set(cfg[key]))!=len(cfg[key]):raise ValueError('Unique nonempty string list required: '+key)
        if not isinstance(cfg['na_strings'],list) or not all(isinstance(x,str) for x in cfg['na_strings']):raise ValueError('Explicit missing-code list required')
        if not all(isinstance(cfg[k],(int,float)) and not isinstance(cfg[k],bool) and math.isfinite(cfg[k]) for k in ['scale_min','scale_max']) or cfg['scale_min']>=cfg['scale_max']:raise ValueError('Documented finite scale bounds required')
        if cfg['standardization']!='none':raise ValueError('Standardization adapter unavailable')
        if 'expected_participants_by_group' in cfg:
            expected=cfg['expected_participants_by_group']
            if not isinstance(expected,dict) or set(expected)!=set(cfg['groups']) or not all(isinstance(n,int) and not isinstance(n,bool) and n>0 for n in expected.values()):raise ValueError('Expected group counts must cover configured groups with positive integers')
    parent=(root/(out_parent or 'edu_output/audit')).resolve()
    if not parent.is_relative_to(root):raise ValueError('Output leaves workspace')
    parent.mkdir(parents=True,exist_ok=True)
    ident=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'_'+cfg['case_id']
    runroot=parent/ident;runroot.mkdir();out=runroot/'output'
    for field in ['input','source_results']:
        target=field+'.csv'
        shutil.copyfile(cfg[field],runroot/target)
        cfg[field]=target
    (runroot/'analysis_config.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2),encoding='utf-8')
    (runroot/'input_provenance.json').write_text(json.dumps(provenance,indent=2),encoding='utf-8')
    shutil.copyfile(cpath,runroot/'original_config.json')
    r=Path(find_rscript(rscript) or '')
    if not r.is_file():
        (runroot/'run_status.json').write_text(json.dumps({'status':'not_executed','reason':'Rscript unavailable'}));return runroot,2
    script=Path(__file__).with_name('recheck.R');shutil.copyfile(script,runroot/'recheck.R')
    cmd=[str(r),'--vanilla','recheck.R','--config','analysis_config.json','--out','output']
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    env=os.environ.copy()
    if os.name=='nt':
        for key in ['LANG','LC_ALL','LC_CTYPE']:env[key]='English_United States.utf8'
    try:
        proc=subprocess.run(cmd,capture_output=True,timeout=120,cwd=runroot,env=env)
        (runroot/'stdout.log').write_bytes(proc.stdout);(runroot/'stderr.log').write_bytes(proc.stderr)
        status={'status':'completed' if proc.returncode==0 else 'failed','returncode':proc.returncode,'started_utc':started,'command':cmd,'r_script_sha256':hashlib.sha256(script.read_bytes()).hexdigest()}
        code=proc.returncode
        status['child_locale']=env.get('LC_ALL','system_default')
        status['r_library']=env.get('R_LIBS_USER','system_default')
    except (OSError,subprocess.TimeoutExpired) as e:
        status={'status':'failed','reason':str(e),'started_utc':started};code=2
    (runroot/'run_status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2),encoding='utf-8')
    return runroot,code

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--workspace',default='.');p.add_argument('--config',required=True);p.add_argument('--rscript');a=p.parse_args()
    try: path,code=run(a.workspace,a.config,a.rscript);print(path);sys.exit(code)
    except (ValueError,KeyError,json.JSONDecodeError) as e:print(str(e),file=sys.stderr);sys.exit(2)
