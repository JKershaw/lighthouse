#!/usr/bin/env python3
"""R-0028: recheck of the figures the resolutions of R-0026 and R-0027 added or changed, recomputed from the retained
tables with code independent of scripts/analyse.py and scripts/posthoc_r0027.py. Offline. Output: r0028_checks.txt."""
import csv
import os
import re
import json
import statistics
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
D = os.path.join(STUDY, 'data')
L15 = os.path.join(os.path.dirname(STUDY), 'LH015', 'data')
csv.field_size_limit(10 ** 9)
out = []


def say(*a):
    out.append(' '.join(str(x) for x in a))


def rd(path):
    return list(csv.DictReader(open(path)))


P = [r for r in rd(os.path.join(D, 'pairs.csv')) if r['status'] == 'read']
J = rd(os.path.join(D, 'job_classes.csv'))
JU = rd(os.path.join(D, 'judgements.csv'))
JB = rd(os.path.join(D, 'judgements_before_check.csv'))
FF = rd(os.path.join(D, 'file_facts.csv'))
RL = rd(os.path.join(D, 'read_log.csv'))
S2 = {r['pair_id']: r for r in rd(os.path.join(D, 's2_log.csv'))}
S3 = {r['pair_id']: r for r in rd(os.path.join(D, 's3_triggers.csv'))}
S5 = rd(os.path.join(D, 's5_docs.csv'))
PY = rd(os.path.join(D, 'pypi.csv'))
P15 = {r['pair_id']: r for r in rd(os.path.join(L15, 'pair_classes.csv'))}
B15 = defaultdict(list)
for r in rd(os.path.join(L15, 'recipe_classes.csv')):
    if r['role'] == 'snapshot':
        B15[r['pair_id']].append(r)
LOCK = ('lockfile', 'both')
byp = defaultdict(list)
for j in J:
    byp[j['pair_id']].append(j)

say('== A. Pair classes (pairs.csv) ==')
say('pairs read:', len(P))
pc = Counter(r['pair_class'] for r in P)
say('pair_class:', dict(pc))
dec = [r for r in P if r['pair_class'] in ('reads the pin', 'does not read the pin')]
say('P2:', pc['reads the pin'], 'of', len(dec), f"({100 * pc['reads the pin'] / len(dec):.1f})")
fr = [r for r in P if r['pair_class'] in ('reads the pin', 'does not read the pin', 'undetermined')]
say('P2 frame (reads, does not, undetermined):', len(fr), '; undetermined share', f"{100 * pc['undetermined'] / len(fr):.1f}")
for k in ('exact pin', 'lockfile', 'both'):
    d = [r for r in dec if r['pin_class'] == k]
    n = sum(1 for r in d if r['pair_class'] == 'reads the pin')
    f = [r for r in fr if r['pin_class'] == k]
    u = sum(1 for r in f if r['pair_class'] == 'undetermined')
    say(f'  {k}: {n} of {len(d)} ({100 * n / len(d):.1f}); undetermined {u} of {len(f)} ({100 * u / len(f):.1f})')
say('does not read the pin, by pin class:', dict(Counter(r['pin_class'] for r in P if r['pair_class'] == 'does not read the pin')))
repos = defaultdict(list)
for r in dec:
    repos[r['repo']].append(r['pair_class'])
say('decided pairs fall in', len(repos), 'repositories;', sum(1 for v in repos.values() if all(c == 'reads the pin' for c in v)),
    'read the pin at every decided pair')
und = [r for r in P if r['pair_class'] == 'undetermined']
say('undetermined pairs:', len(und), 'in', len({r['repo'] for r in und}), 'repositories')
ci = [r for r in P if r['keeps_ci'] == 'yes']
say('pairs with CI:', len(ci), '; no CI:', sum(1 for r in P if r['keeps_ci'] != 'yes'), '; other CI only:', sum(1 for r in P if r['other_ci_only'] == 'yes'))
NOTH = "nothing of the project's requirements"
say('shares of pairs with CI: nothing', f"{100 * pc[NOTH] / len(ci):.1f}", 'undetermined', f"{100 * pc['undetermined'] / len(ci):.1f}")
nothing = [r for r in P if r['pair_class'] == "nothing of the project's requirements"]
say('nothing pairs with a CI container build:', sum(1 for r in nothing if any(j['container_build'] == 'yes' for j in byp[r['pair_id']])))
lk = [r for r in P if r['pin_class'] in LOCK and r['keeps_ci'] == 'yes']
say('lock pairs with CI:', len(lk), dict(Counter(r['lock_class'] for r in lk)))
lr = [r for r in P if r['lock_class'] == 'reads the timed lock']
ln = [r for r in P if r['lock_class'] == 'does not']
say('P3:', len(lr), 'of', len(lr) + len(ln), f'({100 * len(lr) / (len(lr) + len(ln)):.1f})')


