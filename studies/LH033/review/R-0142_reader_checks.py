"""R-0142 stage 2: checks of figures in essays/drafts/seen-from-outside-seen-from-inside-rev.md
against LH033's and LH034's retained reads. Run: python3 -I studies/LH033/review/R-0142_reader_checks.py"""
import json, gzip, os, collections
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
def censys(read):
    return json.loads(gzip.open(f'{R}/LH033/data/{read}/censys.raw.gz').read())['snapshot']

# 1. Totals of PHP services by day (history), from the earliest read holding each day
first = {}
for read in sorted(os.listdir(f'{R}/LH033/data')):
    if not read.startswith('read-') or not os.path.exists(f'{R}/LH033/data/{read}/censys.raw.gz'): continue
    s = censys(read)
    days = collections.defaultdict(dict)
    for h in s['history']: days[h['day']][h['status']] = h['targets']
    for day, st in days.items():
        first.setdefault(day, (read, st))
for day in ['2026-10-21','2026-10-22','2026-10-23','2026-10-28','2026-11-20']:
    read, st = first[day]; tot = sum(st.values()); ver = tot - st.get('unknown', 0)
    print(f"{day} ({read}): all {tot:,}  version-reporting {ver/tot:.1%}  unknown {st.get('unknown',0)/tot:.1%}  "
          f"nofix of versioned {st['affected_nofix']/ver:.1%}  nofix of ALL services {st['affected_nofix']/tot:.1%}")
t1 = sum(first['2026-10-22'][1].values()); t2 = sum(first['2026-10-23'][1].values())
print(f"growth 22->23 Oct: {t2/t1-1:.1%}")

# 2. Largest unsupported branches at the first read (25 October)
s = censys('read-2026-10-25T0855Z')
nofix = sorted([b for b in s['branches'] if b['status']=='affected_nofix'], key=lambda b: -b['targets'])
print('largest no-fix branches, 25 Oct:', [(b['branch'], b['targets']) for b in nofix[:6]])

# 3. Node.js: daily totals, weekend vs weekday, and the unfixed tail days -7..7
t = json.load(open(f'{R}/LH034/data/record_v1.json'))
print('LH034 record keys:', list(t.keys()))

# 1b. Day 7 (28 Oct) from the read the record uses for completed day 7
s = censys('read-2026-10-29T0635Z'); st = {h['status']: h['targets'] for h in s['history'] if h['day']=='2026-10-28'}
tot = sum(st.values()); print(f"day 7 from read-2026-10-29T0635Z: all {tot:,}  version-reporting {1-st['unknown']/tot:.1%}  nofix of ALL {st['affected_nofix']/tot:.1%}")

m = t['measure_2']['daily']
we = {d: v for d, v in m.items() if v['weekday'] in ('Sat','Sun')}
wd = {d: v for d, v in m.items() if v['weekday'] not in ('Sat','Sun') and v['day_n'] != 0}
print(f"Node.js: max weekend total {max(v['total'] for v in we.values()):,}, min weekday total (excl. part day 0) {min(v['total'] for v in wd.values()):,}")
for d in ['2026-10-22','2026-10-23','2026-10-24','2026-10-25','2026-10-26','2026-10-27']:
    print(' ', d, m[d]['weekday'], f"{m[d]['total']:,}")
tail = [(v['day_n'], v['unfixed_pct']) for d, v in sorted(m.items()) if -7 <= v['day_n'] <= 7]
print('unfixed share days -7..7: min', min(x[1] for x in tail), 'max', max(x[1] for x in tail), tail)
print('unfixed share days 8..30: min', min(v['unfixed_pct'] for v in m.values() if 8 <= v['day_n'] <= 30),
      'max', max(v['unfixed_pct'] for v in m.values() if 8 <= v['day_n'] <= 30))
print('weekdays 19 Oct to 30 Oct:', [(d[5:], m[d]['weekday'], round(m[d]['total']/1e6,1)) for d in sorted(m) if '2026-10-19' <= d <= '2026-10-30'])
