"""Draws articles/pins-move-over-weeks.svg, the piece's figure, from data/lags.csv."""
import csv, os
from datetime import datetime, timezone
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..'))
LAGS=os.path.join(ROOT,'studies/LH008/data/lags.csv')
OUT=os.path.join(ROOT,'articles/pins-move-over-weeks.svg')
rows=[r for r in csv.DictReader(open(LAGS)) if r['kind']=='fix']
def t(s): return datetime.fromisoformat(s.replace('Z','+00:00'))
libs=[('urllib3','2026-05-07T16:13:17Z','2026-05-11T14:51:20Z'),
      ('pyjwt','2026-05-21T19:54:35Z','2026-06-15T19:28:06Z'),
      ('starlette','2026-05-23T16:55:39Z','2026-06-15T20:16:30Z'),
      ('cryptography','2026-06-09T22:30:53Z','2026-06-15T20:12:27Z')]
W=720; X0=150; X1=700
D0=datetime(2026,5,1,tzinfo=timezone.utc); D1=datetime(2026,9,27,tzinfo=timezone.utc)
def x(d): return X0+(X1-X0)*(d-D0).total_seconds()/(D1-D0).total_seconds()
R=3.6; GAP=7.8
top=176; rowh=96
o=[]
H=top+rowh*4+122
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">')
o.append('<title id="t">When pinned software moved to a security fix, four Python libraries, May to September 2026</title>')
o.append('<desc id="d">Four rows, one for each library: urllib3, pyjwt, starlette and cryptography, on a time axis from 1 May to 27 September 2026. In each row a dashed line marks the day the fixed release was published and a solid line the day its security advisory was published; the advisories for pyjwt, starlette and cryptography fall on the evening of 15 June, within 48 minutes of each other, among ten GitHub published against the three libraries that evening. Each dot is one pinned or locked repository moving to the fix or later: 18 of 32 for urllib3, 25 of 29 for pyjwt, 5 of 7 for starlette and 25 of 34 for cryptography. Dots are filled blue where a bot wrote the change, blue rings where a person merged a bot\'s branch, and grey where a person made it. They gather a little in the days after each release and in the week after each advisory, but most are spread over the weeks that follow, into August. Git histories, the Python Package Index and OSV read on 27 September 2026.</desc>')
o.append('''<style>
svg { --bg:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --muted:#6f6e69; --grid:#e4e3df; --band:#efeee9; --bot:#2a78d6; --per:#8a8984; }
@media (prefers-color-scheme: dark) { svg { --bg:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --muted:#9a9890; --grid:#383835; --band:#2a2a27; --bot:#4b93ea; --per:#9f9d95; } }
text { font-family: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; fill: var(--ink); }
.head { font-size: 17px; font-weight: 600; } .sub { font-size: 13px; fill: var(--ink2); }
.lab { font-size: 14px; font-weight: 600; } .note { font-size: 11.5px; fill: var(--muted); }
.ann { font-size: 12px; fill: var(--ink2); } .ax { font-size: 12px; fill: var(--muted); }
</style>''')
o.append(f'<rect width="{W}" height="{H}" fill="var(--bg)"/>')
o.append('<text x="16" y="30" class="head">Pinned software moved to a security fix over weeks, not in a burst</text>')
o.append('<text x="16" y="51" class="sub">Each dot is one pinned repository\'s first commit taking the library to its fixed release or later.</text>')
# legend
ly=80
o.append(f'<circle cx="22" cy="{ly-4}" r="{R}" fill="var(--bot)"/><text x="31" y="{ly}" class="ann">a bot wrote it</text>')
o.append(f'<circle cx="146" cy="{ly-4}" r="{R-0.6}" fill="var(--bg)" stroke="var(--bot)" stroke-width="1.8"/><text x="159" y="{ly}" class="ann">a person merged a bot\'s branch</text>')
o.append(f'<circle cx="382" cy="{ly-4}" r="{R}" fill="var(--per)"/><text x="391" y="{ly}" class="ann">a person</text>')
o.append(f'<line x1="20" y1="{ly+12}" x2="20" y2="{ly+26}" stroke="var(--ink)" stroke-width="1.5" stroke-dasharray="3 2.5"/><text x="31" y="{ly+24}" class="ann">fix released</text>')
o.append(f'<line x1="134" y1="{ly+12}" x2="134" y2="{ly+26}" stroke="var(--ink)" stroke-width="1.5"/><text x="143" y="{ly+24}" class="ann">advisory published</text>')
o.append(f'<rect x="290" y="{ly+13}" width="12" height="12" fill="var(--band)"/><text x="309" y="{ly+24}" class="ann">two days after a release; seven after an advisory</text>')
# month grid
bottom=top+rowh*4
for m,lab in [(5,'May'),(6,'June'),(7,'July'),(8,'Aug'),(9,'Sept')]:
    xx=x(datetime(2026,m,1,tzinfo=timezone.utc))
    o.append(f'<line x1="{xx:.1f}" y1="{top-14}" x2="{xx:.1f}" y2="{bottom}" stroke="var(--grid)" stroke-width="1"/>')
    o.append(f'<text x="{xx+4:.1f}" y="{bottom+17}" class="ax">{lab}</text>')
