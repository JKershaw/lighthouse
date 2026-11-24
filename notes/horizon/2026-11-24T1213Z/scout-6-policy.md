# Scout 6, Policy and institutions, run 2026-11-24T1213Z

**In short.** The CCW Seventh Review Conference has an outcome, reported by one academic legal blog (21 November): the conference tasked the Group of Governmental Experts "to elaborate, by consensus, an instrument, without prejudging its nature", meeting in 2027 and 2028, with no negotiating mandate. Several secondary items say US and Russian opposition kept the stronger mandate out; I read none of them as a primary text. For Part B, the best voluntary exercise reports are CISA's Cyber Storm IX after-action report (September 2024, 37 pages, 8 findings, qualitative) and SIFMA's Quantum Dawn VII public report (1 May 2024, survey percentages), with Bank of England SIMEX 24 as a counter-example that published no outcomes. ENISA's Cyber Europe reports are robots-refused to Anthropic's agents, so they are leads only. Everything is "reported by" the page named; WebFetch is a summariser, so quotations are as relayed (PDF text below was extracted locally with pdftotext from the saved bodies, so those are direct reads).

Start 12:15 UTC, end about 12:18 UTC, 24 November 2026 (`date -u`). Sonnet-class scout. Tools: WebSearch, WebFetch, scripts/robots_gate.py (provider anthropic) before each fetch, pdftotext on saved PDFs under the scratchpad (not in the repository), grep of notes/horizon. No keys read, harbour/.session/ untouched, nothing committed.

## Direct publication checks

Scout 6 has no feed endpoint named in plan.md for this run beyond my own searches; none attempted. Gap noted, not a failure.

## Pages opened

| URL | UTC read | Gate | HTTP | Page date | Reported claim | New? |
|---|---|---|---|---|---|---|
| https://apils.org/2026/11/21/ccw-seventh-review-conference-a-new-mandate-on-autonomous-weapons-but-no-review/ | ~12:16 | allowed | 200 (summariser) | 21 Nov 2026 | Reported by APILS: conference "to elaborate, by consensus, an instrument, without prejudging its nature"; GGE meets 2027 and 2028 and reports to the 2028 Meeting of High Contracting Parties with a recommendation on legal nature and form; GGE adopted "elements" in Sept 2026 and the mandate builds on them; Russia blocked consensus on agenda and rules over observer limits (page does not say Russia opposed the mandate itself); headline says "no review" (the review of the Convention itself not completed). | New |
| https://www.jurist.org/news/2026/11/un-arms-conference-falls-short-of-treaty-mandate-on-autonomous-weapons-due-to-us-and-russia-opposition/ | ~12:16 | allowed | 403 | n/a | Wall, body not read. Title only: falls short of treaty mandate due to US and Russia opposition. | New (title only) |
| https://www.cisa.gov/cyber-storm-ix-national-cyber-exercise | ~12:16 | allowed | 200 (summariser) | exercise April 2024 | Reported by CISA: report is the Cyber Storm IX After-Action Report; "3 days of live play"; objectives only, no findings on the page. | New |
| https://cisa.gov/sites/default/files/2024-10/Cyber%20Storm%20IX%20After-Action%20Report%20v00%2020241001_508.pdf | ~12:16 | allowed | 200, PDF 925 KB, read locally | "September 2024", TLP:CLEAR | Direct read: 8 numbered findings (cloud security; internal processes; information sharing; incident reporting; federal coordination; international coordination; distributed sharing networks; established relationships), a consolidated recommendations section, participant appendix. Findings are stated as qualitative lessons; I did not tabulate quantities. | New |
| https://www.sifma.org/wp-content/uploads/2024/04/SIFMA-Quantum-Dawn-VII_Public-AAR-FINAL.pdf | ~12:16 | allowed | 200, PDF 2.1 MB, read locally | file metadata 26 to 30 Apr 2024; release 1 May 2024 per search result | Direct read: "A majority of participants (75%) reported having experienced the loss of a critical third party"; "Ninety-eight percent of firms have developed and maintain response and recovery plans for their critical third parties, and 80% of firms state their plans can account for outages lasting 24 hours or more." Figures are participant self-reports from in-exercise polls, plus role breakdown (about 62%, 22%, ~44% management titles). | New |
| https://www.bankofengland.co.uk/news/2024/october/simex-24-testing-the-uk-financial-sector-resilience | ~12:16 | allowed | 200 (summariser) | 2 Oct 2024 | Reported by the Bank: SIMEX 24 tested a major infrastructure failure needing full shutdown and restart; page "reports no results, metrics, or specific outcomes" and does not promise publication. | New |
| https://www.bankofengland.co.uk/financial-stability/boe-system-wide-exploratory-scenario-exercise/boe-swes-exercise-final-report | ~12:16 | allowed | 200 (summariser, 100k of 968k characters read) | 29 Nov 2024 per page | Reported by the Bank: SWES involved "around 50 different financial firms"; six conclusions not read. Note SWES is a market-stress scenario, not a cyber recovery exercise, so a weak fit. | New |

## Searches

