"""Withhold email addresses inside LH041's gzipped retained files (the keeper, 8 November 2026).

    python3 -I studies/LH041/scripts/redact_gz.py studies/LH041/data

scripts/redact_emails.py skips .gz files; this decompresses each one, applies its
redact_bytes, and recompresses with a fixed mtime, printing a line per file changed.
Fetch logs keep the sha256 of the bytes as received.
"""
import gzip, hashlib, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from redact_emails import redact_bytes  # noqa: E402

for top in sys.argv[1:]:
    for d, _, fs in os.walk(top):
        for f in sorted(fs):
            if not f.endswith(".gz"):
                continue
            p = os.path.join(d, f)
            raw = gzip.decompress(open(p, "rb").read())
            red, n = redact_bytes(raw)
            if n:
                with open(p, "wb") as out:
                    out.write(gzip.compress(red, compresslevel=9, mtime=0))
                print("%s\t%d replaced\tsha256 (uncompressed) before %s\tafter %s" % (
                    p, n, hashlib.sha256(raw).hexdigest(), hashlib.sha256(red).hexdigest()))
