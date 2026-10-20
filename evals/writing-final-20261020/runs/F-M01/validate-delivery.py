import hashlib, json, pathlib, re
root = pathlib.Path(r'@experiment')
out = root / 'runs' / 'F-M01'
skill = root / 'snapshot' / 'skills'
inputs = pathlib.Path(r'@inputs\F-M01')
request = inputs.parent.parent / 'request.md'
p = {
 'request': request, 'skill': skill/'edu-writing/SKILL.md',
 'argument': skill/'edu-writing/references/argument.md',
 'framing': skill/'edu-writing/references/framing-results.md',
 'voice': skill/'edu-writing/references/voice-en.md',
 'integrity': skill/'edu-shared/references/integrity.md',
 'bridge': skill/'edu-writing/references/analysis-bridge.md',
 'quant': skill/'edu-writing/references/quantitative-discussion.md',
 'qual': skill/'edu-writing/references/qualitative-narrative.md',
 'foundation': skill/'edu-writing/references/foundation.md',
 'voicepy': skill/'edu-writing/scripts/check_voice.py',
 'prosepy': skill/'edu-writing/scripts/check_prose.py',
 'new': inputs/'new-evidence.md', 'original': inputs/'revision-original.md',
 'context': inputs/'revision-context.md'
}
events = [
 ('request','instructions'), ('skill','instructions'),
 *[(x,'new: evidence and planning; batch display partly truncated') for x in ['argument','framing','voice','integrity','new']],
 *[(x,'new: route reading; voice and integrity reread after truncated batch') for x in ['voice','integrity','bridge','quant','qual']],
 ('new','new: full evidence display reread; middle truncated'),
 ('new','new: recover truncated middle lines 355-850'),
 ('voicepy','new: inspect required checks'),('prosepy','new: inspect required checks; display partly truncated'),
 *[(x,'new: first-draft automated checks; runtime read') for x in ['voicepy','new','prosepy']],
 *[(x,'revise: initial reading after new final saved; context display partly truncated') for x in ['foundation','original','context']],
 ('context','revise: targeted recovery of PDF pages 13-16 after truncated display'),
 *[(x,'revise: first-edit automated checks; runtime read') for x in ['voicepy','original','context','prosepy']],
 *[(x,'delivery: new final automated check; runtime read, no edits') for x in ['voicepy','new','prosepy']],
 *[(x,'delivery: revise final automated check; runtime read, no edits') for x in ['voicepy','context','prosepy']]
]
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest().upper()
log = [dict(order=i,path=str(p[key]),sha256=sha(p[key]),stage=stage) for i,(key,stage) in enumerate(events,1)]
(out/'read-log.json').write_text(json.dumps(log,indent=2,ensure_ascii=False),encoding='utf-8')
report = json.loads((out/'completion-report.json').read_text(encoding='utf-8-sig'))
report['read_log_serialization_repair'] = 'The PowerShell JSON append method nested arrays and truncated older entries at serialization depth. Rebuilt the ordered 33-event log directly from actual tool-call history with current file hashes. Original malformed log preserved. No source or final manuscript was edited.'
report['all_read_files_hashes_unchanged'] = 'No source writes performed. Current hashes recorded; earlier nested log did not preserve all initial hashes in readable form, so independent before/after verification of every initial hash is unavailable.'
report['read_log_entries'] = len(log)
report['final_check_disposition'] = 'New discussion: low citation density and absent self-mentions retained deliberately; no unread literature added. Revision: no prose prompts. Voice checks found no unsupported numbers, stacked hedges, or semantic equivalence cues in either final. These are AI checks, not expert validation.'
for check in report['checks']:
 path=out/check['task']/'final.md'
 saved=json.loads((out/check['task']/'completion.json').read_text(encoding='utf-8-sig'))
 assert sha(path)==saved['final_sha256']
 assert sha(path)==check['final_sha256']
for e in log:
 assert e['sha256']==sha(pathlib.Path(e['path']))
(out/'completion-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'read_log_events':len(log),'finals_unchanged':True,'words':[x['words'] for x in report['checks']]},indent=2))
