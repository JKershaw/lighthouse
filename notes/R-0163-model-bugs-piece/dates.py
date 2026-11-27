"""R-0163 evidence review of articles/drafts/model-found-flaw-dates.md (v0.1, f36d24c).
Re-extracts every date the piece uses from the retained bodies (not from the records'
summaries or timeline.py) and recomputes every day count and date difference it states.
Run from the repository root: python3 -I notes/R-0163-model-bugs-piece/dates.py"""
import gzip, re, json, html, datetime as dt
from email.utils import parsedate_to_datetime

R17 = 'studies/LH038/data/read-2026-11-17T1419Z/'
SC = 'studies/LH038/data/suse-clocks-2026-11-21T1420Z/'
L16 = 'studies/LH036/data/read-2026-11-16T1419Z/'
def b(p): return gzip.open(p).read().decode('utf-8', 'replace')
def utc(d): return d.astimezone(dt.timezone.utc)
D = {}

print('== Stable changelogs: release commit (first) and the fix commit (upstream e3f33b0a1d89)')
rel = {}
for v in ['6.18.56', '7.2.10', '6.12.113', '5.10.272', '5.15.223', '6.1.190', '6.6.159']:
    t = b(R17 + f'changelog_{v}.raw.gz')
    commits = re.split(r'(?m)^commit [0-9a-f]{40}\n', t)[1:]
    first = commits[0]
    assert re.search(r'^\s+Linux ' + re.escape(v) + r'\s*$', first, re.M)
    rd = utc(dt.datetime.strptime(re.search(r'^Date:\s+(.*)$', first, re.M).group(1).strip(), '%a %b %d %H:%M:%S %Y %z'))
    fx = [c for c in commits if 'commit e3f33b0a1d89' in c]
    assert len(fx) == 1
    fd = utc(dt.datetime.strptime(re.search(r'^Date:\s+(.*)$', fx[0], re.M).group(1).strip(), '%a %b %d %H:%M:%S %Y %z'))
    rep = re.findall(r'^\s+Reported-by:.*$', fx[0], re.M)
    has_date_near_rep = any(re.search(r'\d{4}-\d{2}-\d{2}|20\d\d', r) for r in rep)
    rel[v] = rd
    print(f'{v}: release author date {rd:%Y-%m-%d %H:%M} UTC; fix author date {fd:%Y-%m-%d %H:%M:%S} UTC; Reported-by trailers {len(rep)}, any date in them: {has_date_near_rep}')
    D.setdefault('fix', fd)
    assert D['fix'] == fd
by_day = {}
for v, d in rel.items(): by_day.setdefault(d.date(), []).append(v)
for k in sorted(by_day): print(f'  stable releases on {k}: {len(by_day[k])} {sorted(by_day[k])}')

print('\n== CVE record (LH036 retained cve_org, read 16 Nov)')
t = b(L16 + 'cve_org.raw.gz')
res = re.search(r'"dateReserved":"([^"]+)"', t).group(1); pub = re.search(r'"datePublished":"([^"]+)"', t).group(1)
print('dateReserved', res, '| datePublished', pub)
D['reserved'] = dt.date.fromisoformat(res[:10]); D['cvepub'] = dt.date.fromisoformat(pub[:10])

print('\n== Anthropic post (LH038 read 17 Nov)')
t = b(R17 + 'anthropic_post.raw.gz')
dp = re.search(r'"datePublished":"([^"]+)"', t).group(1)
print('datePublished', dp, '| visible "Published Oct 27, 2026":', 'Oct 27, 2026' in t)
txt = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>', '', t, flags=re.S))))
for q in ['allows a remote attacker to send packets to Linux servers with a multipath TCP listener to run arbitrary commands as root, without any credentials or user interaction',
          'it takes 48 minutes to leak a kernel pointer and another five minutes to reach the shell command execution',
          'We reported each vulnerability to the affected vendor under our coordinated vulnerability disclosure',
          '90 days to patch and a further 45 days', 'unreleased, internal research model', 'After initial prompting, Claude wrote an exploit that allows']:
    print(f'  quote present: {q[:60]!r}... -> {q in txt}')
