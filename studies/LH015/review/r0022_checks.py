# R-0022 checks: the pieces' figures against the retained data, and the build- and recipe-level shares.
import csv, collections, re
D = '/home/user/lighthouse/studies/LH015/data/'
pairs = list(csv.DictReader(open(D + 'pair_classes.csv')))
rc = list(csv.DictReader(open(D + 'recipe_classes.csv')))
frame = {r['pair_id']: r for r in csv.DictReader(open(D + 'frame.csv'))}
order = ['from the pinned file', 'not from the pinned file', 'undetermined', "nothing of the project's requirements", 'no recipe']
print('# figure counts by pin class (from, not from, undetermined, nothing, no recipe)')
for pc in ['all', 'lockfile', 'exact pin', 'both']:
    sel = [p for p in pairs if pc == 'all' or p['pin_class'] == pc]
    c = collections.Counter(p['pair_class'] for p in sel)
    print(pc, len(sel), [c[k] for k in order])
snap = [b for b in rc if b['role'] == 'snapshot']
print('# snapshot builds by class', sorted(collections.Counter(b['class'] for b in snap).items()))
dec = [b for b in snap if b['class'] in '1234']
print('build-level: class 1 among classes 1-4 =', sum(b['class'] == '1' for b in dec), 'of', len(dec))
for pc in ['lockfile', 'exact pin', 'both']:
    s = [b for b in dec if frame[b['pair_id']]['pin_class'] == pc]
    print('  ', pc, sum(b['class'] == '1' for b in s), 'of', len(s))
bp = collections.Counter(b['pair_id'] for b in dec)
print('decided builds per pair, top 6:', [(k, v, frame[k]['repo'].split('/')[-1]) for k, v in bp.most_common(6)])
rec = {}
for b in dec:
    rec.setdefault((b['pair_id'], b['path']), []).append(b['class'])
print('recipes with a decided build:', len(rec), '; every build class 1:', sum(all(c == '1' for c in v) for v in rec.values()))
c3 = set(b['pair_id'] for b in snap if b['class'] == '3')
pyp = set(r['build_id'].split('-')[0] for r in csv.DictReader(open(D + 'pypi.csv')))
print('# pairs with a class 3 snapshot build', len(c3), '; pairs in pypi.csv', len(pyp), '; not in pypi.csv', sorted(c3 - pyp))
for p in c3 - pyp:
    for b in snap:
        if b['pair_id'] == p and b['class'] == '3':
            print('   ', b['build_id'], b['pypi'], b['pypi_spec'], b['reason'][:120])
print('# bbot')
for p in pairs:
    if 'bbot' in p['repo']:
        f = frame[p['pair_id']]
        print(p['pair_id'], p['library'], p['threshold'], p['pin_class'], p['pair_class'], 'classes', p['classes'],
              'release', f['release_time'][:10], 'advisory', f['advisory_time'][:10], f['outcome'], f['lag_release_days'])
lock90 = [p for p in pairs if p['pin_class'] in ('lockfile', 'both') and p['pair_class'] in ('from the pinned file', 'not from the pinned file')]
print('# decided pairs with a timed lock', len(lock90), '; reads_T_lock yes', sum(p['reads_T_lock'] == 'yes' for p in lock90))
nf = [p for p in lock90 if p['pair_class'] == 'not from the pinned file']
subs = collections.Counter()
for p in nf:
    s = set((b['class'], b['sub']) for b in snap if b['pair_id'] == p['pair_id'] and b['class'] in '234')
    subs[tuple(sorted(s))] += 1
print('not-from pairs with a timed lock', len(nf), 'by their class 2-4 builds:')
for k, v in subs.most_common():
    print('   ', v, k)
print('# how class 1 builds take L from T (first T:: effect, file names replaced by F)')
eff = collections.Counter()
for b in snap:
    if b['class'] == '1':
        t = [e.strip() for e in b['effects'].split('||') if e.strip().startswith('T::')]
        key = t[0] if t else 'reason: ' + b['reason']
        key = re.sub(r'\S+\.(txt|lock|toml|py|cfg|in)\b', 'F', key)
        eff[key] += 1
for k, v in eff.most_common(14):
    print(v, k)
print('# the 129 from-the-pinned-file pairs: by pin class, whether any build reads the timed lock')
fr = [p for p in pairs if p['pair_class'] == 'from the pinned file']
print(collections.Counter((p['pin_class'], p['reads_T_lock']) for p in fr).most_common())
print('# undetermined pairs by pin class and reason of their class 6 builds')
und = [p for p in pairs if p['pair_class'] == 'undetermined']
reasons = collections.Counter()
for p in und:
    subs6 = set(b['sub'] for b in snap if b['pair_id'] == p['pair_id'] and b['class'] == '6')
    reasons[(p['pin_class'], tuple(sorted(subs6)))] += 1
for k, v in reasons.most_common(12):
    print('   ', v, k)
