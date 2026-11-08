"""LH046 analysis: classify each hourly file read and make the brief's comparisons. Offline, from retained counts.

Usage (from the repository root):  python3 -I studies/LH046/scripts/analyse.py studies/LH046/data
Reads hours.csv and minutes.csv; writes files.csv (one row per file, with the derived classes) and results.txt.
Definitions are the brief's (studies/LH046/brief.md, protocol 0.1 and amendment 1).
"""
import csv, json, os, statistics as st, sys
from collections import defaultdict

D = sys.argv[1]
TYPES = ["PushEvent", "CreateEvent", "DeleteEvent", "PullRequestEvent", "PullRequestReviewEvent",
         "PullRequestReviewCommentEvent", "IssuesEvent", "IssueCommentEvent", "WatchEvent", "ForkEvent",
         "ReleaseEvent", "MemberEvent", "PublicEvent", "GollumEvent", "CommitCommentEvent", "DiscussionEvent"]
CONTROL = ["PullRequestEvent", "IssuesEvent", "IssueCommentEvent", "WatchEvent"]
rows = list(csv.DictReader(open(os.path.join(D, "hours.csv"), newline="")))
out = []
P = lambda *a: out.append(" ".join(str(x) for x in a))


def day(r): return r["label"].rsplit("-", 1)[0]
def hr(r): return int(r["label"].rsplit("-", 1)[1])
def ok(r): return r["http_status"] == "200"
def n(r, k): return int(r[k] or 0)


first = {}  # first read of each label (re-reads kept apart)
for r in rows:
    if r["set"] != "reread" and r["label"] not in first:
        first[r["label"]] = r
sets = defaultdict(set)
for r in rows:
    if r["set"] != "reread":
        sets[r["set"]].add(r["label"])
panel = sorted((first[l] for l in sets["panel"]), key=lambda r: (day(r), hr(r)))
refs16 = [first[l] for l in sets["reference"] if l != "2026-04-02-14"]


def med(rs, k):
    v = [n(r, k) for r in rs if ok(r)]
    return st.median(v) if v else None


# --- baselines -------------------------------------------------------------
sept = [r for r in panel if day(r) <= "2026-09-30" and ok(r)]
sept_push_zero = sum(n(r, "PushEvent") == 0 for r in sept)
sept_clean = sept and sept_push_zero / len(sept) <= 0.10
P("== Baseline")
P(f"September panel files read: {len(sept)}; with zero PushEvents: {sept_push_zero} "
  f"({100*sept_push_zero/max(1,len(sept)):.0f}%). Clean-reference test (<=10%): {'passed' if sept_clean else 'FAILED'}")
base_sept = {h: {k: med([r for r in sept if hr(r) == h], k) for k in TYPES + ["events"]} for h in (0, 6, 12, 18)}
base_ref = {k: med(refs16, k) for k in TYPES + ["events"]}
P("September medians by hour of day (events, PushEvent, CreateEvent, control types):")
for h in (0, 6, 12, 18):
    b = base_sept[h]
    P(f"  hour {h:2d}: events {b['events']}, push {b['PushEvent']}, create {b['CreateEvent']}, control {sum(b[k] or 0 for k in CONTROL)}")
P(f"January to August reference medians (16 files, hour 12): events {base_ref['events']}, push {base_ref['PushEvent']}, "
  f"create {base_ref['CreateEvent']}, delete {base_ref['DeleteEvent']}, control {sum(base_ref[k] or 0 for k in CONTROL)}")
OPERATIVE = "september" if sept_clean else "reference"
P(f"Operative baseline (brief, inconclusive clause): {OPERATIVE}")


def baseline(r):
    if OPERATIVE == "reference":
        return base_ref
    h = hr(r)
    near = 0 if h <= 2 or h >= 21 else 6 if h <= 8 else 12 if h <= 14 else 18
    return base_sept[near]


# --- per-file classes --------------------------------------------------------
mins = defaultdict(list)
for m in csv.DictReader(open(os.path.join(D, "minutes.csv"), newline="")):
    mins[(m["label"], m["set"])].append((int(m["minute"]), int(m["events"]), int(m["push_events"]), int(m["create_events"])))