print('  <pre> or <code> in post body:', bool(re.search(r'<(pre|code)\b', t)))
D['post'] = dt.date.fromisoformat(dp[:10])

print('\n== Policies (read 4 Nov)')
a = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', b('studies/LH038/data/policies-2026-11-04T1415Z/anthropic_cvd.raw.gz'))))
for q in ['we would generally wait 45 days before publishing full technical details',
          'if the details are already publicly known through other channels, or if earlier publication would materially help defenders identify and mitigate ongoing attacks']:
    print(f'  Anthropic policy: {q[:50]!r}... -> {q in a}')
print('  "full technical details" defined anywhere on the page (count of phrase):', a.count('full technical details'))
u = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', b('studies/LH038/data/policies-2026-11-04T1415Z/ubuntu_disclosure.raw.gz'))))
print('  Ubuntu: "held private for at least one week after fixes are published" ->', 'held private for at least one week after fixes are published' in u)
k = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', b('studies/LH038/data/policies-2026-11-04T1416Z/kernel_cve_docs.raw.gz'))))
print('  Kernel CVE: automatic only after fix applied to stable ->', 'assignment will only automatically happen after a fix is available and applied to a stable kernel tree' in k,
      '| early identifier on request ->', 'get an identifier assigned from their batch of reserved identifiers' in k)

print('\n== SUSE advisory pages (Release Date, read 17 Nov) and list messages (archive date, read 21 Nov)')
suse = []
for n in [24386, 24422, 24437, 24446, 24479, 24480, 24481, 24482, 24483, 24484, 24485, 24486]:
    p = b(R17 + f'suse_suse_su_2026{n}_1.raw.gz')
    rd = re.search(r'Release Date:</th>\s*<td>([^<]+)</td>', p).group(1).strip()
    m = b(SC + f'msg-{n}.raw.gz')
    ad = dt.datetime.strptime(re.search(r'<I>([^<]*\d{4})</I>', m).group(1).strip(), '%a %b %d %H:%M:%S UTC %Y')
    named = 'CVE-2026-98432' in m
    suse.append((n, dt.date.fromisoformat(rd[:10]), ad))
    print(f'  SUSE-SU-2026:{n}-1 Release Date {rd}; list message {ad:%Y-%m-%d %H:%M:%S} UTC; CVE named in message: {named}')
g24 = [s for s in suse if s[1] == dt.date(2026, 10, 24)]; g02 = [s for s in suse if s[1] == dt.date(2026, 11, 2)]
print(f'  groups: {len(g24)} with Release Date 24 Oct, list days {sorted({s[2].date() for s in g24})}; {len(g02)} with 2 Nov, list days {sorted({s[2].date() for s in g02})}')
D['suse_rel'] = min(s[1] for s in suse); D['suse_list'] = min(s[2] for s in suse).date()

print('\n== SUSE CVE page (LH036 read 16 Nov): announcement stamps before the post')
page = b(L16 + 'suse.raw.gz')
rows = re.findall(r'>([A-Z]+-[A-Z0-9:-]+)</a>, published (\w{3} \w{3} +\d+ [\d:]+) (CET|CEST|UTC) (\d{4})', page)
off = {'CET': 1, 'CEST': 2, 'UTC': 0}
st = [(dt.datetime.strptime(re.sub(' +', ' ', s) + ' ' + y, '%a %b %d %H:%M:%S %Y') - dt.timedelta(hours=off[z]), i) for i, s, z, y in rows]
su = {i for _, i in st if i.startswith('SUSE-SU')}
print(f'  items with a published stamp {len(st)}; distinct SUSE-SU ids {len(su)}; stamped before 27 Oct (UTC): {sum(1 for d,_ in st if d.date() < D["post"])}; earliest {min(st)[0]}')

