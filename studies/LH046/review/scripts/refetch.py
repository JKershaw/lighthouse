"""LH046 evidence review (R-0056): re-read a sample of GH Archive hourly files, stream and count, keep counts and hashes.

Written by the evidence reviewer, independently of studies/LH046/scripts/collect.py (not imported, not copied).
Usage (from the repository root):
  python3 -I studies/LH046/review/scripts/refetch.py plan        # write review/out/plan.csv (sample + unread hours) and stop
  python3 -I studies/LH046/review/scripts/refetch.py fetch       # read every file in plan.csv not yet in counts.csv
Each file is streamed: the compressed bytes are hashed and decompressed as they arrive, each line parsed and counted,
and nothing of the body is written. Pacing: one request at a time, at least 2 seconds between requests.
Writes review/out/counts.csv (one row per file) and review/out/fetch-log.tsv (every request).
"""
import csv, datetime as dt, hashlib, json, os, random, sys, time, urllib.request, urllib.error, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "out")
STUDY_DATA = os.path.join(HERE, "..", "..", "data")
UA = "Lighthouse-research/1.0 (+https://lighthouse.harbour.cat)"
SEED = 56046  # R-0056, LH046; fixed before drawing
N_SAMPLE = 24
# Unread hours: 3, 9, 15, 21 UTC on five days spaced 16 days apart from 3 September (none is a whole day the study read).
UNREAD_DAYS = ["2026-09-03", "2026-09-19", "2026-10-05", "2026-10-21", "2026-11-06"]
UNREAD_HOURS = [3, 9, 15, 21]
TYPES = ["PushEvent", "CreateEvent", "DeleteEvent", "PullRequestEvent", "PullRequestReviewEvent",
         "PullRequestReviewCommentEvent", "IssuesEvent", "IssueCommentEvent", "WatchEvent", "ForkEvent",
         "ReleaseEvent", "MemberEvent", "PublicEvent", "GollumEvent", "CommitCommentEvent", "DiscussionEvent"]


