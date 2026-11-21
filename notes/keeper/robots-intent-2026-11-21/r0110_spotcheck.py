#!/usr/bin/env python3
"""R-0110 spot-check of derived files (fresh checker, 21 November 2026). Offline; reads the repository only.

For a seeded sample of derived files (every study, 24 files): (a) no email address and the longest string in
"extracted"; (b) URL, read time and SHA-256 against the read log in the same folder; (c) SHA-256 of the original
body at commit 240e6fb (bytes as received: gunzipped for .gz); (d) every string and number leaf of "extracted"
looked for in the original body's text (tags stripped, entities unescaped, whitespace collapsed) and in the raw
text; misses are printed for reading by hand.
Usage: python3 -I r0110_spotcheck.py
"""
import gzip, hashlib, html, json, random, re, subprocess, sys
R = "/home/user/lighthouse"; PRE = "240e6fb"
EMAIL = re.compile(rb"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

def git(*a):
    return subprocess.run(["git", "-C", R] + list(a), capture_output=True, check=True).stdout

added = [f for f in git("diff", "--name-only", "--diff-filter=A", PRE, "HEAD", "--", "studies").decode().split()
         if f.endswith(".derived.json")]
deleted = git("diff", "--name-only", "--diff-filter=D", PRE, "HEAD", "--", "studies").decode().split()
by = {}
for f in added: by.setdefault(f.split("/")[1], []).append(f)
rnd = random.Random(20261121); sample = []
quota = {"LH033": 5, "LH039": 7}
for s, fs in sorted(by.items()):
    sample += rnd.sample(sorted(fs), min(len(fs), quota.get(s, 2 if len(fs) > 1 else 1)))

def leaves(x):
    if isinstance(x, dict):
        for v in x.values(): yield from leaves(v)
    elif isinstance(x, list):
        for v in x: yield from leaves(v)
    elif isinstance(x, (str, int, float)) and not isinstance(x, bool):
        yield x

def find_log(d, sha):
    out = []
    for f in git("ls-tree", "--name-only", "HEAD", d + "/").decode().split():
        if f.endswith(".derived.json") or not re.search(r"(log|read_log|reads)[^/]*\.(json|jsonl|tsv|csv|txt)$", f): continue
        t = git("show", "HEAD:" + f).decode("utf8", "replace")
        if sha not in t: continue
        try:
            j = json.loads(t)
            items = j if isinstance(j, list) else next((v for v in j.values() if isinstance(v, list)), [])
            for it in items:
                if sha in json.dumps(it): out.append((f, json.dumps(it)))
        except ValueError:
            for line in t.splitlines():
                if sha in line: out.append((f, line.strip()))
    return out

for f in sample:
    d = json.loads(open(R + "/" + f).read())
    raw = open(R + "/" + f, "rb").read()
    stem = f[: -len(".derived.json")]
    body_f = [x for x in deleted if re.fullmatch(re.escape(stem) + r"\.(body|raw\.gz|raw|html\.gz|html|json\.gz|json)", x)]
    ex = d.get("extracted", d.get("facts"))
    strs = [x for x in leaves(ex) if isinstance(x, str)]
    print("==", f)
    print("   keys:", sorted(d.keys()))
    print("   emails in derived:", len(EMAIL.findall(raw)), "| longest extracted string:", max((len(s) for s in strs), default=0),
          repr(max(strs, key=len)[:120]) if strs else "")
    sha, url, t = d.get("sha256") or d.get("sha256_retained_response"), d.get("url"), d.get("read_utc") or d.get("read_time") or d.get("time_utc")
    if not body_f:
        print("   ORIGINAL BODY NOT FOUND among deleted files"); continue
    b = git("show", PRE + ":" + body_f[0])
    rb = gzip.decompress(b) if body_f[0].endswith(".gz") else b
    print("   body:", body_f[0].split("/")[-1], "| sha(body as received) == derived:", hashlib.sha256(rb).hexdigest() == sha,
          "| sha(file) == derived:", hashlib.sha256(b).hexdigest() == sha)
    logs = find_log("/".join(f.split("/")[:-1]), sha)
    if logs:
        lf, rec = next(((a, b) for a, b in logs if stem.split("/")[-1] in b), logs[0])
        print("   read log", lf.split("/")[-1], "| url in record:", url in rec, "| read time in record:",
              (t in rec) if t else "no read time in derived", "| records with this sha:", len(logs))
        if t and t not in rec: print("     record:", rec[:300])
    else:
        print("   READ LOG RECORD WITH THIS SHA NOT FOUND")
    txt = rb.decode("utf8", "replace")
    flat = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<script.*?</script>|<style.*?</style>", "", txt))))
    miss = []
    for v in leaves(ex):
        s = str(v)
        if s in flat or s in txt or html.escape(s) in txt or json.dumps(v)[1:-1] in txt: continue
        miss.append(s + ("  [found ignoring case]" if s.lower() in flat.lower() else ""))
    n = sum(1 for _ in leaves(ex))
    print("   extracted leaves:", n, "| not found verbatim in body:", len(miss), miss[:8])
    print('   extracted (first 400 chars):', json.dumps(ex)[:400]) if miss else None
