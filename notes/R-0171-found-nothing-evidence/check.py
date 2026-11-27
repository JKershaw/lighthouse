"""R-0171: reproduce the counts, dates and quotations the found-nothing draft (0.1) uses,
from the files the records retain. Offline; standard library only.
Replay from the repository root:
    python3 -I notes/R-0171-found-nothing-evidence/check.py > notes/R-0171-found-nothing-evidence/check_output.txt
"""
import csv, glob, gzip, json, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
S = os.path.join(ROOT, "studies")


def rd(path):
    with (gzip.open if path.endswith(".gz") else open)(path, "rb") as f:
        return f.read().decode("utf-8", "replace")


def text(html):
    """Visible text, roughly: tags dropped, whitespace collapsed."""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))


print("== 1. LH013 Stage A (studies/LH013/data/installer/)")
rows = list(csv.DictReader(open(os.path.join(S, "LH013/data/installer/stage_a_A1.csv"))))
tot = sum(int(r["rows"]) for r in rows)
meta = sum(int(r["metadata_rows"]) for r in rows)
print("A1 groups:", len(rows), "| distinct installer names (blank counted separately):",
      len({r["installer"] for r in rows if r["installer"]}), "+ blank" if any(not r["installer"] for r in rows) else "")
print("A1 rows summed:", f"{tot:,}", "| metadata_rows summed:", meta,
      "| groups with metadata_rows > 0:", sum(int(r["metadata_rows"]) > 0 for r in rows))
print("A1 Python 3.9 rows:", f"{sum(int(r['rows']) for r in rows if r['py']=='3.9'):,}",
      "| other:", f"{sum(int(r['rows']) for r in rows if r['py']!='3.9'):,}")
a2 = list(csv.DictReader(open(os.path.join(S, "LH013/data/installer/stage_a_A2.csv"))))
print("A2:", a2[0]["date"], a2[0]["project"], f"{int(a2[0]['total']):,}", "| equals A1:", int(a2[0]["total"]) == tot)
for line in open(os.path.join(S, "LH013/data/read_log.csv")):
    if "installer-A" in line:
        print("read log:", line.split(",")[0], line.split(",")[3])

print("\n== 2. LH036 (studies/LH036/data/read-*/): CISA catalogue and the kernel announcement")
REVIEWED = {"2026-11-01T0830Z", "2026-11-02T1526Z", "2026-11-05T1414Z", "2026-11-09T1430Z",
            "2026-11-12T1417Z", "2026-11-16T1419Z"}
for d in sorted(glob.glob(os.path.join(S, "LH036/data/read-*"))):
    lab = os.path.basename(d)[5:]
    k = json.loads(rd(os.path.join(d, "kev.raw.gz")))
    listed = any(v.get("cveID") == "CVE-2026-98432" for v in k["vulnerabilities"])
    log = json.load(open(os.path.join(d, "read_log.json")))
    ents = log if isinstance(log, list) else log.get("entries", [])
    ka = [e for e in ents if e.get("name") == "kernel_announcement"]
    if ka:
        e = ka[0]
        if "status" in e:
            der = os.path.join(d, "kernel_announcement.derived.json")
            ch = json.load(open(der))["extracted"]["challenge_page"] if os.path.exists(der) else "?"
            kan = f"HTTP {e['status']}, challenge page: {ch}"
        else:
            r = e.get("robots", {})
            kan = f"not fetched: {r.get('rule')} for {r.get('decided_by')} ({e.get('error','')[:40]})"
    else:
        kan = "no entry"
    print(f"{lab} {'reviewed  ' if lab in REVIEWED else 'UNREVIEWED'} KEV {k['catalogVersion']} "
          f"(released {k['dateReleased'][:16]}) title={k['title']!r} CVE-2026-98432 listed: {listed} | announcement: {kan}")

print("\n== 3. LH038 read of 17 November (studies/LH038/data/read-2026-11-17T1419Z/)")
d38 = os.path.join(S, "LH038/data/read-2026-11-17T1419Z")
for f in sorted(glob.glob(os.path.join(d38, "changelog_*.raw.gz"))):
    t = rd(f)
    blocks = re.split(r"\n(?=commit [0-9a-f]{40})", t)
    fix = [b for b in blocks if "e3f33b0a1d89" in b]
    first = blocks[0] if blocks[0].startswith("commit") else blocks[1]
    rel_date = re.search(r"\nDate:\s+(.+)", first).group(1).strip()
    for b in fix:
        date = re.search(r"\nDate:\s+(.+)", b).group(1).strip()
        rep = re.findall(r"Reported-by:[^\n]*", b)
        rep_has_date = any(re.search(r"\b(20\d\d|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b", r) for r in rep)
        print(os.path.basename(f), "| release commit date:", rel_date, "| fix author date:", date,
              "| Reported-by lines:", len(rep), "| a date in them:", rep_has_date)
post_raw = rd(os.path.join(d38, "anthropic_post.raw.gz"))
post = text(post_raw)
q = "We reported each vulnerability to the affected vendor under our coordinated vulnerability disclosure"
print("post quote present:", q in post, "| datePublished:", re.findall(r'"datePublished"\s*:\s*"([^"]+)"', post_raw)[:1])

