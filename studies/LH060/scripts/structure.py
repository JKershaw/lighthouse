"""LH060 structure-only check of LH033's and LH039's retained aggregates.

Brief: studies/LH060/brief.md, "The structure-only check of retained data".
Prints, for each named file, only: JSON key paths (list positions collapsed
to [*]) with value types, or a CSV header row. Every digit in every key is
replaced by '#' (keys that are dates, versions or labels used as data); paths
identical after masking are printed once with a count. No value is printed.
For each named file it also reports whether every other read directory's file
of the same name has the same masked key paths (same or different only).

Run from the repository root: python3 -I studies/LH060/scripts/structure.py
"""
import csv
import gzip
import io
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LH033 = ROOT / "studies/LH033/data"
LH039 = ROOT / "studies/LH039"

FILES = [
    ("LH033", LH033 / "read-2026-11-21T1414Z/censys.raw.gz"),
    ("LH033", LH033 / "read-2026-11-21T1414Z/tables.json"),
    ("LH033", LH033 / "read-2026-11-21T1414Z/read_log.json"),
    ("LH033", LH033 / "read-2026-11-21T1414Z/w3techs-details-8.3.derived.json"),
    ("LH033", LH033 / "read-2026-11-21T1414Z/w3techs-history_details-8.3.derived.json"),
    ("LH033", LH033 / "read-2026-10-25T0855Z/packagist.json"),
    ("LH033", LH033 / "record_v1.json"),
    ("LH033", LH033 / "python_side.json"),
    ("LH039", LH039 / "data/raw-2026-11-21T1411Z/w3-71.derived.json"),
    ("LH039", LH039 / "data/raw-2026-11-21T1411Z/w3h-71.derived.json"),
    ("LH039", LH039 / "data/raw-2026-11-21T1411Z/cand-3.derived.json"),
    ("LH039", LH039 / "data/raw-2026-11-21T1411Z/readlog.csv"),
    ("LH039", LH039 / "data/packagist-2026-11-21T1415Z/roots-7.1.4.json"),
    ("LH039", LH039 / "data/packagist-2026-11-21T1415Z/johnpbloch-7.1.4.json"),
    ("LH039", LH039 / "data/packagist-2026-11-21T1415Z/readlog.csv"),
    ("LH039", LH039 / "data/oneoff-2026-11-22T1514Z/archive.facts.json"),
    ("LH039", LH039 / "data/oneoff-2026-11-22T1514Z/feed.facts.json"),
    ("LH039", LH039 / "data/oneoff-2026-11-22T1514Z/readlog.csv"),
    ("LH039", LH039 / "record-1.0-packagist.csv"),
    ("LH039", LH039 / "checkpoints/2026-11-21-packagist.csv"),
]

DIGIT = re.compile(r"\d")


def mask(key):
    return DIGIT.sub("#", str(key))


def tname(v):
    if v is None:
        return "null"
    return {bool: "bool", int: "int", float: "float", str: "str",
            list: "list", dict: "object"}.get(type(v), type(v).__name__)


def walk(obj, path, out):
    """Collect masked path -> set of value types. Never stores a value."""
    if isinstance(obj, dict):
        out.setdefault(path or "$", set()).add("object")
        for k, v in obj.items():
            walk(v, f"{path}.{mask(k)}", out)
    elif isinstance(obj, list):
        out.setdefault(path or "$", set()).add("list")
        for v in obj:
            walk(v, f"{path}[*]", out)
    else:
        out.setdefault(path or "$", set()).add(tname(obj))


def load_json(p):
    raw = p.read_bytes()
    if p.suffix == ".gz":
        raw = gzip.decompress(raw)
    return json.loads(raw.decode("utf-8"))


def paths_of(p):
    out = {}
    walk(load_json(p), "", out)
    return out


def header_of(p):
    with p.open(newline="", encoding="utf-8") as fh:
        return next(csv.reader(fh), [])


def siblings(p):
    """Files of the same name in other read directories of the same kind."""
    parent = p.parent
    prefix = parent.name.split("-")[0]
    if parent.parent.name not in ("data",) or prefix not in ("read", "raw", "packagist", "oneoff"):
        return []
    others = []
    for d in sorted(parent.parent.glob(prefix + "-*")):
        if d != parent and (d / p.name).exists():
            others.append(d / p.name)
    return others


def main():
    for study, p in FILES:
        rel = p.relative_to(ROOT)
        print(f"== {study} {rel}")
        if not p.exists():
            print("   MISSING")
            continue
        sibs = siblings(p)
        if p.suffix == ".csv":
            h = header_of(p)
            print("   csv header: " + " | ".join(mask(c) for c in h))
            if sibs:
                same = sum(1 for s in sibs if header_of(s) == h)
                print(f"   same-name files in other reads: {len(sibs)}; same header: {same}; different: {len(sibs) - same}")
            continue
        try:
            ps = paths_of(p)
        except (ValueError, UnicodeDecodeError, OSError) as e:
            print(f"   not parseable as JSON ({type(e).__name__})")
            continue
        for k in sorted(ps):
            print(f"   {k}: {'/'.join(sorted(ps[k]))}")
        if sibs:
            same = 0
            for s in sibs:
                try:
                    if set(paths_of(s)) == set(ps):
                        same += 1
                except (ValueError, UnicodeDecodeError, OSError):
                    pass
            print(f"   same-name files in other reads: {len(sibs)}; same key paths: {same}; different: {len(sibs) - same}")


if __name__ == "__main__":
    main()
