"""r0025: the one exception in boto3's Python 3.9 run, and what the walk reading implies.

Reader-and-inference review of version 1.2 (notes/R-0025.md), stage two. Offline, over the
retained files only: data/week/python/{boto3,aiobotocore,botocore}.csv (W sums by version and
Python minor, 21 to 27 September 2026) and data/versions.csv (PyPI metadata as read on
29 September 2026). Made after the counts and after the record's own post hoc readings, so
everything here is post hoc; it tests nothing on data not yet read.

Questions:
 1. The record (Findings, "the shape of the older downloads") gives 1.42.87 at 486,869 as the one
    exception among the 50 versions below boto3's Python 3.9 edge. Is anything in PyPI's metadata
    for 1.42.87 (yanked, Requires-Python, files) different from its neighbours? If not, a pure
    resolver walk cannot skip it, unless the environments walking already hold that version
    installed, which pip uses without fetching.
 2. Does the dip at 1.42.87 appear on other Python minors, or only on 3.9?
 3. What does the walk reading imply for numbers: how many walks a week, how deep, and how many
    of the edge's fetches are walk starts rather than fresh installs that stop there.
 4. Are there other single-version dips (a version under 0.7 of both neighbours) in the first
    hundred below the edge, on 3.9, for boto3, botocore and aiobotocore?
"""
import csv
import os
from collections import defaultdict

try:
    from packaging.version import Version
except ImportError:  # fall back to a plain numeric parse; every boto3 version here is x.y.z
    class Version(tuple):
        def __new__(cls, s):
            return super().__new__(cls, tuple(int(p) for p in s.split(".")))

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")


def load_python(project):
    counts = defaultdict(lambda: defaultdict(int))  # minor -> version -> n
    with open(os.path.join(DATA, "week", "python", f"{project}.csv")) as f:
        for row in csv.DictReader(f):
            counts[row["python_minor"]][row["version"]] += int(row["n"])
    return counts


def load_meta(project):
    meta = {}
    with open(os.path.join(DATA, "versions.csv")) as f:
        for row in csv.DictReader(f):
            if row["project"] == project:
                meta[row["version"]] = row
    return meta


def parseable(v):
    try:
        Version(v)
        return True
    except Exception:
        return False


def run_below(counts, meta, edge, n=100):
    """Versions below the edge in descending PEP 440 order, non-pre-release, with W counts."""
    vs = [v for v in meta if parseable(v) and meta[v]["is_prerelease"] == "False"]
    vs = sorted(vs, key=Version, reverse=True)
    below = [v for v in vs if Version(v) < Version(edge)]
    return [(v, counts.get(v, 0)) for v in below[:n]]


def dips(seq, ratio=0.7):
    out = []
    for i in range(1, len(seq) - 1):
        v, c = seq[i]
        a, b = seq[i - 1][1], seq[i + 1][1]
        if a > 0 and b > 0 and c < ratio * a and c < ratio * b:
            out.append((v, c, a, b))
    return out


