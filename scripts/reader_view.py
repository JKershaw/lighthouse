#!/usr/bin/env python3
"""A text-only reader's view of the built site, for reader-task tests.

Usage: python3 -I scripts/reader_view.py <site dir> <url path>
       e.g. python3 -I scripts/reader_view.py site/_site /investigations/

Prints what a reader would see on the page, in order: headings marked with #,
paragraphs and list items as text, and each link as [n] with its target listed
at the end, so an agent can "click" by calling the script again with that
target. Scripts, styles and hidden elements are left out. Only pages inside the
site directory are read; nothing is fetched from the network.
"""
import html.parser
import os
import sys

SKIP = {"script", "style", "template", "noscript", "svg"}
BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "dt", "dd", "tr", "figcaption", "summary", "blockquote", "pre", "header", "footer", "nav", "section", "article", "aside", "main", "div", "ul", "ol", "dl", "table", "details", "figure"}


class View(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.line, self.links, self.skip, self.href, self.hidden = [], [], [], 0, None, 0
        self.stack = []

    def flush(self):
        text = " ".join("".join(self.line).split())
        if text and text != "-":
            self.out.append(text)
        self.line = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        hidden = "hidden" in a or a.get("aria-hidden") == "true"
        self.stack.append((tag, hidden))
        if hidden:
            self.hidden += 1
        if tag in SKIP:
            self.skip += 1
        if tag in BLOCK:
            self.flush()
            if tag[0] == "h" and tag[1:].isdigit():
                self.line.append("#" * int(tag[1:]) + " ")
            elif tag == "li":
                self.line.append("- ")
        if tag == "a" and a.get("href"):
            self.href = a["href"]
        if tag == "img" and a.get("alt") and not self.skip and not self.hidden:
            self.line.append(f"[image: {a['alt']}] ")
        if tag == "br":
            self.flush()

    def handle_endtag(self, tag):
        while self.stack:
            t, hidden = self.stack.pop()
            if hidden:
                self.hidden -= 1
            if t in SKIP:
                self.skip -= 1
            if t == "a" and self.href is not None:
                self.links.append(self.href)
                self.line.append(f" [{len(self.links)}]")
                self.href = None
            if t in BLOCK:
                self.flush()
            if t == tag:
                break

    def handle_data(self, data):
        if not self.skip and not self.hidden:
            self.line.append(data)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    root = os.path.realpath(sys.argv[1])
    url = sys.argv[2].split("#")[0].split("?")[0] or "/"
    rel = url.lstrip("/")
    path = os.path.realpath(os.path.join(root, rel))
    if os.path.isdir(path):
        path = os.path.join(path, "index.html")
    elif not path.endswith(".html") and os.path.isfile(path + "/index.html"):
        path += "/index.html"
    if not path.startswith(root + os.sep) or not os.path.isfile(path):
        sys.exit(f"no page at {url}")
    if not path.endswith(".html"):
        print(f"{url} is a file, not a page ({os.path.getsize(path)} bytes).")
        return
    v = View()
    v.feed(open(path, encoding="utf-8", errors="replace").read())
    v.flush()
    print(f"PAGE {url}\n")
    print("\n".join(v.out))
    print("\nLINKS")
    for i, href in enumerate(v.links, 1):
        print(f"[{i}] {href}")


if __name__ == "__main__":
    main()
