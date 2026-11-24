# Scout 5, Research, run 2026-11-24T1213Z

**In short.** The arXiv cs.CR pastweek listing showed only 23 and 24 November in the text I could read (the 19 November listings are still not visible). Two new papers bear directly on the charter: a count of hidden AI-directed text across about 145 million GitHub items (21 November) and a preregistered study of what decides the damage of an agent's database mistake, whose finding is that recoverability is the lever (23 November). For the keeper's two directions, the literature check found a small set of independent aggregate sources for each, but only a minority of them with public data. Everything is "reported by" the page, read through WebFetch's summariser.

Started 12:15Z, ended about 12:20Z, 24 November 2026 (`date -u`). Tools: robots_gate.py, WebFetch, WebSearch, grep of notes/horizon. No direct publication checks assigned.

## Pages opened (all gated; all gate answers "allowed"; WebFetch summaries, not direct reads; status 200 unless noted)

| URL | Read (UTC) | Page date | Reported by the page |
| --- | --- | --- | --- |
| arxiv.org/list/cs.CR/pastweek?show=250 | ~12:18 | 24 Nov (23 Nov partial) | Only Tue 24 and Mon 23 Nov headings readable; first 100000 of 189306 characters read. 19 to 22 Nov not visible (gap carried forward). |
| arxiv.org/abs/2611.28763 | ~12:19 | 21 Nov 2026 | "2,281 validated findings" of AI-directed hidden text in about 145 million GitHub items; attacks "roughly one in 3.3 million items"; orchestration about two-thirds, "grew fivefold in four months". |
| arxiv.org/abs/2611.30483 | ~12:19 | 23 Nov 2026 | Preregistered, 792 Layer A cells and 9,468 agent trials: engines "differ less in what a mistake destroys than in what they let you undo". Agent-level findings preliminary. |
| arxiv.org/abs/2611.30533 | ~12:19 | 23 Nov 2026 | CyberDualEval, 430 vulnerable tasks, ten models; open-weight models "rarely refuse" on risky requests. |
| arxiv.org/abs/2512.01891 | ~12:17 | 1 Dec 2025 | Stivala et al., IEEE S&P 2026: interviews with 24 shared-hosting providers; low fees and high daily compromise volume discourage proactive and reactive security; web-app issues treated as the customer's responsibility. |
| arxiv.org/abs/1708.06693 | ~12:17 | 22 Aug 2017 | 1,259 shared hosting providers, 442,684 domains; four patching and security factors explain "between 10% and 19% of the variance in abuse" after controlling for size. |
| repository.tudelft.nl/record/uuid:b7587090-... | ~12:17 | 2015 | Asghari et al., Conficker cleanup after six years of sinkhole data; "national anti-botnet centers had no visible impact"; nearly a million machines still infected. |
| arxiv.org/abs/2603.12498 | ~12:18 | 12 Mar 2026 (v3 14 Sep) | 10 million rendered sites, 1,748 credentials for 14 providers; credentials "often persist for months to years". |
| cyentia.com/publication/prioritization-to-prediction-vol-3/ | ~12:18 | citation 2019, uploads 2026 | About 300 organisations, 2 billion vulnerabilities: half closed in about 100 days, a quarter open after a year; smaller firms fix faster, capacity about one in ten open per month at any size. Vendor-built (Kenna) sample. |
| cse.buffalo.edu/.../ndss19_domain_takedown.pdf; faculty.cc.gatech.edu/~frankli/papers/notifications_ndss_2018.pdf | ~12:17 | | Gate allowed, but WebFetch returned unreadable PDF binary; used only through search snippets (below). Not opened in effect. |

## Searches (WebSearch, standard, 7)

1. containment measures, takedown, sinkholing empirical study: snippets surfaced NDSS 2019 domain takedown (first systematic study of takedowns, sinkhole durations), Nadji et al. CCS 2013 (some takedowns effective, others no lasting impact; most of 45 botnets disabled by DNS-based takedown alone, as estimated), the Conficker cleanup paper, Kelihos news. Not opened: usenix.org/node/190883, Dark Reading, Shin TIFS12, Botacin SBSeg, Gatech Beheading Hydras pages.
2. small business patch barriers: only vendor surveys (Kaseya 2019, Bitdefender, Tripwire, Ivanti); none opened, none rigorous.
3. Dissanayake patch management: Dissanayake et al. arXiv 2012.00544 (systematic review; "only 20.8% of reported solutions rigorously evaluated in industrial settings" per snippet), 2202.09016 (healthcare field study: coordination delays most prominent cause), 2106.03458. None opened.
4. hosting, notification by size: Stock et al. USENIX Security 2016, Li et al. NDSS 2018 (notifications), Patchstack vendor test, Help Net Security coverage. Not opened.
5. Cyentia/Kenna by size: opened Vol 3 only; Vol 4 and other posts not opened.
6. credential revocation: TruffleHog (31 days, 74% still live, vendor), Meli et al. NDSS 2019, CSA note of Oct 2026 (median credential public 784 days), Cybenari canary tokens. Not opened: all except 2603.12498.
7. Verizon DBIR edge remediation: 2025 DBIR via Tenable and others (54% fully remediated, median 32 days), 2026 via watchTowr (vendor summary). None opened.

