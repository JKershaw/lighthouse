#!/usr/bin/env python3
"""LH008 step 5: the tables. No network access.
data/lags.csv             one row per kept repository (per frame): outcome, lags in days from the release,
                          from the advisory (GHSA time) and, for pyjwt and urllib3, from the NVD/PYSEC time;
                          whether it held exactly the release before; the next advisory after a comparison release.
data/summary_by_frame.csv per frame and pooled by kind: kept, moved, censored, removed; quartiles of lags
                          among movers; counts within windows of the release and of the advisory.
data/by_authorship.csv    by kind and authorship class: moves, and those within 2 days after the advisory.
data/advisory_window.csv  fix frames: moves in each day from 7 days before to 7 days after the advisory."""
import datetime, os, statistics, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv, ts, iso, norm
from packaging.version import Version

EV = {e['library']: e for e in read_csv('events.csv') if e['chosen'] == 'yes'}
# NVD publication of the CVEs aliased by the chosen advisories, where OSV gives it (events.csv), which is also
# when the PYSEC records appeared (osv_advisories.csv); used as a second advisory time.
ADV = read_csv('osv_advisories.csv')
DAY = 86400.0


def days(a, b):
    return (ts(a) - ts(b)).total_seconds() / DAY


def next_advisory(lib, after):
    later = [a for a in ADV if a['project'] == lib and a['published'] and ts(a['published']) > ts(after)]
    return min(later, key=lambda a: ts(a['published'])) if later else None


def quart(xs):
    if not xs:
        return '', '', ''
    xs = sorted(xs)
    if len(xs) == 1:
        return xs[0], xs[0], xs[0]
    q = statistics.quantiles(xs, n=4, method='inclusive')
    return round(q[0], 2), round(statistics.median(xs), 2), round(q[2], 2)


