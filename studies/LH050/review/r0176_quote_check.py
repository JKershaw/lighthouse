"""R-0176 stage 2: check the essay's quotations against LH050's retained copies.
Run: python3 -I studies/LH050/review/r0176_quote_check.py  (from the repository root)"""
import html, json, re, subprocess, sys
from html.parser import HTMLParser
B = "studies/LH050/data/2026-11-13T1454Z/bodies/"
class T(HTMLParser):
    def __init__(s): super().__init__(); s.o=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in ("script","style"): s.skip+=1
    def handle_endtag(s,t):
        if t in ("script","style") and s.skip: s.skip-=1
    def handle_data(s,d):
        if not s.skip: s.o.append(d)
def text(p):
    if p.endswith(".pdf"):
        t = subprocess.run(["pdftotext","-layout",p,"-"],capture_output=True,text=True).stdout
    elif p.endswith(".json"):
        t = json.dumps(json.load(open(p)), ensure_ascii=False)
    else:
        x=T(); x.feed(open(p,encoding="utf-8",errors="replace").read()); t=" ".join(x.o)
    t = t.replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"').replace(" "," ")
    return re.sub(r"\s+"," ",html.unescape(t))
Q = {
 B+"S26_assemblymag.derived.json": ["is designed to carry a maximum payload of 44 pounds, including lethal weaponry"],
 B+"S24_techcentral.html": ["can carry more than 20kg of equipment or weapons","Phantoms will not have full autonomy when it comes to making decisions in combat","could paradoxically make military action more likely by reducing the perceived risks and consequences"],
 B+"S25_eweek.html": ["earlier this year","remain far from battlefield-ready","lacks waterproofing, and does not yet have the battery life needed for extended deployments","for industrial work and defense applications","Army, Navy, and Air Force","previously investing"],
 B+"S27_tnw.html": ["for feasibility testing in inspection, logistics, and weapons handling","said some weaponised uses of the Phantom robots will retain human confirmation in the decision loop","In certain time-critical scenarios, the robots will need to make fully autonomous decisions.","Making robots look like humans is a complex and expensive engineering challenge","Army, Navy","Sisson"],
 B+"S05_spf.html": ["capable of autonomous patrol","interim intervention measures (blinkers, siren, and speakers) to enforce a cordon or warn bystanders","April 2023"],
 B+"S28_spf_gibson_lc.html": ["on trial at the Terminal 4 Departure Hall since July 2025"],
 B+"S29_htx_gibson.html": ["arm and activate the handlebar when they first take over manual control","largely unresponsive","Excuse me"],
 B+"S11_icrc_faq.html": ["requires qualitative understanding of factors such as intent, conduct and context that a machine calculation cannot provide","can change rapidly","International humanitarian law already applies to autonomous weapons","does not disappear simply because technology becomes more accurate","designed to target humans directly","unpredictable in their effects","not whether the weapon flies autonomously, but whether it has autonomy in the critical targeting functions"],
 "studies/LH050/data/2026-11-27T1415Z/bodies/S44_crp1_rev3.pdf": ["is to continue","to elaborate, by consensus, an instrument, without prejudging its nature, that specifies international humanitarian law, including principles and requirements, applicable to lethal autonomous weapon systems","for 10 days in Geneva each year","to the 2028 Meeting","whether the High Contracting Parties should adopt the instrument as a binding protocol","as orally amended"],
}
ABSENT = {"studies/LH050/data/2026-11-27T1415Z/bodies/S44_crp1_rev3.pdf": ["human control","negotiat","legally binding"]}
for p,qs in Q.items():
    t=text(p)
    for q in qs: print("FOUND " if q in t else "MISSING", p.split("/")[-1], "|", q)
for p,ws in ABSENT.items():
    t=text(p).lower()
    for w in ws: print("COUNT", t.count(w), p.split("/")[-1], "|", w)
