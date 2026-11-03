"""R-0047: check the figures the 3 November later-evidence notices quote against LH013's retained analysis files.
Reads only studies/LH013/data/analysis/; run with python3 -I from the repository root."""
import csv, statistics, re, pathlib
A = pathlib.Path("studies/LH013/data/analysis")
older = list(csv.DictReader(open(A / "older.csv")))
holds = list(csv.DictReader(open(A / "holds.csv")))
py = list(csv.DictReader(open(A / "python.csv")))
for w in ("W0", "W1", "W2"):
    Os = [float(r["O"]) for r in older if r["week"] == w]
    print(f"{w}: projects {len(Os)}, median O {100*statistics.median(Os):.1f}")
inband = [r["project"] for r in holds if r["O_holds"] == "True"]
print("O within 5 points of W0 in W1 and W2:", len(inband), "of", len(holds))
print("left the band:", [(r["project"], r["dO_W1"], r["dO_W2"]) for r in holds if r["O_holds"] != "True"])
fell = {w: sum(float(r["dO_" + w]) < 0 for r in holds) for w in ("W1", "W2")}
print("O lower than W0:", fell)
for w in ("W0", "W1", "W2"):
    most = sorted(r["project"] for r in py if r["week"] == w and r["class"] == "accounts for most")
    print(w, "P accounts for most:", most)
print("P class changes:", [(r["project"], r["P_class_W0"], r["P_class_W1"], r["P_class_W2"]) for r in holds if r["P_holds"] != "True"])
txt = open(A / "results.txt").read()
for m in re.finditer(r"(W[012]): boto3 Python 3\.9 ([\d,]+) of ([\d,]+) \(([\d.]+) per cent\); boto3 over botocore on 3\.9 ([\d.]+), all Pythons ([\d.]+).*?below 1\.42\.97 ([\d.]+) per cent", txt):
    w, a, b, s, r39, rall, below = m.groups()
    a, b = int(a.replace(",", "")), int(b.replace(",", ""))
    print(f"{w}: boto3 3.9 share {100*a/b:.2f} (stated {s}); ratio 3.9 {r39} vs all {rall}; below edge {below}")
print([l.strip() for l in txt.splitlines() if "flatness W0" in l])
