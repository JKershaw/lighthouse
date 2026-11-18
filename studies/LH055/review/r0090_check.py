#!/usr/bin/env python3
"""R-0090: independent checks for the evidence review of LH055 round 2 (record 0.4).

Written by the reviewer, independently of scripts/r2_tables.py. Offline, standard library only.
Prints counts, hashes and short verdicts; it prints no withheld detail, address or email.

Replay (from the repository root):
  python3 -I studies/LH055/review/r0090_check.py > studies/LH055/review/r0090_check_output.txt
"""
import csv, gzip, hashlib, json, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
S = os.path.join(ROOT, "studies", "LH055")
R2 = os.path.join(S, "data", "round2-2026-11-17T2124Z")
BL = os.path.join(S, "data", "baseline-2026-11-17T2030Z")
SRC = {"S08": "R01", "S09": "R02", "S10": "R03", "S11": "R04", "S12": "R05", "S13": "R06", "S14": "R07"}


def h(b):
    return hashlib.sha256(b).hexdigest()


def sq(s):
    return " ".join(s.split())


def rd(p, binary=False):
    with open(p, "rb" if binary else "r", **({} if binary else {"encoding": "utf-8"})) as f:
        return f.read()


def body(fid, base=R2):
    return gzip.open(os.path.join(base, "bodies", fid + ".raw.gz")).read()


def txt(fid, base=R2):
    return rd(os.path.join(base, "text", fid + ".txt"))


print("== A. hash chain: fetch log -> redactions.json -> withholding_pass2.json -> files on disk")
log = [json.loads(l) for l in open(os.path.join(R2, "fetch_log.jsonl"))]
red = json.load(open(os.path.join(R2, "redactions.json")))
p2 = json.load(open(os.path.join(R2, "withholding_pass2.json")))
for r in log:
    fid = r["id"]
    b, t = body(fid), rd(os.path.join(R2, "text", fid + ".txt"), True)
    hb, ht = h(b), h(t)
    chain_b = r["retained_sha256"]
    steps = ["log"]
    if fid in red:
        assert red[fid]["body_sha256_before"] == chain_b, fid
        chain_b = red[fid]["body_sha256_after"]
        steps.append("redactions")
    if fid in p2:
        assert p2[fid]["body"]["sha256_before"] == chain_b, fid
        chain_b = p2[fid]["body"]["sha256_after"]
        steps.append("pass2")
    text_expected = None
    if fid in p2:
        text_expected = p2[fid]["text"]["sha256_after"]
        if fid in red:
            assert red[fid]["text_sha256_after"] == p2[fid]["text"]["sha256_before"], fid
    elif fid in red:
        text_expected = red[fid]["text_sha256_after"]
    print(f"{fid}: body {'OK' if hb == chain_b else 'MISMATCH'} via {'>'.join(steps)}; "
          f"text {'OK' if text_expected is None or ht == text_expected else 'MISMATCH'}"
          f"{'' if text_expected else ' (no text hash recorded in the log; not checkable)'}; "
          f"status {r['status']}; received {r['received_bytes']:,} bytes")

print("\n== B. round 2 quotations: verbatim within locator, and unique in the whole text")
claims = list(csv.DictReader(open(os.path.join(S, "claims.csv"), encoding="utf-8")))
r2c = [c for c in claims if c["source_id"] in SRC]
probs = 0
for c in r2c:
    m = re.search(r"text/(R\d\d)\.txt lines (\d+)(?:-(\d+))?$", c["passage_locator"])
    fid, a, z = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
    assert fid == SRC[c["source_id"]]
    lines = txt(fid).split("\n")
    within = sq(c["passage"]) in sq(" ".join(lines[a - 1:z]))
    n_all = sq(txt(fid)).count(sq(c["passage"]))
    if not within or n_all != 1:
        probs += 1
        print(f"{c['claim_id']}: within={within} occurrences_in_text={n_all}")
print(f"{len(r2c)} round 2 claims; problems: {probs}; total rows in claims.csv: {len(claims)}; "
      f"ids C{min(int(c['claim_id'][-3:]) for c in r2c)} to C{max(int(c['claim_id'][-3:]) for c in r2c)}; "
      f"contiguous: {sorted(int(c['claim_id'][-3:]) for c in r2c) == list(range(130, 168))}")
print("by source:", dict(sorted(Counter(c["source_id"] for c in r2c).items())))
print("basis labels:", dict(Counter(x.strip() for c in r2c for x in c["basis"].split(";"))))
print("claims with empty campaign:", sum(1 for c in r2c if not c["campaign"].strip()))