def main():
    rows = []
    screen = read_csv('screen.csv')
    TR = {(t['frame'], t['package']): t for t in read_csv('trailers.csv')}
    for m in read_csv('moves.csv'):
        e = EV[m['library']]
        kind = m['kind']
        r = dict(frame=m['frame'], library=m['library'], kind=kind, package=m['package'], repo=m['repo'],
                 held_min=m['held_min'], held_release_before='yes' if Version(m['held_min']) == Version(
                     e['release_before_fix'] if kind == 'fix' else e['release_before_comparison']) else 'no',
                 outcome=m['outcome'].split(':')[0], move_commit=m['move_commit'], committer_time=m['committer_time'],
                 author_time=m['author_time'], moved_to=m['moved_to'], authorship=m['authorship'], bot_name=m['bot_name'],
                 security_word=m['security_word'], ai_coauthor=TR.get((m['frame'], m['package']), {}).get('ai_coauthor', ''), release_time=iso(ts(m['release_time'])))
        r['lag_release_days'] = round(days(m['committer_time'], m['release_time']), 3) if m['committer_time'] else ''
        r['lag_release_days_author_time'] = round(days(m['author_time'], m['release_time']), 3) if m['author_time'] else ''
        if kind == 'fix':
            r['advisory_time'] = e['advisory_published']
            r['lag_advisory_days'] = round(days(m['committer_time'], e['advisory_published']), 3) if m['committer_time'] else ''
            r['nvd_time'] = e['nvd_published_at']
            r['lag_nvd_days'] = round(days(m['committer_time'], e['nvd_published_at']), 3) if m['committer_time'] and e['nvd_published_at'] else ''
        else:
            na = next_advisory(m['library'], m['release_time'])
            r['next_advisory'] = na['id'] if na else ''
            r['next_advisory_time'] = na['published'] if na else ''
            r['after_next_advisory'] = ('yes' if na and m['committer_time'] and ts(m['committer_time']) > ts(na['published']) else 'no') if m['committer_time'] else ''
        r['active_after_release'] = 'yes' if m['outcome'] == 'moved' or ts(m['head_time']) > ts(m['release_time']) + datetime.timedelta(days=30) else 'no'
        r['shared_by'] = ' '.join(s['package'] for s in screen if s['frame'] == m['frame'] and s['repo'] == m['repo'] and s['package'] != m['package'] and s['kept'] == 'yes')
        rows.append(r)
    fields = ['frame', 'library', 'kind', 'package', 'shared_by', 'repo', 'held_min', 'held_release_before', 'outcome',
              'move_commit', 'committer_time', 'author_time', 'moved_to', 'release_time', 'lag_release_days',
              'lag_release_days_author_time', 'advisory_time', 'lag_advisory_days', 'nvd_time', 'lag_nvd_days',
              'next_advisory', 'next_advisory_time', 'after_next_advisory', 'active_after_release', 'authorship', 'bot_name', 'security_word', 'ai_coauthor']
    write_csv('lags.csv', rows, fields)

    def summ(label, kind, rs):
        mv = [r for r in rs if r['outcome'] == 'moved']
        lr = [r['lag_release_days'] for r in mv]
        out = dict(group=label, kind=kind, kept=len(rs), moved=len(mv),
                   censored=sum(r['outcome'].startswith('censored') or r['outcome'].startswith('not moved') for r in rs),
                   removed=sum(r['outcome'] == 'removed' for r in rs))
        out['lag_release_q1'], out['lag_release_median'], out['lag_release_q3'] = quart(lr)
        for d in (1, 2, 7, 30):
            out[f'moved_within_{d}d_of_release'] = sum(0 <= x <= d for x in lr)
        out['negative_release_lag'] = sum(x < 0 for x in lr)
        if kind == 'fix':
            la = [r['lag_advisory_days'] for r in mv]
            out['moved_before_advisory'] = sum(x < 0 for x in la)
            out['lag_advisory_q1'], out['lag_advisory_median'], out['lag_advisory_q3'] = quart([x for x in la if x >= 0])
            for d in (1, 2, 7, 30):
                out[f'moved_within_{d}d_after_advisory'] = sum(0 <= x <= d for x in la)
            out['moved_2d_before_advisory'] = sum(-2 <= x < 0 for x in la)
        else:
            out['moved_after_next_advisory'] = sum(r['after_next_advisory'] == 'yes' for r in mv)
            out['moved_within_30d_of_release_and_after_next_advisory'] = sum(
                r['after_next_advisory'] == 'yes' and r['lag_release_days'] <= 30 for r in mv)
        return out

    S = []
    for fr in sorted({r['frame'] for r in rows}, key=lambda f: (f.split(':')[1], f)):
        rs = [r for r in rows if r['frame'] == fr]
        S.append(summ(fr, rs[0]['kind'], rs))
    for kind in ('fix', 'comparison'):
        rs = [r for r in rows if r['kind'] == kind]
        S.append(summ(f'all {kind} frames', kind, rs))
        S.append(summ(f'all {kind} frames, held exactly the release before', kind, [r for r in rs if r['held_release_before'] == 'yes']))
    for kind in ('fix', 'comparison'):
        S.append(summ(f'all {kind} frames, repositories with a commit more than 30 days after the release or a move', kind,
                      [r for r in rows if r['kind'] == kind and r['active_after_release'] == 'yes']))
    pj = [r for r in rows if r['library'] == 'pyjwt' and r['kind'] == 'fix' and r['outcome'] == 'moved']
    S.append(dict(group='pyjwt:fix, against the NVD/PYSEC time (2026-05-28T16:16:29Z)', kind='fix', kept=sum(r['library'] == 'pyjwt' and r['kind'] == 'fix' for r in rows),
                  moved=len(pj), moved_before_advisory=sum(r['lag_nvd_days'] < 0 for r in pj),
                  moved_within_1d_after_advisory=sum(0 <= r['lag_nvd_days'] <= 1 for r in pj),
                  moved_within_2d_after_advisory=sum(0 <= r['lag_nvd_days'] <= 2 for r in pj),
                  moved_within_7d_after_advisory=sum(0 <= r['lag_nvd_days'] <= 7 for r in pj)))
    keys = list(dict.fromkeys(k for s in S for k in s))
    write_csv('summary_by_frame.csv', S, keys)

    A = []
    for kind in ('fix', 'comparison'):
        for cls in ("bot", "person merging a bot's branch", 'person'):
            mv = [r for r in rows if r['kind'] == kind and r['outcome'] == 'moved' and r['authorship'] == cls]
            a = dict(kind=kind, authorship=cls, moves=len(mv),
                     within_2d_of_release=sum(0 <= r['lag_release_days'] <= 2 for r in mv),
                     with_security_word=sum(bool(r['security_word']) for r in mv),
                     bots=' '.join(f'{k} ({v})' for k, v in collections.Counter(r['bot_name'] for r in mv if r['bot_name']).most_common()))
            if kind == 'fix':
                a['before_advisory'] = sum(r['lag_advisory_days'] < 0 for r in mv)
                a['within_2d_after_advisory'] = sum(0 <= r['lag_advisory_days'] <= 2 for r in mv)
                a['within_2d_after_advisory_with_security_word'] = sum(0 <= r['lag_advisory_days'] <= 2 and bool(r['security_word']) for r in mv)
            A.append(a)
    write_csv('by_authorship.csv', A, ['kind', 'authorship', 'moves', 'within_2d_of_release', 'before_advisory',
                                       'within_2d_after_advisory', 'with_security_word',
                                       'within_2d_after_advisory_with_security_word', 'bots'])

    W = []
    fixmv = [r for r in rows if r['kind'] == 'fix' and r['outcome'] == 'moved']
    for dday in range(-7, 7):
        W.append(dict(day_from_advisory=f'{dday} to {dday + 1}',
                      **{lib: sum(dday <= r['lag_advisory_days'] < dday + 1 for r in fixmv if r['library'] == lib) for lib in EV},
                      all=sum(dday <= r['lag_advisory_days'] < dday + 1 for r in fixmv)))
    write_csv('advisory_window.csv', W)
    # repo-days at risk and moves per 100 repo-days in windows (derived). A repository is at risk from the
    # window's start until its move, removal, or the end of observation (its clone time, read_log.csv).
    clone_t = {}
    for x in read_csv('read_log.csv'):
        if x['source'] == 'git over HTTPS' and x['endpoint'] not in clone_t:
            clone_t[x['endpoint']] = x['read_utc']
    MV = {(m['frame'], m['package']): m for m in read_csv('moves.csv')}
    H = []

    def hazard(kind, label, rs, lo_of, hi_of):
        """lo_of and hi_of give each pair's window bounds; the window is clipped at the clone time."""
        at_risk, n = 0.0, 0
        for r in rs:
            end_obs = ts(clone_t.get('https://' + r['repo'] + '.git', '2026-09-27T07:30:00Z'))
            lo, hi = lo_of(r), min(hi_of(r), end_obs)
            t_ev = ts(r['committer_time']) if r['committer_time'] else end_obs
            if t_ev <= lo or hi <= lo:
                continue
            at_risk += (min(t_ev, hi) - lo).total_seconds() / DAY
            n += r['outcome'] == 'moved' and lo <= t_ev < hi
        H.append(dict(kind=kind, window=label, repositories=len(rs), moves=n, repo_days_at_risk=round(at_risk, 1),
                      moves_per_100_repo_days=round(100 * n / at_risk, 2) if at_risk else ''))

    fx = [r for r in rows if r['kind'] == 'fix']
    cmp_ = [r for r in rows if r['kind'] == 'comparison']
    rel0 = lambda r: ts(r['release_time'])
    adv0 = lambda r: ts(r['advisory_time'])
    td = datetime.timedelta
    # Windows from the fixed release. urllib3's advisory came 3.9 days and cryptography's 5.9 days after the
    # release, so a window from +2 to +7 days straddles them; the second row stops at the advisory where it came
    # first (the review, R-0008, found the earlier row's "all before the advisory" label wrong: 5 of its 10 moves
    # were urllib3's after its advisory). The +2 to +7 row is kept, labelled, for comparison with rates.svg's
    # earlier edition.
    hazard('fix', 'release +0 to +2 days (before every advisory)', fx, rel0, lambda r: rel0(r) + td(days=2))
    hazard('fix', 'release +2 to +7 days, or to the advisory where it came first (urllib3 +3.9, cryptography +5.9)',
           fx, lambda r: rel0(r) + td(days=2), lambda r: min(rel0(r) + td(days=7), adv0(r)))
    hazard('fix', 'release +2 to +7 days (mixed: includes 5 urllib3 moves after its advisory)',
           fx, lambda r: rel0(r) + td(days=2), lambda r: rel0(r) + td(days=7))
    hazard('fix', 'release +2 days to the advisory (all four libraries)', fx, lambda r: rel0(r) + td(days=2), adv0)
    hazard('fix', 'release +7 days to the advisory (pyjwt and starlette, whose advisories came 25 and 23 days after)',
           [r for r in fx if r['library'] in ('pyjwt', 'starlette')], lambda r: rel0(r) + td(days=7), adv0)
    # Windows from the advisory. The week before it starts at the release where that came later (urllib3,
    # cryptography), since no pair could move to a fix before the fix existed; that row therefore includes the
    # release's own days for those two libraries.
    hazard('fix', 'advisory -7 to +0 days, from the release at the earliest (includes release days for urllib3 and cryptography)',
           fx, lambda r: max(adv0(r) - td(days=7), rel0(r)), adv0)
    for a, b in ((0, 1), (0, 2), (2, 7), (7, 30), (30, 90)):
        hazard('fix', f'advisory {a:+d} to {b:+d} days', fx, lambda r, a=a: adv0(r) + td(days=a), lambda r, b=b: adv0(r) + td(days=b))
    for a, b in ((0, 2), (2, 7), (7, 30), (30, 90)):
        hazard('comparison', f'release +{a} to +{b} days', cmp_, lambda r, a=a: rel0(r) + td(days=a), lambda r, b=b: rel0(r) + td(days=b))
    write_csv('hazard.csv', H)
    for h in H:
        print(h)
    for s in S:
        print({k: v for k, v in s.items() if v != ''})
    for a in A:
        print(a)
    for w in W:
        print(w)


if __name__ == '__main__':
    main()