## Refused or unreached

No robots refusals. Two PDFs unreadable through the summariser. cs.CR 19 to 22 November and the cs.AI, cs.NI, cs.SE, cs.CY listings not read this run (time); venue accepted-lists (IMC, USENIX Security, NDSS, PAM) not reached. Part A is therefore thin and the 19 November gap persists.

## Part B findings

### P-0046, do containment measures work? (aggregate, methodological)

Best sources, all outcome measurements by independent parties, ranked:
1. Nadji et al., "Beheading Hydras", CCS 2013 (snippet only, not opened): retrospective takedown evaluation; some takedowns effective, others no significant long-term effect. Public data: unknown; not checked.
2. Asghari, Ciere, van Eeten, "Post-mortem of a Zombie", USENIX Security 2015 (opened record page): sinkhole data, country-level cleanup; no visible effect of national anti-botnet centres. Underlying data: not stated; reuse limited.
3. Domain takedown study, NDSS 2019 (Buffalo; snippet only): sinkhole durations by takedown party, reuse of taken-down domains. Not opened.
4. Meli et al., NDSS 2019 (snippet only) and TruffleHog 2023 (vendor): revocation after leaks; 74% still live at 31 days (vendor), revocation almost always within three days or never. CSA note of October 2026 ties survival to whether the provider revokes automatically. Credential-revocation outcomes at aggregate level; cs.CR 2603.12498 adds persistence "months to years".
5. 2611.30483 (23 Nov 2026, preregistered): recoverability over damage prevention for agent database mistakes; small open-weight models, preliminary.
Tested: DNS and sinkhole takedowns have measured, often short-lived or partial effects; provider-side automatic revocation measurably changes survival. Untested in what I found: segmentation and isolation as aggregate outcome studies (search said none surfaced); effect of containment on AI-agent incidents beyond one lab study. Candidate bounded dataset: sinkhole or Conficker-type public aggregates (Shadowserver-style public dashboards, not checked); CSA credential counts (published aggregates). No public dataset confirmed.

### P-0047, what stops small operators deploying fixes?

1. Stivala et al., S&P 2026 (arXiv 2512.01891, opened): 24 hosting providers; incentives and responsibility boundaries. Qualitative; no public data stated.
2. Tajalizadehkhoob et al. "Herding Vulnerable Cats" (arXiv 1708.06693, opened): 1,259 providers; patching factors versus abuse; provider size controlled. Data not stated.
3. Kenna/Cyentia Prioritization to Prediction Vol 3 (opened): by-size result that smaller firms fix faster, equal capacity. Vendor sample, data not public.
4. Dissanayake et al., 2012.00544 and 2202.09016 (snippets): systematic review and healthcare field study; coordination the leading delay cause. Not opened.
5. Stock et al. USENIX Security 2016 and Li et al. NDSS 2018 notification campaigns (snippets): whether notifications lead to patching. Not opened.
6. Verizon DBIR 2025 edge-device remediation (via secondary coverage): 54% fully remediated, median 32 days; no breakdown by size found. Not opened.
Gap: no direct, quantified patch timing by operator size from a public dataset found. A Lighthouse study would more safely read published aggregates (DBIR tables, Cyentia, W3Techs-style version shares as already used in LH039) than anything per host. Overlap to check: LH039 (WordPress) and LH033 (PHP, Censys) already read lagged aggregate views.

## Five best leads

1. **2611.28763, hidden AI-directed text on GitHub** (21 Nov). https://arxiv.org/abs/2611.28763. Counts agent-targeting text in 145 million items, attacks rare, orchestration growing fivefold in four months. Bears on activity on the open internet and agents online. New.
2. **2611.30483, what decides the damage of an agent's database mistake** (23 Nov). https://arxiv.org/abs/2611.30483. A preregistered containment-relevant result (recoverability). Best direct hook for P-0046. New.
3. **Asghari et al. 2015, Conficker cleanup** (https://repository.tudelft.nl/record/uuid:b7587090-7292-4836-afbc-eb8256e326b7) with Nadji et al. 2013 and NDSS 2019 takedown: the core independent outcome evidence on takedown and sinkholing. New to the horizon files.
4. **Stivala et al. 2512.01891 with 1708.06693**: independent evidence on why hosting operators do not remediate. Core for P-0047. New.
5. **Cyentia Vol 3 and the credential-persistence literature (2603.12498, Meli NDSS 2019, CSA October note)**: aggregate remediation speed by size and revocation outcomes; vendor and non-peer-reviewed caveats stated. New.
Also new, lower: 2611.30533 CyberDualEval (open-weight models "rarely refuse"), 2611.30590 POMA, 2611.30750 SchemaCaps, 2611.31010 Airlock (not opened).

## Withheld

None needed; no exposure lists or routes were compiled.
