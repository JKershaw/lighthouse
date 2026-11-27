# Scout 6, Policy and institutions, run 2026-11-27T1212Z

**In short.** The standing policy sources are now checked (the gap of 24 November). The IETF's two working groups on automated traffic are still at draft stage: the AI preferences vocabulary draft is at revision 08 (14 September 2026) and the Web Bot Auth protocol draft at revision 01 (29 October 2026), both still "WG Document" with no IESG state, well past their charter milestones. Four publishers' suits against Brave over a crawler that reportedly neither identifies itself nor follows robots.txt (2 November) are new, and Google v. SerpApi was dismissed again with leave to refile. For physical authority, the ICRC page lists four November statements, the CCW outcome is described as a mandate to elaborate an instrument rather than negotiate, and the UN Security Council held a debate on 24 November; all are proposals or statements, not adopted rules, and no implementation evidence was found. The CCW final document was not fetched (LH050 reads it today).

Start 12:14 UTC, end 12:16 UTC (clock as read by `date -u`; the read times below are approximate and fall in that window), 27 November 2026 (`date -u`). Sonnet-class scout. Tools: WebFetch (a summariser, so quotations are as relayed), WebSearch, scripts/robots_gate.py (provider anthropic, strict mode) before each fetch, grep of notes/horizon. No keys read, harbour/.session/ untouched, nothing committed, no bodies saved.

## Direct publication checks

| Endpoint | UTC read | Interval | Outcome |
|---|---|---|---|
| none named for Scout 6 in plan.md | n/a | n/a | not applicable; standing pages read instead (below) |

## Standing-source results

| Source | Result (reported by the page, via summariser) |
|---|---|
| IETF aipref, https://datatracker.ietf.org/wg/aipref/about/ and draft-ietf-aipref-vocab | WG active; charter milestones (vocab and attach drafts to IESG) were due August 2026. Vocab draft is -08, dated 14 September 2026, "WG Document", IESG state "I-D Exists", no AD, shepherd or telechat. Not past last call on the page read. |
| IETF webbotauth, https://datatracker.ietf.org/wg/webbotauth/about/ and draft-ietf-webbotauth-httpsig-protocol | WG active; milestones due 30 April and 31 August 2026. Protocol draft -01, dated 29 October 2026, "WG Document", IESG "I-D Exists". Search snippet (not opened) says IETF 126 minutes mention a session at IETF 127 and that the WG had no adopted documents as of August. |
| NIST CAISI, https://www.nist.gov/caisi | One November item: 24 November 2026, call for public comment on draft NIST SP 2400-801 "Practices for Evaluating SI-Driven Uplift", comments to 22 February 2027. No agent-specific November item; page also names an "SI Agent Standards Initiative" without detail. Draft not opened. |
| UK AI Security Institute, https://www.aisi.gov.uk/blog | One November post: "Attack policy selection can make monitor evaluations misleading" (23 November 2026). Not opened. |
| EU AI Office, https://digital-strategy.ec.europa.eu/en/policies/ai-office | Gate allowed; page not opened. Search (secondary sources only) found no November AI Office agents publication; background: Digital Omnibus on AI described as in force 27 July 2026, and a transparency guideline said to require agents to disclose they are AI and for whom (dated about 118 days before, unverified). |
| Courts and enforcement | See searches 2 and 6 below. |
| UNIDIR, https://www.unidir.org/ ; SIPRI emerging technologies page | Gates allowed; not opened for lack of time. SIPRI items met only through search (below). |
| ICRC, https://www.icrc.org/en/law-and-policy/autonomous-weapons | Opened; see pages table. |

## Searches

