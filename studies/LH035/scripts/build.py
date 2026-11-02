"""Build studies/LH035/sources.md (the survey table) from the study's data files,
and print the counts the record quotes.
Run from the repository root: python3 studies/LH035/scripts/build.py
Offline: it reads only studies/LH035/data/."""
import csv
import json
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parent.parent
LAYERS = {
    1: "Physical and interconnection", 2: "Routing", 3: "Addresses and reachability",
    4: "Names", 5: "Certificates", 6: "Running services and their software",
    7: "Web content and technology", 8: "Software supply",
    9: "Vulnerability and exploitation records", 10: "Traffic",
}

inst = json.loads((D / "data/instruments.json").read_text())
rows = inst["rows"]
cands = json.loads((D / "data/candidates.json").read_text())["rows"]
lit = json.loads((D / "data/literature.json").read_text())["papers"]
fetches = list(csv.DictReader(open(D / "data/fetchlog.csv")))


def cell(s):
    return (s or "").replace("|", "/").replace("\n", " ")


def counts():
    any_layer = Counter(l for r in rows for l in r["layers"])
    primary = Counter(r["primary"] for r in rows)
    other = Counter()
    for c in cands:
        for l in c["layers"]:
            other[(c["class"], l)] += 1
    return any_layer, primary, other


LEADS = [
    ("iGDB, a research database of physical and logical topology", "L1b result 4", 1),
    ("M-Lab's IP Route Survey (IPRS) dataset", "L2a result 2", 2),
    ("NPD-Routes traceroutes, 1994 to 1995", "L2a result 1", 2),
    ("TARTAN traceroute dataset (IEEE DataPort)", "L2a results 7 and 8", 2),
    ("GEANT and Abilene traffic matrices", "L2a result 10; L10a result 2", 10),
    ("RIPE NCC Internet measurement data repository", "L4a result 7", 3),
    ("CAIDA DNS Names dataset; WAND WITS traces", "L4a summary", 4),
    ("ICANN's new public data page (announcement of 15 June 2026)", "L4b result 2", 4),
    ("Net Data Directory (Berkman)", "L4b result 9", None),
    ("EFF SSL Observatory", "L5b result 11", 5),
    ("UpGuard CyberResilience; Zondex; Cambridge CCCC scanner", "L6b results 2, 4, 8", 6),
    ("KIT web measurement datasets", "L7a results 1 to 7", 7),
    ("Similarweb website datasets (commercial)", "L7a result 5", 7),
    ("CodeSupply (EU Horizon project)", "L8b result 3", 8),
    ("OSPtrack package-behaviour dataset", "L8a results 4 and 5", 8),
    ("Vulners; VulnCheck; cyberdetails.org corpus", "L9b results 5 to 7; L9a result 6", 9),
    ("DScope cloud telescope", "L9a result 3", 9),
    ("ZoomEye", "L9b summary", 6),
    ("MIRAGE-2019 mobile traffic; NDN testbed traces; CAIDA passive traces", "L10a results 4 and 6; L10a summary", 10),
    ("Internet Society Pulse IXP tracker (a menu link on the page read)", "L10b result 11", 10),
]
LIT_NAMED = "Instruments named only in papers read (leads outside the fixed plan, not read): OpenINTEL (L07's ground truth), bgp.tools (L06), the Merit and SURF telescopes (L09), Fofa, BinaryEdge and ONYPHE (L01), Hispar (L08)."


