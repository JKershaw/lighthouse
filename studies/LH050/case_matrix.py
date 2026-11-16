# Builds studies/LH050/case_matrix.csv from the cell codings below, which cite
# claims.csv and reads.csv. Run from the repository root:
#   python3 -I studies/LH050/case_matrix.py studies/LH050/case_matrix.csv
# Written for the initial record (version 0.1, 16 November 2026); no network access.
import csv, sys

OUT = sys.argv[1]
B = "studies/LH050/data/2026-11-13T1454Z/"
R = {  # read_id: (source_id, observed_at, retained path or robots record)
    "R001": ("PA-S01", "2026-11-13T14:55:02Z", B + "robots/S01_ft.json (robots decision; no body)"),
    "R003": ("PA-S03", "2026-11-13T14:55:03Z", B + "robots/S03_foundation.json (HTTP 404; no body)"),
    "R004": ("PA-S04", "2026-11-13T14:55:03Z", B + "robots/S04_marines.json (HTTP 403; no body)"),
    "R005": ("PA-S05", "2026-11-13T14:55:04Z", B + "bodies/S05_spf.html"),
    "R027": ("PA-S24", "2026-11-13T14:57:58Z", B + "bodies/S24_techcentral.html"),
    "R028": ("PA-S25", "2026-11-13T14:58:00Z", B + "bodies/S25_eweek.html"),
    "R029": ("PA-S26", "2026-11-13T14:58:02Z", B + "bodies/S26_assemblymag.html"),
    "R030": ("PA-S27", "2026-11-13T14:58:04Z", B + "bodies/S27_tnw.html"),
    "R032": ("PA-S29", "2026-11-13T14:58:56Z", B + "bodies/S29_htx_gibson.html"),
    "R033": ("PA-S28", "2026-11-13T14:59:09Z", B + "bodies/S28_spf_gibson_lc.html"),
    "R034": ("PA-Q01", "2026-11-13T14:57Z (approximate minute)", B + "searches/armed_comparison_replacement.json"),
}

FIELDS = ["armament", "AI function", "target selection", "force authorisation",
          "intervention", "deployment evidence", "civilian evidence"]

rows = []

def add(case, config, field, status, cell, label, kind, claims, reads, facet="", note=""):
    assert field in FIELDS
    assert status in {"supported-by-source", "not-established", "conflicting", "unavailable", "not-applicable"}
    rows.append({
        "case_id": case, "configuration": config, "field": field, "facet": facet,
        "status": status, "cell": cell, "label": label, "evidence_kind": kind,
        "claim_ids": ";".join("LH050-" + c for c in claims),
        "source_ids": ";".join(R[r][0] for r in reads),
        "read_ids": ";".join("LH050-" + r for r in reads),
        "read_at_utc": ";".join(R[r][1] for r in reads),
        "retained_paths": ";".join(R[r][2] for r in reads),
        "note": note,
    })

# A. Foundation, proposed Gaza application: the only lead is unreadable.
g = "Phantom, proposed Gaza application"
for f in FIELDS:
    add("foundation", g, f, "unavailable",
        "The only source for this configuration, the FT report (PA-S01), is disallowed by robots.txt for our tokens and was not requested; no source read mentions Gaza.",
        "observation (access outcome)", "third-party-report", ["C020"], ["R001"],
        note="Unavailable is not zero: no discussion, order, deployment or targeting arrangement is established or ruled out.")

# B. Foundation, Phantom as described: design and stated intentions.
d = "Phantom, design and stated company intentions (configuration not specified)"
add("foundation", d, "armament", "supported-by-source",
    "Assembly reports the Phantom is designed to carry a maximum payload of 44 pounds 'including lethal weaponry'; TechCentral reports it can carry more than 20kg of 'equipment or weapons'.",
    "observation of reported design intention", "third-party-report", ["C022", "C023"], ["R029", "R027"],
    facet="design intention",
    note="Third-party reports relaying the company and CEO; no first-party company statement retained (PA-S03 HTTP 404, claim LH050-C021).")
add("foundation", d, "armament", "not-established",
    "No source read says a Phantom has been armed, tested with a weapon or fired.",
    "observation (what the sources do not state)", "third-party-report", ["C022", "C026"], ["R027", "R028", "R029", "R030"],
    facet="fielded")
add("foundation", d, "AI function", "not-established",
    "None of the four reports read attributes any named function (navigation, perception, recommendation, target selection, engagement, abort) to AI.",
    "observation (this record's reading of the retained text, 16 November 2026)", "third-party-report", [], ["R027", "R028", "R029", "R030"],
    note="No ledger claim codes AI involvement for Foundation. Autonomy statements (C024, C025) are coded under force authorisation, not as AI evidence.")
add("foundation", d, "target selection", "not-established",
    "Who selects targets for any Phantom is not established by any source read.",
    "observation (what the sources do not state)", "third-party-report", ["C026"], ["R027", "R028", "R029", "R030"])
