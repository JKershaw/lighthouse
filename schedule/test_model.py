"""Readiness defects, fixed clocks and evidence gates; all fixtures stay offline."""
import csv
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('readiness_model', HERE / 'model.py')
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)
NOW = model.aware_instant('2026-11-14T12:00:00Z')


def row(identity, **values):
    result = dict.fromkeys(model.FIELDS, '')
    result.update(id=identity, study='LH900', task=f'Do {identity}', status='open', kind='analyse')
    result.update(values)
    if result['status'] == 'running':
        if 'run_id' not in values:
            result['run_id'] = 'fixture-' + identity
        if 'by' not in values:
            result['by'] = 'Fixture owner'
    return result


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / 'schedule').mkdir()
        (self.root / 'evidence.md').write_text('Retained fixture evidence.\n')

    def tearDown(self):
        self.temp.cleanup()

    def write(self, rows, fields=None):
        with (self.root / 'schedule/due.csv').open('w', newline='') as handle:
            writer = csv.writer(handle)
            writer.writerow(fields or model.FIELDS)
            for item in rows:
                writer.writerow([item[field] for field in (fields or model.FIELDS)])

    def evaluate(self, rows, now=NOW):
        self.write(rows)
        return model.evaluate(self.root, now)

    def assert_invalid(self, report, text):
        self.assertFalse(report['valid'])
        self.assertTrue(any(text in message for message in report['diagnostics']), report['diagnostics'])
        self.assertEqual(report['ready'], [])
        self.assertEqual(report['overdue'], [])
        self.assertTrue(all(not item['actionable'] for item in report['rows']))

    def test_exact_header_even_when_empty(self):
        self.write([])
        self.assertTrue(model.evaluate(self.root, NOW)['valid'])
        self.write([], model.FIELDS[:-1])
        self.assert_invalid(model.evaluate(self.root, NOW), 'columns')
        (self.root / 'schedule/due.csv').write_text('')
        self.assert_invalid(model.evaluate(self.root, NOW), 'columns')

    def test_missing_file_is_structured(self):
        self.assert_invalid(model.evaluate(self.root, NOW), 'cannot read')

    def test_unresolvable_root_is_structured(self):
        loop = self.root / 'root-loop'
        loop.symlink_to(loop)
        self.assert_invalid(model.evaluate(loop, NOW), 'root cannot be resolved')
        self.assert_invalid(model.evaluate(self.root / 'evidence.md', NOW), 'cannot read')

    def test_short_and_long_rows_fail_closed(self):
        for cells in [2, 14]:
            with self.subTest(cells=cells):
                self.write([row('otherwise-ready')])
                with (self.root / 'schedule/due.csv').open('a') as handle:
                    handle.write(','.join(['x'] * cells) + '\n')
                self.assert_invalid(model.evaluate(self.root, NOW), 'cells')

    def test_csv_keeps_commas_quotes_and_embedded_newlines(self):
        task = 'Read "one, two"\nthen retain the result'
        report = self.evaluate([row('quoted', task=task)])
        self.assertTrue(report['valid'], report['diagnostics'])
        self.assertEqual(report['rows'][0]['task'], task)

    def test_malformed_csv_does_not_throw(self):
        for text in ['"unterminated', 'id,bad"quote', '"closed"junk']:
            (self.root / 'schedule/due.csv').write_text(text)
            self.assert_invalid(model.evaluate(self.root, NOW), 'CSV')

    def test_canonical_dates_and_reversed_bounds(self):
        for value in ['20261114', '2026-W46-6', '2026-2-01', '2026-02-30', '2026-99-01']:
            self.assert_invalid(self.evaluate([row('date', earliest=value)]), 'canonical')
        self.assert_invalid(self.evaluate([row('reverse', earliest='2026-11-15', latest='2026-11-14')]), 'latest before')

    def test_validation_stops_an_otherwise_valid_ready_frontier(self):
        report = self.evaluate([row('ready'), row('bad', earliest='broken')])
        self.assert_invalid(report, 'canonical')
        self.assertEqual(report['rows'][0]['readiness'], 'invalid')

    def test_duplicate_missing_self_and_cyclic_ids(self):
        cases = [([row('a'), row('a')], 'duplicate id'),
                 ([row('a', depends_on='missing')], 'missing dependency'),
                 ([row('a', depends_on='a')], 'self-dependency'),
                 ([row('a', depends_on='b'), row('b', depends_on='a')], 'cycle'),
                 ([row('a', depends_on='b;b'), row('b')], 'duplicate dependency'),
                 ([row('a', depends_on='b;'), row('b')], 'empty dependency')]
        for rows, message in cases:
            with self.subTest(message=message):
                self.assert_invalid(self.evaluate(rows), message)

    def test_dependency_diamond_exposes_only_done_frontier(self):
        rows = [row('a', status='done', ref='evidence.md'), row('b', depends_on='a'),
                row('c', depends_on='a'), row('d', depends_on='b; c')]
        report = self.evaluate(rows)
        self.assertEqual(report['ready'], ['b', 'c'])
        self.assertEqual(report['rows'][3]['unmet_dependencies'], ['b', 'c'])
        rows[1].update(status='done', ref='evidence.md')
        rows[2].update(status='running', updated='2026-11-14T11:00Z', run_id='fixture-c', by='Fixture owner')
        self.assertEqual(self.evaluate(rows)['ready'], [])
        rows[2].update(status='done', ref='evidence.md')
        self.assertEqual(self.evaluate(rows)['ready'], ['d'])

    def test_missed_cancelled_and_blocked_do_not_satisfy_evidence_gate(self):
        for status in ['missed', 'cancelled', 'blocked', 'keeper', 'open']:
            report = self.evaluate([row('source', status=status), row('analysis', depends_on='source')])
            self.assertFalse(report['rows'][1]['actionable'])
        # An explicit closure can be done without fabricating the missing read.
        report = self.evaluate([row('read', status='missed'), row('closure', status='done', ref='evidence.md'),
                                row('honest-record', depends_on='closure')])
        self.assertEqual(report['ready'], ['honest-record'])

    def test_manual_blocks_survive_done_dependencies(self):
        for status in ['blocked', 'keeper']:
            report = self.evaluate([row('evidence', status='done', ref='evidence.md'),
                                    row('wait', status=status, depends_on='evidence', note='Needs an account')])
            self.assertEqual(report['rows'][1]['state'], status)
            self.assertIn('Needs an account', report['rows'][1]['reasons'])
            self.assertFalse(report['rows'][1]['actionable'])

    def test_calendar_and_dependency_states_are_independent(self):
        report = self.evaluate([row('gate', status='blocked'), row('late', latest='2026-11-13', depends_on='gate'),
                                row('early', earliest='2026-11-15', depends_on='gate')])
        self.assertEqual(report['rows'][1]['calendar_state'], 'overdue')
        self.assertEqual(report['rows'][1]['state'], 'dependency_wait')
        self.assertEqual(report['rows'][2]['calendar_state'], 'upcoming')
        self.assertTrue(any('Not before' in reason for reason in report['rows'][2]['reasons']))
        self.assertEqual(report['overdue'], [])

    def test_inclusive_bounds_open_ended_and_stable_deadline_order(self):
        report = self.evaluate([row('open-ended'), row('last', latest='2026-11-14'),
                                row('first', earliest='2026-11-14', latest='2026-11-14'),
                                row('late', latest='2026-11-13'), row('soon', earliest='2026-11-21'),
                                row('far', earliest='2026-11-22')])
        self.assertEqual(report['ready'], ['last', 'first', 'open-ended'])
        self.assertEqual(report['overdue'], ['late'])
        self.assertEqual(report['upcoming'], ['soon'])
        self.assertEqual(report['rows'][-1]['calendar_state'], 'future')

    def test_claim_exact_six_hours_and_timezone_conversion(self):
        report = self.evaluate([row('exact', status='running', updated='2026-11-14T07:00:00+01:00'),
                                row('stale', status='running', updated='2026-11-14T05:59:59Z')])
        self.assertTrue(report['valid'])
        self.assertEqual(report['rows'][0]['state'], 'running')
        self.assertEqual(report['stale'], ['stale'])
        self.assertEqual(report['rows'][1]['state'], 'recovery')
        self.assertFalse(any(item['actionable'] for item in report['rows']))

    def test_naive_date_only_and_broken_claims_fail_closed(self):
        for value in ['2026-11-01', '2026-11-01T12:00:00', 'broken', '']:
            report = self.evaluate([row('claim', status='running', updated=value), row('ready')])
            self.assert_invalid(report, 'timezone-aware')
            self.assertEqual(report['stale'], ['claim'])

    def test_running_claim_requires_public_identity_and_attribution(self):
        self.assert_invalid(self.evaluate([row('claim', status='running', updated='2026-11-14T11:00Z', run_id='')]), 'public run_id')
        self.assert_invalid(self.evaluate([row('claim', status='running', updated='2026-11-14T11:00Z', by='')]), 'by attribution')

    def test_run_registry_schema_uniqueness_and_unfinished_claim(self):
        registry = self.root / 'schedule/runs.csv'
        registry.write_text('started,by,did,commit,run_id\n2026-11-01,old,retained,,\n2026-11-02,old,retained,,\n')
        report = self.evaluate([row('claim', status='running', updated='2026-11-14T11:00Z')])
        self.assertTrue(report['valid'], report['diagnostics'])
        for header in ['started,by,did,commit,plain,run_id', 'started,by,did,commit,run_id,plain']:
            registry.write_text(header + '\n')
            self.assertTrue(model.evaluate(self.root, NOW)['valid'])
        registry.write_text('started,by,did,commit,run_id\na,b,c,,public-one\nd,e,f,,public-one\n')
        self.assert_invalid(model.evaluate(self.root, NOW), 'duplicate run_id')
        registry.write_text('started,by,did,commit\n')
        self.assert_invalid(model.evaluate(self.root, NOW), 'schedule/runs.csv')
        registry.write_text('started,by,did,commit,run_id\na,b,c\n')
        self.assert_invalid(model.evaluate(self.root, NOW), 'cells')

    def test_fixed_clock_replays_at_utc_midnight(self):
        rows = [row('boundary', earliest='2026-11-14'), row('claim', status='running', updated='2026-11-13T18:00:00Z')]
        instant = model.aware_instant('2026-11-14T01:00:00+01:00')
        report = self.evaluate(rows, instant)
        self.assertEqual(report['today'], '2026-11-14')
        self.assertEqual(report['stale'], [])
        self.assertEqual(report, model.evaluate(self.root, instant))

    def test_offset_clock_uses_utc_date_across_local_midnight(self):
        report = self.evaluate([row('tomorrow', earliest='2026-11-14')],
                               model.aware_instant('2026-11-14T00:30:00+01:00'))
        self.assertEqual(report['today'], '2026-11-13')
        self.assertEqual(report['rows'][0]['state'], 'calendar_wait')
        self.assertEqual(report['ready'], [])

    def test_terminal_history_can_leave_new_metadata_blank(self):
        rows = [row('old', status='done', ref='evidence.md (version 0.2); d647c90', kind='', updated='2026-11-01')]
        report = self.evaluate(rows)
        self.assertTrue(report['valid'], report['diagnostics'])
        for field in model.FIELDS:
            self.assertEqual(report['rows'][0][field], rows[0][field])
        self.assertEqual(report['rows'][0]['state'], 'done')
        self.assert_invalid(self.evaluate([row('active', kind='')]), 'kind')
        self.assert_invalid(self.evaluate([row('badkind', kind='collect')]), 'kind')

    def test_done_requires_a_real_nonblank_reference_before_unblocking(self):
        for reference in ['   ', ';', ' ; ; ', 'looks fine']:
            report = self.evaluate([row('done', status='done', ref=reference), row('next', depends_on='done')])
            self.assertFalse(report['valid'], reference)
            self.assertEqual(report['ready'], [])
            self.assertFalse(report['rows'][1]['actionable'])
        historical = self.evaluate([row('historical', status='done', kind='', ref='retained narrative')])
        self.assertTrue(historical['valid'], historical['diagnostics'])
        for identity in [' padded', 'padded ', 'two words', 'line\nbreak']:
            self.assert_invalid(self.evaluate([row(identity)]), 'whitespace')

    def test_reference_fragments_urls_missing_and_containment(self):
        report = self.evaluate([row('done', status='done', ref='evidence.md#not-interpreted; https://example.invalid/never-fetched')])
        self.assertTrue(report['valid'], report['diagnostics'])
        self.assert_invalid(self.evaluate([row('missing', status='done', ref='absent.md')]), 'does not exist')
        self.assert_invalid(self.evaluate([row('escape', status='done', ref='../outside.md')]), 'outside')
        self.assert_invalid(self.evaluate([row('done', status='done')]), 'no ref')
        (self.root / 'escape.md').symlink_to(self.root.parent / 'outside.md')
        self.assert_invalid(self.evaluate([row('symlink', ref='escape.md')]), 'outside')
        self.assert_invalid(self.evaluate([row('badurl', ref='http://[broken')]), 'malformed')
        for scheme in ['javascript:alert(1)', 'data:text/plain,fixture', 'file:///etc/passwd', 'mailto:test@example.invalid']:
            self.assert_invalid(self.evaluate([row('scheme', status='done', ref=scheme)]), 'unsupported URL scheme')
        self.assert_invalid(self.evaluate([row('nul', ref='bad\x00path.md')]), 'outside')
        (self.root / 'studies/LH000').mkdir(parents=True)
        self.assertTrue(self.evaluate([row('annotated', ref='studies/LH000, LH002 to LH006')])['valid'])

    def test_historical_review_prefix_requires_unique_local_match(self):
        (self.root / 'notes').mkdir()
        (self.root / 'notes/R-0043-evidence.md').write_text('A retained historical review.')
        historical = row('old', status='done', kind='', ref='notes/R-0043 to R-0045')
        self.assertTrue(self.evaluate([historical])['valid'])
        self.assert_invalid(self.evaluate([row('active', ref='notes/R-0043')]), 'does not exist')
        (self.root / 'notes/R-0043-other.md').write_text('An ambiguous shorthand.')
        self.assert_invalid(self.evaluate([historical]), 'ambiguous')

    def test_advisory_pipeline_coverage_does_not_block_work(self):
        folder = self.root / 'studies/LH901'
        folder.mkdir(parents=True)
        (folder / 'brief.md').write_text('A completed or missing continuation needs a human audit.')
        report = self.evaluate([row('publish', kind='publish')])
        self.assertTrue(report['valid'])
        self.assertEqual(report['ready'], ['publish'])
        self.assertEqual(report['gaps'], ['continuation:LH901'])
        self.assertIn('review-predecessor:publish', report['warnings'])
        (folder / 'LH901.md').write_text('version: 1.0\n\nA final archival record.')
        self.assertNotIn('continuation:LH901', self.evaluate([row('publish', kind='publish')])['warnings'])
        (folder / 'LH901.md').write_text('version: 0.1 (interim)\n')
        self.assertIn('continuation:LH901', self.evaluate([row('publish', kind='publish')])['warnings'])
        report = self.evaluate([row('review', kind='review', status='done', ref='evidence.md'),
                                row('publish', kind='publish', depends_on='review')])
        self.assertNotIn('review-predecessor:publish', report['warnings'])

    def test_ms365_successful_availability_attempt_is_not_substantive_report_gate(self):
        report = self.evaluate([row('availability', kind='observe', status='done', ref='evidence.md'),
                                row('report-gate', kind='plan', status='blocked', note='No accessible substantive report'),
                                row('comparison', depends_on='report-gate')])
        self.assertEqual(report['rows'][-1]['unmet_dependencies'], ['report-gate'])
        self.assertFalse(report['rows'][-1]['actionable'])

    def test_installer_stage_a_record_does_not_wait_for_account_blocked_b(self):
        report = self.evaluate([row('A', status='done', ref='evidence.md'), row('B', status='blocked'),
                                row('initial', depends_on='A'), row('final', depends_on='B')])
        self.assertEqual(report['ready'], ['initial'])

    def test_cost_files_are_not_readiness_dependencies(self):
        (self.root / 'schedule/costs.csv').write_text('malformed and unavailable accounting')
        self.assertEqual(self.evaluate([row('ready')])['ready'], ['ready'])
        (self.root / 'schedule/costs.csv').unlink()
        self.assertEqual(model.evaluate(self.root, NOW)['ready'], ['ready'])

    def cli(self, *args):
        return subprocess.run([sys.executable, str(HERE / 'check.py'), '--root', str(self.root), *args],
                              capture_output=True, text=True)

    def test_cli_json_and_date_replay_share_model_result(self):
        self.write([row('ready'), row('claim', status='running', updated='2026-11-13T18:00:00Z')])
        result = self.cli('2026-11-14', '--json')
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = model.evaluate(self.root, model.aware_instant('2026-11-14T00:00:00Z'))
        self.assertEqual(json.loads(result.stdout), expected)
        self.assertEqual(json.loads(self.cli('--now', '2026-11-14T00:00:00Z', '--json').stdout), expected)
        self.assertIn('midnight UTC', self.cli('2026-11-14').stdout)

    def test_shared_contract_fixture(self):
        fixture = HERE / 'fixtures/readiness-v1'
        expected = json.loads((fixture / 'expected.json').read_text())
        report = model.evaluate(fixture, NOW)
        self.assertEqual(report, expected)
        self.assertEqual(report['ready'], ['record'])
        self.assertEqual(report['overdue'], ['late-ready'])
        self.assertEqual(report['stale'], ['old-claim'])
        self.assertEqual(report['rows'][3]['calendar_state'], 'overdue')
        self.assertEqual(report['rows'][3]['state'], 'dependency_wait')

    def test_cli_can_run_as_namespace_module(self):
        self.write([row('ready')])
        result = subprocess.run([sys.executable, '-m', 'schedule.check', '--root', str(self.root),
                                 '--now', '2026-11-14T12:00:00Z', '--json'],
                                cwd=HERE.parent, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['ready'], ['ready'])

    def test_cli_invalid_clock_and_queue_are_json_without_traceback(self):
        self.write([row('ready')])
        for args in [('2026-11-14', '--now', '2026-11-14T00:00:00Z'),
                     ('20261114',), ('--now', '2026-11-14T00:00:00')]:
            result = self.cli(*args, '--json')
            self.assertEqual(result.returncode, 1)
            self.assertFalse(json.loads(result.stdout)['valid'])
            self.assertNotIn('Traceback', result.stderr)
        self.write([row('bad', earliest='bad')])
        result = self.cli('--json')
        self.assertEqual(result.returncode, 1)
        self.assertFalse(json.loads(result.stdout)['valid'])
        self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
