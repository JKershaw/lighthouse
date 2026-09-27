#!/usr/bin/env python3
"""LH010 step 3e (new): the twelve events that are the same release as LH008's, read from LH008's and LH009's data
as they stand at commit 15bd521 (brief.md, reuse). No network access.

For each reused frame (data/frame_defs.csv, reused LH008 or LH009): the earlier study's frame cut to its first 20
packages in hash order; their screening rows; the kept packages re-tested against LH010's advisory ranges for the
event (data/event_advisory_ranges.csv), from the versions the earlier study recorded at each snapshot
(snapshot_files.csv), since an event's first advisory can now be a different record; one pair per repository per
frame, the first in hash order, as before; the pair's move, times, authorship and trailers from the earlier
study's moves.csv and trailers.csv, and its end of observation from the earlier study's read_log.csv.

Writes data/reused_screen.csv (the first 20 packages of each reused frame, with kept_LH010) and
data/reused_moves.csv (the kept pairs, in collect.py's moves.csv columns where they exist)."""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv, norm
from collect import affected, range_fix, uploaded, V

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
rd = lambda st, n: list(csv.DictReader(open(os.path.join(ROOT, st, 'data', n))))


def clone_times(st):
    out = {}
    for x in rd(st, 'read_log.csv'):
        if x['source'] == 'git over HTTPS' and x['endpoint'] not in out and x['note'] in ('cloned', 'already cloned'):
            out[x['endpoint']] = x['read_utc']
    return out


screen_out, moves_out = [], []
for f in read_csv('frame_defs.csv'):
    if f['reused'] == 'no':
        continue
    st, old = f['reused'], f"{norm(f['library'])}:fix"
    fr = f['frame']
    CT = clone_times(st)
    snap = {}
    for x in rd(st, 'snapshot_files.csv'):
        if x['frame'] == old:
            snap.setdefault(x['package'], []).extend(x['versions'].split(','))
    mv = {m['package']: m for m in rd(st, 'moves.csv') if m['frame'] == old}
    tr = {t['package']: t for t in rd(st, 'trailers.csv') if t['frame'] == old}
    rows = sorted([s for s in rd(st, 'screen.csv') if s['frame'] == old and int(s['hash_rank']) <= 20], key=lambda s: int(s['hash_rank']))
    seen = set()
    for s in rows:
        vs = [v for v in snap.get(s['package'], []) if v]
        aff = [v for v in vs if affected(fr, v)]
        k10 = 'yes' if s['kept'] == 'yes' and aff else 'no'
        screen_out.append(dict(frame=fr, source=st, hash_rank=s['hash_rank'], package=s['package'], repo=s['repo'],
                               reason=s['reason'], pin_class=s.get('pin_class', ''), kept_earlier=s['kept'], kept_LH010=k10,
                               affected_versions=','.join(aff)))
        if k10 != 'yes' or s['repo'] in seen:
            continue
        seen.add(s['repo'])
        m = dict(mv[s['package']])
        pf = range_fix(fr, min(aff, key=V))
        m.update(frame=fr, source=st, pair_fix=pf, pair_release_time=uploaded(f['library'], pf),
                 advisory_time=f['advisory_published'], clone_utc=CT.get('https://' + s['repo'] + '.git', ''),
                 ai_or_bot_coauthors=tr.get(s['package'], {}).get('ai_or_bot_coauthors', ''),
                 ai_coauthor=tr.get(s['package'], {}).get('ai_coauthor', m.get('ai_coauthor', '')))
        moves_out.append(m)
write_csv('reused_screen.csv', screen_out)
write_csv('reused_moves.csv', moves_out, list(dict.fromkeys(k for m in moves_out for k in m)))
for fr in dict.fromkeys(s['frame'] for s in screen_out):
    ss = [s for s in screen_out if s['frame'] == fr]
    print(fr, 'screened', len(ss), 'kept earlier', sum(s['kept_earlier'] == 'yes' for s in ss), 'kept LH010', sum(s['kept_LH010'] == 'yes' for s in ss),
          'pairs', sum(m['frame'] == fr for m in moves_out), 'moved', sum(m['frame'] == fr and m['outcome'] == 'moved' for m in moves_out))