1. IETF aipref OR web bot auth last call November 2026: results mostly secondary blogs with conflicting dates; no last call found. Not opened: WorkOS, natielimelech, nerdleveltech, llm4agents, info.link, minutes-126-webbotauth, charter pages.
2. Court ruling AI crawler robots.txt lawsuit November 2026: Brave suits (2 November), Google v. SerpApi, Ziff Davis v. OpenAI (2025 ruling that robots.txt is not a DMCA access control, per a summary), Meta terms delay to 20 November, a Google robots.txt change around 22 November. Opened only Plagiarism Today. Not opened: Lexology, Pearl Cohen, saascity, crawlpilot, lawfold, ppc.land Google Maps item, Fiund, Courthouse News PDF. One snippet mentions a San Francisco "AI freeze" suit of 12 November from a single thin source: unverified.
3. EU AI Office GPAI code of practice agents guidance: secondary law-firm roundups only; nothing opened.
4. Autonomous weapons directive procurement SIPRI UNIDIR ICRC: no November items; SIPRI "Responsible Procurement of Military Artificial Intelligence" (February 2026), SIPRI at the CCW GGE (March 2026), UNIDIR 2025 IHL report. None opened.
5. Security Council open debate 24 November: ICRC statement, UN News live page (news.un.org/en/story/2026/11/1168866), a Microsoft remark on time from flaw to attack (dailyaibrief), Wisevoter, archyde, a Yahoo piece on Russia allegedly using Nvidia hardware in a drone that killed civilians in Ukraine. Not opened (none gated or fetched): all of these except as summarised by the search tool.
6. Google v. SerpApi: law-firm and trade write-ups give 9 or 10 November for the dismissal with 21 days to refile (about 30 November per PPC Land's own count). Court order not found. Not opened.

## Pages opened

| URL | UTC read | Gate | Status | Page's date | Reported claim |
|---|---|---|---|---|---|
| https://datatracker.ietf.org/wg/aipref/about/ | ~12:15 | allowed | ok (summariser) | undated | Reported by the Datatracker: charter covers a vocabulary and attachment methods; out of scope "technical enforcement of preferences, client and crawler authentication". |
| https://datatracker.ietf.org/wg/webbotauth/about/ | ~12:15 | allowed | ok (summariser) | undated | Reported by the Datatracker: WG will "standardize ways to cryptographically authenticate automated clients"; milestones 30 April and 31 August 2026. |
| https://datatracker.ietf.org/doc/draft-ietf-aipref-vocab/ | ~12:15 | allowed | ok (summariser) | 14 Sep 2026 | Reported by the Datatracker: revision -08, "WG Document", IESG "I-D Exists". |
| https://datatracker.ietf.org/doc/draft-ietf-webbotauth-httpsig-protocol/ | ~12:15 | allowed | ok (summariser; last 2,513 characters unread) | 29 Oct 2026 | Reported by the Datatracker: revision -01, "WG Document", IESG "I-D Exists". |
| https://www.nist.gov/caisi | ~12:15 | allowed | ok (summariser) | 24 Nov 2026 item | Reported by NIST: comment period on SP 2400-801 to 22 February 2027. |
| https://www.aisi.gov.uk/blog | ~12:15 | allowed | ok (summariser) | 23 Nov 2026 item | Reported by AISI: post title only. |
| https://www.plagiarismtoday.com/2026/11/03/what-the-brave-lawsuit-says-about-ai/ | ~12:15 | allowed | ok (summariser) | 3 Nov 2026 | Reported by the blog: four news publishers sued Brave in two suits; the suits say its crawler "does not respect robots.txt and does not identify itself"; court not named; Brave says it only indexes what Google can. |
| https://www.icrc.org/en/law-and-policy/autonomous-weapons | ~12:15 | allowed | ok (summariser) | 13, 18, 21, 24 Nov 2026 items | Reported by the ICRC: four statements; 21 November "renews its call for legally binding rules on autonomous weapons after negotiations failed to launch"; 24 November: "No weapon, technology or method of war should put the conduct of hostilities beyond the limits of human control." Headlines only on the page; statements themselves not opened. |

## Five best leads

1. Brave crawler suits (2 November, four publishers, two suits): https://www.plagiarismtoday.com/2026/11/03/what-the-brave-lawsuit-says-about-ai/ (secondary; find the complaints or the Reuters item). Reported by the blog: a crawler that neither identifies itself nor follows robots.txt, which sits directly on the evidence Lighthouse's robots work depends on. Touches the AI cost and spread investigation (rules for robots). New against earlier sweeps (grep found no Brave suit entries beyond older mentions; treat as new).
2. IETF aipref and webbotauth drafts at stage "WG Document", past charter milestones: https://datatracker.ietf.org/doc/draft-ietf-webbotauth-httpsig-protocol/ and https://datatracker.ietf.org/doc/draft-ietf-aipref-vocab/. Whether agents can be identified and preferences expressed in a standard way is open; a watch on revisions and the IETF 127 outcome could be cheap. Touches the AI cost and spread investigation. Datatracker URLs are new in this form (earlier sweeps mention aipref; not these doc pages).
3. Google v. SerpApi, dismissed again around 9 or 10 November with leave to refile by about 30 November: https://ppc.land/google-faces-21-day-deadline-to-save-its-dmca-case-against-serpapi/ (not opened; secondary). The refiling or dismissal with prejudice will be an enforcement datum on anti-scraping measures as access controls. Not tied to a study; new.
4. ICRC statements of 18, 21 and 24 November and the Security Council debate: https://www.icrc.org/en/law-and-policy/autonomous-weapons and https://news.un.org/en/story/2026/11/1168866 (not opened). Proposals and positions, not adopted rules; the 24 November debate adds states' and the Secretary-General's positions (per search summaries, unverified). Touches LH050 and the physical-authority investigation as context for the CCW outcome.
5. NIST CAISI draft SP 2400-801, comment to 22 February 2027, and SIPRI's "Responsible Procurement of Military Artificial Intelligence" (February 2026): https://www.nist.gov/caisi and https://www.sipri.org/sites/default/files/2026-02/0226_milai_procurement.pdf (neither draft nor report opened). One is a proposal on evaluating AI capability uplift; the other a source on where weapons legal obligations are applied (procurement). Lower priority; the SIPRI report is a lead to original procurement texts for physical authority.

## Gaps and refusals

- No refusals this run. No wall met.
- CCW final document not fetched (LH050-policy-final reads it today).
- UNIDIR, SIPRI and EU AI Office pages gated but not opened; ICRC statements and the UN Security Council record not opened; court documents for Brave and SerpApi not found.
- No revised Directive 3000.09, armed-robot procurement, suspension, investigation or civilian-consequence item found this run; two searches only, so weak.
- All search results are from a summarising search tool, US-centred; absence means little.
