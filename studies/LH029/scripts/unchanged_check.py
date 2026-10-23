#!/usr/bin/env python3
"""For the reader update's 'Unchanged' line: compare OpenAI's extracted visible text and Amazon's body across LH028's retained snapshots."""
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import re

LH028 = Path(__file__).resolve().parents[2] / 'LH028' / 'data'


class Visible(HTMLParser):
    """Ordered text chunks outside script, style and svg, whitespace normalised, as LH028's checkpoints compare them."""
    def __init__(self):
        super().__init__()
        self.skip, self.chunks = 0, []

    def handle_starttag(self, tag, attrs):
        self.skip += tag in ('script', 'style', 'svg')

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'svg') and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        data = re.sub(r'\s+', ' ', data).strip()
        if data and not self.skip:
            self.chunks.append(data)


for snap in sorted(LH028.glob('snapshot-*')):
    parser = Visible()
    parser.feed((snap / 'openai.raw').read_text(encoding='utf-8', errors='replace'))
    text = sha256('\n'.join(parser.chunks).encode()).hexdigest()[:16]
    amazon = (snap / 'amazon.raw').read_bytes()
    print(snap.name, 'openai visible-text', text, len(parser.chunks), 'chunks | amazon', len(amazon), 'bytes', sha256(amazon).hexdigest()[:16])