add("foundation", d, "force authorisation", "conflicting",
    "TechCentral (22 December 2025) reports 'Phantoms will not have full autonomy when it comes to making decisions in combat'; The Next Web (30 May 2026) reports the CEO said some weaponised uses will keep human confirmation and that in certain time-critical scenarios the robots will need to make fully autonomous decisions.",
    "observation of two reported intentions; the 'conflicting' class is this record's coding judgement", "third-party-report", ["C024", "C025"], ["R027", "R030"],
    facet="stated intention",
    note="Accounts of intention five months apart, for a configuration not shown to be fielded; they may reflect a change of position rather than a contradiction. Not resolved.")
add("foundation", d, "force authorisation", "not-established",
    "Who authorises force for any fielded Phantom is not established by any source read.",
    "observation (what the sources do not state)", "third-party-report", ["C026"], ["R027", "R028", "R029", "R030"],
    facet="in practice")
add("foundation", d, "intervention", "not-established",
    "No intervention or abort mechanism for any Phantom is described in the sources read.",
    "observation (what the sources do not state)", "third-party-report", ["C026"], ["R027", "R028", "R029", "R030"])
add("foundation", d, "deployment evidence", "supported-by-source",
    "Proposals and reported research contracts only: $24 million in US Army, Navy and Air Force research contracts for feasibility testing (no award record read); production targets that differ between reports; a target of front-line US deployment within 12 to 18 months (The Next Web; eWeek gives the period as an aim to begin testing with the US military).",
    "observation of reported claims", "third-party-report", ["C030", "C032", "C033"], ["R030", "R029", "R027", "R028"],
    note="Events LH050-E005 (award/purchase as reported) and LH050-E006 (proposal). No delivery or operational use of an armed configuration is established. Research contracts are not a weapons purchase.")
add("foundation", d, "civilian evidence", "not-established",
    "No report of civilian harm, coercion, complaint, investigation or remedy involving Phantom appears in the sources read; harm, operator attribution and AI-function attribution are each not established.",
    "observation (what the sources do not state)", "third-party-report", ["C034"], ["R027", "R028", "R029", "R030"],
    note="Not zero. Specialist harm sources were not searched for this case; the Gaza reporting was unavailable.")

# C. Foundation, Phantom MK-1 Ukraine logistics pilot.
u = "Phantom MK-1, Ukraine logistics pilot (two robots, as reported)"
add("foundation", u, "armament", "not-established",
    "The reports describe logistics demonstrations (retrieving and transporting supplies); none states whether the two robots sent were armed.",
    "observation (what the sources do not state)", "third-party-report", ["C027"], ["R028", "R030"])
add("foundation", u, "AI function", "not-established",
    "Neither report of the pilot attributes any function to AI.",
    "observation (this record's reading of the retained text, 16 November 2026)", "third-party-report", [], ["R028", "R030"])
add("foundation", u, "target selection", "not-established",
    "Not described for the pilot; the pilot is described as logistics.",
    "observation (what the sources do not state)", "third-party-report", ["C026"], ["R028", "R030"])
add("foundation", u, "force authorisation", "not-established",
    "Not described for the pilot.",
    "observation (what the sources do not state)", "third-party-report", ["C026"], ["R028", "R030"])
add("foundation", u, "intervention", "not-established",
    "Not described for the pilot.",
    "observation (what the sources do not state)", "third-party-report", ["C026"], ["R028", "R030"])
add("foundation", u, "deployment evidence", "supported-by-source",
    "eWeek and The Next Web report two MK-1 robots were sent to Ukraine 'earlier this year' for pilot demonstrations of logistics, with Ukrainian officials and US government support; eWeek relays the company's claim of 'the first known use of humanoid robots in an active combat theater'; both report the MK-1 lacks waterproofing and battery life, and eWeek calls the robots 'far from battlefield-ready'.",
    "observation of reported claims", "third-party-report; supplier-claim (C028)", ["C027", "C028", "C029"], ["R028", "R030"],
    note="Event LH050-E004, maturity stage demonstration. Event date not given beyond 'earlier this year' in sources dated 30 May and 3 June 2026. Both reports rest on the company and a CNBC interview; repetition adds no corroboration. No Ukrainian or US official record read.")
add("foundation", u, "civilian evidence", "not-established",
    "No civilian harm, complaint, investigation or remedy is reported for the pilot in the sources read.",
    "observation (what the sources do not state)", "third-party-report", ["C034"], ["R028", "R030"],
    note="Not zero.")

# D. Armed non-humanoid comparison: unavailable.
a = "candidate: US Marine Corps armed quadruped test, 2023 (not admitted)"
for f in FIELDS:
    add("armed-comparison", a, f, "unavailable",
        "The candidate record (PA-S04) returned HTTP 403, a wall not retried; the brief's single replacement query (PA-Q01) returned no first-party armed ground-robot test record in its first ten results, so no case was admitted.",
        "observation (access and selection outcome)", "official-account", ["C040"], ["R004", "R034"],
        note="Results judged by domain and title without opening; connector order retained, completeness unverifiable. Amendment 1's Ukraine series does not fill this comparison.")

