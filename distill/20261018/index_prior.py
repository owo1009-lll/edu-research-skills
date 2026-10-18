"""Index available pre-round source records; a citation alone is not a full reading."""
import json
from pathlib import Path
import re
import subprocess
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
BASELINE = 'a4020c41a4f3d8ab180a4e2818955d90e40f6f3b'
HERE = Path(__file__).parent


def normalized(value):
    return re.sub(r'[^\w]', '', unicodedata.normalize('NFKC', value).lower())


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def main():
    prior = []
    for name in ['distill/manifest_en.json', 'distill/manifest_zh.json']:
        for item in read(name):
            prior.append({k: item.get(k) for k in ['id', 'doi', 'title', 'authors', 'year', 'design']} | {'record': name})
    for file in sorted((ROOT / 'skills/edu-writing/references/sources').glob('*.json')):
        item = json.loads(file.read_text(encoding='utf-8'))
        prior.append({k: item.get(k) for k in ['id', 'doi', 'title', 'status', 'body_coverage']} | {'record': file.relative_to(ROOT).as_posix()})
    split_name = 'evals/capability-20261013/distillation/split.json'
    for group in ['training', 'holdout']:
        for item in read(split_name)[group]:
            if item.get('type', '').startswith('synthetic'):
                continue
            prior.append(item | {'record': split_name, 'historical_role': group, 'current_role': 'prior_exposure'})
    # Restore identities explicitly supplied by the existing method cards.
    for item in read('distill/20261018/sources.json')['sources']:
        if 'reuse' in item['prior_use'].lower():
            prior.append({k: item.get(k) for k in ['id', 'doi', 'title', 'prior_use']} | {'record': 'existing method cards; reconstructed identity'})
    paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASELINE], cwd=ROOT).decode().splitlines()
    texts = {}
    for path in paths:
        if path.endswith(('.md', '.json')) and (path.startswith('skills/') or path.startswith('distill/') or path.startswith('evals/')):
            texts[path] = subprocess.check_output(['git', 'show', f'{BASELINE}:{path}'], cwd=ROOT).decode('utf-8')
    historical_markers = {}
    for path, body in texts.items():
        if '/references/methods/' in path:
            for marker in set(re.findall(r'\bW\d{2}\b', body)):
                historical_markers.setdefault(marker, []).append(path)
    candidates = read('distill/20261018/new-sources.json')['sources']
    candidates += [x for x in read('distill/20261018/sources.json')['sources'] if x['id'] == 'E06']
    novelty = []
    for item in candidates:
        matches = [p for p in prior if (p.get('doi') and p['doi'].lower() == item['doi'].lower()) or (p.get('title') and normalized(p['title']) == normalized(item['title']))]
        mentions = [path for path, body in texts.items() if item['doi'].lower() in body.lower() or normalized(item['title']) in normalized(body)]
        novelty.append({'id': item['id'], 'doi': item['doi'], 'title': item['title'], 'prior_source_matches': matches,
                        'text_mentions': mentions, 'status': 'prior_source' if matches else 'not_found_in_available_prior_source_records'})
    result = {'baseline': BASELINE,
              'scope': '77 original corpus records, six current source records, earlier training/holdout exposure, reconstructed method-card identities; searched all baseline skills/distill/evals Markdown and JSON for candidate DOI/title mentions.',
              'limitation': 'Several W-series identities are missing from available records. The private development repository HEAD 27cbb4758d0c27a152c959316589f89c37397793 exposes the same original manifests and six source cards but no W-series manifest. Absence here establishes novelty relative to available records, not proof of no prior reading in a lost session.',
              'historical_w_markers': historical_markers, 'prior_records': prior, 'candidate_comparison': novelty}
    (HERE / 'prior-index.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'prior_records': len(prior), 'historical_w_markers': len(historical_markers), 'candidates': [{k: x[k] for k in ['id', 'status', 'text_mentions']} for x in novelty]}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
