# Scout 7, Wildcard: horizon sweep 2026-11-18T1300Z

**In short.** I looked at what the other scouts might miss between 17 November 14:20 UTC and 18 November 13:07 UTC. Hacker News had three things. A newspaper's anonymous sources say patches for AI-found flaws are causing the recent outages, though nobody quoted on the record says so. Quad9 says its free resolver stops serving France on 24 November because of a court penalty. And Codeberg's domain was suspended by its registrar for a few hours this morning. The robotics searches found no new November armed-robot item. The biggest gap was older: rights groups, UNICEF and a Gaza journalist report crane-mounted, remotely operated machine guns firing on civilians in Gaza since June 2026, and nothing in Lighthouse's records mentions them.

Question: what would Lighthouse regret not having watched?

- Start: 2026-11-18T13:02:51Z. End: 2026-11-18T13:09Z (UTC, from `date -u`).
- Everything below is **reported by** the page named. None of it is a Lighthouse observation. Shell fetches carry the second they started. WebFetch reads fall between two timed shell calls, so their times are given as "about". WebFetch returns a small model's summary, so its quotations are as the summariser relayed them.
- Every URL went through `scripts/robots_gate.py` (provider anthropic) before it was fetched.
- "New?" means the URL was not found in notes/horizon/ (earlier sweeps and today's six other scout logs as they stood at 13:07), in proposals.md or in studies/LH050.
- Saved bodies: HN JSON, the NANOG listing and threads, the Mastodon error bodies and the Codeberg status JSON are under /tmp/claude-0/-home-user-lighthouse/77ce94cc-96f2-57d9-a33d-ffc9870568e6/scratchpad/s7/ only. `python3 -I scripts/redact_emails.py` ran over that directory after each save. Nothing was saved in the repository.

**Direct publication checks.** None assigned to this scout.

**Language and geography limits.** I searched in English, German, French, Ukrainian, Russian, Chinese (simplified), Arabic, Japanese, Turkish, Persian and Spanish. Every search went through one US-indexed tool that answers with a model's summary in the query's language. I opened pages in English, Ukrainian and German, and nothing in Chinese, Arabic, Japanese, Turkish, Persian, French or Spanish. Two Arabic leads (eremnews) are disallowed by robots.txt. The geography covered is Ukraine, Gaza and Israel, Germany, France, the US and, via search summaries only, Iran, Turkey and China. I covered nothing from Africa, South or Southeast Asia or Latin America beyond search summaries that found nothing dated November. The Gaza crane reports form one source family: The New Arab, Novara (which cites The New Arab), PCHR, UNICEF and one journalist's posts on X. A language with no November item means only that this search found none.

## Standing sources read

1. HN Algolia API: stories created after 2026-11-17T14:20:00Z (epoch 1794925200) with more than 40 points. 57 hits (row 1).
2. NANOG archive, latest threads (row 7). No new thread since yesterday's read. The Ethiopia BGP, cms.ups.com and DAZN threads were already seen on 13 November. The "Microsoft post-op" and FAA/NWS threads show no reply newer than yesterday's read (row 8).
3. Mastodon, infosec.exchange public tag timelines for `aiscrapers`, `infosec` and `outage`. All three refused: HTTP 422, "This method requires an authenticated user" (row 9). I tried no other instance.

## Searches

1. `Codeberg domain disappeared NameSilo November 2026`: social.kernel.org, infinityfree forum (an older NameSilo vanishing), openwrt forum, lowendtalk ×2, namepros, activitypub.space (Codeberg's account). Nothing dated except the account. Answered from rows 4, 5 and 10 instead.
2. `AI-found vulnerabilities patches causing outages banks NSA Congress November 2026`: cryptobriefing (Garbarino, Mythos), pymnts ×3, scworld, thenextweb (9 May), finance.yahoo (Bessent and bank CEOs), cybernews (Gold Eagle), ifp.org (Operation Patchlight PDF), eenews ("AI is overwhelming their response"), thehill (NSA PHP warning), advisorperspectives (Bloomberg, 10 Nov, "fears ai cyber apocalypse bit premature"), webpronews. The summary found no confirmed November report of AI-driven patches causing outages.
3. `наземний роботизований комплекс листопад 2026 автономний`: censor.net (MoD: 50 UGVs admitted in 2026), armyinform (Jul), dou.ua digests #52, #54, #55 and #56 (#56 seen yesterday), mod.gov.ua DOT-Chain, kyivpost uk/post/78062 and 74577, texty, 24tv, theins.ru, forbes.ua. Nothing new from November.
4. `机器狼 无人战车 2026年11月`: 163.com, militaeraktuell.at (seen 13 Nov), eweek, TVB, finance.sina (4 Jun), huanqiu (an Airshow China "robot wolf pack" piece dated 10 November with no year, so probably 2024), FDD memo (Apr). Nothing from November 2026.
5. `"Дайджест НРК #57"`: nothing. Issue #57 is not indexed.
6. `روبوتات مفخخة غزة المدنيين 2026`: eremnews i9kjp0q and rlow4fg (2026 testimonies of explosive-laden robots in Shuja'iyya and al-Tuffah; disallowed), ajnet and aljazeera (12 Oct 2024), novaramedia (row 12), newarab (row 11), truthout, asianews, palestine-studies (7 Jul 2026), yahoo. Euro-Med is quoted in the summary for at least 60 civilians killed by quadcopter fire or munitions between the October 2025 ceasefire and early September 2026 (not opened).
7. `наземный робот мирные жители удар ноябрь 2026`: thepage.ua (seen 13 Nov), armyinform (2025), kyivpost uk/post/89169 and 89376 (row 13), www1.ru (Aug, a Russian drone destroying a UGV), militarytimes (8 May), liga, euromaidanpress ×3, forcesnews, verstka, trenchart. No report of a ground robot harming civilians.
8. `armed robot deployment halted OR scrapped OR withdrawn November 2026`: Amazon Blue Jay (Feb, unarmed), the US Army drone battalion ending (Aug: techradar, militarytimes, defensenews, AA), the UK dropping a Watchkeeper transfer (united24), Ukraine halting HX-2 orders (defence-blog), aiweekly (seen). No armed-robot withdrawal in November.
9. `Phantasialand Chlor Sauna E-Mail Alarm Microsoft Störung Ermittlungen`: infranken (dpa, row 14), tageskarte, drweb, betanews, it-daily, notebookcheck, ms-aktuell, leinetal24, apfeltalk, iflscience, android.com.pl, zeli.app. No authority's investigation named.
10. `Quad9 France retrait résolveur DNS décision tribunal Canal+ novembre 2026`: it-connect.fr and .tech, torrentfreak, next.ink ×3, korben ×3, universfreebox, kulturegeek, cyberinsider, reclaimthenet, clubic. As summarised: a judgment of 21 October 2026 from the Paris judicial court on beIN Sports' application set a penalty of €1,000 a day, following a 13 May blocking order. Quad9 is appealing.
11. `AIエージェント 暴走 障害 事故 2026年11月`: st-hakky, newsbytes, businessinsider.jp (OpenAI agent on a US government site, Sep), aibusiness, digitaltrends (Axios: "tens of thousands" of incidents; disallowed), impress, forbesjapan. Nothing from November. This is scout 1's beat, and L-0085 already holds the evaluation breakouts.
12. `silahlı insansız kara aracı teslimat Kasım 2026`: tr.euronews (30 Oct: ARX Robotics and Roboneers armed robot, first deliveries by the end of 2026), cnnturk (ASELSAN and Katmerciler "mini tank", undated), benguturk (disallowed yesterday), armyinform en (66,000 missions, Aug), mod.gov.ua en. The summary relays the MoD's October figure as 31,398 missions.
13. `ربات جنگی مسلح زمینی رونمایی آبان ۱۴۰۵`: oecd.ai (Iran's "Arya", Sep 2025), ecoiran, hamshahri, radiofarda, intellinews. Nothing from Aban 1405 (October to November 2026).
14. `robot policial patrulla retirado OR suspendido OR polémica noviembre 2026`: elobservador, crhoy and acento (NYPD K5, 2024), WOSU (DubBot, 17 Jun 2026), zamin.uz, foxnews. Nothing from November. These are the US withdrawals already logged.

## Pages opened

| # | URL | Page date | Read (UTC) | Status | New? | Claim reported by the page |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | https://hn.algolia.com/api/v1/search_by_date?tags=story&hitsPerPage=200&numericFilters=created_at_i%3E1794925200,points%3E40 | n/a | 13:03:16 (a first call at 13:03:11 with hitsPerPage=300 got HTTP 400) | 200 | new (query window) | 57 stories. Beyond other scouts' beats, the relevant ones: "Bank CEOs, NSA Tell Congress That AI-Driven Patches Are Behind Outages" (84 points); "Quad9's withdrawal from France" (709); "Highly classified US national security communications network goes down" (CNN, 614, and Reuters, 334); "Apple Services Down" (698); "Codeberg.org Not Reachable" (235) and "Codeberg seems to have vanished from DNS" (50); "Google's AI answers reducing search traffic by 40%" (revscope, 497); "AI is killing All About Berlin" (471); "Archive Team is archiving the Apple Support Community" (218); "California bans Waymo autonomous vehicles from state freeways" (AP, 61); "Microsoft's ONNX Runtime has disappeared from GitHub" (364, left to scout 3); "Java4Shell" (1,012, left to scout 2); Charles Schwab website down (55). |
| 2 | https://www.washingtonsun.com/technology/bank-ceos-nsa-tell-congress-ai-driven-patches-behind-outages | 2026-11-17 19:45 | about 13:03:45 | fetched | new URL (scout 6 reached the host today through a redirect) | Jeff Stein. As relayed: the claim rests on "private conversations" with three unnamed sources and a "congressional official briefed on the matter": "These models are identifying massive vulnerabilities, and that increases the urgency to patch right away", with more patches at once "than the system was designed to handle". The outages named are the FAA ground stop, JPMorgan Chase, the NSA's classified network and Microsoft Outlook. On record, JPMorgan blamed software bugs, the NSA "scheduled routine maintenance" and Microsoft a technical defect, and none links AI. No hearing, committee or transcript is named. |
| 3 | https://blog.cloudflare.com/quad9-withdrawal-from-france/ | 2026-11-17 (metadata) | about 13:03:45 | fetched | new | No author named. As relayed: after a French court imposed daily penalties for not blocking domains, Quad9 will withdraw its resolver from France. Removal could leave "hospitals, schools, and government bodies" with failing connections. A Belgian court has ordered Cloudflare, Google and Cisco to block through their resolvers by early January 2027, and they have appealed. The post includes no measurement of its own. |
| 4 | https://social.anoxinon.de/@codebergstatus/117636437840688845 | n/a | about 13:03:50 | fetched (truncated preview) | new | Only the opening was visible: "As you probably noticed, our domain codeberg.org …". Read in full at row 5. |
| 5 | https://social.anoxinon.de/api/v1/statuses/117636437840688845 | 2026-11-18T08:13:11Z | 13:03:59 | 200 | new | Codeberg's status account: "our domain codeberg.org is entirely unreachable. It was registered with namesilo and entirely disappeared from our account … No, we didn't forget to renew. There are no suspicious logins". |
| 6 | https://nicolasbouliane.com/blog/death-by-ai | 2026-05-26 | about 13:03:45 | fetched | new | As relayed: All About Berlin "has lost 70% 75% of its traffic to Google AI Overviews" after seven years of growth. No analytics tool or period is given, only a chart. The post is from May and resurfaced on HN today. |
| 7 | https://lists.nanog.org/archives/list/nanog@…/latest | threads to 17 Nov | 13:04:08 | 200 | seen (path) | Ten threads. Only "NANOG 99 early rates" and "BGP Insight in ARIN Online" were not seen before. Neither concerns AI or an incident. |
| 8 | NANOG threads 5P2RX22MB4437GD6L7TOW5IVGK6FOA66 ("Microsoft post-op") and HCONUTDYINCL53QSCVP4HXM2S2HVVTYI (FAA/NWS) | 17 and 13 Nov | 13:04:24 | 200, 200 | seen | The pages show "last active" one day ago for the Microsoft thread, with 9 participants, and the FAA thread has 19 participants. I found no reply newer than yesterday's read and read no new message bodies. |
| 9 | https://infosec.exchange/api/v1/timelines/tag/{aiscrapers,infosec,outage}?limit=40 | n/a | 13:04:40 to 13:04:41 | 422 ×3 | n/a | "This method requires an authenticated user". A wall, recorded. I did not get around it. |
| 10 | https://hn.algolia.com/api/v1/items/50544261 | 18 Nov 10:02 onwards | 13:06:58 | 200 | new | 228 comments. The top comment quotes Codeberg's update: "We have received the confirmation that our domain was suspended and our case got forwarded to the abuse team. We're still waiting for a final decision." Commenters say "And its back" (11:28Z) and "It's back up" (12:28Z). These are commenters' claims. I did not check them, and I did not query codeberg.org. |
| 11 | https://www.newarab.com/news/civilians-gaza-under-fire-israels-killer-cranes | 2026-06-19 (updated 16 Jul) | about 13:05:40 | fetched | new | Matthew Hoare. As relayed: PCHR says "23 military cranes equipped with machine guns and cameras" are at 23 locations behind the "yellow line", and "some" are operated remotely. UNICEF said a 12-year-old girl was "shot in the chest from a crane-mounted gun while in her tent". The journalist Tamer Nahed says they "fire randomly and almost continuously". No Israeli military response is included. |
| 12 | https://novaramedia.com/2026/07/01/israel-installs-cranes-equipped-with-unmanned-machine-guns-to-kill-gazans/ | 2026-07-01 | about 13:05:40 | fetched | new | Joshua Carroll. As relayed: 23 cranes with "remotely-operated" machine guns, with no source given for the figure (it cites The New Arab). Nahed says they were installed around mid-June and that three people were killed in two days, one a five-year-old girl. Automatic or AI targeting is not mentioned. No Israeli army statement. Same family as row 11. |
| 13 | https://www.kyivpost.com/uk/post/89376 | 2026-11-06 18:23 | about 13:05:40 | fetched | new | Vladyslava Vynnykova, citing Ukraine's MoD Telegram: "понад 31 тисячу логістичних та евакуаційних місій" by ground robots in October, a monthly record (January: 7,511). "усі місії НРК зафіксували у бойовій системі DELTA", "верифікували фахівці Brave1". No combat or armed missions, autonomy or civilians are mentioned. |
| 14 | https://www.infranken.de/deutschland/15-verletzte-im-phantasialand-outlook-stoerung-als-ursache-art-6411397,PRINT | 2026-11-16 (dpa, Brühl) | about 13:06:30 | fetched | new | As relayed: the WDR account came "unter Berufung auf das Unternehmen". The claim that no emails arrived is attributed to the park. The fire brigade spoke only about the injured and the pool's closure. A dpa request to the park went "zunächst unbeantwortet". The incident was on Friday 13 November: one person was taken to hospital moderately injured and three lightly. No authority's investigation is named. |
| 15 | https://quad9.net/news/blog/ | index; post 2026-10-22 | about 13:06:30 | fetched | new | The post "Farewell, France" (22 Oct 2026, /news/blog/au-revoir-france/) says Quad9 "will no longer be able to offer its free cyberprotection service to users located in France effective November 24". The excerpt does not say how location is determined. The post itself was not opened. Also listed: "Analysis of Outage 8 May 2026". |

Pages opened: 15 rows, 20 requests counting the three Mastodon calls, the two NANOG threads and the first HN call.

## Refusals and walls

- www.cnn.com (national security network outage): disallowed by robots.txt, not fetched.
- www.reuters.com (the same story): disallowed, not fetched.
- apnews.com (Waymo freeway ban): disallowed, not fetched.
- www.digitaltrends.com (Axios "tens of thousands" of incidents): disallowed, not fetched.
- www.eremnews.com, two pages (2026 Gaza testimonies on explosive-laden robots): disallowed, not fetched.
- infosec.exchange tag timelines: HTTP 422, authentication required, ×3. Not retried, and no other instance tried.
- HN Algolia: HTTP 400 on hitsPerPage=300 (my malformed request, not a wall). It worked at 200.
- I did not query codeberg.org itself. LH044's record says codeberg.org's robots.txt disallows `/` to ClaudeBot.

## Search results not opened

The tageskarte, drweb, betanews and notebookcheck Phantasialand reports (dpa family); torrentfreak, it-connect, next.ink and korben on Quad9; revscope.co (AI answers cutting search traffic 40%); wiki.archiveteam.org Apple_Discussions; the AP Waymo story (disallowed); the eenews, ifp.org Patchlight PDF, advisorperspectives and finance.yahoo pieces on AI-found flaws and banks; tr.euronews on ARX Robotics and Roboneers; censor.net (50 UGVs admitted); Euro-Med on Gaza quadcopter deaths; the UNICEF statement itself; palestine-studies; huanqiu's robot-wolf piece. None of these were opened.

## Quiet

- No new NANOG thread in the window, and none on AI traffic.
- No armed-robot item dated November 2026 in Ukrainian, Russian, Chinese, Turkish, Persian, Arabic or Spanish searches. No November withdrawal or failed deployment of an armed system. No report of a ground robot harming civilians in Ukraine or Russia.
- No authority's investigation of the Phantasialand incident appeared in the German results.
- No on-record official links AI to the recent US outages in anything read.

## Five best new leads

### 1. "AI-driven patches are behind outages": anonymous sources link AI vulnerability discovery to the November outages

- **Primary URL.** https://www.washingtonsun.com/technology/bank-ceos-nsa-tell-congress-ai-driven-patches-behind-outages (17 Nov 2026). Related, not opened: CNN and Reuters on the NSA's classified network going down on 17 November (both disallowed).
- **What was reported.** Unnamed sources and a congressional official say patching driven by model-found flaws has outrun what systems were "designed to handle", behind the FAA, JPMorgan, NSA network and Microsoft outages. Every on-record statement quoted gives a non-AI cause.
- **Why it matters.** It is the charter's question in its indirect form. AI activity could degrade shared infrastructure through the defenders' patching load rather than through attacks. It is also the first time the claim has been tied to named outages. As sourced, it is a claim to track, not evidence.
- **Feeds.** The AI cost investigation (load kept apart from spread), P-0033 and LH036's model-found-bug thread, and the Microsoft outage report watch: Microsoft's final review is the one primary source that could confirm or contradict the claim for one outage.
- **Window.** Days to weeks. A hearing, testimony or letter would be the first on-record version, and its date matters. The NSA network outage is from 17 November.
- **Next step.** Scout 6 or the policy beat should look on each sweep for on-record congressional testimony naming AI-driven patch volume. When Microsoft's final review appears, note whether it mentions the fix's origin.

### 2. Quad9 stops serving France on 24 November: a shared public resolver withdrawn by court penalty

- **Primary URL.** https://quad9.net/news/blog/au-revoir-france/ (22 Oct 2026; index read today, post not opened). Commentary: https://blog.cloudflare.com/quad9-withdrawal-from-france/ (17 Nov).
- **What was reported.** Following a Paris judgment of 21 October on beIN Sports' application, with a penalty of €1,000 a day as summarised, Quad9 will cut off users "located in France" from 24 November. OpenDNS left France in 2024, and a Belgian order on Cloudflare, Google and Cisco takes effect in early January 2027.
- **Why it matters.** It is a dated, announced withdrawal of a free shared service, the closing-web pattern but driven by law, not by AI load. Lighthouse's account of what degrades shared infrastructure needs its non-AI comparators. A known date allows a before-and-after read.
- **Feeds.** LH044's comparison class (not its panel), the AI cost investigation, and scout 4's infrastructure beat.
- **Window.** Fixed: 24 November. A before reading has to be taken before then.
- **Next step.** Scout 4 or the infrastructure beat should check on 25 November whether Cloudflare Radar or RIPE Labs publishes on the cut-off, and note how location is determined once the Quad9 post is read. Lighthouse should not probe Quad9's resolvers for this.

### 3. Remotely operated machine guns on cranes in Gaza, reported firing on civilians since June 2026

- **Primary URL.** https://www.newarab.com/news/civilians-gaza-under-fire-israels-killer-cranes (19 Jun 2026, updated 16 Jul), citing PCHR and a UNICEF statement. Same family: https://novaramedia.com/2026/07/01/israel-installs-cranes-equipped-with-unmanned-machine-guns-to-kill-gazans/.
- **What was reported.** 23 cranes with machine guns and cameras, some operated remotely, at positions behind the yellow line. UNICEF reports a 12-year-old girl shot in her tent. A Gaza journalist reports three deaths in two days. AI or automatic targeting is not mentioned, and no Israeli statement is included.
- **Why it matters.** This is a reported civilian experience of delegated, remote armed force in the same place as LH050's proposed Foundation/Phantom Gaza application, and it is the kind of report the scout's brief asks for and that LH050's civilian-consequence column lacks. Nothing in Lighthouse's records mentions it. It is not a robot in the core sense and no AI function is reported, so it is a lead and a comparator, not a case.
- **Feeds.** LH050's context only. Admitting it would need a dated amendment, and the keeper's lane rules apply to any new case.
- **Window.** Not urgent. The reports are four to five months old. The UNICEF statement and PCHR's documentation are the primary sources to read. The eremnews testimonies on explosive-laden robots are disallowed.
- **Next step.** File it as a lead for LH050 with the UNICEF statement and PCHR's report as the primary sources to read, and with human control and the operating force marked not established.

### 4. Codeberg's domain suspended by its registrar for some hours on 18 November

- **Primary URL.** https://social.anoxinon.de/@codebergstatus/117636437840688845 (08:13Z, 18 Nov). Update quoted on HN thread 50544261.
- **What was reported.** codeberg.org vanished from the registrar account. The registrar confirmed a suspension and forwarded the case to its abuse team. HN commenters say it was back by about 11:28 to 12:28Z.
- **Why it matters.** A shared code commons, one of LH044's named services (F06), was made unreachable by a single intermediary's abuse process, a closure with no AI and no robots.txt involved. If the suspension came from automated abuse reports, it is a case of automation turning on shared infrastructure. Nothing read says so, and that should not be assumed.
- **Feeds.** LH044, as context for how a "closing" can arise. LH044's read 2 is on 22 November, so no read fell inside the outage.
- **Window.** Hours to days. Codeberg's and the registrar's explanation of the cause will appear soon and may be edited. codeberg.org's robots.txt closes it to our tokens, so the Mastodon account is the readable route.
- **Next step.** Read the codebergstatus account's next posts at the next sweep, for the stated reason for the suspension.

### 5. Ukraine's October count: over 31,000 ground-robot missions, logistics and evacuation only

- **Primary URL.** https://www.kyivpost.com/uk/post/89376 (6 Nov 2026), citing the MoD's Telegram post (not opened). Related: tr.euronews (30 Oct) on ARX Robotics and Roboneers armed-robot deliveries by the end of 2026 (not opened). Yesterday's dou.ua digest #56 reported the first autonomous combat-route mission.
- **What was reported.** More than 31,000 missions in October (about 31,398 as one summary relays it), recorded in DELTA and verified by Brave1, against 7,511 in January. The figure counts logistics and evacuation, not armed use.
- **Why it matters.** LH050 keeps a ministry series of mission counts beside its matrix. This October figure is not in its records. The armed-robot deliveries promised for year end are the claim to watch, and nothing armed is in this count.
- **Feeds.** LH050's ukraine-ugv-series (its December read). It is not an extra-read trigger, because it is a count, not a new claim about armament, authorisation or use.
- **Window.** Low. The MoD posts monthly, and the series' own December read will reach it.
- **Next step.** Hand it to LH050's December series read as the October notice to retain from the ministry's own page.

## Notes

- Update to L-0112 (Phantasialand): the dpa report (row 14) attributes the email-loss account to the park via WDR. The fire brigade did not speak to the cause, and the park had not answered dpa. infranken.de is a readable route past WDR's robots.txt wall. Still not an AI event.
- Also seen, outside the five: AI answers cutting publishers' traffic (revscope's 40% claim, not opened; All About Berlin's 70 to 75% from May, row 6), which belongs with LH044 and scout 1. Archive Team is archiving the Apple Support Community (not opened), possibly a closing. California has banned Waymo from freeways (AP, disallowed), which is physical authority but unarmed.
- The search tool again returned almost nothing dated November 2026 in non-English languages. That may be the tool, and it is not a finding.
- Rules: 14 searches and 15 page rows. Every fetch was gated first, and no disallowed URL was fetched. The Mastodon 422 was not worked around. Saved bodies are only in the scratchpad and were redacted. No email address is written here: NANOG's list address in a URL is shortened to "nanog@…" as in yesterday's log, which I took to be the same practice. I did not commit or edit any other file.