fcols = ["label", "set", "date", "hour", "http_status", "bytes", "events", "PushEvent", "CreateEvent", "DeleteEvent",
         "control", "control_ratio", "events_ratio", "missing", "unread", "empty", "short_hour", "partial_hour",
         "partial_push_hour", "gap_types", "shortfall_types", "outside_hour", "id_span", "events_per_id", "bytes_per_event"]
frows = []
for r in sorted(rows, key=lambda r: (r["set"] == "reread", day(r), hr(r))):
    b = baseline(r)
    f = {"label": r["label"], "set": r["set"], "date": day(r), "hour": hr(r), "http_status": r["http_status"], "bytes": r["bytes"]}
    f["missing"] = int(r["http_status"] == "404")
    f["unread"] = int(not ok(r) and r["http_status"] != "404")
    if ok(r):
        ev = n(r, "events")
        f.update(events=ev, PushEvent=n(r, "PushEvent"), CreateEvent=n(r, "CreateEvent"), DeleteEvent=n(r, "DeleteEvent"))
        ctl = sum(n(r, k) for k in CONTROL)
        bctl = sum(b[k] or 0 for k in CONTROL)
        f["control"] = ctl
        f["control_ratio"] = round(ctl / bctl, 3) if bctl else ""
        f["events_ratio"] = round(ev / b["events"], 3) if b["events"] else ""
        f["empty"] = int(ev == 0)
        f["short_hour"] = int(bool(b["events"]) and ev < 0.5 * b["events"])
        f["partial_hour"] = int(ev > 0 and (n(r, "longest_zero_run_min") >= 5 or n(r, "minutes_with_events") < 55))
        f["partial_push_hour"] = int(n(r, "PushEvent") > 0 and n(r, "longest_zero_push_run_min") >= 5)
        gaps = [k for k in TYPES if (b[k] or 0) >= 100 and n(r, k) == 0]
        short = [k for k in TYPES if (b[k] or 0) >= 100 and 0 < n(r, k) < 0.25 * b[k]]
        f["gap_types"] = " ".join(gaps)
        f["shortfall_types"] = " ".join(short)
        f["outside_hour"] = r["outside_hour"]
        if r["id_min"] and r["id_max"]:
            span = int(r["id_max"]) - int(r["id_min"]) + 1
            f["id_span"] = span
            f["events_per_id"] = round(ev / span, 5)
        f["bytes_per_event"] = round(int(r["bytes"]) / ev) if ev else ""
    frows.append(f)
