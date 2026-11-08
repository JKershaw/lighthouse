# LH042 search log (discovery, before the brief)

Searches run with the harness's WebSearch tool (results are a search model's summary plus a list of links; a result is a lead, not a source). Times UTC, 8 November 2026. "Opened" means the page was later fetched raw and retained under data/; everything else is a lead not opened.

## D1 "exposed Ollama servers internet scan count 2026" (about 18:55)
Links: blog.leakix.net/2026/02/ollama-exposed/; scworld.com brief (internet-exposed Ollama widespread); securityboulevard.com 2026/03 exposed Ollama; indusface.com; cybernews.com (175,000 exposed AI systems); en.wikipedia.org/wiki/Ollama; malwarepatrol.net (over 14,000 Ollama instances); tianpan.co forum; particula.tech.
Summary named: 175,000 (SentinelLABS and Censys, 293 days, January 2026); 12,269 (LeakIX, February 2026); 14,000+ (Malware Patrol, undated in summary).

## D2 "OpenClaw exposed instances count Censys Shodan" (about 18:56)
Links: adversa.ai OpenClaw security 101; reco.ai; censys.com/blog/openclaw-in-the-wild-mapping-the-public-exposure-of-a-viral-ai-assistant/; dev.to (220,000+); labs.cloudsecurityalliance.org Claw Chain note; betterclaw.io; blog.cyberdesserts.com (63,070 live instances in March); cyberdesserts malicious skills; penligent.ai.
Summary named: Censys 21,639 at 31 January 2026; 63,070 live at 31 March 2026 (Censys-based); Penligent 1,842 at 30 January (Shodan); CSA note citing Cybersecurity News: May 2026 Shodan about 65,000 and ZoomEye about 180,000; SecurityScorecard 135,000; Penligent 220,000.

## D3 "Shadowserver open Ollama report OR "AI" exposed scan dashboard 2026" (about 18:56)
Links: blog.leakix.net/2026/02/appscan-coverage-2026/; cybernews.com; labs.cloudsecurityalliance.org exposed AI infrastructure note; indusface; CSA LLMjacking note; thebrightbyte.com "A million exposed AI services"; malwarepatrol; aistorm.cc; particula.
Summary named: no Shadowserver Ollama dashboard found; Intruder 5,200 Ollama API servers queried, 31% answered; GreyNoise 91,403 sessions (honeypot, not exposure).

## D4 "unauthenticated ADB port 5555 exposed devices count 2026 Kimwolf" (about 18:58)
Links: thehackernews.com/2026/01/kimwolf-android-botnet-infects-over-2.html; thehackernews.com/2026/08/kimwolf-v7...; esecurityplanet; synthient.com/blog/a-broken-system-fueling-botnets; rescana; teampen; ctrlaltnod; cyberpulseacademy; runtimerebel.
Summary: no internet-wide count of exposed port 5555 for 2026; infection totals (Synthient over 2 million; XLab 1.8 million) are infections, not exposure; Synthient's 67% unauthenticated is a share of one proxy pool.

## D5 "exposed MCP servers internet scan count no authentication 2026" (about 18:58)
Links: securityboulevard.com/2026/11 MCP disclosure; dev.to (38% no auth, 514 servers); daily.dev; darkreading (nearly 2,000 MCP servers); pluto.security (147 unauthenticated of 179); knostic.ai/blog/mapping-mcp-servers-study (1,862, July 2025); mcpplaygroundonline; orcarouter.ai (arXiv 2608.00150, 414 servers); chatforest.com (Censys 12,520 MCP services at 28 April 2026, secondary).

## D6 ""Ollama in the Wild" IMC 2026 longitudinal exposed endpoints" (about 18:59)
Links: arxiv.org/pdf/2609.07115; themoonlight review; arxiv.org/html/2505.02502v2 (Unveiling the Landscape of LLM Deployment in the Wild); xinyi-hou.github.io/files/hou2026mapping.pdf; secureiothouse; radar.offseq.com; rankiteo; longform.social; ctrlaltnod.
Summary: daily active exposed IPs about 10,500 (mid-February 2025) to peak about 16,800 (late April 2025), 16,059 on 2026-02-13; a May 2026 scanner analysis 25,000 to 30,000 at 11 May 2026 (secondary).