# E. Changi, SPF patrol robot (2023 type).
c = "SPF patrol robot (2023 type), Changi Airport Terminal 4"
add("changi", c, "armament", "not-established",
    "The SPF release describes no weapon or force capability beyond 'interim intervention measures (blinkers, siren, and speakers)'.",
    "observation (what the source does not state)", "official-account", ["C004", "C006"], ["R005"],
    note="Absence of mention is not evidence of absence; armament not established either way.")
add("changi", c, "AI function", "not-established",
    "SPF calls the robot 'capable of autonomous patrol' (automated navigation, supported by source) and describes a mast camera giving the Operations Room a live view; it does not say any function uses AI or machine learning.",
    "observation", "official-account", ["C002", "C003"], ["R005"])
add("changi", c, "target selection", "not-established",
    "Not stated. No force capability is described, but the sources do not establish that the robot is unarmed, so the field is not marked not-applicable.",
    "observation; class chosen by this record", "official-account", ["C006"], ["R005"])
add("changi", c, "force authorisation", "not-established",
    "Who sets missions and who triggers the warning measures is not stated.",
    "observation (what the source does not state)", "official-account", ["C005"], ["R005"])
add("changi", c, "intervention", "not-established",
    "How an operator overrides the robot is not stated; the Operations Room's live view and two-way communication do not by themselves establish the control arrangement.",
    "observation (what the source does not state)", "official-account", ["C003", "C005"], ["R005"])
add("changi", c, "deployment evidence", "supported-by-source",
    "SPF states patrol robots have been deployed at Terminal 4 since April 2023 and that it plans to deploy more across Singapore.",
    "observation of an official account", "official-account", ["C001", "C007"], ["R005"],
    note="Events LH050-E001 (operational use, month precision) and LH050-E002 (proposal). Official account, not independent verification; number of robots and status after June 2023 not stated.")
add("changi", c, "civilian evidence", "not-established",
    "No complaint, privacy assessment, harm report, investigation or remedy appears in the sources read.",
    "observation (what the sources do not state)", "official-account", ["C008"], ["R005", "R033", "R032"],
    note="Not zero. No civil-society or complaints source was read; all Changi sources are one government family.")

# F. Changi, GIBSON.
gb = "GIBSON rideable indoor patrol robot, Terminal 4 Departure Hall"
add("changi", gb, "armament", "not-established",
    "Neither SPF nor HTX describes any weapon or force capability on GIBSON.",
    "observation (what the sources do not state)", "official-account", ["C015"], ["R033", "R032"],
    note="Not established either way.")
add("changi", gb, "AI function", "not-established",
    "SPF says in autonomous mode GIBSON navigates with 3D LiDAR, depth cameras and SONAR, detecting obstacles and avoiding collisions (automated navigation, supported by source); neither source says any function uses AI or machine learning.",
    "observation", "official-account", ["C011"], ["R033", "R032"])
add("changi", gb, "target selection", "not-established",
    "Not stated; no force capability is described, and the field is not marked not-applicable because armament is not established.",
    "observation; class chosen by this record", "official-account", ["C015"], ["R033", "R032"])
add("changi", gb, "force authorisation", "not-established",
    "Not stated.",
    "observation (what the sources do not state)", "official-account", ["C015"], ["R033", "R032"])
add("changi", gb, "intervention", "supported-by-source",
    "HTX says officers must arm and activate the handlebar when first taking over manual control; SPF and HTX say officers summon it by app and ride it; HTX says stop sensors and a cordon were added after people tried to mount it in autonomous mode.",
    "observation of an official (developer) account", "official-account", ["C012", "C013", "C014"], ["R032", "R033"],
    note="Takeover and stop mechanisms for mobility and safety, not for force. Who sets autonomous patrol missions is not stated.")
add("changi", gb, "deployment evidence", "supported-by-source",
    "SPF says GIBSON has been on trial at the Terminal 4 Departure Hall since July 2025.",
    "observation of an official account", "official-account", ["C010"], ["R033"],
    note="Event LH050-E003, trial. Status after July 2025 not established.")
add("changi", gb, "civilian evidence", "supported-by-source",
    "HTX reports the public was largely unresponsive to a recorded 'Excuse me' message (replaced by a beep) and that people tried to mount GIBSON while it moved autonomously.",
    "observation of an official (developer) account", "official-account", ["C014"], ["R032"],
    facet="reported public interaction")
add("changi", gb, "civilian evidence", "not-established",
    "No injury, complaint, harm, investigation or remedy is reported; operator and AI-function attribution therefore have nothing established to attach to.",
    "observation (what the sources do not state)", "official-account", ["C014"], ["R032", "R033"],
    facet="harm",
    note="Not zero. Developer and police accounts only.")

cols = ["case_id", "configuration", "field", "facet", "status", "cell", "label", "evidence_kind",
        "claim_ids", "source_ids", "read_ids", "read_at_utc", "retained_paths", "note"]
with open(OUT, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)

from collections import Counter
print(len(rows), "rows")
print(Counter(r["status"] for r in rows))
by = Counter((r["case_id"], r["configuration"][:30], r["status"]) for r in rows)
for k, v in sorted(by.items()):
    print(k, v)
print(Counter(r["case_id"] for r in rows))
