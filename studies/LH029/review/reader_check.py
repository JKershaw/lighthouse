#!/usr/bin/env python3
"""R-0033 reader reviewer's check, kept with its output (reader_check.txt).

Reads only retained bytes already cited by LH029 and LH028: PHP's archive page as retained
by LH029 (23 Oct 17:00 UTC), by R-0032's live read (23 Oct 17:11 UTC) and by LH024 (22 Oct
06:24 UTC), and Cloudflare's page as retained by LH028 at six slots. It verifies the hashes
the record states, counts the strings a reader's belief rests on, and prints the clock
intervals the pieces cite. No network access.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import re

REPO = Path(__file__).resolve().parents[3]
NEW = REPO / 'studies/LH029/data/snapshot-2026-10-23/archive.raw'
LIVE = REPO / 'studies/LH029/review/live-archive-2026-10-23.raw'
OLD = REPO / 'studies/LH024/data/snapshot-2026-10-22/php_0.raw'
LH028 = REPO / 'studies/LH028/data'
out = []
P = out.append

stated = {
    NEW: '941317fe0df9a5e2c642f3b817724c9682ad1e751707b5db8a65d86c21ae11dc',
    LIVE: '941317fe0df9a5e2c642f3b817724c9682ad1e751707b5db8a65d86c21ae11dc',
    OLD: '3b02b9e9f8ebedb87cbe39a2852c8cc3205067f59572000c730844fbc4a03555',
}
P('== hashes against the record ==')
for path, want in stated.items():
    b = path.read_bytes()
    P(f'{path.relative_to(REPO)}: {len(b)} bytes, sha256 matches record: {sha256(b).hexdigest() == want}')

P('\n== strings a reader\'s belief rests on, by copy (count of occurrences) ==')
needles = [b'2026-10-23-1', b'CVE-2026-115560', b'serialize_handler', b'upload_progress.enabled=0',
           b'until the next regular bugfix release', b'to fully protect', b'unlikely RCE vector',
           b'unlikely in practice', b'regular release cycle', b'restart every worker',
           b'8.5.12', b'8.4.27', b'8.3.36', b'8.2.35']
for label, path in (('22 Oct 06:24 (LH024)', OLD), ('23 Oct 17:00 (LH029)', NEW), ('23 Oct 17:11 (R-0032)', LIVE)):
    raw = path.read_bytes()
    P(f'[{label}] ' + ', '.join(f'{n.decode()}={raw.count(n)}' for n in needles))

P('\n== does any sentence of the 23 Oct entry name a PHP version? ==')
raw = NEW.read_text(encoding='utf-8')
i = raw.find('id="2026-10-23-1"')
k = raw.rfind('<article', 0, i)
j = raw.find('</article>', i)
entry = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', raw[k:j]))
P('version-like tokens in entry text: ' + repr(re.findall(r'\b8\.\d\.\d+\b', entry)))

P('\n== Cloudflare retained copies: first to mention the new CVE or upload progress ==')
for snap in sorted(LH028.glob('snapshot-*')):
    f = snap / 'cloudflare.raw'
    b = f.read_bytes()
    mod = re.search(rb'article:modified_time" content="([^"]+)"', b) or re.search(rb'content="([^"]+)" property="article:modified_time"', b)
    P(f'{snap.name}: modified_time={mod.group(1).decode() if mod else "?"} 115560={b.count(b"115560")} '
      f'upload_progress={b.count(b"upload_progress")} "fully patched"={b.count(b"fully patched")} '
      f'"all plans, including Free"={b.count(b"all plans, including Free")}')

P('\n== clock intervals the pieces cite (UTC) ==')
def t(s):
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc) if datetime.fromisoformat(s).tzinfo is None else datetime.fromisoformat(s)
php_stamp = t('2026-10-23T10:12:28+00:00')
pairs = [
    ('LH024 read without the entry (22 Oct 06:24:43) to LH029 read with it (23 Oct 17:00:11)', t('2026-10-22T06:24:43+00:00'), t('2026-10-23T17:00:11+00:00')),
    ('PHP entry stamp (10:12:28) to Cloudflare modified_time (15:09:11)', php_stamp, t('2026-10-23T15:09:11+00:00')),
    ('PHP entry stamp to LH028 read of Cloudflare revision (16:06:07)', php_stamp, t('2026-10-23T16:06:07+00:00')),
    ('PHP entry stamp to LH029 read (17:00:11)', php_stamp, t('2026-10-23T17:00:11+00:00')),
    ('LH028 10:00 slot without the revision (10:00) to 16:06 read with it', t('2026-10-23T10:00:00+00:00'), t('2026-10-23T16:06:07+00:00')),
    ('RC4 entry stamp (21 Oct 15:41:41) to LH024 copy lacking it (22 Oct 06:24:43)', t('2026-10-21T15:41:41+00:00'), t('2026-10-22T06:24:43+00:00')),
]
for label, a, b in pairs:
    d = b - a
    P(f'{label}: {d.days * 24 + d.seconds // 3600}h {(d.seconds % 3600) // 60}m {d.seconds % 60}s')

text = '\n'.join(out)
Path(__file__).with_name('reader_check.txt').write_text(text + '\n')
print(text)
