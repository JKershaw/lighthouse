"""LH041 collector (protocol 0.1). Run once per read, with python3 -I.

    python3 -I studies/LH041/scripts/collect.py --read <UTC label> [--work <dir>]

Steps (brief, "Sources and reads"):
 1. Download OSV's npm and PyPI exports (all.zip) into a work directory outside
    the repository (default: $TMPDIR/lh041-<label>), logging status, size,
    sha256 and the object's generation headers.
 2. Write an index of every MAL- record (id, ecosystem, package, published,
    modified, withdrawn, version count, origin sources, earliest import_time).
 3. Select every MAL- record whose text matches any wave indicator or lineage
    marker in waves.py, or whose package is a named seed; keep their raw JSON.
 4. For each npm package among the selected records: one GET of its packument
    from registry.npmjs.org (gzip), keeping an extract (time object, current
    maintainers as salted hashes, dist-tags, and for the record's versions whose
    document survives the publisher (hashed) and whether it carries an
    attestation), the body's sha256 and size. No package code, script or
    tarball is fetched, installed or run. Ceiling 3,000 packages; above it a seeded sample.
 5. For each PyPI (package, version) among the selected records: one GET of
    pypi.org/pypi/<p>/<v>/json, keeping status and file upload times. Ceiling 300.
 6. Spot-check up to 20 selected records against OpenSSF's own file
    (raw.githubusercontent.com), keeping both.
Every request is logged to requests.csv with URL, UTC time, status and bytes.
No key, token or account is used.
"""
import argparse, csv, gzip, hashlib, io, json, os, random, re, sys, time, urllib.parse, urllib.request, urllib.error, zipfile
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import waves  # noqa: E402

UA = "Lighthouse-research/1.0 (+https://lighthouse.harbour.cat)"
EXPORTS = {"npm": "https://osv-vulnerabilities.storage.googleapis.com/npm/all.zip",
           "PyPI": "https://osv-vulnerabilities.storage.googleapis.com/PyPI/all.zip"}
NPM_CEILING, PYPI_CEILING, SPOT = 3000, 300, 20
PACE = 0.3  # seconds between registry requests


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Log:
    def __init__(self, path):
        self.f = open(path, "a", newline="")
        self.w = csv.writer(self.f)
        if self.f.tell() == 0:
            self.w.writerow(["url", "read_utc", "status", "bytes", "sha256", "note"])

    def row(self, *r):
        self.w.writerow(r); self.f.flush()


def get(url, log, accept=None, retries=1, note=""):
    hdr = {"User-Agent": UA, "Accept-Encoding": "gzip"}
    if accept:
        hdr["Accept"] = accept
    for attempt in range(retries + 1):
        t = now()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=60) as r:
                body = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    body = gzip.decompress(body)
                log.row(url, t, r.status, len(body), hashlib.sha256(body).hexdigest(), note)
                return r.status, body, dict(r.headers)
        except urllib.error.HTTPError as e:
            log.row(url, t, e.code, 0, "", note)
            if e.code in (404, 410):
                return e.code, b"", {}
        except Exception as e:  # network error: unavailable
            log.row(url, t, "error:" + type(e).__name__, 0, "", note)
        time.sleep(2)
    return None, b"", {}


def hid(name):
    """Salted hash of a public username, so retained data name no maintainer."""
    if not name:
        return None
    return "h" + hashlib.sha256(("lh041:" + name.lower()).encode()).hexdigest()[:16]


def norm(text):
    t = text.lower()
    for a, b in (("[.]", "."), ("(.)", "."), ("[dot]", "."), ("(dot)", "."), ("hxxp", "http"), ("[:]", ":")):
        t = t.replace(a, b)
    return t


