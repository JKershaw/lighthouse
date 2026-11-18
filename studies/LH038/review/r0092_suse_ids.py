"""R-0092 check: which SUSE-SU announcement ids does SUSE's CVE page (LH036's read of
16 November 2026) list for CVE-2026-98432, in page order, and how do the 15 SUSE pages
LH038 followed sit among them? Announcement-id order is used only as a rough lead on
release order (an assumption, not a date); no date is inferred from an id.
Run: python3 -I studies/LH038/review/r0092_suse_ids.py (from the repository root)."""
import gzip, re, json
page = gzip.open('studies/LH036/data/read-2026-11-16T1419Z/suse.raw.gz').read().decode('utf-8', 'replace')
ids = []
for m in re.finditer(r'(?i)suse-su-(\d{4})[:-]?(\d{4,5})-(\d+)', page):
    k = f"SUSE-SU-{m.group(1)}:{int(m.group(2)):05d}-{m.group(3)}"
    if k not in ids:
        ids.append(k)
print('distinct SUSE-SU ids on the page:', len(ids))
print('first 20 in page order:', ids[:20])
follow = json.load(open('studies/LH038/follow.json'))
followed = sorted(re.sub(r'.*suse-su-(\d{4})(\d{5})-(\d+).*', r'SUSE-SU-\1:\2-\3', u)
                  for k, u in follow.items() if 'suse-su' in u.lower())
print('followed SUSE-SU:', followed)
nums = sorted(int(i.split(':')[1].split('-')[0]) for i in ids)
lo = min(int(f.split(':')[1].split('-')[0]) for f in followed)
below = [n for n in nums if n < lo]
print(f'ids numerically below the lowest followed ({lo}):', len(below))
print('lowest ten ids:', nums[:10])
# Earliest 'published' stamp per announcement on SUSE's CVE page, all sources.
import datetime
rows = re.findall(r'>([A-Z]+-[A-Z0-9:-]+)</a>, published (\w{3} \w{3} +\d+ [\d:]+) (CET|CEST|UTC) (\d{4})', page)
off = {'CET': 1, 'CEST': 2, 'UTC': 0}
parsed = []
for ident, stamp, tz, yr in rows:
    dt = datetime.datetime.strptime(re.sub(' +', ' ', stamp) + ' ' + yr, '%a %b %d %H:%M:%S %Y') - datetime.timedelta(hours=off[tz])
    parsed.append((dt, ident))
parsed.sort()
print('announcements with a published stamp:', len(parsed))
print('earliest five (UTC):', [(d.isoformat(), i) for d, i in parsed[:5]])
for i in ['SUSE-SU-2026:24386-1', 'SUSE-SU-2026:24422-1', 'SUSE-SU-2026:24437-1', 'SUSE-SU-2026:24446-1']:
    print(i, 'CVE-page published (UTC):', [d.isoformat() for d, j in parsed if j == i])
post = datetime.datetime(2026, 10, 27)
print('stamps dated before the post (27 Oct, UTC):', sum(1 for d, _ in parsed if d < post))
