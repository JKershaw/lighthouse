#!/usr/bin/env python3
"""Tests for studies/LH048/scripts/tabulate.py: thresholds and classes on constructed inputs, and a
deterministic replay on the held reads. Run: python3 -I studies/LH048/scripts/test_tabulate.py
"""
from pathlib import Path
import copy
import gzip
import json
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tabulate as T  # noqa: E402

SEL = json.loads((HERE.parent / 'selection.json').read_text())


class Thresholds(unittest.TestCase):
    def test_cvss_bands(self):
        cases = {0.0: 'None', 0.1: 'Low', 3.9: 'Low', 4.0: 'Medium', 6.9: 'Medium', 7.0: 'High', 8.9: 'High',
                 9.0: 'Critical', 10.0: 'Critical', '7.5': 'High'}
        for s, b in cases.items():
            self.assertEqual(T.cvss_band(s), b, s)
        self.assertIsNone(T.cvss_band(None))

    def test_step_factor_two_either_way(self):
        self.assertTrue(T.is_step(0.001, 0.002))       # exactly x2 up
        self.assertTrue(T.is_step(0.002, 0.001))       # exactly x2 down
        self.assertFalse(T.is_step(0.001, 0.00199))
        self.assertFalse(T.is_step(0.002, 0.00101))
        self.assertTrue(T.is_step(0.00165, 0.00388))
        self.assertFalse(T.is_step(0.01257, 0.01611))
        self.assertFalse(T.is_step(0.0, 0.0))
        self.assertTrue(T.is_step(0.0, 0.001))

    def test_percentile_threshold(self):
        self.assertFalse(T.above_threshold(0.5))      # at 0.5 is "at or below", not above
        self.assertTrue(T.above_threshold(0.50001))

    def test_body_states(self):
        ok = {'status': 200, 'bytes': 200}
        self.assertEqual(T.body_state(ok, True, False), 'ok')
        self.assertEqual(T.body_state({'status': 200, 'bytes': 199}, True, False), T.UNAVAILABLE)
        self.assertEqual(T.body_state({'status': 503, 'bytes': 188}, True, False), T.UNAVAILABLE)
        self.assertEqual(T.body_state({'status': 404, 'bytes': 50}, True, True), T.NO_RECORD)
        self.assertEqual(T.body_state({'status': 404, 'bytes': 50}, True, False), T.UNAVAILABLE)
        self.assertEqual(T.body_state({'error': 'not fetched: robots'}, False, True), T.UNAVAILABLE)
        self.assertEqual(T.body_state(None, False, True), T.NOT_READ)


class Classes(unittest.TestCase):
    def test_held_selection_passes(self):
        notes = T.check_selection(SEL)
        self.assertEqual(len(notes), 2)                 # C1 and C2, ambiguous by the sharing clause

    def mutate(self, step, **kw):
        s = copy.deepcopy(SEL)
        for u in s['units']:
            if u['step'] == step:
                u.update(kw)
        return s

    def test_contradictions_raise(self):
        bad = [
            self.mutate('S1', candidates=['CVE-2026-1']),                 # identified with candidates
            self.mutate('C3', candidates=['CVE-2026-1'], cves=[]),         # unidentified with a candidate
            self.mutate('A', cves=['CVE-2026-1']),                         # no identifier with a CVE
            self.mutate('C3', **{'class': 'ambiguous', 'candidates': ['CVE-2026-9']}),  # one unshared candidate
            self.mutate('S1', **{'class': 'named'}),                       # named outside Windows/Linux
            self.mutate('W', **{'class': 'pending'}),
        ]
        for s in bad:
            with self.assertRaises(AssertionError):
                T.check_selection(s)

    def test_two_candidates_ambiguous_ok(self):
        s = self.mutate('C3', **{'class': 'ambiguous', 'candidates': ['CVE-2026-8', 'CVE-2026-9']})
        T.check_selection(s)

    def test_linked_set_kept_apart(self):
        s = copy.deepcopy(SEL)
        s['linked_set'].append('CVE-2026-113192')
        with self.assertRaises(AssertionError):
            T.check_selection(s)
        r = T.roles(SEL)
        self.assertEqual(r['CVE-2026-113192']['group'], 'ambiguous_candidate')
        self.assertEqual(sorted(r['CVE-2026-113192']['units']), ['C1 (ambiguous)', 'C2 (ambiguous)'])
        self.assertEqual(r['CVE-2026-43715']['group'], 'named_identified')
        self.assertTrue(all(r[c]['group'] == 'linked_set' for c in SEL['linked_set']))


