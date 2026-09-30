#!/usr/bin/env python3
"""R-0027: the figure's comparison of container recipes (LH015) with CI workflows (LH017) under each other's
pair rule. LH015 calls a pair "from the pinned file" only when every build that installs the project's
requirements is class 1; LH017 calls a pair "reads the pin" when any job is class 1. This script recomputes
each study's shares under the other's rule from the retained pair tables, and tabulates LH015's lock reading
against its pair class. Reads only studies/LH015/data/pair_classes.csv and studies/LH017/data/pairs.csv."""
import csv
from collections import Counter

LH015 = list(csv.DictReader(open('../../LH015/data/pair_classes.csv')))
LH017 = list(csv.DictReader(open('../data/pairs.csv')))


def classes(s):
    return [c.strip()[0] for c in s.split() if c.strip()]


def any_rule(cs):
    """LH017's pair rule applied to a list of build classes."""
    if not cs:
        return 'no recipe'
    if '1' in cs:
        return 'from the pinned file'
    if any(c in '234' for c in cs) and '6' not in cs:
        return 'not from the pinned file'
    if '6' in cs:
        return 'undetermined'
    return "nothing of the project's requirements"


def share(n, d):
    return f'{n} of {d} = {100 * n / d:.1f} per cent' if d else f'{n} of 0'


print('== LH015 (container recipes): pair class as recorded, and under LH017\'s "any build" rule ==')
rec = Counter(r['pair_class'] for r in LH015)
print('recorded:', dict(rec))
anyc = Counter(any_rule(classes(r['classes'])) for r in LH015)
print('any-build rule:', dict(anyc))
f, n = rec['from the pinned file'], rec['not from the pinned file']
print('P2 recorded (LH015 rule):', share(f, f + n))
f2, n2 = anyc['from the pinned file'], anyc['not from the pinned file']
print('P2 under the any-build rule:', share(f2, f2 + n2))
mixed = Counter((r['pair_class'], r['mixed']) for r in LH015 if r['pair_class'] == 'not from the pinned file')
print('LH015 "not from the pinned file" by mixed flag:', dict(mixed))
for pc in ('lockfile', 'exact pin', 'both'):
    sub = [r for r in LH015 if r['pin_class'] == pc]
    a = Counter(r['pair_class'] for r in sub)
    b = Counter(any_rule(classes(r['classes'])) for r in sub)
    print(f'  {pc}: recorded', share(a['from the pinned file'], a['from the pinned file'] + a['not from the pinned file']),
          '| any-build', share(b['from the pinned file'], b['from the pinned file'] + b['not from the pinned file']))

print()
print('== LH017 (CI workflows): pair class as recorded, and under LH015\'s rule (pairs.csv, lh015_rule_class) ==')
rec17 = Counter(r['pair_class'] for r in LH017)
print('recorded:', dict(rec17))
l15 = Counter(r['lh015_rule_class'] for r in LH017)
print("LH015's rule:", dict(l15))
print('P2 recorded (any job):', share(rec17['reads the pin'], rec17['reads the pin'] + rec17['does not read the pin']))
print("P2 under LH015's rule:", share(l15['reads the pin'], l15['reads the pin'] + l15['does not read the pin']))

print()
print('== The lock: LH015 lock pairs (pin class lockfile or both), pair class against reads_T_lock ==')
lock15 = [r for r in LH015 if r['pin_class'] in ('lockfile', 'both')]
t = Counter((r['pair_class'], r['reads_T_lock']) for r in lock15)
for k in sorted(t):
    print(f'  {k}: {t[k]}')
dec = [r for r in lock15 if r['pair_class'] in ('from the pinned file', 'not from the pinned file')]
yes = sum(1 for r in dec if r['reads_T_lock'] == 'yes')
print('recorded lock reading (decided under LH015 rule):', share(yes, len(dec)))
# LH017's lock rule applied to recipes: reads when some build reads a T lock; does not when no lock read, no class 6,
# some class 1 to 4; undetermined when no lock read and some class 6; outside otherwise.
c = Counter()
for r in lock15:
    cs = classes(r['classes'])
    if r['reads_T_lock'] == 'yes':
        c['reads'] += 1
    elif not cs or all(x == '5' for x in cs):
        c['outside'] += 1
    elif '6' in cs:
        c['undetermined'] += 1
    else:
        c['does not'] += 1
print("recipes under LH017's lock rule:", dict(c), '|', share(c['reads'], c['reads'] + c['does not']))

print()
print("== The lock: LH017 lock pairs under LH015's rule (decided only when no job is class 2 to 4 or 6 besides class 1/5) ==")
lock17 = [r for r in LH017 if r['pin_class'] in ('lockfile', 'both')]
t2 = Counter((r['lh015_rule_class'], r['lock_class']) for r in lock17)
for k in sorted(t2):
    print(f'  {k}: {t2[k]}')
dec17 = [r for r in lock17 if r['lh015_rule_class'] in ('reads the pin', 'does not read the pin')]
yes17 = sum(1 for r in dec17 if r['lock_class'] == 'reads the timed lock')
print("CI lock reading, decided under LH015's rule:", share(yes17, len(dec17)))
print('CI lock reading as recorded:', share(sum(1 for r in lock17 if r['lock_class'] == 'reads the timed lock'),
                                            sum(1 for r in lock17 if r['lock_class'] in ('reads the timed lock', 'does not'))))

print()
print('== Same pairs, both decided for the lock (LH017 pairs.csv, lh015_reads_T_lock) ==')
both = [r for r in lock17 if r['lock_class'] in ('reads the timed lock', 'does not') and r['lh015_reads_T_lock'] in ('yes', 'no')]
t3 = Counter((r['lh015_reads_T_lock'], r['lock_class']) for r in both)
for k in sorted(t3):
    print(f'  recipe reads lock={k[0]}, CI {k[1]}: {t3[k]}')
print('recipes:', share(sum(v for k, v in t3.items() if k[0] == 'yes'), len(both)),
      '| CI:', share(sum(v for k, v in t3.items() if k[1] == 'reads the timed lock'), len(both)))

print()
print('== Units: pairs against repositories in P2\'s decided frame ==')
d = [r for r in LH017 if r['pair_class'] in ('reads the pin', 'does not read the pin')]
print('decided pairs:', len(d), '| distinct repositories:', len({r['repo'] for r in d}),
      '| repositories with every decided pair reading:', sum(1 for repo in {r['repo'] for r in d}
                                                           if all(x['pair_class'] == 'reads the pin' for x in d if x['repo'] == repo)))
