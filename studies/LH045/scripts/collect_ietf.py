#!/usr/bin/env python3
"""LH045 part C: a census of agent, discovery, bot-authentication and AI-preference
Internet-Drafts from the IETF Datatracker's read-only API, under brief.md (protocol 0.1,
8 November 2026). The census rule is the brief's and is fixed here:

  group stratum: drafts whose group is aipref, webbotauth, agentproto, dawn or audit;
  name stratum: drafts whose name contains one of NAME_TOKENS, or ends with one of
  NAME_SUFFIXES (amendment 0.2 added "-dawn-", "-audit-", "-dawn" and "-audit").

Checks robots.txt first and skips any URL it disallows. GETs paced at about one a second;
every body kept under data/ietf/raw-<label>/ with readlog.csv, except that author records
are kept with each email address replaced by a placeholder (the brief's one departure from
raw retention). Derives census.csv and authors.csv. Idempotent: a label already held is
not fetched again; --derive-only rebuilds the derived tables from the kept bodies.
Usage: python3 -I studies/LH045/scripts/collect_ietf.py --read 2026-11-08T1945Z
"""
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', '..', 'scripts'))
from redact_emails import redact_bytes  # noqa: E402
import argparse, csv, datetime, hashlib, json, os, re, sys, time
import urllib.error, urllib.parse, urllib.request, urllib.robotparser

UA = "Lighthouse-research/1.0 (+https://lighthouse.harbour.cat)"
BASE = "https://datatracker.ietf.org"
GROUPS = ["aipref", "webbotauth", "agentproto", "dawn", "audit"]
NAME_TOKENS = ["agent", "aipref", "ai-pref", "webbotauth", "web-bot-auth", "botauth", "bot-auth",
               "crawler", "robots", "llm", "-ai-",
               # Amendment 0.2 (8 November 2026, after census 0a): the acronyms of the two
               # groups whose individual drafts carry no other token.
               "-dawn-", "-audit-"]
NAME_SUFFIXES = ["-ai", "-dawn", "-audit"]
PAGE = 500
AUTHOR_BATCH = 50

