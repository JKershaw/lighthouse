"""Offline integration tests of real Git claims and role handovers."""
import csv
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import claim as claims
from model import FIELDS, evaluate, iso_utc
from roles import selection, task_role


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.remote = self.root / 'remote.git'
        self.a, self.b = self.root / 'a', self.root / 'b'
        self.git(self.root, 'init', '--bare', '--initial-branch=main', str(self.remote))
        self.git(self.root, 'clone', str(self.remote), str(self.a))
        (self.a / 'schedule').mkdir()
        (self.a / 'evidence.md').write_text('Retained fixture, not a source read.\n')
        self.write([
            self.row('read', kind='observe'),
            self.row('analyse', depends_on='read'),
            self.row('review', kind='review', depends_on='analyse'),
            self.row('publish', kind='publish', depends_on='review'),
            self.row('horizon', kind='plan', study='horizon'),
            self.row('editor', kind='maintain', study='site'),
            self.row('log', kind='maintain', study='log', depends_on='read'),
            self.row('closure', kind='plan', depends_on='read'),
        ])
        self.commit(self.a, 'Fixture queue')
        self.git(self.a, 'push', 'origin', 'HEAD:main')
        self.git(self.root, 'clone', str(self.remote), str(self.b))
        for checkout in (self.a, self.b):
            self.git(checkout, 'config', 'user.name', 'Runner fixture')
            self.git(checkout, 'config', 'user.email', 'fixture@invalid')

    def tearDown(self):
        self.temp.cleanup()

    def git(self, root, *args):
        result = subprocess.run(['git', '-c', 'user.name=Runner fixture', '-c', 'user.email=fixture@invalid',
                                 '-C', str(root), *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def row(self, identity, **values):
        return {**dict.fromkeys(FIELDS, ''), 'id': identity, 'status': 'open', 'kind': 'analyse', **values}

    def write(self, rows):
        with (self.a / 'schedule/due.csv').open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)

    def change(self, identity, **values):
        with (self.a / 'schedule/due.csv').open(newline='') as stream:
            rows = list(csv.DictReader(stream))
        for row in rows:
            if row['id'] == identity:
                row.update(values)
        self.write(rows)

    def report(self, root=None):
        return evaluate(root or self.a, datetime.now(timezone.utc))

    def commit(self, root, message):
        self.git(root, 'add', '.')
        self.git(root, 'commit', '-m', message)

    def test_two_writers_race_rejected_claim_never_enters_session_branch(self):
        original_git = claims.git
        competed = False
        def racing_git(root, *args):
            nonlocal competed
            if args[:1] == ('push',) and not competed:
                competed = True
                claims.claim(self.b, 'read', 'worker-b', 'Fixture B', 'watch')
            return original_git(root, *args)
        before = self.git(self.a, 'rev-parse', 'HEAD')
        with patch.object(claims, 'git', side_effect=racing_git):
            with self.assertRaisesRegex(claims.ClaimError, 'NOT confirmed'):
                claims.claim(self.a, 'read', 'worker-a', 'Fixture A', 'watch')
        self.assertTrue(competed)
        self.assertEqual(self.git(self.a, 'rev-parse', 'HEAD'), before)
        self.assertEqual(self.git(self.a, 'status', '--porcelain'), '')
        with self.assertRaisesRegex(claims.ClaimError, 'owner=worker-b'):
            claims.claim(self.a, 'read', 'worker-a', 'Fixture A', 'watch')
        self.assertNotIn('analyse', self.report()['ready'])

    def test_lost_push_acknowledgement_preserves_claim_and_fails_closed(self):
        original_git = claims.git
        def lost_ack(root, *args):
            result = original_git(root, *args)
            if args[:1] == ('push',):
                raise claims.ClaimError('simulated network failure after accepted push')
            return result
        before = self.git(self.a, 'rev-parse', 'HEAD')
        with patch.object(claims, 'git', side_effect=lost_ack):
            with self.assertRaisesRegex(claims.ClaimError, 'NOT confirmed'):
                claims.claim(self.a, 'read', 'accepted-worker', 'Fixture', 'watch')
        self.assertEqual(self.git(self.a, 'rev-parse', 'HEAD'), before)
        self.assertEqual(self.git(self.a, 'status', '--porcelain'), '')
        with self.assertRaisesRegex(claims.ClaimError, 'owner=accepted-worker'):
            claims.claim(self.b, 'read', 'competitor', 'Fixture', 'watch')

    def test_completion_merges_advancing_main_and_hands_over_to_research(self):
        claim = claims.claim(self.a, 'read', 'worker-a', 'Fixture A', 'watch')
        self.assertEqual(self.git(self.a, 'ls-remote', 'origin', 'refs/heads/main').split()[0], claim)
        self.change('read', status='done', ref='evidence.md')
        self.commit(self.a, 'Complete retained fixture')
        self.git(self.b, 'pull', '--ff-only')
        claims.claim(self.b, 'editor', 'editor-b', 'Fixture B', 'editor')
        (self.b / 'concurrent.md').write_text('Another run advanced main.\n')
        self.commit(self.b, 'Concurrent outcome')
        self.git(self.b, 'push', 'origin', 'HEAD:main')
        self.git(self.a, 'fetch', 'origin', 'main')
        authoritative = self.git(self.a, 'show', 'origin/main:schedule/due.csv')
        owner = next(r for r in csv.DictReader(authoritative.splitlines()) if r['id'] == 'read')
        self.assertEqual((owner['status'], owner['run_id']), ('running', 'worker-a'))
        self.git(self.a, 'merge', '--no-edit', 'origin/main')
        self.assertTrue(self.report()['valid'])
        self.git(self.a, 'push', 'origin', 'HEAD:main')
        self.assertTrue((self.a / 'concurrent.md').exists())
        report = self.report()
        editor = next(row for row in report['rows'] if row['id'] == 'editor')
        self.assertEqual((editor['status'], editor['run_id']), ('running', 'editor-b'))
        self.assertIn('analyse', selection(report, 'research')['ready'])
        self.assertNotIn('analyse', selection(report, 'watch')['ready'])
        self.assertIn('log', selection(report, 'watch')['ready'])
        claims.claim(self.b, 'analyse', 'worker-b', 'Fixture B', 'research')

    def test_stale_interrupted_claim_requires_evidence_reconciliation(self):
        self.change('read', status='running', run_id='interrupted', by='Fixture',
                    updated=iso_utc(datetime.now(timezone.utc) - timedelta(hours=7)))
        self.commit(self.a, 'Interrupted work')
        self.git(self.a, 'push', 'origin', 'HEAD:main')
        with self.assertRaisesRegex(claims.ClaimError, 'recovery.*interrupted'):
            claims.claim(self.b, 'read', 'new-worker', 'Fixture', 'watch')
        self.assertEqual(self.report()['stale'], ['read'])
        # Reconcile against retained output: this was already collected. Do not
        # repeat it merely because ownership aged; complete with its reference.
        self.change('read', status='done', ref='evidence.md', note='Recovered retained output; no repeated read')
        self.commit(self.a, 'Reconcile interrupted output')
        self.git(self.a, 'push', 'origin', 'HEAD:main')
        with self.assertRaisesRegex(claims.ClaimError, 'done'):
            claims.claim(self.b, 'read', 'new-worker', 'Fixture', 'watch')
        self.assertIn('analyse', self.report()['ready'])

    def test_roles_do_not_bypass_dates_blocks_or_publication_reviews(self):
        for identity, values in [('read', dict(earliest='2099-01-01')),
                                 ('review', dict(status='blocked', note='Must-fix unresolved'))]:
            self.change(identity, **values)
        self.commit(self.a, 'Future observation and unresolved review')
        self.git(self.a, 'push', 'origin', 'HEAD:main')
        for identity, role in [('read', 'watch'), ('publish', 'research'), ('horizon', 'editor')]:
            with self.assertRaises(claims.ClaimError):
                claims.claim(self.b, identity, 'worker', 'Fixture', role)
        report = self.report()
        self.assertEqual(selection(report, 'watch')['ready'], [])
        self.assertEqual(selection(report, 'editor')['ready'], ['editor'])
        self.assertEqual(selection(report, 'horizon')['ready'], ['horizon'])
        self.assertEqual(task_role(self.row('amend', kind='plan')), 'research')
        self.assertEqual(task_role(self.row('closeout', kind='maintain', study='LH055')), 'research')
        self.assertNotIn('publish', selection(report, 'research')['ready'])
        # All prerequisites and the unresolved review must clear explicitly.
        self.change('read', status='done', earliest='', ref='evidence.md')
        self.change('analyse', status='done', ref='evidence.md')
        self.assertNotIn('publish', selection(self.report(), 'research')['ready'])
        self.change('review', status='done', ref='evidence.md')
        self.assertIn('publish', selection(self.report(), 'research')['ready'])
        # The model is deliberately not a scientific verdict reader: the runner
        # must check the actual version and review notes before release.

    def test_original_runner_default_and_cli_contract_remain_compatible(self):
        report = self.report()
        self.assertEqual(selection(report, 'all'), {key: report[key] for key in ('ready', 'overdue')})
        script = Path(__file__).with_name('check.py')
        args = [sys.executable, str(script), '--root', str(self.a), '--now', report['evaluated_at'], '--json']
        result = subprocess.run(args, capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout), report)
        result = subprocess.run(args + ['--role', 'watch'], capture_output=True, text=True, check=True)
        selected = json.loads(result.stdout)
        self.assertEqual(selected.pop('selection'), dict(role='watch', **selection(report, 'watch')))
        self.assertEqual(selected, report)
        claims.claim(self.b, 'editor', 'legacy-all', 'Fixture')

    def test_dirty_or_unpublished_work_never_gets_pushed_by_claim(self):
        (self.a / 'unfinished.md').write_text('Unfinished local work.\n')
        with self.assertRaisesRegex(claims.ClaimError, 'clean'):
            claims.claim(self.a, 'read', 'worker', 'Fixture')
        self.commit(self.a, 'Unpublished work')
        with self.assertRaisesRegex(claims.ClaimError, 'local commits'):
            claims.claim(self.a, 'read', 'worker', 'Fixture')
        self.assertEqual(self.report(self.b)['rows'][0]['status'], 'open')

    def test_claim_changes_only_target_record_including_multiline_csv(self):
        self.change('read', task='Quoted "task", with\nmultiline text')
        path = self.a / 'schedule/due.csv'
        # Noncanonical but valid quoting in an unrelated row must survive.
        path.write_bytes(path.read_bytes().replace(b'analyse,', b'"analyse",', 1))
        self.commit(self.a, 'Multiline CSV fixture')
        self.git(self.a, 'push', 'origin', 'HEAD:main')
        before = path.read_bytes().split(b'"analyse",', 1)[1]
        claims.claim(self.a, 'read', 'worker', 'Fixture', 'watch')
        self.assertEqual(path.read_bytes().split(b'"analyse",', 1)[1], before)
        self.assertEqual(self.report()['rows'][0]['task'], 'Quoted "task", with\nmultiline text')


if __name__ == '__main__':
    unittest.main()
