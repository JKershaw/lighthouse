#!/usr/bin/env python3
"""LH062: write the derived file for each document read on 27 November 2026 (row LH062-search-read).

No body is kept: PDFs are never kept under the brief ("How fetches are made and what is kept"), and neither
HTML page read states a licence allowing redistribution. Each derived file keeps the URL, read time, status,
SHA-256 of the bytes received (copied from fetchlog.csv), the inclusion decision and the facts claims.csv
uses, with short attributed quotations. Facts were taken by the reading agent from text extracted in
memory or in the session's scratchpad (deleted at the end of the session), never from a kept body.
No credential value, repository, host or account identifier, per-provider figure, reason or finding
method is written here. Usage: python3 -I studies/LH062/derive.py
"""
import csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
from lh_fetch import write_derived  # noqa: E402

LOG = {r["id"]: r for r in csv.DictReader(open(os.path.join(HERE, "fetchlog.csv"))) if r["status"]}
PDF = "PDF: never kept under LH062's brief (email addresses in compressed streams the redaction can't reach)"
NOLIC = "no licence allowing redistribution stated on the page read (copyright notice only)"
USED = "LH062 search-and-read row, 27 November 2026: inclusion decision and claims (claims.csv)"

DOCS = {
 "D01-V1-A07": ("A07-arxiv2603.12498v3.json", PDF, {
   "title": "Keys on Doormats: Exposed API Credentials on the Web",
   "authors": "Demir, Vekaria, Smaragdakis, Durumeric",
   "version_read": "arXiv 2603.12498v3, 14 September 2026, category cs.CR (stamp on page 1)",
   "venue": "text states ACM CCS 2026 (Proceedings, 15 to 19 November 2026); venue stream, tier 1",
   "licence_statement_found": "This work is licensed under a Creative Commons Attribution 4.0 International License. (body still not kept: PDF)",
   "sha256_vs_LH061": "matches LH061's derived file A07-arxiv2603.12498.json (800ed93f...)",
   "inclusion": "included: measures removal and revocation over time (archival snapshots before notification; daily days 0 to 14 and day 172 after notification), population stated (1,748 verified credentials, 14 services, HTTP Archive September 2025 crawl), method stated (rescan and daily verification; nine HTTP Archive snapshots)",
   "facts": [
     "Population: 1,748 credentials confirmed valid, for 14 services, from HTTP Archive's September 2025 crawl (landing pages; about 10M rendered websites in the abstract, 11.9M hostnames after filtering in the method).",
     "Unprompted (archival): nine HTTP Archive snapshots, up to five years before September 2025; 'exposed credentials remain publicly accessible for an average of 12 months (min: 1; SD: 14; max: 60)'; 'In the first month after exposure, we observe a 10% reduction in the number of active credentials'; later called 'approximately 10% removed per month without intervention'.",
     "Notification: 2,435 entities notified (2,279 first-party, 156 third-party), 9,746 emails; at least one email delivered to 1,668 websites (68.5%); 'we sent notifications to 71% of sites (1,729 domains)'; reminder after one week. Day 0 = day of first disclosure email, measured before sending; calendar date not stated.",
     "Observation points after notification: daily rescan and daily validity check for the first two weeks, then one scan at day 172.",
     "After notification, exposures: 'reducing 50% from 1,405 (Day 0) to 706 (Day 14)'.",
     "After notification, still valid: 'verified credential exposures dropping from 1,175 to 865 ... about 26% within 14 days'.",
     "Day 172: 'total non-removed exposures increase from 706 (Day 14) to 1,019 (Day 172) but non-revoked exposure counts show a further decrease from 865 (Day 14) to 660 (Day 172)'. The authors offer an interpretation of the rise (not restated).",
     "Day 0 totals differ because, the authors say, some services blocked their address during verification (services not recorded here).",
     "Design: the authors compare the post-notification fall with the same credentials' archival rate; no unnotified group observed in the same period. Classed before-and-after.",
     "Data: analysis data not shared; only monitoring-crawler code released. Funder: not stated. AI providers' keys: one AI developer's API keys are among the 14 services (named by the study); no per-provider figure kept.",
     "Per-provider and per-country figures exist in the paper; not recorded (brief, Never done). The authors give reasons for exposure and for removal without revocation; not restated."]}),
 "D02-V2-A02": ("A02-meli-ndss2019.json", PDF, {
   "title": "How Bad Can It Git? Characterizing Secret Leakage in Public GitHub Repositories",
   "authors": "Meli, McNiece, Reaves", "venue": "NDSS 2019 (copy on the symposium's site); venue stream, tier 1",
   "sha256_vs_LH061": "matches LH061's derived file A02-meli-ndss2019.json (b660895a...)",
   "inclusion": "included: measures removal over time (hourly for 24 hours, then daily to 16 days), population stated as a frame (secrets collected through GitHub's Search API from 4 April 2018; count of monitored secrets not stated), method stated",
   "facts": [
     "Monitoring: 'we began monitoring all secrets collected via the Search API after they were discovered starting on April 4th, 2018'; hourly for 24 hours from discovery whether the repo, the file and the secret still existed on the head of the default branch; then daily (figure to day 16). Search API collection ran 31 October 2017 to 20 April 2018. Number of monitored secrets: not stated.",
     "'about 6% of all detected secrets were removed' in the first hour; 'at the end of the first day, over 12% of secrets were gone, while only 19% were gone after 16 days'; '81% of the secrets we discover were not removed'; '19% of our results amounts of tens of thousands of secrets'.",
     "History: for secrets removed while the repo was kept, 'none of the monitored repos had their history rewritten, meaning the secrets were trivially accessible via Git history' (checked through the Commits API).",
     "Validity over time: not measured (validity assessed at discovery only). Notification: none during monitoring; 'as of the camera-ready we are currently working to notify'. Platform notices during the window: not stated.",
     "Data: public sources (GitHub Search API, BigQuery); dataset release not stated. Funder: not stated in the text read. AI providers' keys: not among the population named."]}),
 "D03-V3-arxiv2307.09317": ("arxiv2307.09317v1.json", PDF, {
   "title": "Measuring the Leakage and Exploitability of Authentication Secrets in Super-apps: The WeChat Case",
   "authors": "Baskaran, Zhao, Mannan, Youssef",
   "version_read": "arXiv 2307.09317v1, 18 July 2023, category cs.CR (stamp on page 1); the text states RAID 2023, not one of the five conferences, so venue stream tier 2",
   "inclusion": "included: measures validity at two or more points (first analysis December 2022, recheck March 2023, July 2023) and presence in current versions (sample of 100, January and March 2023); population stated; method stated at the document's level. Its contribution includes an analysis framework and an exploitability analysis; nothing of either is recorded",
   "facts": [
     "Population: WeChat mini-app packages crawled July to December 2021 (115,392 crawled; 110,993 unpacked); app secrets found in 36,425 (32.8%) mini-apps with valid secrets at the first analysis (December 2022). The study is of one platform's mini-apps; figures are the study's whole population.",
     "Recheck: 'tested all the previously identified WeChat mini-apps with app secrets (36,425 mini-apps) if those app secrets are still valid ... in March 2023 ... for 36,293 mini-apps (99.6%) the secrets remain valid'.",
     "Sample: 100 mini-apps chosen at random from those with valid secrets; current versions downloaded 24 January and 6 March 2023, 'before and after our report to WeChat respectively': 83 still had the same secret hard-coded; 4 had removed it but the earlier secret was still valid; 3 had changed to other hard-coded values; 9 had invalid earlier secrets and no secret in current code; results the same in January and March 2023.",
     "July 2023: 'we observed a significant decrease in the percentage of valid secrets to 16.5% (18,332 mini-apps) as a result of WeChat's restrictions'; denominator not stated (16.5% matches 18,332 of the 110,993 analysed, Lighthouse's arithmetic). The causal attribution is the authors'.",
     "Notification: the authors reported to the platform operator (the secrets' issuer), between the January and March 2023 downloads (date not stated); whether owners (developers) were told is not stated; the operator's reply says it will notify developers of existing ones. The platform introduced a publishing restriction 'exact timeline unknown'.",
     "Data: not stated as released (tool offered on request). Funder: not stated. AI providers' keys: none."]}),
 "D07-W4-truffle-never-revoked": ("W4-truffle-2024-01-10.json", NOLIC, {
   "title": "74% of publicly leaked keys are never revoked", "publisher": "Truffle Security Co. (vendor; own blog, 'The Dig')",
   "author_date": "Joe Leon, 10 January 2024",
   "inclusion": "included (vendor stream): daily checks over 31 days of file availability, key presence and validity; population stated (10,000 live secrets in 9,399 public GitHub files from public event feeds, commits 28 September to 17 October 2023); method stated at the post's level",
   "facts": [
     "'74% of all leaked keys were still live/valid 31 days after being leaked.'",
     "'If a key was revoked, the developer most likely revoked it in the first 3 days.'",
     "'63% of files exposing live/valid secrets were still public and continued to expose the live/valid secret on GitHub, 31 days after exposure.'",
     "'Only 17% of all files containing a secret were unpublished; the rest remained public.' Unpublishing most likely within the first week.",
     "'In more than 50% of cases when exposed keys were taken down off GitHub, they remained live/valid.'",
     "Clock: each secret tracked 'for 31 days since the initial exposure date' (commits seen on public event feeds; whether the date is commit time or first observation is not stated). Notification of owners: not stated. Data: the vendor's own tool's data, not public."]}),
 "D08-W5-gg-why-stay-valid": ("W5-gitguardian-2025-06-05.json", NOLIC, {
   "title": "Why Most Exposed Secrets Never Get Fixed", "publisher": "GitGuardian (vendor; own blog)",
   "author_date": "Anna Nabiullina, 5 June 2025",
   "inclusion": "excluded: fails condition 3 (no stated method: how exposure and validity were established is not described in the post); relays the vendor's State of Secrets Sprawl 2025 report, whose page robots.txt refused (D05)",
   "facts": ["Headline relay only, not a claim of this study: '70% of secrets exposed in public repositories in 2022 are still valid today'. The post gives reasons; not restated. Per-service shares not recorded."]}),
 "D09-W6-gg-zombie-leaks": ("W6-gitguardian-2024-04-29.json", NOLIC, {
   "title": "Zombie Leaks: Unrevoked Secrets Lurking on GitHub", "publisher": "GitGuardian (vendor; own blog)",
   "author_date": "Thomas Segura, 29 April 2024",
   "inclusion": "included (vendor stream), narrowly: repeated validity checks over five days after the vendor's alert to repository owners; population stated as a frame (secrets the pro-bono service alerted on in public Git commits; count not stated); method stated at the post's level (repeated checks over five days). Relays the vendor's own State of Secrets Sprawl 2024 report, not read (robots refusal, D06)",
   "facts": [
     "'GitGuardian's pro-bono service alerts repository owners when we discover a leaked secret in their public Git commits. Over the next five days, we'll perform repeated checks to determine whether those secrets remain valid.'",
     "'over 91% of leaks remained valid after 5 days'.",
     "'Randomly selecting 5,000 repositories where the secret was gone within 5 days showed that 28.2% of the repositories were still public while 71.8% had been deleted or made private.' What 'gone' means is not stated.",
     "Observation period: the report's past year (calendar dates not stated). Data: the vendor's own, not public."]}),
}

for did, (fname, reason, ext) in DOCS.items():
    r = LOG[did]
    write_derived(os.path.join(HERE, "derived", fname), r["url"], reason, ext, read_utc=r["utc"],
                  final_url=r["final_url"], http_status=int(r["status"]), content_type=r["content_type"],
                  bytes=int(r["bytes"]), sha256=r["sha256"], used_for=USED)
    print("wrote", fname)
