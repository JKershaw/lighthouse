#!/usr/bin/env python3
"""Evidence review R-0043: check each retained page's SHA-256 against read_log.json and
write a plain-text rendering of it (tags stripped, entities decoded) beside this script."""
import hashlib, html, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
log = json.loads((ROOT / 'read_log.json').read_text())
for row in log:
    if 'file' not in row:
        print(f"{row['source']}: not retained, logged sha256 {row['sha256'][:16]}..")
        continue
    raw = (ROOT / row['file']).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    print(f"{row['source']}: {len(raw)} bytes, sha256 {'matches' if digest == row['sha256'] else 'DIFFERS'}")
    text = raw.decode('utf-8', 'replace')
    text = re.sub(r'(?is)<(script|style|noscript|svg)\b.*?</\1>', ' ', text)
    text = re.sub(r'(?i)<br\s*/?>|</(p|div|li|h[1-6]|tr|td|th|section|article|header|footer)>', '\n', text)
    text = re.sub(r'(?s)<[^>]+>', ' ', text)
    text = html.unescape(text)
    text = re.sub(r'[ \t\xa0]+', ' ', text)
    text = re.sub(r'\n\s*\n+', '\n', text)
    (HERE / (row['source'] + '.txt')).write_text(text.strip() + '\n')
