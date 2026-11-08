"""LH046 collector: read GH Archive hourly files once each, count what they hold, keep the counts.

Usage (from the repository root):
  python3 -I studies/LH046/scripts/collect.py studies/LH046/data            # the brief's sample, resumable
  python3 -I studies/LH046/scripts/collect.py studies/LH046/data --list     # print the sample and stop

Writes, appending (a label already in hours.csv is skipped, so a broken run can resume):
  hours.csv    one row per file read: response, size, hash, headers, counts by type, payload shape, minute coverage
  minutes.csv  one row per file and minute of its hour: events, PushEvents, CreateEvents by created_at
  fetch-log.tsv  every request: UTC time, status, bytes, sha256, URL, set, attempt
Nothing from a file is kept but these counts; actor and repository ids are counted, never written.
Brief: studies/LH046/brief.md (protocol 0.1). Ceiling: 520 requests, 20 GB (amendment 1; was 9 GB), 10 consecutive failures.
"""
import csv, datetime as dt, gzip, hashlib, io, json, os, sys, time, urllib.request, urllib.error

UA = "Lighthouse-research/1.0 (+https://lighthouse.harbour.cat)"
BASE = "https://data.gharchive.org/"
TYPES = ["PushEvent", "CreateEvent", "DeleteEvent", "PullRequestEvent", "PullRequestReviewEvent",
         "PullRequestReviewCommentEvent", "IssuesEvent", "IssueCommentEvent", "WatchEvent", "ForkEvent",
         "ReleaseEvent", "MemberEvent", "PublicEvent", "GollumEvent", "CommitCommentEvent", "DiscussionEvent"]
MAX_REQ, MAX_BYTES, MAX_CONSEC_FAIL = 520, 20 * 10**9, 10  # bytes raised from 9 GB by amendment 1
PAUSE = 1.0


def sample():
    """Return [(label, set)] in reading order, as fixed in the brief."""
    out, seen = [], set()
    def add(d, h, s):
        lab = f"{d.isoformat()}-{h}"
        if lab not in seen:
            seen.add(lab); out.append((lab, s))
    d = dt.date(2026, 9, 1)
    while d <= dt.date(2026, 11, 7):
        for h in (0, 6, 12, 18):
            add(d, h, "panel")
        d += dt.timedelta(days=1)
    for ds in ("2026-09-15", "2026-10-01", "2026-10-07", "2026-10-14",
               "2026-10-15", "2026-10-26", "2026-11-05", "2026-11-07"):
        for h in range(24):
            add(dt.date.fromisoformat(ds), h, "wholeday")
    for m in range(1, 9):
        for day in (1, 15):
            add(dt.date(2026, m, day), 12, "reference")
    add(dt.date(2026, 4, 2), 14, "reference")
    for h in (0, 6, 12):
        add(dt.date(2026, 11, 8), h, "latest")
    rereads = ["2026-10-01-12", "2026-10-15-12", "2026-10-26-12", "2026-11-05-3", "2026-11-07-12", "2026-11-07-18"]
    return out + [(r, "reread") for r in rereads]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            body = r.read()
            return r.status, body, r.headers.get("Last-Modified", ""), r.headers.get("ETag", "")
    except urllib.error.HTTPError as e:
        try:
            e.read()
        except Exception:
            pass
        return e.code, b"", "", ""
    except Exception as e:
        return "ERR:" + type(e).__name__, b"", "", ""


def count(label, body):
    date, hour = label.rsplit("-", 1)
    prefix = f"{date}T{int(hour):02d}:"
    c = dict(lines=0, json_errors=0, events=0, gzip_ok=1, push_with_commits=0, outside_hour=0,
             created_min="", created_max="", id_min="", id_max="")
    by_type, ubytes, push_keys, create_ref = {}, {}, {}, {}
    repos, actors = set(), set()
    per_min = [[0, 0, 0] for _ in range(60)]
    idmin = idmax = None
    try:
        f = gzip.GzipFile(fileobj=io.BytesIO(body))
        for line in f:
            c["lines"] += 1
            try:
                e = json.loads(line)
            except Exception:
                c["json_errors"] += 1
                continue
            c["events"] += 1
            t = e.get("type") or "(none)"
            by_type[t] = by_type.get(t, 0) + 1
            ubytes[t] = ubytes.get(t, 0) + len(line)
            r = (e.get("repo") or {}).get("id")
            if r is not None:
                repos.add(r)
            a = (e.get("actor") or {}).get("id")
            if a is not None:
                actors.add(a)
            p = e.get("payload") or {}
            if t == "PushEvent":
                for k in p:
                    push_keys[k] = push_keys.get(k, 0) + 1
                if p.get("commits"):
                    c["push_with_commits"] += 1
            elif t == "CreateEvent":
                rt = str(p.get("ref_type"))
                create_ref[rt] = create_ref.get(rt, 0) + 1
            ca = e.get("created_at") or ""
            if ca:
                if not c["created_min"] or ca < c["created_min"]:
                    c["created_min"] = ca
                if ca > c["created_max"]:
                    c["created_max"] = ca
                if ca.startswith(prefix):
                    m = int(ca[14:16])
                    per_min[m][0] += 1
                    per_min[m][1] += t == "PushEvent"
                    per_min[m][2] += t == "CreateEvent"
                else:
                    c["outside_hour"] += 1
            try:
                i = int(e.get("id"))
                idmin = i if idmin is None or i < idmin else idmin
                idmax = i if idmax is None or i > idmax else idmax
            except Exception:
                pass
    except Exception as ex:
        c["gzip_ok"] = 0
        c["gzip_error"] = type(ex).__name__
    c["id_min"] = "" if idmin is None else idmin
    c["id_max"] = "" if idmax is None else idmax
    c["distinct_repos"], c["distinct_actors"] = len(repos), len(actors)
    zero = [m for m in range(60) if per_min[m][0] == 0]
    run = best = 0
    for m in range(60):
        run = run + 1 if per_min[m][0] == 0 else 0
        best = max(best, run)
    c["minutes_with_events"] = 60 - len(zero)
    c["longest_zero_run_min"] = best
    prun = pbest = 0
    for m in range(60):
        prun = prun + 1 if per_min[m][1] == 0 else 0
        pbest = max(pbest, prun)
    c["minutes_with_push"] = sum(1 for m in range(60) if per_min[m][1])
    c["longest_zero_push_run_min"] = pbest
    return c, by_type, ubytes, push_keys, create_ref, per_min


