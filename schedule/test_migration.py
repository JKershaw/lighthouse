#!/usr/bin/env python3
"""Check the immutable migration account; --audit-current also checks this rollout.

Ordinary CI tests the retained proposal rather than freezing tomorrow's legitimate
completions and scientific corrections to today's migrated CSV.
"""
import csv
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = '7a79e2906cf30a8e386553162ef4196e91f8837e'
ORIGINAL_FIELDS = ['id', 'study', 'task', 'earliest', 'latest', 'status', 'updated', 'by', 'ref', 'note']
FIELDS = ORIGINAL_FIELDS + ['kind', 'depends_on', 'run_id']
TERMINAL = {'done', 'missed', 'cancelled'}
KINDS = {'plan', 'observe', 'analyse', 'review', 'publish', 'maintain'}
AUDIT_CURRENT = '--audit-current' in sys.argv
if AUDIT_CURRENT:
    sys.argv.remove('--audit-current')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def csv_text(data):
    return list(csv.DictReader(io.StringIO(data)))


class MigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = csv_text((ROOT / 'notes/readiness/migration.csv').read_text())
        cls.old = [json.loads(r['old_json']) for r in cls.manifest if r['old_json']]
        cls.new = [json.loads(r['new_json']) for r in cls.manifest]
        cls.by = {r['id']: r for r in cls.new}

    def test_complete_unique_snapshot(self):
        self.assertEqual(len(self.old), 346)
        self.assertEqual(len(self.by), len(self.new))
        self.assertEqual([r['id'] for r in self.old], [r['id'] for r in self.new[:len(self.old)]])
        self.assertEqual(sum(r['status'] in TERMINAL for r in self.old), 136)
        for r in self.new:
            self.assertEqual(set(r), set(FIELDS))

    def test_preserved_history_and_documented_field_changes(self):
        for m, new in zip(self.manifest, self.new):
            reasons = json.loads(m['field_reasons_json'])
            sources = json.loads(m['field_sources_json'])
            if not m['old_json']:
                self.assertIn(new['status'], {'open', 'blocked'})
                self.assertTrue(m['source'])
                self.assertTrue(reasons['new_row'])
                continue
            old = json.loads(m['old_json'])
            for field in ORIGINAL_FIELDS:
                if old[field] != new[field]:
                    self.assertTrue(reasons.get(field), (new['id'], field))
                    self.assertTrue(sources.get(field), (new['id'], field))
            if old['status'] in TERMINAL:
                self.assertEqual(old, {f: new[f] for f in ORIGINAL_FIELDS})
                self.assertEqual([new[f] for f in FIELDS[10:]], ['', '', ''])
            else:
                self.assertIn(new['kind'], KINDS)
                self.assertFalse(new['run_id'])
                self.assertTrue(new['ref'])

    def test_dependency_graph_and_uninvented_review_clearance(self):
        visiting, visited = set(), set()
        def visit(id):
            self.assertNotIn(id, visiting, id)
            if id in visited:
                return
            visiting.add(id)
            for dependency in filter(None, self.by[id]['depends_on'].split(';')):
                self.assertIn(dependency, self.by)
                self.assertNotEqual(dependency, id)
                visit(dependency)
            visiting.remove(id)
            visited.add(id)
        for id in self.by:
            visit(id)
        for row in self.new[len(self.old):]:
            if row['kind'] == 'review':
                self.assertNotEqual(row['status'], 'done')

    def test_ready_initial_work_and_protected_order(self):
        self.assertEqual(self.by['LH042-reader-review']['depends_on'], 'LH042-review')
        self.assertEqual(self.by['LH042-resolution-recheck']['depends_on'], 'LH042-reader-review')
        self.assertEqual(self.by['LH047-paper-draft']['status'], 'done')
        self.assertEqual(self.by['LH047-paper-draft']['ref'], 'articles/drafts/rules-for-robots.md')
        self.assertEqual(self.by['LH047-paper-reviews']['depends_on'], 'LH047-paper-draft')
        self.assertEqual(self.by['LH047-paper-reviews']['earliest'], '')
        self.assertEqual(self.by['LH048-baseline-tabulator']['depends_on'], 'LH048-baseline')
        self.assertIn('LH048-2026-12-07', self.by['LH048-interim']['depends_on'])
        self.assertEqual(self.by['LH049-checkpoint']['earliest'], '2026-11-17')
        self.assertEqual(self.by['LH049-checkpoint']['depends_on'], 'LH049-2026-11-17')
        self.assertEqual(self.by['LH051-checkpoint']['earliest'], '2026-11-17')
        self.assertEqual(self.by['LH051-checkpoint']['depends_on'], 'LH051-2026-11-16')
        for id in ['LH050-record', 'LH050-panel-lock']:
            self.assertEqual(self.by[id]['earliest'], '')
            self.assertEqual(self.by[id]['depends_on'], 'LH050-baseline')

    def test_actual_clocks_and_no_duplicate_completed_read(self):
        self.assertEqual(self.by['LH049-2026-11-24']['latest'], '2026-11-24')
        self.assertEqual(self.by['LH051-last']['latest'], '2026-11-26')
        self.assertEqual(self.by['LH051-record']['latest'], '2026-11-27')
        self.assertEqual(self.by['horizon-2027-01-08']['kind'], 'plan')
        self.assertEqual(self.by['horizon-2027-01-12']['kind'], 'plan')
        self.assertEqual(self.by['LH044-read-01-review']['kind'], 'review')
        self.assertEqual(self.by['LH044-read-01-review']['depends_on'], 'LH044-read-01')
        self.assertEqual(self.by['LH039-checkpoint-2026-11-14']['status'], 'done')
        self.assertEqual(self.by['LH039-checkpoint-2026-11-21']['kind'], 'analyse')
        self.assertNotIn('LH039-packagist-2026-11-14', self.by)
        self.assertNotIn('LH039-batch-2026-11-14', self.by)
        self.assertEqual(self.by['MS365-report-2026-11-14']['status'], 'done')

    def test_conditional_and_missing_evidence_gates(self):
        self.assertEqual(self.by['LH030-stop']['status'], 'blocked')
        self.assertEqual(self.by['LH030-record']['depends_on'], 'LH030-stop')
        self.assertEqual(self.by['MS365-substantive-report']['status'], 'blocked')
        self.assertEqual(self.by['MS365-report-compare']['depends_on'], 'MS365-substantive-report')
        self.assertEqual(self.by['MS365-report-close']['depends_on'], '')
        self.assertEqual(self.by['MS365-report-close']['latest'], '2026-12-12')
        self.assertEqual(self.by['LH013-installer-A-record']['depends_on'], 'LH013-installer-A')
        self.assertEqual(self.by['LH013-installer-record']['depends_on'], 'LH013-installer-B')
        self.assertEqual(self.by['LH013-installer-B']['status'], 'blocked')
        for r in self.new:
            if r['task'].startswith('Collection closure decision:'):
                self.assertEqual(r['depends_on'], '')
                self.assertIn('done/missed/cancelled', r['task'])
                self.assertIn('Do not mark a read missed before its permitted window ends', r['task'])

    @unittest.skipUnless(AUDIT_CURRENT, 'one-time rollout audit; future research may legitimately change files')
    def test_current_queue_and_frozen_source(self):
        original = csv_text(git('show', SOURCE + ':schedule/due.csv').decode())
        current = csv_text((ROOT / 'schedule/due.csv').read_text())
        self.assertEqual(original, self.old)
        self.assertEqual(current, self.new)
        original_runs = csv_text(git('show', SOURCE + ':schedule/runs.csv').decode())
        current_runs = csv_text((ROOT / 'schedule/runs.csv').read_text())
        self.assertGreaterEqual(len(current_runs), len(original_runs))
        for added in current_runs[len(original_runs):]:
            self.assertTrue(added['run_id'])
        new_ids = [r['run_id'] for r in current_runs if r['run_id']]
        self.assertEqual(len(new_ids), len(set(new_ids)))
        for before, after in zip(original_runs, current_runs):
            self.assertEqual(before, {f: after[f] for f in before})
            self.assertEqual(after['run_id'], '')

    @unittest.skipUnless(AUDIT_CURRENT, 'one-time rollout audit; future science must remain editable')
    def test_scientific_evidence_preserved(self):
        amended = {f'studies/{s}/brief.md' for s in ['LH047', 'LH049', 'LH050', 'LH051']}
        listing = git('ls-tree', '-rz', SOURCE, '--', 'studies').split(b'\0')
        for entry in filter(None, listing):
            metadata, raw_path = entry.split(b'\t', 1)
            path = raw_path.decode()
            original_oid = metadata.decode().split()[2]
            current = ROOT / path
            self.assertTrue(current.exists(), path)
            if path in amended:
                original = git('cat-file', 'blob', original_oid)
                self.assertTrue(current.read_bytes().startswith(original), path)
                self.assertIn(b'Operational scheduling amendment, 14 November 2026', current.read_bytes()[len(original):])
            else:
                current_oid = subprocess.check_output(['git', 'hash-object', '--', str(current)], cwd=ROOT).decode().strip()
                self.assertEqual(current_oid, original_oid, path)


if __name__ == '__main__':
    unittest.main()
