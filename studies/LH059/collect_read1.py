#!/usr/bin/env python3
"""LH059 first-read collector (row LH059-read-1), implementing studies/LH059/brief.md protocol 0.1,
"Sources and event definitions". It changes nothing in that section.

Usage (always LIGHTHOUSE_PROVIDER set, always python3 -I):
  python3 -I studies/LH059/collect_read1.py fetch  <label> <localdir> <Dn=url>...
  python3 -I studies/LH059/collect_read1.py keepD1 <label> <localdir>
  python3 -I studies/LH059/collect_read1.py derive <label> <Dn> <extracted.json>

fetch: for each Dn=url, ask the robots gate in the one-off mode (access='oneoff'; the keeper,
21 November 2026), then make one GET through scripts/lh_fetch.py's urlopen (redirects checked
against robots.txt), with one retry only on a timeout, a connection error or HTTP 500, 502 or 504
(brief, Missing evidence). A refusal, challenge, rate limit, 403 or 503 is logged and not retried.
Each request is logged to data/<label>/fetch_log.jsonl with UTC times, URL, status, bytes and the
sha256 of the bytes received. The bytes received are held for this run only in <localdir> (outside
the repository; never committed), so fields can be taken from them. For the JSON records D2 to D6
the brief's fields are extracted here (extract_*) and written with write_derived; no body is kept.
D7 and D8 (HTML reports) are read from the local text and their derived files written with
`derive`. D1's text is checked for indicators before anything is written, then `keepD1` withholds
email addresses, IPv4 addresses, defanged indicators, key- and hash-shaped strings, and each
literal phrase listed in the local file D1.extra_withhold (one per line, kept only in <localdir>:
hostnames in an indicator passage, and the passages that describe the exploit mechanism, which the
driver's instruction for this read withholds), and writes the body only through save_body. No link inside a fetched document is followed. Nothing
fetched is executed.
"""
import datetime, gzip, hashlib, json, os, re, sys, time
from urllib.error import HTTPError, URLError
from urllib.request import Request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from lh_fetch import UA, NotFetched, check, urlopen, save_body, keep_decision, write_derived  # noqa: E402
from redact_emails import redact_bytes  # noqa: E402
from reader_view import View  # noqa: E402

CVE = "CVE-2026-133968"
ACCESS = "oneoff"

