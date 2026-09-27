#!/usr/bin/env python3
"""LH009 step 5: the tables, by class. No network access. Modelled on LH008's analyse.py.

Pairs are the kept repository and event pairs of all sixteen fix frames: LH008's four (from studies/LH008/data,
kind 'fix', as they stand at commit 76043cb) and LH009's twelve (data/moves.csv). Each event's class is from
data/fix_classes.csv.

data/lags.csv              one row per pair: class, outcome, lags from the release and the advisory.
data/summary_by_event.csv  per event: gap, kept, moved, censored, removed, moves before the advisory, rates.
data/summary_by_class.csv  pooled by class (and by strict class): the same, and the median of the events' rates.
data/hazard_by_class.csv   moves per 100 repository-days at risk, by class and window, with the moves counted.
data/by_authorship.csv     by class and authorship class.
"""
import csv, datetime, os, statistics, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv, ts, iso

LH008 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'LH008', 'data')
DAY = 86400.0
td = datetime.timedelta


def rd(path):
    return list(csv.DictReader(open(path)))


EV = {e['library']: e for e in rd(os.path.join(LH008, 'events.csv'))}
CL = {r['library']: r for r in read_csv('fix_classes.csv') if r['event'] == 'yes'}


def clone_times(log):
    out = {}
    for x in rd(log):
        if x['source'] == 'git over HTTPS' and x['endpoint'] not in out and x['note'] in ('cloned', 'already cloned'):
            out[x['endpoint']] = x['read_utc']
    return out


CT = {**clone_times(os.path.join(LH008, 'read_log.csv')), **clone_times(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'read_log.csv'))}


def days(a, b):
    return (ts(a) - ts(b)).total_seconds() / DAY


def quart(xs):
    if not xs:
        return '', '', ''
    xs = sorted(xs)
    if len(xs) == 1:
        return round(xs[0], 2), round(xs[0], 2), round(xs[0], 2)
    q = statistics.quantiles(xs, n=4, method='inclusive')
    return round(q[0], 2), round(statistics.median(xs), 2), round(q[2], 2)


def load():
    rows = []
    srcs = [('LH008', [m for m in rd(os.path.join(LH008, 'moves.csv')) if m['kind'] == 'fix'],
             {(t['frame'], t['package']): t for t in rd(os.path.join(LH008, 'trailers.csv'))}),
            ('LH009', read_csv('moves.csv'), {(t['frame'], t['package']): t for t in read_csv('trailers.csv')})]
    for src, moves, tr in srcs:
        for m in moves:
            e, c = EV[m['library']], CL[m['library']]
            adv = e['advisory_published']
            nvd = e['nvd_published_at']
            first_public = min([ts(adv)] + ([ts(nvd)] if nvd else []))
            end_obs = CT.get('https://' + m['repo'] + '.git')
            r = dict(source=src, library=m['library'], cls=c['class'], strict_class=c['strict_class'],
                     package=m['package'], repo=m['repo'], held_min=m['held_min'],
                     outcome=m['outcome'].split(':')[0].replace('not moved within the first 400 commits touching pin or lock files (cap)', 'capped'),
                     move_commit=m['move_commit'], committer_time=m['committer_time'], author_time=m['author_time'],
                     moved_to=m['moved_to'], authorship=m['authorship'], bot_name=m['bot_name'],
                     security_word=m['security_word'], ai_coauthor=tr.get((m['frame'], m['package']), {}).get('ai_coauthor', ''),
                     release_time=iso(ts(m['release_time'])), advisory_time=adv, first_public_time=iso(first_public),
                     end_of_observation=end_obs or '')
            if m['committer_time']:
                r['lag_release_days'] = round(days(m['committer_time'], r['release_time']), 3)
                r['lag_advisory_days'] = round(days(m['committer_time'], adv), 3)
                r['lag_first_public_days'] = round(days(m['committer_time'], r['first_public_time']), 3)
                r['lag_release_days_author_time'] = round(days(m['author_time'], r['release_time']), 3)
            else:
                r['lag_release_days'] = r['lag_advisory_days'] = r['lag_first_public_days'] = r['lag_release_days_author_time'] = ''
            rows.append(r)
    return rows


def hazard(rs, lo_of, hi_of):
    """(moves, repository-days at risk) in the window [lo, hi) of each pair, clipped at the end of observation."""
    at, n = 0.0, 0
    for r in rs:
        end = ts(r['end_of_observation']) if r['end_of_observation'] else ts('2026-09-27T09:00:00Z')
        lo, hi = lo_of(r), min(hi_of(r), end)
        t_ev = ts(r['committer_time']) if r['committer_time'] else end
        if t_ev <= lo or hi <= lo:
            continue
        at += (min(t_ev, hi) - lo).total_seconds() / DAY
        n += r['outcome'] == 'moved' and lo <= t_ev < hi
    return n, at


