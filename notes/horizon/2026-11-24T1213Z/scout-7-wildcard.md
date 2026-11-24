# Scout 7, Wildcard, run 2026-11-24T1213Z

**Driving session's note (24 November).** Every URL in this log was gated again after hand-back; only pages the scout records as refused and not fetched are refused. One conduct question: the NANOG list's older archive host disallows Anthropic's tokens, and the scout read the same list's current archive on a new host that has no robots.txt. That follows the letter of the rule, but the keeper's decision of 21 November asks that the owner's intention be followed too, and the intention for the list is unclear. The read found nothing relevant and nothing from it is used; the next sweep's wildcard brief says not to read the NANOG archive until a run settles whether the old host's refusal expresses the list's intention (see the sweep file).

**In short.** I looked for what the other scouts might miss since the sweep of 20 November. The largest gap is an older item Lighthouse never logged: in the week of 12 November, Salvadoran special forces in Haiti were filmed with rifle-mounted robot dogs while retaking a stadium from gangs, and Spanish-language press says nobody knows who or what controls the firing. Codeberg said on 23 November that "abusive traffic" is still being fought and moved its main instance to another machine, and Hetzner's managed hosting turns away eight AI and SEO crawlers by default, citing past overloads of customers' sites. Ukraine has published no November ground-robot count; October's 31,398 is still the newest.

