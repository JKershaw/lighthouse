#!/usr/bin/env python3
"""Check schedule/due.csv and say what is due. Offline, standard library only.

Usage: python3 schedule/check.py [YYYY-MM-DD]   (default: today, UTC)

Prints, in order: problems with the table itself; rows due now; rows overdue (window closed, still open);
claims gone stale; rows waiting on the keeper or blocked; the next seven days; and gaps (a study with a brief
but no record and no rows, or an interim record with no open row). Exits 1 if the table has problems.
"""
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
import csv
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / 'schedule' / 'due.csv'
FIELDS = ['id', 'study', 'task', 'earliest', 'latest', 'status', 'updated', 'by', 'ref', 'note']
STATUSES = {'open', 'running', 'done', 'missed', 'blocked', 'keeper', 'cancelled'}
STALE = timedelta(hours=6)

today = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.now(timezone.utc).date()
now = datetime.now(timezone.utc)
rows = list(csv.DictReader(open(TABLE, newline='')))
problems = []

if rows and list(rows[0]) != FIELDS:
    problems.append(f'columns are {list(rows[0])}, expected {FIELDS}')
seen = set()
for n, r in enumerate(rows, start=2):
    where = f'line {n} ({r.get("id")})'
    if not r.get('id'):
        problems.append(f'{where}: no id')
    elif r['id'] in seen:
        problems.append(f'{where}: duplicate id')
    seen.add(r.get('id'))
    if r.get('status') not in STATUSES:
        problems.append(f'{where}: status {r.get("status")!r} not one of {sorted(STATUSES)}')
    for k in ('earliest', 'latest'):
        if r.get(k):
            try:
                date.fromisoformat(r[k])
            except ValueError:
                problems.append(f'{where}: {k} {r[k]!r} is not YYYY-MM-DD')
    if r.get('earliest') and r.get('latest') and r['latest'] < r['earliest']:
        problems.append(f'{where}: latest before earliest')
    if r.get('status') == 'done' and not r.get('ref'):
        problems.append(f'{where}: done with no ref (a read directory, file or commit)')

def d(s):
    return date.fromisoformat(s) if s else None

def claimed_at(r):
    """A running row's updated field holds its claim time, ISO with hour, e.g. 2026-11-02T06:35Z."""
    try:
        return datetime.fromisoformat(r['updated'].replace('Z', '+00:00'))
    except ValueError:
        return None

due, overdue, stale, waiting, upcoming = [], [], [], [], []
for r in rows:
    s, e, l = r['status'], d(r['earliest']), d(r['latest'])
    if s == 'open':
        if l and l < today:
            overdue.append(r)
        elif (e is None or e <= today):
            due.append(r)
        elif e <= today + timedelta(days=7):
            upcoming.append(r)
    elif s == 'running':
        t = claimed_at(r)
        if t is None or (t.tzinfo and now - t > STALE):
            stale.append(r)
    elif s in ('keeper', 'blocked'):
        waiting.append(r)

gaps = []
studies_with_open = {r['study'] for r in rows if r['status'] in ('open', 'running', 'keeper', 'blocked')}
for brief in sorted(ROOT.glob('studies/LH*/brief.md')):
    sid = brief.parent.name
    record = brief.parent / f'{sid}.md'
    if sid in studies_with_open:
        continue
    if not record.exists():
        gaps.append(f'{sid}: a brief, no record and no open row')
    elif re.search(r'^version:.*interim', record.read_text(), re.M):
        gaps.append(f'{sid}: an interim record and no open row')

def show(title, items, fmt=lambda r: f'  {r["id"]}  [{r["earliest"]} to {r["latest"] or "open-ended"}]  {r["task"]}'):
    print(f'\n{title}: {len(items)}')
    for r in items:
        print(fmt(r) if isinstance(r, dict) else f'  {r}')

print(f'schedule/due.csv on {today.isoformat()}: {len(rows)} rows')
show('Problems with the table', problems)
show('Due now', due)
show('Overdue (window closed, still open: do it if the brief allows, or mark missed)', overdue)
show('Stale claims (running for more than six hours: treat as open)', stale)
show('Waiting on the keeper or blocked', waiting, lambda r: f'  {r["id"]}  {r["status"]}: {r["note"]}')
show('Next seven days', upcoming)
show('Gaps', gaps)
sys.exit(1 if problems else 0)