REL = lambda r: ts(r['release_time'])
ADV = lambda r: ts(r['advisory_time'])
PUB = lambda r: ts(r['first_public_time'])
WINDOWS = [
    ('release +0 to +2 days, or to the advisory where it came first', REL, lambda r: min(REL(r) + td(days=2), ADV(r))),
    ('release +2 days to the advisory', lambda r: REL(r) + td(days=2), ADV),
    ('release to the advisory (all of it)', REL, ADV),
    ('release +2 to +7 days, stopping at the advisory', lambda r: REL(r) + td(days=2), lambda r: min(REL(r) + td(days=7), ADV(r))),
    ('release +7 to +30 days, stopping at the advisory', lambda r: REL(r) + td(days=7), lambda r: min(REL(r) + td(days=30), ADV(r))),
    ('advisory +0 to +2 days', ADV, lambda r: ADV(r) + td(days=2)),
    ('advisory +2 to +7 days', lambda r: ADV(r) + td(days=2), lambda r: ADV(r) + td(days=7)),
    ('advisory +7 to +30 days', lambda r: ADV(r) + td(days=7), lambda r: ADV(r) + td(days=30)),
    ('advisory +30 to +90 days', lambda r: ADV(r) + td(days=30), lambda r: ADV(r) + td(days=90)),
    ('release to the first public record (GHSA or NVD, whichever first)', REL, PUB),
]


def rate(n, at):
    return round(100 * n / at, 2) if at else ''


def summ(label, rs, **extra):
    mv = [r for r in rs if r['outcome'] == 'moved']
    lr = [r['lag_release_days'] for r in mv]
    la = [r['lag_advisory_days'] for r in mv]
    before = sum(x < 0 for x in la)
    out = dict(group=label, **extra, kept=len(rs), moved=len(mv),
               censored=sum(r['outcome'].startswith('censored') or r['outcome'] == 'capped' for r in rs),
               removed=sum(r['outcome'] == 'removed' for r in rs), moved_before_advisory=before,
               share_of_moves_before_advisory=f'{before}/{len(mv)}' + (f' ({round(100 * before / len(mv))}%)' if mv else ''),
               share_of_kept_moving_before_advisory=f'{before}/{len(rs)}' + (f' ({round(100 * before / len(rs))}%)' if rs else ''),
               moved_before_first_public=sum(r['lag_first_public_days'] < 0 for r in mv),
               moved_within_2d_of_release=sum(0 <= x <= 2 for x in lr),
               moved_within_2d_after_advisory=sum(0 <= x <= 2 for x in la),
               moved_within_7d_after_advisory=sum(0 <= x <= 7 for x in la),
               moved_within_30d_of_release=sum(0 <= x <= 30 for x in lr))
    out['lag_release_q1'], out['lag_release_median'], out['lag_release_q3'] = quart(lr)
    out['lag_advisory_median_after'] = quart([x for x in la if x >= 0])[1]
    for name, lo, hi in WINDOWS[:3] + WINDOWS[5:6]:
        n, at = hazard(rs, lo, hi)
        k = name.split(',')[0].replace(' ', '_').replace('+', '')
        out[f'moves[{name}]'] = n
        out[f'per100[{name}]'] = rate(n, at)
    return out


