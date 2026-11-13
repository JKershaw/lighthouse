#!/usr/bin/env python3
"""LH051 pre-brief read: the event's own records (the vendors' posts), read and kept before the brief is fixed.

It reads no GH Archive file and no GitHub page: no count of any kind. Modelled on
studies/LH049/scripts/collect_prebrief.py.

Usage:
  python3 -I studies/LH051/scripts/collect_prebrief.py --read <UTC label> [--extra name=url ...]
  python3 -I studies/LH051/scripts/collect_prebrief.py --rewithhold <pre-brief dir>
      re-applies the withholding below to bodies already kept (the log's SHA-256 stays that of the bytes received)

Every request is asked of scripts/robots_gate.py first (set LIGHTHOUSE_PROVIDER=anthropic). Only the vendors' own
hosts are allowed. Bodies are kept gzipped under data/pre-brief-<label>/ after withholding; read_log.json keeps URL,
UTC start and finish, status, bytes received, their SHA-256 (of the bytes as received, before withholding), and how
much was withheld. A target already held is skipped.

Withheld from every retained body (gate conditions 3 and 4, notes/horizon/2026-11-13T1452Z.md, Gate):
  email addresses (scripts/redact_emails.py redact_bytes);
  github.com account or repository paths, raw and gist links;
  t.me and telegram.me links;
  owner/name tokens in the page's text and attributes (outside <script> and <style>), the form in which the posts
  name repositories and packages in prose;
  words on a short list given here only as truncated SHA-256 hashes: the organisations, accounts, repositories and
  third-party app the posts name without a slash, and the Telegram chat and bot identifiers. So this script names
  no one. The withholding also catches some ordinary file paths and media types written as a/b; that is accepted.
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

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
from robots_gate import RobotsGate  # noqa: E402
from redact_emails import redact_bytes  # noqa: E402

UA = 'Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)'
ROOT = Path(__file__).resolve().parents[1]
CEILING = 16 * 1024 * 1024
MAX_REQUESTS = 8
# never a GitHub page, raw file, gist, Telegram channel or GH Archive file
FORBIDDEN = ('github.com', 'githubusercontent.com', 'gist.', 't.me', 'telegram', 'gharchive')
ALLOWED_HOSTS = ('www.stepsecurity.io', 'www.aikido.dev', 'aikido.dev')

GH_PATH = re.compile(rb'(?:https?:)?(?://)?(?:www\.|api\.)?github\.com/(?!(?:features|enterprise|security|about|pricing|'
                     rb'site|login|marketplace|topics|sponsors|solutions|resources|customer-stories|readme|events)\b)'
                     rb'[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.%-]+)*', re.I)
GH_RAW = re.compile(rb'(?:https?:)?(?://)?(?:raw\.githubusercontent\.com|gist\.github\.com|gist\.githubusercontent\.com)'
                    rb'/[^\s"\'<>)]*', re.I)
TG = re.compile(rb'(?:https?:)?(?://)?(?:t\.me|telegram\.me)/[^\s"\'<>)]*', re.I)
OWNER_NAME = re.compile(rb'(?<![\w./:@%#?=&-])[A-Za-z0-9][A-Za-z0-9_-]*(?:\.[A-Za-z0-9_-]+)?/[A-Za-z0-9_][A-Za-z0-9_.-]*'
                        rb'(?![\w/])')
WORD = re.compile(rb'-?[A-Za-z0-9][A-Za-z0-9_.-]*[A-Za-z0-9]|-?[A-Za-z0-9]')
BLOCK = re.compile(rb'(?is)(<(script|style)\b.*?</\2\s*>)')
MARK_GH = b'[github path withheld by Lighthouse]'
MARK_TG = b'[telegram link withheld by Lighthouse]'
MARK_NAME = b'[name withheld by Lighthouse]'
WITHHELD = {
    '023fa99679b2305de288', '0361fee6f348848d0f05', '0c291a1b4d7a18bbb655', '1370eab0e027d1e8bf84',
    '1381c45fa78cf6e9eab3', '1785cffc82139bd21f71', '1d4987a84a357d9c0e79', '27efd856472c752e4804',
    '33809f89c4ea27d4983b', '3ae1099a33dc8ce2f7ae', '44f804cce2269e996536', '478a1aa4c76bde9824c4',
    '5482d2628bdea7dd5951', '589fa4c6cd1c7cbe86f6', '5f100930d5befe2d277b', '608e304780bd36fe28f8',
    '62f5bb26d25bd09c9c10', '6c38443916788768cd7a', '719d04e71596689bffd4', '7aff4641241b98235eca',
    '91459b41a93ea8dd87eb', '92288b5c6a491031474f', '9bcbe8d684d7b9b0169d', '9e34ac473df62a4c4485',
    'a0a6d2ddde54a6fffa2f', 'a2a1e69c4f8340f60ff8', 'b31dd0f4af37adf1c6f5', 'b7104964fa557aa260c2',
    'b89a199ea81b6a925de7', 'c41aaf739d7d04382cd8', 'c9e2f0e7685f6f72e29c', 'cf54da387b37ec0bb7ff',
    'ddffa04bd707959537d3', 'f44a450395fd2ad9f393', 'fa2b780cf21fb1a269a9',
}

TARGETS = [
    ('stepsecurity_post', 'https://www.stepsecurity.io/blog/wfx-phantom-the-github-actions-secret-stealer'),
    ('stepsecurity_blog', 'https://www.stepsecurity.io/blog'),
    ('aikido_blog', 'https://www.aikido.dev/blog'),
]


def withhold(data):
    """Return (body with the withheld classes replaced, counts by class)."""
    data, n_email = redact_bytes(data)
    data, n_raw = GH_RAW.subn(MARK_GH, data)
    data, n_gh = GH_PATH.subn(MARK_GH, data)
    data, n_tg = TG.subn(MARK_TG, data)
    parts = BLOCK.split(data)        # text, block, tag name, text, block, tag name, ..., text
    n_owner = 0
    out = []
    for i, seg in enumerate(parts):
        if i % 3 == 0:
            seg, k = OWNER_NAME.subn(MARK_NAME, seg)
            n_owner += k
            out.append(seg)
        elif i % 3 == 1:
            out.append(seg)          # a <script> or <style> block, unchanged
    data = b''.join(out)
    n_word = 0

    def word(m):
        nonlocal n_word
        w = m.group(0)
        cands = {w, w.lstrip(b'-'), w.rstrip(b'.')}
        sub = [p for p in re.split(rb'[-_.]', w.lower()) if p]
        for i in range(len(sub)):       # names inside longer tokens, such as an image's file name
            for j in range(i + 1, min(i + 5, len(sub)) + 1):
                cands.add(b'-'.join(sub[i:j]))
                cands.add(b'.'.join(sub[i:j]))
        if any(sha256(c.lower()).hexdigest()[:20] in WITHHELD for c in cands):
            n_word += 1
            return MARK_NAME
        return w
    data = WORD.sub(word, data)
    return data, {'emails_withheld': n_email, 'github_paths_withheld': n_raw + n_gh, 'telegram_links_withheld': n_tg,
                  'owner_name_tokens_withheld': n_owner, 'listed_words_withheld': n_word}


def rewithhold(d):
    """Re-apply the withholding to bodies already kept in directory d, and add the counts to its log."""
    log = d / 'read_log.json'
    rows = json.loads(log.read_text())
    for r in rows:
        if r.get('file'):
            f = d / r['file']
            red, counts = withhold(gzip.decompress(f.read_bytes()))
            f.write_bytes(gzip.compress(red, mtime=0))
            for k, v in counts.items():
                r[k] = r.get(k, 0) + v
            r['rewithheld_utc'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
    log.write_text(json.dumps(rows, indent=2) + '\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--read')
    ap.add_argument('--extra', action='append', default=[], help='name=url, a page found in a kept record')
    ap.add_argument('--rewithhold', help='a pre-brief directory whose kept bodies to withhold again')
    a = ap.parse_args()
    if a.rewithhold:
        rewithhold(Path(a.rewithhold))
        return
    datetime.strptime(a.read, '%Y-%m-%dT%H%MZ')
    targets = TARGETS if not a.extra else [tuple(e.split('=', 1)) for e in a.extra]
    for _, url in targets:
        assert not any(f in url.lower() for f in FORBIDDEN), 'refused: ' + url
        assert url.split('/')[2] in ALLOWED_HOSTS, 'refused (not a vendor page): ' + url
    assert len(targets) <= MAX_REQUESTS
    gate = RobotsGate(UA)
    out = ROOT / 'data' / ('pre-brief-' + a.read)
    out.mkdir(parents=True, exist_ok=True)
    log = out / 'read_log.json'
    rows = json.loads(log.read_text()) if log.exists() else []
    held = {r['name'] for r in rows if r.get('file')}
    for name, url in targets:
        if name in held:
            continue
        row = {'name': name, 'url': url, 'method': 'GET',
               'start_utc': datetime.now(timezone.utc).isoformat(timespec='seconds')}
        ok, info = gate.check(url)
        row['robots'] = info
        if not ok:
            row['error'] = 'not fetched: ' + info['reason']
        else:
            try:
                try:
                    resp = urlopen(Request(url, headers={'User-Agent': UA}), timeout=60)
                except HTTPError as err:
                    resp = err
                with resp:
                    data = resp.read(CEILING + 1)
                    row.update(finish_utc=datetime.now(timezone.utc).isoformat(timespec='seconds'), status=resp.status,
                               final_url=resp.geturl(), content_type=resp.headers.get('Content-Type', ''),
                               last_modified=resp.headers.get('Last-Modified', ''), bytes=len(data),
                               sha256=sha256(data).hexdigest())
                    if len(data) <= CEILING:
                        red, counts = withhold(data)
                        (out / (name + '.raw.gz')).write_bytes(gzip.compress(red, mtime=0))
                        row.update(file=name + '.raw.gz', **counts)
            except Exception as err:
                row.update(finish_utc=datetime.now(timezone.utc).isoformat(timespec='seconds'),
                           error=type(err).__name__ + ': ' + str(err)[:300])
        rows.append(row)
        log.write_text(json.dumps(rows, indent=2) + '\n')
        print(json.dumps({k: row.get(k) for k in ('name', 'status', 'bytes', 'sha256', 'error')}), flush=True)


if __name__ == '__main__':
    main()
