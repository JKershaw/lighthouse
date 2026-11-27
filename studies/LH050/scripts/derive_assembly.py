# Replaces LH050's kept copies of Assembly's page (PA-S26, reads LH050-R029 of 13 November and LH050-R042 of
# 19 November 2026) with derived files, under the keeper's decision of 21 November 2026
# (notes/keeper/2026-11-21-robots-intent.md): assemblymag.com's robots.txt refuses an AI-training crawler
# (meta-externalagent) on this path, so Lighthouse keeps no body of the page. Written 27 November 2026 (row
# LH050-policy-final, run 2026-11-27T141100Z-anthropic-watch) by Claude Opus under Claude Code.
#
# Run from the repository root, with the bodies still present:
#   python3 -I studies/LH050/scripts/derive_assembly.py
# It extracts the facts the record uses (title, standfirst, dates, the passages claims LH050-C022, C031 and C032
# quote, and a SHA-256 of the article's visible text for later weekly comparisons), checks each quote is in the
# page, and writes bodies/S26_assemblymag.derived.json beside each body through lh_fetch.write_derived. It does
# not delete anything; the bodies are removed by hand only after it succeeds. No network access.
import hashlib, html, json, os, re, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "scripts"))
from lh_fetch import write_derived  # noqa: E402

URL = "https://www.assemblymag.com/articles/99717-start-up-aims-to-make-humanoid-robots-for-military"
REASON = "meta-externalagent (a training or archiving crawler) is refused at this path"
READS = [  # read_id, label, read time, received sha256, http status, received bytes (from reads.csv and fetch_log.jsonl)
    ("LH050-R029", "2026-11-13T1454Z", "2026-11-13T14:58:02Z"),
    ("LH050-R042", "2026-11-19T1417Z", "2026-11-19T14:17:44Z"),
]
QUOTES = {  # short attributed passages the ledger uses, as the page has them
    "LH050-C022": ["is designed to carry a maximum payload of 44 pounds, including lethal weaponry",
                   "Pretending that you don’t need to weaponize robots...sounds virtuous on face value, but it really isn’t"],
    "LH050-C031": ["Foundation’s business model is to lease the robots, rather than sell them"],
    "LH050-C032": ["The company plans to build 40 robots this year, 10,000 in 2026, and 40,000 in 2027"],
}
START, END = "SAN FRANCISCO", "efficiency of electric motors."


def visible_lines(raw):
    s = re.sub(r"(?is)<(script|style).*?</\1>", "", raw)
    s = re.sub(r"(?s)<!--.*?-->", "", s)
    s = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h\d|tr|a)>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    return [l.strip() for l in html.unescape(s).splitlines() if l.strip()]


def fetch_log_entry(label):
    with open(os.path.join(REPO, "studies/LH050/data", label, "fetch_log.jsonl")) as fh:
        for line in fh:
            rec = json.loads(line)
            if rec.get("source_id") == "PA-S26":
                return rec
    raise SystemExit("no PA-S26 line in %s fetch log" % label)


for read_id, label, read_at in READS:
    d = os.path.join(REPO, "studies/LH050/data", label, "bodies")
    body_path = os.path.join(d, "S26_assemblymag.html")
    raw_bytes = open(body_path, "rb").read()
    raw = raw_bytes.decode("utf-8", errors="replace")
    lines = visible_lines(raw)
    i = next(n for n, l in enumerate(lines) if l.startswith(START))
    j = next(n for n, l in enumerate(lines) if l.endswith(END))
    article = "\n".join(lines[i:j + 1])
    joined = " ".join(lines[i:j + 1])
    for cid, qs in QUOTES.items():
        for q in qs:
            assert q in joined, (read_id, cid, q)
    title = lines[lines.index("Start-up Aims to Make Humanoid Robots for Military")]
    standfirst = lines[lines.index(title) + 1]
    date_shown = lines[i - 1]
    pub = re.search(r'"datePublished":"([^"]+)"', raw).group(1)
    mod = re.search(r'"dateModified":"([^"]+)"', raw).group(1)
    log = fetch_log_entry(label)
    extracted = {
        "title": title,
        "standfirst": standfirst,
        "date_shown": date_shown,
        "datePublished": pub,
        "dateModified": mod,
        "quotes_used": QUOTES,
        "article_text_sha256": hashlib.sha256(article.encode("utf-8")).hexdigest(),
        "article_text_rule": "SHA-256 of the page's visible text lines (scripts, styles, comments and tags removed; lines stripped; "
                             "blank lines dropped; joined with newlines) from the line starting 'SAN FRANCISCO' to the line ending "
                             "'efficiency of electric motors.', as computed by this script",
        "article_paragraph_count_lines": j - i + 1,
    }
    meta = {
        "read_id": read_id,
        "read_utc": read_at,
        "http_status": log.get("status", log.get("http_status")),
        "bytes_received": log.get("received_bytes", log.get("bytes")),
        "sha256_received": log.get("received_sha256"),
        "sha256_copy_kept_until_2026_11_27": hashlib.sha256(raw_bytes).hexdigest(),
        "used_for": ("Claims LH050-C022, C031 and C032 (and C026 and C034, which list the page among those read) and the "
                     "case_matrix.csv rows citing LH050-R029; the baseline for the 19 November comparison." if read_id == "LH050-R029"
                     else "The weekly comparison of 19 November with LH050-R029 (checkpoints/2026-11-19-read.md) and the previous "
                          "readable copy for the 26 November comparison (checkpoints/2026-11-26-read.md)."),
        "removed": "27 November 2026; the copy is in git history before the removal commit (studies/LH050/data/REMOVED.md)",
    }
    out = os.path.join(d, "S26_assemblymag.derived.json")
    write_derived(out, URL, REASON, extracted, **meta)
    print(read_id, out, extracted["article_text_sha256"], meta["sha256_copy_kept_until_2026_11_27"])
