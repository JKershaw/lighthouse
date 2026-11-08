"""Plain text from a retained HTML page, for reading only (stdlib)."""
import sys, html.parser, re, gzip

class P(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.out = []; self.skip = 0
    def handle_starttag(self, t, a):
        if t in ("script", "style", "noscript", "svg"): self.skip += 1
        if t in ("p", "br", "li", "h1", "h2", "h3", "h4", "tr", "div", "pre", "code"): self.out.append("\n")
    def handle_endtag(self, t):
        if t in ("script", "style", "noscript", "svg") and self.skip: self.skip -= 1
    def handle_data(self, d):
        if not self.skip: self.out.append(d)

opener = gzip.open if sys.argv[1].endswith(".gz") else open
p = P(); p.feed(opener(sys.argv[1], "rt", encoding="utf-8", errors="replace").read())
txt = re.sub(r"\n\s*\n+", "\n\n", "".join(p.out))
print(re.sub(r"[ \t]+", " ", txt))