def relock_only(pid):
    ones = [j for j in byp[pid] if j['final_class'] == '1' and j['T_lock'] == 'yes']
    return bool(ones) and all('may re-lock' in j['flags'] for j in ones)


ro = [r for r in lr if relock_only(r['pair_id'])]
say('P3 readers whose every lock-reading job may re-lock:', len(ro), '; relock_lock column:', dict(Counter(r['relock_lock'] for r in P if r['pin_class'] in LOCK and r['keeps_ci'] == 'yes')))
rl_dec = Counter(r['relock_lock'] for r in P)
say('P3 strict (relock_lock):', rl_dec.get('reads the timed lock'), 'of', rl_dec.get('reads the timed lock', 0) + rl_dec.get('does not', 0),
    '; of the', len(ro), 're-lock-only readers,', sum(1 for r in ro if r['relock_lock'] == 'undetermined'), 'become undetermined and',
    sum(1 for r in ro if r['relock_lock'] == 'does not'), 'does not')
c15 = Counter(r['lh015_rule_class'] for r in P)
say("P2 under LH015's rule:", c15['reads the pin'], 'of', c15['reads the pin'] + c15['does not read the pin'],
    f"({100 * c15['reads the pin'] / (c15['reads the pin'] + c15['does not read the pin']):.1f})")
c15l = Counter(r['lh015_rule_class'] for r in P if r['pin_class'] in LOCK)
say("  lockfile pairs:", c15l['reads the pin'], 'of', c15l['reads the pin'] + c15l['does not read the pin'])
mx = [r for r in P if r['pair_class'] == 'reads the pin' and r['mixed'] == 'yes']
say('mixed:', len(mx), 'of', pc['reads the pin'], f"({100 * len(mx) / pc['reads the pin']:.1f})")
kinds = Counter()
for r in mx:
    ks = set()
    for j in byp[r['pair_id']]:
        if j['final_class'] == '2':
            ks.add('2 ' + j['final_sub'])
        elif j['final_class'] in ('3', '4'):
            ks.add(j['final_class'])
    kinds.update(ks)
say('  mixed kinds (a pair can count under several):', dict(sorted(kinds.items())))
say('reads the pin only through conditional steps:', sum(1 for r in P if r['pair_class'] == 'reads the pin' and r['conditional_only'] == 'yes'))
rt = Counter(r['routine_class'] for r in P)
say('routine: P2', rt['reads the pin'], 'of', rt['reads the pin'] + rt['does not read the pin'],
    f"({100 * rt['reads the pin'] / (rt['reads the pin'] + rt['does not read the pin']):.1f})")
rtl = Counter(r['routine_lock'] for r in P)
say('routine: P3', rtl['reads the timed lock'], 'of', rtl['reads the timed lock'] + rtl['does not'],
    f"({100 * rtl['reads the timed lock'] / (rtl['reads the timed lock'] + rtl['does not']):.1f})")
rp = [r for r in P if r['pair_class'] == 'reads the pin']
say('S3: readers routine', sum(1 for r in rp if S3[r['pair_id']]['routine'] == 'yes'), 'not routine', sum(1 for r in rp if S3[r['pair_id']]['routine'] != 'yes'),
    'gitlab', sum(1 for r in rp if S3[r['pair_id']]['gitlab'] == 'yes'))
say('S2: pip or uv reads', sum(1 for r in rp if S2[r['pair_id']]['a pip or uv install reads the pin'] == 'yes'),
    '; every class 1 job cached', sum(1 for r in rp if S2[r['pair_id']]['every class 1 job restores an installer cache as written'] == 'yes'),
    '; some class 1 job no cache', sum(1 for r in rp if S2[r['pair_id']]['some class 1 job has no cache setting'] == 'yes'),
    '; other values:', dict(Counter(S2[r['pair_id']]['a pip or uv install reads the pin'] for r in rp)))
say('S5: documented', sum(1 for r in S5 if r['documented'] == 'yes'), '; reads the pin', sum(1 for r in S5 if r['a documented command reads the pin'] == 'yes'),
    '; own package', sum(1 for r in S5 if r['own package from the index documented'] == 'yes'))

