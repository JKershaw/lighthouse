# R-0022: the 68 undetermined pairs by repository, with the reasons of their class 6 builds.
import csv, collections
D = '/home/user/lighthouse/studies/LH015/data/'
pairs = list(csv.DictReader(open(D + 'pair_classes.csv')))
snap = [b for b in csv.DictReader(open(D + 'recipe_classes.csv')) if b['role'] == 'snapshot' and b['class'] == '6']
byrepo = collections.defaultdict(list)
for p in pairs:
    if p['pair_class'] == 'undetermined':
        byrepo[p['repo']].append(p)
print('undetermined pairs', sum(len(v) for v in byrepo.values()), 'in', len(byrepo), 'repositories')
for repo, ps in sorted(byrepo.items(), key=lambda kv: -len(kv[1])):
    ids = [p['pair_id'] for p in ps]
    bs = [b for b in snap if b['pair_id'] in ids]
    subs = collections.Counter(b['sub'] for b in bs)
    reason = bs[0]['reason'] if bs else ''
    print(f"{len(ps):2d} {repo.split('/',1)[1][:38]:38s} {ps[0]['pin_class']:9s} {dict(subs)} | {reason[:110]}")