def main():
    print("r0025_walk_dip: post hoc checks on the walk reading (LH012 record, 'the shape of the older downloads')")
    print()

    # 1. boto3 on Python 3.9: the run below the edge, and 1.42.87's metadata
    boto3 = load_python("boto3")
    meta = load_meta("boto3")
    edge = "1.42.97"
    py39 = boto3["3.9"]
    seq = run_below(py39, meta, edge, 60)
    print("1. boto3, Python 3.9, 21 to 27 September 2026")
    print(f"   edge {edge}: {py39.get(edge, 0):,}")
    first50 = seq[:50]
    inband = [c for v, c in first50 if 882_000 <= c <= 906_000]
    print(f"   of the 50 below it, within 882,000 to 906,000: {len(inband)}; outside: "
          + ", ".join(f"{v} {c:,}" for v, c in first50 if not 882_000 <= c <= 906_000))
    print("   metadata of 1.42.86, 1.42.87, 1.42.88 (versions.csv):")
    for v in ("1.42.86", "1.42.87", "1.42.88"):
        m = meta[v]
        print(f"     {v}: first upload {m['first_upload_utc']}, requires_python {m['requires_python']!r}, "
              f"files {m['n_files']}, any_yanked {m['any_yanked']}, all_yanked {m['all_yanked']}, "
              f"wheel {m['wheel_interpreters']}-{m['wheel_abis']}-{m['wheel_platforms']}, sdist {m['has_sdist']}")
    neighbours = [c for v, c in first50 if v != "1.42.87"]
    med = sorted(neighbours)[len(neighbours) // 2]
    print(f"   1.42.87 as a fraction of the median of the other 49: {py39.get('1.42.87', 0) / med:.3f}")
    print("   1.42.87 was boto3's newest version from its upload on 2026-04-09T19:39 UTC until 1.42.88's on 2026-04-10T19:41 UTC.")
    print()

    # 2. the same version on other Python minors
    print("2. 1.42.86, 1.42.87 and 1.42.88 on each Python minor with at least 100,000 boto3 downloads on those three versions together")
    for minor in sorted(boto3, key=lambda m: (m == "", m)):
        c = boto3[minor]
        trio = [c.get("1.42.86", 0), c.get("1.42.87", 0), c.get("1.42.88", 0)]
        if sum(trio) < 100_000:
            continue
        ratio = trio[1] / ((trio[0] + trio[2]) / 2) if (trio[0] + trio[2]) else float("nan")
        print(f"   Python {minor or '(none)'}: 1.42.86 {trio[0]:,}; 1.42.87 {trio[1]:,}; 1.42.88 {trio[2]:,}; "
              f"1.42.87 over the mean of its neighbours {ratio:.2f}")
    print()

    # 3. what the walk reading implies in numbers
    print("3. What the walk reading implies, if every fetch below the edge on Python 3.9 belongs to a walk")
    below_all = [(v, py39.get(v, 0)) for v in meta if parseable(v) and meta[v]["is_prerelease"] == "False"
                 and Version(v) < Version(edge)]
    total_below = sum(c for v, c in below_all)
    plateau = sorted(c for v, c in first50 if v != "1.42.87")[24]
    print(f"   fetches below the edge: {total_below:,}; at the edge: {py39.get(edge, 0):,}")
    print(f"   walks a week, read as the plateau just below the edge: about {plateau:,}")
    print(f"   so of the edge's fetches, walk starts: {plateau / py39.get(edge, 0):.1%}; fresh installs that stop at the edge: "
          f"about {py39.get(edge, 0) - plateau:,}")
    print(f"   mean depth of a walk, fetches below the edge over walks: about {total_below / plateau:,.0f} versions")
    print(f"   at 1.42.87, walks that did not fetch it: about {plateau - py39.get('1.42.87', 0):,} of {plateau:,} "
          f"({(plateau - py39.get('1.42.87', 0)) / plateau:.0%})")
    print()

    # 4. other single-version dips in the first hundred below the edge, on 3.9
    print("4. Single-version dips (under 0.7 of both neighbours) in the first hundred below each edge, Python 3.9")
    for project, edge_p in (("boto3", "1.42.97"), ("botocore", "1.42.97"), ("aiobotocore", "3.5.0")):
        counts = load_python(project)
        m = load_meta(project)
        s = run_below(counts["3.9"], m, edge_p, 100)
        d = dips(s)
        print(f"   {project} (edge {edge_p}, {counts['3.9'].get(edge_p, 0):,} at the edge; first below: "
              + ", ".join(f"{v} {c:,}" for v, c in s[:3]) + ")")
        for v, c, a, b in d:
            mm = m.get(v, {})
            print(f"     {v}: {c:,} between {a:,} and {b:,}; any_yanked {mm.get('any_yanked')}, "
                  f"requires_python {mm.get('requires_python')!r}, first upload {mm.get('first_upload_utc', '')[:10]}")
        if not d:
            print("     none")
    print()

    # 5. what the walk reading would do to two shares the pieces give
    print("5. Two shares with the walk-shaped fetches set aside (walk shares from review/r0018_walkshare.txt, N; totals from data/analysis/week.csv)")
    week = {r["project"]: r for r in csv.DictReader(open(os.path.join(DATA, "analysis", "week.csv")))}
    tot = sum(int(r["total"]) for r in week.values())
    old = sum(int(r["older"]) for r in week.values())
    fam = ("boto3", "botocore", "s3transfer", "aiobotocore")
    tot_nb = tot - int(week["boto3"]["total"]); old_nb = old - int(week["boto3"]["older"])
    tot_nf = tot - sum(int(week[p]["total"]) for p in fam); old_nf = old - sum(int(week[p]["older"]) for p in fam)
    print(f"   pooled older share over the 37: {old / tot:.1%}; without boto3: {old_nb / tot_nb:.1%}; without boto3, botocore, s3transfer and aiobotocore: {old_nf / tot_nf:.1%}")
    walk = {"boto3": 0.789, "aiobotocore": 0.842}  # clear-walk shares of older downloads, r0018_walkshare.txt
    for p in ("boto3", "aiobotocore"):
        r = week[p]
        t, o, n = int(r["total"]), int(r["older"]), int(r["at_or_newer"])
        w = walk[p] * o
        print(f"   {p}: at-or-newer share in the week {n / t:.1%}; with {walk[p]:.0%} of older fetches set aside as walk-shaped, {n / (t - w):.1%} "
              f"(the reference is the newest version of 21 August, so this is a month-old release's share, not LH011's day-1 share)")
    print()
    print("Reading (post hoc, untested): pip's resolver uses an already-installed distribution as the candidate for its "
          "version without fetching it, so a walk from environments that hold 1.42.87 installed would fetch every "
          "version it tries except that one. That fits the dip and nothing else in the metadata does. It would mean "
          "that about half of the walks come from environments built while 1.42.87 was the newest boto3 (9 to 10 "
          "April 2026) or that install it by name. If so, the dip stays at 1.42.87 on later weeks until those "
          "environments are rebuilt; LH013's weeks can check it.")


if __name__ == "__main__":
    main()