with open(os.path.join(D, "files.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fcols)
    w.writeheader()
    w.writerows(frows)
F = {(f["label"], f["set"]): f for f in frows}
FF = {f["label"]: f for f in frows if f["set"] != "reread"}

# --- coverage ------------------------------------------------------------------
P("\n== Coverage")
for s in ("panel", "wholeday", "reference", "latest", "reread"):
    rs = [r for r in rows if r["set"] == s]
    P(f"{s}: {len(rs)} rows; 200: {sum(ok(r) for r in rs)}; 404: {sum(r['http_status']=='404' for r in rs)}; "
      f"other: {sum(not ok(r) and r['http_status']!='404' for r in rs)}")
distinct = {r["label"] for r in rows}
P(f"distinct files: {len(distinct)}; unread share of distinct: "
  f"{sum(1 for l in distinct if all(not ok(r) and r['http_status']!='404' for r in rows if r['label']==l))}/{len(distinct)}")
P(f"bytes received (hours.csv rows): {sum(int(r['bytes']) for r in rows):,}")

# --- comparison 1 ------------------------------------------------------------------
P("\n== Comparison 1: PushEvent and CreateEvent gaps in the panel, before and from 15 October")
def share(rs, typ):
    rs = [r for r in rs if ok(r)]
    g = sum(typ in FF[r["label"]]["gap_types"].split() for r in rs)
    return g, len(rs)
for typ in ("PushEvent", "CreateEvent", "DeleteEvent"):
    for h in (None, 0, 6, 12, 18):
        a = [r for r in panel if day(r) <= "2026-10-14" and (h is None or hr(r) == h)]
        c = [r for r in panel if day(r) >= "2026-10-15" and (h is None or hr(r) == h)]
        ga, na = share(a, typ); gc, nc = share(c, typ)
        P(f"  {typ:12s} hour {'all' if h is None else h:>3}: 1 Sep-14 Oct {ga}/{na} ({100*ga/max(1,na):.0f}%); "
          f"15 Oct-7 Nov {gc}/{nc} ({100*gc/max(1,nc):.0f}%)")
P("  Zero-push panel files by month: " + ", ".join(
    f"{m}: {sum(n(r,'PushEvent')==0 for r in panel if ok(r) and day(r)[:7]==m)}/{sum(ok(r) for r in panel if day(r)[:7]==m)}"
    for m in ("2026-09", "2026-10", "2026-11")))
P(f"  Fixed reading: {'applied' if sept_clean else 'not applied (September failed the clean-reference test; described against the references)'}")

# --- comparison 2 ------------------------------------------------------------------
P("\n== Comparison 2: control types (PR, issues, issue comments, stars) against baseline, gap vs non-gap files")
for lo, hi, name in (("2026-09-01", "2026-10-14", "1 Sep-14 Oct"), ("2026-10-15", "2026-11-07", "15 Oct-7 Nov")):
    for g in (True, False):
        rs = [FF[r["label"]] for r in panel if ok(r) and lo <= day(r) <= hi and (("PushEvent" in FF[r["label"]]["gap_types"].split()) == g)]
        cr = [f["control_ratio"] for f in rs if f["control_ratio"] != ""]
        er = [f["events_ratio"] for f in rs if f["events_ratio"] != ""]
        if cr:
            P(f"  {name}, {'push gap' if g else 'pushes present'}: n={len(rs)}, control ratio median {st.median(cr):.2f} "
              f"(range {min(cr):.2f}-{max(cr):.2f}); all-events ratio median {st.median(er):.2f}")
        else:
            P(f"  {name}, {'push gap' if g else 'pushes present'}: n=0")

# --- comparison 3 ------------------------------------------------------------------
P("\n== Comparison 3: whole days, hour by hour (events / PushEvents / CreateEvents; * = partial hour, p = partial push hour)")
for d in sorted({day(first[l]) for l in sets["wholeday"]}):
    cells = []
    for h in range(24):
        f = FF.get(f"{d}-{h}")
        if not f:
            cells.append(f"{h}:?"); continue
        if f["missing"] or f["unread"]:
            cells.append(f"{h}:{f['http_status']}"); continue
        mark = ("*" if f["partial_hour"] else "") + ("p" if f["partial_push_hour"] else "")
        cells.append(f"{h}:{f['events']}/{f['PushEvent']}/{f['CreateEvent']}{mark}")
    P(f"  {d}: " + "  ".join(cells))
P("  Boundary hours (push presence changes between consecutive whole-day hours): per-minute PushEvents, minutes 0-59")
for d in sorted({day(first[l]) for l in sets["wholeday"]}):
    for h in range(24):
        f = FF.get(f"{d}-{h}")
        if not f or not f.get("events"):
            continue
        prev = FF.get(f"{d}-{h-1}") if h else None
        nxt = FF.get(f"{d}-{h+1}") if h < 23 else None
        has = f["PushEvent"] > 0
        boundary = any(o and o.get("events") is not None and (o.get("PushEvent", 0) > 0) != has for o in (prev, nxt))
        if boundary and has:
            ms = sorted(mins[(f["label"], f["set"])])
            P(f"    {f['label']}: push minutes {sum(1 for m in ms if m[2])}/60, longest run without push "
              f"{first[f['label']]['longest_zero_push_run_min']} min; per minute: " + " ".join(str(m[2]) for m in ms))

P("  Control types (PR, issues, issue comments, stars) per file on whole days with both kinds of hour:")
P("  files with no PushEvent against files with PushEvents and no minute without one (per-minute DeleteEvents were not kept,")
P("  so a per-minute comparison of the other types would mix them in; this compares whole files of the same day)")
for d in sorted({day(first[l]) for l in sets["wholeday"]}):
    fs = [FF.get(f"{d}-{h}") for h in range(24)]
    fs = [f for f in fs if f and f.get("events") is not None]
    on = [f["control"] for f in fs if f["PushEvent"] > 0 and not f["partial_push_hour"]]
    off = [f["control"] for f in fs if f["PushEvent"] == 0]
    if on and off:
        P(f"    {d}: no pushes n={len(off)}, control median {st.median(off):,.0f}; pushes all hour n={len(on)}, control median {st.median(on):,.0f}")
P("  Where in the hour pushes stop: minute of the last PushEvent in partial push hours whose pushes start at minute 0")
stops = []
for f in frows:
    if f["set"] == "reread" or not f.get("partial_push_hour"):
        continue
    ms = sorted(mins[(f["label"], f["set"])])
    if ms and ms[0][2] > 0:
        last = max(m for m, _, p, _ in ms if p > 0)
        stops.append((f["label"], last))
P("    " + ", ".join(f"{l}: {m}" for l, m in stops))

# --- comparison 4 ------------------------------------------------------------------
P("\n== Comparison 4: PushEvent payload keys and CreateEvent ref_type across files read")
keysets, refts = defaultdict(list), defaultdict(int)
for r in rows:
    if not ok(r) or r["set"] == "reread":
        continue
    pk = json.loads(r["push_payload_keys"] or "{}")
    if pk:
        ks = tuple(sorted(pk))
        full = all(v == n(r, "PushEvent") for v in pk.values())
        keysets[(ks, full)].append(r["label"])
    for k, v in json.loads(r["create_ref_types"] or "{}").items():
        refts[k] += v
for (ks, full), labs in sorted(keysets.items(), key=lambda x: -len(x[1])):
    P(f"  keys {list(ks)}{'' if full else ' (not on every PushEvent)'}: {len(labs)} files, {min(labs)} to {max(labs)}")
P(f"  push events with a non-empty commits list: {sum(n(r,'push_with_commits') for r in rows if ok(r) and r['set']!='reread')}")
P(f"  CreateEvent ref_type totals: {dict(refts)}")
P("  Mean uncompressed bytes per event, by type, panel files by month:")
for typ in ("PushEvent", "PullRequestEvent", "IssueCommentEvent", "WatchEvent", "CreateEvent"):
    parts = []
    for m in ("2026-09", "2026-10", "2026-11"):
        ub = ev = 0
        for r in panel:
            if ok(r) and day(r)[:7] == m:
                ub += json.loads(r["ubytes_by_type"] or "{}").get(typ, 0); ev += n(r, typ)
        parts.append(f"{m}: {ub/ev:,.0f}" if ev else f"{m}: -")
    ub = ev = 0
    for r in refs16:
        if ok(r):
            ub += json.loads(r["ubytes_by_type"] or "{}").get(typ, 0); ev += n(r, typ)
    parts.append(f"Jan-Aug refs: {ub/ev:,.0f}" if ev else "Jan-Aug refs: -")
    P(f"    {typ}: " + "; ".join(parts))

# --- comparison 5 ------------------------------------------------------------------
P("\n== Comparison 5: stability")
for r in rows:
    if r["set"] == "reread":
        o = first.get(r["label"])
        P(f"  {r['label']}: first {o['utc_read']} {o['bytes']} {o['sha256'][:16]} events {o['events']}; "
          f"re-read {r['utc_read']} {r['bytes']} {r['sha256'][:16]} events {r['events']}; "
          f"{'same' if o['sha256'] == r['sha256'] else 'DIFFERENT'}")
rv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "essays", "what-the-watch-would-see", "reader-review", "fetch-log.tsv")
same = diff = 0
diffs = []
if os.path.exists(rv):
    for line in open(rv):
        p = line.rstrip("\n").split("\t")
        if len(p) >= 6 and "data.gharchive.org" in p[1]:
            lab = p[1].rsplit("/", 1)[1].replace(".json.gz", "")
            o = first.get(lab)
            if o and ok(o):
                if o["sha256"].startswith(p[5]) and o["bytes"] == p[4]:
                    same += 1
                else:
                    diff += 1; diffs.append(f"{lab} reviewer {p[4]} {p[5]} vs {o['bytes']} {o['sha256'][:16]}")
P(f"  against the reviewer's fetch log (size and 16-hex hash prefix): {same} same, {diff} different " + "; ".join(diffs))
o = first.get("2026-04-02-14")
if o:
    P(f"  LH002 2026-04-02-14: recorded 35617941 bytes, 153261 events; now {o['bytes']} bytes, {o['events']} events, "
      f"PushEvent {o['PushEvent']}")
o = first.get("2026-07-01-12")
if o:
    P(f"  LH043 2026-07-01-12: recorded 21587792 bytes, sha256 1c74717a5441b202...; now {o['bytes']}, {o['sha256'][:16]}..., "
      f"{'same' if o['sha256']=='1c74717a5441b202307aefb4c4ffc71f5bfd440509a062c7db387b4b427f03b1' else 'DIFFERENT'}; "
      f"events {o['events']}, PushEvent {o['PushEvent']}, CreateEvent {o['CreateEvent']}")
lm = [r for r in rows if ok(r) and r["last_modified"]]
P(f"  Last-Modified present on {len(lm)} of {sum(ok(r) for r in rows)} files")
late = []
for r in lm:
    from email.utils import parsedate_to_datetime
    import datetime as dt
    t = parsedate_to_datetime(r["last_modified"]).astimezone(dt.timezone.utc)
    d, h = r["label"].rsplit("-", 1)
    end = dt.datetime.fromisoformat(d).replace(tzinfo=dt.timezone.utc) + dt.timedelta(hours=int(h) + 1)
    late.append(((t - end).total_seconds() / 3600, r["label"], r["set"]))
late.sort()
if late:
    P(f"  Hours from the end of the file's hour to Last-Modified: median {st.median(x[0] for x in late):.2f}, "
      f"min {late[0][0]:.2f} ({late[0][1]}), max {late[-1][0]:.2f} ({late[-1][1]})")
    P("  Files written more than 24 hours after their hour: " + ", ".join(f"{l} ({x:.0f} h)" for x, l, s in late if x > 24))

# --- comparison 6 ------------------------------------------------------------------
P("\n== Comparison 6: reference hours, January to August 2026 (and LH002's hour)")
for l in sorted(sets["reference"]):
    f = FF[l]; r = first[l]
    P(f"  {l}: status {f['http_status']}, bytes {f['bytes']}, events {f.get('events','')}, push {f.get('PushEvent','')}, "
      f"create {f.get('CreateEvent','')}, delete {f.get('DeleteEvent','')}, control {f.get('control','')}, "
      f"partial {f.get('partial_hour','')}, gaps [{f.get('gap_types','')}]")

# --- other derived -------------------------------------------------------------------
P("\n== Other derived measures over all first reads")
ok1 = [f for f in FF.values() if f.get("events") is not None and f["http_status"] == "200"]
P(f"empty files: {[f['label'] for f in ok1 if f['empty']]}")
P(f"missing (404): {[f['label'] for f in FF.values() if f['missing']]}; unread: {[f['label'] + ':' + f['http_status'] for f in FF.values() if f['unread']]}")
P(f"partial hours: {len([f for f in ok1 if f['partial_hour']])} of {len(ok1)}: " + ", ".join(f["label"] for f in ok1 if f["partial_hour"]))
P(f"partial push hours: {len([f for f in ok1 if f['partial_push_hour']])}: " + ", ".join(f["label"] for f in ok1 if f["partial_push_hour"]))
P(f"short hours (events < 50% of operative baseline): {len([f for f in ok1 if f['short_hour']])} of {len(ok1)}")
P(f"files with events outside their hour: {len([f for f in ok1 if int(f['outside_hour'] or 0) > 0])}; total such events "
  f"{sum(int(f['outside_hour'] or 0) for f in ok1)}")
pp = [f for f in panel if ok(f)]
for lo, hi, name in (("2026-01-01", "2026-08-31", "Jan-Aug refs"), ("2026-09-01", "2026-10-14", "1 Sep-14 Oct"), ("2026-10-15", "2026-11-08", "15 Oct-8 Nov")):
    src = refs16 if name.startswith("Jan") else [r for r in rows if ok(r) and r["set"] in ("panel", "latest") and lo <= day(r) <= hi]
    for g in (True, False):
        e = [FF[r["label"]]["events_per_id"] for r in src if FF[r["label"]].get("events_per_id") not in (None, "") and (n(r, "PushEvent") == 0) == g]
        if e:
            P(f"  events per event-id step, {name}, {'no pushes' if g else 'pushes present'}: n={len(e)}, median {st.median(e):.4f}")
P("  (Event ids in files with pushes span billions of ids, in files without pushes a few million: the id field mixes ranges,")
P("   so the span measure fixed in the brief is kept in files.csv but not interpreted.)")

P("\n== Runs of consecutive panel (and latest) files without PushEvents, in time order")
seq = sorted([r for r in rows if r["set"] in ("panel", "latest") and ok(r)], key=lambda r: (day(r), hr(r)))
run = []
for r in seq + [None]:
    if r is not None and n(r, "PushEvent") == 0:
        run.append(r["label"]); continue
    if run:
        P(f"  {run[0]} to {run[-1]}: {len(run)} files")
        run = []
P("  Whole-day files without PushEvents: " + ", ".join(
    f"{d}: {sum(1 for h in range(24) if FF.get(f'{d}-{h}', {}).get('PushEvent') == 0)}/24"
    for d in sorted({day(first[l]) for l in sets["wholeday"]})))
P("  Latest files (8 November): " + "; ".join(f"{l}: events {FF[l].get('events')}, push {FF[l].get('PushEvent')}"
                                           for l in sorted(sets["latest"], key=lambda l: int(l.rsplit('-', 1)[1]))))

P("\n== Push-present panel files: PushEvents and all events per file (median, range)")
for lo, hi, name in (("2026-09-01", "2026-10-14", "1 Sep-14 Oct"), ("2026-10-15", "2026-11-07", "15 Oct-7 Nov")):
    rs = [r for r in panel if ok(r) and lo <= day(r) <= hi and n(r, "PushEvent") > 0]
    pv = [n(r, "PushEvent") for r in rs]; ev = [n(r, "events") for r in rs]
    P(f"  {name}: n={len(rs)}; PushEvent median {st.median(pv):,.0f} ({min(pv):,}-{max(pv):,}); events median {st.median(ev):,.0f}")
rv16 = [n(r, "PushEvent") for r in refs16 if ok(r)]
P(f"  January to August references: PushEvent median {st.median(rv16):,.0f} ({min(rv16):,}-{max(rv16):,})")
P("\n== Push-free panel files: all events per file (median, range), and the four control types")
for lo, hi, name in (("2026-09-01", "2026-10-14", "1 Sep-14 Oct"), ("2026-10-15", "2026-11-07", "15 Oct-7 Nov")):
    rs = [r for r in panel if ok(r) and lo <= day(r) <= hi and n(r, "PushEvent") == 0]
    ev = [n(r, "events") for r in rs]; cv = [sum(n(r, k) for k in CONTROL) for r in rs]
    P(f"  {name}: n={len(rs)}; events median {st.median(ev):,.0f} ({min(ev):,}-{max(ev):,}); control median {st.median(cv):,.0f} ({min(cv):,}-{max(cv):,})")
P("  Types present in push-free files (files holding at least one): " + ", ".join(
    f"{k} {sum(1 for r in panel if ok(r) and n(r,'PushEvent')==0 and n(r,k)>0)}" for k in TYPES))
P("  Files (all first reads) holding PushEvents but no CreateEvent or DeleteEvent, or the reverse: " + str(
    [r["label"] for r in first.values() if ok(r) and ((n(r,'PushEvent')>0) != (n(r,'CreateEvent')>0) or (n(r,'PushEvent')>0) != (n(r,'DeleteEvent')>0))]))
open(os.path.join(D, "results.txt"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
