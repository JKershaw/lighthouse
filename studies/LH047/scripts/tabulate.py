"""LH047 part C tables from data/audit/requests-judged.csv. Offline.
Run from the repository root: python3 -I studies/LH047/scripts/tabulate.py
Writes data/audit/tables.md and data/audit/summary.json."""
import csv, json, os
from collections import Counter, defaultdict

D = os.path.join(os.getcwd(), 'studies/LH047/data/audit')
R = list(csv.DictReader(open(os.path.join(D, 'requests-judged.csv'), newline='')))
out = []
summ = {}


def table(title, header, rows):
    out.append('\n### ' + title + '\n')
    out.append('| ' + ' | '.join(header) + ' |')
    out.append('|' + '---|' * len(header))
    for r in rows:
        out.append('| ' + ' | '.join(str(x) for x in r) + ' |')


def group(r):
    w = r['who']
    if r['source'] == 'transcript':
        return 'ad hoc: ' + w
    return w


summ['requests'] = len(R)
summ['by_source'] = Counter(r['source'] for r in R)
summ['reached'] = Counter(r['reached'] for r in R)
for k in ('overall_A', 'overall_B', 'overall_B_agent', 'R1', 'R2', 'R2_agent', 'R4', 'R5', 'R5_excl_robots', 'R6', 'R7', 'R8'):
    summ[k] = Counter(r[k].split(' (')[0] if r[k].startswith('does not comply') else r[k] for r in R)
summ['robots_prov'] = Counter(r['robots_prov'] for r in R)
summ['use'] = Counter(r['use'] for r in R)

g = defaultdict(list)
for r in R:
    g[group(r)].append(r)
rows = []
for k in sorted(g, key=lambda k: -len(g[k])):
    rs = g[k]
    c = lambda col, v: sum(1 for x in rs if x[col] == v)
    rows.append([k, len(rs), c('overall_A', 'complies'), c('overall_A', 'does not comply'), c('overall_A', 'unknown'),
                 c('overall_B_agent', 'does not comply'), c('overall_B', 'does not comply')])
table('Requests by who made them, and overall verdicts', ['who', 'requests', 'A complies', 'A does not comply', 'A unknown',
      'B (agent tokens) does not comply', 'B (all seven tokens) does not comply'], rows)

rows = []
for rule, col, why in (('R1 robots.txt, own token or *', 'R1', 'R1_rule'), ('R2 robots.txt, Anthropic tokens', 'R2', 'R2_tokens'),
                       ('R4 usage preference', 'R4', 'R4_why'), ('R5 Crawl-delay', 'R5', 'R5_why'), ('R6 walls', 'R6', 'R6_why'),
                       ('R7 terms', 'R7', 'R7_why'), ('R8 identification', 'R8', 'ua')):
    bad = [x for x in R if x[col].startswith('does not comply')]
    cc = Counter((group(x), x['host'], (x[why] or '')[:90]) for x in bad)
    for (w, h, y), n in sorted(cc.items(), key=lambda kv: (-kv[1], kv[0])):
        prov = Counter(x['robots_prov'] for x in bad if group(x) == w and x['host'] == h).most_common(1)[0][0]
        rows.append([rule, w, h, n, y.replace('|', '/'), prov if col in ('R1', 'R2') else ''])
table('Every request that does not comply, by rule (a request can appear under more than one rule)',
      ['rule', 'who', 'host', 'requests', 'why', 'robots.txt copy used'], rows)

rows = []
for x in R:
    if x['R2'] == 'does not comply' and x['R1'] != 'does not comply':
        rows.append([group(x), x['host'], x['url'][:70], x['R2_tokens'], x['R2_agent']])
table('Requests that comply under reading A but not under reading B, with the tokens whose groups disallow them',
      ['who', 'host', 'url', 'tokens disallowing', 'B with agent tokens only'], rows)

rows = []
for x in R:
    if x['R1'] == 'unknown':
        rows.append([group(x), x['url'][:70], x['reached'], x['R1_rule'][:100]])
table('Requests whose robots.txt verdict is unknown', ['who', 'url', 'reached the site', 'why'], rows)

lg = defaultdict(Counter)
for x in R:
    lg[(x['log'] if x['source'] == 'log' else 'ad hoc commands in transcripts', x['robots_first'])][x['R1']] += 1
rows = [[k[0], k[1], sum(v.values()), v['does not comply'], v['unknown']] for k, v in sorted(lg.items())]
table('Practice: did the collector read robots.txt before the host\'s first request?', ['log', 'robots.txt read first', 'requests', 'R1 does not comply', 'R1 unknown'], rows)

rows = []
seen = set()
for x in R:
    k = (group(x), x['host'])
    if k in seen:
        continue
    seen.add(k)
    cd = next((y['crawl_delay'] for y in R if group(y) == k[0] and y['host'] == k[1] and y['crawl_delay']), '')
    if int(x['host_n']) >= 20 or x['R5'] != 'complies' or cd:
        rows.append([k[0], k[1], x['host_n'], x['host_max60'], x['host_min_gap'], cd, x['R5'], x['R5_excl_robots']])
rows.sort(key=lambda r: -int(r[2]))
table('Rate: every who-and-host pair with 20 or more requests or a Crawl-delay', ['who', 'host', 'requests', 'most in any 60 s',
      'shortest gap (s)', 'Crawl-delay', 'R5', 'R5 without robots.txt reads'], rows)

rows = [[group(x), x['host'], x['status'], x['wall'], x['utc'][11:19]] for x in R if x['wall']]
table('Walls and refusals met (R6 inputs)', ['who', 'host', 'status', 'kind', 'UTC'], rows)
rows = [[group(x), x['url'][:70], x['R6_why'][:120]] for x in R if x['R6_why']]
table('Later requests to the same URL after a wall or refusal', ['who', 'url', 'note'], rows)

rows = [[group(x), x['url'][:70], x['signal'], x['use'], x['kept'], x['status'], x['R4'], x['R4_why']] for x in R if x['R4'] != 'not applicable']
table('Usage preferences (Content-Signal, Content-Usage) and what was done with the body', ['who', 'url', 'signal', 'use', 'kept', 'status', 'R4', 'why'], rows)

ua = Counter((group(x), x['ua'], x['R8'].split(' (')[0]) for x in R)
table('Identification', ['who', 'User-Agent class', 'R8', 'requests'], [[a, b, c, n] for (a, b, c), n in sorted(ua.items())])

open(os.path.join(D, 'tables.md'), 'w').write('# LH047 part C tables\n\nGenerated by scripts/tabulate.py from requests-judged.csv. Do not edit by hand.\n' + '\n'.join(out) + '\n')
json.dump(summ, open(os.path.join(D, 'summary.json'), 'w'), indent=1, default=dict)
print(json.dumps(summ, indent=1, default=dict))
