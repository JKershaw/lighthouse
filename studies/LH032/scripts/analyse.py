#!/usr/bin/env python3
"""LH032: walk the full history of a clone of NCSC-NL/php2shell, parse every software list table at every commit,
and write per-entry first appearance and status changes, with counts at HEAD.
Usage: analyse.py <clone path> <read label>"""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import json
import re
import subprocess
import sys

CLONE, LABEL = Path(sys.argv[1]), sys.argv[2]
OUT = Path(__file__).resolve().parents[1] / 'data' / ('read-' + LABEL)
OUT.mkdir(parents=True, exist_ok=True)
PHP_RELEASE = datetime(2026, 10, 21, 13, 30, tzinfo=timezone.utc)  # CERT-EU's reported release time (LH024)


def git(*args):
    return subprocess.run(['git', '-C', str(CLONE), *args], capture_output=True, text=True, check=True).stdout


def entries_at(commit):
    files = [f for f in git('ls-tree', '-r', '--name-only', commit).split('\n')
             if re.fullmatch(r'software/software_list(_[0-9a-z-]+)?\.md', f)]
    out = {}
    for f in files:
        header = None
        for line in git('show', f'{commit}:{f}').split('\n'):
            if not line.startswith('|'):
                continue
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if cells and cells[0].lower() == 'supplier':
                header = [c.lower() for c in cells]
                continue
            if header is None or set(''.join(cells)) <= set(':- '):
                continue
            row = dict(zip(header, cells))
            key = (row.get('supplier', ''), row.get('product', ''))
            if key[0]:
                statuses = tuple(v for k, v in row.items() if k.startswith('status'))
                out[key] = {'status': statuses, 'version': row.get('version (see status)', row.get('version', '')),
                            'links': row.get('links', '')}
    return out


commits = [l.split(' ', 1) for l in git('log', '--reverse', '--format=%H %cI').strip().split('\n')]
first, changes, previous = {}, {}, {}
for sha, when in commits:
    current = entries_at(sha)
    for key, value in current.items():
        if key not in first:
            first[key] = when
        if previous.get(key, {}).get('status') != value['status']:
            changes.setdefault(key, []).append({'commit': sha[:12], 'time': when, 'status': list(value['status'])})
    previous = current
head_sha, head_time = commits[-1]
head = previous


def hours(when):
    return round((datetime.fromisoformat(when).astimezone(timezone.utc) - PHP_RELEASE).total_seconds() / 3600, 1)


rows = []
for key, value in sorted(head.items()):
    resolved = next((c for c in changes.get(key, []) if any(s in ('Fix', 'Not vuln') for s in c['status'])), None)
    rows.append({'supplier': key[0], 'product': key[1], 'status_at_head': list(value['status']), 'version': value['version'],
                 'links_vendor': bool(re.search(r'https?://', value['links'])), 'first_listed': first[key],
                 'status_changes': changes.get(key, []),
                 'first_fix_or_not_vuln': resolved['time'] if resolved else None,
                 'hours_from_php_release_to_that_commit': hours(resolved['time']) if resolved else None})
summary = {'clone_head': head_sha, 'head_commit_time': head_time, 'commits': len(commits), 'entries_at_head': len(head),
           'status_at_head_cve_109618': dict(Counter(v['status'][0] if v['status'] else '' for v in head.values())),
           'status_at_head_cve_109619': dict(Counter(v['status'][1] if len(v['status']) > 1 else '' for v in head.values())),
           'entries_linking_a_url': sum(r['links_vendor'] for r in rows),
           'entries_ever_changing_status': sum(len(r['status_changes']) > 1 for r in rows),
           'first_commit_time': commits[0][1]}
(OUT / 'entries.json').write_text(json.dumps(rows, indent=1) + '\n')
(OUT / 'summary.json').write_text(json.dumps(summary, indent=1) + '\n')
print(json.dumps(summary, indent=1))
