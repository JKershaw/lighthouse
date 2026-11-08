import json, sys
from datetime import datetime, timezone
d = json.load(open(sys.argv[1]))
origins = d["database_specific"]["malicious-packages-origins"]
o = [x for x in origins if "1.107.0" in x.get("versions", [])]
print("origins listing 1.107.0:", [(x["source"], x.get("id"), x["import_time"], x["modified_time"]) for x in o])
def p(s):
    s = s.rstrip("Z")
    if "." in s:
        a, b = s.split("."); s = a + "." + b[:6]
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=timezone.utc)
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
up_early = datetime(2026,10,21,11,39,tzinfo=timezone.utc)   # "between 11:39 and 11:40 UTC" in details
up_late  = datetime(2026,10,21,11,40,tzinfo=timezone.utc)
for label, t in [("import_time", p(o[0]["import_time"])), ("origin modified_time", p(o[0]["modified_time"])), ("record modified", p(d["modified"]))]:
    for ul, u in [("11:39", up_early), ("11:40", up_late)]:
        g = t - u
        print(f"{label} {t.isoformat()} - upload {ul}: {g}  = {g.total_seconds()/86400:.3f} days")
