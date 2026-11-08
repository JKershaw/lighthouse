"""R-0057: check read 1's selection against the whole OSV export, which the
reviewer downloaded again at 2026-11-08T20:21:57Z (npm) and 20:22:08Z (PyPI);
both answered 200 with the same GCS generation and sha256 as read 1, so these
are the same bytes. The zips are not retained (258 MB); pass their directory.

    python3 -I studies/LH041/review/selection_check.py <dir with npm-all.zip and PyPI-all.zip>

Records are parsed as JSON text; nothing in them is run.
"""
import ast, collections, gzip, json, os, re, sys, zipfile
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
Z = sys.argv[1]
tree = ast.parse(open(os.path.join(ROOT, "scripts", "waves.py")).read())
LINEAGE, WAVES = None, []
for n in tree.body:
    if isinstance(n, ast.Assign) and n.targets[0].id == "LINEAGE":
        LINEAGE = ast.literal_eval(n.value)
    if isinstance(n, ast.Assign) and n.targets[0].id == "WAVES":
        WAVES = [{k.arg: ast.literal_eval(k.value) for k in c.keywords} for c in n.value.elts]
pats = [re.compile(p) for p in LINEAGE] + [re.compile(p) for w in WAVES for p in w["specific"] + w["shared"]]
seeds = [(s.lower()) for w in WAVES for s in w["seeds"]]

def defang(s):
    s = s.lower()
    for x, y in (("[.]", "."), ("(.)", "."), ("[dot]", "."), ("(dot)", "."), ("hxxp", "http"), ("[:]", ":")):
        s = s.replace(x, y)
    return s

mine, counts, since = set(), collections.Counter(), collections.Counter()
for eco in ("npm", "PyPI"):
    z = zipfile.ZipFile(os.path.join(Z, eco + "-all.zip"))
    for nm in z.namelist():
        if not nm.startswith("MAL-"):
            continue
        raw = z.read(nm).decode("utf-8", "replace")
        r = json.loads(raw)
        counts[eco] += 1
        if (r.get("published") or "") >= "2025-09-01":
            since[eco] += 1
        pkg = (((r.get("affected") or [{}])[0] or {}).get("package") or {}).get("name", "").lower()
        t = defang(raw)
        if any(p.search(t) for p in pats) or any((s.endswith("/") and pkg.startswith(s)) or pkg == s for s in seeds):
            mine.add(r["id"])
theirs = {json.loads(json.loads(l)["raw"])["id"] for l in gzip.open(os.path.join(ROOT, "data", "2026-11-08T1910Z", "osv-selected.jsonl.gz"), "rt")}
print("MAL records:", dict(counts), "published since 2025-09-01:", dict(since))
print("selected by the reviewer:", len(mine), "| by read 1:", len(theirs), "| both:", len(mine & theirs),
      "| reviewer only:", sorted(mine - theirs)[:20], "| read 1 only:", sorted(theirs - mine)[:20])
