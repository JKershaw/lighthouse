"""Independent recount of LH047 week-47 re-audit from requests-judged.csv (R-0124).
Run from repo root: python3 -I notes/R-0124-lh047-reaudit-evidence/recount.py"""
import csv, collections as C, sys
P = 'studies/LH047/data/reaudit-2026-W47/requests-judged.csv'
rows = list(csv.DictReader(open(P, newline='')))
print('rows', len(rows))
print('counted:', C.Counter(r['counted'] for r in rows))
aud = [r for r in rows if r['counted'] == 'audited']
print('audited', len(aud))
print('kind x sent:', C.Counter((r['kind'], r['sent'][:30]) for r in aud))
print('logs (audited):', len({r['log'] for r in aud}), 'hosts:', len({r['host'] for r in aud}), 'practices:', len({r['practice'] for r in aud}))
def tri(col, sub=aud):
    c = C.Counter(sub_r[col] for sub_r in sub)
    return c
for col in ['R1','R2','K8','R4','R5','R5_excl_robots','R6','R7','R8','overall_A','overall_B','overall_K8']:
    print(col, dict(tri(col)))
NC = 'does not comply'
def isnc(v): return v.startswith(NC)
def isunk(v): return v.startswith('unknown')
# Recompute overall A from components, two ways
def overall(r, rob):
    comps = [r[rob], r['R4'], r['R5'], r['R6'], r['R7'], r['R8']]
    if any(isnc(v) for v in comps): return 'nc'
    any_unk = any(isunk(v) for v in comps)
    return 'unk' if any_unk else 'ok', ('unk' if isunk(r[rob]) else 'ok')
cA = C.Counter(); cA_brief = C.Counter(); cB = C.Counter()
for r in aud:
    o = overall(r, 'R1')
    if o == 'nc': cA['nc'] += 1; cA_brief['nc'] += 1
    else: cA[o[0]] += 1; cA_brief[o[1]] += 1
    o = overall(r, 'R2')
    cB['nc' if o == 'nc' else o[0]] += 1
print('recomputed overall A (any rule unknown -> unknown):', dict(cA))
print('recomputed overall A (brief s5 literal: unknown only if R1 unknown):', dict(cA_brief))
print('recomputed overall B (any unknown):', dict(cB))
# Agreement with stored overall
mis = [r['id'] for r in aud if (r['overall_A'].startswith(NC)) != (overall(r,'R1') == 'nc')]
print('overall_A nc mismatches:', mis)
# R5 overall A without robots reads
nA2 = sum(1 for r in aud if any(isnc(r[c]) for c in ['R1','R4','R5_excl_robots','R6','R7','R8']))
print('overall A nc with R5 excl robots:', nA2)
failA = [r for r in aud if isnc(r['overall_A'])]
failB = [r for r in aud if isnc(r['overall_B'])]
print('fail A', len(failA), 'fail B', len(failB))
print('by practice A:')
for p, n in C.Counter(r['practice'] for r in failA).most_common(): print('  ', n, p)
print('by practice B:')
for p, n in C.Counter(r['practice'] for r in failB).most_common(): print('  ', n, p)
print('by practice x rule (A):')
for r in failA:
    pass
pr = C.Counter()
for r in failA:
    rules = [c for c in ['R1','R4','R5','R6','R7','R8'] if isnc(r[c])]
    pr[(r['practice'], '+'.join(rules))] += 1
for k, n in sorted(pr.items()): print('  ', n, k)
def scls(s):
    s = s.strip()
    if s[:1] == '2': return '2xx'
    if s[:1] == '3': return '3xx'
    if s in ('404','403','429'): return s
    if not s: return 'none'
    return s