o.append(f'<line x1="{X1}" y1="{top-14}" x2="{X1}" y2="{bottom}" stroke="var(--muted)" stroke-width="1" stroke-dasharray="1 3"/>')
o.append(f'<text x="{X1}" y="{bottom+17}" class="ax" text-anchor="end">27 Sept</text>')
# 15 June annotation
xj=x(t('2026-06-15T19:28:06Z'))
o.append(f'<text x="{xj+6:.1f}" y="{top-18}" class="ann">15 June, 19:28 to 20:16 UTC:</text>')
o.append(f'<text x="{xj+6:.1f}" y="{top-4}" class="ann">the three advisories we followed, within 48 minutes</text>')
for i,(lib,rel,adv) in enumerate(libs):
    y0=top+rowh*i; base=y0+rowh-18
    kept=[r for r in rows if r['library']==lib]
    mv=sorted([r for r in kept if r['outcome']=='moved'],key=lambda r:r['committer_time'])
    cen=sum(1 for r in kept if r['outcome'].startswith('censored')); rem=sum(1 for r in kept if r['outcome']=='removed')
    rt,at=t(rel),t(adv)
    from datetime import timedelta
    o.append(f'<rect x="{x(rt):.1f}" y="{y0+8}" width="{x(rt+timedelta(days=2))-x(rt):.1f}" height="{base-y0-2}" fill="var(--band)"/>')
    o.append(f'<rect x="{x(at):.1f}" y="{y0+8}" width="{x(at+timedelta(days=7))-x(at):.1f}" height="{base-y0-2}" fill="var(--band)"/>')
    o.append(f'<line x1="{X0}" y1="{base+6}" x2="{X1}" y2="{base+6}" stroke="var(--grid)" stroke-width="1"/>')
    o.append(f'<line x1="{x(rt):.1f}" y1="{y0+8}" x2="{x(rt):.1f}" y2="{base+6}" stroke="var(--ink)" stroke-width="1.5" stroke-dasharray="3 2.5"/>')
    o.append(f'<line x1="{x(at):.1f}" y1="{y0+8}" x2="{x(at):.1f}" y2="{base+6}" stroke="var(--ink)" stroke-width="1.5"/>')
    o.append(f'<text x="16" y="{y0+34}" class="lab">{lib}</text>')
    o.append(f'<text x="16" y="{y0+52}" class="note">{len(mv)} of {len(kept)} moved</text>')
    o.append(f'<text x="16" y="{y0+67}" class="note">{cen} had not by 27 Sept</text>')
    if rem: o.append(f'<text x="16" y="{y0+82}" class="note">{rem} stopped pinning it</text>')
    levels=[]
    for r in mv:
        cx=x(t(r['committer_time']))
        lv=0
        while any(l==lv and abs(px-cx)<GAP for px,l in levels): lv+=1
        levels.append((cx,lv))
        cy=base-lv*GAP
        a=r['authorship']
        tip=f"{r['committer_time'][:10]}: {r['held_min']} to {r['moved_to']}, {float(r['lag_release_days']):.1f} days after the release, {a}"
        if a=='bot': o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R}" fill="var(--bot)"><title>{tip}</title></circle>')
        elif a.startswith('person merging'): o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R-0.6}" fill="var(--bg)" stroke="var(--bot)" stroke-width="1.8"><title>{tip}</title></circle>')
        else: o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R}" fill="var(--per)"><title>{tip}</title></circle>')
    print(lib, max(l for _,l in levels))
fy=bottom+46
for k,line in enumerate(["102 pairs of a repository and a library it pinned or locked below the fix, from the dependents",
 "of each library that Open Source Insights lists, sampled by a rule fixed in advance. A dot is a",
 "commit on the default branch, at its commit time: a change to what the project asks for, not an",
 "installation. Git histories, the Python Package Index and OSV read on 27 September 2026."]):
    o.append(f'<text x="16" y="{fy+16*k}" class="note">{line}</text>')
o.append('</svg>')
open(OUT,'w').write('\n'.join(o)+'\n')