## D7 "shadowserver.org news new report accessible Ollama OR "LLM" OR "AI agent" scanning 2026" (about 19:00)
Links: cyberdefensemagazine; wikipedia Ollama; sysdig.com LLMjacking evolved; indusface; wikipedia Garak; medium praetorian Julius; scworld; honeylabs.net/blog/ai-scanning-may-2026 (scanning towards honeypots, not exposure); bankinfosecurity (Cisco Talos, over 1,100 Ollama, 2025); wikipedia Moltbook.
Summary: no Shadowserver AI-service report found.

## D8 "exposed OpenClaw instances count September OR October 2026" (about 19:00)
Links: dev.to 220,000+; conscia.com; getpanto.ai; infosecurity-magazine.com (40,000+); gbhackers.com (15,200 control panels); wikipedia OpenClaw; penligent.ai (220,000+); cyberdesserts; tech-insider.org.
Summary: no count dated September or October 2026 found; SecurityScorecard 40,214 then 135,000 (February); Bitsight 30,000+ (27 January to 8 February).

## D9 "SecurityScorecard STRIKE OpenClaw declawed exposure dashboard live count" (about 19:01)
Links: x.com/security_score/status/2024892391874814391; github joylarkin/openclaw-security-news; securityscorecard.com blog posts (three); github centminmod explain-openclaw strike report copy; nhimg.org; medium; how2shout (42,900, 15,200 RCE); declawed.io.
Summary: DECLAWED is a live public dashboard by SecurityScorecard's STRIKE team, said to refresh every 15 minutes.
Design reads of declawed.io (structure only, scratchpad, not retained as evidence): robots.txt allows `User-agent: *` with "Content-Signal: search=yes,ai-train=no,use=reference" and disallows named training crawlers; the page loads its figures from an unauthenticated JSON endpoint /api/stats (HTTP 200; field names read, values not read before the brief), whose fields include total_exposed, active_count, inactive_variants, unique_ips, variant_counts and last_sync; its method section names "favicon hash and HTTP title fingerprinting" from "SecurityScorecard internet-wide scans"; "inactive" is defined on the page as "Previously discovered but no longer responding".

## D10 "Censys report exposed AI infrastructure 2026 Ollama vLLM llama.cpp count hosts" (about 19:02)
Links: thehackernews.com/2026/01/researchers-find-175000-publicly.html; CSA LLMjacking notes (two); securityweek.com 175,000; CSA lmdeploy note; techinformed; blog.cyberdesserts.com/ai-infrastructure-scanning-research/ (Shodan 25,488 Ollama, Censys about 30,000, vLLM about 156, May 2026); censys.com/blog/ollama-drama-... (10.6K high-confidence Ollama, earlier).

## D11 "Shodan Trends OR "Shodan" exposed LLM servers count Open WebUI ComfyUI 2026 report" (about 19:03)
Links: techinformed; CSA; github 7WaySecurity/ai_osint; letsdatascience; trendmicro.com TrendAI State of AI Security report (Shodan, September to mid-December 2025: 313,000 servers, nearly 230,000 Ollama at some point; 35,000 ComfyUI); sysdig misconfigured AI tool; winbuzzer (Open WebUI 17,000, 2025).

## D12 "Shadowserver "Accessible ADB" report Android Debug Bridge scan" (about 19:04)
Links: shadowserver.org Accessible ADB report page (hp-rewrite URL); Honeypot ADB Scanner Events report page; bitdefender 2018; duo decipher; securityboulevard 2018; abuseipdb; securityweek; others.
Summary: Shadowserver runs an "Accessible ADB" scan report (TCP 5555); its public dashboard is where aggregates would be (unreachable from this container: connection reset at 19:05, as LH035 found on 2 and 6 November).