print("\n== C. links_r2.csv tallies (my count)")
L = list(csv.DictReader(open(os.path.join(S, "links_r2.csv"), encoding="utf-8")))
short = lambda s: s.split()[0]
print("rows:", len(L), "; sources:", dict(Counter(l["source_id"] for l in L)))
print("all:", dict(Counter(short(l["status"]) for l in L)))
c1 = [l for l in L if not l["bears_on_amazon_campaign1"].startswith("no")]
print("bearing on Campaign 1 (field not starting 'no'):", len(c1), dict(Counter(short(l["status"]) for l in c1)),
      "sources", sorted({l["source_id"] for l in c1}))
print("supported rows:", [(l["source_id"], l["link_id"]) for l in L if l["status"].startswith("supported")])
print("claimed rows:", [(l["source_id"], l["link_id"]) for l in L if l["status"].startswith("claimed")])
ids = {c["claim_id"]: c["source_id"] for c in claims}
bad = [(l["source_id"], l["link_id"], x) for l in L for x in [y.strip() for y in l["claim_ids"].split(";") if y.strip()]
       if ids.get(x) != l["source_id"]]
print("cited claims missing or from another source:", bad)
print("distinct campaign strings:", len({l["campaign"] for l in L}))

print("\n== D. statements checked against source text (presence of key words, lower case)")
def has(fid, *terms):
    t = txt(fid).lower()
    return {x: t.count(x.lower()) for x in terms}
print("S08 hedge and summary:", has("R01", "might have attempted to abuse", "abuse of azure ai services",
      "suggests that the threat actor", "ai model deployments", "suspected artex use", "artex"))
print("S10 payment words:", has("R03", "bought", "purchas", "paid", "pay ", "payment", "subscri", "credit", "reseller", "proxy/reseller"))
print("S11 Amazon mentions and loop words:", has("R04", "amazon", "loop", "inference", "self-sustain", "stolen key", "api key"))
print("S13 Amazon, loop, campaigns listed:", has("R06", "amazon", "madpot", "crowdstrike", "microsoft", "check point", "datadog", "dosu"))
print("S14 AI service words:", has("R07", "bedrock", "sagemaker", "invokemodel", "openai", "deepseek", "llm/pool", "bans or cuts off"))
print("S09 gateway/pool words:", has("R02", "gateway", "pool", "self-updater"))
s02 = txt("S02", BL)
print("S02 phrases bearing on post hoc reading 4:", {k: s02.count(k) for k in
      ["framework’s own model gateway", "different AI gateways", "managed pool"]})
stack = sq(txt("R05"))
q = "Each call shipped system prompts, task context, tool-use histories, knowledge-graph state agents' reported findings straight into Amazon's telemetry."
print("The Stack's CISO quotation present in R05:", q.split(",")[0] in stack)
l99 = s02.split("\n")[98]
print("S02 line 99 carries the same five items:",
      all(k in l99 for k in ["task context", "system prompts", "tool histories", "knowledge-graph state", "reported findings"]),
      "; 'shipped' in S02 text:", "shipped" in s02)

print("\n== E. clocks")
from datetime import datetime, timezone
am = datetime.fromisoformat("2026-11-13T13:26:42-07:00")
ta = datetime.fromisoformat("2026-11-13T20:57:13+00:00")
print("Talos minus Amazon (minutes):", round((ta - am).total_seconds() / 60, 1))
for r in log:
    print(r["id"], "HTTP Last-Modified:", r["headers"].get("Last-Modified"), "| started", r["started"], "| finished", r["finished"])
for fid in ["R07"]:
    m = re.search(rb'article:published_time" content="([^"]+)"', body(fid))
    print(fid, "article:published_time:", m.group(1).decode() if m else None)

print("\n== F. budget and robots")
q2 = re.findall(r"^## Q(\d+)", rd(os.path.join(R2, "searches", "queries.md")), re.M)
q1 = re.findall(r"^## Q(\d+)", rd(os.path.join(BL, "searches", "queries.md")), re.M)
print("round 2 queries:", q2, "; round 1 queries:", q1, "; pilot total:", len(q1) + len(q2))
print("round 2 content GETs:", len(log), "; statuses:", Counter(r["status"] for r in log))
print("round 2 bytes received (content bodies only):", f"{sum(r['received_bytes'] for r in log):,}")
rob = sorted(os.listdir(os.path.join(R2, "robots")))
print("robots decision files:", len(rob), "; all allowed:",
      all(json.load(open(os.path.join(R2, "robots", f)))["reason"] == "allowed by robots.txt" for f in rob),
      "; provider:", {json.load(open(os.path.join(R2, "robots", f)))["provider"] for f in rob})
