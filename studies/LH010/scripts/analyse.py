#!/usr/bin/env python3
"""LH010 step 4: the tables. No network access. Copied from LH009's analyse.py and changed as LH010's brief says:
- pairs come from data/moves.csv (frames read here) and data/reused_moves.csv (LH008's and LH009's frames, first
  20 packages; reuse.py); each frame's class, advisory and gap from data/frame_defs.csv;
- a pair's release time is its own fix's first upload (pair_release_time; the event's fixed release unless the
  pair held an older branch with its own fix), and its end of observation the time its clone was made;
- the main measures use the event frames only; the within-library second frames enter only within_library.csv;
- new: the library as the unit (each library's own rate in two windows, the median by class, a permutation test
  of class labels over libraries), leave-one-library-out ranges, and the class with incidental security words
  dropped (idna 3.15 and aiohttp 3.13.4 counted silent; brief.md amendment 1).

data/lags.csv               one row per pair.
data/summary_by_event.csv   per frame: gap, kept, moved, censored, removed, before the advisory, rates.
data/summary_by_class.csv   pooled by class, strict class and the incidental-words grouping.
data/hazard_by_class.csv    moves per 100 repository-days at risk, by grouping, class and window, with moves by library.
data/library_rates.csv      each library's rate in the two library-unit windows, with its moves and repository-days.
data/library_unit.csv       by grouping and window: libraries, median of library rates per class, observed
                            difference, permutation p (10,000 shuffles, seed 20260927), leave-one-out ranges.
data/by_authorship.csv      by class and authorship class.
data/within_library.csv     the five libraries' two fixes side by side.
"""
import csv, datetime, os, random, statistics, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv, ts, iso

DAY = 86400.0
td = datetime.timedelta
FD = {f['frame']: f for f in read_csv('frame_defs.csv')}
INCIDENTAL = {'idna', 'aiohttp'}  # events whose only security words concern another release (amendment 1)
NPERM, SEED = 10000, 20260927


def clone_times():
    out = {}
    for x in read_csv('read_log.csv'):
        if x['source'] == 'git over HTTPS' and x['note'] in ('cloned', 'already cloned'):
            out.setdefault(x['endpoint'], x['read_utc'])
    return out


CT = clone_times()


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
    for src, ms in (('LH010', read_csv('moves.csv')), ('reused', read_csv('reused_moves.csv'))):
        for m in ms:
            f = FD[m['frame']]
            adv, nvd = f['advisory_published'], f['nvd_published_at']
            first_public = min([ts(adv)] + ([ts(nvd)] if nvd else []))
            rel = m.get('pair_release_time') or f['fixed_uploaded']
            end = m.get('clone_utc') or CT.get('https://' + m['repo'] + '.git', '')
            r = dict(source=m.get('source', src) if src == 'reused' else 'LH010', frame=m['frame'], kind=f['kind'],
                     library=f['library'], rank=int(f['rank']), cls=f['cls'], strict_class=f['strict_class'],
                     incidental_class='silent' if f['library'] in INCIDENTAL and f['kind'] == 'event' else f['cls'],
                     package=m['package'], repo=m['repo'], held_min=m['held_min'], pair_fix=m.get('pair_fix', ''),
                     backport='yes' if m.get('pair_fix', '') and m.get('pair_fix') != f['fixed_release'] else 'no',
                     outcome=m['outcome'].split(':')[0].replace('not moved within the first 400 commits touching pin or lock files (cap)', 'capped'),
                     move_commit=m['move_commit'], committer_time=m['committer_time'], author_time=m['author_time'],
                     moved_to=m['moved_to'], authorship=m['authorship'], bot_name=m['bot_name'],
                     security_word=m['security_word'], ai_coauthor=m.get('ai_coauthor', ''),
                     ai_or_bot_coauthors=m.get('ai_or_bot_coauthors', ''), message_first_line=m.get('message_first_line', ''),
                     release_time=iso(ts(rel)), advisory_time=adv, first_public_time=iso(first_public), end_of_observation=end)
            if m['committer_time']:
                r['lag_release_days'] = round(days(m['committer_time'], r['release_time']), 3)
                r['lag_advisory_days'] = round(days(m['committer_time'], adv), 3)
                r['lag_first_public_days'] = round(days(m['committer_time'], r['first_public_time']), 3)
            else:
                r['lag_release_days'] = r['lag_advisory_days'] = r['lag_first_public_days'] = ''
            rows.append(r)
    return rows


