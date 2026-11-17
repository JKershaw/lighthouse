# LH055 round 2 discovery queries (four of four allowed; with round 1's six, the pilot's ten are now used)

Run by a Claude Opus 5.5 subagent for the Claude Code driver of run 2026-11-17T202935Z-anthropic-artex (row LH055-r2-record), through the harness's WebSearch tool, mode "extended", one at a time. The tool returns result titles and URLs plus a model-written summary. The summaries are search metadata: leads, not sources, and nothing below is evidence for a claim. "Opened" means fetched under the brief by studies/LH055/scripts/collect.py into this directory (fetch_log.jsonl). Results not opened were not read. Times are `date -u` read immediately before each query; the next reading bounds its end.

## Q7 (round 2 query a), 2026-11-17T21:22:49Z to before 21:23:00Z
"Amazon MadPot ARTEX agents decoy LLM inference backends "model gateway" stolen keys"
Purpose: any Amazon statement on how its decoys came to be used as inference backends, or on what "the framework's own model gateway" is.
Results: aws.amazon.com/blogs/security/amazon-threat-intelligence-observes-threat-actors-running-cybercrime-campaigns-with-artex-ai-agents/ (S02, already retained); brandefense.io/security-news/artex-ai-provider-key-campaign/; qz.com/amazon-ai-agents-steal-provider-keys-artex-111626; securityaffairs.com/203188/ai/artex-how-cybercriminals-use-ai-agents-to-scale-their-attacks.html; thestack.technology/amazon-spins-up-ai-honeypot-grabs-full-artex-powered-attack-chain/; tbreak.com/ai-agents-hunt-litellm-dify-api-keys/; thenextweb.com/news/fbi-artex-ai-hacking-tool-amazon-barracuda; finance.biggo.com/news/80f9cdce-7859-44ee-bacd-8487d85cb932; explainx.ai/blog/amazon-madpot-artex-agent-memory-decoy-llm-api-2026; aichatdaily.com/ai-security/amazon-says-chinese-nexus-hackers-ran-artex-ai-agents.
Summary (lead only): restates S02; names no Amazon statement beyond it. The summary says sources disagree on whether Amazon's post is dated 13 or 14 November.
Opened: The Stack (R05), because its title ("spins up") suggested it might carry an Amazon comment beyond the post. The others are secondary and were not opened.

## Q8 (round 2 query d), 2026-11-17T21:23:00Z to before 21:23:09Z
"ARTEX stolen AI keys self-sustaining loop new research telemetry November 2026 -Amazon independent confirmation"
Purpose: whether reports after 13 November that describe the loop cite telemetry of their own or only Amazon.
Results: therecord.media/artex-ai-tool-fbi-flash-alert; aws.amazon.com (S02); gbhackers.com/hackers-llm-api-keys-artex-ai-agents/; webpronews.com/fbi-flash-alert-artex-ai-agent-cyberattacks; aviatrix.ai/threat-research-center/artex-ai-agents-credential-theft-kyc-deepfake-2026/; explainx.ai (as Q7); archyde.com/fbi-says-artex-ai-tool-is-automating-cyberattacks-at-machine-speed/; aichatdaily.com (as Q7); techtimes.com/articles/330784/20261116/....
Summary (lead only): the tool says it dropped the "-Amazon" operator; it reports that every account of the loop it found traces to Amazon, and gives Check Point's 2,557 and 1,608 panel figures (a lead, already known from L-0091).
Opened: none from this list. The dependence check instead opened two post-13 November items already returned by Q7 or round 1's Q4: The Stack (R05, 16 November) and Equixly (R04, 16 November, an outcome-verification analysis named in round 1 as the lead for this audit). Both are secondary and count against round 2's eight documents.

## Q9 (round 2 query b), 2026-11-17T21:23:09Z to before 21:23:23Z
"stolen LLM API keys abused through New API OR "One API" OR CLIProxyAPI gateway victim incident report unexpected spend ARTEX"
Purpose: a victim-side or provider-side account of stolen LLM keys consumed through a gateway tied to ARTEX.
Results: dev.to/anoymask/llmjacking-stolen-credentials-fuel-llm-access-resale-and-1m-in-cumulative-charges-2i8e; aws.amazon.com (S02); gbhackers (as Q8); qz.com (as Q7); secnews.gr/en/751482/litellm-dify-ai-agents-klopi-api-keys/; securitybrief.asia/story/google-warns-of-llmjacking-spike-hitting-firms-hard; dev.to/hackerme/exposed-api-keys-how-ai-agents-now-hunt-them-on-websites-and-ai-apps-12bc; thehackernews.com/2026/11/amazon-uncovers-ai-agent-campaign.html; finance.biggo.com (as Q7).
Summary (lead only): no victim incident report ties spend to New API, One API or CLIProxyAPI; CLIProxyAPI appears in no result. It points to a Google report of about early November on "LLMjacking", in which, by the summary, an actor linked to new-api and gcli2api pooled stolen keys; that report is not tied to ARTEX in the summary.
Opened: none (all secondary; no victim or provider account returned).

## Q10 (the optional fourth query, used because a Google primary report could have been a second origin for gateway pooling of stolen keys), 2026-11-17T21:23:23Z to before 21:23:56Z
"Google Threat Intelligence LLMjacking new-api gcli2api stolen API keys pooling report"
Purpose: the URL of Google's primary report, needed before it could be read.
Results: siliconangle.com/2026/11/02/google-finds-llmjacking-attackers-running-up-100k-a-day-in-fraudulent-cloud-charges/; csoonline.com/article/4243863/enterprises-pay-100000-a-day-for-ai-they-never-ordered.html; dev.to (as Q9); gbhackers.com/google-warns-of-llmjacking-attacks/; securitybrief.news/story/google-warns-of-llmjacking-spike-hitting-firms-hard; mallory.ai/stories/01a19d06-f32b-743f-864c-6cccab545dc0; cyberpress.org/hackers-hijack-cloud-ai-models/; shattered.io/llmjacking-attacks-1-million-cloud-bills-mandiant-google-2026/; explainx.ai/blog/google-gtig-llmjacking-llm-mixers-1-million-stolen-cloud-ai-access-what-to-do-2026.
Summary (lead only): Google's threat intelligence group is said to report an actor it calls UNC6993 using new-api and gcli2api "likely to pool stolen keys", "LLM mixers" that resell unauthorised model access, and charges above $100,000 a day in some cases. None of these figures is evidence here. No result ties the report to ARTEX.
Opened: none. Google's own URL was not returned, and guessed paths are not evidence, so the primary report stays unread; it is a lead for the horizon intake (brief: up to four prospective documents if they could change a consequential claim).

## Documents fetched in round 2 (collector, one GET each)

R01 to R05 at 2026-11-17T21:23:56Z to 21:24:01Z; R06 at 21:26:04Z; R07 at 21:26:48Z. Candidate URLs came from links inside retained bodies (R01, R02, R03 from S03 or S07; R06 from R05; R07 from R06) or from query results (R04 from round 1's Q4, R05 from Q7). Seven of the eight allowed; one left unused.
