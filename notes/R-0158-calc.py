"""R-0158: the evidence review of LH061 record 0.1, its consequential checks as code.

Run from the repository root:
    python3 -I notes/R-0158-calc.py > notes/R-0158-calc-output.txt

1. Reruns studies/LH061/scripts/tally.py and compares its output byte for byte with the committed
   tally-output.txt.
2. Checks how tally.py's data_label sorts each claim's data_public value (it reads "not applicable"
   as "no", because "not applicable" starts with "no").
3. Compares the hashes of the reviewer's rereads of 26 November 2026 (constants below, from the reread
   log in R-0158.md) with studies/LH061/fetchlog.csv.
4. Recomputes the percentages the record quotes from A07's counts.
5. Recounts Part A's labels under the review's should-fix rulings (S2: A05-5 setting; S3: vendor label
   for A05's claims run on a security company's internal passive DNS), without changing claims.csv.
Reads only files in the repository; no network.
"""
import csv
import hashlib
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STUDY = ROOT / "studies" / "LH061"

print("R-0158 calc")
print()
print("== 1. tally.py rerun")
out = subprocess.run([sys.executable, "-I", str(STUDY / "scripts" / "tally.py"), str(STUDY)],
                     capture_output=True, check=True).stdout
committed = (STUDY / "scripts" / "tally-output.txt").read_bytes()
print("rerun sha256    ", hashlib.sha256(out).hexdigest())
print("committed sha256", hashlib.sha256(committed).hexdigest())
print("identical:", out == committed)

print()
print("== 2. data_public labels as tally.py sorts them")
sys.dont_write_bytecode = True
sys.path.insert(0, str(STUDY / "scripts"))
import tally  # noqa: E402

with open(STUDY / "claims.csv", newline="", encoding="utf-8") as f:
    claims = list(csv.DictReader(f))
for r in claims:
    lab = tally.data_label(r["data_public"])
    raw = r["data_public"].strip().lower()
    if raw.startswith("not applicable") and lab != "not applicable":
        print(f"  {r['claim_id']}: value '{r['data_public']}' sorted as '{lab}'")


def label(v):
    v = v.strip().lower()
    for key in ("yes", "partly", "not applicable", "no"):
        if v.startswith(key):
            return key
    return "other"


partA = [r for r in claims if r["part"] == "A"]
print("Part A data public, as tally.py:", dict(Counter(tally.data_label(r["data_public"]) for r in partA)))
print("Part A data public, corrected: ", dict(Counter(label(r["data_public"]) for r in partA)))
meas = [r for r in partA if r["class"] == "measured outcome"]
print("Part A measured, corrected:    ", dict(Counter(label(r["data_public"]) for r in meas)))

print()
print("== 3. reread hashes against fetchlog.csv")
REREAD = {  # id: (reread UTC, status, bytes, sha256), reviewer's gated one-off GETs, 26 November 2026
    "A01-alowaisheq-ndss2019": ("2026-11-26T20:38:49Z", "200", 2281755, "87c3432a1eaed781f38a377e8c19b8c727aa6e3a531d463bbd007413621ac42b"),
    "A02-meli-ndss2019": ("2026-11-26T20:38:50Z", "200", 423795, "b660895aa0b5fa61577b06173ca1daf009a08779f5d9df6988eed496e7c3cba9"),
    "A03-kim-usenix2018": ("2026-11-26T20:38:51Z", "200", 8522, "4546ba7ec595d67cf9e99e772efdfdbaf6ee028c33613c097a83a827203b4810"),
    "A05-nadji-ccs2013": ("2026-11-26T20:38:52Z", "200", 576571, "d24b6ca0719c9db06c67d11d26b526bd493c084b285913ea17b74e069d49b663"),
    "A07-arxiv2603.12498": ("2026-11-26T20:38:53Z", "200", 1034943, "800ed93fdbee6b8d852997973b7bbfe24142de1169d8cafbcc18c7054ab226ce"),
    "A08-arxiv2611.30483": ("2026-11-26T20:38:54Z", "200", 452625, "a3d646eb856c40b66edfae0d80f2d0430f8fdee318d31da851d749a4ace75019"),
    "A09-arxiv2104.01631": ("2026-11-26T20:38:54Z", "200", 5498363, "3a2766109ba7cbfad1482f64cadbe67050384a34c7b3d29552d305b22b239f86"),
    "B04-simex24": ("2026-11-26T20:38:56Z", "200", 77778, "a26fd2695df464aca4dac23ce1e422b10477df2911e967add4789982c3d716c6"),
    "B07-quantumdawn-vii": ("2026-11-26T20:38:56Z", "200", 2166342, "05da103f7564f8a6f2645035ad60826be882e1e2f13774e18e9c0929102aa97f"),
    "B11-canada-capstone-2024": ("2026-11-26T20:38:58Z", "200", 59029, "d2c3b012f8004eea9a40a17d0023873acfefdfa1046ff2690a242a3a2e18d489"),
}
with open(STUDY / "fetchlog.csv", newline="", encoding="utf-8") as f:
    log = {r["id"]: r for r in csv.DictReader(f)}
same = 0
for did, (utc, st, n, h) in REREAD.items():
    r = log[did]
    match = r["sha256"] == h
    same += match
    print(f"  {did}: logged {r['bytes']} bytes {r['sha256'][:16]}, reread {n} bytes {h[:16]}: "
          f"{'same bytes' if match else 'different bytes (HTML page; ' + str(n - int(r['bytes'])) + ' bytes difference)'}")
print(f"same bytes: {same} of {len(REREAD)}")

print()
print("== 4. A07 percentages from the paper's counts")
for label_, a, b in (("exposures day 0 to 14", 1405, 706), ("still-valid day 0 to 14", 1175, 865)):
    print(f"  {label_}: {a} to {b}, fall {100 * (a - b) / a:.1f}%")
print(f"  exposures day 14 to 172: 706 to 1019, rise {100 * (1019 - 706) / 706:.1f}%")
print(f"  still-valid day 14 to 172: 865 to 660, fall {100 * (865 - 660) / 865:.1f}%")

print()
print("== 5. Part A labels under the review's should-fix rulings (claims.csv unchanged)")
setting = {r["claim_id"]: r["setting"] for r in partA}
vendor = {r["claim_id"]: r["vendor"] for r in partA}
setting["A05-5"] = "laboratory"                 # S2: a modelled takedown not carried out (simulation on field data)
for cid in ("A05-1", "A05-3", "A05-4"):         # S3: run on the security company's internal passive DNS
    vendor[cid] = "yes"
print("  setting, all Part A:", dict(Counter(setting.values())))
print("  vendor yes, all Part A:", sum(v == "yes" for v in vendor.values()))
mids = [r["claim_id"] for r in meas]
print("  measured claims: field", sum(setting[c] == "field" for c in mids),
      "laboratory", sum(setting[c] == "laboratory" for c in mids),
      "vendor", sum(vendor[c] == "yes" for c in mids), "of", len(mids))
