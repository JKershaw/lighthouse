"""R-0097: offline reproduction of LH013 record version 0.3's Stage A figures from retained files only.
No network read. Run from the repository root: python3 -I studies/LH013/review/r0097_stage_a_reproduce.py"""
import csv, hashlib, os, subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
D = os.path.join(ROOT, 'studies', 'LH013', 'data')
a1 = list(csv.DictReader(open(os.path.join(D, 'installer', 'stage_a_A1.csv'))))
a2 = list(csv.DictReader(open(os.path.join(D, 'installer', 'stage_a_A2.csv'))))
log = [r for r in csv.DictReader(open(os.path.join(D, 'read_log.csv'))) if r['read_utc'].startswith('2026-11-19')]

tot = sum(int(r['rows']) for r in a1)
py39 = sum(int(r['rows']) for r in a1 if r['py'] == '3.9')
oth = sum(int(r['rows']) for r in a1 if r['py'] == 'other')
meta = sum(int(r['metadata_rows']) for r in a1)
names = {r['installer'] for r in a1}
nonblank = sorted(n for n in names if n)
g = {(r['py'], r['installer']): int(r['rows']) for r in a1}
print('A1 rows (groups):', len(a1))
print('A1 total rows:', f'{tot:,}')
print('  Python 3.9:', f'{py39:,}', ' other:', f'{oth:,}', ' 3.9+other == total:', py39 + oth == tot)
print('  metadata rows, all groups:', meta, '; groups with metadata_rows > 0:', sum(int(r['metadata_rows']) > 0 for r in a1))
print('  distinct installer values:', len(names), '; non-blank names:', len(nonblank), '; blank present:', '' in names)
print('  non-blank names:', ', '.join(nonblank))
for k in [('3.9', 'pip'), ('3.9', 'uv'), ('3.9', 'setuptools'), ('3.9', '')]:
    print('  ', k, f'{g.get(k, 0):,}')
print('  3.9 groups sum check (pip+uv+setuptools+blank):', g[('3.9','pip')] + g[('3.9','uv')] + g[('3.9','setuptools')] + g[('3.9','')] == py39)
print('A2:', a2[0], '; A2 total == A1 total:', int(a2[0]['total']) == tot)
print('Brief class rule: present if >= 1% of rows, trace if >=1 below that, absent if 0 ->',
      'present' if meta >= 0.01 * tot else ('trace' if meta > 0 else 'absent'))
print('Read log, 2026-11-19 rows:', len(log))
for r in log:
    print('  ', r['read_utc'], r['label'], 'HTTP', r['http_status'], 'rows_returned', r['rows_returned'], 'read_rows', r['read_rows'], 'output', r['output'])
rr = sum(int(r['read_rows']) for r in log)
print('Queries:', len(log), 'of ceiling 5; rows read:', f'{rr:,}', 'of ceiling 1,000,000,000; within:', len(log) <= 5 and rr <= 1_000_000_000)
print('rows_returned matches CSV rows: A1', int(log[0]['rows_returned']) == len(a1), '; A2', int(log[1]['rows_returned']) == len(a2))
print('all overflow-throw settings in queries:', all("read_overflow_mode = 'throw'" in r['query'] and "result_overflow_mode = 'throw'" in r['query'] for r in log))
cur = hashlib.sha256(open(os.path.join(ROOT, 'studies', 'LH013', 'installer-brief.md'), 'rb').read()).hexdigest()
old = hashlib.sha256(subprocess.run(['git', '-C', ROOT, 'show', '67eac9c:studies/LH013/installer-brief.md'], capture_output=True).stdout).hexdigest()
print('installer-brief.md SHA-256 now:', cur)
print('installer-brief.md SHA-256 at 67eac9c:', old, '; unchanged:', cur == old)