print('statuses fail A:', C.Counter(scls(r['status']) for r in failA))
print('statuses fail A by practice:')
for k, n in sorted(C.Counter((r['practice'], scls(r['status'])) for r in failA).items()): print('  ', n, k)
print('R5 robots-read-only failures (R5 nc but R5_excl ok):', sum(1 for r in aud if isnc(r['R5']) and not isnc(r['R5_excl_robots'])))
print('R5 nc by practice:', C.Counter(r['practice'] for r in aud if isnc(r['R5'])))
print('R5 nc by host:', C.Counter(r['host'] for r in aud if isnc(r['R5'])))
print('R1 nc rows:'); [print('  ', r['id'], r['practice'], r['url'], r['ua'][:40], r['robots_prov']) for r in aud if isnc(r['R1'])]
print('R2 nc rows:'); [print('  ', r['id'], r['practice'], r['url'], r['R2_agent']) for r in aud if isnc(r['R2'])]
print('R6 nc rows:'); [print('  ', r['id'], r['practice'], r['utc'], r['status'], r['R6_why'][:90]) for r in aud if isnc(r['R6'])]
# W4 evidence split for page requests
pages = [r for r in aud if r['kind'] != 'robots']
print('non-robots audited:', len(pages), C.Counter(r['kind'] for r in pages))
print('robots_prov among non-robots:')
for k, n in C.Counter(r['robots_prov'] for r in pages).most_common(): print('  ', n, k)
# unknowns
uA = [r for r in aud if isunk(r['overall_A'])]
print('unknown A', len(uA), 'R8 unk', sum(isunk(r['R8']) for r in aud), 'R1 unk', sum(isunk(r['R1']) for r in aud), 'R5 unk', sum(isunk(r['R5']) for r in aud))
print('R8 values:', C.Counter(r['R8'] for r in aud))
print('R4 applicable:', C.Counter(r['R4'] for r in aud))
# Overall-unknown rule as the 8 November audit coded it (R1 or R8 unknown), versus the re-audit's (adds R4, R5)
c8 = C.Counter()
for r in aud:
    comps = [r['R1'], r['R4'], r['R5'], r['R6'], r['R7'], r['R8']]
    if any(isnc(v) for v in comps): c8['nc'] += 1
    elif isunk(r['R1']) or isunk(r['R8']): c8['unk'] += 1
    else: c8['ok'] += 1
print('overall A under the 8 November audit.py rule (unknown if R1 or R8 unknown):', dict(c8))
# R5 robots-only failures detail
print('R5 nc only when robots reads counted:')
for r in aud:
    if isnc(r['R5']) and not isnc(r['R5_excl_robots']):
        print('  ', r['id'], r['practice'], r['kind'], r['host'], r['R5_why'][:80])
# --- 8 November audit: R1 count (W5) and the finding-12 status correction
print('\n== 8 November audit ==')
r8 = list(csv.DictReader(open('studies/LH047/data/audit/requests-judged.csv', newline='')))
print('rows', len(r8))
print('R1:', C.Counter(r['R1'] for r in r8))
st = C.Counter(r['status'] for r in r8)
print('status values (non-numeric or blank):', {k: v for k, v in st.items() if not k[:1].isdigit()})
f172 = [r for r in r8 if r['overall_A'].startswith(NC)]
print('172?', len(f172), C.Counter(r['status'] for r in f172))
for r in r8:
    if 'shadowserver' in r.get('host', '') or 'shadowserver' in r.get('url', ''):
        print('  shadowserver:', {k: r[k] for k in r if k in ('who','source','log','url','status','reached','R1','overall_A','note')})
print('8 Nov reached:', C.Counter(r['reached'] for r in r8))
print('8 Nov reached x status for not-yes:', C.Counter((r['reached'], r['status']) for r in r8 if r['reached'] != 'yes'))
print('172 reached:', C.Counter(r['reached'] for r in f172))
print('blank-status rows:', [(r['log'], r['url'][:60], r['reached']) for r in r8 if r['status'] == ''])
print('\n== R8 by User-Agent string (audited) ==')
for (ua, v), n in C.Counter((r['ua'][:70], r['R8']) for r in aud).most_common(): print('  ', n, v, repr(ua))
