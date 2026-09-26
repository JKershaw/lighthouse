#!/usr/bin/env python3
"""LH002: count one GH Archive hour's events for the cohort and record the file's shape.
Usage: python3 gharchive_hour.py <scratch_dir> <study_dir> <YYYY-MM-DD-H>
Actor logins are read but never written; only counts and payload field names are published."""
import collections, csv, gzip, json, os, sys, time
T0 = time.time()
S, STUDY, HOUR = sys.argv[1:4]
path = os.path.join(S, 'raw', 'gharchive', f'{HOUR}.json.gz')
repos = {l.split()[1].lower(): l.split()[0] for l in open(os.path.join(S, 'repos.txt')) if l.strip()}
total, types, lines = 0, collections.Counter(), 0
cohort = collections.Counter(); push_fields = collections.Counter(); raw = []
norepo = collections.Counter(); ids = set(); dup = 0; minmax = [None, None]
with gzip.open(path, 'rt') as f:
    for line in f:
        lines += 1
        e = json.loads(line)
        total += 1; types[e['type']] += 1
        if e['id'] in ids: dup += 1
        ids.add(e['id'])
        c = e['created_at']; minmax[0] = min(minmax[0] or c, c); minmax[1] = max(minmax[1] or c, c)
        if e['type'] == 'PushEvent':
            for k in e['payload']: push_fields[k] += 1
        name = (e.get('repo') or {}).get('name', '').lower()
        if not name: norepo[e['type']] += 1
        if name in repos:
            cohort[(repos[name], e['type'])] += 1
            p = e['payload']
            raw.append(dict(repo=repos[name], type=e['type'], created_at=c, id=e['id'],
                            payload_keys=sorted(p), head=p.get('head'), before=p.get('before'), ref=p.get('ref'),
                            size=p.get('size'), distinct_size=p.get('distinct_size'),
                            ncommits=len(p.get('commits') or []), action=p.get('action')))
json.dump(raw, open(os.path.join(S, f'gharchive_{HOUR}_cohort_events.json'), 'w'), indent=1)
out = dict(file=os.path.basename(path), bytes=os.path.getsize(path), parse_seconds=round(time.time() - T0, 1), events=total, duplicate_ids=dup, events_without_repo_name=dict(norepo),
           created_min=minmax[0], created_max=minmax[1], types=dict(types.most_common()),
           pushevent_payload_fields=dict(push_fields), cohort=[dict(repo=r, type=t, events=n) for (r, t), n in sorted(cohort.items())])
json.dump(out, open(os.path.join(STUDY, 'data', f'gharchive_{HOUR}_summary.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'types'}, indent=1)); print('top types', types.most_common(8))
for r in raw: print(r)
