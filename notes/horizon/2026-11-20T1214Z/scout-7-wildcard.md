# Scout 7, Wildcard: horizon sweep 2026-11-20T1214Z

**In short.** I looked for what the other scouts might miss between 18 November 13:07 UTC and 20 November 12:26 UTC. The claim that patching for AI-found flaws lies behind the November outages has moved partly on the record: at a House hearing on 18 November the Director of National Intelligence said the rate of patching is rising, without mentioning AI, while two Democratic lawmakers tied it to AI-driven discovery, and the FAA has named a single router flooding its network as the cause of its ground stop. A Maryland lawsuit filed on 17 November says an AI gun detector mistook a bag of crisps for a firearm and armed police handcuffed students anyway, which is the clearest civilian experience of AI-triggered force found this sweep. No new armed-robot item dated November 2026 turned up in any of the nine languages searched, and Ukraine has published no November count yet.

Question: what would Lighthouse regret not having watched?

- Start: 2026-11-20T12:16:04Z. End: 2026-11-20T12:26Z (UTC, from `date -u`).
- Tools: shell `curl` (user agent `Lighthouse-research`) for the HN Algolia API, the Codeberg status account's Mastodon API, NANOG's archive and ioc.exchange; WebSearch (one US-indexed tool that answers with a model's summary); WebFetch (a small model's summary of the page, so its quotations are as the summariser relayed them).
- Everything below is **reported by** the page named. None of it is a Lighthouse observation. Shell fetches carry the second they started. WebFetch reads fall between two timed shell calls, so their times are given as "about".
- Every URL went through `LIGHTHOUSE_PROVIDER=anthropic python3 -I scripts/robots_gate.py` before it was fetched. Nothing it refused was fetched.
- "New?" means the URL was not found in notes/horizon/ (earlier sweeps and today's six other scout logs as they stood at about 12:22), proposals.md, studies/LH050 or studies/LH044.
- Saved bodies (HN JSON, Codeberg status JSON, NANOG listing and three threads, ioc.exchange error bodies) are only under /tmp/claude-0/-home-user-lighthouse/442ebca6-ae98-5331-869b-fad86ec7c59c/scratchpad/scout7/. `python3 -I scripts/redact_emails.py` ran over that directory after the saves and again at the end. Nothing was saved in the repository but this log.

**Direct publication checks.** None assigned to this scout.

## Standing sources read

1. HN Algolia API: stories created after 2026-11-18T13:07:00Z (epoch 1795007220) with more than 40 points. 122 hits (row 1).
2. Codeberg's status account (social.anoxinon.de), the readable route since codeberg.org and status.codeberg.org close themselves to our tokens (rows 2 and 3).
3. NANOG archive, latest threads (rows 4 and 5).
4. Mastodon: infosec.exchange refused tag timelines on 18 November, so I tried ioc.exchange's public tag timelines for `infosec`, `outage` and `aiscrapers`. All three refused with HTTP 422, "This method requires an authenticated user" (row 6). mastodon.social's tag timeline is disallowed by its robots.txt and was not fetched.

## Searches

Each line gives the query, its language, and what came back. Results were read from search summaries unless a row number points to a page opened.

1. `AI-driven patches outages Congress hearing testimony November 2026` (English): nextgov (row 7), cyberscoop (row 8), futurism, gizmodo, thenextweb, promptzone, theoutpost, forth.news, explainx, foxbusiness (Clayton: no sign of a cyberattack), saharareporters (senators' warning, 18 Nov), citizen.org (coalition asks DOJ and Congress to investigate). Two results describe a "December 17 hearing", which postdates today; misdated or unreliable, not opened.
2. `Codeberg NameSilo suspension reason abuse report explanation` (English): linuxiac (opened by scout 4 today), NameSilo's abuse procedures (72-hour response window, as summarised), phishdestroy (an advocacy group's dispute with NameSilo, no link to Codeberg found), 2025 items on far-right harassment of Codeberg. No stated cause.
3. `наземні роботизовані комплекси листопад 2026 місії Міноборони` (Ukrainian): thepage.ua, mod.gov.ua (June 16,600), censor.net (50 admitted), kmu.gov.ua (66,300), thepage.ua on robots with two AK rifles in combat trials (undated, not opened), kyivpost uk/post/89376 (seen 18 Nov), armyinform, militarnyi (25,000 to be contracted), dev.ua, mezha. Newest is October's 31,398. No November count.
4. `боевой наземный робот пулемёт применение ноябрь 2026` (Russian): gazeta.ru (Apr), theins, 24tv, theweek, sciencefocus, eweek (Kinburn spit, seen 17 Nov), yahoo (grenade-launcher robot, Mar), majalla, pulse.bot (six-week position defence, May). Nothing from November.
5. `무장 로봇 경계 비무장지대 2026년 11월` (Korean): korea.kr (a column reporting a first 43 billion won "physical AI" demonstration line in the 2027 defence budget for hazardous materials and garrison guard; not opened), koreancenter (Army TIGER+ demonstration, 14 Oct), koreatimes (row 10), thedefensepost (30 Oct, a lawmaker's AI and robot network proposal for the DMZ; not opened), gcsp, stripes (Jun), koreatimes (29 Jul, western border guarded without loaded ammunition). No armed robot and nothing from November.
6. `armed robot police deployment suspended OR scrapped OR failed November 2026` (English): San Francisco 2022 reversal, Knightscope withdrawals, DubBot (Jun, seen), fox5dc Montgomery County (row 9), 404media roboguard (seen 17 Nov), gujaratsamachar (DubBot). No armed police robot withdrawn in November.
7. `Montgomery County ends security robot pilot program surveillance concerns` (English): fox5dc (row 9), wtop (Jan 2026), mymcmedia, dronexl (13 Nov 2026, the county police drone director rebuked by the council; not opened), wdbj7 (a different Montgomery County dropping Flock cameras, 1 Oct). 
8. `机器狗 武装 部署 民众 2026年11月 报道` (Chinese, simplified; results came back in English): oodaloop, eweek and militaeraktuell (robot-dog "wolf packs", seen 13 Nov), techradar (China considering robot squads for armed and riot police; not opened). Nothing from November.
9. `רובוט חמוש עזה תושבים נובמבר 2026` (Hebrew): algemeiner and jdn.co.il (seen), novaramedia (seen 18 Nov), truthout (seen), aljazeera (Oct 2025), al-monitor (row 11), arabnews.pk, commondreams. No November armed-robot report.
10. `KI Crawler Last Server lahmgelegt Website Betreiber November 2026` (German): drweb (Gentoo Bugzilla offline from AI scrapers, 8 Aug 2026 per other summaries), it-daily (Triplegangers, older), kinsta, seahawkmedia, computerwoche, ifun.de (7 in 10 requests from AI bots; not opened). No dated November case.
11. `AIクローラー アクセス集中 サーバー停止 2026年11月` (Japanese): startuphub (university libraries, dated 18 Nov 2026 in the summary), getcoai, theregister (Dec 2025), rocket-boys.co.jp (Jan 2025 GPTBot case). No Japanese service outage found.
12. `robot armado policía militar América Latina África despliegue noviembre 2026` (Spanish): infobae (Apr: a US Southern Command autonomous warfare command for Latin America), keyt/CNN en Español (Sep: about 670 armed-drone events by organised crime since 2018, over 72% between January 2025 and August 2026), euronews (Mar: Chacao, Caracas, unarmed robot dogs), BBC via opovo (Jan: Colombia's AI-equipped attack drones). None opened; nothing from November; nothing on Africa.
13. `AI scrapers taking university library catalogues offline November 2026` (English): cp24 (17 Nov 2026, Canadian Press; disallowed), ctvnews (same; disallowed), cybernews (seen 10 Nov), aiweekly (Marmot consortium "2B AI-bot hits in 30 days", citing CBC; not opened), Duke library page, NYU Engelberg GLAM-E Lab (2025). Per the summary, CP24 reports the University of Victoria now blocks autonomous AI agents.
14. `Gentoo bugs.gentoo.org offline AI scrapers Górny 2026` (English): zeli.app, drweb, promptzone, labmemo. Bugzilla taken offline 8 August 2026, per aggregators citing a developer's Mastodon post. Older than this window; bugs.gentoo.org is already in LH044's read data.
15. `University of Victoria block autonomous AI agents university information systems announcement` (English): uvic.ca notice (row 13), uvic AI guidelines, Wharton, UVM, Birmingham, Toronto agentic AI guidance pages (not opened).
16. `"Дайджест НРК" #57 OR #58 dou.ua` (Ukrainian): no match. Issues #57 and later are not indexed.
17. `Ukraine ground robots November 2026 record missions armed combat robot first` (English): pravda.com.ua, ceskenoviny (Czech Ukrinform, the 31,398 figure), united24, kyivindependent, armyinform, mod.gov.ua, dronexl. October is still the newest month.
18. `AI 爬虫 网站 宕机 封禁 2026年11月` (Chinese, simplified): aitoolly (Anubis, May), technews.tw (Aug), theregister, 36kr. Nothing from November.
19. `pannes informatiques correctifs IA vulnérabilités novembre 2026 France` (French): next.ink 268124 (disallowed), it-connect (November Patch Tuesday: 1,093 flaws, after a record 1,407 in October, as summarised), cyber.gc.ca bulletin AV26-1142, esecurityplanet, ayinedjimi-consultants. None opened.
20. `Ausfälle Patches KI-gefundene Schwachstellen USA November 2026` (German): t3n, thestar.com.my (Reuters, 19 Nov; opened by scout 4 today), computerwoche, borncity and boerse-express (CISA now requires 72-hour patching of high-risk flaws by US agencies; not opened), bdnews24. None opened by me.
21. `روبوت قتالي أرضي مسلح نشر السودان OR اليمن OR ليبيا 2026` (Arabic): every result was about Ukraine or China. Nothing on Sudan, Yemen or Libya.
22. `सशस्त्र रोबोट सेना तैनाती सीमा नवंबर 2026` (Hindi): aajtak (Dec 2025, China's robot plans for the Vietnam border), arynews (Indian Army robots in Kashmir, undated), claws.co.in. Nothing from November.
23. `российский НРК "Курьер" OR "Депеша" штурм пулемёт ноябрь 2026` (Russian): espreso, criticalthreats, rg.ru (Mar), pravda.com.ua (Sep: Courier tests with machine guns), liga, kyivpost post/89428 and 89491 (row 14). No November assault by a Russian ground robot found.
24. `UK fridges secured from hackers secret nationwide operation NCSC November 2026` (English): retailgazette, theweek, lbc, computing, cityam, irishnews, therecord, newsbytes. Early-November coverage of the European refrigeration attacks (known since 10 Nov). The BBC item of 20 Nov that prompted the search is disallowed.
25. `AI 에이전트 장애 사고 서비스 중단 2026년 11월` (Korean): zdnet.co.kr (row 15), itworld.co.kr, cio.com Korean edition (simultaneous ChatGPT, Claude and Grok outage; date unclear), oecd.ai (Sep). 
26. `robôs de IA raspagem derrubam site bloqueio crawler Brasil novembro 2026` (Portuguese): fastcompanybrasil (row 16), outraspalavras on Wikifavelas (disallowed), tecnoblog, tabnews, correiobraziliense. Nothing from November.

## Pages opened

| # | URL | Page date | Read (UTC) | Status | New? | Claim reported by the page |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | https://hn.algolia.com/api/v1/search_by_date?tags=story&hitsPerPage=200&numericFilters=created_at_i%3E1795007220,points%3E40 | n/a | 12:16:25 | 200 | new (query window) | 122 stories. Beyond other scouts' beats: "Black high school students sue after AI mistakes Doritos bag for gun" (117 points, row 12); "Chrome AI features wasting much bandwidth" (130, row 17); "Court: 4th Amendment Disallows Use Of AI-Generated 'Probable Cause'" (techdirt, 65; left to scout 6); "UK fridges secured from hackers in secret nationwide operation" (BBC, 55; disallowed); "RegExr: Temporarily Offline" (82; disallowed, no cause known); "Visa, Mastercard and JPMorgan Customer Data Leaked by Hackers" (WSJ, 182; disallowed); "DNS resolvers are the wrong place to fight piracy" (Quad9, 680; seen 18 Nov); "Unauthenticated remote code execution in Nginx" (1,496) and "Java4Shell" items, left to scouts 2 and 4. |
| 2 | https://social.anoxinon.de/api/v1/accounts/lookup?acct=codebergstatus | n/a | 12:16:38 | 200 | n/a | Account id and 142 statuses. |
| 3 | https://social.anoxinon.de/api/v1/accounts/115651402898351746/statuses?limit=15 | to 2026-11-18T11:23:53Z | 12:16:50 | 200 | new (posts after 08:13Z) | Newest post, 11:23:53Z on 18 Nov: "The domain is slowly recovering … We haven't yet received an official response from Namesilo's abuse department about the incident." Nothing since, so no stated cause as of this read. 08:53Z: "our domain was suspended and our case got forwarded to the abuse team." 09:20Z: they did not switch to codeberg.eu; "activating a second domain is a long-term project". Earlier, 12 Nov 13:56Z: "We had to temporarily restrict pulling images from the Codeberg container registry due to an abuse wave" (marked resolved). |
| 4 | https://lists.nanog.org/archives/list/nanog@…/latest | threads to 19 Nov | 12:19:08 | 200 | seen (path) | Ten threads. Only "EA Games, Contact off List Please" is new since 18 Nov. |
| 5 | NANOG threads NH7NTDZNFVHBLMNW7C5KUJ6PGTBF7OG2, VXWTZ6LVR3FTNSFJ4HOU2TNDTYLWTGZJ, 5P2RX22MB4437GD6L7TOW5IVGK6FOA66 | 19, 16 and 17 Nov | 12:19:19 to 12:19:20 | 200 ×3 | first new; others seen | A small ISP says ranges used in a large apartment building "are blocked and affecting customers" and asks for an EA contact. No cause given. The Geoflaw thread (seen 17 Nov) has one reply. "Microsoft post-op" still shows 9 participants and last active three days ago. |
| 6 | https://ioc.exchange/api/v1/timelines/tag/{infosec,outage,aiscrapers}?limit=40 | n/a | 12:20:15 to 12:20:17 | 422 ×3 | n/a | "This method requires an authenticated user". A wall, recorded, not worked around. |
| 7 | https://www.nextgov.com/cybersecurity/2026/11/security-officials-tell-congress-tech-outages-are-not-malicious/417312/ | 2026-11-18 | about 12:17 to 12:18 | fetched | new | David DiMolfetta. House Homeland Security Committee, 18 Nov; witnesses Mullin, Clayton and Raia. Clayton: "We are in an environment where the rate of patching, the rate of upgrading of systems is increasing." No witness on record names AI; two unnamed people say most outages "appear to be linked to efforts to rapidly patch vulnerabilities with AI." |
| 8 | https://cyberscoop.com/?p=91641 | 2026-11-18 | about 12:17 to 12:18 | fetched | new URL (cyberscoop host seen 17 Nov) | Tim Starks, "Consensus mounts that tech outages were fueled by patching of AI-discovered vulnerabilities". Witnesses cited patching but "didn't specify that the patches were a result of AI unearthing vulnerabilities". Sen. Warner: AI discovery is "creating enormous pressure on companies and government agencies to patch those vulnerabilities immediately". Rep. Himes: increased discovery and patching "could cause more frequent outages". Witnesses saw no evidence of malicious attacks. |
| 9 | https://www.fox5dc.com/news/montgomery-county-ends-security-robot-pilot-program-amid-community-concerns-about-surveillance | 2026-01-15 | about 12:18 to 12:19 | fetched | new | Shirin Rajaee. Montgomery County (Maryland) DOT dropped "Parker", a Knightscope garage patrol robot, before launch: "we have decided not to move forward with this pilot program", after backlash over surveillance and trust among immigrant residents. Unarmed. A withdrawal, but from January. |
| 10 | https://www.koreatimes.co.kr/southkorea/defense/20261016/army-chief-proposes-deploying-robots-in-dmz-in-talks-with-brunson | 2026-10-16 (upd. 18 Oct) | about 12:18 to 12:19 | fetched | new | Bahk Eun-ji. After a 21 Sept mine blast injured three soldiers, Gen. Kim Kyu-ha proposed "robots and drones should go in instead" for hazardous DMZ work; he says Gen. Brunson agreed. Armament and human control not mentioned. A proposal. |
| 11 | https://www.al-monitor.com/originals/2026/11/israel-army-launches-ground-operation-hamas-controlled-area-gaza | 2026-11-18 | about 12:18 to 12:19 | fetched | new | AFP. A ground operation in a Hamas-controlled area; "three separate Israeli drone strikes on Wednesday", three killed per Gaza's civil defence. Robots, cranes and remote weapons not mentioned. Context only. |
| 12 | https://www.lawyerscommittee.org/lawyers-committee-files-lawsuit-on-behalf-of-black-students-detained-and-searched-due-to-ai-alert-falsely-identifying-a-bag-of-chips-as-a-firearm/ | 2026-11-17 | about 12:21:45 to 12:22:13 | fetched | new | Suit in the Circuit Court for Baltimore County against Omnilert LLC, Baltimore County Public Schools and Baltimore County Police. Omnilert Gun Detect flagged a bag of crisps at Kenwood High School in October 2025 as a "90% probability" gun; though school and police officials cancelled the alert, armed police were dispatched and students were "ordered to their knees, handcuffed, and searched". The Lawyers' Committee: "This should have never been escalated to the police." Claims are the plaintiffs'; no response from the defendants is included. Students' names are not recorded here. |
| 13 | https://www.uvic.ca/systems/about/notices/restricting-ai-agent-access-to-university-resources.php | 2026-10-13 | about 12:21:00 to 12:21:34 | fetched | new (uvic.ca appears in LH044 data only as an OAI-PMH registry entry) | "Restricting AI Agent Access to University Resources": autonomous agents, "such as OpenAI Dots and Meta Muse", are "blocked from accessing university information systems"; sign-ins may be blocked and a NetLink ID disabled if used to give an agent access. Reason given: security and privacy of data. Load and scraping are not mentioned. |
| 14 | https://www.kyivpost.com/post/89491 and /post/89428 | 2026-11-08, 2026-11-07 | about 12:22:42 to 12:23:03 | fetched | new | Drone-post and launcher strikes. No ground robots. Not relevant. |
| 15 | https://zdnet.co.kr/view/?no=20261116153535 | 2026-11-16 17:33 KST | about 12:23:30 onwards | fetched | new | Jang Yumi and Kim Dongwon. MS365 down about 36 hours from the 12th, "740만 건이 넘는 장애 신고" from over 70 countries; the FAA outage from "라우터 과부하" during copper-to-fibre conversion. No AI-found flaw or patch is named as a cause. No Korean impact described. |
| 16 | https://fastcompanybrasil.com/tech/bots-de-ia-da-meta-e-alibaba-quase-tiraram-do-ar-um-arquivo-historico-lgbtqia/ | 2026-08-14 | about 12:23:30 onwards | fetched | new | Chris Stokel-Walker, apparently adapted from Fast Company in English. The UK LGBT History Project, self-funded by one person: one Meta crawler made about 26,000 requests in a day, about 12 GB, ignoring robots.txt, as he reports from his own log analysis; he doubled server capacity; Alibaba- and Tencent-linked crawlers hit it over three weeks. "Não existe fiscalização da internet. Não há ninguém a quem recorrer." The companies did not reply. |
| 17 | https://perishablepress.com/chrome-ai-wasting-much-bandwidth/ | updated 2026-11-20 | about 12:19:20 to 12:19:48 | fetched | new | Jeff Starr. Says Chrome's on-device AI features caused "many GBs per month" of traffic that stopped when he turned them off. No tool, figures or source beyond a post on X. An anecdote. |
| 18 | https://www.washingtonsun.com/technology/ | index | about 12:19:20 to 12:19:48 | fetched | new (index) | Follow-ups since 17 Nov include "Trump's Cyber Chief Departs the White House as Online Outages Stack Up" (19 Nov), "Lawmakers Zero In on CISA Staffing Shortages After Outages" (19 Nov, not opened), "Vance Pulls Out of an Event to Attend Meetings About Outages" (18 Nov, not opened), "FAA Halts Installation of Routers That Led to a Ground Stop" (17 Nov). |
| 19 | https://www.washingtonsun.com/us-news/faa-halts-router-installation-after-ground-stop | 2026-11-17 14:19 | about 12:19:48 to 12:20:05 | fetched | new | AP (Josh Funk, Kevin Freking). On record, the FAA traced the ground stop to one router recently installed in El Dorado, Arkansas, sending "excessive data … at a rate of 1,000 connection attempts every 4 to 5 seconds"; installation paused and installed Juniper routers turned off. Democrats: "Identifying the device that failed does not establish why it failed." No patch or AI mentioned. |
| 20 | https://www.washingtonsun.com/administration/trumps-cyber-chief-sean-cairncross-leaving-resigns-white-house-faa-outages | 2026-11-19 19:31 (upd. 20:40) | about 12:19:48 to 12:20:05 | fetched | new | Gavin J. Quinton. National Cyber Director Sean Cairncross is leaving; an anonymous source says Trump backed firing him. Cairncross attributed the disruptions to upgrades of aging systems, "not any sort of coordinated, nefarious cyberattack from a malicious actor". Patching and AI-found flaws are not discussed in the body. |

Pages opened: 20 rows, 27 requests counting the three NANOG threads, the three ioc.exchange calls and the two Kyiv Post pages.

## Refusals and walls

- ioc.exchange tag timelines: HTTP 422, authentication required, ×3. Not retried. infosec.exchange gave the same on 18 November.
- mastodon.social tag timeline: disallowed by robots.txt, not fetched.
- www.cp24.com and www.ctvnews.ca (Canadian Press, 17 Nov, university libraries swamped by bots): disallowed, not fetched.
- www.bbc.co.uk (UK fridges secured, 20 Nov): disallowed, not fetched.
- regexr.com (temporarily offline): disallowed, not fetched.
- www.wsj.com (Visa, Mastercard and JPMorgan data leak): disallowed, not fetched.
- next.ink 268124 (French piece on the US outages): disallowed, not fetched.
- outraspalavras.net (Wikifavelas, a Brazilian community wiki said to be hit by AI crawlers): disallowed, not fetched.
- I did not query codeberg.org, status.codeberg.org or any NameSilo page.

## Search results not opened

futurism, gizmodo, thenextweb, promptzone, theoutpost and explainx on the Washington Sun claim (one source family: the Washington Sun's anonymous sourcing); the foxbusiness Clayton interview; citizen.org's call for an investigation; saharareporters on the senators' letter; Washington Sun's CISA staffing and Vance items; korea.kr's budget column and thedefensepost's DMZ network piece; dronexl on the Montgomery County police drone director; thepage.ua on robots with AK rifles in combat trials; techradar on Chinese robot squads for riot police; infobae on SOUTHCOM's autonomous command; keyt/CNN en Español on organised-crime drones; aiweekly on the Marmot consortium; startuphub on libraries; it-connect on Patch Tuesday; borncity and boerse-express on CISA's 72-hour rule; ifun.de on bot share; cio.com's Korean edition on the three-chatbot outage; the techdirt court ruling. None of these were opened.

## Quiet

- No armed-robot item dated November 2026 in Ukrainian, Russian, Korean, Chinese, Hebrew, Arabic, Hindi, Spanish or Portuguese searches. Nothing at all on Sudan, Yemen, Libya or elsewhere in Africa.
- Ukraine has published no November ground-robot count; October's 31,398 (seen 18 Nov) is still the newest.
- No armed police robot withdrawn or suspended in November. The only withdrawal found, Montgomery County's Parker, was unarmed and from January.
- No new NANOG thread on AI traffic or the outages.
- Codeberg's account has said nothing since 11:23Z on 18 November, and gives no cause.

## Language and geography limits

I searched in English, Ukrainian, Russian, Korean, Chinese (simplified), Hebrew, German, Japanese, Spanish, French, Arabic, Hindi and Portuguese. Every search went through one US-indexed tool whose summaries are in the query's language but whose results are often English; the Chinese and Arabic searches came back almost wholly in English. I opened pages in English, Korean and Portuguese, and nothing in Chinese, Arabic, Hebrew, Hindi, Japanese, Russian, German, French or Spanish. Geography covered by opened pages: the US, Canada, South Korea, the UK, Gaza and Ukraine. Africa, South and Southeast Asia, Latin America and the Gulf appear only in search summaries that found nothing dated November. The outage claims form one source family on the AI link (the Washington Sun's anonymous sources, repeated by at least six outlets); the on-record hearing remarks are a second, reported by Nextgov and CyberScoop from the same session. A language with no November item means only that this search found none.

## Five best new leads

### 1. The AI-patching claim, partly on the record: lawmakers link it to AI, witnesses and operators do not

- **Primary URLs.** https://cyberscoop.com/?p=91641 and https://www.nextgov.com/cybersecurity/2026/11/security-officials-tell-congress-tech-outages-are-not-malicious/417312/ (both 18 Nov); FAA cause via AP at https://www.washingtonsun.com/us-news/faa-halts-router-installation-after-ground-stop (17 Nov); Cairncross at https://www.washingtonsun.com/administration/trumps-cyber-chief-sean-cairncross-leaving-resigns-white-house-faa-outages (19 Nov). The hearing record itself was not found or read.
- **What was reported.** At the House Homeland Security hearing on 18 November, the DNI said the rate of patching is increasing and witnesses saw no attack; none of them, as reported, said AI found the flaws. Sen. Warner and Rep. Himes did tie patch pressure to AI discovery. The FAA's on-record cause is one router's connection flood; the departing cyber director names upgrades of aging systems.
- **Why it matters.** This is the charter's indirect route, AI activity degrading shared infrastructure through defenders' load, and it now has a dated, on-record first version from legislators, beside operator statements that give other causes. Unknown stays unknown: no operator has said a model-found flaw's patch caused an outage.
- **Feeds.** The AI cost investigation (load), the model-found-bug thread, and scout 4's map of the eight outages (CSA note, Reuters).
- **Window.** Days to weeks: the hearing transcript, the Democrats' letter to the Transportation Secretary on root cause, and Microsoft's final review.
- **Next step.** Read the committee's hearing record when posted and quote what each witness said about patching and AI; treat any later operator post-incident review as the test.

### 2. An AI gun detector's false alert brings armed police to students: lawsuit filed 17 November

- **Primary URL.** https://www.lawyerscommittee.org/lawyers-committee-files-lawsuit-on-behalf-of-black-students-detained-and-searched-due-to-ai-alert-falsely-identifying-a-bag-of-chips-as-a-firearm/ (17 Nov 2026).
- **What was reported.** Omnilert Gun Detect flagged a bag of crisps as a probable gun at a Baltimore County school in October 2025; despite cancellation, armed police were dispatched and students handcuffed and searched. The suit names the vendor, the school system and the police.
- **Why it matters.** The physical-authority question is about delegated force and the people subjected to it; here an AI classification, not a robot, set armed human force in motion, and a court case now tests accountability. It is the civilian-experience report the scout's brief asks for, though unarmed by the system itself and outside LH050's robot panel.
- **Feeds.** The physical-authority investigation as a comparator; not an LH050 case and not an extra-read trigger.
- **Window.** Months: the defendants' answers and any court ruling. The allegations are the plaintiffs'.
- **Next step.** Note it as a comparator lead for the investigation page's context; read the complaint itself, if public, before quoting more.

### 3. A university blocks autonomous AI agents from its systems, as Canadian libraries report bot overload

- **Primary URL.** https://www.uvic.ca/systems/about/notices/restricting-ai-agent-access-to-university-resources.php (13 Oct 2026). Related, disallowed: Canadian Press via CP24 and CTV (17 Nov).
- **What was reported.** UVic blocks agents "such as OpenAI Dots and Meta Muse" from its information systems and may disable accounts used to give them access, citing security and privacy. Per search summaries only, Canadian Press reports libraries swamped by AI scraping, and a Colorado consortium logged over 2 billion bot connection attempts in 30 days.
- **Why it matters.** A named institution closing its systems to user-side agents, not just crawlers, is a new kind of closing for the closing-web watch, and it is dated. The library load claims are the cost side, but rest so far on a disallowed wire story.
- **Feeds.** LH044 (as comparison class, not its panel) and scout 1's beat.
- **Window.** Low urgency; the policy is in force from 13 October.
- **Next step.** Scout 1 or LH044's next read should look for other universities' agent bans and for the Marmot consortium's own figures from a readable primary source.

### 4. Codeberg: no cause stated two days on, and a registry "abuse wave" a week before

- **Primary URL.** https://social.anoxinon.de/@codebergstatus/117637187711177698 (11:23Z, 18 Nov); https://social.anoxinon.de/@codebergstatus/117603812330018096 (12 Nov).
- **What was reported.** The domain recovered on 18 November; NameSilo's abuse department had sent "no official response". On 12 November Codeberg restricted pulls from its container registry "due to an abuse wave".
- **Why it matters.** A shared code commons was cut off by one intermediary's abuse process and, separately, throttled by abuse traffic. Neither is said to involve AI, and that should not be assumed; but this is how a commons closes, and LH044 counts closings.
- **Feeds.** LH044 context (its read 2 is on 22 November); scout 4 covered the suspension today via Linuxiac.
- **Window.** Days: the registrar's explanation may come late or not at all.
- **Next step.** Read the status account again at the next sweep for a stated cause, and note whether the 12 November abuse wave is ever characterised.

### 5. A one-person LGBT history archive says AI crawlers nearly took it offline

- **Primary URL.** https://fastcompanybrasil.com/tech/bots-de-ia-da-meta-e-alibaba-quase-tiraram-do-ar-um-arquivo-historico-lgbtqia/ (14 Aug 2026, Portuguese adaptation of a Fast Company piece).
- **What was reported.** The UK LGBT History Project's owner says one Meta crawler made about 26,000 requests in a day, about 12 GB, ignoring robots.txt; he doubled capacity and spent nights building blocks. Alibaba and Tencent crawlers are also named. The companies did not respond.
- **Why it matters.** It is a concrete, self-funded cultural commons paying for AI load, with a per-day figure, found through non-English press that the English-language scouts would not search. The figure is the owner's own log reading, not a measurement anyone checked.
- **Feeds.** The AI cost investigation (load on the open web) and LH044's comparison class.
- **Window.** Low; the event is from August.
- **Next step.** Find the English original and the owner's own account, then file it beside the Gentoo and library cases as owner-reported load, labelled as such.

## Notes

- Also seen, outside the five: South Korea's Army chief proposed robots for hazardous DMZ work (row 10, 16 Oct; armament not mentioned), and a column reports a first 43 billion won "physical AI" line in the 2027 defence budget including garrison guard (not opened). This is the nearest non-Western physical-authority item found and is a proposal, not a deployment. Montgomery County's January withdrawal of an unarmed patrol robot (row 9) adds to the US withdrawal list.
- The Chrome bandwidth post (row 17) is an anecdote without figures; left for scout 1 if it recurs with measurement.
- The European refrigeration attacks are already known (10 Nov); the BBC's 20 Nov follow-up was disallowed.
- Rules: 26 searches and 20 page rows. Every fetch was gated first and no disallowed URL was fetched. The Mastodon 422s were not worked around. Saved bodies are only in the scratchpad and were redacted; the NANOG list address in a URL is shortened to "nanog@…" and an address in one thread body was withheld by the redactor. No student is named. I did not commit or edit any other file.