print("provider in fetch log:", {r["provider"] for r in log})
bl = [json.loads(l) for l in open(os.path.join(BL, "fetch_log.jsonl"))]
print("pilot distinct requested URLs:", len({r["requested_url"] for r in log} | {r["requested_url"] for r in bl}))

print("\n== G. provenance of round 2 addresses (each requested URL found in a named retained body or query record)")
def inbody(url, fid, base):
    return url.encode() in body(fid, base)
u = {r["id"]: r["requested_url"] for r in log}
print("R01 in S03 body:", inbody(u["R01"], "S03", BL), "; in S07 body:", inbody(u["R01"], "S07", BL))
print("R02 in S07 body:", inbody(u["R02"], "S07", BL))
print("R03 in S04 body:", inbody(u["R03"], "S04", BL), "; in S07 body:", inbody(u["R03"], "S07", BL))
print("R04 in round 1 queries.md:", u["R04"].split("//")[1] in rd(os.path.join(BL, "searches", "queries.md")))
print("R05 in round 2 queries.md:", u["R05"].split("//www.")[1] in rd(os.path.join(R2, "searches", "queries.md")))
print("R06 (with tracking parameter) in R05 body:", (u["R06"] + "?ref=").encode() in body("R05"))
print("R07 in R06 body:", inbody(u["R07"], "R06", R2))

print("\n== H. withholding")
email = re.compile(rb"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
img = re.compile(rb"\.(png|jpe?g|svg|webp|gif|js|css)$", re.I)
ipv4 = re.compile(rb"(?<![\d.])\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?![\d.])")
part = re.compile(rb"(?<![\d.])\d{1,3}\.\d{1,3}\.\[")
for fid in SRC.values():
    b, t = body(fid), rd(os.path.join(R2, "text", fid + ".txt"), True)
    eb = [x for x in email.findall(b) if not img.search(x)]
    print(f"{fid}: emails body {len(eb)} text {len(email.findall(t))}; dotted quads body {len(ipv4.findall(b))} "
          f"text {len(ipv4.findall(t))}; partial-octet prefixes body {len(part.findall(b))} text {len(part.findall(t))}")
print("fetch log email counts withheld at collection:", {r["id"]: (r["withheld_body"]["email"], r["withheld_text"]["email"]) for r in log})
b3 = body("R03").decode("utf-8", "replace")
t3 = txt("R03")
print("R03 personal-details marker body/text:", b3.count("[personal details withheld by Lighthouse]"),
      t3.count("[personal details withheld by Lighthouse]"), "; username marker:",
      b3.count("[username withheld by Lighthouse]"), t3.count("[username withheld by Lighthouse]"))
i = t3.find("following personal details")
blk = t3[i:i + 200].split("\n")
print("R03 text lines after the 'personal details' sentence:", [("marker" if "withheld by Lighthouse" in x else ("OTHER" if x.startswith("- ") else "prose")) for x in blk[1:3]])
print("R03 body: 'mailto:' occurrences", b3.count("mailto:"), "; all followed by the email marker:",
      all(b3[m.end():m.end() + 30].startswith("[email withheld") for m in re.finditer("mailto:", b3)))
for f in ["LH055.md", "claims.csv", "links_r2.csv", "sources.md", "checkpoints/2026-11-17-round2.md",
          "scripts/r2_redact.py", "scripts/r2_claims_rows.py", "scripts/r2_links_rows.py", "scripts/r2_tables.py"]:
    d = rd(os.path.join(S, f), True)
    print(f"{f}: emails {len(email.findall(d))}; dotted quads {len(ipv4.findall(d))}")

print("\n== I. public surfaces: the reseller sentence")
inv = rd(os.path.join(ROOT, "investigations", "ai-cost-and-spread.md"))
prog = rd(os.path.join(ROOT, "programme.md"))
for name, d in [("investigation page", inv), ("programme.md", prog)]:
    print(name, {k: d.count(k) for k in ["probably bought", "probably reached its AI model through a reseller or proxy",
          "probably reaching its model through a reseller or proxy", "doesn't say how that access was paid for"]})

print("\n== J. the record's absolutes and phrasing (counts of phrases in LH055.md and the round 2 checkpoint)")
rec = rd(os.path.join(S, "LH055.md"))
ck = rd(os.path.join(S, "checkpoints", "2026-11-17-round2.md"))
for k in ["Microsoft only suggests", "Microsoft says only that", "says only that the attacker likely reached",
          "no email address or key-shaped string occurred", "only quotes Amazon", "may be what Amazon meant",
          "the only round 2 evidence that bears on that campaign"]:
    print(f"{k!r}: record {rec.count(k)}, checkpoint {ck.count(k)}")
print("\ndone")
