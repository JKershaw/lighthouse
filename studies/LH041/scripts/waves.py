"""LH041 protocol: the waves, their named indicators, seeds and vendor clocks.

Fixed with the brief (studies/LH041/brief.md, protocol 0.1, 8 November 2026)
before any OSV record of the waves was read. Every indicator is quoted from a
source retained under data/prebrief/web/ (file named in `src`). Changing this
file after collection is an amendment and must be dated in the brief.

Matching (see brief, "How a record joins a wave"):
- The text searched is the whole OSV record serialised as JSON, lower-cased,
  with defanging undone ("[.]" and "(.)" and "[dot]" become ".", "hxxp" becomes
  "http").
- `specific` indicators assign a record to that wave. A record matching the
  specific indicators of two or more waves is "ambiguous" and counted in none.
- `shared` indicators belong to more than one wave; a record matching only
  shared and lineage indicators is assigned by date window, like a lineage-only
  record, among the waves that list that shared indicator.
- LINEAGE markers make a record "lineage"; it joins a wave only by window.
- `seeds` are packages a source names as the wave's first or headline victims;
  they are a coverage check and never assign a record by themselves.
"""

# Lineage markers: names of the family and its operators, as the sources use them.
LINEAGE = [
    r"shai[- _]?hulud", r"sha1[- _]?hulud", r"mini shai", r"miasma", r"chaindrop",
    r"canistersprawl", r"canisterworm", r"teampcp", r"\bhades\b",
]

