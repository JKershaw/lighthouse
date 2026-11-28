"""R-0174: reproduce the case-matrix counts used by articles/armed-robots-who-decides.{md,svg}.
Run: python3 -I notes/R-0174-lh050-reader-evidence/matrix_counts.py studies/LH050/case_matrix.csv"""
import csv, sys
from collections import Counter
rows = list(csv.DictReader(open(sys.argv[1], newline='')))
print('cells', len(rows))
print('all statuses', dict(Counter(r['status'] for r in rows)))
configs = []
for r in rows:
    if r['configuration'] not in configs: configs.append(r['configuration'])
print('configurations', len(configs))
readable = [c for c in configs if not all(r['status']=='unavailable' for r in rows if r['configuration']==c)]
print('readable configurations', len(readable))
CONTROL = {'target selection','force authorisation','intervention'}
for name, pred in [('stage (deployment evidence)', lambda r: r['field']=='deployment evidence'),
                   ('control (target, force, intervention)', lambda r: r['field'] in CONTROL),
                   ('armament', lambda r: r['field']=='armament'),
                   ('AI function', lambda r: r['field']=='AI function'),
                   ('civilian evidence', lambda r: r['field']=='civilian evidence')]:
    sel = [r for r in rows if r['configuration'] in readable and pred(r)]
    print(f'readable rows, {name}: n={len(sel)}', dict(Counter(r['status'] for r in sel)))
print('supported control cells in readable rows:')
for r in rows:
    if r['configuration'] in readable and r['field'] in CONTROL and r['status']=='supported-by-source':
        print('  ', r['configuration'][:50], '|', r['field'], '|', r['facet'])
print('figure grid, by configuration (field[facet]:status):')
for c in configs:
    print(' ', c[:45])
    print('    ', '; '.join(f"{r['field']}{'['+r['facet']+']' if r['facet'] else ''}:{r['status']}" for r in rows if r['configuration']==c))