def write_read(root, label, files, log_extra=None):
    d = Path(root) / ('read-' + label)
    d.mkdir(parents=True)
    rows = []
    for name, (status, obj) in files.items():
        body = obj if isinstance(obj, bytes) else json.dumps(obj).encode()
        (d / (name + '.raw.gz')).write_bytes(gzip.compress(body, mtime=0))
        rows.append({'name': name, 'status': status, 'bytes': len(body), 'file': name + '.raw.gz'})
    rows += log_extra or []
    (d / 'read_log.json').write_text(json.dumps(rows))


def epss_obj(cve, series):
    dates = sorted(series, reverse=True)
    return {'data': [{'cve': cve, 'date': dates[0], 'epss': str(series[dates[0]][0]),
                      'percentile': str(series[dates[0]][1]),
                      'time-series': [{'date': d, 'epss': str(series[d][0]), 'percentile': str(series[d][1])}
                                      for d in dates[1:]]}], 'pad': 'x' * 200}


def cve_rec(score):
    return {'cveMetadata': {'datePublished': '2026-10-15T00:00:00Z', 'dateUpdated': '2026-10-20T00:00:00Z',
                            'assignerShortName': 'Linux'},
            'containers': {'cna': {'providerMetadata': {'shortName': 'Linux', 'orgId': 'L1', 'dateUpdated': 'x'},
                                   'metrics': [{'cvssV3_1': {'baseScore': score, 'vectorString': 'v'}}]}},
            'pad': 'x' * 200}