## D13 "number of internet-exposed Android Debug Bridge devices Shodan 2025 OR 2026 research" (about 19:05)
Links: shodan.io search page (a scanner query interface; not used); securityboulevard 2026/05 xlabs_v1 botnet; bleepingcomputer 2018; cyware; thehackernews 2018; wikipedia; chlebda.de/blog/thousands-android-devices-exposed-adb.html (5,000+ devices, 4 March 2026, a short session); zerotrustoffsec 2024; whitehatinstitute.
Summary: Beaumont 2018 (1,100 to 15,600 after Shodan added ADB); a 2024 Shodan blog 4,425 unauthenticated; no 2025 or 2026 census.

## D14 "arXiv 2026 measurement internet-exposed LLM inference servers vLLM llama.cpp LM Studio scan census" (about 19:06)
Links: arxiv 2605.24217; 2609.08307; 2605.20706; arxiv.org/pdf/2604.19487 (IPv6 periphery, includes LM Studio and vLLM probes); arxiv.org/html/2609.07115; arxiv.org/pdf/2609.29757 (OllamaDrama, honeypot); arxiv 2609.20614; wikipedia; blogs.cisco.com detecting exposed LLM servers (Shodan case study on Ollama).
Summary: 2609.07115 says it releases aggregate, de-identified data for its 362-day window.