def matches(text):
    t = norm(text)
    hit = {"lineage": [m for m in waves.LINEAGE if re.search(m, t)], "specific": {}, "shared": {}}
    for w in waves.WAVES:
        s = [m for m in w["specific"] if re.search(m, t)]
        if s:
            hit["specific"][w["id"]] = s
        sh = [m for m in w["shared"] if re.search(m, t)]
        if sh:
            hit["shared"][w["id"]] = sh
    return hit


def is_seed(eco, name):
    n = name.lower()
    for w in waves.WAVES:
        for s in w["seeds"]:
            s = s.lower()
            if (s.endswith("/") and n.startswith(s)) or n == s:
                return w["id"]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--read", required=True)
    ap.add_argument("--work", default=None)
    ap.add_argument("--skip-download", action="store_true", help="reuse zips already in --work")
    a = ap.parse_args()
    out = os.path.join(HERE, "..", "data", a.read)
    os.makedirs(out, exist_ok=True)
    work = a.work or os.path.join(os.environ.get("TMPDIR", "/tmp"), "lh041-" + a.read)
    os.makedirs(work, exist_ok=True)
    log = Log(os.path.join(out, "requests.csv"))
    meta = {"read": a.read, "started": now(), "exports": {}}

    # 1. exports
    for eco, url in EXPORTS.items():
        zp = os.path.join(work, eco + "-all.zip")
        if not a.skip_download:
            st, body, hd = get(url, log, note="OSV export " + eco)
            if st != 200:
                sys.exit("export unavailable: " + url)
            open(zp, "wb").write(body)
            meta["exports"][eco] = {"url": url, "status": st, "bytes": len(body),
                                    "sha256": hashlib.sha256(body).hexdigest(),
                                    "last_modified": hd.get("Last-Modified"), "etag": hd.get("ETag"),
                                    "generation": hd.get("x-goog-generation"), "read_utc": now()}

    # 2-3. index and selection
    idx = gzip.open(os.path.join(out, "osv-mal-index.csv.gz"), "wt", newline="")
    iw = csv.writer(idx)
    iw.writerow(["id", "ecosystem", "package", "published", "modified", "withdrawn", "n_versions",
                 "has_ranges", "origin_sources", "first_import"])
    sel = gzip.open(os.path.join(out, "osv-selected.jsonl.gz"), "wt")
    selected = []
    for eco in EXPORTS:
        z = zipfile.ZipFile(os.path.join(work, eco + "-all.zip"))
        for nm in z.namelist():
            if not nm.startswith("MAL-"):
                continue
            raw = z.read(nm).decode("utf-8", "replace")
            rec = json.loads(raw)
            aff = rec.get("affected", [{}])
            pkg = aff[0].get("package", {}).get("name", "") if aff else ""
            vers = sorted({v for x in aff for v in x.get("versions", [])})
            origins = rec.get("database_specific", {}).get("malicious-packages-origins", [])
            imps = sorted(o.get("import_time", "") for o in origins if o.get("import_time"))
            iw.writerow([rec["id"], eco, pkg, rec.get("published", ""), rec.get("modified", ""),
                         rec.get("withdrawn", ""), len(vers), int(any(x.get("ranges") for x in aff)),
                         ";".join(sorted({o.get("source", "") for o in origins})), imps[0] if imps else ""])
            h = matches(raw)
            seed = is_seed(eco, pkg)
            if h["lineage"] or h["specific"] or h["shared"] or seed:
                sel.write(json.dumps({"ecosystem": eco, "file": nm, "match": h, "seed": seed, "raw": raw}) + "\n")
                selected.append((eco, pkg, vers))
    idx.close(); sel.close()
    meta["selected_records"] = len(selected)

    # 4. npm packuments
    npm_pk = sorted({p for e, p, v in selected if e == "npm" and p})
    if len(npm_pk) > NPM_CEILING:
        random.seed(41)
        npm_pk = sorted(random.sample(npm_pk, NPM_CEILING))
        meta["npm_sampled"] = True
    wanted = {}
    for e, p, v in selected:
        if e == "npm":
            wanted.setdefault(p, set()).update(v)
    ex = gzip.open(os.path.join(out, "npm-extract.jsonl.gz"), "wt")
    for p in npm_pk:
        url = "https://registry.npmjs.org/" + urllib.parse.quote(p, safe="@")
        st, body, hd = get(url, log, note="npm packument")
        rec = {"package": p, "status": st, "read_utc": now(), "bytes": len(body),
               "sha256": hashlib.sha256(body).hexdigest() if body else ""}
        if st == 200:
            try:
                d = json.loads(body)
                rec["time"] = d.get("time", {})
                # Maintainer usernames are kept only as salted hashes (the keeper's caution of
                # 8 November 2026: no hijacked maintainer is named); clustering needs identity, not names.
                rec["maintainers_h"] = sorted(hid(m.get("name")) for m in d.get("maintainers", []) if isinstance(m, dict))
                rec["dist_tags"] = d.get("dist-tags", {})
                rec["n_versions_listed"] = len(d.get("versions", {}))
                rec["versions_listed"] = sorted(d.get("versions", {}).keys())[-400:]
                vd = {}
                for v in wanted.get(p, ()):  # surviving documents of the record's versions
                    doc = d.get("versions", {}).get(v)
                    if doc:
                        vd[v] = {"npmUser_h": hid((doc.get("_npmUser") or {}).get("name")),
                                 "has_attestations": bool((doc.get("dist") or {}).get("attestations"))}
                rec["record_version_docs"] = vd
            except Exception as e:
                rec["parse_error"] = type(e).__name__
        ex.write(json.dumps(rec) + "\n"); ex.flush()
        time.sleep(PACE)
    ex.close()

    # 5. PyPI releases
    py = sorted({(p, v) for e, p, vs in selected if e == "PyPI" for v in vs})[:PYPI_CEILING]
    pe = gzip.open(os.path.join(out, "pypi-extract.jsonl.gz"), "wt")
    for p, v in py:
        url = "https://pypi.org/pypi/%s/%s/json" % (urllib.parse.quote(p), urllib.parse.quote(v))
        st, body, hd = get(url, log, note="PyPI release JSON")
        rec = {"package": p, "version": v, "status": st, "read_utc": now()}
        if st == 200:
            try:
                d = json.loads(body)
                rec["uploads"] = sorted(u.get("upload_time_iso_8601") for u in d.get("urls", []))
                rec["yanked"] = any(u.get("yanked") for u in d.get("urls", []))
            except Exception as e:
                rec["parse_error"] = type(e).__name__
        pe.write(json.dumps(rec) + "\n"); pe.flush()
        time.sleep(PACE)
    pe.close()

    # 6. OpenSSF spot check
    random.seed(4101)
    lines = gzip.open(os.path.join(out, "osv-selected.jsonl.gz"), "rt").read().splitlines()
    sc = gzip.open(os.path.join(out, "openssf-spotcheck.jsonl.gz"), "wt")
    for ln in random.sample(lines, min(SPOT, len(lines))):
        r = json.loads(ln); rec = json.loads(r["raw"])
        src = (rec.get("affected", [{}])[0].get("database_specific") or {}).get("source", "")
        m = re.match(r"https://github\.com/ossf/malicious-packages/blob/(.+)$", src)
        if not m:
            sc.write(json.dumps({"id": rec["id"], "source": src, "status": "no source path"}) + "\n"); continue
        url = "https://raw.githubusercontent.com/ossf/malicious-packages/" + m.group(1)
        st, body, hd = get(url, log, note="OpenSSF spot check")
        sc.write(json.dumps({"id": rec["id"], "url": url, "status": st, "raw": body.decode("utf-8", "replace")}) + "\n")
        time.sleep(PACE)
    sc.close()
    meta["ended"] = now()
    json.dump(meta, open(os.path.join(out, "meta.json"), "w"), indent=1)
    print(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
