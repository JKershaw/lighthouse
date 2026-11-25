"""R-0138: where CVE-2026-126051 appears on each kept page (in memory)."""
import gzip, html, re
for v in ['v22.23.5', 'v24.22.3', 'v26.13.1']:
    t = gzip.open('studies/LH034/oneoff-2026-11-25/' + v + '.html.gz').read().decode('utf-8', 'replace')
    t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', t)))
    i = t.find('Notable')
    j = t.find('Commits')
    notable = t[i:j] if i >= 0 else ''
    print(v, 'notable-section CVEs', len(set(re.findall(r'CVE-\d{4}-\d+', notable))), 'has 126051 in notable:', '126051' in notable)
    for m in re.finditer('CVE-2026-126051', t):
        print('   ...', t[max(0, m.start()-120):m.end()+60])