class Constructed(unittest.TestCase):
    """A small constructed study: one named Linux flaw over three reads."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.sel = {'rule_applied_at': 'test', 'linked_set': [],
                    'units': [{'chain': 'linux', 'step': 'L', 'class': 'named', 'cves': ['CVE-2026-1'],
                               'candidates': []},
                              {'chain': 'android', 'step': 'A', 'class': 'no identifier', 'cves': [],
                               'candidates': []}]}
        kev0 = {'catalogVersion': '1', 'dateReleased': 'd', 'count': 0, 'vulnerabilities': [], 'pad': 'x' * 200}
        kev2 = dict(kev0, vulnerabilities=[{'cveID': 'CVE-2026-1', 'dateAdded': '2026-11-20', 'dueDate': 'x',
                                            'knownRansomwareCampaignUse': 'Unknown', 'notes': ''}])
        nvd = {'vulnerabilities': [{'cve': {'vulnStatus': 'Received', 'lastModified': 'm', 'metrics': {}}}],
               'pad': 'x' * 200}
        write_read(self.tmp.name, '2026-11-10T1400Z', {
            'kev': (200, kev0), 'epss_0': (200, epss_obj('CVE-2026-1', {
                '2026-10-24': (0.001, 0.30), '2026-10-25': (0.002, 0.40),        # x2: a step
                '2026-10-26': (0.0011, 0.35)})),                                   # /1.82: not a step
            'cve_org_CVE-2026-1': (200, cve_rec(8.8)), 'nvd_CVE-2026-1': (200, nvd)})
        write_read(self.tmp.name, '2026-11-16T1400Z', {
            'kev': (503, b'busy'), 'epss_0': (200, epss_obj('CVE-2026-1', {
                '2026-10-26': (0.0099, 0.99),                                      # earlier read's value kept
                '2026-10-28': (0.0030, 0.45)})),                                   # gap of a day: not day-on-day
            'cve_org_CVE-2026-1': (404, b'{}'), 'nvd_CVE-2026-1': (200, nvd)})
        write_read(self.tmp.name, '2026-11-23T1400Z', {
            'kev': (200, kev2), 'epss_0': (200, epss_obj('CVE-2026-1', {'2026-11-22': (0.0031, 0.50)})),
            'cve_org_CVE-2026-1': (200, cve_rec(9.8)), 'nvd_CVE-2026-1': (200, nvd)})
        self.out = T.tabulate(self.tmp.name, self.sel)

    def tearDown(self):
        self.tmp.cleanup()

    def flaw(self, label):
        return self.out['as_of'][label]['flaws']['named_identified']['CVE-2026-1']

    def test_epss(self):
        e = self.flaw('2026-11-23T1400Z')['measure2_epss']
        self.assertEqual([s['date'] for s in e['steps']], ['2026-10-25'])
        self.assertEqual(e['steps'][0]['days_from_E2'], -2)
        self.assertEqual(e['steps'][0]['days_from_V'], 10)
        self.assertEqual(e['steps'][0]['days_from_K'], -26)
        self.assertEqual(len(e['factor_two_changes_across_missing_dates']), 1)
        held = {s['date']: s for s in e['series']}
        self.assertEqual(held['2026-10-26']['epss'], 0.0011)          # earliest read's value
        self.assertEqual(len(e['later_read_differences']), 1)
        self.assertFalse(e['percentile_ever_above_0_5'])                # 0.99 was a later, discarded value
        self.assertEqual(e['last_date_held']['percentile'], 0.50)

    def test_kev_interval_skips_unavailable(self):
        k = self.flaw('2026-11-23T1400Z')['measure3_kev']
        self.assertEqual(k['per_read']['2026-11-16T1400Z'], T.UNAVAILABLE)
        self.assertEqual(k['K'], '2026-11-20')
        self.assertEqual(k['interval'], {'after_read': '2026-11-10T1400Z', 'at_or_before_read': '2026-11-23T1400Z'})

    def test_rating_change_and_no_record(self):
        m1 = self.flaw('2026-11-23T1400Z')['measure1_severity']
        self.assertEqual(m1['per_read']['2026-11-16T1400Z']['cve_record'], T.NO_RECORD)
        ch = [c for c in m1['rating_changes'] if c['key'] == 'cna:Linux:cvssV3_1']
        # "no record" is a reading, so 8.8 -> no record -> 9.8 are two changes, each with its interval
        self.assertEqual(len(ch), 2)
        self.assertEqual(ch[1]['to']['band'], 'Critical')
        self.assertEqual(ch[1]['after_read'], '2026-11-16T1400Z')

    def test_gap_parts(self):
        g0 = self.flaw('2026-11-10T1400Z')['measure4_gap_parts']
        self.assertIs(g0['rated_high_or_critical'], True)
        self.assertIs(g0['epss_percentile_at_or_below_0_5_on_last_date_held'], True)
        self.assertIs(g0['not_in_kev_at_last_read'], True)
        self.assertIs(g0['meets_all_three'], True)
        g1 = self.flaw('2026-11-16T1400Z')['measure4_gap_parts']
        self.assertEqual(g1['not_in_kev_at_last_read'], T.UNKNOWN)      # KEV unavailable: unknown, not no
        # the CVE record answered 404 ("no record", a reading) and NVD gives no metric: no source rates it High
        self.assertIs(g1['rated_high_or_critical'], False)
        self.assertIs(g1['meets_all_three'], False)                     # one part is False, so not unknown
        g2 = self.flaw('2026-11-23T1400Z')['measure4_gap_parts']
        self.assertIs(g2['epss_percentile_at_or_below_0_5_on_last_date_held'], True)   # 0.50 is at or below
        self.assertIs(g2['not_in_kev_at_last_read'], False)
        self.assertIs(g2['meets_all_three'], False)

    def test_no_identifier_unknown(self):
        u = self.out['units_unknown_in_every_measure']
        self.assertEqual(u, [{'chain': 'android', 'step': 'A', 'class': 'no identifier', 'all_measures': 'unknown'}])
        ch = self.out['as_of']['2026-11-23T1400Z']['chains_side_by_side']['android']
        self.assertFalse(ch['has_named_or_identified_flaw'])


class Replay(unittest.TestCase):
    def test_deterministic_on_held_reads(self):
        data = HERE.parent / 'data'
        a = json.dumps(T.tabulate(data, SEL, '2026-11-10T1418Z'), sort_keys=True)
        b = json.dumps(T.tabulate(data, SEL, '2026-11-10T1418Z'), sort_keys=True)
        self.assertEqual(a, b)
        full1 = json.dumps(T.tabulate(data, SEL), indent=1, sort_keys=True, ensure_ascii=False) + '\n'
        full2 = json.dumps(T.tabulate(data, SEL), indent=1, sort_keys=True, ensure_ascii=False) + '\n'
        self.assertEqual(full1, full2)
        held = data / 'tables.json'
        if held.exists():
            self.assertEqual(held.read_text(), full1, 'data/tables.json differs from a fresh replay')

    def test_baseline_values(self):
        t = T.tabulate(HERE.parent / 'data', SEL, '2026-11-10T1418Z')['as_of']['2026-11-10T1418Z']
        L = t['flaws']['named_identified']['CVE-2026-98432']
        self.assertEqual(L['measure2_epss']['last_date_held'], {'date': '2026-11-09', 'epss': 0.0076,
                                                                'percentile': 0.55549})
        self.assertEqual([s['date'] for s in L['measure2_epss']['steps']], ['2026-10-25'])
        c = t['flaws']['ambiguous_candidates']['CVE-2026-113192']
        self.assertEqual(c['measure1_severity']['per_read']['2026-11-10T1418Z']['vendor']['chrome_word'],
                         T.UNAVAILABLE)                                   # the page answered 503 at the baseline
        self.assertEqual(c['measure1_severity']['chrome_word_on_discovery_copy']['word'], 'High')


if __name__ == '__main__':
    unittest.main(verbosity=1)
