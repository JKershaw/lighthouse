#!/usr/bin/env python3
"""Withhold LH044's kept page bodies from sites whose robots.txt refuses AI-training or archiving crawlers
(the keeper's decision of 21 November 2026, notes/keeper/2026-11-21-robots-intent.md; found by
notes/keeper/robots-intent-2026-11-21/sweep_may_keep.py once its log tie was fixed, output
sweep_may_keep_output_2.json).

LH044 already has a form for a body it may not keep (amendment of 9 November 2026, use=reference): <n>.b holds a
placeholder, <n>.withheld.json the URL, read time, status and SHA-256 of the bytes received with a short extract,
and the classifier's result is kept in the record's "derived" field, which do_classify reads when the body is
gone. This script puts each listed body into that form:
  1. writes <n>.withheld.json (from readlog.csv and the body: title, and for the statement page the quotation
     statements/coded.csv takes from it, checked against the page's text) and the run copy <n>.b.withheld-local,
     and replaces <n>.b with the keeper's placeholder;
then the caller runs `collect.py --classify <label>` once, which saves the class, detail, marker and echoes
derived from the local copy into each record, deletes the local copies, and runs --classify again to check
that every output is unchanged. Offline, standard library only.
Usage: python3 -I studies/LH044/scripts/derive_kept.py
"""
import csv, hashlib, html, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT.parents[1] / 'scripts'))
import content_signal  # noqa: E402

WHY = ("The site's robots.txt refuses AI-training or archiving crawlers (here ClaudeBot by name, read through "
       "scripts/robots_gate.py on 21 November 2026), so Lighthouse keeps no copy of the page in its public repository "
       "(the keeper's decision of 21 November 2026, notes/keeper/2026-11-21-robots-intent.md). Withheld by a subagent "
       "of the Watch run of that day.")
TARGETS = [  # (folder, request number, host)
    ('read-2026-11-08T1920Z', 10, 'codeberg.org'), ('read-2026-11-08T1920Z', 12, 'git.sr.ht'),
    ('read-2026-11-08T1920Z', 40, 'repo1.maven.org'), ('read-2026-11-08T1920Z', 70, 'archive.ubuntu.com'),
    ('read-2026-11-08T1920Z', 106, 'runescape.wiki'), ('read-2026-11-08T1920Z', 113, 'wiki.gentoo.org'),
    ('read-2026-11-08T1920Z', 228, 'ftp.eq.uc.pt'), ('read-2026-11-15T1413Z', 70, 'archive.ubuntu.com'),
    ('statements-2026-11-08T1920Z', 11, 'lwn.net'),
]


def text(raw):
    t = raw.decode('utf-8', 'replace')
    t = re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>', ' ', t)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', t)))


def main():
    coded = {r['kept_as']: r for r in csv.DictReader(open(ROOT / 'statements' / 'coded.csv'))}
    n_done = 0
    for folder, n, host in TARGETS:
        d = ROOT / 'data' / folder
        b = d / ('%04d.b' % n)
        if content_signal.load_record(b) is not None:
            continue  # already withheld
        row = next(r for r in csv.DictReader(open(d / 'readlog.csv')) if r['n'] == str(n))
        assert row['url'].split('/')[2] == host, (folder, n, row['url'])
        body = b.read_bytes()
        extract = {'title': content_signal.title_of(body)}
        c = coded.get('data/%s/%04d.b' % (folder, n))
        if c and c.get('quote'):
            assert re.sub(r'\s+', '', c['quote']) in re.sub(r'\s+', '', text(body)), 'quotation not in the page'
            extract['quote_in_statements_coded_csv'] = c['quote']
        rec = {'why': WHY, 'date': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
               'by': 'studies/LH044/scripts/derive_kept.py', 'url': row['url'], 'service': row['service'],
               'kind': row['kind'], 'fetched_utc': row['utc'], 'http_status': int(row['status']) if row['status'] else None,
               'fetch_log': 'studies/LH044/data/%s/readlog.csv (n=%d)' % (folder, n),
               'sha256_received': row['sha256'], 'bytes_received': int(row['bytes']),
               'headers': '%04d.h (kept unchanged)' % n, 'extract': extract}
        content_signal.write_withheld(b, body, rec, keeper=True)
        rp = content_signal.record_path(b)
        r = json.loads(rp.read_text())
        r.update(sha256_kept_until_withheld=hashlib.sha256(body).hexdigest(), bytes_kept_until_withheld=len(body))
        rp.write_text(json.dumps(r, indent=1, ensure_ascii=False) + '\n')
        n_done += 1
    print('withheld:', n_done)


if __name__ == '__main__':
    main()
