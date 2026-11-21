"""R-0106 (reader review of LH038 0.4): offsets between SUSE's clocks per advisory,
parsed from scripts/timeline_output.txt (no network). Run: python3 -I r0106_offsets.py"""
import re, sys
from datetime import datetime, timezone
from pathlib import Path
out = Path(__file__).resolve().parent.parent / "scripts" / "timeline_output.txt"
pat = re.compile(r"^(SUSE-SU-\S+) \[(.+?)\]: Release Date (\S+ \S+)Z.*?CVE-page stamp (\S+ \S+)Z; "
                 r"list message \(archive\) (\S+ \S+)Z.*?OSV published (\S+) modified (\S+?)\.\d+Z")
def p(s): return datetime.fromisoformat(s.replace("T", " ")).replace(tzinfo=timezone.utc)
print("advisory | group | stamp-list h | OSVmod-list h | list-ReleaseDate d")
for line in out.read_text().splitlines():
    m = pat.match(line)
    if not m: continue
    adv, grp, rd, st, li, op, om = m.groups()
    rd, st, li, om = p(rd), p(st), p(li), p(om)
    print(f"{adv} | {grp} | {(st-li).total_seconds()/3600:.2f} | {(om-li).total_seconds()/3600:.1f} | {(li-rd).total_seconds()/86400:.2f}")
