#!/usr/bin/env python3
"""R-0032 reviewer's independent re-extraction, kept with its output (extract_check.txt).

Uses html.parser rather than LH029's regular expressions. Reads only retained bytes:
PHP's archive page as retained by LH029 (23 Oct 17:00 UTC) and LH024 (22 Oct 06:24 UTC),
and Cloudflare's page as retained by LH028 at six slots.
"""
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import difflib
import re
import sys

REPO = Path(__file__).resolve().parents[3]
NEW = REPO / 'studies/LH029/data/snapshot-2026-10-23/archive.raw'
OLD = REPO / 'studies/LH024/data/snapshot-2026-10-22/php_0.raw'
LH028 = REPO / 'studies/LH028/data'


class Articles(HTMLParser):
    """Collect each <article class="newsItem"> as {id, datetime, heading, text, links}."""
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.items = []
        self.cur = None
        self.in_header = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'article' and 'newsItem' in (a.get('class') or ''):
            self.depth = 1
            self.cur = {'id': '', 'datetime': '', 'text': [], 'links': [], 'header_links': []}
            return
        if not self.cur:
            return
        if tag == 'article':
            self.depth += 1
        if tag == 'header':
            self.in_header = True
        if tag == 'a':
            if a.get('id') and not self.cur['id']:
                self.cur['id'] = a['id']
            if a.get('href'):
                (self.cur['header_links'] if self.in_header else self.cur['links']).append(a['href'])
        if tag == 'time' and a.get('datetime'):
            self.cur['datetime'] = a['datetime']

    def handle_endtag(self, tag):
        if not self.cur:
            return
        if tag == 'header':
            self.in_header = False
        if tag == 'article':
            self.depth -= 1
            if self.depth == 0:
                self.cur['text'] = re.sub(r'\s+', ' ', ' '.join(self.cur['text'])).strip()
                self.items.append(self.cur)
                self.cur = None

    def handle_data(self, data):
        if self.cur:
            self.cur['text'].append(data)


class Visible(HTMLParser):
    """Visible text chunks outside script/style/svg, plus meta tags."""
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.chunks = []
        self.meta = {}
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('script', 'style', 'svg'):
            self.skip += 1
        if tag == 'meta' and (a.get('property') or a.get('name')):
            self.meta[a.get('property') or a.get('name')] = a.get('content', '')
        if tag == 'a' and a.get('href'):
            self.hrefs.append(a['href'])

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'svg') and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        d = re.sub(r'\s+', ' ', data).strip()
        if d and not self.skip:
            self.chunks.append(d)


def parse_articles(path):
    p = Articles()
    p.feed(path.read_text(encoding='utf-8'))
    return {i['id']: i for i in p.items}


def visible(path):
    p = Visible()
    p.feed(path.read_text(encoding='utf-8', errors='replace'))
    return p


out = []
P = out.append

for label, path in (('LH029 23 Oct archive.raw', NEW), ('LH024 22 Oct php_0.raw', OLD)):
    b = path.read_bytes()
    P(f'{label}: {len(b)} bytes sha256 {sha256(b).hexdigest()}')

new, old = parse_articles(NEW), parse_articles(OLD)
P(f'\nentries parsed: 23 Oct copy {len(new)}, 22 Oct copy {len(old)}')
e = new.get('2026-10-23-1')
P('\n== entry 2026-10-23-1 in 23 Oct copy ==')
if e:
    P('datetime attribute: ' + e['datetime'])
    P('header links: ' + repr(e['header_links']))
    P('body links: ' + repr(e['links']))
    P('text: ' + e['text'])
    stored = (REPO / 'studies/LH029/data/entry-2026-10-23-1.txt').read_text().strip()
    P('matches LH029 stored extraction: ' + str(e['text'] == stored))
    # also show the raw HTML of the entry for a byte-level look
    raw = NEW.read_text(encoding='utf-8')
    i = raw.find('id="2026-10-23-1"')
    j = raw.find('</article>', i)
    k = raw.rfind('<article', 0, i)
    P('raw HTML of the entry:\n' + raw[k:j + len('</article>')])
