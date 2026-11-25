"""R-0138: find the Apigee quotes the piece uses in LH037's retained bodies (in memory)."""
import gzip, html, re, sys
from pathlib import Path
for rd in ['read-2026-11-02T1530Z', 'read-2026-11-23T1425Z']:
    for f in sorted(Path('studies/LH037/data', rd).glob('*apigee*')):
        if f.suffix == '.gz':
            t = gzip.decompress(f.read_bytes()).decode('utf-8', 'replace')
        else:
            t = f.read_text()
        t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', t)))
        print(rd, f.name, len(t))
        for pat in ['run PHP 7.3 or 7.4 on RHEL/CentOS 7, RHEL 8, or Amazon Linux 2, where no packaged fix is available',
                    'Drupal 7 and 9', 'Drupal 7 and Drupal 9', 'Edge for Private Cloud', 'offline', 'migrat', 'GCP-2026-072', '2026-10-24', 'October 24']:
            i = t.find(pat); print('   ', repr(pat[:50]), t.count(pat), ('... ' + t[max(0, i-150):i+200]) if i >= 0 and pat in ('offline', 'Drupal 7 and 9', 'Drupal 7 and Drupal 9', 'GCP-2026-072') else '')
