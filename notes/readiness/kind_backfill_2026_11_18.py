"""Fill the blank `kind` of historical schedule rows (18 November 2026, at the
keeper's request). Rule 1: a dated repeat takes the kind of later typed rows of
the same task (the id with its date or number replaced) when they agree on one
kind. Rule 2: the rest are classified by hand from their task text, below.
A row whose main act is a read is `observe`, as the current twice-weekly rows
are typed even though they also tabulate. Run from the repository root:
python3 -I notes/readiness/kind_backfill_2026_11_18.py [--apply]"""
import csv, io, re, sys

HAND = {
    "observe": "LH013-run LH035-survey php-leads LH031-criteria LH036-baseline LH035-raw-reread "
               "LH039-raw-2026-11-08 LH039-raw-2026-11-09 LH039-raw-2026-11-10 LH039-raw-2026-11-11 "
               "LH039-raw-2026-11-12 LH039-raw-2026-11-13 LH039-raw-2026-11-14 LH040-read-1 "
               "LH045-capture-0 LH045-census-1 LH041-read-1 LH048-discover LH048-baseline "
               "LH050-baseline LH051-first LH052-iteration-1 LH052-iteration-2",
    "plan": "contact-rules PANW-reread-amendment appliance-panel-brief LH037-routes "
            "disclosure-timeline-brief five-chains-brief LH013-installer-brief P-0017-brief P-0015-brief "
            "P-0014-page P-0013-brief LH041-amend2-scripts LH047-brief P-0026-brief P-0025-amendment "
            "LH034-amend-unlisted LH037-amend-keyword P-0029-brief LH050-amend-ukraine LH052-protocol LH052-close",
    "analyse": "LH019-record LH024-synthesis LH025-summary LH030-interim php-flags-2026-11-02 LH035-next "
               "LH040-checkpoint LH046-record LH047-record LH047-paper-draft",
    "review": "LH013-reader LH042-review watch-see-claims watch-see-reader watch-see-recheck LH041-reviews "
              "LH046-review LH047-review LH052-evidence-review LH052-reader-review",
    "publish": "php-later-evidence-10-30 LH035-map-page LH046-notices",
    "maintain": "robots-sweep-1 use-reference-1 ux-1-model ux-2-paths ux-3-preview ux-4-land ux-5-answer "
                "ux-6-daily gap-licence gap-indexes gap-stale-pages ai-cost-page-tidy",
}
hand = {i: k for k, ids in HAND.items() for i in ids.split()}

path = "schedule/due.csv"
text = open(path, newline="").read()
rows = list(csv.DictReader(io.StringIO(text)))
fields = rows[0].keys()
pat = lambda i: re.sub(r"\d{4}-\d{2}-\d{2}", "D", re.sub(r"-\d{2}$", "-N", i))
typed = {}
for r in rows:
    if r["kind"]:
        typed.setdefault(pat(r["id"]), set()).add(r["kind"])
changes, missing = [], []
for r in rows:
    if r["kind"]:
        continue
    sib = typed.get(pat(r["id"]))
    if sib and len(sib) == 1:
        kind, rule = next(iter(sib)), "sibling"
    elif r["id"] in hand:
        kind, rule = hand[r["id"]], "hand"
    else:
        missing.append(r["id"]); continue
    changes.append((r["id"], r["status"], kind, rule))
    r["kind"] = kind
for c in changes:
    print(",".join(c))
if missing:
    sys.exit(f"unclassified: {missing}")
if "--apply" in sys.argv:
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
    w.writeheader(); w.writerows(rows)
    open(path, "w", newline="").write(out.getvalue())
