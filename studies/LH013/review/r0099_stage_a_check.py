"""R-0099 reader review: recompute Stage A's sums and counts from the retained CSVs (offline)."""
import csv, pathlib
d = pathlib.Path(__file__).resolve().parent.parent / 'data' / 'installer'
rows = list(csv.DictReader(open(d / 'stage_a_A1.csv')))
tot = sum(int(r['rows']) for r in rows)
py39 = sum(int(r['rows']) for r in rows if r['py'] == '3.9')
meta = sum(int(r['metadata_rows']) for r in rows)
names = {r['installer'] for r in rows}
a2 = int(next(csv.DictReader(open(d / 'stage_a_A2.csv')))['total'])
print('groups', len(rows), 'named installers', len(names - {''}), 'blank present', '' in names)
print('total', tot, 'py3.9', py39, 'other', tot - py39, 'metadata rows', meta, 'A2', a2, 'equal', tot == a2)
# rows from installers that resolve from PEP 658 metadata when offered (uv; pip >= 23.2, version not in ClickPy)
uv = sum(int(r['rows']) for r in rows if r['installer'] == 'uv')
pip_other = sum(int(r['rows']) for r in rows if r['installer'] == 'pip' and r['py'] == 'other')
print('uv rows (all Pythons)', uv, 'pip rows on other Pythons', pip_other)
