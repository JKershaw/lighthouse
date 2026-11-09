#!/usr/bin/env python3
"""One LH048 read. Modelled on studies/LH036/scripts/collect.py.

Usage:
  python3 -I studies/LH048/scripts/collect.py --discover --read 2026-11-10T1415Z
      the post and the two vendor pages it links, once, before the selection rule is applied (brief, Selection)
  python3 -I studies/LH048/scripts/collect.py --read 2026-11-10T1430Z [--full]
      the signals for every CVE in selection.json: KEV catalogue, EPSS series (batched), Microsoft's record for
      the Windows CVE, the CVE record and NVD for each chain CVE, and the three pages; --full (the baseline and
      the last read) adds the CVE record and NVD for every CVE in the linked set.

Every request is asked of scripts/robots_gate.py first (the keeper's rule of 8 November 2026; set
LIGHTHOUSE_PROVIDER to the provider running the session, or every provider's tokens are obeyed). A URL the gate
refuses is logged "not fetched", a missing reading and never a negative. Bodies are saved gzipped after
scripts/redact_emails.py redact_bytes; the log keeps the SHA-256 of the bytes received.

Reads already held are skipped: if data/<kind>-<label>/ exists, the run resumes it, and a target whose body is
already saved there with an HTTP status is not requested again. Nothing is overwritten.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import argparse
import gzip
import json
import re
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
from robots_gate import RobotsGate  # noqa: E402  the keeper's robots.txt rule, 8 November 2026
from redact_emails import redact_bytes  # noqa: E402  email addresses withheld

UA = 'Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)'
GATE = RobotsGate(UA)
ROOT = Path(__file__).resolve().parents[1]
PANEL = json.loads((ROOT / 'panel.json').read_text())
CEILING = 4 * 1024 * 1024          # bytes kept per body
MAX_GETS = {'discover': 3, 'read': 40, 'full': 220}   # brief, Ceiling (robots.txt fetches not counted)
NVD_GAP = 6.5                      # seconds between NVD requests: its public limit is 5 per rolling 30 s
CVE_RE = re.compile(r'^CVE-\d{4}-\d{4,}$')

parser = argparse.ArgumentParser()
parser.add_argument('--read', required=True, help='UTC label, e.g. 2026-11-10T1430Z')
parser.add_argument('--discover', action='store_true')
parser.add_argument('--full', action='store_true')
args = parser.parse_args()
datetime.strptime(args.read, '%Y-%m-%dT%H%MZ')
assert not (args.discover and args.full), '--discover and --full do not combine'


def chain_and_linked():
    sel = json.loads((ROOT / 'selection.json').read_text())
    assert sel.get('rule_applied_at'), 'selection rule not yet applied: run --discover and fill selection.json first'
    assert not [u for u in sel['units'] if u['class'] == 'pending'], 'a unit is still pending'
    chain = []
    for u in sel['units']:
        for c in u['cves'] + u.get('candidates', []):
            if c not in chain:
                chain.append(c)
    linked = [c for c in sel.get('linked_set', []) if c not in chain]
    for c in chain + linked:
        assert CVE_RE.match(c), c
    return chain, linked


targets = []   # (group, name, url)
if args.discover:
    kind, mode = 'discover', 'discover'
    targets.append(('pages', 'post', PANEL['post']))
    for k, u in PANEL['linked_pages'].items():
        targets.append(('pages', k, u))
else:
    kind, mode = 'read', ('full' if args.full else 'read')
    chain, linked = chain_and_linked()
    sig = PANEL['signals']
    targets.append(('signals', 'kev', sig['kev']))
    every = chain + linked
    for i in range(0, len(every), 100):
        targets.append(('signals', 'epss_%d' % (i // 100), sig['epss'].format(cves=','.join(every[i:i + 100]))))
    for c in PANEL['msrc_cves']:
        targets.append(('signals', 'msrc_' + c, sig['msrc'].format(cve=c)))
    for c in chain + (linked if args.full else []):
        targets.append(('signals', 'cve_org_' + c, sig['cve_org'].format(cve=c)))
        targets.append(('signals', 'nvd_' + c, sig['nvd'].format(cve=c)))
    targets.append(('pages', 'post', PANEL['post']))
    for k, u in PANEL['linked_pages'].items():
        targets.append(('pages', k, u))
assert len(targets) <= MAX_GETS[mode], 'over the ceiling of %d GETs for a %s read' % (MAX_GETS[mode], mode)

OUT = ROOT / 'data' / ('%s-%s' % (kind, args.read))
LOG = OUT / 'read_log.json'
rows = json.loads(LOG.read_text()) if LOG.exists() else []
held = {r['name'] for r in rows if r.get('file') and isinstance(r.get('status'), int) and (OUT / r['file']).exists()}
rows = [r for r in rows if r['name'] in held]   # earlier failed attempts are re-tried; their rows are replaced
OUT.mkdir(parents=True, exist_ok=True)
last_nvd = 0.0
for group, name, url in targets:
    if name in held:
        print(json.dumps({'name': name, 'skipped': 'already held'}), flush=True)
        continue
    if name.startswith('nvd_'):
        wait = NVD_GAP - (time.monotonic() - last_nvd)
        if wait > 0:
            time.sleep(wait)
        last_nvd = time.monotonic()
    row = {'group': group, 'name': name, 'url': url, 'start_utc': datetime.now(timezone.utc).isoformat()}
    ok, rinfo = GATE.check(url)
    row['robots'] = rinfo
    if not ok:
        row['error'] = 'not fetched: ' + rinfo['reason']
    else:
        try:
            request = Request(url, headers={'User-Agent': UA})
            try:
                response = urlopen(request, timeout=40)
            except HTTPError as error:
                response = error
            with response:
                body = response.read(CEILING + 1)
                row.update(finish_utc=datetime.now(timezone.utc).isoformat(), status=response.status,
                           final_url=response.geturl(), content_type=response.headers.get('Content-Type', ''),
                           last_modified=response.headers.get('Last-Modified', ''), bytes=len(body),
                           sha256=sha256(body).hexdigest())
                if len(body) <= CEILING:
                    redacted, n = redact_bytes(body)
                    (OUT / (name + '.raw.gz')).write_bytes(gzip.compress(redacted, mtime=0))
                    row.update(file=name + '.raw.gz', emails_withheld=n)
                else:
                    row['error'] = 'over the 4 MiB ceiling; no body retained'
        except Exception as error:
            row.update(finish_utc=datetime.now(timezone.utc).isoformat(), error=type(error).__name__ + ': ' + str(error))
    rows.append(row)
    LOG.write_text(json.dumps(rows, indent=2) + '\n')
    print(json.dumps({k: row.get(k) for k in ('name', 'status', 'bytes', 'error')}), flush=True)
LOG.write_text(json.dumps(rows, indent=2) + '\n')
