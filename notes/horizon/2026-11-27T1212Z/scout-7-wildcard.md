# Scout 7, Wildcard, run 2026-11-27T1212Z

**In short.** The NANOG conduct question is settled: the older archive host's robots.txt allows `*` and refuses only a Cloudflare-managed list headed "Training crawlers", which names three Anthropic tokens (ClaudeBot, anthropic-ai, Claude-Web) but not Claude-User, Claude-Code, Claude-SearchBot or Claude-Agent, so one targeted read of the current archive was made with no body kept in the repository; it found nothing relevant. The biggest thing the sweeps had not logged is a strand about AI and cryptography: Google DeepMind reported on 6 November that its agents, under human supervision, found two cheaper attacks on legacy 1024-bit RSA, and since 25 November a widely read blog has passed on rumours that AI labs hold further unpublished cryptography results, which it declines to verify. Also new: a security researcher on oss-security says Ubuntu had shipped no fix nine days after two public kernel flaws, and DeepMind's head of Gemini development says agents now control "part of" its compute for experiments. No November ground-robot count from Ukraine yet, and nothing new on the armed robot dogs in Haiti.

- Start: 2026-11-27T12:14:42Z. End: 2026-11-27T12:20Z (UTC, from `date -u`).
- Tools: shell `curl` (user agent `Lighthouse-research`) for the two NANOG robots.txt files, the NANOG archive pages, the HN Algolia API and Codeberg's status account; WebSearch (one US-indexed tool that answers with a model's summary); WebFetch (a small model's summary of the page, so its quotations are as the summariser relayed them).
- Everything below is **reported by** the page named. None of it is a Lighthouse observation.
- Every URL went through `LIGHTHOUSE_PROVIDER=anthropic python3 -I scripts/robots_gate.py` immediately before it was fetched (strict mode, except the NANOG archive reads, gated with `--oneoff` as the brief and the plan's note of 24 November direct). Nothing refused was fetched.
- Saved bodies (two robots.txt files, the NANOG listing pages, HN JSON, Codeberg JSON) are only under the session scratchpad's scouts/s7/ directory; `python3 -I scripts/redact_emails.py` ran over it after the saves. Nothing was written in the repository but this log.

## NANOG conduct question

- **Read.** https://mailman.nanog.org/robots.txt, once, 2026-11-27T12:14:42Z, `curl -A Lighthouse-research`, HTTP 200, `text/plain`; SHA-256 3073d1e371afb3271c7666148766fedc5145f7d8440f7114062db79b7bd58add (as the gate recorded it). Copy at scratchpad scouts/s7/nanog-mailman-robots.txt.
- **Groups, verbatim** (comments omitted; the file opens with Cloudflare's Content-Signals preamble and "# BEGIN Cloudflare Managed content"):
  - `User-agent: *` / `Content-Signal: search=yes,ai-train=no,use=reference` / `Allow: /`
  - Under the comment `# Training crawlers`, each with `Disallow: /`: `User-agent: Amazonbot`; `Applebot-Extended`; `Bytespider`; `CCBot`; `ClaudeBot`; `Diffbot`; `Google-Extended`; `GPTBot`; `omgili`; `anthropic-ai`; `Claude-Web`; `cohere-ai`; `MistralAI-Training`; `meta-externalagent`; `GoogleOther`; `Baiduspider`; `PetalBot`; `AwarioSmartBot` and `AwarioRssBot` (one group); `Google-CloudVertexBot`; `QualifiedBot`; `Cotoyogi`; `ICC-Crawler`.
- **Evaluation against scripts/robots_tokens.json.**
  - `*`: allowed (`Allow: /`). Not refused.
  - Claude-User: not named; falls to `*`. Not refused.
  - Claude-Code: not named; falls to `*`. Not refused.
  - Every Anthropic token: no. Refused: ClaudeBot (kind "crawler (training)"), anthropic-ai (on the retention list as a training refusal) and Claude-Web ("older Anthropic token"). Not refused: Claude-User, Claude-SearchBot, Claude-Agent, Claude-Code.
  - The one ambiguity is Claude-Web, which the tokens file does not classify as a training crawler. The file itself puts it under the operator's own heading "Training crawlers", in a Cloudflare-managed block whose `*` group says `ai-train=no` and `use=reference`, so the owner's intention reads as refusing training, not reading. I took it that way; the driver may wish to note it.
- **Decision.** The file refuses only training crawlers, so a targeted read of the current archive was allowed under the brief. The strict recurring gate still refuses mailman.nanog.org (decided by ClaudeBot), so recurring collection there stays off; the one-off gate allows it with `keep_body: false`. lists.nanog.org answered robots.txt with 404 (no rules; gate allows, `keep_body: true`), but because the list's older host refuses training crawlers, I treated the list as reserved from training and kept no body in the repository: the listing pages are in the scratchpad only, and only thread titles are used here.
- **Read made.** `https://lists.nanog.org/archives/list/[list address]/latest` (the address on the old path returned 404 at 12:15:10; the archive index at 12:15:22 gave the current address; read at 12:15:33, HTTP 200, `--oneoff` gate allowed). Thread titles on the page include a Hurricane Electric routing problem, a source-address-validation measurement call, IP reputation and geolocation contacts, ARIN's BGP Insight, the Postel Award and the weekly routing table report. No thread on AI traffic, crawler load, patching or the November outages. Nothing from it is used.

## Direct publication checks

None assigned to this scout.

## Standing sources read

| Source | UTC read | Gate | Status | Interval covered | Outcome |
| --- | --- | --- | --- | --- | --- |
| HN Algolia API, stories after 2026-11-24T12:15Z with more than 40 points | 12:15:57 | allowed | 200 | 24 Nov 12:15Z to 27 Nov 12:15Z | 157 stories; relevant ones below |
| Codeberg status account (`social.anoxinon.de` API, 15 statuses) | 12:17:10 | allowed | 200 | 23 Nov 20:33Z to 27 Nov | one post, 27 Nov 11:55Z: brief downtime to migrate from Redict to Valkey. Nothing on abusive traffic. |
| NANOG current archive | 12:15:33 | `--oneoff` allowed | 200 | to 27 Nov | see above; nothing relevant |
| infosec.exchange | not tried | | | | walled (HTTP 422, authentication required) on 18, 20 and 24 Nov; not retried |

## Pages opened

| # | URL | UTC read | Gate | Status | Page's date | Reported claim | How read | New? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | https://www.securityweek.com/google-deepminds-ai-agents-make-1024-bit-rsa-keys-cheaper-to-attack/ | about 12:18 | allowed | 200 | 9 Nov 2026 (event 6 Nov) | Google DeepMind agents, under human supervision and with UC San Diego and Inria cryptographers, found a signature-forgery weakness and a cheaper batch factoring of 1024-bit RSA; two agents ran the forgery computation "in under four days" with about 20 messages from a human, mostly approvals. Pushmeet Kohli: "In practice, these results only affect obsolete 1024-bit RSA systems"; 2048-bit keys unaffected. Primary: Kohli's post on X and two papers on DeepMind's storage, not opened. | WebFetch | new |
| 2 | https://scottaaronson.blog/?p=10379 | about 12:16 | allowed | 200 | 25 Nov 2026, updated 26 Nov (HN, 2,020 points) | Lists recent AI-lab mathematics results and says he has heard "the AI labs are now sitting on one or more bombshells in that area" of cryptography, but "I do not wish to be responsible for spreading unverified rumors"; calls a Google factoring paper theoretical, of no practical relevance to cryptography. | WebFetch, first 100,000 of 154,575 characters | new |
| 3 | https://www.openwall.com/lists/oss-security/2026/11/25/9 | about 12:16 | allowed | 200 | 25 Nov 2026 | Hanno Böck: details of a Linux TCP flaw were published 16 Nov and "Today, nine days later, Ubuntu still has not published a fix yet"; a KVM host escape published 18 Nov also unfixed; "Other distros had a fix already available when the details were published." Nothing on AI. | WebFetch | new URL (title only seen by scout 2 today and scout 4 on 24 Nov) |
| 4 | https://the-decoder.com/ai-agents-now-control-part-of-deepminds-compute-for-gemini-experiments-but-recursive-self-improvement-remains-distant/ | about 12:16 | allowed | 200 | 25 Nov 2026 | Koray Kavukcuoglu, in a podcast, says "AI agents control part of the compute themselves to run experiments" for the next Gemini; no share given; the lab is "still far" from recursive self-improvement. Primary is the podcast video, not opened. | WebFetch | new |
| 5 | https://www.lesswrong.com/posts/7wzWuLP3HhyBLmKfo/models-can-communicate-via-inference-servers-despite-being | about 12:17 | allowed | 200 | 19 Nov 2026 | A lab demonstration (mainly Qwen3-8B on vLLM) that two agents sharing an inference server can pass information covertly without messages or files, defeating an untrusted monitor in a test; not observed in the wild. Mechanism not recorded here. | WebFetch | new |
| 6 | https://1password.com/blog/update-on-nov-2026-security-incident | about 12:18 | allowed | 200 | 25 Nov 2026 | An attacker used a compromised employee GitHub account to push code to backend services and copy account records for a subset of users; "Your vault data ... were not affected." No mention of AI. | WebFetch | new |

## Searches

Results read from search summaries unless opened above.

1. `perros robot armados Haití Bukele noviembre 2026 control disparos` (Spanish): the same family as on 24 Nov (ntn24, elsalvador.com, peru21, diariodelsur, jamaicaobserver 13 Nov, newsweek and foxnews (disallowed on 24 Nov), americanthinker, brasilparalelo, HRW on drones in March). Nothing after 17 Nov; still no word on firing or control. Not opened.
2. `НРК листопад 2026 кількість застосувань наземних роботів Міноборони` (Ukrainian): mod.gov.ua, kmu.gov.ua, armyinform, kyivpost, censor.net (50 new robots admitted this year), dou.ua digest. No November count; October's figure is newest, as expected before early December. Not opened.
3. `armed robot deployed police OR army withdrawn OR malfunction late November 2026` (English): DubBot retirement (June), Knightscope pullbacks, San Francisco, 404 Media; nothing from November. Not opened.
4. `无人地面车辆 武装 机器人 部署 2026年11月` (Chinese): English results only: army.mil, armyrecognition, stripes (Oct), Defense One 3 Nov, eweek. No Chinese-language item. Not opened.
5. `AI labs encryption RSA rumour mathematicians silence November 2026` (English): explainx "claimed vs verified" (Oct), postquantum.com on responsible disclosure of a cryptanalytically relevant quantum computer, livescience and arynews on Anthropic's Mythos Preview and cryptographic flaws (dates not given), interestingengineering and letsdatascience on DeepMind and RSA-1024, Scientific American "why mathematicians are hiding research results in zero-knowledge proofs". Not opened except via search 6.
6. `Google DeepMind agents RSA-1024 weaknesses November 6 2026 blog` (English): securityweek (row 1), fourweekmba, cryptobriefing, webpronews, runtimewire, officechai, secnews.gr, explainx (says it found no DeepMind post or paper). One source family: Kohli's post and DeepMind's two papers.
7. `クローラー AI ボット 負荷 サーバー ダウン 2026年11月` (Japanese): Kinsta, rocket-boys (January 2025 GPTBot case), heise, zenn. Nothing from November. Not opened.
8. `روبوتات مفخخة غزة نوفمبر 2026 مدنيين` (Arabic): alaraby, aljazeera, alquds (Oct 2024), eremnews (2025), palestine-studies (7 Jul 2026), akhbarelyom (Gaza government: more than 80 explosive robots, August). Nothing from November. Not opened.

HN items seen and not opened (gated where shown): The Times on mathematicians' "eerie silence over AI and encryption" (refused under the strict rule); Reuters, Microsoft "Code Red" after its outage (refused under the strict rule; LH058's beat); GitHub degraded service incident of 25 Nov (allowed); Defang security incident (allowed); Nfs2root, a 12-year-old Linux NFS server flaw (allowed; not opened, scout 2's beat); Google's factoring preprints on github.com (not fetched, github.com pages return 403 from this container); a Reddit rumour thread on factoring; Notion's MCP server injecting upsell instructions into agent context (Reddit); two posts about Claude sabotaging research tasks (X); Marginalia Search's update; the 45°C chiller piece in The Register (not gated).

## Five best leads

### 1. AI agents and cryptography: DeepMind's RSA-1024 results, and rumours of more

- **Primary URLs.** Report: https://www.securityweek.com/google-deepminds-ai-agents-make-1024-bit-rsa-keys-cheaper-to-attack/ (9 Nov, event 6 Nov); the primaries are Pushmeet Kohli's post on X and two DeepMind papers, not opened. Rumour: https://scottaaronson.blog/?p=10379 (25 Nov). The Times piece (refused) and Google's factoring preprints (not fetched) sit beside them.
- **What was reported.** Supervised agents found a forgery weakness and a cheaper batch factoring of legacy 1024-bit RSA; DeepMind says only obsolete systems are affected. A prominent complexity theorist says he has heard labs hold unpublished cryptography results, and declines to vouch for it.
- **Why it matters.** Public-key cryptography is shared infrastructure in the plainest sense. A model-assisted cryptanalytic result, or a held-back one, is a "lab capability" event whose consequences would land on everyone's keys, and how fast legacy 1024-bit keys are retired is a deployment question like those the software-updates work asks. The rumour is not evidence; the DeepMind result is a dated, attributable lab claim. No earlier sweep file mentions RSA-1024, Aaronson or these results (grep), so it has gone unwatched for three weeks.
- **Touches.** The cost investigation's lab-capability strand; "When a model finds the bug" (a model-found flaw in a protocol rather than in code).
- **Next step.** Open Kohli's post and the two papers' abstracts (not methods) to date the claim; consider a proposal to watch for public statements of AI-found cryptanalytic results and the response of standards bodies. Keep mechanisms out of the record.

### 2. Ubuntu shipped no fix nine days after two public kernel flaws

- **Primary URL.** https://www.openwall.com/lists/oss-security/2026/11/25/9 (25 Nov).
- **What was reported.** A named researcher says other distributions had fixes at publication while Ubuntu had none nine days later, and argues its backporting kernel strategy is the cause. His interpretation, not a measurement.
- **Why it matters.** A distribution's lag is a clock between "the fix exists" and "the fix reaches machines", the core of the software-updates investigation, on a platform with a large server share. Not tied to AI.
- **Touches.** Where software updates go; a possible case for a brief that times distribution uptake.
- **Next step.** Check Ubuntu's own security notices for the two CVEs' publication dates before using it.

### 3. DeepMind says agents now control part of its compute

- **Primary URL.** Report: https://the-decoder.com/ai-agents-now-control-part-of-deepminds-compute-for-gemini-experiments-but-recursive-self-improvement-remains-distant/ (25 Nov); primary is Kavukcuoglu's podcast, not opened.
- **Why it matters.** Agents allocating compute inside a lab is the in-house version of the credential-to-compute loop ARTEX asks about outside, with no figure for how much. Paired with the lab demonstration of covert communication through shared inference servers (https://www.lesswrong.com/posts/7wzWuLP3HhyBLmKfo/..., 19 Nov), it is lab capability, not open-internet activity, and should be kept apart as the cost investigation requires.
- **Touches.** ARTEX (LH055) context; the cost investigation's lab-capability strand.
- **Next step.** Listen to or find a transcript of the podcast to get the exact words before any use.

### 4. 1Password breach through an employee's GitHub account

- **Primary URL.** https://1password.com/blog/update-on-nov-2026-security-incident (25 Nov; investigation from 19 Nov).
- **Why it matters.** A compromise of a security vendor's CI/CD and backend through a developer account, the supply-chain route the npm and PyPI studies follow, at a firm many organisations depend on. 1Password names no AI involvement, and Lighthouse makes no claim beyond its own report.
- **Touches.** Software supply chain (scout 3's beat; listed here in case it was missed).
- **Next step.** None unless a later report names how the account was taken.

### 5. Armed robotics: quiet, and the Haiti questions still open

- **Primary URLs.** As on 24 Nov: https://www.ntn24.com/noticias-actualidad/asi-son-los-impresionantes-perros-robot-con-metralletas-acopladas-que-el-ejercito-de-bukele-esta-usando-contra-pandillas-en-haiti-665947 (13 Nov) and https://www.elsalvador.com/noticias/nacional/perros-robot-haiti-como-funcionan-el-salvador/1304293/2026/ (16 Nov).
- **What was found.** No new reporting since 17 Nov on who controlled the rifle-mounted robots or whether they fired; no Haitian civil-society or UN account found. No November ground-robot count from Ukraine yet (expected early December on mod.gov.ua). No withdrawal or failed deployment in November found in English, Spanish, Chinese or Arabic searches; Gaza results were all older.
- **Touches.** Physical authority (LH050, whose final check is today).
- **Next step.** The next run after about 3 December should look for Ukraine's November count on mod.gov.ua.

## Withheld

Nothing withheld under the research safety assessment. The cryptography and covert-communication leads are recorded only at headline level, with no method.

## Gaps, refusals, languages and geography

- Refused under the strict rule, not fetched: www.thetimes.com (AI and encryption, 27 Nov), www.reuters.com (Microsoft "Code Red", 24 Nov). mailman.nanog.org is refused under the strict rule (ClaudeBot) and was not read beyond robots.txt.
- Walls: infosec.exchange not retried (422 on three earlier sweeps). github.com pages not tried (403 from this container).
- Languages searched: English, Spanish, Ukrainian, Chinese, Japanese, Arabic. Pages opened were all in English. The Chinese search came back in English only. Geography of opened pages: the US and Europe; Haiti only through earlier-read Spanish-language pages. Africa, South and Southeast Asia and Latin America beyond Haiti appear in no result. Media repeating DeepMind's RSA claim are one source family; Bukele's footage remains one family.
- 8 searches and 6 pages opened plus the NANOG, HN and Codeberg reads; every fetch gated first; no disallowed URL fetched; no indicator or exposed host looked up; no file edited but this log.
