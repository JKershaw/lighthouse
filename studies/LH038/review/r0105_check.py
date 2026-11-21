"""R-0105 (21 November 2026): independent recomputation of LH038 v0.4's SUSE classing from retained bodies.
Replay from the repository root: python3 -I studies/LH038/review/r0105_check.py > studies/LH038/review/r0105_check_output.txt"""
import gzip, re, json, sys, os, csv
from datetime import datetime, timedelta, timezone, date
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
D = os.path.join(ROOT, "studies/LH038/data/suse-clocks-2026-11-21T1420Z")
R17 = os.path.join(ROOT, "studies/LH038/data/read-2026-11-17T1419Z")
CVEP = os.path.join(ROOT, "studies/LH036/data/read-2026-11-16T1419Z/suse.raw.gz")
IDS = ["24386","24422","24437","24446","24479","24480","24481","24482","24483","24484","24485","24486"]
g = lambda p: gzip.open(p).read().decode("utf-8", "replace")
MON = {m:i+1 for i,m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}
# month indexes
idx = g(os.path.join(D,"month-2026-10.raw.gz")) + g(os.path.join(D,"month-2026-11.raw.gz"))
for m in ("10","11"):
    t = g(os.path.join(D,f"month-2026-{m}.raw.gz"))
    print(m, "messages:", re.search(r"<b>Messages:</b>\s*(\d+)", t).group(1), "LI:", t.count("<LI>"),
          "start/end:", re.findall(r"<i>(\w{3} \w{3}\s+\d+ [\d:]+ UTC 2026)</i>", t))
# CVE page stamps (CET; 29 Oct and 3 Nov 2026 are after the end of CEST on 25 Oct, so UTC+1)
cp = g(CVEP)
stamps = {}
for i in IDS:
    m = re.search(rf"SUSE-SU-2026:{i}-1</a>, published (\w{{3}}) (\w{{3}})\s+(\d+) (\d\d):(\d\d):(\d\d) (\w+) 2026", cp)
    assert m and m.group(7) == "CET", (i, m and m.group(7))
    local = datetime(2026, MON[m.group(2)], int(m.group(3)), int(m.group(4)), int(m.group(5)), int(m.group(6)))
    stamps[i] = (local - timedelta(hours=1)).replace(tzinfo=timezone.utc), local.date()
allst = re.findall(r"SUSE-SU-\d{4}:\d+-\d+</a>, published \w{3} (\w{3})\s+(\d+) [\d:]+ \w+ (\d{4})", cp)
earliest = min(date(int(y), MON[mo], int(d_)) for mo, d_, y in allst)
print("CVE page announcements:", len(allst), "earliest stamp date (local):", earliest)
POST = date(2026,10,27)
rows = []
for i in IDS:
    n = len(re.findall(rf">SUSE-SU-2026:{i}-1:", idx))
    msg = g(os.path.join(D, f"msg-{i}.raw.gz"))
    dates = re.findall(r"<I>(\w{3}) (\w{3})\s+(\d+) (\d\d):(\d\d):(\d\d) (\w+) (\d{4})</I>", msg)
    assert len(dates) == 1 and dates[0][6] == "UTC", (i, dates)
    _, mo, d_, H, M, S, _, Y = dates[0]
    lm = datetime(int(Y), MON[mo], int(d_), int(H), int(M), int(S), tzinfo=timezone.utc)
    # Message-ID timestamp (Python make_msgid: int(time*100)) as a cross-check
    mid = re.search(r"In-Reply-To=%3C(\d+)\.", msg).group(1)
    midt = datetime.fromtimestamp(int(mid)/100, timezone.utc)
    rd_msg = re.search(r"Release Date: (\S+)", msg).group(1)
    xref = msg.split("Cross-References:")[1].split("CVSS scores:")[0]
    listed = "CVE-2026-98432" in xref
    page = g(os.path.join(R17, f"suse_suse_su_2026{i}_1.raw.gz"))
    flat = re.sub(r"<[^>]*>", " ", page)
    rd_page = re.search(r"Release Date:\s*([0-9T:\-]+Z)", flat).group(1)
    assert rd_page == rd_msg, (i, rd_page, rd_msg)
    rd = datetime.strptime(rd_msg, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    osv = json.loads(g(os.path.join(D, f"osv-{i}.raw.gz")))
    st, st_local_day = stamps[i]
    ld = lm.date()
    if ld == st.date() and ld != rd.date(): cls = "CVE-page stamp"
    elif ld == rd.date() and ld != st.date(): cls = "Release Date"
    else: cls = "neither/none chosen"
    rows.append((i, n, lm, midt, rd_msg, rd_page, listed, st, st_local_day, osv["published"], cls,
                 (ld - POST).days, (rd.date() - POST).days, (st - lm).total_seconds()/3600))
for r in rows:
    print(f"SUSE-SU-2026:{r[0]}-1 idx_hits={r[1]} list={r[2]:%Y-%m-%d %H:%M:%S}Z msgid={r[3]:%Y-%m-%d %H:%M:%S}Z "
          f"RD(msg)={r[4]} RD(page17Nov)={r[5]} listed={r[6]} stampUTC={r[7]:%Y-%m-%d %H:%M:%S}Z stampCETday={r[8]} "
          f"OSVpub={r[9]} -> {r[10]}; list-post={r[11]}d RD-post={r[12]}d stamp-list={r[13]:.2f}h")
from collections import Counter
print("24 Oct group:", Counter(r[10] for r in rows[:4]), " 2 Nov group:", Counter(r[10] for r in rows[4:]))
print("earliest list message:", min(r[2] for r in rows), "days after post:", (min(r[2] for r in rows).date()-POST).days)
fs, ls = date(2026,10,11), date(2026,10,15)
print("first stable -> earliest list day:", (date(2026,10,29)-fs).days, " last stable ->", (date(2026,10,29)-ls).days)
print("post +45/+90 from 29 Oct:", date(2026,10,29)+timedelta(45), date(2026,10,29)+timedelta(90))
print("stamp-list hours min/max:", round(min(r[13] for r in rows),2), round(max(r[13] for r in rows),2))
print("OSV source hosts:", sorted({a.get("database_specific",{}).get("source","")[:20] for r in IDS for a in json.loads(g(os.path.join(D,f"osv-{r}.raw.gz"))).get("affected",[])}))
# Post hoc context (not part of the rule): order of SUSE-SU identifiers in the list's date index around the followed messages
for m, lo, hi in (("10", 30163, 30240), ("11", 30340, 30366)):
    t = g(os.path.join(D, f"month-2026-{m}.raw.gz"))
    seq = [(int(a), b) for a, b in re.findall(r'HREF="0?(\d+)\.html">SUSE-SU-2026:(\d+)-\d+', t) if lo <= int(a) <= hi]
    print(f"index {m}, messages {lo}-{hi}:", " ".join(b for _, b in seq))
