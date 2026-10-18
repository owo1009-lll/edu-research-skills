"""Record actual task resource use and verify local UTF-8 deliverables."""
from pathlib import Path
import json

out = Path(__file__).resolve().parent
skill = Path('C:/Users/Administrator/Downloads/edu-writing-snapshot-p01-20261018/skills/edu-writing')
inputs = Path('C:/Users/Administrator/Downloads/edu-research-skills-work/evals/writing-20261018/inputs')

def entry(path, purpose, mode='UTF-8 text read'):
    return {'path': str(path).replace('\\', '/'), 'purpose': purpose, 'access': mode}

resources = [
    entry(skill / 'SKILL.md', 'Follow the explicitly supplied edu-writing revision, artifact and checking workflow.'),
    entry(inputs / 'H7-request.md', 'Identify the revision scope, English audience, 650–800-word limit, evidence restrictions and required artifacts.'),
    entry(inputs / 'H7-materials.md', 'Read the original published excerpt, attributed provenance and sole permitted factual packet; also used as the voice checker source.'),
    entry(skill / 'references/foundation.md', 'Preserve the original argument and supported judgments; classify consequential revisions.'),
    entry(skill / 'references/argument.md', 'Plan contribution, evidence levels, qualifications and cross-section claim alignment.'),
    entry(skill / 'references/voice-en.md', 'Calibrate English finding statements, explanations and recommendations; reread fully after a truncated batch output.'),
    entry(skill / 'references/framing-results.md', 'Check grade comparisons, non-significance and unsupported mechanism claims; reread fully after a truncated batch output.'),
    entry(skill / 'references/quantitative-discussion.md', 'Integrate the reported grade pattern with interpretation and rival explanations.'),
    entry(skill / 'references/qualitative-narrative.md', 'Preserve participant accounts and avoid implying independent qualitative recoding.'),
    entry(skill / 'references/conclusion-implications.md', 'Keep conclusions consistent and retain grounded practical judgments.'),
    entry(skill.parent / 'edu-shared/references/integrity.md', 'Apply attribution, nonfabrication and AI-self-review distinctions.'),
    entry(skill / 'references/methods/cases-develop-explanations.md', 'Use source accounts to explain delayed relevance without manufacturing within-person trajectories.'),
    entry(skill / 'scripts/check_voice.py', 'Inspect command arguments/imports/read-write behavior and execute the required stance/source-number check.', 'UTF-8 rg inspection; Python -X utf8 execution'),
    entry(skill / 'scripts/check_prose.py', 'Inspect command arguments/imports/read-write behavior and execute the required prose-cue check.', 'UTF-8 rg inspection; Python -X utf8 execution'),
    entry(skill / 'scripts/check_consistency.py', 'Inspect command arguments/imports/read-write behavior and execute the required two-section consistency check.', 'UTF-8 rg inspection; Python -X utf8 execution'),
]

own_reads = {
    'first.md': 'Read by all three check scripts and the word counter; final artifact verification.',
    'final.md': 'Read by all three check scripts and the word counter, directly inspected for final coherence, and final artifact verification.',
    'review.md': 'UTF-8 final artifact verification after recording substantive AI review and cue adjudication.',
    'rationale.md': 'UTF-8 final artifact verification of argument/evidence/term/source-query records.',
    'change_log.md': 'UTF-8 final artifact verification of consequential edits.',
    'loads.json': 'Parse and verify the resource manifest in this script.',
    'run_checks.py': 'Executed to run supplied checks and calculate word counts; UTF-8 final artifact verification.',
    'record_loads.py': 'Executed to record resource use and verify artifacts; UTF-8 final artifact verification.',
    'first_voice.txt': 'Read the actual first-draft cues and adjudicate them in review.md.',
    'first_prose.txt': 'Read the actual first-draft prose metrics/prompts and adjudicate them in review.md.',
    'first_consistency.txt': 'Read the actual first-draft consistency output and compare with manual review.',
    'final_voice.txt': 'Read both final-run outputs, including the rerun after local corrections; adjudicate the retained cues.',
    'final_prose.txt': 'Read both final-run outputs, including the rerun; adjudicate low citation density and word-count method.',
    'final_consistency.txt': 'Read both final-run outputs, including the rerun; confirm successful execution and supplement with manual review.',
    'first_checks.json': 'Parse exact first-check commands, exits and word-count results during final verification.',
    'final_checks.json': 'Parse exact final-check commands, exits and final word-count results during final verification.',
    'final_verification.json': 'Read the final saved artifact-verification report before delivery.',
}

manifest = {
    'task': 'H7 attributed secondary Discussion and Conclusion revision',
    'output_directory': str(out).replace('\\', '/'),
    'model_identity': 'unavailable',
    'model_settings': 'unavailable',
    'model_metadata_note': 'No reliable served-model identifier, decoding settings or reasoning setting was exposed as runtime metadata; none is inferred.',
    'encoding': 'UTF-8; all Python checks executed with -X utf8; bytecode writes disabled.',
    'resource_log_scope': 'Task content/instruction/script reads and generated artifacts; standard-library and operating-system runtime loading are not content-resource reads.',
    'external_resources_read': resources,
    'generated_artifacts_read': [entry(out / name, reason, 'UTF-8 read or Python -X utf8 execution as specified') for name, reason in own_reads.items()],
    'failed_read_attempts': [
        {'description': 'An initial PowerShell array expression combined the eight intended reference paths into one invalid path; Get-Content returned file-not-found and no content was read. The command was corrected to join each relative path separately.'}
    ],
    'restrictions_observed': {
        'network_used': False,
        'other_runs_read': False,
        'evaluation_or_development_reports_read': False,
        'other_installed_skills_read': False,
        'subagents_spawned': False,
        'skills_or_inputs_modified': False,
        'all_outputs_within_designated_new_directory': True,
    },
    'scope_limitations': [
        'Only the supplied factual packet and published excerpt support research claims.',
        'The original article and theoretical originals were not independently accessed.',
        'No raw data or qualitative transcripts were reanalyzed.',
        'Course-availability discrepancy and incomplete gender analysis remain unresolved in work records.',
        'AI review and check execution do not constitute expert review or original-author approval.',
    ],
}
(out / 'loads.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

checked = []
for name in own_reads:
    if name == 'final_verification.json':
        continue
    content = (out / name).read_text(encoding='utf-8')
    assert content.strip(), name
    if name.endswith('.json'):
        parsed = json.loads(content)
        if name in ('first_checks.json', 'final_checks.json'):
            assert all(item['returncode'] == 0 for item in parsed['checks']), name
            assert parsed['word_counts']['within_650_800'], name
    checked.append(name)

final_report = json.loads((out / 'final_checks.json').read_text(encoding='utf-8'))
verification = {
    'files_verified_as_nonempty_utf8': checked,
    'external_resource_count': len(resources),
    'required_deliverables_present': all((out / name).is_file() for name in ('first.md', 'review.md', 'final.md', 'rationale.md', 'change_log.md', 'loads.json')),
    'all_six_required_check_executions_returned_zero': True,
    'final_word_counts': final_report['word_counts'],
    'final_check_outputs_inspected': True,
    'qualitative_status': 'AI self-review and source-packet comparison; not expert review or new research analysis',
}
(out / 'final_verification.json').write_text(json.dumps(verification, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(verification, ensure_ascii=False, indent=2))
