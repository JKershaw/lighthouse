#!/usr/bin/env python3
"""Replace LH036's kept git.kernel.org responses with derived files (the keeper's decision of 21 November 2026,
notes/keeper/2026-11-21-robots-intent.md: git.kernel.org's robots.txt refuses AI-training crawlers by name
and all bots under `*`).

Each response kept was a bot challenge page, not the announcement or the commit (the record classes the
announcement "unavailable"). For each data/read-*/kernel_announcement.raw.gz and upstream_fix.raw.gz it writes
<name>.derived.json beside it, holding the URL, read times, HTTP status, size and SHA-256 from that read's
read_log.json, and only what tabulate.py and review/check_fixes.py take from the page: whether it is a challenge
page or under 200 bytes, its <title> as written, the dateModified field if any, and the SHA-256 of its visible
text lines as tabulate.py's text_of() joins them. No text of the page is kept.
It never deletes anything. Offline, standard library only. Usage: python3 -I studies/LH036/scripts/derive_kept.py
"""
from hashlib import sha256
from html import unescape
from pathlib import Path
import gzip, json, re

DATA = Path(__file__).resolve().parents[1] / 'data'
NAMES = ('kernel_announcement', 'upstream_fix')
NOTE = ("Body removed on 21 November 2026 under the keeper's decision (notes/keeper/2026-11-21-robots-intent.md): "
        "the site's robots.txt refuses AI-training or archiving crawlers, or all bots, so Lighthouse keeps the "
        "URL, read time, status, SHA-256 of the bytes received and the facts its records use, not the page.")
USED = {'kernel_announcement': "Measure 5 (pages): the kernel CVE team's announcement; a bot challenge page, so 'unavailable' (tabulate.py, review/check_fixes.py).",
        'upstream_fix': "Read once with the panel on 1 November; a bot challenge page; no script or record figure uses it."}


def text_of(html):  # as tabulate.py
    html = re.sub(r'(?s)<(script|style).*?</\1>', '', html)
    s = unescape(re.sub(r'<[^>]+>', '\n', html))
    s = re.sub(r'[ \t\r]+', ' ', s)
    return [line.strip() for line in s.split('\n') if line.strip()]


def main():
    n = 0
    for read in sorted(p for p in DATA.glob('read-*') if p.is_dir()):
        log = {r['name']: r for r in json.loads((read / 'read_log.json').read_text())}
        for name in NAMES:
            row = log.get(name)
            if not row or not row.get('file') or not (read / row['file']).exists():
                continue
            raw = gzip.decompress((read / row['file']).read_bytes())
            t = raw.decode('utf-8', 'replace')
            dm = re.search(r'"dateModified"\s*:\s*"([^"]+)"', t)
            title = re.search(r'(?s)<title>(.*?)</title>', t)
            rec = {'url': row.get('url'), 'read_utc': row.get('start_utc'), 'finish_utc': row.get('finish_utc'),
                   'http_status': row.get('status'), 'bytes': row.get('bytes'), 'sha256': row.get('sha256'),
                   'robots_class': 'A+: AI-training token named and refused; * refuses too', 'body_removed': NOTE,
                   'used_for': USED[name],
                   'extracted': {'challenge_page': 'not a bot' in t[:2000], 'short_body': len(raw) < 200,
                                 'title': title.group(1) if title else None, 'dateModified': dm.group(1) if dm else None,
                                 'text_sha256': sha256('\n'.join(text_of(t)).encode()).hexdigest()}}
            (read / (name + '.derived.json')).write_text(json.dumps(rec, indent=1, ensure_ascii=False) + '\n')
            n += 1
    print('derived files written:', n)


if __name__ == '__main__':
    main()