1. CCW Review Conference autonomous weapons outcome final report negotiating mandate: pre-conference only (HRW 7 Sep, 12 and 18 Nov, ICRC). Not opened: HRW items, ICRC statement, transcripts.un.org, Stop Killer Robots GGE page, Harvard clinic pieces.
2. Extended: "Review Conference" CCW concluded ... : found APILS and JURIST (above). Not opened: dev.to piece, archyde, anarchistfederation, dailynewsegypt, streamlinefeed, strongmocha, Wikipedia GGE page (secondary or low-quality; one says the Eighth Review Conference is about 2031, from a "UN draft cited by a secondary source": unverified). Search summary also relayed a quote from the Conference president and an ICRC regret statement, both unopened, so not relied on.
3. Cyber Europe after action report ENISA: ENISA pages for 2014, 2018, 2022, 2024 reports; Cyber Europe 2026 announcement says findings will go in after-action reports (none out). Not opened (robots-refused for Anthropic agents).
4. Cyber Storm IX after action report: CISA pages for IX, VIII (Aug 2022 file), VI, 2020 (Jan 2021), V (2016) reports. Only IX opened.
5. Locked Shields 2026 and Quantum Dawn VII: Locked Shields coverage is press and vendor (SecurityWeek, Dynatrace, AWS); CCDCOE's own lessons text not seen. Not opened.
6. Bank of England SIMEX/SWES: opened two pages above.
7. Cyber Europe 2024 AAR figures: ENISA news item and PDF (robots-refused). Snippets via search only: about 5,000 participants, energy sector, 19 to 20 June 2024, report 10 Dec 2024; a snippet claims distribution is restricted to planners and participants, conflicting with the public listing: unresolved.

## Refused or unreached

- ENISA Cyber Europe 2024 AAR page, node/19416, and the AAR PDF: robots.txt disallows for provider anthropic (recurring access). Not fetched. A CERT-LV copy exists but was not opened (sidestepping the owner's rule; not gated).
- JURIST: HTTP 403, recorded.

## Part A: since 20 November

- CCW: outcome as above, reported by one blog; primary text (final report or decision on docs-library.unoda.org or UN Geneva) not yet located. LH050 note: the conference outcome is a policy framework item, not clearly one of the listed claim kinds; I would class it as an adopted-process outcome (a mandate to elaborate an instrument), a proposal-stage, not a rule, and no implementation evidence exists.
- Not found this sweep (searches 1 to 2 only, so weak): any revised Directive 3000.09; EU AI Office agents guidance; NIST/CAISI or UK AISI agents publications; IETF changes since 20 November; court actions on crawlers; any armed-robot procurement, suspension or civilian-consequence claim. These were not specifically searched again this run beyond the CCW; I spent the time on Part B. I did not re-read the IETF Datatracker pages.

## Part B: what a bounded comparison could read

Classes: proposed vs published outcomes. Voluntary public reports with documented outcomes:

1. CISA Cyber Storm IX AAR (Sept 2024; exercise April 2024; 2,000+ participants per search result): 8 numbered findings and consolidated recommendations, TLP:CLEAR. Earlier editions public (2016, 2020 report Jan 2021, VIII Aug 2022 file), so a series exists. Detail: qualitative findings, recommendations; I did not check for per-finding measures. New.
2. SIFMA Quantum Dawn VII public AAR (1 May 2024; exercise 14 to 16 Nov 2023): participant-reported percentages (75%, 98%, 80% above), third-party outage scenario, participants unnamed. Self-report, poll-based; plans stated rather than recovery demonstrated. New.
3. ENISA Cyber Europe AARs (2014, 2018, 2022, 2024; 2024 published 10 Dec 2024, about 5,000 participants): a long public series; headline claims reported by ENISA (snippet): reporting collaboration good, limits in showing cross-border impact. Needs a way to read it that respects robots (the driver may ask the keeper). Cyber Europe 2026 report not out. Not opened.
4. Bank of England SIMEX 24 (2 Oct 2024) and SWES final report (29 Nov 2024): SIMEX publishes no outcomes on the page read (a useful "assurance only" case); SWES is a stress-scenario report with about 50 firms and six conclusions (not read). SIMEX 22 (Nov 2022) also mentioned. Possibly other summary text exists that I did not find.
5. NATO CCDCOE Locked Shields 2026 (ended 24 April 2026, 41 nations reported): results are scoring and press, a technical defence exercise; I found no primary lessons report. Weak fit for cross-organisation recovery measures.

Possible bounded comparison (suggestion only): for each series, table what is reported (counts, rates, times to restore, named unresolved gaps, recommendations, follow-up on earlier recommendations) against what is assurance. Sparse in my reading: none of the PDFs I read gave measured time to restore services; Quantum Dawn gives plan coverage self-reports. I did not check whether Cyber Storm reports follow up prior recommendations. Limits: two PDFs read by text extraction, headline only. No dependency maps or operator names recorded.

## Five best leads

1. CCW Seventh Review Conference final text: find the decision and final report (primary, UN). APILS reports mandate "to elaborate, by consensus, an instrument". Matters for LH050 and the policy picture. Source blog is new against 20 November sweep (no earlier APILS file).
2. CISA Cyber Storm IX AAR, https://cisa.gov/sites/default/files/2024-10/Cyber%20Storm%20IX%20After-Action%20Report%20v00%2020241001_508.pdf: best Part B primary source, a series. New.
3. SIFMA Quantum Dawn VII public AAR, https://www.sifma.org/wp-content/uploads/2024/04/SIFMA-Quantum-Dawn-VII_Public-AAR-FINAL.pdf: measures (self-reported). New.
4. ENISA Cyber Europe AAR series: https://www.enisa.europa.eu/publications/cyber-europe-2024-after-action-report (robots-refused to Anthropic's agents; needs keeper decision on access, or a secondary route). Not opened. New.
5. Bank of England SIMEX 24 and SWES: https://www.bankofengland.co.uk/news/2024/october/simex-24-testing-the-uk-financial-sector-resilience ; counter-example of no published outcomes plus SWES final report. New.

## Withheld under research safety

No items withheld.

## Limits

Search is US-only and date-fuzzy; WebFetch summaries drop detail; one-source claim on the CCW outcome; Part A coverage beyond the CCW was thin this run.
