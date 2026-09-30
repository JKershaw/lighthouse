#!/usr/bin/env python3
"""LH017: two readings made after the counts, prompted by the reader-and-inference review (notes/R-0027.md); each is
post hoc and one reading. Offline; writes data/posthoc_r0027.txt.

1. The container recipes under this study's pair rule. LH015 calls a pair "from the pinned file" only when every build
   that installs the project's requirements is class 1 (its brief, "Pair class"); this study calls a pair "reads the
   pin" when any job is class 1 (brief, choice 4). Here LH015's retained snapshot builds (studies/LH015/data/
   recipe_classes.csv, role snapshot) are put under this study's rules: for the pin, reads when some build is class 1,
   undetermined when none is and some build is class 6, does not when neither and some build is class 2 to 4, nothing
   otherwise; for the timed lock, reads when some class 1 build reads a timed lockfile (re-lock only when every such
   build is flagged "may re-lock"), undetermined when none does and some build is class 6, does not when neither and
   some build is class 1 to 4, outside otherwise. Beside them, this study's CI under LH015's rule (pairs.csv,
   lh015_rule_class) and the cross-tabulations for pairs both readings decide.
2. What setup-uv's cache holds, by the defaults its README gives at the tag a job names (read 09:11 to 09:12 UTC,
   logged in data/read_log.csv): at v4, caching described as something a workflow enables, with no default stated, read
   here as off unless `enable-cache` is set; at v5 to v7, caching by default on
   GitHub-hosted runners; at v4 to v7, the cache pruned of pre-built wheels before it is saved unless `prune-cache` is
   false; at the current v10.1.0, the whole cache kept unless `prune-cache` is true. v1 to v3, v8 and v9, and a
   commit or branch named instead of a version, were not read. For the pairs S2 counted as "every class 1 job restores
   an installer cache as written", each class 1 job's cache is put in one of: keeps downloaded files (setup-python's
   pip or Poetry cache, actions/cache over an installer's cache or a virtual environment, or setup-uv's whole cache),
   pruned, no cache, or defaults not read."""
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA, STUDY  # noqa: E402

csv.field_size_limit(10 ** 9)
L15 = os.path.join(os.path.dirname(STUDY), 'LH015', 'data')
out = []


def say(*a):
    out.append(' '.join(str(x) for x in a))


def pct(n, d):
    return f'{n} of {d} ({100 * n / d:.1f} per cent)' if d else f'{n} of 0'


P17 = {r['pair_id']: r for r in csv.DictReader(open(os.path.join(DATA, 'pairs.csv'))) if r['status'] == 'read'}
P15 = {r['pair_id']: r for r in csv.DictReader(open(os.path.join(L15, 'pair_classes.csv')))}
B = defaultdict(list)
for r in csv.DictReader(open(os.path.join(L15, 'recipe_classes.csv'))):
    if r['role'] == 'snapshot':
        B[r['pair_id']].append(r)
LOCK = ('lockfile', 'both')


def pin_any(bs):
    cs = [b['class'] for b in bs]
    if not cs:
        return 'no recipe'
    if '1' in cs:
        return 'reads'
    if '6' in cs:
        return 'undetermined'
    if any(c in ('2', '3', '4') for c in cs):
        return 'does not'
    return 'nothing'


def lock_any(bs):
    cs = [b['class'] for b in bs]
    if not cs:
        return 'no recipe'
    ones = [b for b in bs if b['class'] == '1' and b['T_lock'] == 'yes']
    if ones:
        return 'reads, re-lock only' if all('may re-lock' in b['flags'] for b in ones) else 'reads'
    if '6' in cs:
        return 'undetermined'
    if any(c in ('1', '2', '3', '4') for c in cs):
        return 'does not'
    return 'outside'


say('== 1. Container recipes (LH015) under this study\'s pair rule, and CI under LH015\'s ==')
rp = Counter(pin_any(B[p]) for p in P15)
say('recipes, pin, some build:', dict(sorted(rp.items())), '| reads', pct(rp['reads'], rp['reads'] + rp['does not']))
r15 = Counter(r['pair_class'] for r in P15.values())
say('recipes, pin, LH015\'s rule (every build):', pct(r15['from the pinned file'],
                                                      r15['from the pinned file'] + r15['not from the pinned file']))
c15 = Counter(r['lh015_rule_class'] for r in P17.values())
say('CI, pin, LH015\'s rule (every job):', pct(c15['reads the pin'], c15['reads the pin'] + c15['does not read the pin']))
c17 = Counter(r['pair_class'] for r in P17.values())
say('CI, pin, this study\'s rule (some job):', pct(c17['reads the pin'], c17['reads the pin'] + c17['does not read the pin']))
lk15 = [p for p in P15 if P15[p]['pin_class'] in LOCK]
rl = Counter(lock_any(B[p]) for p in lk15)
rr = rl['reads'] + rl['reads, re-lock only']
say('recipes, timed lock, some build:', dict(sorted(rl.items())), '| reads', pct(rr, rr + rl['does not']))
dec15 = [p for p in lk15 if P15[p]['pair_class'] in ('from the pinned file', 'not from the pinned file')]
say('recipes, timed lock, LH015\'s frame (as its record gives it):',
    pct(sum(1 for p in dec15 if P15[p]['reads_T_lock'] == 'yes'), len(dec15)))
