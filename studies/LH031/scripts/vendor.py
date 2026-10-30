#!/usr/bin/env python3
"""LH031 amendment 5: one read of Palo Alto Networks' advisory (page and CSAF) and Unit 42's brief; extracts the dated fields."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import argparse
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [('advisory', 'https://security.paloaltonetworks.com/CVE-2026-109618'),
           ('csaf', 'https://security.paloaltonetworks.com/csaf/CVE-2026-109618'),
           ('unit42', 'https://unit42.paloaltonetworks.com/cve-2026-109618-cve-2026-109619/')]
CEILING = 2 * 1024 * 1024
# Sentences whose presence or absence the amendment classes; each is matched in the page's text, whitespace collapsed.
ADVISORY_SENTENCES = {'will_be_fixed': 'This issue will be fixed in the upcoming releases of PAN-OS',
                      'until_fix_available': 'Until PAN-OS fix versions are available',
                      'active_exploitation': 'Active exploitation has been observed'}
UNIT42_SENTENCES = {'actively_exploited': 'being actively exploited against PAN-OS management interfaces',
                    'independently_verified': 'independently verified the same attacker',
                    'patched_not_affected': 'Customers who have applied the available patches are not affected',
                    'share_impacted': 'approximately .02%'}


def text_of(body):
    page = body.decode('utf-8', errors='replace')
    page = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', page, flags=re.S | re.I)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', page))).strip()


def label_after(text, label):
    found = re.search(re.escape(label) + r' (\S+)', text)
    return found.group(1) if found else None


def advisory(body):
    text = text_of(body)
    return {'published': label_after(text, 'Published'), 'updated': label_after(text, 'Updated'),
            'exploit_maturity': label_after(text, 'Exploit Maturity'),
            'sentences': {k: s in text for k, s in ADVISORY_SENTENCES.items()},
            'fixed_builds': sorted(set(re.findall(r'>= (\d+\.\d+\.\d+(?:-h\d+)?)', text))),
            'upgrade_to': sorted(set(re.findall(r'(\d+\.\d+\.\d+(?:-h\d+)?)', ' '.join(re.findall(r'Upgrade to (.*?) or later', text))))),
            'previously_impacted': re.findall(r'[^.*]*previously impacted[^.]*\.', text)}


def csaf(body):
    data = json.loads(body)
    tracking = data.get('document', {}).get('tracking', {})
    fixed = sorted({p for v in data.get('vulnerabilities', []) for p in v.get('product_status', {}).get('fixed', [])})
    return {'version': tracking.get('version'), 'initial_release_date': tracking.get('initial_release_date'),
            'current_release_date': tracking.get('current_release_date'),
            'revision_history': tracking.get('revision_history'),
            'fixed_product_ids': fixed,
            'remediations': [{k: r.get(k) for k in ('category', 'date', 'details')}
                             for v in data.get('vulnerabilities', []) for r in v.get('remediations', [])]}


def unit42(body):
    text = text_of(body)
    title = re.search(r'<title>([^<]*)', body.decode('utf-8', errors='replace'))
    return {'title': html.unescape(title.group(1)).strip() if title else None,
            'published': published.group(1) if (published := re.search(r'Published: (\w+ \d+, \d{4})', text)) else None,
            'update_headings': re.findall(r'Update (\w+ \d+, \d{4})', text),
            'sentences': {k: s in text for k, s in UNIT42_SENTENCES.items()}}


EXTRACT = {'advisory': advisory, 'csaf': csaf, 'unit42': unit42}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--read', required=True, help='UTC label, e.g. 2026-11-02T0630Z')
    args = parser.parse_args()
    datetime.strptime(args.read, '%Y-%m-%dT%H%MZ')
    OUT = ROOT / 'data' / ('vendor-' + args.read)
    assert not OUT.exists(), 'read already exists'
    OUT.mkdir(parents=True)
    log, result = [], {}
    for name, url in SOURCES:
        row = {'source': name, 'url': url, 'start_utc': datetime.now(timezone.utc).isoformat()}
        try:
            try:
                response = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Lighthouse research observation)'}), timeout=30)
            except HTTPError as error:
                response = error
            with response:
                body = response.read(CEILING + 1)
                row.update(finish_utc=datetime.now(timezone.utc).isoformat(), status=response.status, final_url=response.geturl(),
                           bytes=len(body), sha256=sha256(body).hexdigest(), content_type=response.headers.get('Content-Type', ''))
                if len(body) > CEILING:
                    row['error'] = 'over 2 MiB ceiling; no body retained'
                else:
                    (OUT / (name + '.raw')).write_bytes(body)
                    row['file'] = name + '.raw'
                    if response.status == 200:
                        result[name] = EXTRACT[name](body)
        except Exception as error:
            row.setdefault('finish_utc', datetime.now(timezone.utc).isoformat())
            row['error'] = type(error).__name__ + ': ' + str(error)[:200]
        log.append(row)
        print(json.dumps({k: row.get(k) for k in ('source', 'status', 'bytes', 'error')}))
    (OUT / 'read_log.json').write_text(json.dumps(log, indent=2) + '\n')
    (OUT / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=1))