def hazard(rs, lo_of, hi_of):
    at, n = 0.0, 0
    for r in rs:
        end = ts(r['end_of_observation']) if r['end_of_observation'] else ts('2026-09-27T12:00:00Z')
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
W = {w[0]: w for w in WINDOWS}
UNIT_WINDOWS = ['release to the advisory (all of it)', 'release +2 to +7 days, stopping at the advisory']
GROUPINGS = [('class', 'cls'), ('strict class', 'strict_class'), ('incidental security words dropped', 'incidental_class')]


def rate(n, at):
    return round(100 * n / at, 2) if at else ''


def summ(label, rs, **extra):
    mv = [r for r in rs if r['outcome'] == 'moved']
    lr = [r['lag_release_days'] for r in mv]
    la = [r['lag_advisory_days'] for r in mv]
    before = sum(x < 0 for x in la)
    out = dict(group=label, **extra, kept=len(rs), moved=len(mv),
               censored=sum(r['outcome'].startswith('censored') or r['outcome'] == 'capped' for r in rs),
               removed=sum(r['outcome'] == 'removed' for r in rs), backport_pairs=sum(r['backport'] == 'yes' for r in rs),
               moved_before_advisory=before,
               share_of_moves_before_advisory=f'{before}/{len(mv)}' + (f' ({round(100 * before / len(mv))}%)' if mv else ''),
               share_of_kept_moving_before_advisory=f'{before}/{len(rs)}' + (f' ({round(100 * before / len(rs))}%)' if rs else ''),
               moved_before_first_public=sum(r['lag_first_public_days'] < 0 for r in mv),
               moved_within_2d_of_release=sum(0 <= x <= 2 for x in lr),
               moved_within_2d_after_advisory=sum(0 <= x <= 2 for x in la),
               moved_within_30d_of_release=sum(0 <= x <= 30 for x in lr))
    out['lag_release_q1'], out['lag_release_median'], out['lag_release_q3'] = quart(lr)
    out['lag_advisory_median_after'] = quart([x for x in la if x >= 0])[1]
    for name in ('release +0 to +2 days, or to the advisory where it came first', 'release to the advisory (all of it)',
                 'release +2 to +7 days, stopping at the advisory', 'advisory +0 to +2 days'):
        n, at = hazard(rs, W[name][1], W[name][2])
        out[f'moves[{name}]'] = n
        out[f'repo_days[{name}]'] = round(at, 1)
        out[f'per100[{name}]'] = rate(n, at)
    return out


def lib_rates(rs, name):
    """{library: (rate, moves, repo-days)} for libraries with repository-days at risk in the window."""
    out = {}
    for lib in dict.fromkeys(r['library'] for r in rs):
        n, at = hazard([r for r in rs if r['library'] == lib], W[name][1], W[name][2])
        if at > 0:
            out[lib] = (100 * n / at, n, at)
    return out


def perm_test(a, s, rng):
    obs = statistics.median(a) - statistics.median(s)
    pool, k, hits = a + s, len(a), 0
    for _ in range(NPERM):
        rng.shuffle(pool)
        if abs(statistics.median(pool[:k]) - statistics.median(pool[k:])) >= abs(obs) - 1e-12:
            hits += 1
    return obs, (1 + hits) / (NPERM + 1)


