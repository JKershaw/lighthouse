"""Accounting checks keep partial estimates distinct from observed bills."""
import csv
from pathlib import Path
import tempfile
import unittest

from cost_summary import FIELDS, summarise


class CostsTest(unittest.TestCase):
    def report(self, rows, selected_date=None):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'costs.csv'
            with path.open('w', newline='') as stream:
                writer = csv.writer(stream)
                writer.writerow(FIELDS)
                writer.writerows(rows)
            return summarise(path, selected_date)

    def test_unknown_is_separate_and_bases_and_currencies_are_not_combined(self):
        result = self.report([
            ['2026-11-14', 'r1', 'driver', '0.1', 'USD', 'provider_reported', ''],
            ['2026-11-14', 'r1', 'review', '0.2', 'USD', 'provider_reported', ''],
            ['2026-11-14', 'r2', 'driver', '2', 'USD', 'list_rate_estimate', ''],
            ['2026-11-14', 'r3', 'driver', '3', 'GBP', 'provider_reported', ''],
            ['2026-11-14', 'r4', 'driver', '', '', 'unavailable', 'Unknown pricing'],
        ])
        self.assertTrue(result['valid'])
        self.assertEqual({(r['currency'], r['basis']): r['amount'] for r in result['subtotals']},
                         {('USD', 'provider_reported'): '0.3', ('USD', 'list_rate_estimate'): '2',
                          ('GBP', 'provider_reported'): '3'})
        self.assertEqual(len(result['unpriced']), 1)

    def test_duplicate_components_and_overlapping_total_fail_closed(self):
        row = ['2026-11-14', 'r1', 'driver', '1', 'USD', 'provider_reported', '']
        for rows in ([row, row], [row, [*row[:2], 'total', *row[3:]]]):
            result = self.report(rows)
            self.assertFalse(result['valid'])
            self.assertEqual(result['subtotals'], [])

    def test_invalid_dates_nonfinite_negative_and_unknown_basis_rejected(self):
        for day, amount, basis in [('20261114', '1', 'provider_reported'),
                                   ('2026-99-14', '1', 'provider_reported'),
                                   ('2026-11-14', 'NaN', 'provider_reported'),
                                   ('2026-11-14', '-1', 'provider_reported'),
                                   ('2026-11-14', '1', 'guessed')]:
            with self.subTest(day=day, amount=amount, basis=basis):
                self.assertFalse(self.report([[day, 'r1', 'driver', amount, 'USD', basis, '']])['valid'])

    def test_unknown_amount_must_stay_blank(self):
        self.assertFalse(self.report([['2026-11-14', 'r1', 'driver', '0', 'USD', 'unavailable', '']])['valid'])

    def test_filter_does_not_hide_bad_records_elsewhere(self):
        result = self.report([['2026-11-13', 'r1', 'driver', 'bad', 'USD', 'provider_reported', '']], '2026-11-14')
        self.assertFalse(result['valid'])

    def test_header_only_wrong_schema_is_invalid(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'costs.csv'
            path.write_text('wrong,header\n')
            self.assertFalse(summarise(path)['valid'])


if __name__ == '__main__':
    unittest.main()
