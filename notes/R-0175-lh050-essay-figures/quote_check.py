"""R-0175: check every quotation in the LH050 essay draft against Lighthouse's retained copies.
Run from the repository root: python3 -I notes/R-0175-lh050-essay-figures/quote_check.py
Text extraction: standard-library regex tag strip + html.unescape for HTML; pdftotext -layout and plain for the PDF.
Whitespace is collapsed and curly quotes/apostrophes normalised before substring search."""
import re, html, subprocess, json, hashlib

B = 'studies/LH050/data/2026-11-13T1454Z/bodies/'
P = 'studies/LH050/data/2026-11-27T1415Z/bodies/S44_crp1_rev3.pdf'

def norm(t):
    t = t.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"').replace(' ', ' ')
    return re.sub(r'\s+', ' ', t)

def htmltext(path):
    t = open(path, encoding='utf-8', errors='replace').read()
    t = re.sub(r'(?is)<(script|style|noscript)\b.*?</\1>', ' ', t)
    t = re.sub(r'(?s)<!--.*?-->', ' ', t)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    return norm(t)

def pdftext(path):
    out = subprocess.run(['pdftotext', path, '-'], capture_output=True, text=True).stdout
    # join hyphen-free line breaks
    return norm(out)

src = {
 'S24_techcentral': htmltext(B + 'S24_techcentral.html'),
 'S25_eweek': htmltext(B + 'S25_eweek.html'),
 'S27_tnw': htmltext(B + 'S27_tnw.html'),
 'S05_spf': htmltext(B + 'S05_spf.html'),
 'S28_spf_gibson': htmltext(B + 'S28_spf_gibson_lc.html'),
 'S29_htx': htmltext(B + 'S29_htx_gibson.html'),
 'S11_icrc': htmltext(B + 'S11_icrc_faq.html'),
 'S44_final': pdftext(P),
}
assembly = json.load(open(B + 'S26_assemblymag.derived.json'))
src['S26_assembly_derived'] = norm(' '.join(sum(assembly['extracted']['quotes_used'].values(), [])))

quotes = [
 ('S26_assembly_derived', 'is designed to carry a maximum payload of 44 pounds, including lethal weaponry'),
 ('S24_techcentral', 'can carry more than 20kg of equipment or weapons'),
 ('S25_eweek', 'earlier this year'),
 ('S25_eweek', 'remain far from battlefield-ready'),
 ('S25_eweek', 'lacks waterproofing, and does not yet have the battery life needed for extended deployments'),
 ('S27_tnw', 'earlier this year'),
 ('S27_tnw', 'for feasibility testing in inspection, logistics, and weapons handling'),
 ('S24_techcentral', 'Phantoms will not have full autonomy when it comes to making decisions in combat'),
 ('S27_tnw', 'said some weaponised uses of the Phantom robots will retain human confirmation in the decision loop'),
 ('S27_tnw', 'In certain time-critical scenarios, the robots will need to make fully autonomous decisions.'),
 ('S25_eweek', 'for industrial work and defense applications'),
 ('S27_tnw', 'Making robots look like humans is a complex and expensive engineering challenge.'),
 ('S24_techcentral', 'could paradoxically make military action more likely by reducing the perceived risks and consequences'),
 ('S11_icrc', 'requires qualitative understanding of factors such as intent, conduct and context that a machine calculation cannot provide'),
 ('S11_icrc', 'can change rapidly'),
 ('S11_icrc', 'International humanitarian law already applies to autonomous weapons'),
 ('S11_icrc', 'does not disappear simply because technology becomes more accurate'),
 ('S11_icrc', 'designed to target humans directly'),
 ('S11_icrc', 'unpredictable in their effects'),
 ('S11_icrc', 'not whether the weapon flies autonomously, but whether it has autonomy in the critical targeting functions'),
 ('S05_spf', 'capable of autonomous patrol'),
 ('S05_spf', 'interim intervention measures (blinkers, siren, and speakers) to enforce a cordon or warn bystanders'),
 ('S05_spf', 'April 2023'),
 ('S28_spf_gibson', 'on trial at the Terminal 4 Departure Hall since July 2025'),
 ('S29_htx', 'arm and activate the handlebar when they first take over manual control'),
 ('S29_htx', 'largely unresponsive'),
 ('S29_htx', 'Excuse me'),
 ('S44_final', 'is to continue'),
 ('S44_final', 'to elaborate, by consensus, an instrument, without prejudging its nature, that specifies international humanitarian law, including principles and requirements, applicable to lethal autonomous weapon systems'),
 ('S44_final', 'for 10 days in Geneva each year'),
 ('S44_final', 'to the 2028 Meeting'),
 ('S44_final', 'whether the High Contracting Parties should adopt the instrument as a binding protocol'),
 ('S44_final', 'as orally amended'),
 ('S44_final', 'Final document'),
]
print('PDF sha256', hashlib.sha256(open(P, 'rb').read()).hexdigest())
for k, q in quotes:
    n = src[k].count(norm(q))
    print(f'{"OK " if n else "MISS"} {n} {k}: {q}')

print('\n-- word search in final document (case-insensitive) --')
low = src['S44_final'].lower()
for w in ['human control', 'negotiat', 'binding', 'legally binding', 'moratorium', 'deadline', 'mandate']:
    print(w, low.count(w))
print('\n-- weapon in Changi texts (case-insensitive) --')
for k in ['S05_spf', 'S28_spf_gibson', 'S29_htx']:
    print(k, src[k].lower().count('weapon'), 'arm(ed)', len(re.findall(r'\barmed\b', src[k].lower())))
print('\n-- precision/civilian/casualty in Foundation reports --')
for k in ['S24_techcentral', 'S25_eweek', 'S27_tnw']:
    l = src[k].lower(); print(k, {w: l.count(w) for w in ['precis', 'civilian', 'casualt', 'gaza', 'israel']})

print('\n-- misses re-checked case-insensitively and without trailing punctuation --')
for k, q in quotes:
    if src[k].count(norm(q)) == 0:
        q2 = norm(q).rstrip('.').lower()
        i = src[k].lower().find(q2)
        print(('FOUND' if i >= 0 else 'STILL MISSING'), k, '|', src[k][max(0, i - 5):i + len(q2) + 6] if i >= 0 else q)

print('\n-- final document context: para 49 subject; para 31 --')
f = src['S44_final']
i = f.find('49. The Seventh Review Conference decides that the work'); print(f[i:i + 420])
i = f.find('31. At its final plenary'); print(f[i:i + 260])
print('\n-- final document: passages on how weapons are used (tests the essay line "neither says anything about how any state builds or uses a weapon") --')
for w in ['condemns any use of incendiary weapons', 'Calls on all parties to armed conflicts to respect', 'all feasible precautions, in the use of laser systems']:
    print(w, f.count(w))
