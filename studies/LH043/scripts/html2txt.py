"""Convert retained HTML pages to plain text for reading. Usage: python3 -I html2txt.py in.html out.txt"""
import html, re, sys
t = open(sys.argv[1], encoding="utf-8", errors="replace").read()
t = re.sub(r"(?is)<script.*?</script>|<style.*?</style>|<svg.*?</svg>", "", t)
t = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</h\d>|</div>", "\n", t)
t = re.sub(r"<[^>]+>", " ", t)
t = html.unescape(t)
lines = [re.sub(r"[ \t]+", " ", l).strip() for l in t.splitlines()]
open(sys.argv[2], "w", encoding="utf-8").write("\n".join(l for l in lines if l))
