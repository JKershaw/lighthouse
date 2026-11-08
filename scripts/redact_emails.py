"""Replace email addresses in retained text files with a placeholder.

The keeper, 8 November 2026: "Let's redact the email addresses. Feels polite,
and we've not much need to share them." Lighthouse keeps sources as received,
except that email addresses are withheld; a fetch log's sha256 stays the hash
of the bytes received, so a replay that refetches can still compare.

Usage:
  python3 -I scripts/redact_emails.py <dir-or-file>...   redact in place, print a log line per file changed
Import:
  from redact_emails import redact_bytes                 for collectors, before writing a body
Binary files (PDF, ZIP, images, gzip) are skipped; their text conversions are redacted.
"""
import hashlib, os, re, sys

PLACEHOLDER = b"[email withheld by Lighthouse]"
EMAIL = re.compile(rb"(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}(?![A-Za-z0-9-])")
# also the JSON-escaped and URL-encoded forms of "@"
EMAIL_ENC = re.compile(rb"[A-Za-z0-9._%+-]+(?:\\u0040|%40)[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
BINARY_EXT = {".pdf", ".zip", ".gz", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".woff", ".woff2", ".parquet"}


def redact_bytes(b):
    """Return (redacted bytes, number of addresses replaced)."""
    b, n1 = EMAIL.subn(PLACEHOLDER, b)
    b, n2 = EMAIL_ENC.subn(PLACEHOLDER, b)
    return b, n1 + n2


def is_binary(path, head):
    return os.path.splitext(path)[1].lower() in BINARY_EXT or b"\x00" in head


def redact_path(path):
    with open(path, "rb") as f:
        b = f.read()
    if is_binary(path, b[:4096]):
        return None
    r, n = redact_bytes(b)
    if n:
        with open(path, "wb") as f:
            f.write(r)
        return n, hashlib.sha256(b).hexdigest(), hashlib.sha256(r).hexdigest()
    return None


def main(args):
    for a in args:
        paths = [a] if os.path.isfile(a) else [os.path.join(d, f) for d, _, fs in os.walk(a) for f in fs]
        for p in sorted(paths):
            res = redact_path(p)
            if res:
                print("%s\t%d replaced\tsha256 before %s\tafter %s" % (p, *res))


if __name__ == "__main__":
    main(sys.argv[1:])
