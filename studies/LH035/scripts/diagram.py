"""Draw studies/LH035/figure.svg: the brief's ten layers as bands, with each
included instrument placed on every layer it sits on (filled on its primary
layer, outlined elsewhere) and the candidates without a row shown dashed.
A draft diagram, as the brief asks; it may later seed a map page.
Run from the repository root: python3 studies/LH035/scripts/diagram.py"""
import json
from pathlib import Path
from xml.sax.saxutils import escape

D = Path(__file__).resolve().parent.parent
LAYERS = {
    1: "Physical and|interconnection", 2: "Routing", 3: "Addresses and|reachability",
    4: "Names", 5: "Certificates", 6: "Running services|and their software",
    7: "Web content and|technology", 8: "Software supply",
    9: "Vulnerability and|exploitation records", 10: "Traffic",
}
SHORT = {
    "I01": "PeeringDB", "I02": "TeleGeography cables", "I03": "Epoch AI data centres",
    "I04": "Interconnection Measurement Project", "I05": "RouteViews", "I06": "RIPE RIS",
    "I07": "PCH BGP data", "I08": "CAIDA AS relationships", "I09": "Cloudflare Radar",
    "I10": "RIPE Atlas", "I11": "CAIDA Ark topology", "I12": "Censys", "I13": "UCSD telescope",
    "I14": "Tranco", "I15": "CrUX", "I16": "CT logs", "I17": "Shadowserver", "I18": "urlscan.io",
    "I19": "HTTP Archive", "I20": "W3Techs", "I21": "Common Crawl", "I22": "PyPI BigQuery",
    "I23": "pypistats", "I24": "ClickPy", "I25": "npm counts", "I26": "nodejs.org logs",
    "I27": "Packagist", "I28": "GH Archive", "I29": "deps.dev", "I30": "CISA KEV",
    "I31": "CVE List", "I32": "OSV", "I33": "GitHub advisories", "I34": "EPSS",
    "I35": "Exploit-DB", "I36": "Breaking Trust", "I37": "DShield", "I38": "GreyNoise",
    "I39": "MAWI", "I40": "M-Lab",
    "I41": "CAIDA AS facilities", "I42": "DNS Coffee", "I43": "Docker Hub",
    "I44": "Hugging Face", "I45": "Netlas", "I46": "Software Heritage", "I47": "NVD",
    "I48": "RIPEstat",
}
CAND_SHORT = {
    "CAIDA AS Facilities": "CAIDA AS facilities", "USC/ISI ANT datasets (censuses, hitlists, outages, Trinocular)": "ISI ANT",
    "ICANN Centralized Zone Data Service (CZDS)": "ICANN CZDS", "DNS Coffee": "DNS Coffee",
    "Docker Hub": "Docker Hub", "Hugging Face Hub download counts": "Hugging Face", "Shodan": "Shodan",
    "Netlas": "Netlas", "Software Heritage": "Software Heritage", "National Vulnerability Database (NVD)": "NVD",
    "Internet Atlas (University of Wisconsin)": "Internet Atlas", "RIPEstat": "RIPEstat",
}

rows = json.loads((D / "data/instruments.json").read_text())["rows"]
cands = [c for c in json.loads((D / "data/candidates.json").read_text())["rows"] if c["class"] in ("undetermined", "unreadable")]

W, LABEL_W, PAD, CH, GAP, FS = 720, 168, 10, 20, 6, 11


def text_w(s):
    return int(len(s) * FS * 0.6) + 14


chips = {k: [] for k in LAYERS}
for r in rows:
    for l in r["layers"]:
        chips[l].append((SHORT[r["id"]], "primary" if l == r["primary"] else "secondary"))
for c in cands:
    for l in c["layers"]:
        chips[l].append((CAND_SHORT[c["name"]], c["class"]))