print("\n== 4. LH030 (studies/LH030/data/read-*/)")
dirs = sorted(glob.glob(os.path.join(S, "LH030/data/read-*")))
retained = [d for d in dirs if not os.path.exists(os.path.join(d, "FAILED.md"))]
print("read directories:", len(dirs), "| retained reads (no FAILED.md):", len(retained),
      "| first:", os.path.basename(retained[0]), "| last:", os.path.basename(retained[-1]))
walls = {"cisa_0": set(), "akamai_0": set()}
n_entries = 0
for d in dirs:
    for e in json.load(open(os.path.join(d, "read_log.json"))):
        if e["name"] in walls:
            walls[e["name"]].add(e.get("status"))
            n_entries += 1
print("CISA and Akamai log entries (all 30 logs):", n_entries, "| statuses:", {k: sorted(v) for k, v in walls.items()})
TRK = ["cve_org_0", "nvd_0", "osv_0", "debian_0", "ubuntu_0", "redhat_0", "suse_0"]
for d in retained:
    lab = os.path.basename(d)[5:]
    st = {}
    for e in json.load(open(os.path.join(d, "read_log.json"))):
        if e["name"] in TRK:
            s = e.get("status")
            if e["name"] == "nvd_0" and s == 200:
                try:
                    s = "200/total=%s" % json.loads(open(os.path.join(d, "nvd_0.raw"), "rb").read())["totalResults"]
                except Exception as ex:
                    s = "200/?"
            st[e["name"][:-2]] = s
    norec = [k for k, v in st.items() if v in (404, "200/total=0")]
    print(lab, st, "| no record:", len(norec), "of", len(st))
for lab in ("2026-11-19T1417Z", "2026-11-23T1421Z"):
    raw = open(os.path.join(S, f"LH030/data/read-{lab}/php_0.raw"), "rb").read().decode("utf-8", "replace")
    t = text(raw)
    promise = "will publish a full advisory for CVE-2026-115560 with the next release"
    arts = [text(a) for a in raw.split('<article class="newsItem">')[1:]]
    nov19 = [a for a in arts if a.strip().startswith("19 Nov 2026")]
    print(lab, "php_0: CVE-2026-115560 occurrences:", t.count("CVE-2026-115560"),
          "| promise present:", promise in t, "| entries dated 19 Nov 2026:", len(nov19),
          "| of them saying 'This is a security release':", sum("This is a security release" in a for a in nov19),
          "| naming CVE-2026-115560:", sum("CVE-2026-115560" in a for a in nov19))
    prom = [a for a in arts if "CVE-2026-115560" in a]
    print("   the entry naming the flaw is dated:", [a.strip()[:11] for a in prom])
    print("   titles of the entries dated 19 Nov 2026:", [re.match(r"\s*19 Nov 2026 (.*? Released!)", a).group(1) for a in nov19])

print("\n== 5. LH043 (studies/LH043/data/sources/)")
src = os.path.join(S, "LH043/data/sources")
inc = rd(os.path.join(src, "aisi-INC-2026-07-28-01.txt"))
print("GITHUB_ACCOUNT_A (whole word) in INC-2026-07-28-01:", len(re.findall(r"\bGITHUB_ACCOUNT_A\b", inc)),
      "| PERSON_C:", len(re.findall(r"\bPERSON_C\b", inc)))
print("anonymity quote present:", "to preserve the anonymity of the affected repository and users" in inc)
print("'Organization 1' in openai-hf-report:", rd(os.path.join(src, "openai-hf-report.txt")).count("Organization 1"))
print("'[account name redacted]' in metr-hf-investigation:", rd(os.path.join(src, "metr-hf-investigation.txt")).count("[account name redacted]"))
fl = [l.split("\t") for l in open(os.path.join(S, "LH043/data/fetch-log.tsv")).read().splitlines()]
docs = [r for r in fl if "robots" not in r[3]]
print("fetch log: documents", len(docs), "| status 200:", sum(r[1] == "200" for r in docs),
      "| refused:", [(r[1], r[2]) for r in docs if r[1] != "200"], "| times:", fl[0][0], "to", fl[-1][0])

print("\n== 6. LH060 (studies/LH060/)")
fr = list(csv.DictReader(open(os.path.join(S, "LH060/fetchlog.csv"))))
print("fetches:", len(fr), "| dates:", sorted({r["start_utc"][:10] for r in fr}))
sq = [l for l in open(os.path.join(S, "LH060/searches.md")) if l.startswith("## Q")]
print("searches:", len(sq))
b = open(os.path.join(S, "LH060/brief.md")).read()
print("brief, fewer-than-three rule present:", "Fewer than three documents included" in b)
reg = open(os.path.join(S, "LH060/register.md")).read()
print("register summary line:", [l for l in reg.splitlines() if l.startswith("- Included")],
      "| C08 excluded line present:", "C08 excluded" in reg)