def plan():
    rows = list(csv.DictReader(open(os.path.join(STUDY_DATA, "hours.csv"), newline="")))
    labels = sorted({r["label"] for r in rows if r["set"] != "reread"})
    rng = random.Random(SEED)
    pick = sorted(rng.sample(labels, N_SAMPLE))
    with open(os.path.join(OUT, "plan.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["label", "kind"])
        for l in pick:
            w.writerow([l, "resample"])
        for d in UNREAD_DAYS:
            for h in UNREAD_HOURS:
                lab = f"{d}-{h}"
                assert lab not in labels, lab
                w.writerow([lab, "unread"])
    print(len(labels), "distinct labels in hours.csv; drew", N_SAMPLE, "with seed", SEED)


class Counter:
    def __init__(self, label):
        d, h = label.rsplit("-", 1)
        self.prefix = f"{d}T{int(h):02d}:"
        self.types, self.push_keys, self.ref_types = {}, {}, {}
        self.events = self.bad = self.outside = self.push_commits = 0
        self.minute_any = [0] * 60
        self.minute_push = [0] * 60
        self.minute_create = [0] * 60
        self.buf = b""

    def feed(self, chunk, final=False):
        self.buf += chunk
        parts = self.buf.split(b"\n")
        self.buf = b"" if final else parts.pop()
        for p in parts:
            if p.strip():
                self.line(p)

    def line(self, p):
        try:
            e = json.loads(p)
        except ValueError:
            self.bad += 1
            return
        self.events += 1
        t = e.get("type")
        self.types[t] = self.types.get(t, 0) + 1
        pl = e.get("payload") or {}
        if t == "PushEvent":
            ks = ",".join(sorted(pl.keys()))
            self.push_keys[ks] = self.push_keys.get(ks, 0) + 1
            if pl.get("commits"):
                self.push_commits += 1
        if t == "CreateEvent":
            rt = str(pl.get("ref_type"))
            self.ref_types[rt] = self.ref_types.get(rt, 0) + 1
        ts = e.get("created_at") or ""
        if ts.startswith(self.prefix):
            m = int(ts[len(self.prefix):len(self.prefix) + 2])
            self.minute_any[m] += 1
            if t == "PushEvent":
                self.minute_push[m] += 1
            if t == "CreateEvent":
                self.minute_create[m] += 1
        else:
            self.outside += 1


def read(label):
    url = f"https://data.gharchive.org/{label}.json.gz"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    t = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    h, n, c = hashlib.sha256(), 0, Counter(label)
    status, lm, err = None, "", ""
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            status, lm = r.status, r.headers.get("Last-Modified", "")
            z = zlib.decompressobj(16 + zlib.MAX_WBITS)
            while True:
                chunk = r.read(1 << 20)
                if not chunk:
                    break
                h.update(chunk); n += len(chunk)
                data = z.decompress(chunk)
                while z.eof and z.unused_data:  # concatenated gzip members
                    rest = z.unused_data
                    z = zlib.decompressobj(16 + zlib.MAX_WBITS)
                    data += z.decompress(rest)
                c.feed(data)
            c.feed(z.flush(), final=True)
    except urllib.error.HTTPError as e:
        status = e.code
    except Exception as e:  # recorded, never retried here
        err = type(e).__name__
    return t, url, status, n, h.hexdigest(), lm, err, c


def fetch():
    plan_rows = list(csv.DictReader(open(os.path.join(OUT, "plan.csv"), newline="")))
    cp, lp = os.path.join(OUT, "counts.csv"), os.path.join(OUT, "fetch-log.tsv")
    done = set()
    if os.path.exists(cp):
        done = {r["label"] for r in csv.DictReader(open(cp, newline=""))}
    cols = (["label", "kind", "utc_read", "http_status", "bytes", "sha256", "last_modified", "error", "events",
             "json_errors", "outside_hour"] + TYPES + ["other_types", "push_payload_keys", "push_with_commits",
             "create_ref_types", "minutes_with_events", "minutes_with_push", "first_push_minute", "last_push_minute",
             "push_by_minute"])
    new = not os.path.exists(cp)
    cf, lf = open(cp, "a", newline=""), open(lp, "a")
    w = csv.DictWriter(cf, cols)
    if new:
        w.writeheader()
    for pr in plan_rows:
        lab = pr["label"]
        if lab in done:
            continue
        t, url, status, n, sha, lm, err, c = read(lab)
        lf.write(f"{t}\t{status}\t{n}\t{sha}\t{url}\t{pr['kind']}\t{err}\n"); lf.flush()
        pm = [i for i in range(60) if c.minute_push[i]]
        row = {"label": lab, "kind": pr["kind"], "utc_read": t, "http_status": status, "bytes": n,
               "sha256": sha if status == 200 and not err else "", "last_modified": lm, "error": err,
               "events": c.events, "json_errors": c.bad, "outside_hour": c.outside,
               "other_types": json.dumps({k: v for k, v in c.types.items() if k not in TYPES}, sort_keys=True),
               "push_payload_keys": json.dumps(c.push_keys, sort_keys=True), "push_with_commits": c.push_commits,
               "create_ref_types": json.dumps(c.ref_types, sort_keys=True),
               "minutes_with_events": sum(1 for x in c.minute_any if x), "minutes_with_push": len(pm),
               "first_push_minute": pm[0] if pm else "", "last_push_minute": pm[-1] if pm else "",
               "push_by_minute": " ".join(map(str, c.minute_push))}
        for ty in TYPES:
            row[ty] = c.types.get(ty, 0)
        w.writerow(row); cf.flush()
        print(t, lab, pr["kind"], status, n, c.events, c.types.get("PushEvent", 0), err, flush=True)
        time.sleep(2.0)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    {"plan": plan, "fetch": fetch}[sys.argv[1]]()
