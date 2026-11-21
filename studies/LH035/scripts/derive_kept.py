#!/usr/bin/env python3
"""Replace LH035's kept pages from sites whose robots.txt refuses AI-training or archiving crawlers, or all
bots, with derived files (the keeper's decision of 21 November 2026, notes/keeper/2026-11-21-robots-intent.md).

For each page below it writes <file stem>.derived.json beside it, holding the URL, read time, HTTP status,
size and SHA-256 from that directory's readlog.csv, and only what the record uses of the page: the quoted
phrases and the figures of the instruments.json rows that cite it, each with whether the page bore it out,
in the form scripts/reread_check.py compares (lower-cased and normalised as its norm() does; "text" is a
match in the page's visible text, "raw" a match only in its markup). Nothing else from the page is kept.
It never deletes anything. Offline, standard library only. Run from studies/LH035:
python3 -I scripts/derive_kept.py
"""
import csv, html, json, os, re

NOTE = ("Body removed on 21 November 2026 under the keeper's decision (notes/keeper/2026-11-21-robots-intent.md): "
        "the site's robots.txt refuses AI-training or archiving crawlers, or all bots, so Lighthouse keeps the "
        "URL, read time, status, SHA-256 of the bytes received and the facts its records use, not the page.")
PAGES = [  # (directory, file, robots class, what the record used it for)
    ("data/reads-2026-11-06", "07-I05-routeviews-org-routeviews.html", "A: AI-training token named and refused; * allows",
     "Row I05 (RouteViews): re-read of 6 November, checked against the row's quotations and figures."),
    ("data/reads-2026-11-06", "12-I07-downloads-pch-net-bgp-routing-data.html", "B: * refuses all bots (no AI token named)",
     "Row I07 (PCH routing data): re-read of 6 November; a directory listing, checked against the row's quotations and figures."),
    ("data/reads-2026-11-06", "32-I20-w3techs-com-technologies.html", "A: AI-training token named and refused; * allows",
     "Row I20 (W3Techs): methodology page, re-read of 6 November, checked against the row's quotations and figures."),
    ("data/reads-2026-11-06", "33-I20-w3techs-com-disclaimer.html", "A: AI-training token named and refused; * allows",
     "Row I20 (W3Techs): disclaimer page, re-read of 6 November, checked against the row's quotations and figures."),
    ("data/reads-2026-11-05", "14-caida-publicdata-asfac.html", "B: * refuses all bots (no AI token named)",
     "Row I41 (CAIDA AS facilities): the public data directory, read 5 November; source of the row's file listing."),
]
FIELDS = ['counts', 'vantage', 'cadence', 'history', 'access', 'page_date', 'window', 'cannot_see', 'note']


def norm(s):  # as scripts/reread_check.py
    s = html.unescape(html.unescape(s))
    s = s.replace('\\u0026', '&').replace('\\"', '"').replace('\\n', ' ')
    s = re.sub(r'[‘’‛′]', "'", s); s = re.sub(r'[“”″]', '"', s)
    s = re.sub(r'[‐-―−]', '-', s); s = s.replace(' ', ' ').replace('…', '...')
    s = re.sub(r'\s+', ' ', s); return s.lower()


def text(raw):  # as scripts/reread_check.py
    t = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', raw, flags=re.S | re.I)
    t = re.sub(r'<[^>]+>', ' ', t); return norm(t)


def main():
    rows = json.load(open('data/instruments.json'))['rows']
    n = 0
    for d, fn, robots, used in PAGES:
        p = os.path.join(d, fn)
        if not os.path.exists(p):
            continue
        log = {r['file']: r for r in csv.DictReader(open(os.path.join(d, 'readlog.csv')))}[fn]
        raw = open(p, encoding='utf-8', errors='replace').read()
        t, rw = text(raw), norm(raw)
        both = t + ' ' + rw
        cite = [r for r in rows if any(u.split(' ')[0] == log['url'] for u in r['urls_read'])]
        segs_t, segs_r, nums = [], [], []
        for r in cite:
            for f in FIELDS:
                for q in re.findall(r'"([^"]+)"', r.get(f, '') or ''):
                    for s in [s.strip(' .,;') for s in re.split(r'\.\.\.|…', q) if s.strip(' .,;')]:
                        ns = norm(s)
                        if ns in t and ns not in segs_t:
                            segs_t.append(ns)
                        if ns in rw and ns not in segs_r:
                            segs_r.append(ns)
                v = re.sub(r'"[^"]+"', '', r.get(f, '') or '')
                for num in re.findall(r'\d[\d,\.]*\d|\d', v):
                    for x in (num.rstrip('.,'), num.rstrip('.,').replace(',', '')):
                        if x in both and x not in nums:
                            nums.append(x)
        rec = {'url': log['url'], 'read_utc': log['start_utc'], 'http_status': log['http_status'], 'bytes': int(log['bytes']),
               'sha256': log['sha256'], 'final_url': log.get('final_url') or None, 'robots_class': robots, 'body_removed': NOTE,
               'used_for': used, 'cited_by_rows': [r['id'] for r in cite],
               'extracted': {'quoted_segments_in_text': segs_t, 'quoted_segments_in_markup': segs_r, 'figures_found': nums,
                             'note': 'Only the quotations and figures of the rows that cite this page, as of the instruments.json '
                                     'read on 21 November 2026; a quotation added later cannot be checked against this file.'}}
        open(os.path.join(d, fn.rsplit('.', 1)[0] + '.derived.json'), 'w').write(json.dumps(rec, indent=1, ensure_ascii=False) + '\n')
        n += 1
    print('derived files written:', n)


if __name__ == '__main__':
    main()
