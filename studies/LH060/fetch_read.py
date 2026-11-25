#!/usr/bin/env python3
"""LH060 search-read: one gated one-off GET per candidate document, in the brief's fixed order.

Run: LIGHTHOUSE_PROVIDER=anthropic python3 -I studies/LH060/fetch_read.py <out_dir> <scratch_dir>

- Every request goes through scripts/lh_fetch.py with access='oneoff', robots checked before the
  request and before every redirect (check_redirects=True).
- One retry only on a timeout, a connection error or HTTP 500, 502 or 504 (brief, "Ceiling").
- Any other non-200 answer, a challenge, login or form is a wall: logged, never got around.
- A body is kept only through save_body and only where the document text states a Creative Commons
  licence; otherwise nothing of the body is written to <out_dir>. PDF text is extracted with the
  system's pdftotext (a fixed binary, no code from the download is run) into <scratch_dir>, outside
  the repository, for reading only; the reader then writes facts with write_derived.
- Every attempt, including robots refusals, is appended to studies/LH060/fetchlog.csv.
Written 25 November 2026 for queue row LH060-search-read.
"""
import csv
import hashlib
import os
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'scripts'))
from lh_fetch import urlopen, save_body, NotFetched, UA, keep_decision  # noqa: E402

# The fixed reading order (brief: tier, then most recent year, then first appearance; known
# documents not returned follow on ties). Fifteen candidates, so every candidate gets one GET.
ORDER = [
    ('C01', 'https://www.ndss-symposium.org/wp-content/uploads/2018/02/ndss2018_02A-2_Stock_paper.pdf'),
    ('C02', 'https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_li.pdf'),
    ('C03', 'https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_stock.pdf'),
    ('C04', 'https://www.verizon.com/business/resources/reports/2025-dbir-data-breach-investigations-report.pdf'),
    ('C05', 'https://www.cyentia.com/?p=24352'),
    ('C06', 'https://www.cyentia.com/?p=24354'),
    ('C07', 'https://arxiv.org/pdf/2611.09703'),
    ('C08', 'https://arxiv.org/pdf/2605.18901'),
    ('C09', 'https://arxiv.org/pdf/2512.01891'),
    ('C10', 'https://arxiv.org/pdf/2405.19871'),
    ('C11', 'https://arxiv.org/pdf/2202.09016'),
    ('C12', 'https://arxiv.org/pdf/2106.08024'),
    ('C13', 'https://arxiv.org/pdf/2104.04030'),
    ('C14', 'https://arxiv.org/pdf/2012.00544'),
    ('C15', 'https://arxiv.org/pdf/1708.06693'),
]
FIELDS = ['candidate', 'url', 'final_url', 'attempt', 'start_utc', 'finish_utc', 'outcome', 'http_status',
          'content_type', 'bytes', 'sha256', 'licence_stated', 'body_kept', 'note']
RETRY_STATUS = {500, 502, 504}
WALL_WORDS = re.compile(rb'(captcha|cf-challenge|just a moment|access denied|sign in to|log in to|register to download|'
                        rb'please fill out|request access)', re.I)
CC = re.compile(r'creative\s*commons|CC[\s-]BY', re.I)


def now():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urlopen(req, timeout=60, check_redirects=True, access='oneoff') as r:
        return r.status, r.geturl(), r.headers.get('Content-Type', ''), dict(r.headers), r.read()


def main(out_dir, scratch):
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(scratch, exist_ok=True)
    log = os.path.join(HERE, 'fetchlog.csv')
    new = not os.path.exists(log)
    only = set(sys.argv[3:])
    with open(log, 'a', newline='') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        for cid, url in ORDER:
            if only and cid not in only:
                continue
            for attempt in (1, 2):
                row = {'candidate': cid, 'url': url, 'attempt': attempt, 'start_utc': now()}
                retry = False
                try:
                    status, final, ctype, headers, body = get(url)
                    row.update(final_url=final, http_status=status, content_type=ctype, bytes=len(body),
                               sha256=hashlib.sha256(body).hexdigest())
                    text = ''
                    if body[:5] == b'%PDF-':
                        p = subprocess.run(['pdftotext', '-layout', '-', '-'], input=body, capture_output=True,
                                           timeout=120)
                        text = p.stdout.decode('utf-8', 'replace')
                        row['outcome'] = 'full text (PDF)' if text.strip() else 'PDF, no text extracted'
                    else:
                        text = body.decode('utf-8', 'replace')
                        row['outcome'] = 'non-PDF body' + ('; wall words present' if WALL_WORDS.search(body) else '')
                    with open(os.path.join(scratch, cid + '.txt'), 'w', encoding='utf-8') as t:
                        t.write(text)
                    lic = bool(CC.search(text[:20000]))
                    row['licence_stated'] = 'Creative Commons mention in text' if lic else 'none found'
                    if lic:
                        ext = '.pdf' if body[:5] == b'%PDF-' else '.html'
                        kept, why = save_body(os.path.join(out_dir, cid + ext), body, final, headers,
                                              access='oneoff')
                        row['body_kept'] = ('yes: ' if kept else 'no: ') + str(why)
                    else:
                        k, why = keep_decision(final, body, headers, access='oneoff')
                        row['body_kept'] = 'no: no redistribution licence stated (robots/page rule: %s)' % why
                except NotFetched as e:
                    row.update(outcome='robots refusal, not requested', note=str(e)[:300], body_kept='no')
                except urllib.error.HTTPError as e:
                    row.update(outcome='wall: HTTP %s' % e.code, http_status=e.code, body_kept='no',
                               final_url=getattr(e, 'url', ''))
                    retry = e.code in RETRY_STATUS
                except (socket.timeout, TimeoutError, urllib.error.URLError, ConnectionError) as e:
                    row.update(outcome='error: %s' % type(e).__name__, note=str(e)[:300], body_kept='no')
                    retry = True
                row['finish_utc'] = now()
                w.writerow(row)
                f.flush()
                print(cid, attempt, row.get('outcome'), row.get('http_status', ''), row.get('bytes', ''),
                      row.get('body_kept', ''))
                if not (retry and attempt == 1):
                    break
                time.sleep(5)
            time.sleep(3)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