lk17 = [p for p in P17 if P17[p]['pin_class'] in LOCK]
d17 = [p for p in lk17 if P17[p]['lh015_rule_class'] in ('reads the pin', 'does not read the pin')]
say('CI, timed lock, decided under LH015\'s rule:', pct(sum(1 for p in d17 if P17[p]['lock_class'] == 'reads the timed lock'), len(d17)))
cl = Counter(P17[p]['lock_class'] for p in lk17)
say('CI, timed lock, this study\'s rule:', pct(cl['reads the timed lock'], cl['reads the timed lock'] + cl['does not']))
t = Counter()
for p in lk17:
    a, c = lock_any(B[p]), P17[p]['lock_class']
    if a in ('reads', 'reads, re-lock only', 'does not') and c in ('reads the timed lock', 'does not'):
        t[('reads' if a.startswith('reads') else 'does not', c)] += 1
n = sum(t.values())
say(f'timed lock, pairs both decide under the same rule: {n}; a container build reads it in',
    sum(v for k, v in t.items() if k[0] == 'reads'), '; a CI job in', sum(v for k, v in t.items() if k[1] == 'reads the timed lock'),
    '; where no container build reads it,', t[('does not', 'reads the timed lock')], 'of',
    t[('does not', 'reads the timed lock')] + t[('does not', 'does not')], 'have a CI job that does')
t2 = Counter()
for p in P17:
    a, c = pin_any(B[p]), P17[p]['pair_class']
    if a in ('reads', 'does not') and c in ('reads the pin', 'does not read the pin'):
        t2[(a, c)] += 1
n2 = sum(t2.values())
say(f'pin, pairs both decide under the same rule: {n2}; a container build reads it in',
    sum(v for k, v in t2.items() if k[0] == 'reads'), '; a CI job in', sum(v for k, v in t2.items() if k[1] == 'reads the pin'),
    '; where no container build reads it,', t2[('does not', 'reads the pin')], 'of',
    t2[('does not', 'reads the pin')] + t2[('does not', 'does not read the pin')], 'have a CI job that does')

say('')
say('== 2. What setup-uv\'s cache holds, by its README at the tag a job names ==')
S2 = {r['pair_id']: r for r in csv.DictReader(open(os.path.join(DATA, 's2_log.csv')))}
cached = sorted(p for p, r in S2.items() if r['every class 1 job restores an installer cache as written'] == 'yes')
ones = defaultdict(list)
for r in csv.DictReader(open(os.path.join(DATA, 'job_classes.csv'))):
    if r['final_class'] == '1' and r['pair_id'] in S2:
        ones[r['pair_id']].append(r)
keys = {j['job_key'] for p in cached for j in ones[p]}
uv = defaultdict(list)
for r in csv.DictReader(open(os.path.join(DATA, 'ci_lines.csv'))):
    if r['job_key'] in keys and 'astral-sh/setup-uv@' in r['text']:
        try:
            d = json.loads(r['text'])
        except ValueError:
            continue
        if isinstance(d, dict) and 'astral-sh/setup-uv@' in str(d.get('uses', '')):
            w = d.get('with') or {}
            uv[r['job_key']].append((str(d['uses']).split('@', 1)[1], str(w.get('enable-cache', '')).lower(),
                                     str(w.get('prune-cache', '')).lower()))


def uv_kind(ref, en, pr):
    m = re.match(r'v(\d+)(?:\.|$)', ref)
    mj = int(m.group(1)) if m else None
    if en == 'false':
        return 'no cache'
    if mj is None or mj <= 3 or mj in (8, 9):
        return 'defaults not read'
    if mj == 4 and en != 'true':
        return 'no cache'
    if mj <= 7:
        return 'keeps downloaded files' if pr == 'false' else 'pruned'
    return 'pruned' if pr == 'true' else 'keeps downloaded files'


def job_kinds(j):
    ks = set()
    for part in (x.strip() for x in j['cache'].split('|')):
        if not part:
            continue
        if part.startswith('setup-uv'):
            for ref, en, pr in uv.get(j['job_key']) or [('', '', '')]:
                ks.add(uv_kind(ref, en, pr))
        else:
            ks.add('keeps downloaded files')
    return ks


jk = Counter()
pk = Counter()
for p in cached:
    kinds = set()
    for j in ones[p]:
        k = job_kinds(j)
        jk.update(k)
        kinds |= k
    if kinds & {'no cache', 'pruned'}:
        pk['some class 1 job fetches its pre-built wheels at each run (no cache, or a pruned one)'] += 1
    elif 'defaults not read' in kinds:
        pk['some class 1 job names a setup-uv version whose defaults were not read'] += 1
    else:
        pk['every class 1 job restores a cache that keeps downloaded files'] += 1
say('pairs S2 counted as cached:', len(cached))
say('class 1 jobs in them, by cache (a job with two caches counts under each):', dict(sorted(jk.items())))
for k, v in sorted(pk.items()):
    say(f'  {k}: {v}')
nuv = sum(1 for p in cached if any(j['cache'].startswith('setup-uv') for j in ones[p]))
say('pairs with a setup-uv cache on some class 1 job:', nuv)

path = os.path.join(DATA, 'posthoc_r0027.txt')
open(path, 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
