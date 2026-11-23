"""LH047 re-audit, W47: the authorities that need a current robots.txt re-read (brief section 4 and 10,
Amendment 2): every scheme://host of a sent page request with no robots.txt copy retained from the week
(LH044's and LH045's kept robots.txt bodies) and no robots.txt status other than 200 recorded at the time
by the same log. Writes needs-current.txt. Run from the repository root."""
import csv, os
from urllib.parse import urlsplit
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = list(csv.DictReader(open(os.path.join(D, 'requests.csv'), newline='')))
auth = lambda u: '%s://%s' % (urlsplit(u).scheme, urlsplit(u).netloc)
retained = {auth(r['url']) for r in R if r['kind'] == 'robots' and r['sent'] == 'yes' and r['status'] == '200'
            and r['log'].startswith(('studies/LH044/', 'studies/LH045/'))}
# an LH044 robots.txt redirect chain kept to its end counts as retained for its first authority
lh = sorted([r for r in R if r['log'].startswith('studies/LH044/') and r['kind'] == 'robots' and r['sent'] == 'yes'], key=lambda r: (r['log'], int(r['n'] or 0)))
for a0, b0 in zip(lh, lh[1:]):
    if a0['status'].startswith('3') and b0['status'] and not b0['status'].startswith(('3', '5', 'e')):
        retained.add(auth(a0['url']))
logstate = {(r['log'], auth(r['url'])): r['status'] for r in R if r['kind'] == 'robots' and r['sent'] == 'yes' and r['status'] not in ('', '200')}
need = set()
for r in R:
    if r['kind'] != 'page' or r['sent'] != 'yes' or not r['url']:
        continue
    a = auth(r['url'])
    st = r['robots_logged_status'] or logstate.get((r['log'], a), '')
    if a in retained or (st and st != '200' and not st.startswith('3')):
        continue
    need.add(a)
open(os.path.join(D, 'needs-current.txt'), 'w').write(''.join(a + '/robots.txt\n' for a in sorted(need)))
print(len(need))
