Recheck of 8 November 2026 (notes/R-0060-what-the-watch-would-see-recheck.md).

fetch-log.tsv: every request made for the recheck, with UTC time, HTTP status, bytes and sha256 prefix
(hashes are of the bytes as received, before email redaction).
data/: the sources as received, read as text only; emails withheld by scripts/redact_emails.py.
Not kept here because byte-identical copies (same sha256) are already retained in studies/LH043/data/sources/:
  aisi.html                    = aisi-incident-blog.html
  aisi-INC-2026-07-28-01.pdf   = aisi-INC-2026-07-28-01.pdf
  metr.html                    = metr-hf-investigation.html (after email redaction)
  anthropic-incidents.html     = anthropic-three-incidents.html (after email redaction)
The HTML and PDF were converted to text with a short standard-library HTML parser and pdftotext -layout;
the text was read, not executed. The OSV record was compared with the claims check's copy
(claims-check/osv-MAL-2026-2144.json): identical apart from key order and one withheld email.