else:
    P('ENTRY ABSENT')

P('\n== presence checks in the 22 Oct copy ==')
oldraw = OLD.read_bytes()
for needle in (b'2026-10-23-1', b'115560', b'Informational advisory', b'upload_progress', b'serialize_handler', b'2026-10-21-6', b'RC4', b'remirepo'):
    P(f'{needle.decode()!r}: {oldraw.count(needle)} occurrence(s)')
newraw = NEW.read_bytes()
P('\n== presence checks in the 23 Oct copy ==')
for needle in (b'2026-10-23-1', b'115560', b'upload_progress', b'serialize_handler', b'2026-10-21-6', b'RC4', b'remirepo', b'8.5.12', b'8.4.27', b'8.3.36', b'8.2.35'):
    P(f'{needle.decode()!r}: {newraw.count(needle)} occurrence(s)')

P('\n== entries dated 21 Oct or later, both copies (id, datetime) ==')
for key in sorted(set(new) | set(old)):
    if key >= '2026-10-20':
        P(f'{key}: 23Oct={new.get(key, {}).get("datetime", "ABSENT")} 22Oct={old.get(key, {}).get("datetime", "ABSENT")}')

P('\n== 21 Oct security advisory entry (2026-10-21-5): sentences mentioning upload_progress, in each copy ==')
for label, d in (('22 Oct', old), ('23 Oct', new)):
    t = d['2026-10-21-5']['text']
    for s in re.split(r'(?<=[.!?]) ', t):
        if 'upload_progress' in s or 'confirmed session' in s or 'reduce' in s.lower() or 'not make' in s.lower():
            P(f'[{label}] {s}')
P('\nsentence-level diff of 2026-10-21-5 between copies:')
a = re.split(r'(?<=[.!?]) ', old['2026-10-21-5']['text'])
b = re.split(r'(?<=[.!?]) ', new['2026-10-21-5']['text'])
for line in difflib.unified_diff(a, b, 'old', 'new', lineterm='', n=0):
    P(line)

P('\n== Cloudflare retained copies: modified_time and key sentences ==')
cf = {}
for snap in sorted(LH028.glob('snapshot-*')):
    f = snap / 'cloudflare.raw'
    v = visible(f)
    cf[snap.name] = v
    P(f'\n[{snap.name}] bytes={f.stat().st_size} sha256={sha256(f.read_bytes()).hexdigest()}')
    P('  article:modified_time=' + v.meta.get('article:modified_time', '?') + '  article:published_time=' + v.meta.get('article:published_time', '?'))
    P('  links to php.net archive: ' + repr([h for h in v.hrefs if 'php.net/archive' in h]))
    for c in v.chunks:
        if any(k in c for k in ('115560', 'upload progress', 'upload_progress', 'fully patched', 'all plans', 'Managed Response', 'Free', '8.5.12', 'informational')):
            P('  > ' + c)

P('\n== visible-text diff Cloudflare 2026-10-22T1600Z -> 2026-10-22T2200Z ==')
for line in difflib.unified_diff(cf['snapshot-2026-10-22T1600Z'].chunks, cf['snapshot-2026-10-22T2200Z'].chunks, '1600Z', '2200Z', lineterm='', n=0):
    P(line)
P('\n== visible-text diff Cloudflare 2026-10-23T1000Z -> 2026-10-23T1600Z ==')
for line in difflib.unified_diff(cf['snapshot-2026-10-23T1000Z'].chunks, cf['snapshot-2026-10-23T1600Z'].chunks, '1000Z', '1600Z', lineterm='', n=0):
    P(line)

text = '\n'.join(out)
(Path(__file__).with_name('extract_check.txt')).write_text(text + '\n')
print(text)
