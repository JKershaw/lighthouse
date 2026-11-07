"""Evidence review recount for the LH035 map page (notes/R-0049-lh035-map-evidence.md).
Run from the repository root: python3 studies/LH035/review/recount.py
Offline: reads only studies/LH035/data/instruments.json."""
import json, re
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parent.parent
rows = json.loads((D / "data/instruments.json").read_text())["rows"]
ids = {r["id"] for r in rows}
print("included rows", len(rows))

anyl = Counter(l for r in rows for l in r["layers"])
prim = Counter(r["primary"] for r in rows)
print("any-layer", dict(sorted(anyl.items())))
print("primary  ", dict(sorted(prim.items())))
print("layers with zero rows", [l for l in range(1, 11) if anyl[l] == 0])
print("certificate rows (layer 5):", [(r["id"], r["name"]) for r in rows if 5 in r["layers"]])
print("names rows (layer 4):", [(r["id"], r["name"]) for r in rows if 4 in r["layers"]])
print("running-services rows (layer 6):", [(r["id"], r["name"]) for r in rows if 6 in r["layers"]])
print("traffic rows (layer 10):", [(r["id"], r["name"]) for r in rows if 10 in r["layers"]])
print("routing rows (layer 2):", [(r["id"], r["name"]) for r in rows if 2 in r["layers"]])
print("address rows (layer 3):", [(r["id"], r["name"]) for r in rows if 3 in r["layers"]])

# Dependencies on another included instrument, coded by hand from each row's
# vantage / note fields (what each row's own page says it draws on), as the
# record's Answer lists them. Each entry: row -> rows it draws on, and the field text.
DEPS = {
    "I08": (["I05", "I06"], "vantage"),          # RouteViews and RIPE RIS snapshots
    "I09": (["I05", "I06", "I16"], "vantage"),   # MRT data from RouteViews and RIS; CT logs
    "I14": (["I15", "I09"], "vantage"),          # CrUX, Cloudflare Radar
    "I19": (["I15"], "vantage"),                 # URLs from CrUX
    "I20": (["I15", "I14"], "vantage"),          # CrUX and customised Tranco list
    "I23": (["I22"], "vantage"),                 # PSF public BigQuery dataset
    "I33": (["I47"], "vantage"),                 # unreviewed from the NVD feed
    "I32": (["I33"], "vantage"),                 # GitHub Security Advisories
    "I41": (["I01", "I08"], "note"),
    "I48": (["I06", "I10"], "note"),
    "I47": (["I31"], "note"),
}
for k, (deps, field) in DEPS.items():
    assert all(d in ids for d in deps)
    r = next(x for x in rows if x["id"] == k)
    print(f"  {k} {r['name']} -> {deps}  [{field}: {r[field][:110]}]")
print("rows drawing on another included instrument:", len(DEPS), "of", len(rows))
# Rows that plausibly draw on another included instrument but are not counted.
print("  not counted, check: I24 ClickPy vantage =", next(x for x in rows if x["id"] == "I24")["vantage"])
print("  not counted, check: I11 Ark vs I08 (I08 serial-2 adds Ark traceroutes): I08 already counted")
print("  not counted, check: I29 deps.dev vulns source:", next(x for x in rows if x["id"] == "I29")["vantage"])

# Rows whose pages state no limit of their own: cannot_see begins with "not stated"
# or says only "No coverage limit stated" / "no general statement".
def no_limit(r):
    c = r["cannot_see"].strip()
    return c.lower().startswith("not stated")
nl = [r for r in rows if no_limit(r)]
print("cannot_see starts 'not stated':", len(nl))
for r in nl:
    print(f"  {r['id']} {r['name']}: {r['cannot_see']}")
qual = [r["id"] for r in nl if r["cannot_see"].strip().lower() not in ("not stated", "not stated on the page read", "not stated in the documentation read")]
print("of which carry a qualification ('beyond', ';', etc.):", qual)
print("v0.1 rows (I01-I40) in that set:", sum(1 for r in nl if int(r["id"][1:]) <= 40),
      " rows I41-I48:", sum(1 for r in nl if int(r["id"][1:]) > 40))
other = [r for r in rows if not no_limit(r) and re.search(r"no general statement|no coverage limit stated", r["cannot_see"], re.I)]
print("borderline rows not counted:", [(r["id"], r["cannot_see"][:100]) for r in other])

# Numeric coverage statement
print("rows giving a percentage of their own coverage:",
      [(r["id"], r["name"]) for r in rows if re.search(r"coverage[^.]*\d+%|\d+% *\(90", r["cannot_see"])])

# IPv6 mentions in any field
for r in rows:
    blob = json.dumps(r)
    if "IPv6" in blob or "/48" in blob:
        print("IPv6 mention:", r["id"], r["name"])

# Sensitivity of the "17 of 48 state no limit" count to how borderline rows are read.
base = {r["id"] for r in nl}                       # cannot_see begins "not stated": 16
caveat_only = {"I44", "I46"}                        # "not stated, beyond ..." a stated caveat
print("\nno-limit count, by reading:")
print("  mechanical (cannot_see begins 'not stated'):", len(base))
print("  + I06 ('No coverage limit stated', page states only a deprecation note):", len(base | {"I06"}))
print("  + I06 + I17 ('no general statement', one report's spoofing caveat):", len(base | {"I06", "I17"}))
print("  strict 'no limit at all' (drop I44, I46, which state a caveat):", len(base - caveat_only))
print("  record's own figure: 13 of I01-I40 + 4 of I41-I48 = 17; mechanical I01-I40 =",
      sum(1 for i in base if int(i[1:]) <= 40))

# Coverage stated as a number on a row's page (not only Epoch AI's completeness estimate).
for i, pat in [("I03", "45%"), ("I13", "1/256"), ("I04", ">75%")]:
    r = next(x for x in rows if x["id"] == i)
    print(f"  {i} {r['name']}: '{pat}' in fields:", pat in json.dumps(r))