HOUR_COLS = (["label", "set", "url", "utc_read", "attempts", "http_status", "bytes", "sha256", "last_modified", "etag",
              "gzip_ok", "gzip_error", "lines", "json_errors", "events"] + TYPES +
             ["other_types", "distinct_repos", "distinct_actors", "push_with_commits", "push_payload_keys",
              "create_ref_types", "ubytes_by_type", "created_min", "created_max", "outside_hour",
              "minutes_with_events", "longest_zero_run_min", "minutes_with_push", "longest_zero_push_run_min",
              "id_min", "id_max"])


def main():
    out = sys.argv[1]
    plan = sample()
    if "--list" in sys.argv:
        for lab, s in plan:
            print(lab, s)
        print(len(plan), "entries,", len({l for l, _ in plan}), "distinct files")
        return
    os.makedirs(out, exist_ok=True)
    hp, mp, lp = (os.path.join(out, n) for n in ("hours.csv", "minutes.csv", "fetch-log.tsv"))
    done = set()
    if os.path.exists(hp):
        with open(hp, newline="") as f:
            done = {(r["label"], r["set"]) for r in csv.DictReader(f)}
    new_h, new_m = not os.path.exists(hp), not os.path.exists(mp)
    hf, mf, lf = open(hp, "a", newline=""), open(mp, "a", newline=""), open(lp, "a")
    hw, mw = csv.DictWriter(hf, HOUR_COLS), csv.writer(mf)
    if new_h:
        hw.writeheader()
    if new_m:
        mw.writerow(["label", "set", "minute", "events", "push_events", "create_events"])
    nreq = nbytes = consec = 0
    if os.path.exists(lp):
        for line in open(lp):
            parts = line.rstrip("\n").split("\t")
            if len(parts) > 2 and parts[2].isdigit():
                nreq += 1; nbytes += int(parts[2])
    for lab, s in plan:
        if (lab, s) in done:
            continue
        url = BASE + lab + ".json.gz"
        attempts = 0
        while True:
            if nreq >= MAX_REQ or nbytes >= MAX_BYTES:
                print("ceiling reached:", nreq, "requests,", nbytes, "bytes"); return
            attempts += 1
            t = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            status, body, lm, et = fetch(url)
            nreq += 1; nbytes += len(body)
            h = hashlib.sha256(body).hexdigest()
            lf.write(f"{t}\t{status}\t{len(body)}\t{h}\t{url}\t{s}\t{attempts}\n"); lf.flush()
            time.sleep(PAUSE)
            if status == 200 or attempts >= 2:
                break
            time.sleep(60 if status in (429, 503) else 5)
        row = {"label": lab, "set": s, "url": url, "utc_read": t, "attempts": attempts, "http_status": status,
               "bytes": len(body), "sha256": h if status == 200 else "", "last_modified": lm, "etag": et}
        if status == 200:
            consec = 0
            c, by_type, ub, pk, cr, pm = count(lab, body)
            row.update({k: v for k, v in c.items() if k in HOUR_COLS})
            for ty in TYPES:
                row[ty] = by_type.get(ty, 0)
            row["other_types"] = json.dumps({k: v for k, v in by_type.items() if k not in TYPES}, sort_keys=True)
            row["push_payload_keys"] = json.dumps(pk, sort_keys=True)
            row["create_ref_types"] = json.dumps(cr, sort_keys=True)
            row["ubytes_by_type"] = json.dumps(ub, sort_keys=True)
            for m in range(60):
                mw.writerow([lab, s, m] + pm[m])
            mf.flush()
        else:
            consec += 1
        del body
        hw.writerow(row); hf.flush()
        print(t, lab, s, status, row["bytes"], row.get("events", ""), row.get("PushEvent", ""), flush=True)
        if consec >= MAX_CONSEC_FAIL:
            print("stopping: 10 consecutive failures"); return
    print("done:", nreq, "requests,", nbytes, "bytes")


if __name__ == "__main__":
    main()