class Reader:
    def __init__(self, d):
        self.d = d; self.n = 0
        self.log = open(os.path.join(d, "readlog.csv"), "w", newline="")
        self.w = csv.writer(self.log)
        self.w.writerow(["file", "url", "utc_start", "status", "content_type", "size", "sha256", "note"])
        self.rp = None

    def get(self, name, url, redact_email=False):
        time.sleep(1)
        t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        fn = "%03d-%s.body" % (self.n, name); self.n += 1
        if self.rp is not None and not self.rp.can_fetch(UA, url):
            self.w.writerow([fn, url, t, "skipped", "", 0, "", "disallowed by robots.txt"]); return None, None
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json, text/plain, */*"})
        note = ""
        for attempt in (1, 2):
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    st, ct, body = r.status, r.headers.get("Content-Type", ""), r.read(64 << 20)
                break
            except urllib.error.HTTPError as e:
                st, ct, body, note = e.code, e.headers.get("Content-Type", ""), e.read() or b"", "http error"; break
            except Exception as e:  # one retry after a connection reset, as the brief allows
                st, ct, body, note = "error", "", repr(e).encode(), "no response"
                if attempt == 2 or "reset" not in repr(e).lower():
                    break
                time.sleep(5)
        sha_received = hashlib.sha256(body).hexdigest()
        if redact_email and st == 200:
            try:
                j = json.loads(body)
                for o in j.get("objects", []):
                    if "email" in o:
                        o["email"] = "[withheld by Lighthouse]"
                body = json.dumps(j, ensure_ascii=False).encode()
                note = "email fields replaced; sha256 is of the bytes received"
            except ValueError:
                note = "redaction failed; body withheld"; body = b""
        body, n_red = redact_bytes(body)  # the keeper, 8 November 2026: email addresses withheld
        if n_red:
            note = (note + "; " if note else "") + "%d email addresses withheld; sha256 is of the bytes received" % n_red
        open(os.path.join(self.d, fn), "wb").write(body)
        self.w.writerow([fn, url, t, st, ct, len(body), sha_received, note]); self.log.flush()
        print(fn, st, len(body))
        return st, body

    def get_all(self, name, path, params):
        """Follow a list endpoint's pages; return objects, or None if any page failed."""
        objs, offset = [], 0
        while True:
            q = dict(params, format="json", limit=PAGE, offset=offset)
            st, body = self.get(name, BASE + path + "?" + urllib.parse.urlencode(q))
            if st != 200:
                return None
            j = json.loads(body); objs += j["objects"]
            if not j["meta"].get("next"):
                return objs
            offset += PAGE

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--read", required=True, help="UTC label YYYY-MM-DDTHHMMZ, the minute the collector starts")
    ap.add_argument("--derive-only", action="store_true")
    a = ap.parse_args()
    if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d{4}Z", a.read):
        sys.exit("label must look like 2026-11-08T1945Z")
    here = os.path.dirname(os.path.abspath(__file__))
    d = os.path.normpath(os.path.join(here, "..", "data", "ietf", "raw-" + a.read))
    if a.derive_only:
        derive(d); return
    if os.path.exists(d):
        print("already held:", d); return
    os.makedirs(d)
    R = Reader(d)
    st, body = R.get("robots", BASE + "/robots.txt")
    if st == 200:
        R.rp = urllib.robotparser.RobotFileParser(); R.rp.parse(body.decode("utf-8", "replace").splitlines())
    R.get("meeting127", BASE + "/api/v1/meeting/meeting/?format=json&number=127")
    R.get("agenda127", BASE + "/meeting/127/agenda.txt")
    st, body = R.get("groups", BASE + "/api/v1/group/group/?format=json&acronym__in=" + ",".join(GROUPS))
    groups = {g["acronym"]: g["id"] for g in json.loads(body)["objects"]} if st == 200 else {}
    queries = {}
    for acr in GROUPS:
        if acr in groups:
            queries["group:" + acr] = R.get_all("docs-group-" + acr, "/api/v1/doc/document/", {"type": "draft", "group": groups[acr]})
        else:
            queries["group:" + acr] = None
    for tok in NAME_TOKENS:
        queries["name:" + tok] = R.get_all("docs-name-" + tok.strip("-"), "/api/v1/doc/document/", {"type": "draft", "name__contains": tok})
    for suf in NAME_SUFFIXES:
        queries["suffix:" + suf] = R.get_all("docs-suffix-" + suf.strip("-"), "/api/v1/doc/document/", {"type": "draft", "name__endswith": suf})
    R.get_all("states", "/api/v1/doc/state/", {"type__slug__in": "draft,draft-stream-ietf,draft-iesg,draft-iana-review,draft-rfceditor"})
    docs = {}
    for key, objs in queries.items():
        for o in objs or []:
            docs.setdefault(o["name"], o)
    gref = sorted({int(o["group"].rstrip("/").split("/")[-1]) for o in docs.values() if o.get("group")}
                  - set(groups.values()))
    for i in range(0, len(gref), AUTHOR_BATCH):
        q = {"format": "json", "limit": PAGE, "id__in": ",".join(map(str, gref[i:i + AUTHOR_BATCH]))}
        R.get("groups-ref", BASE + "/api/v1/group/group/?" + urllib.parse.urlencode(q))
    ids = sorted(o["id"] for o in docs.values())
    for i in range(0, len(ids), AUTHOR_BATCH):
        batch = ids[i:i + AUTHOR_BATCH]
        q = {"format": "json", "limit": PAGE, "document__in": ",".join(map(str, batch))}
        R.get("authors", BASE + "/api/v1/doc/documentauthor/?" + urllib.parse.urlencode(q), redact_email=True)
    day = datetime.datetime.strptime(a.read, "%Y-%m-%dT%H%MZ")
    for n in (14, 30):
        since = (day - datetime.timedelta(days=n)).strftime("%Y-%m-%dT%H:%M:%S")
        R.get("baseline-%dd" % n, BASE + "/api/v1/doc/document/?" + urllib.parse.urlencode(
            {"format": "json", "limit": 1, "type": "draft", "time__gte": since}))
    json.dump({k: (None if v is None else len(v)) for k, v in queries.items()},
              open(os.path.join(d, "query-counts.json"), "w"), indent=1)
    R.log.close()
    derive(d)

def derive(d):
    files = sorted(f for f in os.listdir(d) if f.endswith(".body"))
    log = {r["file"]: r for r in csv.DictReader(open(os.path.join(d, "readlog.csv")))}
    def objs(prefix):
        out = []
        for f in files:
            if f[4:].startswith(prefix) and str(log.get(f, {}).get("status")) == "200":
                try:
                    out += json.load(open(os.path.join(d, f)))["objects"]
                except (ValueError, KeyError):
                    pass
        return out
    gobjs = objs("groups")
    gid = {g["resource_uri"]: g["acronym"] for g in gobjs}
    states = {s["resource_uri"]: "%s:%s" % (s["type"].rstrip("/").split("/")[-1], s["slug"]) for s in objs("states")}
    rows = {}
    for f in files:
        m = re.match(r"\d{3}-docs-(group|name|suffix)-(.+)\.body$", f)
        if not m or str(log.get(f, {}).get("status")) != "200":
            continue
        kind, tok = m.groups()
        for o in json.load(open(os.path.join(d, f)))["objects"]:
            r = rows.setdefault(o["name"], {"o": o, "strata": set(), "tokens": set()})
            if kind == "group":
                r["strata"].add("group"); r["tokens"].add("group:" + tok)
            else:
                r["strata"].add("name"); r["tokens"].add(tok if kind == "name" else "suffix:-" + tok)
    cols = ["name", "id", "rev", "title", "time", "expires", "group", "stream", "intended_std_level",
            "states", "pages", "strata", "tokens", "abstract"]
    with open(os.path.join(d, "census.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(cols)
        for name in sorted(rows):
            o, r = rows[name]["o"], rows[name]
            g = o.get("group") or ""
            w.writerow([name, o.get("id"), o.get("rev"), o.get("title"), o.get("time"), o.get("expires"),
                        gid.get(g, g.rstrip("/").split("/")[-1]),
                        (o.get("stream") or "").rstrip("/").split("/")[-1],
                        (o.get("intended_std_level") or "").rstrip("/").split("/")[-1],
                        ";".join(sorted(states.get(s, s) for s in o.get("states") or [])),
                        o.get("pages"), ";".join(sorted(r["strata"])), ";".join(sorted(r["tokens"])),
                        (o.get("abstract") or "").replace("\r", " ").replace("\n", " ")])
    with open(os.path.join(d, "authors.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["draft", "order", "affiliation", "country", "person"])
        seen = set()
        for o in objs("authors"):
            if o["id"] in seen:
                continue
            seen.add(o["id"])
            w.writerow([o["document"].rstrip("/").split("/")[-1], o.get("order"), o.get("affiliation"),
                        o.get("country"), (o.get("person") or "").rstrip("/").split("/")[-1]])
    print("census.csv:", len(rows), "drafts; authors.csv:", len(seen), "author lines")

if __name__ == "__main__":
    main()
