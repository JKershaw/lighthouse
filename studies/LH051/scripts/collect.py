#!/usr/bin/env python3
"""One LH051 read, as fixed in studies/LH051/brief.md (protocol 0.1). Run only under a schedule row, after the
brief is committed. Modelled on studies/LH049/scripts/collect.py and studies/LH046/scripts/collect.py.

Usage:
  LIGHTHOUSE_PROVIDER=anthropic python3 -I studies/LH051/scripts/collect.py --read 2026-11-14T1500Z
  ... --read <label> --dry-run
      lists the hours a read would fetch and asks the robots.txt gate about each URL (which fetches only
      robots.txt); fetches no GH Archive file and no post, and writes nothing.
  ... --read <label> --to 2026-11-12-7      stop at an earlier hour than the last complete one

Each read:
  1. asks scripts/robots_gate.py about each hourly file https://data.gharchive.org/YYYY-MM-DD-H.json.gz from
     2026-11-09-0 to the last complete hour (its end at least 30 minutes before the read starts), never after
     LAST_HOUR, and fetches the hours not already held, one at a time, at least a second apart;
  2. streams each file, hashing the bytes received and decompressing in memory, and for every event reads only
     the branch-name fields the brief names (PullRequestEvent and PullRequestReviewEvent payload.pull_request.head.ref,
     CreateEvent and DeleteEvent payload.ref, PushEvent payload.ref) and matches them against the three markers;
  3. writes per hour only counts: data/hours.csv (the file's status, bytes, SHA-256, Last-Modified, lines, totals by
     type, minutes with events, gap-hour flag) and data/counts.csv (hour, marker, event type, action, events,
     distinct repositories, distinct actors), and logs every request in data/fetch-log.tsv; an hour held in
     hours.csv (HTTP 200, gzip_ok 1) with no row in counts.csv held no matching event;
  4. re-reads the two vendors' posts once, kept with names withheld (collect_prebrief.withhold) under
     data/read-<label>/, with read_log.json.

No repository, actor, organisation, branch, URL, SHA or timestamp of any matching event is written, printed or
retained (gate conditions 2 and 3): the distinct counts are formed in memory per hour and only their sizes kept.
No title, body, commit message, file or code is read; no payload, workflow, script, run log or Telegram channel is
ever requested (condition 4); no GitHub page or API. No key, token or credential.

A held hour (HTTP 200, decompressed whole, counted) is never fetched again. Ceilings: 480 hours in all; 1 GiB per
file (a larger one is unavailable, not counted); 30 GB received across the study (summed from data/hours.csv and
the fetch log); at most one retry per unavailable hour per read.
"""
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import argparse
import csv
import gzip
import json
import re
import subprocess
import sys
import time
import zlib

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / 'scripts'))
sys.path.insert(0, str(HERE))
from robots_gate import RobotsGate  # noqa: E402  the keeper's robots.txt rule, 8 November 2026
from collect_prebrief import withhold  # noqa: E402  emails, GitHub paths, names and Telegram links withheld

UA = 'Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)'
ROOT = HERE.parent
DATA = ROOT / 'data'
FIRST_HOUR = datetime(2026, 11, 9, 0)
LAST_HOUR = datetime(2026, 11, 28, 23)
MAX_HOURS = 480
FILE_CEILING = 1024 ** 3
STUDY_CEILING = 30 * 10 ** 9
POST_CEILING = 16 * 1024 * 1024
COMPLETE_AFTER = timedelta(minutes=30)
PAUSE = 1.0
POSTS = [
    ('stepsecurity_post', 'https://www.stepsecurity.io/blog/wfx-phantom-the-github-actions-secret-stealer'),
    ('aikido_post', 'https://www.aikido.dev/blog/compromised-github-accounts-push-ci-secret-stealer-to-tens-of-'
                    'thousands-of-repositories'),
]
MARKERS = [
    ('M1', re.compile(r'wfx-docs\Z')),
    ('M2', re.compile(r'chore/[a-z0-9]{8}\Z')),
    ('M3', re.compile(r'ci-check-[0-9]{4}\Z')),
]
TOTAL_TYPES = ('PushEvent', 'CreateEvent', 'DeleteEvent', 'PullRequestEvent', 'PullRequestReviewEvent')
PR_ACTIONS = ('opened', 'closed', 'reopened')
HOUR_FIELDS = ['hour', 'read', 'url', 'utc_start', 'utc_finish', 'http_status', 'bytes', 'sha256', 'last_modified',
               'gzip_ok', 'lines', 'json_errors', 'events'] + list(TOTAL_TYPES) + ['minutes_with_events', 'gap_hour']
