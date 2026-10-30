#!/usr/bin/env python3
"""Reader review R-0044: three small calculations behind its material problems.
Run from the repository root: python3 -I notes/php-leads-2026-10-30/review/r0044_calc.py
Figures are taken from the stripped renderings beside this script (checked against the retained
bytes by strip.py) and from LH031's retained feed of 29 October; nothing is fetched."""
import json, re
from datetime import datetime, timezone
from pathlib import Path

R = Path('notes/php-leads-2026-10-30/review')
delft = R.joinpath('delft.txt').read_text()
unit42 = R.joinpath('unit42.txt').read_text()
dream = R.joinpath('dream.txt').read_text()
advisory = R.joinpath('panw-advisory.txt').read_text()

def num(s):
    return int(s.replace(',', ''))

print('1. Delft dashboard, furthest step, as rendered at 11:47:10 UTC on 30 October')
total = num(re.search(r'([\d,]+) exploitation requests from', delft).group(1))
block = delft[delft.index('Furthest step'):delft.index('Techniques')]
steps = dict((m[0], num(m[1])) for m in re.findall(r'\n (probe|code execution|overload|dropper)\n ([\d,]+)\n', block))
for k, v in steps.items():
    print(f'   {k:15s} {v:7,d}  {v / total:6.1%}')
print(f'   sum of steps {sum(steps.values()):,} against headline {total:,}')

print('\n2. Palo Alto Networks, "approximately .02%" of its installed base "were impacted"')
assert 'approximately .02%' in unit42 and 'were impacted' in unit42
share = 0.0002
for label, n in [('rooted firewalls (Dream, 24)', 24), ('servers exploited (Dream, 25)', 25),
                 ('firewalls targeted (Dream, 240)', 240), ('exposed firewalls found (Dream, about 19,000)', 19000)]:
    print(f'   if .02% were the {label}: implied installed base {n / share:,.0f}')
print('   (the installed base is not in any retained source; the readings differ by a factor of about 800)')
for line in advisory.splitlines():
    if 'previously impacted' in line:
        print('   advisory usage of "impacted":', line.strip())

print('\n3. Clocks: PHP fixed releases against the dates Dream gives')
release = datetime(2026, 10, 21, 14, 0, tzinfo=timezone.utc)
for label, pat in [('first government firewall rooted', r'rooted on Oct 23 at (\d\d):(\d\d) UTC'),
                   ('second government firewall exploited', r'exploited it on Oct 24 at (\d\d):(\d\d) UTC'),
                   ('management server exploited', r'At (\d\d):(\d\d) UTC, less than 90 minutes')]:
    h, m = re.search(pat, dream).groups()
    day = 23 if 'first' in label else 24
    t = datetime(2026, 10, day, int(h), int(m), tzinfo=timezone.utc)
    print(f'   {label}: {t:%d %b %H:%M} UTC, {(t - release).total_seconds() / 3600:.1f} h after PHP\'s 14:00 UTC release of 21 October')
print('   Dream figure 1 caption:', re.search(r'Figure 1: [^.]*', dream).group(0))
print('   advisory, at the 11:51 UTC read:', re.search(r'This issue will be fixed[^.]*\.', advisory).group(0))
print('   Unit 42, at the 11:50 UTC read:', re.search(r'Customers who have applied the available patches[^.]*\.', unit42).group(0))
fixed = re.search(r'fixed PHP releases \(([^)]*)\)', delft).group(1)
print('   PHP fixed releases, as Delft lists them:', fixed)
print('   PHP inside PAN-OS, by Dream:', sorted(set(re.findall(r'\b([78]\.[0-4]\.\d\d)\b', dream))))

feed = json.loads(Path('studies/LH031/data/read-2026-10-29T0634Z/feed.raw').read_bytes())
e = next(v for v in feed['vulnerabilities'] if v['cveID'] == 'CVE-2026-46300')
print(f"   CISA CVE-2026-46300 dateAdded {e['dateAdded']}; Dream's post dated 26 October, updated 29 October")
