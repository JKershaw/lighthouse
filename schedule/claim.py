#!/usr/bin/env python3
"""Publish one ready claim to origin/main before authorising work. No execution."""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
import subprocess
import sys
import tempfile

if __package__:
    from .model import FIELDS, evaluate, iso_utc
    from .roles import ROLES, accepts
else:
    from model import FIELDS, evaluate, iso_utc
    from roles import ROLES, accepts


class ClaimError(RuntimeError):
    pass


def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], text=True, capture_output=True)
    if result.returncode:
        raise ClaimError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def claim(root, identity, run_id, by, role='all'):
    """A losing push leaves the session branch untouched; never auto-retry it.

    Use a disposable detached worktree so a rejected claim cannot later leak
    into main through the session's completion commits. Main is the Git lock.
    """
    root = Path(root).resolve()
    if not run_id.strip() or not by.strip():
        raise ClaimError('run_id and by must be non-empty public labels')
    if role not in ROLES:
        raise ClaimError(f'unknown role: {role}')
    if git(root, 'status', '--porcelain'):
        raise ClaimError('commit finished work first; the checkout must be clean')
    git(root, 'fetch', 'origin', 'main')
    git(root, 'merge', '--ff-only', 'origin/main')
    base = git(root, 'rev-parse', 'origin/main')
    if git(root, 'rev-parse', 'HEAD') != base:
        raise ClaimError('publish/reconcile local commits before claiming more work')
    with tempfile.TemporaryDirectory(prefix='lighthouse-claim-') as directory:
        work = Path(directory) / 'checkout'
        git(root, 'worktree', 'add', '--detach', str(work), base)
        try:
            now = datetime.now(timezone.utc)
            report = evaluate(work, now)
            if not report['valid']:
                raise ClaimError('invalid authoritative queue: ' + '; '.join(report['diagnostics']))
            row = next((r for r in report['rows'] if r['id'] == identity), None)
            if row is None:
                raise ClaimError(f'unknown task: {identity}')
            if not row['actionable']:
                raise ClaimError(f'{identity}: {row["state"]}; owner={row["run_id"] or "none"}; '
                                 + '; '.join(row['reasons']))
            if not accepts(row, role):
                raise ClaimError(f'{identity}: outside {role} role')
            table = work / 'schedule/due.csv'
            # Replace only this CSV record; retain every other byte, including
            # historical formatting and multiline notes.
            content = table.read_bytes().decode('utf-8')
            lines = StringIO(content, newline='').readlines()
            reader = csv.DictReader(StringIO(content, newline=''))
            previous = 1
            for item in reader:
                end = reader.line_num
                if item['id'] == identity:
                    item.update(status='running', updated=iso_utc(now), by=by, run_id=run_id)
                    output = StringIO(newline='')
                    writer = csv.DictWriter(output, fieldnames=FIELDS, lineterminator='\n')
                    writer.writerow(item)
                    table.write_bytes((''.join(lines[:previous]) + output.getvalue()
                                       + ''.join(lines[end:])).encode('utf-8'))
                    break
                previous = end
            git(work, 'add', 'schedule/due.csv')
            git(work, 'commit', '-m', f'Schedule: claim {identity} ({run_id})')
            commit = git(work, 'rev-parse', 'HEAD')
            try:
                git(work, 'push', 'origin', 'HEAD:main')
            except ClaimError as exc:
                raise ClaimError('claim NOT confirmed; do not start work. Refresh main and '
                                 're-read ownership before trying again. ' + str(exc)) from exc
            # A failure here is also conservative: main may own the claim, but
            # this invocation does not authorise execution until local sync succeeds.
            git(root, 'merge', '--ff-only', commit)
            return commit
        finally:
            git(root, 'worktree', 'remove', '--force', str(work))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('id')
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--by', required=True)
    parser.add_argument('--role', choices=ROLES, default='all')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    try:
        commit = claim(args.root, args.id, args.run_id, args.by, args.role)
    except (ClaimError, OSError, ValueError) as exc:
        print(f'No execution authorised: {exc}', file=sys.stderr)
        return 1
    print(f'Claim confirmed on main: {args.id} {commit}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
