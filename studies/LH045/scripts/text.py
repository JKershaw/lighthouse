#!/usr/bin/env python3
"""Print the visible text of a kept HTML body (scripts and styles removed). Usage: python3 -I text.py <file> [start] [length]"""
import gzip, html, re, sys
b = open(sys.argv[1], "rb").read()
if b[:2] == b"\x1f\x8b":
    b = gzip.decompress(b)
s = b.decode("utf-8", errors="replace")
t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S | re.I)
t = html.unescape(re.sub(r"<[^>]+>", " ", t)); t = re.sub(r"\s+", " ", t)
a = int(sys.argv[2]) if len(sys.argv) > 2 else 0; n = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
print(len(t)); print(t[a:a + n])