def main():
    rows = load()
    fields = ['source', 'frame', 'kind', 'library', 'rank', 'cls', 'strict_class', 'incidental_class', 'package', 'repo', 'held_min',
              'pair_fix', 'backport', 'outcome', 'move_commit', 'committer_time', 'author_time', 'moved_to', 'release_time',
              'advisory_time', 'first_public_time', 'end_of_observation', 'lag_release_days', 'lag_advisory_days',
              'lag_first_public_days', 'authorship', 'bot_name', 'security_word', 'ai_coauthor', 'ai_or_bot_coauthors']
    write_csv('lags.csv', rows, fields)
    ev_rows = [r for r in rows if r['kind'] == 'event']

    E = []
    for fr, f in FD.items():
        rs = [r for r in rows if r['frame'] == fr]
        E.append(summ(fr, rs, library=f['library'], rank=f['rank'], kind=f['kind'], fixed_release=f['fixed_release'],
                      cls=f['cls'], strict_class=f['strict_class'], release_to_advisory_days=f['release_to_advisory_days'],
                      reused=f['reused']))
    write_csv('summary_by_event.csv', E, list(dict.fromkeys(k for s in E for k in s)))

    S = []
    for gname, key in GROUPINGS:
        for c in ('announced', 'silent'):
            evs = [f for f in FD.values() if f['kind'] == 'event' and
                   (('silent' if f['library'] in INCIDENTAL else f['cls']) if key == 'incidental_class' else f[key if key != 'cls' else 'cls']) == c]
            rs = [r for r in ev_rows if r[key] == c]
            s = summ(f'{c} ({gname})', rs, events=len(evs), libraries_with_kept=len({r['library'] for r in rs}),
                     gap_days_median=round(statistics.median(float(f['release_to_advisory_days']) for f in evs), 2))
            S.append(s)
    write_csv('summary_by_class.csv', S, list(dict.fromkeys(k for s in S for k in s)))

    H = []
    for gname, key in GROUPINGS:
        for c in ('announced', 'silent'):
            rs = [r for r in ev_rows if r[key] == c]
            for name, lo, hi in WINDOWS:
                n, at = hazard(rs, lo, hi)
                per = collections.Counter()
                for lib in dict.fromkeys(r['library'] for r in rs):
                    k, _ = hazard([r for r in rs if r['library'] == lib], lo, hi)
                    if k:
                        per[lib] = k
                H.append(dict(grouping=gname, cls=c, window=name, pairs=len(rs), libraries=len({r['library'] for r in rs}),
                              moves=n, repo_days_at_risk=round(at, 1), moves_per_100_repo_days=rate(n, at),
                              moves_by_library=' '.join(f'{k} {v}' for k, v in per.items())))
    write_csv('hazard_by_class.csv', H)

    LR, LU = [], []
    for name in UNIT_WINDOWS:
        lr = lib_rates(ev_rows, name)
        for lib, (x, n, at) in lr.items():
            f = FD[[fr for fr in FD if FD[fr]['library'] == lib and FD[fr]['kind'] == 'event'][0]]
            LR.append(dict(window=name, library=lib, rank=f['rank'], cls=f['cls'], strict_class=f['strict_class'],
                           pairs=sum(r['library'] == lib for r in ev_rows), moves=n, repo_days_at_risk=round(at, 1),
                           per100=round(x, 2)))
    write_csv('library_rates.csv', LR)
    for gname, key in GROUPINGS:
        for name in UNIT_WINDOWS:
            lr = lib_rates(ev_rows, name)
            lab = {r['library']: r[key] for r in ev_rows}
            A = [lr[l][0] for l in lr if lab[l] == 'announced']
            Sx = [lr[l][0] for l in lr if lab[l] == 'silent']
            row = dict(grouping=gname, window=name, announced_libraries=len(A), silent_libraries=len(Sx))
            if len(A) >= 1 and len(Sx) >= 1:
                row['announced_median'] = round(statistics.median(A), 2)
                row['silent_median'] = round(statistics.median(Sx), 2)
                row['announced_mean'] = round(statistics.mean(A), 2)
                row['silent_mean'] = round(statistics.mean(Sx), 2)
                row['announced_libraries_with_no_move'] = sum(x == 0 for x in A)
                row['silent_libraries_with_no_move'] = sum(x == 0 for x in Sx)
            if len(A) >= 5 and len(Sx) >= 5:
                obs, p = perm_test(list(A), list(Sx), random.Random(SEED))
                row.update(observed_difference_of_medians=round(obs, 2), permutation_p_two_sided=round(p, 4),
                           permutations=NPERM, seed=SEED)
            # leave one library out: pooled rate and library median, per class
            for c, xs in (('announced', A), ('silent', Sx)):
                libs = [l for l in lr if lab[l] == c]
                pooled, meds = [], []
                for l in libs:
                    n, at = hazard([r for r in ev_rows if r[key] == c and r['library'] != l], W[name][1], W[name][2])
                    pooled.append(100 * n / at if at else float('nan'))
                    rest = [lr[m][0] for m in libs if m != l]
                    if rest:
                        meds.append(statistics.median(rest))
                n, at = hazard([r for r in ev_rows if r[key] == c], W[name][1], W[name][2])
                row[f'{c}_pooled'] = rate(n, at)
                row[f'{c}_pooled_moves'] = n
                if pooled:
                    row[f'{c}_pooled_leave_one_out'] = f'{min(pooled):.2f} to {max(pooled):.2f}'
                if meds:
                    row[f'{c}_median_leave_one_out'] = f'{min(meds):.2f} to {max(meds):.2f}'
            LU.append(row)
    write_csv('library_unit.csv', LU, list(dict.fromkeys(k for s in LU for k in s)))

    A = []
    for c in ('announced', 'silent'):
        for cls in ('bot', "person merging a bot's branch", 'person'):
            mv = [r for r in ev_rows if r['cls'] == c and r['outcome'] == 'moved' and r['authorship'] == cls]
            A.append(dict(cls=c, authorship=cls, moves=len(mv),
                          within_2d_of_release=sum(0 <= r['lag_release_days'] <= 2 for r in mv),
                          release_2_to_7d_before_advisory=sum(2 <= r['lag_release_days'] < 7 and r['lag_advisory_days'] < 0 for r in mv),
                          before_advisory=sum(r['lag_advisory_days'] < 0 for r in mv),
                          within_2d_after_advisory=sum(0 <= r['lag_advisory_days'] <= 2 for r in mv),
                          with_security_word=sum(bool(r['security_word']) for r in mv),
                          before_advisory_with_security_word=sum(r['lag_advisory_days'] < 0 and bool(r['security_word']) for r in mv),
                          ai_coauthor=sum(r['ai_coauthor'] == 'yes' for r in mv),
                          bots=' '.join(f'{k} ({v})' for k, v in collections.Counter(r['bot_name'] for r in mv if r['bot_name']).most_common())))
    write_csv('by_authorship.csv', A)

    WL = []
    for fr, f in FD.items():
        if f['kind'] != 'within-library second fix':
            continue
        for g in (FD[[x for x in FD if FD[x]['library'] == f['library'] and FD[x]['kind'] == 'event'][0]], f):
            rs = [r for r in rows if r['frame'] == g['frame']]
            row = dict(library=f['library'], frame=g['frame'], fixed_release=g['fixed_release'], cls=g['cls'],
                       strict_class=g['strict_class'], release_to_advisory_days=g['release_to_advisory_days'], kept=len(rs),
                       moved=sum(r['outcome'] == 'moved' for r in rs))
            for name in UNIT_WINDOWS:
                n, at = hazard(rs, W[name][1], W[name][2])
                row[f'moves[{name}]'], row[f'repo_days[{name}]'], row[f'per100[{name}]'] = n, round(at, 1), rate(n, at)
            WL.append(row)
    for c in ('announced', 'silent'):
        libs = {w['library'] for w in WL if w['kept']}
        rs = [r for r in rows if r['library'] in libs and FD[r['frame']]['cls'] == c and
              (r['kind'] == 'within-library second fix' or any(FD[x]['library'] == r['library'] for x in FD if FD[x]['kind'] != 'event'))]
        row = dict(library='sum over the libraries with kept pairs in either frame', frame='', fixed_release='', cls=c, kept=len(rs),
                   moved=sum(r['outcome'] == 'moved' for r in rs))
        for name in UNIT_WINDOWS:
            n, at = hazard(rs, W[name][1], W[name][2])
            row[f'moves[{name}]'], row[f'repo_days[{name}]'], row[f'per100[{name}]'] = n, round(at, 1), rate(n, at)
        WL.append(row)
    write_csv('within_library.csv', WL, list(dict.fromkeys(k for s in WL for k in s)))

    short = lambda d: {k: v for k, v in d.items() if not k.startswith('repo_days') and not k.startswith('moves[')}
    for s in S:
        print(short(s))
    for h in H:
        if h['grouping'] == 'class':
            print(h['cls'], h['window'][:40], h['moves'], h['repo_days_at_risk'], h['moves_per_100_repo_days'])
    for u in LU:
        print(u)
    for w in WL:
        print(short(w))
    for a in A:
        print(a)


if __name__ == '__main__':
    main()
