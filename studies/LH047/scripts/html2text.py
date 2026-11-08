"""Crude HTML to text for reading retained pages: drops script/style, tags, collapses space.
Usage: python3 -I studies/LH047/scripts/html2text.py <in> <out>"""
import html, re, sys
b = open(sys.argv[1], 'rb').read().decode('utf-8', 'replace')
b = re.sub(r'(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>', ' ', b)
b = re.sub(r'(?i)<br\s*/?>|</(p|div|h[1-6]|li|tr|pre|section|article)>', '\n', b)
b = re.sub(r'(?s)<[^>]+>', ' ', b)
b = html.unescape(b)
b = re.sub(r'[ \t\r\f\v]+', ' ', b)
b = re.sub(r'\n\s*\n+', '\n', b)
open(sys.argv[2], 'w').write(b.strip() + '\n')