def main():
    rows = load()
    fields = ['source', 'library', 'cls', 'strict_class', 'package', 'repo', 'held_min', 'outcome', 'move_commit',
              'committer_time', 'author_time', 'moved_to', 'release_time', 'advisory_time', 'first_public_time',
              'end_of_observation', 'lag_release_days', 'lag_release_days_author_time', 'lag_advisory_days',
              'lag_first_public_days', 'authorship', 'bot_name', 'security_word', 'ai_coauthor']
    write_csv('lags.csv', rows, fields)

    order = sorted(CL, key=lambda l: int(CL[l]['rank']))
    E = []
    for lib in order:
        rs = [r for r in rows if r['library'] == lib]
        E.append(summ(lib, rs, cls=CL[lib]['class'], strict_class=CL[lib]['strict_class'],
                      release_to_advisory_days=CL[lib]['release_to_advisory_days'], source='LH008' if EV[lib]['chosen'] == 'yes' else 'LH009'))
    write_csv('summary_by_event.csv', E, list(dict.fromkeys(k for s in E for k in s)))

    S = []
    for key in ('cls', 'strict_class'):
        for c in ('announced', 'silent'):
            rs = [r for r in rows if r[key] == c]
            ev = [e for e in E if e['cls' if key == 'cls' else 'strict_class'] == c]
            s = summ(f'{c} ({"class" if key == "cls" else "strict class, security words only"})', rs,
                     events=len(ev), events_with_kept=sum(e['kept'] > 0 for e in ev),
                     gap_days_median=round(statistics.median(float(e['release_to_advisory_days']) for e in ev), 2))
            pre = [e['per100[release to the advisory (all of it)]'] for e in ev if e['per100[release to the advisory (all of it)]'] != '']
            s['median_of_event_rates_release_to_advisory'] = round(statistics.median(pre), 2) if pre else ''
            s['event_rates_release_to_advisory'] = ' '.join(f"{e['group']}:{e['per100[release to the advisory (all of it)]']}({e['moves[release to the advisory (all of it)]']})" for e in ev if e['kept'])
            loo = []
            for e in ev:
                n, at = hazard([r for r in rs if r['library'] != e['group']], REL, ADV)
                loo.append(f"{e['group']}:{rate(n, at)}({n})")
            s['release_to_advisory_rate_leaving_out_each_event'] = ' '.join(loo)
            S.append(s)
        # without the largest event of each class, as a check on one library carrying a class
    for c in ('announced', 'silent'):
        ev = [e for e in E if e['cls'] == c]
        big = max(ev, key=lambda e: e['kept'])['group']
        rs = [r for r in rows if r['cls'] == c and r['library'] != big]
        S.append(summ(f'{c} (class) without {big}, its largest event', rs))
    write_csv('summary_by_class.csv', S, list(dict.fromkeys(k for s in S for k in s)))

    H = []
    for key in ('cls', 'strict_class'):
        for c in ('announced', 'silent'):
            rs = [r for r in rows if r[key] == c]
            for name, lo, hi in WINDOWS:
                n, at = hazard(rs, lo, hi)
                per_ev = collections.Counter()
                for lib in order:
                    k, _ = hazard([r for r in rs if r['library'] == lib], lo, hi)
                    if k:
                        per_ev[lib] = k
                H.append(dict(grouping='class' if key == 'cls' else 'strict class', cls=c, window=name, pairs=len(rs), moves=n,
                              repo_days_at_risk=round(at, 1), moves_per_100_repo_days=rate(n, at),
                              moves_by_event=' '.join(f'{k} {v}' for k, v in per_ev.items())))
    # Sensitivity: the five silent events whose entries name the fix's change without the flaw
    # (data/flaw_judgements.csv, near_miss) counted as announced; the silent class is then litellm, mcp, langchain.
    NEAR = {'cryptography', 'starlette', 'aiohttp', 'python-multipart', 'soupsieve'}
    for c in ('announced', 'silent'):
        rs = [r for r in rows if (r['cls'] == 'announced' or r['library'] in NEAR) == (c == 'announced')]
        for name, lo, hi in WINDOWS:
            n, at = hazard(rs, lo, hi)
            H.append(dict(grouping='near misses counted as announced', cls=c, window=name, pairs=len(rs), moves=n,
                          repo_days_at_risk=round(at, 1), moves_per_100_repo_days=rate(n, at), moves_by_event=''))
    write_csv('hazard_by_class.csv', H)

    A = []
    for c in ('announced', 'silent'):
        for cls in ('bot', "person merging a bot's branch", 'person'):
            mv = [r for r in rows if r['cls'] == c and r['outcome'] == 'moved' and r['authorship'] == cls]
            A.append(dict(cls=c, authorship=cls, moves=len(mv),
                          within_2d_of_release=sum(0 <= r['lag_release_days'] <= 2 for r in mv),
                          before_advisory=sum(r['lag_advisory_days'] < 0 for r in mv),
                          within_2d_after_advisory=sum(0 <= r['lag_advisory_days'] <= 2 for r in mv),
                          with_security_word=sum(bool(r['security_word']) for r in mv),
                          before_advisory_with_security_word=sum(r['lag_advisory_days'] < 0 and bool(r['security_word']) for r in mv),
                          ai_coauthor=sum(r['ai_coauthor'] == 'yes' for r in mv),
                          bots=' '.join(f'{k} ({v})' for k, v in collections.Counter(r['bot_name'] for r in mv if r['bot_name']).most_common())))
    write_csv('by_authorship.csv', A)
    for x in E:
        print({k: v for k, v in x.items() if not k.startswith('per100') and not k.startswith('moves[')})
    for x in S:
        print(x)
    for h in H:
        print(h)
    for a in A:
        print(a)


if __name__ == '__main__':
    main()