## D15 "exposed Ollama instances count June OR July OR August OR September 2026 scan" (about 19:10)
Links: arxiv.org/html/2609.07115; blog.leakix.net/2026/02/ollama-exposed/; CSA LLMjacking note; malwarepatrol; blogs.cisco.com Shodan case study; threatfrontier.com/articles/ollama-pull-api-ssrf-cve-2026-108836-exposed-servers-public-exploit (April 2026 sweep, 25,036 matching Shodan's Ollama signature); particula; wikipedia; worldngayon.
Summary: no count with a scan date in June to September 2026 found.

## D16 "LeakIX blog 2026 exposed AI agents OR MCP OR OpenClaw OR Ollama count" (about 19:11)
Links: dev.to mistaike_ai (42,000 AI agents); pointguardai (two); longform.social (two); buttondown.com/watchdesk (four issues, August and September 2026); besthub.dev (245,000; 250k watchboard); venturebeat.com openclaw-500000-instances; siliconangle.com/?p=730316 (9 February 2026); foxxelabs (2 million hosts); dev.to tiamatenity; radar.offseq; ctrlaltnod.
Summary: a "watchboard" catalogue of OpenClaw instances; CyberDesserts says exposure fell after February (Censys data).

## D17 "OpenClaw "watchboard" exposed instances public tracker" (about 19:12)
Links: news.lavx.hu; feedbagel.com (605,904); ngloverr.blogspot; besthub.dev; getclawkit.com (two); clawhub.ai exposure-sentinel; letsdatascience (135,000); wz-it.com; clawmate.pages.dev; dev.to (three); moltbook-ai.pages.dev; claudemarket.ai; gentic.news; nbot.ai.
Summary: the OpenClaw Exposure Watchboard at openclaw.allegro.earth lists individual instances; figures relayed from 224,015 to 605,904; operator and method not given in the summary.

## D18 ""2 million" hosts exposed AI infrastructure research 2026 scan report" (about 19:13)
Links: basil-brightmoor.github.io; foxxelabs (three); blog.rankiteo.com; cipherssecurity.com (two); techjuice.pk; thehackernews labels (two); securityscientist.net; beri.net (1M exposed AI servers, 31% no auth); algeriatech.news; letsdatascience (1 million exposed AI services); iotinsider; intelligibberish; penligent.
Summary: Intruder's scan (covered 5 May 2026): about 2 million hosts from certificate transparency, about 1 million exposed AI services; Censys's 2026 State of the Internet report (14 October 2026), 113,926 n8n hosts.

## D19 "Censys 2026 State of the Internet report AI services exposed Ollama MCP n8n" (about 19:14)
Links: finance.yahoo.com (Censys press release, 63% growth in nine months); dev.to cortexflow; censys.com/blog/state-of-the-internet-report-2026; thehackernews 175,000; arabianreseller.com; prnewswire Censys H1; axios.com/2026/10/13/censys-ai-vibe-coding-exposures; techitupme; enterpriseitworldmea.
Summary: about 268,000 internet-facing systems across 44 AI-related products as of July 2026, up from about 164,000 in October 2025; n8n 113,926; OpenClaw more than 54,000 control panels.

## D20 "Ollama 暴露 公网 数量 测绘 2026" (about 19:15)
Links: vpncentral; letsdatascience; radar.offseq; scribe.disroot.org; techradar (175,000); vulners; theregister.com/2025/09/02/exposed_ollama_servers_insecure_research/; insecurestack.substack.com (EU's exposed AI infrastructure); news.lavx.hu (1,100).
Summary: an independent writer re-ran Cisco Talos's September 2025 Shodan query (1,139) in April 2026 and found over 25,000. No Chinese-language census (FOFA, ZoomEye, Quake, CNCERT) surfaced.

## D21 "Bitsight OpenClaw exposed instances blog; Hunt.io OpenClaw exposure CVE-2026-25253 count" (about 19:16)
Links: hunt.io/blog/cve-2026-25253-openclaw-ai-agent-exposure (3 February 2026, over 17,500 vulnerable); hivesecurity.gitlab.io; mintmcp; vibegraveyard.ai (135,000+); dovpn; dev.to (three); clawspiral; feedly CVE page; techzine.eu (over 40,000); clawdocs; claw-times; extuitive; betterclaw.io; ai-news-site; cvefeed; beyondmachines; besthub; openclawdc.
Summary: Bitsight's own post not in the results; secondary pages give 30,000+ for 27 January to 8 February 2026.

## D22 "Censys blog MCP servers exposed internet count 2026" (about 19:17)
Links: censys.com/blog/mcp-servers-on-the-internet/ (12,520 services on 8,758 IPs as of 28 April 2026, from a 24 April snapshot; a later note says more than 21,000 as of 6 May); backlist.sdan.io; adversa.ai (two); nhimg.org (two); doppler.com; boundev.ai; siliconangle (11 December 2025); knostic.ai (two); apify (two); wiz.io/blog/the-risk-hiding-behind-exposed-mcp-servers; byteiota; pluto.security; mcpplaygroundonline.
Summary: Knostic 1,862 (Shodan); Trend Micro 1,467.

## D23 ""Hermes Agent" exposed instances internet scan OR "Open WebUI" exposed instances 2026 count" (about 19:18)
Links: hexnode (two); bleepingcomputer (Hermes agent, Thai finance ministry); thehackernews.com/2026/07/hacker-runs-hermes-ai-agent-unattended.html; letsdatascience; cryptika; aiweekly; decryptiondigest; hackmag; craftedsignal feeds; hendryadrian; borncity; buttondown witcheer; theoutpost; Open WebUI results (letsdatascience; pulse.bot; securityscientist; cvefeed; bitsight groma pages; techradar; ionix; akaoma; imfht).
Summary: Hunt.io's banner search for the Hermes web panel, about 5,900 scan events over a month to 23 July 2026, sightings not distinct hosts; Open WebUI 17,000 (Shodan, reported March 2026) and 12,000 (cryptomining report).

## Design read (touches no count)
- Anthropic, "self-replicating AI", https://www.anthropic.com/research/self-replicating-ai, read with WebFetch (extract) about 19:08: the testbed's vector is "an ADB port open without authentication"; devices named include off-brand Android TV boxes, smart appliances, AI-enabled cameras, NAS boxes and mini-PCs; it cites Kimwolf's "over two million devices" (Synthient), an infection count, and a FOFA search for one reachable camera host; forecast "by the end of 2026". Used to fix the device class; it gives no exposure count for ADB.
