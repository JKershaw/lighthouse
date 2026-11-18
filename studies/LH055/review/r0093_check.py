"""R-0093 reader-and-inference review of LH055 0.5: checks the passages the note relies on.
Run from the repository root: python3 -I studies/LH055/review/r0093_check.py"""
import re, pathlib
base = pathlib.Path("studies/LH055/data")
s02 = (base / "baseline-2026-11-17T2030Z/text/S02.txt").read_text()
r01 = (base / "round2-2026-11-17T2124Z/text/R01.txt").read_text()
norm = lambda t: re.sub(r"\s+", " ", t)
s02n, r01n = norm(s02), norm(r01)
checks = {
  "S02 decoys present as LLM inference APIs": "sensors configured to present as popular large language model (LLM) inference APIs" in s02n,
  "S02 agents treated decoys as inference backends": "treating them as LLM inference backends" in s02n,
  "S02 telemetry content sent to an LLM": "ordinarily send to an LLM to make operational decisions" in s02n,
  "S02 decoy replies described": bool(re.search(r"MadPot (returned|responded|replied)", s02n)),
  "S02 says how decoys entered agents' configuration": bool(re.search(r"(configured|added|listed) (the|these) (sensors|decoys)", s02n)),
  "R01 'attempted to validate stolen Azure resources'": "attempted to validate stolen Azure resources, including compromised Azure AI services" in r01n,
  "R01 'valid leaked or stolen application credentials'": "valid leaked or stolen application credentials" in r01n,
  "R01 says GitHub-found AI keys were used": bool(re.search(r"(used|using) (the )?(AI|inference)[- ]related API keys", r01n)),
}
for k, v in checks.items():
    print(f"{k}: {v}")
ioc = re.findall(r"IPv4 (\d{4}-\d\d-\d\d) (\d{4}-\d\d-\d\d) (Campaign \d)", s02)
for c in ("Campaign 1", "Campaign 2"):
    rows = [r for r in ioc if r[2] == c]
    print(f"{c}: {len(rows)} IOC rows, first seen {min(r[0] for r in rows)}, last seen {max(r[1] for r in rows)}")
