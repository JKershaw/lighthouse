#!/usr/bin/env python3
"""R-0014: checks of the piece's and record's smaller figures against the retained tables
(data/releases.csv, data/analysis/release_days.csv, project_outcomes.csv, ci_projects.csv,
crosscheck_pypistats.csv, read_log.csv). Output: piece_checks.txt beside it."""
import csv, os, statistics
from collections import defaultdict
STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(STUDY, 'data'); A = os.path.join(D, 'analysis')
rel = list(csv.DictReader(open(os.path.join(D, 'releases.csv'))))
days = list(csv.DictReader(open(os.path.join(A, 'release_days.csv'))))
po = {r['project']: r for r in csv.DictReader(open(os.path.join(A, 'project_outcomes.csv')))}

print('== the opening example: pandas 3.0.3 and requests 2.34.0')
for r in rel:
    if (r['project'], r['version']) in (('pandas', '3.0.3'), ('requests', '2.34.0')):
        print(r['project'], r['version'], 'uploaded', r['first_upload_utc'], 'next newest', r['next_newest_version'], 'hours to next', r['hours_to_next_newest'])
for r in days:
    if (r['project'], r['version']) in (('pandas', '3.0.3'), ('requests', '2.34.0')) and r['day'] in ('1', '30'):
        print(r['project'], r['version'], 'day', r['day'], r['date'], 'total', r['total'], 'at_or_newer', r['at_or_newer'], 'own', r['own'], 'share', r['share_at_or_newer'])
print('requests releases in window:', [r['version'] for r in rel if r['project'] == 'requests'])
print('pandas releases in window:', [r['version'] for r in rel if r['project'] == 'pandas'])

print('== hours left in day 0: median', statistics.median(float(r['hours_left_in_day0']) for r in rel))
print('== kinds:', {k: sum(r['kind'] == k for r in rel) for k in ('major', 'minor', 'patch')},
      'released again within 7d:', sum(r['released_again_within_7d'] == 'True' for r in rel),
      'yanked:', [(r['project'], r['version']) for r in rel if r['yanked'] == 'True'],
      'ci subsample:', sum(r['ci_subsample'] == 'True' for r in rel))
print('== single-release projects:', sorted(p for p in po if po[p]['releases'] == '1'), 'all reached:', all(po[p]['reached'] == '1' for p in po if po[p]['releases'] == '1'))
# days to half
first = {}
for r in days:
    k = (r['project'], r['version'])
    if r['status'] == 'known' and r['share_at_or_newer'] and float(r['share_at_or_newer']) >= 0.5 and k not in first:
        first[k] = int(r['day'])
print('== reached half by day 30:', len(first), 'on day 0:', sum(v == 0 for v in first.values()), 'median day:', statistics.median(first.values()))
lit = [v for k, v in first.items() if k[0] == 'litellm']
print('   litellm reaching:', len(lit), 'of', po['litellm']['releases'], 'median day', statistics.median(lit) if lit else None)
# eleven plateau: day-1 and day-2 medians, day-30 medians
sh = defaultdict(lambda: defaultdict(list))
for r in days:
    if r['status'] == 'known' and r['share_at_or_newer']:
        sh[r['project']][int(r['day'])].append(float(r['share_at_or_newer']))
print('== the eleven: median day-1, day-2, day-30 shares (per cent, two decimals)')
for p in sorted(po, key=lambda p: float(po[p]['median_day1_share'] or 9)):
    if po[p]['most_reached'] == 'no':
        print(f'   {p}: {statistics.median(sh[p][1])*100:.2f} {statistics.median(sh[p][2])*100:.2f} {statistics.median(sh[p][30])*100:.2f}')
print('== the 26: day-1 median range', min(statistics.median(sh[p][1]) for p in po if po[p]["most_reached"] == "yes"), max(statistics.median(sh[p][1]) for p in po if po[p]["most_reached"] == "yes"),
      'day-30 range', min(statistics.median(sh[p][30]) for p in po if po[p]["most_reached"] == "yes"), max(statistics.median(sh[p][30]) for p in po if po[p]["most_reached"] == "yes"))
print('== projects whose day-30 median is more than 10 points from day-1 median:',
      [(p, round(statistics.median(sh[p][1])*100, 1), round(statistics.median(sh[p][30])*100, 1)) for p in po if po[p]['releases'] != '0' and abs(statistics.median(sh[p][30]) - statistics.median(sh[p][1])) > 0.10])
print('== mixed projects:', [(p, po[p]['reached'], po[p]['releases']) for p in po if po[p]['most_reached'] == 'yes' and po[p]['reached'] != po[p]['releases']])
cp = sorted(csv.DictReader(open(os.path.join(A, 'ci_projects.csv'))), key=lambda r: float(r['median_diff_pp']))
print('== CI largest gaps:', [(r['project'], round(float(r['median_diff_pp']), 1), r['releases']) for r in cp[:6]], 'smallest:', [(r['project'], round(float(r['median_diff_pp']), 1)) for r in cp[-3:]])
cx = list(csv.DictReader(open(os.path.join(A, 'crosscheck_pypistats.csv'))))
print('== cross-check days', len(cx), 'identical', sum(r['rel_diff'] == '0.000000' for r in cx), 'largest', max(abs(float(r['rel_diff'])) for r in cx), 'pygments rows', [(r['date'], r['rel_diff']) for r in cx if r['project'] == 'pygments'])
log = list(csv.DictReader(open(os.path.join(D, 'read_log.csv'))))
print('== read log: rows read for C reads', sum(int(r['read_rows'] or 0) for r in log if r['label'].startswith('C')),
      'first G/V/C read', next(r['read_utc'] for r in log if r['label'][:1] in 'GVC'), 'last read', log[-1]['read_utc'],
      'reads by source', {s: sum(r['source'] == s for r in log) for s in {r['source'] for r in log}})
