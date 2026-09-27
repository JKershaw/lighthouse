#!/usr/bin/env python3
"""Checks for LH010's reanalysis (reanalyse.py) and its baseline replay. Standard library only; no network.
Run from anywhere:  python3 -m unittest discover -s studies/LH010/scripts -p 'test_*.py'

Synthetic fixtures check the two new rules (the earliest reviewed advisory naming the fix; the notes-evidence
states); two checks on the real retained data confirm that analyse.py, replayed into a separate directory,
writes the committed tables byte for byte, and that the reanalysis with the original clock and every event
reproduces version 0.2's library-unit and pooled figures."""
import csv, datetime, filecmp, os, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import reanalyse as R  # noqa: E402
import analyse as A  # noqa: E402
from common import ts, DATA  # noqa: E402

BASELINE = ['lags.csv', 'summary_by_event.csv', 'summary_by_class.csv', 'hazard_by_class.csv', 'library_rates.csv',
            'library_unit.csv', 'by_authorship.csv', 'within_library.csv']


def rec(id, published, fixed, project='lib', reviewed='True', withdrawn='', nvd=''):
    return dict(project=project, rank='1', id=id, aliases='', severity='MODERATE', github_reviewed=reviewed,
                published=published, modified=published, withdrawn=withdrawn, github_reviewed_at=published if reviewed else '',
                nvd_published_at=nvd, fixed=fixed, summary='')


OSV = [
    rec('GHSA-even-t000-0001', '2026-05-10T00:00:00Z', '1.2.0', nvd='2026-05-12T00:00:00Z'),  # the event advisory
    rec('GHSA-earl-y000-0002', '2026-04-01T00:00:00Z', '1.1.9 1.2.0'),  # earlier, names the fix in a second range
    rec('GHSA-with-draw-0003', '2026-03-01T00:00:00Z', '1.2.0', withdrawn='2026-03-02T00:00:00Z'),  # withdrawn
    rec('GHSA-unre-view-0004', '2026-02-01T00:00:00Z', '1.2.0', reviewed=''),  # not reviewed
    rec('PYSEC-2026-5', '2026-01-01T00:00:00Z', '1.2.0', reviewed=''),  # not a GHSA record
    rec('GHSA-late-r000-0006', '2026-06-01T00:00:00Z', '1.2.0', nvd='2026-03-20T00:00:00Z'),  # later, earlier NVD time
    rec('GHSA-othe-rfix-0007', '2026-01-15T00:00:00Z', '1.2.1'),  # names another fix
    rec('GHSA-othe-rlib-0008', '2025-01-01T00:00:00Z', '1.2.0', project='otherlib'),  # another library
]


class EarliestClock(unittest.TestCase):
    def test_picks_earliest_reviewed_before_the_window(self):
        r = R.earliest_reviewed(OSV, 'lib', '1.2.0')
        self.assertEqual(r['id'], 'GHSA-earl-y000-0002')

    def test_ignores_withdrawn_unreviewed_other_fix_and_other_library(self):
        ids = [x['id'] for x in R.records_naming_fix(OSV, 'lib', '1.2.0') if R.counted(x)[0]]
        self.assertEqual(sorted(ids), ['GHSA-earl-y000-0002', 'GHSA-even-t000-0001', 'GHSA-late-r000-0006'])
        self.assertEqual(R.counted(OSV[2]), (False, 'withdrawn'))
        self.assertEqual(R.counted(OSV[3]), (False, 'not GitHub-reviewed'))
        self.assertEqual(R.counted(OSV[4]), (False, 'not a GHSA record'))

    def test_later_advisory_not_picked_but_its_nvd_time_counts_for_earliest_public(self):
        t, id, field = R.earliest_public(OSV, 'lib', '1.2.0')
        self.assertEqual((R.iso(t), id, field), ('2026-03-20T00:00:00Z', 'GHSA-late-r000-0006', 'nvd_published_at'))

    def test_clock_before_the_release_leaves_no_time_before_it(self):
        frame = dict(frame='lib:event', library='lib', kind='event', fixed_release='1.2.0',
                     fixed_uploaded='2026-04-10T00:00:00Z', advisory='GHSA-even-t000-0001',
                     advisory_published='2026-05-10T00:00:00Z', nvd_published_at='2026-05-12T00:00:00Z', cls='announced')
        c, recs = R.build_clocks([frame], OSV)
        c = c[0]
        self.assertEqual(c['earliest_reviewed'], '2026-04-01T00:00:00Z')
        self.assertEqual((c['earliest_reviewed_differs'], c['earliest_reviewed_before_release']), ('yes', 'yes'))
        self.assertEqual(len(recs), 6)  # every record against lib naming 1.2.0, counted or not
        pair = dict(release_time='2026-04-10T00:00:00Z', advisory_time=c['earliest_reviewed'], committer_time='2026-04-12T00:00:00Z',
                    outcome='moved', end_of_observation='2026-09-27T10:00:00Z', library='lib')
        n, at = A.hazard([pair], A.REL, A.ADV)
        self.assertEqual((n, at), (0, 0.0))
        pair['advisory_time'] = c['event_advisory_published']
        n, at = A.hazard([pair], A.REL, A.ADV)
        self.assertEqual((n, round(at, 3)), (1, 2.0))