say('')
say('== B. Beside LH015 (pairs.csv lh015_* columns and LH015 pair_classes.csv) ==')
for r in P:
    assert r['lh015_class'] == P15[r['pair_id']]['pair_class'], r['pair_id']
    assert r['lh015_reads_T_lock'] == P15[r['pair_id']]['reads_T_lock'], r['pair_id']
t = Counter((r['lh015_reads_T_lock'], r['lock_class']) for r in P if r['pin_class'] in LOCK
            and r['lh015_class'] in ('from the pinned file', 'not from the pinned file') and r['lock_class'] in ('reads the timed lock', 'does not'))
say('2x2 (container reads lock, CI lock):', dict(t))
nf = [r for r in P if r['lh015_class'] == 'not from the pinned file']
say("LH015 not from the pinned file:", len(nf), '; CI decided', sum(1 for r in nf if r['pair_class'] in ('reads the pin', 'does not read the pin')),
    'reads', sum(1 for r in nf if r['pair_class'] == 'reads the pin'))
lu = [r for r in P if r['lh015_lock_unused'] == 'yes']
say('recipe left a timed lock unused:', len(lu), '; CI decided', sum(1 for r in lu if r['pair_class'] in ('reads the pin', 'does not read the pin')),
    'reads', sum(1 for r in lu if r['pair_class'] == 'reads the pin'), '; lock decided', sum(1 for r in lu if r['lock_class'] in ('reads the timed lock', 'does not')),
    'reads', sum(1 for r in lu if r['lock_class'] == 'reads the timed lock'))
nr = [r for r in P if r['lh015_class'] == 'no recipe']
say('no recipe:', len(nr), '; CI decided', sum(1 for r in nr if r['pair_class'] in ('reads the pin', 'does not read the pin')),
    'reads', sum(1 for r in nr if r['pair_class'] == 'reads the pin'), '; neither recipe nor CI', sum(1 for r in nr if r['keeps_ci'] != 'yes'))
either = [r for r in P if r['lh015_class'] == 'from the pinned file' or r['pair_class'] == 'reads the pin']
say('a container build (LH015 class) or a CI job reads the pin:', len(either), 'of', len(P), f'({100 * len(either) / len(P):.1f})')
rec_dec = ('from the pinned file', 'not from the pinned file', "nothing of the project's requirements", 'no recipe')
ci_dec = ('reads the pin', 'does not read the pin', "nothing of the project's requirements", 'no CI')
neither = [r for r in P if r['lh015_class'] in rec_dec and r['pair_class'] in ci_dec and r not in either]
notdec = [r for r in P if r not in either and r not in neither]
say('neither reads, both decided or absent:', len(neither), 'of', len(either) + len(neither), f'({100 * len(neither) / (len(either) + len(neither)):.1f})',
    '; of them no recipe and no CI:', sum(1 for r in neither if r['lh015_class'] == 'no recipe' and r['keeps_ci'] != 'yes'),
    '; remaining pairs (a recipe or CI undetermined, neither reading):', len(notdec), '=', len(P) - len(either) - len(neither))
say('  of the', len(neither), 'neither pairs, the', len(neither) - 59, 'others:', dict(Counter((r['lh015_class'], r['pair_class']) for r in neither
    if not (r['lh015_class'] == 'no recipe' and r['keeps_ci'] != 'yes'))))

say('')
say('== C. Finding 14 recomputed: LH015 builds under this study\'s rule (own code) ==')


def any_pin(bs):
    cs = {b['class'] for b in bs}
    if not bs:
        return 'no recipe'
    if '1' in cs:
        return 'reads'
    if '6' in cs:
        return 'undetermined'
    if cs & {'2', '3', '4'}:
        return 'does not'
    return 'nothing'


def any_lock(bs):
    if not bs:
        return 'no recipe'
    ones = [b for b in bs if b['class'] == '1' and b['T_lock'] == 'yes']
    if ones:
        return 'relock only' if all('may re-lock' in b['flags'] for b in ones) else 'reads'
    cs = {b['class'] for b in bs}
    if '6' in cs:
        return 'undetermined'
    if cs & {'1', '2', '3', '4'}:
        return 'does not'
    return 'outside'


