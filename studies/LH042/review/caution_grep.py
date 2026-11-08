#!/usr/bin/env python3
"""LH042 evidence review: grep everything retained under studies/LH042 (working tree)
for what the keeper's caution withholds. Prints counts only, never the matches.
- IPv4 addresses (any dotted quad, then excluding version-number-like contexts is NOT done:
  every hit is listed by file with its 30-character left context's class only)
- IPv6-like addresses in raw bytes
- email addresses, in plain, JSON-escaped and URL-encoded forms (a wider pattern than
  scripts/redact_emails.py: also '&#64;' and ' [at] ' obfuscations)
- long key-like tokens (sk-..., AKIA..., 32+ hex or base64url runs beside 'key'/'token')
- URL-encoded credential headers (Api-Key%3A%20..., added after the first run found one)
- the Synthient body's redaction marker
Usage: python3 -I studies/LH042/review/caution_grep.py"""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
IPV4 = re.compile(rb"(?<![\d.])(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)(?![\d.])")
IPV6 = re.compile(rb"(?<![0-9A-Fa-f:])(?:[0-9A-Fa-f]{1,4}:){4,7}[0-9A-Fa-f]{1,4}(?![0-9A-Fa-f:])")
EM = [re.compile(rb"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"),
      re.compile(rb"[A-Za-z0-9._%+-]+(?:\\u0040|%40|&#64;|&#x40;)[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}", re.I),
      re.compile(rb"[A-Za-z0-9._%+-]+\s?\[at\]\s?[A-Za-z0-9-]+\s?(?:\[dot\]|\.)\s?[A-Za-z]{2,}", re.I)]
KEY = [re.compile(rb"\bsk-[A-Za-z0-9_-]{20,}"), re.compile(rb"\bAKIA[0-9A-Z]{16}\b"),
       re.compile(rb"(?i)(?:api[_-]?key|apikey|token|secret)[\"'\s:=]{1,6}[\"']?[A-Za-z0-9_\-]{24,}")]
# URL-encoded request headers carrying a credential (as in a code block's copy attribute)
ENC = re.compile(rb"(?i)(?:api-key|x-api-key|authorization)%3A%20(?!%5Bredacted)[A-Za-z0-9%._+/-]{8,}")
tot = {"ipv4": 0, "ipv6": 0, "email": 0, "key": 0}
for p in sorted(ROOT.rglob("*")):
    if not p.is_file() or "__pycache__" in p.parts or p.suffix == ".png":
        continue
    b = p.read_bytes()
    v4 = IPV4.findall(b)
    # keep only dotted quads that are not obviously version strings inside asset URLs
    v6 = IPV6.findall(b)
    em = sum(len(r.findall(b)) for r in EM)
    ky = sum(len(r.findall(b)) for r in KEY)
    enc = len(ENC.findall(b))
    if enc:
        print(f"{p.relative_to(ROOT)}: URL-ENCODED CREDENTIAL HEADER VALUES={enc}")
    if v4 or v6 or em or ky:
        print(f"{p.relative_to(ROOT)}: ipv4-shaped={len(v4)} ipv6-shaped={len(v6)} email={em} keylike={ky}")
    tot["ipv4"] += len(v4); tot["ipv6"] += len(v6); tot["email"] += em; tot["key"] += ky
print("totals:", tot)
s = (ROOT / "data/round1-2026-11-08/034.body").read_bytes()
print("Synthient body: '[redacted-by-Lighthouse]' occurrences:", s.count(b"[redacted-by-Lighthouse]"))
