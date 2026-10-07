"""Source-backed summary/interval plots and explicitly classified diagrams; no estimation."""
import csv
import json
import math
from pathlib import Path
import textwrap


def finite(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError('Plot values must be finite reported or previously computed numbers')
    return value


def validate_spec(spec):
    if not spec.get('source') or not spec.get('locator') or not spec.get('conclusion'):
        raise ValueError('Figure needs source, locator and a supported visual conclusion')
    kind = spec['kind']
    if kind in ('group_means', 'estimate_intervals', 'trajectory', 'prediction_curve'):
        if spec.get('source_kind') not in ('published_summary', 'existing_analysis', 'real_data'):
            raise ValueError('Statistical plot requires real source data or existing output')
        if not spec.get('units'):
            raise ValueError('Statistical plot needs units')
    if kind == 'group_means':
        if not spec.get('panels'):
            raise ValueError('No result panels')
        for panel in spec['panels']:
            if not panel.get('rows'):
                raise ValueError('No reported means')
            keys = [(r['group'], r['condition']) for r in panel['rows']]
            if len(keys) != len(set(keys)):
                raise ValueError('Duplicate group/condition means')
            for row in panel['rows']:
                finite(row['mean'])
                if 'n' in row and (not isinstance(row['n'], int) or row['n'] <= 0):
                    raise ValueError('n must describe a real positive sample size')
    elif kind == 'estimate_intervals':
        for row in spec['rows']:
            low, estimate, high = map(finite, [row['low'], row['estimate'], row['high']])
            if not low <= estimate <= high:
                raise ValueError('Interval must contain the estimate')
        if not spec.get('interval_definition'):
            raise ValueError('Interval level and original algorithm must be recorded')
    elif kind == 'prediction_curve':
        if not spec.get('interval_definition') or not spec.get('x_units') or spec.get('prediction_kind') != 'fixed_effect_population_mean':
            raise ValueError('Prediction curve needs fixed-effect population mean, predictor units and interval definition')
        if not spec.get('rows'):
            raise ValueError('Actual saved prediction rows required')
        last = {}
        for row in spec['rows']:
            x, low, mean, high = map(finite, [row['x'], row['low'], row['mean'], row['high']])
            if not row.get('group') or x <= last.get(row['group'], -math.inf) or not low <= mean <= high:
                raise ValueError('Within-group increasing predictor values and mean-containing intervals required')
            last[row['group']] = x
    elif kind == 'trajectory':
        if not spec.get('interval_definition') or spec.get('trajectory_kind') != 'model_population_mean':
            raise ValueError('Trajectory must explicitly identify model population mean and pointwise interval algorithm')
        if not spec.get('x_units') or not spec.get('rows'):
            raise ValueError('Elapsed-time units and actual saved prediction rows required')
        previous = -math.inf
        for row in spec['rows']:
            x, low, mean, high = map(finite, [row['time'], row['low'], row['mean'], row['high']])
            if x <= previous or not low <= mean <= high:
                raise ValueError('Strictly increasing elapsed times and mean-containing intervals required')
            previous = x
    elif kind in ('flow', 'framework', 'themes'):
        nodes = spec['nodes']
        ids = [n['id'] for n in nodes]
        if not nodes or len(ids) != len(set(ids)):
            raise ValueError('Diagram nodes must have unique identifiers')
        if spec.get('evidence_status') not in ('procedure', 'conceptual', 'hypothesized', 'reported_association', 'candidate_themes'):
            raise ValueError('Diagram relationships need an explicit evidence status')
        if kind == 'themes' and spec['evidence_status'] != 'candidate_themes':
            raise ValueError('AI themes remain candidate interpretations')
        for edge in spec.get('edges', []):
            if edge['from'] not in ids or edge['to'] not in ids:
                raise ValueError('Diagram edge points to an unknown node')
            if edge.get('relation', 'influence') not in ('influence', 'association', 'sequence', 'hypothesized', 'candidate'):
                raise ValueError('Edge relation must be influence, association, sequence, hypothesized or candidate')
    else:
        raise ValueError('Unsupported figure kind; no fake scatter, distributions or trajectories')


def render(spec, destination):
    validate_spec(spec)
    # Lazy import: installation and ordinary prose editing never require plotting packages.
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, Ellipse
    # Chinese labels need a CJK font; listing installed families lets matplotlib fall back glyph by glyph.
    from matplotlib import font_manager
    installed = {f.name for f in font_manager.fontManager.ttflist}
    cjk = [f for f in ['Microsoft YaHei', 'SimHei', 'Noto Sans CJK SC', 'Source Han Sans SC', 'PingFang SC',
                       'Heiti SC', 'WenQuanYi Micro Hei'] if f in installed][:1]
    matplotlib.rcParams.update({'font.family': ['DejaVu Sans'] + cjk, 'axes.unicode_minus': False,
                                 'font.size': 10,
                                 'svg.fonttype': 'none', 'pdf.fonttype': 42,
                                 'axes.spines.top': False, 'axes.spines.right': False})
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    records = []
    kind = spec['kind']
    if kind == 'group_means':
        panels = spec['panels']
        fig, axes = plt.subplots(1, len(panels), figsize=(7.2, 3.9), squeeze=False)
        palette = ['#59788E', '#C7CDD2', '#BF9856', '#7C718A']
        for index, panel in enumerate(panels):
            ax = axes[0, index]
            groups = list(dict.fromkeys(r['group'] for r in panel['rows']))
            conditions = list(dict.fromkeys(r['condition'] for r in panel['rows']))
            width = .72 / len(conditions)
            for j, condition in enumerate(conditions):
                for i, group in enumerate(groups):
                    row = next((r for r in panel['rows'] if r['group'] == group and r['condition'] == condition), None)
                    if row is None:
                        continue  # missing combinations are not fabricated as zero
                    x = i + (j - (len(conditions) - 1) / 2) * width
                    ax.bar(x, row['mean'], width=width * .92, color=palette[j % len(palette)],
                           edgecolor='black', linewidth=.4, hatch=['', '//', '..', 'xx'][j % 4],
                           label=condition if i == 0 else None)
                    ax.text(x, row['mean'] + 1.7, f"{row['mean']:g}", ha='center', va='bottom', fontsize=10)
                    records.append({'panel': panel['title'], **row})
            ax.set_xticks(range(len(groups)), groups)
            ax.set_ylabel(spec['units'])
            ax.set_title(chr(97 + index) + '  ' + panel['title'], loc='left', fontweight='bold')
            if 'limits' in spec:
                ax.set_ylim(*spec['limits'])
            else:
                ax.set_ylim(0, max(r['mean'] for r in panel['rows']) * 1.2)
            ax.legend(fontsize=8, loc='upper right')
    elif kind == 'estimate_intervals':
        fig, ax = plt.subplots(figsize=(7.2, max(3, .5 * len(spec['rows']))))
        for i, row in enumerate(spec['rows']):
            ax.errorbar(row['estimate'], i,
                        xerr=[[row['estimate'] - row['low']], [row['high'] - row['estimate']]],
                        fmt='o', color='#59788E', capsize=4)
            records.append(row)
        ax.set_yticks(range(len(spec['rows'])), [r['label'] for r in spec['rows']])
        ax.set_xlabel(spec['units'])
        if spec.get('reference_line') is not None:
            ax.axvline(finite(spec['reference_line']), color='#888888', linestyle='--')
    elif kind == 'prediction_curve':
        fig, ax = plt.subplots(figsize=(7.2, 4.1))
        for i, group in enumerate(dict.fromkeys(r['group'] for r in spec['rows'])):
            rows = [r for r in spec['rows'] if r['group'] == group]
            x = [r['x'] for r in rows]
            color = ['#59788E', '#BF9856', '#7C718A'][i % 3]
            ax.plot(x, [r['mean'] for r in rows], marker=['o','s','^'][i%3], linestyle=['-','--',':'][i%3], color=color, label=group)
            ax.fill_between(x, [r['low'] for r in rows], [r['high'] for r in rows], color=color, alpha=.13)
            records.extend(rows)
        ax.set_xlabel(spec['x_units']); ax.set_ylabel(spec['units']); ax.legend(frameon=False, fontsize=8)
    elif kind == 'trajectory':
        fig, ax = plt.subplots(figsize=(7.2, 4.1))
        rows = spec['rows']
        times = [r['time'] for r in rows]
        ax.plot(times, [r['mean'] for r in rows], 'o-', color='#59788E', label='Model population mean')
        ax.fill_between(times, [r['low'] for r in rows], [r['high'] for r in rows], color='#59788E', alpha=.18,
                        label='Pointwise mean confidence interval')
        ax.set_xlabel(spec['x_units']); ax.set_ylabel(spec['units'])
        ax.set_xticks(times); ax.legend(frameon=False, fontsize=8)
        records.extend(rows)
    else:
        fig, ax = plt.subplots(figsize=(7.2, 5))
        nodes = spec['nodes']
        positions = {n['id']: (n.get('x', .5), n.get('y', .87 - i * .7 / max(1, len(nodes) - 1)))
                     for i, n in enumerate(nodes)}
        patches = {}
        for node in nodes:
            x, y = positions[node['id']]
            finite(x); finite(y)
            width, height = spec.get('node_width', .36), spec.get('node_height', .12)
            if node.get('measurement_kind') == 'latent':
                patches[node['id']] = ax.add_patch(Ellipse((x, y), width, height, facecolor='#E4EAF0', edgecolor='#59788E'))
            else:
                padding='.01' if 'node_width' in spec or 'node_height' in spec else '.02'
                patches[node['id']] = ax.add_patch(FancyBboxPatch((x-width/2,y-height/2),width,height,boxstyle='round,pad='+padding,
                                            facecolor='#E4EAF0',edgecolor='#59788E'))
            wrap = 14 if any('一' <= ch <= '鿿' for ch in node['label']) else 28
            ax.text(x, y, textwrap.fill(node['label'], wrap), ha='center', va='center', fontsize=9)
            records.append(node)
        for edge in spec.get('edges', []):
            start, end = positions[edge['from']], positions[edge['to']]
            # Per-edge relation: influence/association solid, sequence (process order) grey with a hollow head,
            # hypothesized or candidate relations dashed. Without 'relation' the diagram-level status decides.
            relation = edge.get('relation', 'hypothesized' if spec['evidence_status'] in ('hypothesized', 'candidate_themes') else 'influence')
            style = '--' if relation in ('hypothesized', 'candidate') else '-'
            head, color = ('-|>', '#888888') if relation == 'sequence' else ('->', '#333333')
            ax.annotate('', xy=end, xytext=start, arrowprops={'arrowstyle': head, 'color': color, 'linestyle': style,
                                                            'patchA': patches[edge['from']], 'patchB': patches[edge['to']],
                                                            'shrinkA': 2, 'shrinkB': 2, 'connectionstyle': edge.get('connection', 'arc3,rad=0')})
            if edge.get('label'):
                ax.text((start[0] + end[0]) / 2, (start[1] + end[1]) / 2, edge['label'], fontsize=8,
                        bbox={'facecolor': 'white', 'edgecolor': 'none'}, ha='center')
        if spec.get('show_status', True):
            zh = {'procedure': '流程', 'conceptual': '概念关系', 'hypothesized': '待检验假设', 'reported_association': '已报告的关联', 'candidate_themes': '候选主题关系'}
            label = ('关系性质：' + zh[spec['evidence_status']]) if spec.get('language') == 'zh' else 'Relationship status: ' + spec['evidence_status'].replace('_', ' ')
            ax.text(.02, .025, label, fontsize=9)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    fig.tight_layout()
    for extension in ['svg', 'pdf', 'png']:
        fig.savefig(destination / ('figure.' + extension), dpi=400, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    (destination / 'spec.json').write_bytes((json.dumps(spec, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    columns = list(dict.fromkeys(k for r in records for k in r))
    with (destination / 'source_data.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader(); writer.writerows(records)
    return {'kind': kind, 'source': spec['source'], 'locator': spec['locator'],
            'conclusion': spec['conclusion'], 'extra_analysis': False,
            'statistical_note': spec.get('statistical_note', spec.get('evidence_status')),
            'files': ['figure.svg', 'figure.pdf', 'figure.png', 'spec.json', 'source_data.csv']}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--spec', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(render(json.loads(args.spec.read_text(encoding='utf-8')), args.output), indent=2))
