"""R-0138: check the one-off read's claims against its kept bodies, in memory only."""
import gzip, hashlib, html, re, sys
base = 'studies/LH034/oneoff-2026-11-25/'
for v in ['v22.23.5', 'v24.22.3', 'v26.13.1']:
    raw = gzip.open(base + v + '.html.gz').read()
    print(v, 'kept bytes', len(raw), 'sha256', hashlib.sha256(raw).hexdigest()[:16])
    t = html.unescape(re.sub(r'<[^>]+>', ' ', raw.decode('utf-8', 'replace')))
    t = re.sub(r'\s+', ' ', t)
    for pat in [r'2026-11-11, Version [^)]*\)', r'This is a security release\.?', r'Last Updated [A-Za-z]+ \d+, \d{4}']:
        m = re.findall(pat, t)
        print('  ', repr(pat), '->', len(m), m[:1])
    cves = sorted(set(re.findall(r'CVE-\d{4}-\d+', t)))
    print('   distinct CVEs', len(cves), cves[:1], cves[-1:])
    for w in ['October', 'v22.23.4', 'v24.22.1', 'v26.12.1', 'october-2026', '21 Oct', '2026-10-21']:
        print('   mentions', repr(w), t.count(w))