ap = Counter(any_pin(B15[p]) for p in P15)
say('recipes, pin, any build:', dict(ap), '| reads', ap['reads'], 'of', ap['reads'] + ap['does not'], f"({100 * ap['reads'] / (ap['reads'] + ap['does not']):.1f})")
l15c = Counter(P15[p]['pair_class'] for p in P15)
say("recipes, pin, LH015's rule:", l15c['from the pinned file'], 'of', l15c['from the pinned file'] + l15c['not from the pinned file'],
    f"({100 * l15c['from the pinned file'] / (l15c['from the pinned file'] + l15c['not from the pinned file']):.1f})")
lk15 = [p for p in P15 if P15[p]['pin_class'] in LOCK]
al = Counter(any_lock(B15[p]) for p in lk15)
rr = al['reads'] + al['relock only']
say('recipes, lock, any build:', dict(al), '| reads', rr, 'of', rr + al['does not'], f"({100 * rr / (rr + al['does not']):.1f})", '; relock only', al['relock only'])
d15 = [p for p in lk15 if P15[p]['pair_class'] in ('from the pinned file', 'not from the pinned file')]
r15 = sum(1 for p in d15 if P15[p]['reads_T_lock'] == 'yes')
say("recipes, lock, LH015's frame:", r15, 'of', len(d15), f'({100 * r15 / len(d15):.1f})', '; relock only among them',
    sum(1 for p in d15 if P15[p]['reads_T_lock'] == 'yes' and any_lock(B15[p]) == 'relock only'))
say("  check reads_T_lock == any class 1 build with T_lock among all pairs:", all((P15[p]['reads_T_lock'] == 'yes') == any(b['class'] == '1' and b['T_lock'] == 'yes' for b in B15[p]) for p in P15))
P17 = {r['pair_id']: r for r in P}
d17 = [p for p in P17 if P17[p]['pin_class'] in LOCK and P17[p]['lh015_rule_class'] in ('reads the pin', 'does not read the pin')]
say("CI, lock, in the frame LH015's rule decides:", sum(1 for p in d17 if P17[p]['lock_class'] == 'reads the timed lock'), 'of', len(d17))
both = [(any_lock(B15[p]), P17[p]['lock_class']) for p in P17 if P17[p]['pin_class'] in LOCK]
both = [(a if a == 'does not' else 'reads', c) for a, c in both if a in ('reads', 'relock only', 'does not') and c in ('reads the timed lock', 'does not')]
say('lock, both decided under one rule:', len(both), '; container reads', sum(1 for a, c in both if a == 'reads'), '; CI reads',
    sum(1 for a, c in both if c == 'reads the timed lock'), '; container does not:', sum(1 for a, c in both if a == 'does not'),
    'of which CI reads', sum(1 for a, c in both if a == 'does not' and c == 'reads the timed lock'))
bp = [(any_pin(B15[p]), P17[p]['pair_class']) for p in P17]
bp = [(a, c) for a, c in bp if a in ('reads', 'does not') and c in ('reads the pin', 'does not read the pin')]
say('pin, both decided under one rule:', len(bp), '; container reads', sum(1 for a, c in bp if a == 'reads'), '; CI reads',
    sum(1 for a, c in bp if c == 'reads the pin'), '; container does not:', sum(1 for a, c in bp if a == 'does not'),
    'of which CI reads', sum(1 for a, c in bp if a == 'does not' and c == 'reads the pin'))
say('figure bars: recipes pin', ap['reads'], ap['does not'], ap['undetermined'], 'of', ap['reads'] + ap['does not'] + ap['undetermined'],
    '; CI pin', pc['reads the pin'], pc['does not read the pin'], pc['undetermined'], 'of', len(fr))
say('  recipes lock', al['reads'], al['relock only'], al['does not'], al['undetermined'], 'of', al['reads'] + al['relock only'] + al['does not'] + al['undetermined'],
    '; CI lock', len(lr) - len(ro), len(ro), len(ln), sum(1 for r in P if r['lock_class'] == 'undetermined'), 'of',
    len(lr) + len(ln) + sum(1 for r in P if r['lock_class'] == 'undetermined'))

say('')
say('== D. Jobs (job_classes.csv) ==')
say('rows:', len(J))
fc = Counter(j['final_class'] for j in J)
say('final_class:', dict(sorted(fc.items())))
db = Counter(j['decided_by'] for j in J)
say('decided_by:', dict(db))
decided = [j for j in J if j['final_class'] in ('1', '2', '3', '4', '5')]
inst = [j for j in decided if j['final_class'] in ('1', '2', '3', '4')]
say('class 1 among decided:', fc['1'], 'of', len(decided), '; among installing:', fc['1'], 'of', len(inst))
wf = defaultdict(set)
for j in J:
    wf[(j['pair_id'], j['file'])].add(j['final_class'])
