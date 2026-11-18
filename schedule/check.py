#!/usr/bin/env python3
"""Validate and report the queue offline. Positional dates replay midnight UTC."""
from __future__ import annotations

import argparse
from datetime import datetime, time, timezone
import json
from pathlib import Path
import re
import sys

if __package__:
    from .model import aware_instant, canonical_date, evaluate
    from .roles import ROLES, selection
else:
    from model import aware_instant, canonical_date, evaluate
    from roles import ROLES, selection

ROOT = Path(__file__).resolve().parents[1]


def arguments(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('date', nargs='?', help='YYYY-MM-DD, evaluated at midnight UTC')
    parser.add_argument('--now', help='timezone-aware ISO instant (incompatible with date)')
    parser.add_argument('--root', type=Path, default=ROOT, help='repository or fixture root')
    parser.add_argument('--role', choices=ROLES, help='select work without changing global readiness')
    parser.add_argument('--json', action='store_true', help='emit readiness contract version 1')
    return parser.parse_args(argv)


def show(title, items):
    print(f'\n{title}: {len(items)}')
    for item in items:
        print(f'  {item}')


def human(report, root):
    print(f'schedule/due.csv on {report["today"]}: {len(report["rows"])} rows')
    print(f'Evaluated at {report["evaluated_at"]} (UTC; date arguments mean midnight UTC)')
    show('Problems with the table', report['diagnostics'])
    rows = {row['id']: row for row in report['rows']}
    def tasks(identities):
        return [f'{identity}  [{rows[identity]["earliest"] or "any time"} to {rows[identity]["latest"] or "open-ended"}]  {rows[identity]["task"]}' for identity in identities]
    chosen = report.get('selection', report)
    if 'role' in chosen:
        print(f'Work selection: {chosen["role"]}; waits and warnings below remain global')
    show('Due now (ready)', tasks(chosen['ready']))
    show('Overdue (ready; follow the brief or mark missed)', tasks(chosen['overdue']))
    show('Stale claims (reconcile ownership before reopening)', tasks(report['stale']))
    waiting = [f'{row["id"]}  {row["state"]}: {"; ".join(row["reasons"])}' for row in report['rows']
               if row['state'] in {'blocked', 'keeper', 'dependency_wait', 'running'}]
    show('Waiting on evidence, a running claim, the keeper or a block', waiting)
    proposals = root / 'proposals.md'
    proposals_waiting = []
    if proposals.exists():
        try:
            for match in re.finditer(r'^### (P-\d+) (.+)$([\s\S]*?)(?=^### |^## |\Z)', proposals.read_text(), re.M):
                if re.search(r'Status:\s*waiting for the keeper', match.group(3), re.I):
                    proposals_waiting.append(f'{match.group(1)}  {match.group(2).strip()}')
        except (OSError, UnicodeError):
            proposals_waiting.append('Could not read proposals.md; this does not change queue readiness')
    show('Proposals waiting for the keeper (proposals.md)', proposals_waiting)
    show('Next seven days (calendar only)', tasks(report['upcoming']))
    show('Pipeline coverage warnings (advisory)', [item['message'] for item in report['coverage']])


def main(argv=None):
    args = arguments(argv)
    now = datetime.now(timezone.utc)
    try:
        if args.date and args.now:
            raise ValueError('supply either a positional date or --now, not both')
        if args.date:
            now = datetime.combine(canonical_date(args.date), time(), timezone.utc)
        elif args.now:
            now = aware_instant(args.now)
    except ValueError as exc:
        report = dict(schema_version=1, evaluated_at=None, today=None, valid=False,
                      diagnostics=[f'clock: {exc}'], rows=[], coverage=[],
                      groups={key: [] for key in ('ready', 'overdue', 'upcoming', 'stale', 'gaps', 'warnings')})
        report.update(report['groups'])
        if args.json:
            print(json.dumps(report, ensure_ascii=False))
        else:
            print(f'Invalid evaluation clock: {exc}', file=sys.stderr)
        return 1
    report = evaluate(args.root, now)
    if args.role:
        report['selection'] = dict(role=args.role, **selection(report, args.role))
    if args.json:
        print(json.dumps(report, ensure_ascii=False))
    else:
        human(report, args.root)
    return 0 if report['valid'] else 1


if __name__ == '__main__':
    sys.exit(main())
