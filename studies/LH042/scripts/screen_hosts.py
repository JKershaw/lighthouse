#!/usr/bin/env python3
"""LH042: screen retained bodies for addresses or hostnames of exposed systems.

Usage: python3 -I screen_hosts.py <data dir> [...]
Prints, per body, the count of IPv4 addresses left (should be 0 after fetch.py),
IPv6-like addresses, and hostnames that appear in the page's visible text
(not in markup or links) outside a small allowlist of page furniture. The output
is read by a person, who removes any list of exposed hosts and logs it in
data/SCREENING.md."""
import pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from totext import text_of

IPV4 = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
IPV6 = re.compile(r"(?<![0-9A-Fa-f:])(?:[0-9A-Fa-f]{1,4}:){3,7}[0-9A-Fa-f]{1,4}(?![0-9A-Fa-f:])")
HOST = re.compile(r"\b(?:[a-z0-9-]+\.){2,}(?:com|net|org|io|cn|de|br|ru|jp|kr|fr|uk|ai|cloud|xyz|info|dev|app)\b", re.I)

for d in sys.argv[1:]:
    for b in sorted(pathlib.Path(d).glob("*.body")):
        raw = b.read_bytes()
        t = text_of(raw)
        v4 = IPV4.findall(raw.decode("utf-8", "replace"))
        v6 = IPV6.findall(t)
        hosts = sorted(set(h.lower() for h in HOST.findall(t)))
        print(f"{b}: ipv4={len(v4)} ipv6_in_text={len(v6)} hostnames_in_text={len(hosts)}")
        for h in hosts[:40]:
            print("   ", h)
        for x in v6[:10]:
            print("    v6", x)