wdec = [k for k, v in wf.items() if '6' not in v]
say('workflow files decided:', len(wdec), '; with a class 1 job:', sum(1 for k in wdec if '1' in wf[k]))
tools = Counter()
for j in J:
    if j['final_class'] == '1' and j['decided_by'] == 'script':
        for t in set(j['T_tools'].split()):
            tools[t] += 1
say('S1 tools on script-decided class 1 rows (T_tools, once per row):', dict(tools.most_common()))
relock = [j for j in J if j['final_class'] == '1' and 'may re-lock' in j['flags']]
say('class 1 rows flagged may re-lock:', len(relock), '; tools among them:', dict(Counter(' '.join(sorted(set(j['T_tools'].split()))) for j in relock).most_common()))
mech = Counter()
for r in lr:
    ones = [j for j in byp[r['pair_id']] if j['final_class'] == '1' and j['T_lock'] == 'yes']
    scr = [j for j in ones if j['decided_by'] == 'script']
    if not scr:
        mech['judged'] += 1
    else:
        mech[' and '.join(sorted({t for j in scr for t in j['T_tools'].split()}))] += 1
say('lock-reading installers per P3 reader:', dict(mech.most_common()))
sysc = Counter(j['system'] for j in J)
say('systems:', dict(sysc))
say('rows with an xargs installer in ci lines: (not recomputed)')

say('')
say('== E. Judgements ==')
say('judgements:', len(JU), 'in', len({r['pair_id'] for r in JU}), 'pairs; classes', dict(sorted(Counter(r['class'] for r in JU).items())),
    '; made:', dict(Counter(r['made'] for r in JU)))
say('before check:', len(JB), '; classes', dict(sorted(Counter(r['class'] for r in JB).items())))
rdg = Counter()
for r in JU:
    for x in r['readings'].split():
        rdg[x] += 1
say('readings:', dict(rdg.most_common()))
a1 = [r for r in JU if 'A1' in r['readings'].split() or 'A2' in r['readings'].split()]
say('A1/A2 (manifest takes dependencies from a timed file):', len(a1), 'repos', sorted({r['pair_id'] for r in a1})[:3], '...',
    dict(Counter(re.sub(r'@.*', '', r['job_key']).split('/')[-1] for r in a1)))
anw = [r for r in JU if 'an-website' in r['job_key']]
say('an-website judgements:', len(anw), 'classes', dict(Counter(r['class'] for r in anw)), '; with pip-constraints in reason:',
    sum(1 for r in anw if 'constraint' in r['reason'].lower()), 'class 4 among those', sum(1 for r in anw if 'constraint' in r['reason'].lower() and r['class'] == '4'))
say('grimoirelab judgements:', sum(1 for r in JU if 'grimoirelab' in r['job_key']), '; snowflake-cli:', sum(1 for r in JU if 'snowflake-cli' in r['job_key']),
    '; data-safe-haven:', sum(1 for r in JU if 'data-safe-haven' in r['job_key']))
jj = [j for j in J if j['decided_by'] == 'judged']
say('judged rows in job_classes:', len(jj), 'classes', dict(sorted(Counter(j['final_class'] for j in jj).items())))
say('to-judge total (judged + not judged):', db.get('judged', 0) + db.get('not judged', 0))

say('')
say('== F. Files, reads, PyPI ==')
say('file_facts: files', len(FF), 'at', len({r['pair_id'] for r in FF}), 'pairs; holds_L values', dict(Counter(r['holds_L'] for r in FF)))
src = Counter(r['source'] for r in RL)
say('read_log sources:', dict(src))
meth = Counter((r['source'], r['method']) for r in RL)
say('read_log source/method:', dict(meth))
files = [r for r in RL if r['method'].startswith('git') and 'clone' not in r['method']]
say('git file reads (method starts with git, not clone):', len(files), '; time span', min(r['read_utc'] for r in files), 'to', max(r['read_utc'] for r in files))
say('reads at 08:24:', sum(1 for r in RL if r['read_utc'].startswith('2026-09-30T08:24')), [r['path'] for r in RL if r['read_utc'].startswith('2026-09-30T08:24')])
late = Counter(r['path'] for r in RL if r['read_utc'] > '2026-09-30T08:25' and r['method'].startswith('git') and 'clone' not in r['method'])
say('git file reads after 08:25 by path:', dict(late))
gets = [r for r in RL if r['method'] == 'GET' or r['method'].startswith('HTTP') or 'GET' in r['method']]
say('GET rows:', len(gets), '; pypi.org', sum(1 for r in gets if 'pypi.org' in r['endpoint']), '; other endpoints:',
    [(r['read_utc'][11:19], r['endpoint'], r['status']) for r in gets if 'pypi.org/pypi/' not in r['endpoint'] or 'hatch-pip-compile' in r['endpoint']])
