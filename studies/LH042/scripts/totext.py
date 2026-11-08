#!/usr/bin/env python3
"""LH042: plain text of a saved HTML body (used by the quote check and for reading).
Usage: python3 -I totext.py <body> [<out.txt>]"""
import html, re, sys

def text_of(raw: bytes) -> str:
    s = raw.decode("utf-8", "replace")
    s = re.sub(r"(?is)<(script|style|noscript|svg)\b.*?</\1>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h[1-6]|tr|td|th|section|article|figcaption|caption)>", "\n", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html.unescape(s)
    s = s.replace(" ", " ").replace(" ", " ")
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip()

if __name__ == "__main__":
    t = text_of(open(sys.argv[1], "rb").read())
    if len(sys.argv) > 2:
        open(sys.argv[2], "w").write(t)
    else:
        print(t)
