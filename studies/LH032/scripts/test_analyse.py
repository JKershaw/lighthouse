#!/usr/bin/env python3
"""Offline regression of the actual history and head-validation failure modes."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from verify_inventory import markdown_entries, verify, table_cells

SCRIPT = Path(__file__).with_name('analyse.py')
CVES = ('CVE-2026-109618', 'CVE-2026-109619')


class HistoryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        self.git('init', '-b', 'main')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args, at=None):
        env = os.environ.copy()
        if at:
            env.update(GIT_AUTHOR_DATE=at, GIT_COMMITTER_DATE=at)
        return subprocess.check_output(['git', '-C', str(self.repo), *args], env=env, stderr=subprocess.DEVNULL).decode().strip()

    def write(self, status='Investigation', notes='one', links='https://example.invalid/advisory'):
        directory = self.repo / 'software'
        directory.mkdir(exist_ok=True)
        (directory / 'software_list_a.md').write_text(
            '| Supplier | Product | Version (see Status) | Status CVE-2026-109618 | Status CVE-2026-109619 | Notes | Links |\n'
            '|---|---|---|---|---|---|---|\n'
            f'| Acme | Product | 1 | {status} | {status} | {notes} | {links} |\n')
        graph = [{'spdxId': 'org', 'type': 'Organization', 'name': 'Acme'},
                 {'spdxId': 'pkg', 'type': 'software_Package', 'name': 'Product',
                  'suppliedBy': 'org', 'software_packageVersion': '1', 'externalRef': []}]
        for c in CVES:
            graph.append({'spdxId': c, 'type': 'security_Vulnerability', 'name': c})
            graph.append({'spdxId': c + '-vex', 'type': 'security_VexAssessment', 'from': c,
                          'to': ['pkg'], 'relationshipType': 'fixedIn' if status == 'Fix' else 'underInvestigationFor'})
        source = directory / 'spdx/shared'
        source.mkdir(parents=True, exist_ok=True)
        raw = json.dumps({'@graph': graph})
        (source / 'source.json').write_text(raw)
        (source.parent / 'PHP_Downstream_Inventory.spdx3.json').write_text(raw)

    def commit(self, at):
        self.git('add', '.')
        self.git('commit', '-m', 'fixture', at=at)
        return self.git('rev-parse', 'HEAD')

    def run_analysis(self, sha, output):
        return subprocess.run(['python3', str(SCRIPT), str(self.repo), 'fixture', '--commit', sha,
                               '--output', str(output)], capture_output=True, text=True)

    def test_mainline_clock_pinning_fields_and_no_overwrite(self):
        self.write()
        self.commit('2026-10-21T10:00:00Z')
        self.git('checkout', '-b', 'side')
        self.write('Fix')
        self.commit('2026-10-21T12:00:00Z')
        self.git('checkout', 'main')
        self.git('merge', '--no-ff', 'side', '-m', 'merge', at='2026-10-21T14:00:00Z')
        self.write('Fix', notes=r'left \| right', links='https://example.invalid/new')
        pin = self.commit('2026-10-21T15:00:00Z')
        self.write('Investigation')
        self.commit('2026-10-21T16:00:00Z')
        out = self.root / 'output'
        result = self.run_analysis(pin, out)
        self.assertEqual(result.returncode, 0, result.stderr)
        row = json.loads((out / 'entries.json').read_text())[0]
        self.assertEqual(row['first_fix_or_not_vuln'], '2026-10-21T14:00:00Z')
        self.assertEqual(row['hours_from_php_release_to_that_commit'], 0.5)
        self.assertEqual(row['last_changed_fields']['status']['time'], '2026-10-21T14:00:00Z')
        self.assertEqual(row['last_changed_fields']['links']['time'], '2026-10-21T15:00:00Z')
        self.assertEqual(row['last_changed_fields']['notes']['time'], '2026-10-21T15:00:00Z')
        self.assertEqual(row['notes'], r'left \| right')
        self.assertEqual(row['links'], 'https://example.invalid/new')
        self.assertNotEqual(self.run_analysis(pin, out).returncode, 0)
        self.assertEqual(json.loads((out / 'summary.json').read_text())['clone_head'], pin)

    def test_delimiters_after_even_and_odd_backslash_runs(self):
        self.assertEqual(table_cells('| one ' + chr(92) * 2 + '| two |'), ['one ' + chr(92) * 2, 'two'])
        self.assertEqual(table_cells('| one ' + chr(92) + '| two |'), ['one ' + chr(92) + '| two'])

    def test_mismatched_package_status_fails_validation(self):
        self.write()
        path = self.repo / 'software/software_list_a.md'
        path.write_text(path.read_text().replace('Investigation | Investigation', 'Fix | Fix'))
        sha = self.commit('2026-10-21T10:00:00Z')
        with self.assertRaises(AssertionError):
            verify(self.repo, sha)

    def test_conflicting_identity_is_rejected_and_empty_links_survive(self):
        self.write(links='')
        sha = self.commit('2026-10-21T10:00:00Z')
        self.assertEqual(markdown_entries(self.repo, sha)[('Acme', 'Product')]['links'], '')
        path = self.repo / 'software/software_list_a.md'
        path.write_text(path.read_text() + '| Acme | Product | 2 | Fix | Fix | other | |\n')
        sha = self.commit('2026-10-21T11:00:00Z')
        with self.assertRaises(ValueError):
            markdown_entries(self.repo, sha)


if __name__ == '__main__':
    unittest.main()
