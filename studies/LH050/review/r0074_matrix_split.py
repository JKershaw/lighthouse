"""R-0074: split LH050's 45-cell totals by row readability and field group."""
import csv, collections, sys
rows = list(csv.DictReader(open(sys.argv[1])))
unread = {r['configuration'] for r in rows if r['status'] == 'unavailable'}
print('rows wholly unavailable:', len(unread), 'cells:', sum(r['configuration'] in unread for r in rows))
read = [r for r in rows if r['configuration'] not in unread]
print('readable rows:', len({r['configuration'] for r in read}), 'cells:', len(read))
groups = {'stage': ['deployment evidence'], 'armament': ['armament'],
          'control': ['target selection', 'force authorisation', 'intervention'],
          'AI function': ['AI function'], 'civilian': ['civilian evidence']}
for g, fs in groups.items():
    c = collections.Counter(r['status'] for r in read if r['field'] in fs)
    print(f'{g:12s}', dict(c))
# control cells in readable rows where no source shows a fielded weapon
armed_fielded = [r for r in read if r['field'] == 'armament' and r['status'] == 'supported-by-source' and r['facet'] != 'design intention']
print('readable rows with a fielded weapon supported by source:', len(armed_fielded))
ts_fa = [r for r in read if r['field'] in ('target selection', 'force authorisation') and r['facet'] != 'stated intention']
print('target-selection / force-authorisation-in-practice cells in readable rows:', len(ts_fa),
      collections.Counter(r['status'] for r in ts_fa))