COUNT_FIELDS = ['hour', 'marker', 'event_type', 'action', 'events', 'distinct_repos', 'distinct_actors']


def label_hour(h):
    return '%s-%d' % (h.strftime('%Y-%m-%d'), h.hour)


def parse_hour(s):
    d, h = s.rsplit('-', 1)
    return datetime.strptime(d, '%Y-%m-%d').replace(hour=int(h))


def brief_committed():
    """The brief is tracked by git and unchanged since the last commit (AGENTS.md: commit before any outcome)."""
    try:
        tracked = subprocess.run(['git', '-C', str(ROOT), 'ls-files', '--error-unmatch', 'brief.md'],
                                 capture_output=True).returncode == 0
        clean = subprocess.run(['git', '-C', str(ROOT), 'diff', '--quiet', 'HEAD', '--', 'brief.md'],
                               capture_output=True).returncode == 0
        return tracked and clean
    except OSError:
        return False


def read_csv(path):
    if not path.exists():
        return []
    with path.open(newline='') as f:
        return list(csv.DictReader(f))


def append_csv(path, fields, rows):
    new = not path.exists()
    with path.open('a', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        if new:
            w.writeheader()
        w.writerows(rows)


class Hashing:
    """A file-like wrapper that hashes and counts the bytes received, and stops at the per-file ceiling."""

    def __init__(self, raw):
        self.raw, self.h, self.n = raw, sha256(), 0

    def read(self, size=-1):
        b = self.raw.read(size if size and size > 0 else 1 << 20)
        self.h.update(b)
        self.n += len(b)
        if self.n > FILE_CEILING:
            raise OverflowError('over the 1 GiB per-file ceiling')
        return b


def match(ref):
    if not isinstance(ref, str):
        return []
    if ref.startswith('refs/heads/'):
        ref = ref[len('refs/heads/'):]
    return [m for m, rx in MARKERS if rx.match(ref)]


def count_file(stream, counts, totals):
    """Stream one hourly file; fill counts[(marker, type, action)] = [n, repo ids, actor ids] in memory."""
    lines = errors = events = 0
    minutes = set()
    d = zlib.decompressobj(16 + zlib.MAX_WBITS)
    buf = b''

    def handle(line):
        nonlocal lines, errors, events
        if not line.strip():
            return
        lines += 1
        try:
            e = json.loads(line)
        except ValueError:
            errors += 1
            return
        events += 1
        t = e.get('type', '')
        if t in totals:
            totals[t] += 1
        ca = e.get('created_at') or ''
        if len(ca) >= 16:
            minutes.add(ca[14:16])
        p = e.get('payload') or {}
        action = ''
        if t in ('PullRequestEvent', 'PullRequestReviewEvent'):
            ref = ((p.get('pull_request') or {}).get('head') or {}).get('ref')
            a = p.get('action') or ''
            action = a if (t == 'PullRequestEvent' and a in PR_ACTIONS) else ('other' if t == 'PullRequestEvent' else a)
        elif t in ('CreateEvent', 'DeleteEvent'):
            ref = p.get('ref')
            action = p.get('ref_type') or ''
        elif t == 'PushEvent':
            ref = p.get('ref')
        else:
            return
        for m in match(ref):
            c = counts.setdefault((m, t, action), [0, set(), set()])
            c[0] += 1
            c[1].add((e.get('repo') or {}).get('id'))
            c[2].add((e.get('actor') or {}).get('id'))

    while True:
        chunk = stream.read(1 << 20)
        if not chunk:
            break
        buf += d.decompress(chunk)
        while d.unused_data:                      # a concatenated gzip member
            rest = d.unused_data
            d = zlib.decompressobj(16 + zlib.MAX_WBITS)
            buf += d.decompress(rest)
        *full, buf = buf.split(b'\n')
        for line in full:
            handle(line)
    buf += d.flush()
    for line in buf.split(b'\n'):
        handle(line)
    if not d.eof:
        raise EOFError('gzip stream ended early')
    return lines, errors, events, len(minutes)


def fetch_hour(gate, h, label):
    url = 'https://data.gharchive.org/%s.json.gz' % label_hour(h)
    row = {'hour': label_hour(h), 'read': label, 'url': url,
           'utc_start': datetime.now(timezone.utc).isoformat(timespec='seconds')}
    ok, info = gate.check(url)
    log = {'url': url, 'robots': info.get('reason', '')}
    if not ok:
        row.update(http_status='not fetched: ' + info.get('reason', ''), gzip_ok='')
        return row, [], log
    totals = {t: 0 for t in TOTAL_TYPES}
    counts = {}
    try:
        try:
            resp = urlopen(Request(url, headers={'User-Agent': UA}), timeout=300)
        except HTTPError as err:
            resp = err
        with resp:
            row.update(http_status=resp.status, last_modified=resp.headers.get('Last-Modified', ''))
            hs = Hashing(resp)
            if resp.status == 200:
                try:
                    lines, errors, events, mins = count_file(hs, counts, totals)
                    row.update(gzip_ok=1, lines=lines, json_errors=errors, events=events, minutes_with_events=mins,
                               **totals, gap_hour=int(not (totals['PushEvent'] or totals['CreateEvent']
                                                           or totals['DeleteEvent'])))
                except (OSError, EOFError, zlib.error, OverflowError) as err:
                    row.update(gzip_ok=0, error=type(err).__name__ + ': ' + str(err)[:200])
                    counts = {}
            else:
                hs.read()
                row['gzip_ok'] = ''
            row.update(bytes=hs.n, sha256=hs.h.hexdigest())
    except Exception as err:
        row.update(http_status=row.get('http_status', 'error'), gzip_ok=0,
                   error=type(err).__name__ + ': ' + str(err)[:200])
        counts = {}
    row['utc_finish'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
    out = []
    if row.get('gzip_ok') == 1:
        for (m, t, a), (n, repos, actors) in sorted(counts.items()):
            out.append({'hour': row['hour'], 'marker': m, 'event_type': t, 'action': a, 'events': n,
                        'distinct_repos': len(repos), 'distinct_actors': len(actors)})
    log.update(status=row.get('http_status'), bytes=row.get('bytes', 0), sha256=row.get('sha256', ''),
               error=row.get('error', ''))
    return row, out, log


def read_posts(gate, label):
    out = DATA / ('read-' + label)
    out.mkdir(parents=True, exist_ok=True)
    logp = out / 'read_log.json'
    rows = json.loads(logp.read_text()) if logp.exists() else []
    held = {r['name'] for r in rows if r.get('file')}
    for name, url in POSTS:
        if name in held:
            continue
        row = {'name': name, 'url': url, 'start_utc': datetime.now(timezone.utc).isoformat(timespec='seconds')}
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
                    data = resp.read(POST_CEILING + 1)
                    row.update(finish_utc=datetime.now(timezone.utc).isoformat(timespec='seconds'),
                               status=resp.status, final_url=resp.geturl(),
                               last_modified=resp.headers.get('Last-Modified', ''), bytes=len(data),
                               sha256=sha256(data).hexdigest())
                    if len(data) <= POST_CEILING:
                        red, n = withhold(data)
                        (out / (name + '.raw.gz')).write_bytes(gzip.compress(red, mtime=0))
                        row.update(file=name + '.raw.gz', **n)
            except Exception as err:
                row['error'] = type(err).__name__ + ': ' + str(err)[:300]
        rows.append(row)
        logp.write_text(json.dumps(rows, indent=2) + '\n')
        print(json.dumps({k: row.get(k) for k in ('name', 'status', 'bytes', 'sha256', 'error')}), flush=True)
        time.sleep(PAUSE)


def main():
    ap = argparse.ArgumentParser(description='One LH051 read (studies/LH051/brief.md).')
    ap.add_argument('--read', required=True, help='UTC label, YYYY-MM-DDTHHMMZ')
    ap.add_argument('--to', help='last hour to fetch, YYYY-MM-DD-H (default: the last complete hour)')
    ap.add_argument('--dry-run', action='store_true', help='list the hours and robots.txt decisions; fetch nothing')
    a = ap.parse_args()
    datetime.strptime(a.read, '%Y-%m-%dT%H%MZ')
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    last = min(LAST_HOUR, (now - COMPLETE_AFTER - timedelta(hours=1)).replace(minute=0, second=0, microsecond=0))
    if a.to:
        last = min(last, parse_hour(a.to))
    hours = []
    h = FIRST_HOUR
    while h <= last and len(hours) < MAX_HOURS:
        hours.append(h)
        h += timedelta(hours=1)
    held_rows = read_csv(DATA / 'hours.csv')
    held = {r['hour'] for r in held_rows if r.get('http_status') == '200' and r.get('gzip_ok') == '1'}
    todo = [h for h in hours if label_hour(h) not in held]
    received = sum(int(r.get('bytes') or 0) for r in held_rows)
    gate = RobotsGate(UA)
    if a.dry_run:
        decisions = {}
        for h in todo:
            ok, info = gate.check('https://data.gharchive.org/%s.json.gz' % label_hour(h))
            decisions[info.get('reason', '')] = decisions.get(info.get('reason', ''), 0) + 1
        for name, url in POSTS:
            ok, info = gate.check(url)
            print(json.dumps({'post': name, 'allowed': ok, 'robots': info.get('reason')}))
        print(json.dumps({'dry_run': True, 'brief_committed': brief_committed(), 'hours_in_range': len(hours),
                          'already_held': len(hours) - len(todo), 'to_fetch': len(todo),
                          'first': label_hour(todo[0]) if todo else None, 'last': label_hour(todo[-1]) if todo else None,
                          'robots_decisions': decisions, 'bytes_received_so_far': received,
                          'study_ceiling_bytes': STUDY_CEILING}))
        return
    if not brief_committed():
        sys.exit('brief.md is not committed (or has uncommitted changes): no read before the protocol is fixed')
    DATA.mkdir(parents=True, exist_ok=True)
    for h in todo:
        for _attempt in (1, 2):                # one retry per unavailable hour per read
            if received >= STUDY_CEILING:
                sys.exit('study ceiling of %d bytes reached' % STUDY_CEILING)
            row, counts, log = fetch_hour(gate, h, a.read)
            received += int(row.get('bytes') or 0)
            append_csv(DATA / 'hours.csv', HOUR_FIELDS, [{k: row.get(k, '') for k in HOUR_FIELDS}])
            append_csv(DATA / 'counts.csv', COUNT_FIELDS, counts)
            with (DATA / 'fetch-log.tsv').open('a') as f:
                f.write('\t'.join(str(x) for x in (a.read, row['utc_start'], row['utc_finish'], log['url'],
                                                    log['status'], log['bytes'], log['sha256'], log['robots'],
                                                    log['error'])) + '\n')
            print(json.dumps({'hour': row['hour'], 'status': row.get('http_status'), 'bytes': row.get('bytes'),
                              'gzip_ok': row.get('gzip_ok'), 'gap_hour': row.get('gap_hour', '')}), flush=True)
            time.sleep(PAUSE)
            if row.get('gzip_ok') == 1 or str(row.get('http_status', '')).startswith('not fetched'):
                break
    read_posts(gate, a.read)


if __name__ == '__main__':
    main()