def write_sources():
    any_layer, primary, other = counts()
    out = []
    out.append("# LH035 survey table\n")
    out.append("Built by `python3 studies/LH035/scripts/build.py` from studies/LH035/data/ (instruments.json, candidates.json, literature.json, fetchlog.csv); edit the data, not this file. Every row was filled from the instrument's own pages fetched on 2 November 2026 with WebFetch, which returns a model-written extract of each page rather than the page itself; quotation marks enclose the extract's quotation of the page. \"not stated\" means the pages read did not give it. The last column but one, the characteristic blind spot, is Lighthouse's reading (interpretation), not the instrument's statement, and may be blank. Layer numbers are the brief's: " + "; ".join(f"{k} {v}" for k, v in LAYERS.items()) + ".\n")
    out.append("Origin: a = an instrument Lighthouse's studies used; b = an LH003 row touching a layer here (re-read, not copied); c = the fixed search plan (search ids as in searchlog.md). Literature ids (L01 to L11) are in the table near the end; a paper's evaluation is cited beside the row it concerns.\n")
    out.append(f"## Included: {len(rows)} instruments\n")
    out.append("| Id | Instrument and pages read | Layers (primary first) | What it counts | Vantage | Cadence | History | Access and licence | Page date; observation window; date read | What it says it cannot see | Blind spot (Lighthouse's reading, interpretation) | Origin | Literature |")
    out.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in rows:
        layers = [r["primary"]] + [l for l in r["layers"] if l != r["primary"]]
        out.append("| " + " | ".join(cell(x) for x in [
            r["id"], r["name"] + ": " + "; ".join(r["urls_read"]), ", ".join(map(str, layers)),
            r["counts"], r["vantage"], r["cadence"], r["history"], r["access"],
            f"{r['page_date']}; {r['window']}; read {inst['date_read']}",
            r["cannot_see"], r["blind_spot"] or "(blank)", r["origin"], r["literature"] or "",
        ]) + " |")
    notes = [r for r in rows if r.get("note")]
    if notes:
        out.append("\n### Notes on rows\n")
        for r in notes:
            out.append(f"**{r['id']} {r['name']}.** {r['note']}\n")
    out.append("\n## Counts by layer\n")
    out.append("| Layer | Included, any layer | Included, primary layer | Undetermined | Unreadable |")
    out.append("| --- | --- | --- | --- | --- |")
    for k, v in LAYERS.items():
        out.append(f"| {k} {v} | {any_layer[k]} | {primary[k]} | {other[('undetermined', k)]} | {other[('unreadable', k)]} |")
    out.append("\n## Candidates without a row\n")
    out.append("Inclusion test applied (a decision made in this run, recorded in LH035.md, Method): a row is included when the pages read show data, link to data files, or describe the data as public, published, free or openly licensed. Undetermined: the pages read put the data behind an account, request, credentials or subscription without saying any of it is free, or say nothing of its availability, so the brief's rule could not be applied; not tabulated. Unreadable: the pages could not be read in this run; inconclusive, not excluded. Excluded: fails a rule of the brief.\n")
    out.append("| Candidate | Class | Layers | Origin | Pages tried | Reason |")
    out.append("| --- | --- | --- | --- | --- | --- |")
    for c in cands:
        out.append("| " + " | ".join(cell(x) for x in [c["name"], c["class"], ", ".join(map(str, c["layers"])) or "none", c["origin"], "; ".join(c["urls_read"]) or "not re-read", c["reason"]]) + " |")
    out.append("\n## Leads not reached\n")
    out.append("Named in a search result or a search summary, not opened within the ceiling; leads only, with no row and no claim about them. Layer is the one the lead's wording suggests.\n")
    for name, where, layer in LEADS:
        out.append(f"- {name} ({where}; layer {layer if layer else 'unclear'})")
    out.append("\n" + LIT_NAMED + "\n")
    out.append("\n## Literature opened\n")
    out.append("| Id | Paper | URL and search result | How read | Rows | Method | Findings used | Limits |")
    out.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for p in lit:
        out.append("| " + " | ".join(cell(x) for x in [p["id"], p["cite"], p["url"] + " (" + p["search"] + ")", p["how_read"], ", ".join(p["rows"]), p["method"], p["findings"], p["limits"]]) + " |")
    out.append("\n## Every fetch, 2 November 2026\n")
    n_inst = sum(1 for f in fetches if f["purpose"] == "instrument")
    n_lit = len(fetches) - n_inst
    ok = sum(1 for f in fetches if f["outcome"].startswith("read") or f["outcome"].startswith("PDF"))
    out.append(f"{len(fetches)} page fetches ({n_inst} for instruments, {n_lit} for papers), of which {ok} returned readable content; redirects and failures are counted as fetches. Searches: 28 (20 survey, 8 literature).\n")
    out.append("| # | Purpose | URL | Outcome |")
    out.append("| --- | --- | --- | --- |")
    for f in fetches:
        out.append(f"| {f['n']} | {f['purpose']} | {f['url']} | {f['outcome']} |")
    (D / "sources.md").write_text("\n".join(out) + "\n")


if __name__ == "__main__":
    write_sources()
    any_layer, primary, other = counts()
    print("included", len(rows))
    for k, v in LAYERS.items():
        print(k, v, "any", any_layer[k], "primary", primary[k],
              "undetermined", other[("undetermined", k)], "unreadable", other[("unreadable", k)])
    print("candidates", Counter(c["class"] for c in cands))
    print("origin a/b/c", Counter(o for r in rows for o in "abc" if r["origin"].startswith(o) or f" {o} (" in r["origin"] or f"and {o}" in r["origin"]))
    print("fetches", len(fetches))