def text(source, dated, body, where='x'):
    return dict(source=source, where=where, dated=dated, chars=str(len(body)), security_words='', text=body)


UP = '2026-03-30T20:25:35Z'
NOPART = '(no part of the description names this version)'


class NotesState(unittest.TestCase):
    def test_no_notes_in_any_source_is_insufficient(self):
        ts_ = [text('tag annotation', '', ''), dict(text('PyPI description', UP, NOPART), chars='0')]
        self.assertEqual(R.notes_state('silent', ts_, UP)[0], 'c')
        self.assertEqual(R.notes_state('silent', [], UP)[0], 'c')

    def test_entry_without_announcement_is_inspected_silent(self):
        ts_ = [text('changelog at tag', '2026-03-30T19:55:23Z', '## 3.2.0\n\n- Fix the parser when a header repeats.')]
        self.assertEqual(R.notes_state('silent', ts_, UP)[0], 'b')

    def test_entry_written_only_after_release_is_insufficient_at_release(self):
        ts_ = [text('tag annotation', '', ''),
               text('changelog after the tag (history)', '2026-06-03T02:15:02Z', '**v3.2.0**\n\nA security hardening pass across SSRF.'),
               text('changelog at head', '2026-09-27T02:17:29Z', '**v3.2.0**\n\nA security hardening pass across SSRF.')]
        st, usable, notes = R.notes_state('silent', ts_, UP)
        self.assertEqual(st, 'c')
        self.assertTrue(any('after the 24 hours' in n for n in notes))

    def test_bare_bump_annotation_alone_is_insufficient_but_not_beside_an_entry(self):
        bump = text('tag annotation', '2026-03-01T15:56:54Z', 'Bump version: 1.2.1 → 1.2.2')
        self.assertEqual(R.notes_state('silent', [bump], '2026-03-01T16:00:25Z')[0], 'c')
        entry = text('changelog at tag', '2026-03-01T15:56:49Z', '## [v1.2.2] - 2026-03-01\n\n### Added\n\n- Support for Python 3.14.')
        self.assertEqual(R.notes_state('silent', [bump, entry], '2026-03-01T16:00:25Z')[0], 'b')

    def test_announced_is_a(self):
        ts_ = [text('changelog at tag', UP, 'Security fixes: a path traversal.')]
        self.assertEqual(R.notes_state('announced', ts_, UP)[0], 'a')

    def test_substantive(self):
        for s in ('Release 26.1', 'Release: 2.7.0', 'sig', 'This is 0.6.0.', 'Tagging 1.44.78 release.', 'version 3.9.3',
                  '46.0.6 release\n-----BEGIN SIGNED MESSAGE-----\nMIIEOQYJKoZIhvcNAQcCoIIEKjCCBCYCAQExDTALBglghkgBZQMEAgEw'):
            self.assertFalse(R.substantive(s), s)
        for s in ('1.6.7\n-----\n\n**Released on May 23, 2026**\n\n- Update for type hints.',
                  '0.32.0\n\n  decompression limited by size and ratio'):
            self.assertTrue(R.substantive(s), s)


class RetainedData(unittest.TestCase):
    def test_baseline_replay_equals_committed_tables(self):
        with tempfile.TemporaryDirectory() as d:
            env = dict(os.environ, LH010_OUT=d)
            subprocess.run([sys.executable, os.path.join(HERE, 'analyse.py')], env=env, check=True, capture_output=True)
            for name in BASELINE:
                self.assertTrue(filecmp.cmp(os.path.join(d, name), os.path.join(DATA, name), shallow=False), name)

    def test_original_clock_and_every_event_reproduce_version_0_2(self):
        ev = [r for r in A.load() if r['kind'] == 'event']
        with open(os.path.join(DATA, 'library_unit.csv')) as f:
            lu = {(x['grouping'], x['window']): x for x in csv.DictReader(f)}
        for window in A.UNIT_WINDOWS:
            cell = R.compare(ev, 'cls', window)
            v02 = lu[('class', window)]
            self.assertEqual(str(cell['announced_median']), v02['announced_median'])
            self.assertEqual(str(cell['silent_median']), v02['silent_median'])
            self.assertEqual(str(cell['permutation_p']), v02['permutation_p_two_sided'])
            self.assertEqual(str(cell['announced_pooled']), v02['announced_pooled'])
            self.assertEqual(cell['silent_pooled_leave_one_out'], v02['silent_pooled_leave_one_out'])


if __name__ == '__main__':
    unittest.main()
