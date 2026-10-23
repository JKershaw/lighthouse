#!/usr/bin/env python3
"""LH030's fixed classifier. For each retained body it reports, per the brief's classes:
I   names the 23 October issue (CVE-2026-115560, or a session serialise-handler term);
II  carries the instruction (session.upload_progress.enabled set to 0/off, or disabling session upload progress) near an I anchor;
III carries PHP's condition (serialise handler, php_binary or php_serialize) near an I anchor;
IV  states a version scope near an I anchor (one of the 21 October version numbers, "fully patched", or "21 October releases"), snippets kept for a hand reading;
V   links to PHP's notice or to the CVE record.
For the structured records, whose whole body concerns CVE-2026-115560, "near" means anywhere in the record.
Usage: classify.py <read directory> [more read directories]. Prints one JSON line per body and writes classes.json beside each read log."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import sys

WINDOW = 1500
ANCHOR = re.compile(r'CVE-2026-115560|serial[iz]e[_ ]handler', re.I)
INSTRUCTION = re.compile(r'session\.upload_progress\.enabled[\s`\'"]*(=|to|:)?[\s`\'"]*(0|off|false)\b|disabl\w* (the )?session upload progress', re.I)
CONDITION = re.compile(r'serial[iz]e[_ ]handler|php_binary|php_serialize', re.I)
SCOPE = re.compile(r'8\.5\.12|8\.4\.27|8\.3\.36|8\.2\.35|fully[- ]patched|(21|twenty-first) October releases|October 21(st)? releases', re.I)
LINK = re.compile(r'php\.net/archive/2026\.php#2026-10-23|news-web\.php\.net/php\.announce|CVE-2026-115560', re.I)


class Visible(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip, self.chunks, self.hrefs = 0, [], []

    def handle_starttag(self, tag, attrs):
        self.skip += tag in ('script', 'style', 'svg')
        self.hrefs += [v for k, v in attrs if k == 'href' and v]

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'svg') and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        data = re.sub(r'\s+', ' ', data).strip()
        if data and not self.skip:
            self.chunks.append(data)


def strings(value):
    if isinstance(value, dict):
        return [s for v in value.values() for s in strings(v)]
    if isinstance(value, list):
        return [s for v in value for s in strings(v)]
    return [str(value)] if isinstance(value, str) else []


def text_and_links(raw, content_type):
    if 'json' in content_type:
        try:
            values = strings(json.loads(raw))
            return '\n'.join(values), [v for v in values if v.startswith('http')]
        except ValueError:
            pass
    parser = Visible()
    parser.feed(raw)
    return '\n'.join(parser.chunks), parser.hrefs


def near(pattern, text, anchors, whole):
    hits = []
    for match in pattern.finditer(text):
        if whole or any(abs(match.start() - a) <= WINDOW for a in anchors):
            hits.append(text[max(0, match.start() - 120):match.end() + 120].replace('\n', ' '))
    return hits


def classify(read_dir):
    out = []
    for row in json.loads((read_dir / 'read_log.json').read_text()):
        result = {k: row.get(k) for k in ('group', 'source', 'name', 'status', 'bytes', 'sha256')}
        if 'file' not in row or row.get('status') != 200 or row.get('bytes', 0) < 1000:
            result['access'] = 'unavailable'
            out.append(result)
            continue
        raw = (read_dir / row['file']).read_text(encoding='utf-8', errors='replace')
        text, links = text_and_links(raw, row.get('content_type', ''))
        whole = row['group'] == 'records' and 'CVE-2026-115560' in text
        anchors = [m.start() for m in ANCHOR.finditer(text)]
        result.update(access='read', I=bool(anchors) or whole,
                      II=near(INSTRUCTION, text, anchors, whole), III=near(CONDITION, text, anchors, whole),
                      IV=near(SCOPE, text, anchors, whole), V=sorted({l for l in links if LINK.search(l)}))
        for key in ('II', 'III', 'IV'):
            result[key + '_yes'] = bool(result[key])
        out.append(result)
    (read_dir / 'classes.json').write_text(json.dumps(out, indent=2) + '\n')
    return out


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        for result in classify(Path(arg)):
            print(json.dumps({k: result.get(k) for k in ('name', 'access', 'I', 'II_yes', 'III_yes', 'IV_yes', 'V')}))