PATTERNS = [  # as LH055's collector, plus hash-shaped strings
    (re.compile(rb"\b\d{1,3}(?:(?:\[\.\]|\.)\d{1,3}){3}(?:/\d{1,2})?\b"), b"[ipv4 withheld]"),
    (re.compile(rb"\b(?:sk|pk|rk)-[A-Za-z0-9_\-]{16,}"), b"[key withheld]"),
    (re.compile(rb"\bAKIA[0-9A-Z]{16}\b"), b"[key withheld]"),
    (re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{20,}"), b"[key withheld]"),
    (re.compile(rb"\bAIza[0-9A-Za-z_\-]{30,}"), b"[key withheld]"),
    (re.compile(rb"hxxps?://\S+", re.I), b"[defanged indicator withheld]"),
    (re.compile(rb"\b[\w\-]+(?:\[\.\][\w\-]+)+\b"), b"[defanged indicator withheld]"),
    (re.compile(rb"(?<![0-9A-Fa-f])[0-9A-Fa-f]{64}(?![0-9A-Fa-f])"), b"[hash withheld]"),
    (re.compile(rb"(?<![0-9A-Fa-f])[0-9A-Fa-f]{40}(?![0-9A-Fa-f])"), b"[hash withheld]"),
    (re.compile(rb"(?<![0-9A-Fa-f])[0-9A-Fa-f]{32}(?![0-9A-Fa-f])"), b"[hash withheld]"),
]


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def outdir(label):
    d = os.path.join(HERE, "data", "read-" + label)
    os.makedirs(os.path.join(d, "derived"), exist_ok=True)
    os.makedirs(os.path.join(d, "robots"), exist_ok=True)
    return d


def to_text(body):
    v = View()
    v.feed(body.decode("utf-8", "replace"))
    v.flush()
    return "\n".join(v.out)


def withhold(b, extra=()):
    b, n_email = redact_bytes(b)
    counts = {"email": n_email}
    for pat, rep in PATTERNS:
        b, n = pat.subn(rep, b)
        counts[rep.decode()] = counts.get(rep.decode(), 0) + n
    for phrase in extra:
        b, n = re.subn(re.escape(phrase.encode()), b"[detail withheld by Lighthouse]", b, flags=re.I)
        counts["[detail withheld by Lighthouse]"] = counts.get("[detail withheld by Lighthouse]", 0) + n
    return b, counts


def get_once(url):
    """One GET; returns (outcome, status, final, ctype, headers, body, error)."""
    try:
        with urlopen(Request(url, headers={"User-Agent": UA, "Accept": "*/*"}), timeout=60,
                     check_redirects=True, access=ACCESS) as r:
            hdr = {k: r.headers.get(k) for k in ("Content-Type", "Last-Modified", "ETag", "Date",
                                                  "Content-Length", "X-RateLimit-Remaining")}
            return "received", r.status, r.geturl(), r.headers.get("Content-Type", ""), hdr, r.read(), "", r.headers
    except NotFetched as e:
        return "not_fetched_robots", None, url, "", {}, b"", str(e)[:300], None
    except HTTPError as e:
        body = e.read() if hasattr(e, "read") else b""
        ct = e.headers.get("Content-Type", "") if e.headers else ""
        return "http_error", e.code, url, ct, {}, body, str(e)[:200], e.headers
    except (URLError, OSError) as e:
        return "network_error", None, url, "", {}, b"", str(e)[:300], None


# ---------------------------------------------------------------- field extraction (brief, D2 to D6)

def extract_D2_osv(d):
    """OSV's record, classed as relaying GitHub's advisory record (brief, D2)."""
    refs = d.get("references") or []
    kinds = {}
    for r in refs:
        kinds[r.get("type", "")] = kinds.get(r.get("type", ""), 0) + 1
    aff = []
    for a in d.get("affected") or []:
        rng = []
        for rg in a.get("ranges") or []:
            rng.append({"type": rg.get("type"), "events": rg.get("events")})
        aff.append({"package": (a.get("package") or {}).get("name"), "ecosystem": (a.get("package") or {}).get("ecosystem"),
                    "ranges": rng, "versions_listed": len(a.get("versions") or [])})
    ds = d.get("database_specific") or {}
    return {"route": "OSV relay of GitHub's advisory record", "id": d.get("id"), "aliases": d.get("aliases"),
            "summary_line": d.get("summary"), "published": d.get("published"), "modified": d.get("modified"),
            "withdrawn": d.get("withdrawn"),
            "severity_vectors_count": len(d.get("severity") or []),
            "database_specific": {k: ds.get(k) for k in ("severity", "cwe_ids", "github_reviewed",
                                                          "github_reviewed_at", "nvd_published_at")},
            "affected": aff, "references_count": len(refs), "references_kinds": kinds,
            "credits_count": len(d.get("credits") or [])}


def extract_D2(body):
    data = json.loads(body)
    if isinstance(data, dict) and "aliases" in data and "id" in data:
        return extract_D2_osv(data)
    recs = data if isinstance(data, list) else [data]
    out = []
    for a in recs:
        refs = a.get("references") or []
        kinds = {}
        for r in refs:
            u = r if isinstance(r, str) else r.get("url", "")
            m = re.match(r"https?://([^/]+)/([^/]+/[^/]+/)?([^/]+)?", u)
            host = m.group(1) if m else ""
            kind = host
            if host == "github.com" and m:
                seg = (m.group(3) or "")
                kind = "github.com/<repo>/" + seg if seg else "github.com"
            kinds[kind] = kinds.get(kind, 0) + 1
        out.append({
            "ghsa_id": a.get("ghsa_id"), "cve_id": a.get("cve_id"), "type": a.get("type"),
            "summary_line": a.get("summary"), "published_at": a.get("published_at"),
            "updated_at": a.get("updated_at"), "github_reviewed_at": a.get("github_reviewed_at"),
            "nvd_published_at": a.get("nvd_published_at"), "withdrawn_at": a.get("withdrawn_at"),
            "severity": a.get("severity"),
            "cvss": {k: (a.get("cvss_severities") or {}).get(k, {}).get("score") for k in ("cvss_v3", "cvss_v4")},
            "cwes": [(c.get("cwe_id"), c.get("name")) for c in (a.get("cwes") or [])],
            "vulnerabilities": [{"package": (v.get("package") or {}).get("name"),
                                 "ecosystem": (v.get("package") or {}).get("ecosystem"),
                                 "vulnerable_version_range": v.get("vulnerable_version_range"),
                                 "first_patched_version": v.get("first_patched_version")}
                                for v in (a.get("vulnerabilities") or [])],
            "source_code_location": a.get("source_code_location"),
            "credits_count": len(a.get("credits") or []),
            "credit_types": sorted({c.get("type", "") for c in (a.get("credits") or [])}),
            "references_count": len(refs), "references_kinds": kinds,
            "description_names_discoverer_or_basis": None,  # filled by hand from the local copy, if at all
        })
    return {"records_returned": len(recs), "advisories": out}


def extract_D3(body):
    d = json.loads(body)
    md = d.get("cveMetadata", {})
    cna = (d.get("containers") or {}).get("cna", {})
    pts = []
    for pt in cna.get("problemTypes") or []:
        for de in pt.get("descriptions") or []:
            pts.append({"cweId": de.get("cweId"), "description": de.get("description")})
    metrics = []
    for m in cna.get("metrics") or []:
        for k, v in m.items():
            if isinstance(v, dict) and "baseScore" in v:
                metrics.append({"kind": k, "baseScore": v.get("baseScore"), "baseSeverity": v.get("baseSeverity")})
    adp = [a.get("providerMetadata", {}).get("shortName") for a in (d.get("containers") or {}).get("adp") or []]
    return {"cveId": md.get("cveId"), "state": md.get("state"), "assignerShortName": md.get("assignerShortName"),
            "datePublished": md.get("datePublished"), "dateUpdated": md.get("dateUpdated"),
            "dateReserved_not_a_public_date": md.get("dateReserved"),
            "cna_title": cna.get("title"), "problemTypes": pts, "cna_metrics": metrics,
            "cna_datePublic": cna.get("datePublic"),
            "credits_count": len(cna.get("credits") or []),
            "credit_types": sorted({c.get("type", "") for c in (cna.get("credits") or [])}),
            "references_count": len(cna.get("references") or []), "adp_containers": adp}


def extract_D4(body):
    d = json.loads(body)
    vs = d.get("vulnerabilities") or []
    out = {"totalResults": d.get("totalResults"), "timestamp": d.get("timestamp")}
    if vs:
        c = vs[0].get("cve", {})
        out.update(id=c.get("id"), published=c.get("published"), lastModified=c.get("lastModified"),
                   vulnStatus=c.get("vulnStatus"), sourceIdentifier=c.get("sourceIdentifier"),
                   cisaExploitAdd=c.get("cisaExploitAdd"), cisaActionDue=c.get("cisaActionDue"),
                   cisaVulnerabilityName=c.get("cisaVulnerabilityName"),
                   weaknesses=[[x.get("value") for x in w.get("description", [])] for w in c.get("weaknesses") or []],
                   references_count=len(c.get("references") or []))
    return out


def extract_D5(body):
    d = json.loads(body)
    ent = [v for v in d.get("vulnerabilities") or [] if v.get("cveID") == CVE]
    out = {"catalogVersion": d.get("catalogVersion"), "dateReleased": d.get("dateReleased"), "count": d.get("count"),
           "entries_found": len(ent)}
    if ent:
        e = ent[0]
        out.update({k: e.get(k) for k in ("cveID", "vendorProject", "product", "vulnerabilityName", "dateAdded",
                                         "shortDescription", "requiredAction", "dueDate",
                                         "knownRansomwareCampaignUse", "notes", "cwes")})
    return out


def extract_D6(body):
    d = json.loads(body)
    rels = d if isinstance(d, list) else [d]
    out = []
    for r in rels:
        notes = r.get("body") or ""
        out.append({"tag_name": r.get("tag_name"), "name": r.get("name"), "published_at": r.get("published_at"),
                    "created_at": r.get("created_at"), "draft": r.get("draft"), "prerelease": r.get("prerelease"),
                    "notes_name_cve": CVE.lower() in notes.lower(),
                    "notes_name_ghsa": bool(re.search(r"GHSA-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}", notes, re.I)),
                    "notes_mention_security_word": bool(re.search(r"securit|vulnerab|advisor", notes, re.I))})
    return {"releases_returned": len(rels), "releases": out}


EXTRACT = {"D2": extract_D2, "D3": extract_D3, "D4": extract_D4, "D5": extract_D5, "D6": extract_D6}


def fetch(label, localdir, pairs):
    out = outdir(label)
    os.makedirs(localdir, exist_ok=True)
    log = open(os.path.join(out, "fetch_log.jsonl"), "a")
    for pair in pairs:
        did, url = pair.split("=", 1)
        ok, info = check(url, ACCESS)
        json.dump(info, open(os.path.join(out, "robots", did + ".json"), "w"), indent=1, sort_keys=True)
        attempt = 0
        while True:
            attempt += 1
            rec = {"id": did, "requested_url": url, "attempt": attempt, "access": ACCESS,
                   "provider": os.environ.get("LIGHTHOUSE_PROVIDER", ""), "user_agent": UA, "started": now(),
                   "robots_ok": ok, "robots_ref": "robots/%s.json" % did}
            if not ok:
                rec.update(outcome="not_fetched_robots", reason=info.get("reason"), finished=now())
                log.write(json.dumps(rec) + "\n"); log.flush()
                print(did, "NotFetched (robots)", info.get("reason"))
                break
            outcome, status, final, ctype, hdr, body, err, rh = get_once(url)
            rec.update(outcome=outcome, status=status, final_url=final, content_type=ctype, headers=hdr,
                       received_bytes=len(body), received_sha256=hashlib.sha256(body).hexdigest() if body else "",
                       error=err, finished=now())
            retry = attempt == 1 and (outcome == "network_error" and "timed out" in err.lower() or
                                      outcome == "network_error" or status in (500, 502, 504))
            if outcome == "not_fetched_robots":
                retry = False
            if outcome == "received" or body:
                ext = ".json" if "json" in (ctype or "") else ".html"
                open(os.path.join(localdir, did + ext), "wb").write(body)  # this run only, outside the repo
                if ext == ".html":
                    open(os.path.join(localdir, did + ".txt"), "w").write(to_text(body))
            if outcome == "received":
                kd = keep_decision(final or url, body, rh, ACCESS)
                rec["keep_decision"] = {"keep": kd[0], "reason": kd[1]}
                if did in EXTRACT and "json" in (ctype or ""):
                    try:
                        ex = EXTRACT[did](body)
                    except Exception as e:  # a parse failure is logged, never guessed round
                        ex = {"parse_error": str(e)[:200]}
                    path = os.path.join(out, "derived", did + ".json")
                    write_derived(path, final or url,
                                  "derived only under the brief (D2 to D8 keep no body)" +
                                  ("" if kd[0] else "; keep rule also refuses: " + kd[1]), ex,
                                  read_utc=rec["started"], finish_utc=rec["finished"], http_status=status,
                                  content_type=ctype, bytes=len(body), sha256=rec["received_sha256"],
                                  used_for="LH059 %s, brief protocol 0.1" % did)
                    rec["derived"] = "derived/%s.json" % did
                elif did == "D1":
                    rec["body_kept"] = "pending indicator check (keepD1)"
                else:
                    rec["derived"] = "pending hand extraction (derive)"
            log.write(json.dumps(rec) + "\n"); log.flush()
            print(did, outcome, status, final, ctype, len(body), err)
            if not retry:
                break
            time.sleep(5)


def keepD1(label, localdir):
    out = outdir(label)
    body = open(os.path.join(localdir, "D1.html"), "rb").read()
    extra_path = os.path.join(localdir, "D1.extra_withhold")
    extra = [l.strip() for l in open(extra_path)] if os.path.exists(extra_path) else []
    extra = [e for e in extra if e]
    recs = [json.loads(l) for l in open(os.path.join(out, "fetch_log.jsonl"))]
    rec = [r for r in recs if r["id"] == "D1" and r["outcome"] == "received"][-1]
    kept, counts = withhold(body, extra)
    text, tcounts = withhold(to_text(body).encode("utf-8"), extra)
    ok, why = save_body(os.path.join(out, "D1.html.gz"), kept, rec["final_url"], {"Content-Type": rec["content_type"]},
                        ACCESS)
    note = {"id": "D1", "decided": now(), "save_body": {"kept": ok, "reason": why},
            "withheld_body": counts, "withheld_text": tcounts,
            "extra_phrases_withheld": len(extra),
            "received_sha256": rec["received_sha256"]}
    if ok:
        open(os.path.join(out, "D1.txt"), "wb").write(text)
        note.update(retained_body="D1.html.gz", retained_text="D1.txt",
                    retained_sha256=hashlib.sha256(gzip.decompress(open(os.path.join(out, "D1.html.gz"), "rb").read())).hexdigest())
    json.dump(note, open(os.path.join(out, "D1_keep.json"), "w"), indent=1)
    print(json.dumps(note, indent=1))


def derive(label, did, exfile):
    out = outdir(label)
    ex = json.load(open(exfile))
    recs = [json.loads(l) for l in open(os.path.join(out, "fetch_log.jsonl"))]
    rec = [r for r in recs if r["id"] == did][-1]
    write_derived(os.path.join(out, "derived", did + ".json"), rec.get("final_url") or rec["requested_url"],
                  "derived only under the brief (D2 to D8 keep no body)" +
                  ("" if rec.get("keep_decision", {}).get("keep", True) else
                   "; keep rule also refuses: " + rec["keep_decision"]["reason"]),
                  ex, read_utc=rec["started"], finish_utc=rec.get("finished"), http_status=rec.get("status"),
                  content_type=rec.get("content_type"), bytes=rec.get("received_bytes"),
                  sha256=rec.get("received_sha256"), outcome=rec.get("outcome"),
                  used_for="LH059 %s, brief protocol 0.1" % did)
    print("written derived/%s.json" % did)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "fetch":
        fetch(sys.argv[2], sys.argv[3], sys.argv[4:])
    elif cmd == "keepD1":
        keepD1(sys.argv[2], sys.argv[3])
    elif cmd == "derive":
        derive(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        sys.exit(__doc__)