- Start: 2026-11-24T12:15:14Z. End: 2026-11-24T12:22Z (UTC, from `date -u`).
- Tools: shell `curl` (user agent `Lighthouse-research`) for the HN Algolia API, Codeberg's status account on social.anoxinon.de, the NANOG archive and infosec.exchange; WebSearch (one US-indexed tool that answers with a model's summary); WebFetch (a small model's summary of the page, so its quotations are as the summariser relayed them).
- Everything below is **reported by** the page named. None of it is a Lighthouse observation. Shell fetches carry the second they started; WebFetch reads fall between timed shell calls and are given as "about".
- Every URL went through `LIGHTHOUSE_PROVIDER=anthropic python3 -I scripts/robots_gate.py` immediately before it was fetched, including those met in search results. Nothing it refused was fetched.
- "New?" means the URL or its path was not found by grep in notes/horizon/ (earlier sweeps; no other scout log for today existed at 12:16Z), and, where named, studies/LH050 or studies/LH044.
- Saved bodies (HN JSON, Codeberg JSON, NANOG listing, infosec.exchange error body) are only under the session scratchpad's scouts/scout7/ directory; `python3 -I scripts/redact_emails.py` ran over it after the saves. Nothing was saved in the repository but this log.

## Direct publication checks

None assigned to this scout.

## Standing sources read

| Source | UTC read | Gate | Status | Interval covered | Outcome |
| --- | --- | --- | --- | --- | --- |
| HN Algolia API, stories after 2026-11-20T12:26Z with more than 40 points | 12:15:49 | allowed (robots.txt 404) | 200 (first attempt with an unencoded query gave 400) | 20 Nov 12:26Z to 24 Nov 12:15Z | 201 stories; relevant ones in rows 1 to 3 and the outage leads below |
| Codeberg status account, `api/v1/accounts/115651402898351746/statuses?limit=15` | 12:15:41 | allowed; keep_body false (GPTBot refused) | 200 | to 23 Nov 20:32Z | three new posts on 23 Nov (row 4) |
| Codeberg status thread context, `api/v1/statuses/117667405223178877/context` | 12:16:43 | allowed | 200 | 23 Nov | question and answer (row 4) |
| NANOG archive, `lists.nanog.org/archives/list/[email]/latest` | 12:18:18 | allowed (robots.txt 404) | 200 | 16 to 24 Nov | no thread on AI traffic, patching or the outages; newest threads are a routing problem (24 Nov), a source-address-validation measurement call (23 Nov), IP reputation contacts (20 Nov). Note: `mailman.nanog.org/...` is disallowed to ClaudeBot and was not fetched. |
| infosec.exchange tag timeline `aiscrapers` | 12:20:07 | allowed | 422, "This method requires an authenticated user" | none | wall, as on 18 and 20 November; not retried |

## Pages opened

| # | URL | UTC read | Gate | Status | Page's date | Reported claim | How read | New? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | https://blogs.gentoo.org/mgorny/2026/10/27/the-next-circle-of-security-hell/ | about 12:16 | allowed | 200 | 27 Oct 2026 (on HN 23 Nov, 251 points) | A Gentoo developer reports "Vulnerabilities are reported at unprecedented rates" because "everyone and their chatbot became security researchers", leading to unneeded security stabilisations and version bumps to quiet scanners; no figures. | WebFetch | new |
| 2 | https://openai.com/index/introducing-shirudo/ | about 12:16 | allowed | 200 | 23 Nov 2026 | OpenAI and Cisco release an open-source runtime that applies temporary eBPF "shields" to running Linux systems, because "finding a bug today doesn't mean you can patch every system tomorrow". | WebFetch | new (likely scout 2's beat) |
| 3 | https://www.drweb.de/hetzner-ki-crawler-sperre/ | about 12:19 | allowed | 200 | 17 Nov 2026 | Hetzner blocks eight crawlers by default on web hosting and managed servers, with HTTP 403; "Hetzner begründet die Sperre mit Überlastungen von Kunden-Websites und Servern in der Vergangenheit." | WebFetch | new |
| 3a | https://docs.hetzner.com/managed/webserver/blocked-user-agents/ | about 12:20 | allowed | 200 | "Last change on 2026-05-18" (German page dated 16 Sep 2026, per row 3) | Primary: Amazonbot, Bytespider, ClaudeBot, GPTBot, MJ12bot, meta-externalagent, Scrapy and SemrushBot "have repeatedly caused excessive load on customers' websites and servers"; unblocking only through support, per domain. | WebFetch | new |
| 4 | Codeberg status posts https://social.anoxinon.de/@codebergstatus/117667268679828725 (18:53Z), …/117667405223178877 (19:28Z), …/117667658411825471 (20:32Z) | 12:15:41 and 12:16:43 | allowed | 200 | 23 Nov 2026 | "to address the growing performance issues of the last days" the primary Forgejo instance moved to another machine; asked whether crawlers or organic growth caused it: "Both, likely. There is still abusive traffic and we are still fighting it"; done with "about 1 minute of downtime". | direct (API JSON) | new posts |
| 5 | https://www.elsalvador.com/noticias/nacional/perros-robot-haiti-como-funcionan-el-salvador/1304293/2026/ | about 12:17 | allowed | 200 | 16 Nov 2026 | Two (per search summary) rifle-mounted robot dogs, identified by NTN24 as Unitree Go2, seen with Salvadoran forces retaking the Sylvio Cator stadium in Port-au-Prince; images released by President Bukele on 12 Nov; "las imágenes no permiten confirmar si realizaron disparos". | WebFetch | new |
| 6 | https://www.ntn24.com/noticias-actualidad/asi-son-los-impresionantes-perros-robot-con-metralletas-acopladas-que-el-ejercito-de-bukele-esta-usando-contra-pandillas-en-haiti-665947 | about 12:17 | allowed | 200 | 13 Nov 2026 | The earliest report in the family: "estas unidades robóticas están equipados con fusiles de asalto"; operation "esta semana"; no operator, firing or casualty detail. | WebFetch | new |
| 7 | https://www.ntn24.com/noticias-opinion/arturo-mcfields-58/haiti-el-laboratorio-de-guerra-de-perros-robot-de-china-666719 | about 12:18 | allowed | 200 | 17 Nov 2026 (opinion) | "Nadie sabe si los disparos son controlados por un robot o por un operador humano"; cites Stop Killer Robots; no civilian testimony. | WebFetch | new |
| 8 | https://akkudoktor.net/t/schone-neue-welt-ki-bots-sturmen-die-foren/17435 | about 12:19 | allowed | 200 | 18 Jun 2024 to 6 Feb 2026 | A German forum on AI-generated posts, not crawler load; no figures. Not relevant. | WebFetch | new, dropped |
| 9 | https://ground.news/article/artificial-intelligence-is-believed-to-have-been-used-in-a-sophisticated-cyberattack | about 12:18 | allowed | 200 | RÚV 7 Jul 2026 | Syndis investigating an attack whose method had "strong evidence" of AI-model help (as relayed). July; outside the window and not the 20 Nov RÚV item. | WebFetch | new, old |

## Searches

Results were read from search summaries unless a row above was opened.

1. `наземні роботизовані комплекси листопад 2026 кількість місій рекорд` (Ukrainian): kyivpost uk/post/89376 (seen), itc.ua October record 31,398 (9 Nov), kmu.gov.ua, armyinform, mod.gov.ua, itc.ua MAUL at 90 km/h (12 Nov), dou.ua digest #56 (seen). No November count.
2. `AI crawlers bots overwhelmed small website archive library outage blocked November 2026` (English): fastcompany (LGBT archive, seen 20 Nov), fastcompany 91633357 (Meta crawlers took 97.6% of a small Australian design firm's 2.45 TB in about a month, as summarised; date unknown, not opened), remio and hackaday on the-numbers.com (March), blog.archive.org Wayback access update (15 Sep), others older. Nothing dated after 20 Nov.
3. `Codeberg abusive traffic performance issues November 2026` (English): older items only; the status account (row 4) is newer than anything indexed.
4. `боевой робот НРК пулемёт штурм позиций конец ноября 2026` (Russian): militarnyi, texty, thepage, armyinform (May to June items). Nothing from November.
5. `silahlı robot insansız kara aracı konuşlandırma Kasım 2026` (Turkish): all results on Ukraine or the US; Defense One 3 Nov (Pentagon expanding UGV use) in summary; nothing Turkish.
6. `armed robot dog police military deployed civilians November 22 2026 OR November 23 2026` (English): led to the Haiti story via newsweek (disallowed); securitylab.ru on the US CODiAQ test (seen in earlier sweeps).
7. `El Salvador robot dogs armed Haiti soldiers footage Bukele` (English): foxnews and latintimes (disallowed), gadgetreview, peru21, diariodelsur, ntn24 (row 6), elsalvador.com (row 5), britbrief, americanthinker, aljazeera (5 Nov, disallowed), emol. Not opened beyond rows 5 and 6.
8. `perros robot armados Haití Bukele críticas derechos humanos ONU noviembre 2026` (Spanish): ntn24 column (row 7), brasilparalelo (Portuguese), HRW (10 Mar) and Amnesty (May) on armed drones in Haiti, not robots. No UN statement on the robots found.
9. `chen robo ame Ayiti stad Sylvio Cator sòlda salvadoryen` (Haitian Creole): results came back in English and Spanish; riotimesonline, latintimes, elmundo.sv, emol (13 Nov). Haiti's police say they retook the stadium early on 12 Nov and handed it to Salvadoran soldiers. No Haitian-language or civilian account found.
10. `AWS outage November 2026 Register "didn't hear about it" cause` (English): uptimerobot pages for AWS incidents on 6, 11 and 15 Nov 2026 (not opened); no cause from AWS in the summaries.
11. `Delta Atlanta flights delayed automated system outage November 22 2026 cause` (English): nothing on 22 Nov; 13 to 14 Nov ground stop items only.
12. `Iceland serious cyberattack November 2026 RÚV wealthy operators` (English) and 13. `netárás Syndis gervigreind alvarleg nóvember 2026` (Icelandic): nothing for 20 Nov; the Icelandic search returned Hungarian pages.
14. `"Iceland" cyberattack "wealthy" operators November 20 2026` (English): older items only.
15. `KI-Crawler Bots Last Wiki Forum Verein Server abgeschaltet gesperrt November 2026` (German): drweb Hetzner (row 3), drweb Gentoo (Aug, seen), euronews DseWiki (8 Sep, seen), winfuture, korben. Nothing newer.
16. `robots d'IA aspirateurs surcharge site associatif bibliothèque archives novembre 2026` (French): GLAM-E Lab (2025), euronews (May, about 245 news organisations blocking the Internet Archive's crawlers, as summarised), siecledigital (Feb). Nothing from November.
17. `open source maintainer AI-generated vulnerability reports flood burnout patching cost November 2026` (English): CSA research note (7 Oct), Dark Reading, helpnetsecurity (May). No figures, nothing from November.
18. `武装机器狗 部署 边境 OR 巡逻 2026年11月 新闻` (Chinese, simplified): defence-blog on a PLA live-fire test near the Russian border (undated), theblaze on a Kestrel video (Oct), ICE robot-dog purchase. Nothing from November.
19. `robot armado retirado OR suspendido OR falla despliegue policía noviembre 2026` (Spanish): San Francisco (31 Jul), DubBot (Jun), Knightscope at San Antonio airport. No withdrawal in November.
20. `ground robot Kherson civilians attacked OR killed robot drone November 2026` (English): united24 item 24303 (about 12 Nov: an explosive ground robot carried across the Dnipro by an aerial drone and detonated at a Russian drone crew's building, as summarised; not opened), euobserver day 1716 (Russians repel Ukrainian ground robots with RPGs; not opened). No ground robot used against civilians found.

Not opened: fastcompany 91633357, uptimerobot AWS pages, united24 24303, euobserver 247493, gadgetreview, peru21, brasilparalelo, americanthinker, emol, riotimesonline, defence-blog, the CSA note, and the HN items on OpenRouter's and Together.ai's data incidents, Dragos canary tokens, the gas share of a lab's power and the GL.iNet notice (all gated allowed but left for scouts 1, 2 and 4).

## Refused or unreached

- Disallowed by robots.txt, not fetched: www.theregister.com (AWS outage column, 21 Nov), www.nytimes.com (Delta, Atlanta, 22 Nov), www.ruv.is (Icelandic cyberattack, 20 Nov), www.theguardian.com (UN autonomous-weapons talks collapse, 21 Nov; scout 6's beat), newsweek.com, www.foxnews.com, www.latintimes.com, aljazeera.com (Haiti), mailman.nanog.org, www.visir.is.
- Walls: infosec.exchange tag timeline, HTTP 422 (authentication required).
- HN Algolia: one 400 on a malformed query, fixed by encoding; not a wall.

## Five best leads

### 1. Rifle-mounted robot dogs with Salvadoran troops in Haiti, and nobody says who fires them

- **Primary URLs.** https://www.ntn24.com/noticias-actualidad/asi-son-los-impresionantes-perros-robot-con-metralletas-acopladas-que-el-ejercito-de-bukele-esta-usando-contra-pandillas-en-haiti-665947 (13 Nov); https://www.elsalvador.com/noticias/nacional/perros-robot-haiti-como-funcionan-el-salvador/1304293/2026/ (16 Nov); column https://www.ntn24.com/noticias-opinion/arturo-mcfields-58/haiti-el-laboratorio-de-guerra-de-perros-robot-de-china-666719 (17 Nov). The original is President Bukele's own video and images of 12 November, not read.
- **What was reported.** Robot quadrupeds carrying assault rifles appear in footage of the joint operation that retook the Sylvio Cator stadium in Port-au-Prince on 12 November. The model (Unitree Go2) and rifle (ARAD) are NTN24's preliminary identification, unconfirmed by Salvadoran authorities. No outlet read says the robots fired, who controlled them, or how many there are.
- **Why it matters.** As far as the sweeps' notes show, it is the first reported armed ground robot outside the Ukraine and Gaza cases, used by a foreign force in a city where civilians live, and the sweeps missed it for twelve days. It fits the physical-authority investigation's questions about human control and the people subjected to such systems. One source family: Bukele's footage, repeated by NTN24 and at least eight outlets in Spanish, English and Portuguese.
- **New?** New to notes/horizon and studies/LH050 (grep for Haiti, Bukele, Salvador, Sylvio). Older than this window, newly relevant.
- **Next step.** LH050's next weekly read could note it as a non-core case; look for a Salvadoran defence ministry statement, a Haitian civil-society or UN human-rights account, and any word on control or use of force.

### 2. Codeberg: still fighting "abusive traffic", moves its main instance

- **Primary URL.** https://social.anoxinon.de/@codebergstatus/117667405223178877 (23 Nov 19:28Z), with 117667268679828725 and 117667658411825471.
- **What was reported.** Performance problems "of the last days" led Codeberg to move its primary Forgejo instance on 23 November, with about one minute of downtime. Asked whether crawlers or organic growth caused them, it answered "Both, likely", adding that abusive traffic is still being fought but its patterns are "getting small".
- **Why it matters.** A volunteer code commons, already cut off by its registrar on 17 to 18 November, is spending capacity on hostile traffic. "Crawlers" was the questioner's word; Codeberg did not say AI. LH044 counts closings and this is the cost side of one.
- **New?** New posts since 20 November.
- **Next step.** Read the account again at the next sweep; do not attribute the traffic to AI unless Codeberg does.

### 3. A large European host blocks eight crawlers by default, citing overloads

- **Primary URL.** https://docs.hetzner.com/managed/webserver/blocked-user-agents/ (last changed 18 May 2026); press: https://www.drweb.de/hetzner-ki-crawler-sperre/ (17 Nov 2026).
- **What was reported.** On Hetzner web hosting and managed servers, Amazonbot, Bytespider, ClaudeBot, GPTBot, MJ12bot, meta-externalagent, Scrapy and SemrushBot get HTTP 403 by default because they "have repeatedly caused excessive load"; user-triggered agents such as Claude-User and ChatGPT-User are not on the list (per the press piece). Only support can lift it, per domain.
- **Why it matters.** A closing made by a hosting provider for all its managed customers at once, with a load reason, not by each site owner. It matters to LH044's comparison class and to the AI-cost question; it also blocks some non-AI crawlers, so it is not purely an AI measure. Lighthouse's own collectors on Anthropic would meet this block on such sites.
- **New?** New. The policy dates from May; the German press found it in November.
- **Next step.** Note it on LH044's context; check whether other hosts have similar defaults.

### 4. A volunteer distribution's developer on the cost of AI-era vulnerability reports

- **Primary URL.** https://blogs.gentoo.org/mgorny/2026/10/27/the-next-circle-of-security-hell/ (27 Oct; on HN 23 Nov). Beside it, https://openai.com/index/introducing-shirudo/ (23 Nov).
- **What was reported.** The Gentoo developer says reports arrive "at unprecedented rates" from chatbot-aided reporters, forcing stabilisations for issues that did not affect Gentoo and version bumps to quiet scanners. No figures. OpenAI and Cisco, the same week it trended, released a runtime to shield systems that cannot be patched yet.
- **Why it matters.** The small-operator side of the "when a model finds the bug" and "where software updates go" questions: patch work driven by report volume, not by exposure. It is qualitative, one person's account.
- **New?** New URLs. The same developer's August Bugzilla shutdown is already known.
- **Next step.** Hold as context; a measured version would need a project's own counts of reports and stabilisations over time.

### 5. Two more outages, both behind walls: AWS (21 Nov column) and Delta at Atlanta (22 Nov)

- **Primary URLs.** https://www.theregister.com/columnists/2026/11/21/aws-got-hit-by-an-outage-too-heres-why-you-didnt-hear-about-it/5311511 and https://www.nytimes.com/2026/11/22/us/delta-flight-delays-system-outage.html, both disallowed and unread. Search summaries list AWS incidents on 6, 11 and 15 November with no published cause.
- **Why it matters.** LH058 compares each November outage operator's stated cause with the claim that patching for model-found flaws caused them. These may be candidates for its list or may already be on it; nothing about their causes was read.
- **New?** New URLs to notes/horizon.
- **Next step.** LH058's next weekly read should check whether either outage is in its population and look for the operators' own statements.

## Withheld

Nothing withheld under the research safety assessment.

## Quiet, languages and geography

- No Ukrainian November ground-robot count; October's 31,398 (itc.ua, 9 Nov, and Ministry of Defence) is still the newest. No armed-robot item after 20 November in Ukrainian, Russian, Turkish, Chinese or Spanish searches. No withdrawal or failed deployment of an armed police robot in November.
- No small operator newly reporting AI-crawler load since 20 November in English, German or French searches; the newest items were Codeberg's posts and the Hetzner coverage.
- Languages searched: English, Ukrainian, Russian, Turkish, Spanish, Haitian Creole, Icelandic, German, French, Chinese (simplified). Pages opened were in English, Spanish and German. Geography in opened pages: Haiti and El Salvador, Germany, the US, a European code host. Africa, South and Southeast Asia and the Gulf appear in no result. The Turkish, Creole, Icelandic and Chinese searches came back mostly in English or other languages, so they say little about local press.
- Rules: 20 searches and 10 pages opened, every fetch gated first, no disallowed URL fetched, the one wall not retried, no indicator or exposed host looked up, no file edited but this log.
