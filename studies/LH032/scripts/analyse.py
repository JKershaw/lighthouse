#!/usr/bin/env python3
"""LH032: immutable, pinned mainline-history read with SPDX head reconciliation.
Usage: analyse.py <clone path> <read label> [--commit <sha>]
The selected head is a recorded source revision; commit clocks are not push clocks.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import json
import gzip
import re

from verify_inventory import CVES, git, markdown_entries, verify

PHP_RELEASE = datetime(2026, 10, 21, 13, 30, tzinfo=timezone.utc)  # CERT-EU (LH024)


def hours(when):
    return round((datetime.fromisoformat(when).astimezone(timezone.utc) - PHP_RELEASE).total_seconds() / 3600, 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('clone', type=Path)
    parser.add_argument('label')
    parser.add_argument('--commit', default='HEAD')
    parser.add_argument('--output', type=Path, help='Optional new output directory for isolated replay')
    parser.add_argument('--compress', action='store_true', help='Retain deterministic gzip JSON')
    args = parser.parse_args()
    if not re.fullmatch(r'[0-9A-Za-z_-]+', args.label):
        parser.error('label must use letters, digits, underscore or hyphen')
    root = Path(__file__).resolve().parents[1]
    out = args.output or root / 'data' / ('read-' + args.label)
    if out.exists():
        parser.error('read label already exists; preserve it and choose a new label')
    head_sha = git(args.clone, 'rev-parse', args.commit + '^{commit}').decode().strip()
    verification, source_rows = verify(args.clone, head_sha)
    log = git(args.clone, 'log', '--first-parent', '--reverse', '--format=%H %cI', head_sha).decode()
    commits = [line.split(' ', 1) for line in log.strip().splitlines()]
    first, changes, previous, last_fields = {}, {}, {}, {}
    for sha, when in commits:
        current = markdown_entries(args.clone, sha)
        for key, value in current.items():
            first.setdefault(key, {'commit': sha, 'time': when})
            prior = previous.get(key, {})
            if prior.get('status') != value['status']:
                changes.setdefault(key, []).append({'commit': sha, 'time': when, 'status': list(value['status'])})
            for field in ('status', 'version', 'links', 'notes'):
                if prior.get(field) != value[field]:
                    last_fields.setdefault(key, {})[field] = {'commit': sha, 'time': when}
        previous = current
    rows = []
    for key, value in sorted(previous.items()):
        events = changes.get(key, [])
        resolved = next((c for c in events if any(s in ('Fix', 'Not vuln') for s in c['status'])), None)
        per_cve = {}
        for i, cve in enumerate(CVES):
            per_cve[cve] = {status: next(({'commit': c['commit'], 'time': c['time']}
                for c in events if c['status'][i] == status), None) for status in ('Fix', 'Not vuln')}
        rows.append({'supplier': key[0], 'product': key[1], 'status_at_head': list(value['status']),
                     'version': value['version'], 'links': value['links'], 'notes': value['notes'],
                     'links_vendor': bool(re.search(r'https?://', value['links'])),
                     'first_listed': first[key]['time'], 'first_listed_commit': first[key]['commit'],
                     'last_changed_fields': last_fields[key], 'status_changes': events,
                     'first_recorded_per_cve': per_cve,
                     'first_fix_or_not_vuln': resolved['time'] if resolved else None,
                     'hours_from_php_release_to_that_commit': hours(resolved['time']) if resolved else None})
    summary = {'analysis_version': '0.2', 'clone_head': head_sha, 'head_commit_time': commits[-1][1],
               'history_axis': 'first-parent mainline; committer timestamps, not public visibility',
               'commits': len(commits), 'entries_at_head': len(previous),
               'status_at_head_cve_109618': dict(Counter(v['status'][0] for v in previous.values())),
               'status_at_head_cve_109619': dict(Counter(v['status'][1] for v in previous.values())),
               'entries_linking_a_url': sum(r['links_vendor'] for r in rows),
               'entries_with_advisory_typed_url': verification['entries_with_advisory_typed_url'],
               'entries_ever_changing_status': sum(len(r['status_changes']) > 1 for r in rows),
               'first_commit_time': commits[0][1],
               'commit_clock_reversals': sum(datetime.fromisoformat(b[1]) < datetime.fromisoformat(a[1])
                                              for a, b in zip(commits, commits[1:]))}
    out.mkdir(parents=True, exist_ok=False)
    for filename, data in [('entries.json', rows), ('summary.json', summary),
                           ('inventory_verification.json', verification), ('source_entries.json', source_rows)]:
        raw = (json.dumps(data, indent=1) + '\n').encode()
        if args.compress:
            (out / (filename + '.gz')).write_bytes(gzip.compress(raw, mtime=0))
        else:
            (out / filename).write_bytes(raw)
    print(json.dumps(summary, indent=1))


if __name__ == '__main__':
    main()
