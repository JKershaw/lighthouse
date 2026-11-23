"""LH047 re-audit of ISO week 2026-W47: the mechanical search for the population (brief, Amendment 2).

Reads every file in the tree of one commit (git objects, not the working copy), decompressing .gz,
and lists each file that contains at least one UTC timestamp inside the week (16 November 2026
00:00 UTC to 22 November 2026 24:00 UTC) in any of the forms 2026-11-DDTHH:MM, 2026-11-DD HH:MM,
2026-11-DDTHHMM (compact) or a Unix time in seconds inside the week, together with at least one
http(s) URL, or (second criterion) whose file name contains "log", "fetch" or "request". Each candidate is then classed in candidates.csv by classify.csv (written by hand, by
path pattern, before any row was judged): request log or not, with the reason.

Run from the repository root:
  python3 -I studies/LH047/data/reaudit-2026-W47/code/find_logs.py <commit> [<commit2>]
With a second commit, also lists candidates present at <commit2> but not identical at <commit>
(logs committed after the population commit), written to candidates-later.csv.
"""
import csv, gzip, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
WEEK = re.compile(rb'2026-11-(1[6-9]|2[0-2])(T[0-2]\d:[0-5]\d|T[0-2]\d[0-5]\d|\s[0-2]\d:[0-5]\d)')
EPOCH = re.compile(rb'(?<!\d)(179478\d{4}|17948\d{5}|17949\d{5}|17950\d{5}|17951\d{5}|17952\d{5}|17953\d{5})(?:\.\d+)?(?!\d)')
URL = re.compile(rb'https?://')
NAMED = re.compile(r'(log|fetch|request)', re.I)
LO, HI = 1794787200, 1795392000


def tree(commit):
    out = subprocess.run(['git', 'ls-tree', '-r', '-z', commit], capture_output=True, check=True).stdout
    for ent in out.split(b'\0'):
        if not ent:
            continue
        meta, path = ent.split(b'\t', 1)
        mode, typ, sha = meta.split()
        if typ == b'blob':
            yield path.decode(), sha.decode()


def blobs(shas):
    p = subprocess.Popen(['git', 'cat-file', '--batch'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    for sha in shas:
        p.stdin.write(sha.encode() + b'\n'); p.stdin.flush()
        hdr = p.stdout.readline().split()
        n = int(hdr[2])
        data = p.stdout.read(n); p.stdout.read(1)
        yield data
    p.stdin.close(); p.wait()


def has_week(data):
    if WEEK.search(data):
        return 'iso'
    for m in EPOCH.finditer(data):
        v = int(m.group(1))
        if LO <= v < HI:
            return 'epoch'
    return ''


def scan(commit):
    items = [(p, s) for p, s in tree(commit) if not p.startswith('harbour/.session')]
    res = {}
    for (path, sha), data in zip(items, blobs([s for _, s in items])):
        if path.endswith('.gz'):
            try:
                data = gzip.decompress(data)
            except Exception:
                continue
        if b'\0' in data[:8192]:
            continue  # binary
        w = has_week(data)
        if w and URL.search(data):
            res[path] = (sha, w, len(data), 'week time and URL')
        elif w and NAMED.search(os.path.basename(path)):
            res[path] = (sha, w, len(data), 'week time, log-like name, no URL')
    return res


def main():
    c1 = sys.argv[1]
    a = scan(c1)
    with open(os.path.join(OUT, 'candidates-raw.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['path', 'blob', 'week_time_form', 'bytes', 'criterion'])
        for p in sorted(a):
            w.writerow([p, *a[p]])
    print('commit', c1, 'candidates', len(a))
    if len(sys.argv) > 2:
        b = scan(sys.argv[2])
        later = {p: v for p, v in b.items() if p not in a or a[p][0] != v[0]}
        with open(os.path.join(OUT, 'candidates-later-raw.csv'), 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['path', 'blob', 'week_time_form', 'bytes', 'criterion', 'at_population_commit'])
            for p in sorted(later):
                w.writerow([p, *later[p], 'changed' if p in a else 'absent'])
        print('commit', sys.argv[2], 'new or changed candidates', len(later))


if __name__ == '__main__':
    main()
