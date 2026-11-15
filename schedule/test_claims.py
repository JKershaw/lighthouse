"""Exercise the documented Git claim boundary without an executor or collectors."""
import csv
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import tempfile
import unittest

from model import FIELDS, evaluate


class ClaimsTest(unittest.TestCase):
    def test_losing_writer_reloads_owned_row_and_cannot_start_successor(self):
        def git(directory, *args, success=True):
            result = subprocess.run(['git', '-c', 'user.name=Readiness fixture', '-c', 'user.email=invalid',
                                     '-C', str(directory), *args], capture_output=True, text=True)
            if success:
                self.assertEqual(result.returncode, 0, result.stderr)
            return result

        def write(directory, status='open', run_id=''):
            path = directory / 'schedule/due.csv'
            path.parent.mkdir(exist_ok=True)
            with path.open('w', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerow(dict(id='observation', task='Hold a local fixture', kind='observe', status=status,
                                     updated='2026-11-14T12:00:00Z' if run_id else '', run_id=run_id,
                                     by='fixture ' + run_id if run_id else ''))
                writer.writerow(dict(id='analysis', task='Read that fixture', kind='analyse', status='open',
                                     depends_on='observation'))

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            remote, a, b = root / 'remote.git', root / 'a', root / 'b'
            git(root, 'init', '--bare', '--initial-branch=main', str(remote))
            git(root, 'clone', str(remote), str(a))
            write(a)
            git(a, 'add', '.')
            git(a, 'commit', '-m', 'Unowned fixture')
            git(a, 'push', 'origin', 'HEAD:main')
            git(root, 'clone', str(remote), str(b))
            instant = datetime(2026, 11, 14, 12, 0, tzinfo=timezone.utc)
            for checkout, identity in [(a, 'a'), (b, 'b')]:
                self.assertEqual(evaluate(checkout, instant)['ready'], ['observation'])
                write(checkout, 'running', identity)
                git(checkout, 'add', '.')
                git(checkout, 'commit', '-m', f'Claim by {identity}')
            git(a, 'push', 'origin', 'HEAD:main')
            self.assertNotEqual(git(b, 'push', 'origin', 'HEAD:main', success=False).returncode, 0)
            git(b, 'fetch', 'origin', 'main')
            # Re-read the authoritative row before reconciling the losing local claim.
            authoritative = git(b, 'show', 'origin/main:schedule/due.csv').stdout
            (b / 'schedule/due.csv').write_text(authoritative)
            result = evaluate(b, instant)
            self.assertTrue(result['valid'])
            self.assertEqual(result['ready'], [])
            rows = {row['id']: row for row in result['rows']}
            self.assertEqual(rows['observation']['run_id'], 'a')
            self.assertEqual(rows['observation']['state'], 'running')
            self.assertEqual(rows['analysis']['unmet_dependencies'], ['observation'])


if __name__ == '__main__':
    unittest.main()