print('\n== Red Hat errata (Issued, read 17 Nov)')
iss = []
for f in ['93412','93413','93414','93415','93775','94109','94303','94438','94477','94508','94558','94623','94996','95416','98608']:
    t = b(R17 + f'redhat_RHSA-2026_{f}.raw.gz')
    dds = re.findall(r'<dt>[^<]*</dt>\s*<dd>(\d{4}-\d{2}-\d{2})</dd>', t)
    iss.append(dt.date.fromisoformat(dds[0]))
print('  earliest issued', min(iss), '| count on that day', iss.count(min(iss)))
D['rh'] = min(iss)

print('\n== oss-security first message naming the CVE (read 17 Nov)')
t = b(R17 + 'ref_oss_security_10_30_1.raw.gz')
hd = re.search(r'^Date: (.+)$', html.unescape(re.sub(r'<[^>]+>', '', t)), re.M).group(1).strip()
d = utc(parsedate_to_datetime(hd))
print(f'  Date: {hd} = {d:%Y-%m-%d %H:%M} UTC; forwards Go announcement citing the post:',
      'anthropic.com/research/discovering-vulnerabilities-with-claude' in t and 'golang-announce' in t)
D['oss'] = d.date()
for mon in ['09', '10', '11']:
    t = b(R17 + f'oss_security_2026_{mon}.raw.gz')
    subj = re.findall(r'<a href="(\d+/\d+)">([^<]*(?:98432|MPTCP|[Mm]ultipath)[^<]*)</a>', t)
    print(f'  index 2026-{mon}: subjects naming the CVE/MPTCP/multipath: {subj}')

print('\n== Ubuntu notices (LH036 read 16 Nov) and KEV')
ub = json.loads(b(L16 + 'ubuntu.raw.gz'))
up = sorted(n['published'] for n in ub['notices'])
print(f'  notices {len(up)}; earliest {up[0]}; latest {up[-1]}')
D['ubuntu'] = dt.date.fromisoformat(up[0][:10])
kev = json.loads(b(L16 + 'kev.raw.gz'))
print('  KEV catalogVersion', kev['catalogVersion'], '| lists CVE-2026-98432:', any(v['cveID'] == 'CVE-2026-98432' for v in kev['vulnerabilities']))

print('\n== Day counts the piece states (UTC calendar-date differences)')
def dd(a, b_): return (b_ - a).days
post = D['post']; first = min(rel.values()).date(); last = max(rel.values()).date(); fix = D['fix'].date()
checks = [
 ('post - last stable (piece: 12)', dd(last, post), 12),
 ('post - first stable (piece: 16)', dd(first, post), 16),
 ('post - fix author date (piece: 26, upper end of "12 to 26")', dd(fix, post), 26),
 ('post - CVE published (record/investigation: 12)', dd(D['cvepub'], post), 12),
 ('post - SUSE Release Date (piece: "three days before the post")', dd(D['suse_rel'], post), 3),
 ('SUSE list day - post (piece: "two days after")', dd(post, D['suse_list']), 2),
 ('oss-security first message day - post (record: 2 to 3 days)', dd(post, D['oss']), 3),
 ('Red Hat earliest - post', dd(post, D['rh']), 5),
 ('Ubuntu earliest - post', dd(post, D['ubuntu']), 14),
 ('reserved -> fix author date (reserved earlier: positive)', dd(D['reserved'], fix), None),
 ('first stable -> CVE published (published after: positive)', dd(first, D['cvepub']), 4),
]
for lab, got, exp in checks:
    print(f'  {lab}: {got}' + ('' if exp is None else f'  [{"OK" if got == exp else "MISMATCH"}]'))
print('  45-day window ends: ' + '; '.join(f'{n} {s} -> {s + dt.timedelta(45)} (post inside: {post <= s + dt.timedelta(45)})'
      for n, s in [('fix', fix), ('first stable', first), ('last stable', last), ('CVE published', D['cvepub']), ('SUSE Release Date', D['suse_rel'])]))
print('  Ubuntu one-week: first stable +7 =', first + dt.timedelta(7), '| last stable +7 =', last + dt.timedelta(7), '| post after both:', post > last + dt.timedelta(7))
print('  Figure scale: 25 Sep to 10 Nov =', dd(D['reserved'], D['ubuntu']), 'days')
