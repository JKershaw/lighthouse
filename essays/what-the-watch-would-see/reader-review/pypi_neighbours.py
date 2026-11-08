"""List each litellm release (first file upload) uploaded 2026-10-15..2026-11-08 from PyPI's project JSON (read as data only).
python3 -I pypi_neighbours.py <pypi-litellm.json>"""
import json, sys
d = json.load(open(sys.argv[1]))
rows = []
for v, files in d["releases"].items():
    for f in files:
        t = f.get("upload_time_iso_8601", "")
        if "2026-10-15" <= t[:10] <= "2026-11-08":
            rows.append((t, v, f.get("yanked")))
first = {}
for t, v, y in rows:
    if v not in first or t < first[v][0]:
        first[v] = (t, y)
for v, (t, y) in sorted(first.items(), key=lambda kv: kv[1][0]):
    print(t, v, "yanked" if y else "")
print("1.107.0 listed in releases:", "1.107.0" in d["releases"])