say('clones:', sum(1 for r in RL if 'clone' in r['method']), '; first', min(r['read_utc'] for r in RL), 'last read', max(r['read_utc'] for r in RL))
pyr = Counter(r['reading'] for r in PY if r['pair_id'] not in ('P277', 'P278'))
say('pypi readings without chain-gang:', dict(pyr), 'rows', len(PY))

say('')
say('== G. S6 recomputed from pairs.csv ==')
for k in ('reads the pin', 'does not read the pin', "nothing of the project's requirements", 'undetermined', 'no CI'):
    rows = [r for r in P if r['pair_class'] == k]
    oc = Counter('moved' if r['outcome'] == 'moved' else 'removed' if r['outcome'].startswith('removed') else 'censored' for r in rows)
    lags = sorted(float(r['lag_release_days']) for r in rows if r['outcome'] == 'moved' and r['lag_release_days'])
    q = statistics.quantiles(lags, n=4, method='inclusive') if len(lags) > 1 else lags
    q2 = statistics.quantiles(lags, n=4, method='exclusive') if len(lags) > 1 else lags
    say(f'  {k}: {len(rows)}, {dict(oc)}; lags inclusive {[round(x, 1) for x in q]} exclusive {[round(x, 1) for x in q2]}')
say('outcome values:', dict(Counter(r['outcome'] for r in P)))

say('')
say('== H. Finding 15 recomputed (own code over ci_lines.csv) ==')
cached = sorted(p for p, r in S2.items() if r['every class 1 job restores an installer cache as written'] == 'yes')
keys = {j['job_key'] for p in cached for j in byp[p] if j['final_class'] == '1'}
uvs = defaultdict(list)
for r in csv.DictReader(open(os.path.join(D, 'ci_lines.csv'))):
    if r['job_key'] in keys and 'setup-uv@' in r['text']:
        try:
            d = json.loads(r['text'])
        except ValueError:
            continue
        if isinstance(d, dict) and 'astral-sh/setup-uv@' in str(d.get('uses', '')):
            w = d.get('with') or {}
            uvs[r['job_key']].append((str(d['uses']).split('@', 1)[1], str(w.get('enable-cache', '')).lower(), str(w.get('prune-cache', '')).lower()))


def kind(ref, en, pr):
    m = re.match(r'v(\d+)(\.|$)', ref)
    if en == 'false':
        return 'none'
    if not m or int(m.group(1)) in (1, 2, 3, 8, 9):
        return 'unread'
    v = int(m.group(1))
    if v == 4 and en != 'true':
        return 'none'
    if v <= 7:
        return 'keeps' if pr == 'false' else 'pruned'
    return 'pruned' if pr == 'true' else 'keeps'


pk = Counter()
vers = Counter()
for p in cached:
    ks = set()
    for j in byp[p]:
        if j['final_class'] != '1':
            continue
        for part in filter(None, (x.strip() for x in j['cache'].split('|'))):
            if part.startswith('setup-uv'):
                for ref, en, pr in uvs.get(j['job_key']) or [('', '', '')]:
                    ks.add(kind(ref, en, pr))
                    vers[re.sub(r'\..*', '', ref)] += 1
            else:
                ks.add('keeps')
    pk['some job fetches (none or pruned)' if ks & {'none', 'pruned'} else 'some job unread' if 'unread' in ks else 'all keep'] += 1
say('pairs S2 counted as cached:', len(cached), dict(pk))
say('setup-uv major versions named on those jobs (per job reference):', dict(vers.most_common()))
say('cache column values on class 1 jobs of cached pairs:', dict(Counter(part.split(':')[0] for p in cached for j in byp[p] if j['final_class'] == '1' for part in j['cache'].split('|') if part).most_common()))

open(os.path.join(HERE, 'r0028_checks.txt'), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
