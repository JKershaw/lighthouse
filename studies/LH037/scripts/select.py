#!/usr/bin/env python3
"""LH037's panel rule, fixed before it was run (brief, "The panel").

From CISA's Known Exploited Vulnerabilities catalogue as LH031 retained it at 2026-10-23T1845Z
(catalogVersion 2026.10.23), count entries per vendorProject with dateAdded from 2023-01-01 through
2026-10-20, the day before PHP's 21 October releases. Exclude vendorProject "PHP", the source of the flaws.
The panel is the 20 vendorProject values with the most entries, every value tied at 20th place included.
Writes studies/LH037/selection.json. Usage: python3 studies/LH037/scripts/select.py
"""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
FEED = ROOT.parent / 'LH031' / 'data' / 'read-2026-10-23T1845Z' / 'feed.raw'
raw = FEED.read_bytes()
assert sha256(raw).hexdigest() == '07789ad3d7fd68ab0f8fa61d10f0f1dd79753e4ec3f3c1f68fa07bc44679f682'
catalogue = json.loads(raw)
counts = Counter(v['vendorProject'].strip() for v in catalogue['vulnerabilities']
                 if '2023-01-01' <= v['dateAdded'] <= '2026-10-20' and v['vendorProject'].strip() != 'PHP')
ranked = counts.most_common()
cut = ranked[19][1]
panel = [{'vendorProject': name, 'kev_entries': n} for name, n in ranked if n >= cut]
out = {'source': 'studies/LH031/data/read-2026-10-23T1845Z/feed.raw', 'catalogVersion': catalogue['catalogVersion'],
       'window': ['2023-01-01', '2026-10-20'], 'excluded': ['PHP'], 'cut_at_20th': cut,
       'vendors_counted': len(counts), 'panel': panel, 'next_five_outside': [
           {'vendorProject': name, 'kev_entries': n} for name, n in ranked if n < cut][:5]}
(ROOT / 'selection.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
