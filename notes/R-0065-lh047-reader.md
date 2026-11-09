# R-0065: LH047 reader and inference review

## What a reader would believe, written before reading the record

**Principal finding, said back.** Websites ask bots to behave in many ways, but almost nothing enforces those asks. Outside measurements of how well AI crawlers obey disagree, partly because some AI companies (OpenAI, Google, Perplexity) say robots.txt does not cover fetches a user asks for, while Anthropic says its bots honour it. When Lighthouse checked itself over about an hour and a half on 8 November 2026, roughly one request in twenty (172 of about 3,500) broke a rule, far more than the 2 it knew of. Most were reads of PyPI's JSON interface, which PyPI both documents for programs and asks crawlers to avoid, and one reviewer's requests under an anonymous name. Since 9 November every collector checks robots.txt first.

**Observed, explained, caused.** Observed: the request counts, the breakdown, and what the operators' pages say. Explained: the disagreement between published figures is put down to counting different things and to the user-fetch exemption (labelled interpretation). Caused: the faults are attributed to collectors and agents that never read robots.txt; a reader would take the fix as having stopped them.

**Limits a reader would notice.** It is one short evening, a floor, and Lighthouse grading itself. "As our brief fixed it" signals the rule is Lighthouse's own reading, and a second rule gives 191. The page's note that 184 verdicts rest on robots.txt files re-read afterwards is easy to miss and would surprise a reader. A reader might still take "broke a rule" as harm done to sites, and might read the Anthropic contrast as a verdict that Anthropic behaves better, which nothing here measures.

## Stage 2: after reading the record

Read: studies/LH047/ (LH047.md 0.2, brief.md, catalogue.md in part, for-driver.md, searchlog.md, data/audit/requests-judged.csv, summary.json and tables.md, the TollBit and Anthropic copies under data/reads/), the investigation page and programme.md's Next. Counts below are mine, from requests-judged.csv.

**Against the pre-reading.** The measurements hold up: the population, the per-rule counts and the provenance of each verdict are in the table and reproduce. What a reader would carry away goes further than they do in four places: what "broke a rule" means, the 61, the Anthropic contrast, and why the published figures disagree.

## What the round establishes

- On 8 November, 18:57 to 20:26 UTC, at least 3,497 Lighthouse requests were found, and the faults cluster in practices, not in scattered requests: one collector that reads no robots.txt (LH041, 85 PyPI requests in one minute), one reviewer's User-Agent (61), and a handful of others. Many of Lighthouse's own readers did not read robots.txt first, LH042's fetched when robots.txt was unreachable, and LH044's cut it at 64 KiB. Those findings are solid and stated plainly.
- Part A's catalogue: most of the rules are requests that nothing enforces. Part B: the published figures come from different cohorts and definitions and cannot be pooled.
- The worry about re-read files is small for the headline. Of the 172, 9 rest on a current re-read and 3 on a same-study copy read after the request. The PyPI copy that decides 89 was read at 19:19:52, before LH041's PyPI requests (19:32), though after two of the other four. Of the 19 that only reading B adds, 8 rest on current re-reads (BleepingComputer four times, declawed.io three times, Penligent once).

## Material claim problems

