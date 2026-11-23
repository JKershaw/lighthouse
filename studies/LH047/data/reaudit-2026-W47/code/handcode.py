"""LH047 re-audit, W47: requests recorded in prose working notes (not in a structured log), hand-coded
from the notes as committed at the population commit, written to handcoded.csv. Run from the
repository root: python3 -I studies/LH047/data/reaudit-2026-W47/code/handcode.py <population-commit>
Times are as the notes give them ("about 14:19 UTC"), so utc_precision is minute-approx.
"""
import csv, json, os, subprocess, sys
from urllib.parse import urlsplit

P = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'handcoded.csv')
rows = []


def add(**k):
    base = dict(url='', utc='', utc_precision='minute-approx', status='', method='GET', sent='yes', kind_hint='', ua_hint='',
                provider='anthropic', gate_reason='', note='')
    base.update(k)
    n = base['note']
    base['practice'] = ('PHP media sweep (notes)' if 'php-media-sweep' in n else 'LH050 panel locking (gate checks)')
    base['study'] = 'notes' if 'php-media-sweep' in n else 'LH050'
    rows.append(base)


S16 = 'notes/php-media-sweep/2026-11-16T1419Z.md'
for u in ['https://9to5mac.com/2026/10/22/whats-going-on-with-the-web-the-php-issue-and-sites-going-offline/',
          'https://thenewstack.io/ai-php2shell-disclosure-framework', 'https://forklog.com/en/?p=105626']:
    s = urlsplit(u)
    add(url='%s://%s/robots.txt' % (s.scheme, s.netloc), utc='2026-11-16T14:19:00Z', status='200', kind_hint='robots',
        note=S16 + ': gate check, about 14:19 UTC')
    add(url=u, utc='2026-11-16T14:19:00Z', sent='no: refused by the gate', gate_reason='ClaudeBot group, Disallow: /', note=S16)
S19 = 'notes/php-media-sweep/2026-11-19T1417Z.md'
opened = [('https://www.getastra.com/blog/security-advisory/cve-2026-115560/', ''),
          ('https://www.penligent.ai/hackinglabs/?p=8588', ''),
          ('https://windowsforum.com/news/cve-2026-115560-php-rce-disable-session-upload-progress-until-the-next-patch.449755/', ''),
          ('https://saudigazette.com.sa/article/665640/world/critical-security-flaw-shuts-down-websites-worldwide', '402')]
refused = [('https://in.linkedin.com/in/suryaus', 'ClaudeBot group, Disallow: /'),
           ('https://techaeris.com/?p=270144', 'ClaudeBot group, Disallow: /'),
           ('https://carthageelectronics.com/?p=3817', 'ClaudeBot group, Disallow: /'),
           ('https://thenewstack.io/php2shell-ai-vulnerabilities-maintainers/', 'ClaudeBot group, Disallow: /'),
           ('https://www.bizpacreview.com/2026/10/23/heres-how-ai-exposed-long-hidden-web-flaws-hackers-raced-to-exploit-1664620/',
            'anthropic-ai group, Disallow: /')]
for u, x in opened + refused:
    s = urlsplit(u)
    add(url='%s://%s/robots.txt' % (s.scheme, s.netloc), utc='2026-11-19T14:17:00Z',
        status='200' if (u, x) in refused else '', kind_hint='robots', note=S19 + ': gate check, about 14:17 UTC')
for u, st in opened:
    add(url=u, utc='2026-11-19T14:18:00Z', status=st, ua_hint='webfetch', gate_reason='allowed, * group',
        note=S19 + (': fetched with the session fetch tool (WebFetch); the note says "status OK", no code' if not st else ': WebFetch; HTTP 402'))
for u, why in refused:
    add(url=u, utc='2026-11-19T14:17:00Z', sent='no: refused by the gate', gate_reason=why, note=S19)
D = 'studies/LH050/data/2026-11-16T1425Z/robots/'
names = subprocess.run(['git', 'ls-tree', '--name-only', '--full-tree', P, D], capture_output=True, text=True, check=True).stdout.split()
seen = set()
for n in names:
    d = json.loads(subprocess.run(['git', 'show', '%s:%s' % (P, n)], capture_output=True, text=True, check=True).stdout)
    if d['robots_url'] not in seen:
        seen.add(d['robots_url'])
        add(url=d['robots_url'], utc='2026-11-16T14:25:00Z', status=str(d['robots_status']), kind_hint='robots',
            gate_reason='robots sha256 ' + d.get('robots_sha256', ''),
            note=n + ': gate check at panel locking (no time in the file; directory label 14:25Z)')
with open(OUT, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print('hand-coded rows', len(rows))