WAVES = [
    dict(id="W01", name="Shai-Hulud", eco=["npm"], vendor_clock="2025-09 (month only)",
         window=("2025-09-01", "2025-10-14"), src="w16 (Unit 42, updated 26 Nov 2025)",
         specific=[r"shai-hulud-workflow", r"bb8ca5f6-4175-45d2-b042-fc9ebb8170b7",
                   r"46faab8ab153fae6e80e7cca38eab363075bb524edd79e42269217a083628f09"],
         shared=[], seeds=["@ctrl/tinycolor"]),
    dict(id="W02", name="Shai-Hulud 2.0 (Sha1-Hulud: The Second Coming)", eco=["npm"],
         vendor_clock="2025-11 (month only; 'first reported in early November')",
         window=("2025-11-01", "2025-12-14"), src="w16 (Unit 42, updated 26 Nov 2025)",
         specific=[r"setup_bun\.js", r"bun_environment\.js", r"sha1-hulud", r"the second coming",
                   r"62ee164b9b306250c1172583f138c9614139264f889fa99614903c12755468d0",
                   r"f099c5d9ec417d4445a0328ac0ada9cde79fc37410914103ae9c609cbc0ee068",
                   r"cbb9bc5a8496243e02f3cc080efbe3e4a1430ba0671f2e43a202bf45b05479cd",
                   r"a3894003ad1d293ba96d77881ccd2071446dc3f65f434669b49b3da92421901a"],
         shared=[], seeds=["@zapier/", "@ensdomains/"]),
    dict(id="W03", name="CanisterSprawl", eco=["npm", "PyPI"],
         vendor_clock="2026-04-21T22:14Z (pgserve 1.1.11, CSA)",
         window=("2026-04-20", "2026-05-05"), src="w15 (The Hacker News), w17 (CSA)",
         specific=[r"api-monitor\.com", r"cjn37-uyaaa-aaaac-qgnva-cai", r"hacked by teampcp",
                   r"canistersprawl"],
         shared=[], seeds=["pgserve", "@automagik/genie"]),
    dict(id="W04", name="Shai-Hulud: The Third Coming (Bitwarden CLI, Checkmarx)", eco=["npm"],
         vendor_clock="2026-04-22 17:57 'EST' (Bitwarden via Unit 42; 21:57 or 22:57 UTC)",
         window=("2026-04-21", "2026-05-06"), src="w07 (Unit 42 npm threat landscape, updated 15 Jul 2026)",
         specific=[r"third coming", r"\bbw1\.js", r"bw_setup\.js", r"audit\.checkmarx\.cx",
                   r"longlivetheresistanceagainstmachines", r"beautifulcastle",
                   r"checkmarx configuration storage"],
         shared=[], seeds=["@bitwarden/cli"]),
    dict(id="W05", name="Mini Shai-Hulud, SAP wave", eco=["npm"], vendor_clock="2026-04-29 (Unit 42)",
         window=("2026-04-28", "2026-05-10"), src="w07 (Unit 42)",
         specific=[r"a mini shai-hulud has appeared", r"ohnowhatsgoingonwithgithub", r"ctf-scramble"],
         shared=[], seeds=["@cap-js/sqlite", "@cap-js/db-service"]),
    dict(id="W06", name="Mini Shai-Hulud, TanStack wave", eco=["npm", "PyPI"],
         vendor_clock="2026-05-11T19:20Z (CSA; StepSecurity)",
         window=("2026-05-10", "2026-05-18"), src="w01 (StepSecurity), w07 (Unit 42), w12 (CSA)",
         specific=[r"router_init\.js", r"tanstack_runner\.js", r"@tanstack/setup", r"opensearch_init\.js",
                   r"79ac49eedf774dd4b0cfa308722bc463cfe5885c",
                   r"ab4fcadaec49c03278063dd269ea5eef82d24f2124a8e15d7b90f2fa8601266c"],
         shared=[], seeds=["@tanstack/"]),
    dict(id="W07", name="Mini Shai-Hulud, AntV wave", eco=["npm"],
         vendor_clock="2026-05-19T01:39Z (Snyk)",
         window=("2026-05-18", "2026-05-31"), src="w10 (Snyk), w07 (Unit 42)",
         specific=[r"m-kosche", r"niaga og ew ereh"],
         shared=[], seeds=["@antv/"]),
    dict(id="W08", name="Miasma (Red Hat and others)", eco=["npm"], vendor_clock="2026-06-01 (Unit 42)",
         window=("2026-05-31", "2026-06-14"), src="w07 (Unit 42), w02 (SecurityWeek)",
         specific=[r"spreading blight"],
         shared=[], seeds=["@redhat-cloud-services/"]),
    dict(id="W09", name="Hades (PyPI branch of Miasma)", eco=["PyPI"],
         vendor_clock="2026-06 (month only; second wave 8 June, SecurityWeek)",
         window=("2026-06-01", "2026-06-21"), src="w02 (SecurityWeek, 9 Jun 2026)",
         specific=[r"end for the damned"],
         shared=[], seeds=[]),
    dict(id="W10", name="miasma-train-p1 (AsyncAPI)", eco=["npm"], vendor_clock="2026-07-14 (Unit 42)",
         window=("2026-07-13", "2026-07-28"), src="w07 (Unit 42)",
         specific=[r"miasma-train", r"qmet4fhsaawmbuxndfrehwgiydeswy4ysys9wikuw5jgyf",
                   r"qmqobzsp1wrprpseq56qnyq7eczh5bg5k1fnjt4suwwhb9", r"85\.137\.53\.71",
                   r"0x12c37a86a0ed0bebe5d1d6a43e42f07860eac710"],
         shared=[], seeds=["@asyncapi/specs", "@asyncapi/generator-helpers", "@asyncapi/generator-components"]),
    dict(id="W11", name="ChainDrop", eco=["npm"],
         vendor_clock="2026-08-04T09:38:13Z (first publish, StepSecurity)",
         window=("2026-08-03", "2026-08-18"), src="w19 (StepSecurity), w13 (Elastic), w18 (Unit 42), w03 (BleepingComputer)",
         specific=[r"math_init\.js", r"npm-cache\.com", r"awqhnjewqjkl\.icu", r"thebeautifulmarchoftime",
                   r"chaindrop", r"9fc2570b7cef51c1b8df116d144d11ff4096357be7d2c4c6367cfc2509cf1bcc",
                   r"54dc7ea54a1317cca0e890a2770630cf7fa6c97813e0cb9d2caa93012b350668",
                   r"codeql_analysis\.yml"],
         shared=[r"math_symbol\.js", r"here we go again"], seeds=["keyv"]),
    dict(id="W12", name="MemTensor (sckit)", eco=["npm", "PyPI"],
         vendor_clock="2026-09 (month only; The Hacker News, 23 Sep 2026)",
         window=("2026-09-01", "2026-09-30"), src="w04 (The Hacker News)",
         specific=[r"skyleen"],
         shared=[], seeds=["@memtensor/memos-cloud-openclaw-plugin", "memoryos"]),
    dict(id="W13", name="Tensorlake", eco=["npm"], vendor_clock="2026-10-08 (Aikido)",
         window=("2026-10-07", "2026-10-22"), src="w14 (Aikido)",
         specific=[r"iseekaigogo", r"tensrlake",
                   r"b50a00900399ba99fb6ce1fc151519cb99d44320ef2a631f2237e1aea0ad6fec",
                   r"25a0735d0db7dc40e5d45ce42d9c106067e6a66e184d967cfecfab17c3bcb5ef"],
         shared=[r"math_symbol\.js", r"here we go again"], seeds=["tensorlake"]),
]

# "Here We Go Again" is ChainDrop's repository description (w18, w03) and, reversed,
# the AntV wave's (w10, w07); the reversed form is W07's specific indicator, the
# plain form is shared between W11 and W13 (Tensorlake's OX headline, a search
# result only). W07 is not given the plain form because its sources give it reversed.