1. **About a third of the headline is a class made after the result was seen, and the headline does not say so.** In short, the Answer and the investigation page say "172 broke a rule as our brief fixed it". The brief's R8 says a User-Agent does not comply only if "it claims to be a browser". `Mozilla/5.0 (compatible; research-reader/1.0)` has the same shape as LH044's `Mozilla/5.0 (compatible; Lighthouse-research/1.0; ...)`, which complies. F7 and tables.md say it was "classed after it was seen", but that label never reaches the summaries. 59 of the 172 fail on nothing else, so under the brief as fixed the count is 113, with those 59 left unclassified. *Why it matters:* this is a reading chosen after the outcome was seen, inside a figure presented as fixed in advance. *Replace with:* "113 broke a rule as our brief fixed it; 59 more, all from one reviewer whose User-Agent named no one, we classed as failures after seeing them, for 172." Make the same change on the investigation page.
2. **A count of requests reads as a count of misdeeds or of harm.** "172 broke a rule ... against 2 we already knew of" invites "86 times worse than we thought". Of the 172, 90 got HTTP 404, including 88 of the 89 PyPI "reads", so nothing was read. 145 come from two practices. 9 of the 11 Crawl-delay breaches exist only because the brief counts a robots.txt read as a request, which the Limits section says most sites probably don't mean. The 5 `use=reference` verdicts are about keeping pages, not about requests, under a field Cloudflare calls experimental. *Why it matters:* the planned paper will reach readers who will take "broke a rule 172 times" as 172 incidents of harm. *Replace with:* "172 requests, from about seven practices, broke a rule; most were refused or found nothing (90 got 404), and none retried a wall or hid after refusal." Say "requests to PyPI's JSON interface", not "reads".
3. **Wording easier on Anthropic than on others.** In short: "OpenAI, Google and Perplexity ... say robots.txt may not apply ..., while Anthropic says its bots honour it." This sets one operator's self-description against the others' as though the two were comparable evidence. Meanwhile the Answer's part B names Anthropic only where the evidence is favourable (ClaudeBot among the seven that obeyed). The evidence that is unfavourable or unclear stays in the Findings and is never summarised: TollBit's 12.7% spoofing for Claude-User, Cloudflare's "effectively unclear", Reddit's suit. Correction 5 left the Answer "as it stands". Anthropic's page also excludes Claude-Agent, and nothing here measures Anthropic's fetchers. *Replace with:* "...say robots.txt may not apply to fetches a user asks for; Anthropic's page says its bots honour it. Lighthouse runs on Anthropic's models, and the published evidence on Anthropic's bots is mixed (part B)." Add one sentence to the Answer's part B giving the Claude-User spoofing figure and Cloudflare's "effectively unclear" alongside ClaudeBot.
4. **"By TollBit's own breakdown" claims something the text read does not show.** The Reading across says "much of that share, by TollBit's own breakdown, is user-triggered fetchers". TollBit gives a bypass rate per bot, not how the 15% splits between bots, and two of its three highest (Bytespider, PerplexityBot) are crawlers, not user-triggered fetchers. The same paragraph says the share "has grown since late 2024", which is the comparison across cohorts that the Answer itself flags. *Why it matters:* this is the explanation of the disagreement the paper will most want to repeat. *Replace with:* "TollBit's highest per-bot bypass rate is a user-triggered fetcher (ChatGPT-User, 54% of its scrapes), whose operator says robots.txt may not apply; how much of the 15% such fetchers make up is not in the text read." Apply the same check to catalogue.md's "Operators of user-triggered fetchers read the protocol as not covering them at all". OpenAI says "may not apply", Google and Perplexity say "generally ignore", and Anthropic says the reverse.
5. **Stale public figure.** programme.md's Next still says "185 of 3,497 broke a rule", and so does for-driver.md, which also still says "LH042 read six arXiv pages 2 seconds apart" (0.2 says 2 requests). *Replace* these with the 0.2 figures, as amended under problem 1.

The PyPI line "A tension between two of the operator's own statements, not a hidden act" is softer on Lighthouse than it needs to be. "Not a hidden act" is a defence the record does not offer anyone else; drop it.

## Readability suggestions

- Next to "184 verdicts rest on a file re-read afterwards" on the investigation page, add "(9 of the 172)". The reader's worry is about the failures, and the answer is reassuring.
- In short packs four clauses of qualifiers into one sentence. Split it: the rules; the published evidence; our own count; what we changed.

## Next-step recommendation

Correct problems 1 to 5 as record 0.3 before drafting the paper, and update the investigation line and programme.md to match. The paper can then go ahead. The re-audit of a later week is worth doing, after the shared fetcher is in place. Before the week is read, a dated amendment should fix R8's class for a name that is neither Lighthouse's nor a default, settle how Crawl-delay is counted, and report by practice as well as by request. The fetcher should keep each robots.txt copy at the time of the request, so the re-read limit goes away.

The paper must not say or imply:
- that Lighthouse "broke the rules 172 times" as incidents or harm;
- that the 61 broke a rule fixed in advance;
- that it "read" PyPI's interface 89 times;
- that Anthropic's bots comply, or comply better than OpenAI's, Google's or Perplexity's;
- that TollBit shows bypassing rising from 3% to 15%;
- that user-triggered fetchers make up most bypasses;
- that every verdict rests on the robots.txt in force at the time.