body, y = [], 64
for k, name in LAYERS.items():
    x, line, placed = LABEL_W + PAD, 0, []
    for label, kind in chips[k]:
        w = text_w(label)
        if x + w > W - PAD:
            line += 1
            x = LABEL_W + PAD
        placed.append((x, line, w, label, kind))
        x += w + GAP
    h = max(PAD * 2 + (line + 1) * CH + line * GAP, PAD * 2 + 30 if "|" in name else 0)
    body.append(f'<rect class="band{k % 2}" x="0" y="{y}" width="{W}" height="{h}"/>')
    body.append(f'<text class="lnum" x="10" y="{y + PAD + 14}">{k}</text>')
    for i, part in enumerate(name.split("|")):
        body.append(f'<text class="lname" x="30" y="{y + PAD + 14 + i * 15}">{escape(part)}</text>')
    for x0, ln, w, label, kind in placed:
        cy = y + PAD + ln * (CH + GAP)
        body.append(f'<rect class="c-{kind}" x="{x0}" y="{cy}" width="{w}" height="{CH}" rx="4"/>')
        body.append(f'<text class="t-{kind}" x="{x0 + w / 2}" y="{cy + 14}" text-anchor="middle">{escape(label)}</text>')
    y += h

legend_y = y + 18
legend = [("primary", "included, primary layer"), ("secondary", "included, also on this layer"),
          ("undetermined", "free access not established"), ("unreadable", "pages could not be read")]
for i, (kind, label) in enumerate(legend):
    lx, ly = 10 + (i % 2) * 300, legend_y + (i // 2) * 22
    body.append(f'<rect class="c-{kind}" x="{lx}" y="{ly}" width="22" height="14" rx="3"/>')
    body.append(f'<text class="leg" x="{lx + 28}" y="{ly + 11}">{label}</text>')
H = legend_y + 52

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">Public instruments placed on ten layers of the internet (LH035 draft)</title>
<desc id="d">Each band is one of the brief's ten layers. Filled boxes are instruments included in the survey on their primary layer, outlined boxes the other layers they sit on, dashed boxes candidates whose free access was not established or whose pages could not be read. Read 2 and 5 November 2026.</desc>
<style>
:root{{--bg:#ffffff;--band0:#f4f5f7;--band1:#ffffff;--ink:#1d2330;--muted:#5b6475;--p:#2f5d9e;--pt:#ffffff;--s:#2f5d9e;--st:#1d2330;--u:#8a6d1d;--r:#a33a3a}}
@media (prefers-color-scheme: dark){{:root{{--bg:#14171c;--band0:#1c2027;--band1:#14171c;--ink:#e6e8ec;--muted:#a3abb9;--p:#7fa7e0;--pt:#10141a;--s:#7fa7e0;--st:#e6e8ec;--u:#d9b45a;--r:#e08080}}}}
svg{{background:var(--bg)}}
text{{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;font-size:{FS}px}}
.band0{{fill:var(--band0)}} .band1{{fill:var(--band1)}}
.lnum{{fill:var(--muted);font-weight:600}} .lname{{fill:var(--ink);font-weight:600}}
.head{{fill:var(--ink);font-size:14px;font-weight:600}} .sub{{fill:var(--muted)}} .leg{{fill:var(--muted)}}
.c-primary{{fill:var(--p);stroke:var(--p)}} .t-primary{{fill:var(--pt)}}
.c-secondary{{fill:none;stroke:var(--s);stroke-width:1.2}} .t-secondary{{fill:var(--st)}}
.c-undetermined{{fill:none;stroke:var(--u);stroke-dasharray:4 3;stroke-width:1.2}} .t-undetermined{{fill:var(--u)}}
.c-unreadable{{fill:none;stroke:var(--r);stroke-dasharray:2 3;stroke-width:1.2}} .t-unreadable{{fill:var(--r)}}
</style>
<rect width="{W}" height="{H}" fill="var(--bg)"/>
<text class="head" x="10" y="24">Who observes which layer: a first sketch</text>
<text class="sub" x="10" y="44">{len(rows)} public instruments and {len(cands)} further candidates, from their own pages read on 2 and 5 November 2026</text>
{chr(10).join(body)}
</svg>
'''
(D / "figure.svg").write_text(svg)
print("figure.svg", W, "x", H)
