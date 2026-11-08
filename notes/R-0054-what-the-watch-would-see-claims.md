title: Claims check of the draft essay "What the watch would see of a pattern that copies itself"
kind: review note (check of figures and citations), unreviewed
date: 2026-11-08
authors: a claims-checking subagent (Claude Code, Opus 5.5) for the driving session of 8 November 2026; it did not write the essay
piece: essays/what-the-watch-would-see.md (status draft), its figure essays/what-the-watch-would-see/traces.svg and script draw_traces.py

**In short.** We checked every figure, date, quotation and attribution in the draft essay against its source, read afresh from the source itself, together with every absolute, every label and the keeper's caution rules of 8 November. The main figures hold: the OSV subtraction gives 8 days 2.6 hours, 282 of 291 matches the released piece, and 35,024 out of 109 million is 3.2 in ten thousand. Twenty-odd passages were corrected. The essential ones: a misquotation of our own piece, a date ("this summer") that Anthropic does not give, two timings no source states, an outside account relayed under the wrong author, "poisoned" said in our own voice, and several absolutes that went past their sources. The figure was corrected to match. No must-fix item remains. The essay goes next to the reader-and-inference review, then one recheck.

## What we read

Every source was fetched once by this checker on 8 November 2026, using curl with User-Agent "Lighthouse-research/1.0 (+https://lighthouse.harbour.cat)". HTML was converted to text offline with a stdlib parser (`python3 -I totext.py`) and read as text. The small JSON bodies and the subtraction script are kept in [essays/what-the-watch-would-see/claims-check/](../essays/what-the-watch-would-see/claims-check/), with fetch-log.tsv. The larger HTML bodies stayed in the session scratchpad and are recorded here by hash (SHA-256 of the body as fetched).

| Source | URL | UTC read | HTTP | Bytes | SHA-256 |
| --- | --- | --- | --- | --- | --- |
| Anthropic, three incidents, 30 Jul 2026, updated 3 Aug | https://www.anthropic.com/news/investigating-incidents-cybersecurity-evals | 19:12:21 | 200 | 194793 | eb53ffc334d873eac9529c8fe7d11e729500c468384d0ed3ffb0faeff6186615 |
| UK AISI incident report, 4 Aug 2026 | https://www.aisi.gov.uk/blog/incident-report-unsanctioned-agent-behaviour-during-cyber-testing | 19:12:21 | 200 | 41426 | 70a5dc2a751cc4bcd286e2180d4ec4f9dd695281032dbcce605bbd6850a8f71b |
| METR and Redwood Research, 26 Aug 2026 | https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/ | 19:12:22 | 200 | 437174 | 37ec7c48dc11ba00e048e079b161e99d4cdf7c279ed6d0290a0494c81d9a740f |
| StepSecurity, 11 May 2026 | https://www.stepsecurity.io/blog/mini-shai-hulud-is-back-a-self-spreading-supply-chain-attack-hits-the-npm-ecosystem | 19:12:22 | 200 | 254439 | c43a863c4b9deeed8da5db489648474edc7426b8a77f966f43a9f82d970f0e60 |
| BleepingComputer (Toulas), 4 Aug 2026 | https://www.bleepingcomputer.com/news/security/massive-chaindrop-npm-supply-chain-attack-infects-hundreds-of-packages/ | 19:12:22 | 200 | 95422 | 8c7e59738f485426a71472d53e10105120da6aa5d3f3484bdd0d1ce9be6a9e65 |
| Cloud Security Alliance, 31 Oct 2026 | https://labs.cloudsecurityalliance.org/research/csa-research-note-model-hub-reupload-agent-lures-20261031-cs/ | 19:12:23 | 200 | 121284 | 2292a5b2c106fc160af82f0b05c1ef51daf592eec416b7827451750c7ad6c509 |
| Anthropic Frontier Red Team, 12 Oct 2026 | https://www.anthropic.com/research/self-replicating-ai | 19:12:23 | 200 | 266015 | 094f193d9d2a1fae037a98a4925b753f8653611e12ba74b367f2b90e81cb93ab |
| OSV MAL-2026-2144 (API) | https://api.osv.dev/v1/vulns/MAL-2026-2144 | 19:12:23 | 200 | 6273 | ac1dc84549165df3a324a476824b2bde19dad8f4abef78ad568d7530876193a2 |
| PyPI JSON, litellm 1.107.0 | https://pypi.org/pypi/litellm/1.107.0/json | 19:12:23 | 404 | 24 | b82014934f66beeb9e05a37f65357c4b50db0349d25d68d818ed0319dd4feb40 |
| OSV query, litellm 1.107.0 | POST https://api.osv.dev/v1/query | 19:12:24 | 200 | 6285 | 01dc46680dc24457b5779e7c500ac2b6b1291ac2fef24a16c52253d0e424b49b |
| GitHub API, commit history of the OSV record's source file in ossf/malicious-packages | https://api.github.com/repos/ossf/malicious-packages/commits?path=osv/malicious/pypi/litellm/MAL-2026-2144.json | 19:14:49 | 403 | 378 | b3e03aaaff81d68730d67392a135ac3fdfdf022880c66632ab188d2fe084cda3 |

The GitHub request was refused, because the session's proxy does not enable that repository. It is recorded as unread, and we did not work around it. As a result we could not see when version 1.107.0 was first added to the record (see Findings, OSV). The OSV body matches the writer's in length (6273 bytes) but not in hash, and the API's key order differed between reads. The Anthropic incidents page also differed in length from the writer's copy. We read its text and found all the passages the essay quotes.

Lighthouse pages, read in the repository on 8 November 2026: charter.md (paragraph on self-replicating agents), design.md (the three layers, lines 15 and 115 to 121), articles/what-we-can-see.md, articles/where-software-updates-go.md, articles/tests-read-the-lockfile.md, studies/LH017/LH017.md (P2 and pair classes), articles/who-watches-the-internet.md, studies/LH035/LH035.md (version 0.3, Answer) and studies/LH035/sources.md (rows I22 to I25, I28, I29, I32), studies/LH043/LH043.md (version 0.1), studies/LH041/brief.md and studies/LH042/brief.md (openings), investigations/ai-cost-and-spread.md, and essays/it-was-only-a-test.md. The writer's notes (notes/what-the-watch-would-see-draft-notes.md) were used only to find things.

Not read: Island's, Aikido's and Pluto Security's primary research, which the essay cites only through CSA and BleepingComputer, as it says. Not read either: Anthropic's promised redacted transcript, Hugging Face's own pages, and the git history of the OSV record.

## What we checked

1. Every figure, date, quotation and attribution in the title, summary, prose, caption, alt text and notes, against the source as read above. Lighthouse's own figures were checked against the released piece or record each cites.
2. Every absolute (never, always, all, none, no record, every), first in the title and summary, then in the prose.
3. Labels: interpretation against finding, the scenario marked as a scenario, the post hoc reading, and attribution of each claim of harm or compromise.
4. Caution: the scenario and mechanisms stay at the level of traces; no route to evade detection, obtain credentials, persist or spread beyond the sources' own words; nothing re-identified.
5. The figure, rendered with the preinstalled Chromium headless shell in light and dark before and after the changes, against the prose. scripts/check_chart_style.py passes on the redrawn SVG.

## The OSV subtraction, reproduced

The script is kept as [claims-check/osv_gap.py](../essays/what-the-watch-would-see/claims-check/osv_gap.py). Replay it with `python3 -I essays/what-the-watch-would-see/claims-check/osv_gap.py essays/what-the-watch-would-see/claims-check/osv-MAL-2026-2144.json`; on 8 November that replay matched the output kept beside it exactly.

```python
import json, sys
from datetime import datetime, timezone
d = json.load(open(sys.argv[1]))
origins = d["database_specific"]["malicious-packages-origins"]
o = [x for x in origins if "1.107.0" in x.get("versions", [])]
print("origins listing 1.107.0:", [(x["source"], x.get("id"), x["import_time"], x["modified_time"]) for x in o])
def p(s):
    s = s.rstrip("Z")
    if "." in s:
        a, b = s.split("."); s = a + "." + b[:6]
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=timezone.utc)
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
up_early = datetime(2026,10,21,11,39,tzinfo=timezone.utc)   # "between 11:39 and 11:40 UTC" in details
up_late  = datetime(2026,10,21,11,40,tzinfo=timezone.utc)
for label, t in [("import_time", p(o[0]["import_time"])), ("origin modified_time", p(o[0]["modified_time"])), ("record modified", p(d["modified"]))]:
    for ul, u in [("11:39", up_early), ("11:40", up_late)]:
        g = t - u
        print(f"{label} {t.isoformat()} - upload {ul}: {g}  = {g.total_seconds()/86400:.3f} days")
```

Output:

```
origins listing 1.107.0: [('amazon-inspector', 'IN-MAL-2026-022275', '2026-10-29T14:14:39.386127062Z', '2026-10-29T14:11:39Z')]
import_time 2026-10-29T14:14:39.386127+00:00 - upload 11:39: 8 days, 2:35:39.386127  = 8.108 days
import_time 2026-10-29T14:14:39.386127+00:00 - upload 11:40: 8 days, 2:34:39.386127  = 8.107 days
origin modified_time 2026-10-29T14:11:39+00:00 - upload 11:39: 8 days, 2:32:39  = 8.106 days
origin modified_time 2026-10-29T14:11:39+00:00 - upload 11:40: 8 days, 2:31:39  = 8.105 days
record modified 2026-10-29T14:30:33.719516+00:00 - upload 11:39: 8 days, 2:51:33.719516  = 8.119 days
record modified 2026-10-29T14:30:33.719516+00:00 - upload 11:40: 8 days, 2:50:33.719516  = 8.118 days
```

Derived measurement: "about eight days" holds whichever of the record's three October 29 times is used (8.105 to 8.119 days). The upload window comes from the record's `details` text, not from a dated field. The OSV query for litellm 1.107.0 returned only MAL-2026-2144.

## What we found

Each item is an observation from the sources unless it is marked otherwise. "Must fix" means it broke a rule in AGENTS.md (a wrong figure or quotation, an invented timing, an unsupported absolute, a missing attribution or label); "suggestion" means it did not.

**Figures that hold.** The 15 systems; "roughly one hour"; the automatic removal by PyPI's systems; the review beginning Thursday 23 July after OpenAI's 21 July disclosure; "had not previously detected the activity" (Anthropic). Both AISI quotations, word for word, and the late-July dating (25 to 28 July). Roughly 1,200 agents and the 4 July outage (METR). The 11 May date, the spread across maintainers and the provenance sentence (StepSecurity). More than 1,300 and at least 868 (BleepingComputer, quoting Aikido for the second). About 7,600, more than 800, the July date, and assistants finding repositories without a link (CSA relaying Island). The flow-monitoring claim (Anthropic's red team, 12 October). The OSV upload window and import time. The PyPI 404. 282 of 291 (articles/tests-read-the-lockfile.md; LH017 P2: 282 of 291, 96.9 per cent). The 35,024 downloads and three in ten thousand (articles/where-software-updates-go.md: among 109 million; 35,024/109,000,000 × 10,000 = 3.2). The seventeen sources and the broker (articles/what-we-can-see.md). The cadences of Open Source Insights ("within an hour or so", for common packages), OSV ("15 minutes ... 99.5%"), npm (per version, 7 days), pypistats (180 days), GH Archive (hourly), PyPI's BigQuery table (streaming) and ClickPy (daily), all from LH035 rows I22 to I25, I28, I29 and I32. The two charter quotations. The design's typed link and derived measurement. LH043's placeholders finding (as an unreviewed record, labelled so).

**Must fix (all now fixed):**

1. *Misquotation of our own piece.* The essay quoted "every public record stops before a run". That string is not in articles/where-software-updates-go.md, which says "every public record stops at an edge ... None of them reaches a run".
2. *A date the source does not give.* "For about an hour this summer": Anthropic dates none of the three incidents individually, saying only "the earliest incidents date to April", and the PyPI package could have been published in spring. Also, "The earliest of the three incidents dates to April" turned Anthropic's plural into a singular.
3. *An unsupported timing and absolute.* "Those who knew were the lab that read its own logs, months later": the PyPI incident's date is unknown, so "months later" is unsupported. "Those who knew" also passed over PyPI's own systems, which removed the package.
4. *Invented timings.* "A rising count of packages that depend on a new one would show there within a day", and "within a day" again in the closing summary. No source gives this. Open Source Insights promises about an hour only for common packages and says quiet ones can be staler. The figure's "dependency graph: about an hour" had the same gap.
5. *An unsupported cadence.* "ClickPy and pypistats summarise it daily": LH035 records pypistats's update cadence as "not stated".
6. *Wrong attribution.* METR wrote that the 6 July fresh repository "wiped the cache and erased all messages", but as OpenAI's attestation ("which they attest"). The board it erased was also an earlier one, not the 1,200-agent board.
7. *Harm in our own voice.* "The poisoned release of LiteLLM" and "The poisoned LiteLLM release" called a named release compromised in Lighthouse's voice. AGENTS.md wants a claim of compromise attributed to its source.
8. *An absolute about what Anthropic has published.* "Anthropic has not published its package's name": only the 30 July post was read, and the promised redacted transcript was not.
9. *An overstated mechanism in Lighthouse's own figure.* The 282 of 291 counts workflows *set* to install from the pinned file. The released piece says "A workflow says what a job would do when it runs, not whether it ran, how often, or whether it fetched anything", and notes caches at 125 of the 282. The essay's "installed" and "would keep being fetched at every change" went past that. The post hoc reading also needed to name what would test it or say none can (AGENTS.md, lessons of the reviews).
10. *A wrong source.* "The explanations the charter asks to be tested first": "tested first" is design.md's wording, not the charter's.
11. *A missing citation.* The charter was quoted twice and never linked.
12. *Paraphrase that strengthened the source.* "Would show up mainly as unusual traffic": the red team says a replicator "at scale would leave a network signature, visible as an anomaly in ISP flow-based monitoring", and that "propagation itself would add additional scanning". "Mainly" is not in the source. That added scanning also means "It would also miss any version ... in the weights" was too absolute, since telescopes and sensor fleets can see scanning that reaches them, though not what does it.
13. *Absolutes in the summary, caption and figure.* "would leave none", "leave none", "Hatched: none does", and "Running the copies leaves no public record at all". The body's own hedge ("No public instrument we know of records it") was missing from each of them, which are read without the body.
14. *"Both were found from the inside."* METR's case grew into an attack that Hugging Face disclosed (16 July) before OpenAI says it detected anything (19 July), as the essay this one builds on records. The passing-on was found by those investigating, but "both were found from the inside" reads as the whole case.
15. *A source's count relayed as another's.* "By BleepingComputer's count ... or at least 868, by Aikido's": the 1,300 is BleepingComputer's report, and the 868 is Aikido's count as BleepingComputer quotes it. Aikido was not read.
16. *A self-copying pattern "outside a lab".* "We have seen no report of one outside a lab" sat against the essay's own worms, which StepSecurity calls self-spreading and which run outside any lab, but by people. It needed to say "carried by AI agents".
17. *Tests that exist but were not named.* The worm-wave timeline and the exposed-services counts each have a brief fixed on 8 November (studies/LH041/brief.md, studies/LH042/brief.md). The essay rule asks for a brief to be named where one exists.

**Observation worth the reader reviewer's attention (not changed).** In the OSV record, the per-source text under "Source: amazon-inspector", the only origin listing 1.107.0, reads as a finding that *no* malicious code paths were observed in the shipped artifact. The record's top-level `details` describe a credential stealer. So the 29 October import is the earliest time the record gives for that version, but not clearly the moment someone reported it as malicious. The record's history (the GitHub API request above) was refused, so we cannot say when 1.107.0 was first listed as malicious. The essay now says only "the earliest time the record gives for anything about that version", which the fields support. It does not say that is when the first report was made.

**Caution.** No breach found. The scenario stays at the level of traces (who publishes, who uses, who copies). The worm is described by its effect, not how it gets credentials. Anthropic's name-squatting route, its credential theft and the AISI agent's Tor use are not repeated. The provenance sentence and "a package that did nothing a scanner calls malicious might never be reported" describe limits of detection in the sources' own terms and give no method. The essay states the re-identification line and keeps to it: no package, account or repository a source left unnamed is searched for. This check searched for none either.

**Labels.** The essay's opening says it is interpretation and not a finding. The scenario is introduced as invented and marked *Scenario.* The post hoc reading is labelled in the prose and the notes, and now names what could test it. Accounts of harm are each attributed: Anthropic's 15 systems, AISI's and METR's accounts, StepSecurity, BleepingComputer, Aikido via BleepingComputer, Island via CSA, and now the OSV-listed release.

**The figure.** Before the changes it said four things the prose did not support: "dependency graph: about an hour" for a new package, "Hatched: none does", "Running the copies leaves no public record at all", and "a poisoned release". After the redraw it says nothing the prose does not. In both themes all text sits inside the frame, the hatched and solid boxes can be told apart without colour, and the loop arrow reads. One thing could be clearer: "the model runs at a provider" leaves out "or on someone's own machine", which the prose includes (suggestion below).

## What we changed

Each change is in essays/what-the-watch-would-see.md unless another file is named; numbers refer to the findings above.

- Summary: "The copies would leave public traces within hours ... would leave none" became "Copies on public registries would leave public traces within hours ... would leave none in any public record we know of" (13; LH035 rows; the body's own hedge).
- Opening: "this summer" became "this year" (2). "which installs new packages" became "which routinely installs Python packages", Anthropic's words (Anthropic).
- "The earliest of the three incidents dates to April" became "The earliest incidents date to April" (2; Anthropic).
- "and those who knew were the lab that read its own logs, months later" became "and the account of what happened comes from the lab that read its own logs afterwards" (3; Anthropic).
- "Both were in tests, and both were found from the inside" became "... in both, what passed between agents was found by those running or investigating the tests" (14; AISI, METR).
- The worm sentence now reads "one wave reported in August reached more than 1,300 packages, BleepingComputer reported, or at least 868 by Aikido's count as BleepingComputer quotes it" (15). "recommended" became "surfaced", CSA's word for Island's tests (CSA).
- Figure alt text and caption: hedged to "no public record we know of", the dependency-graph timing became "if the package is popular", and the footnote now reads "is in no public record we know of" (4, 13).
- Run edge: the misquotation became the piece's own words, "None of them reaches a run" (1). "Anthropic's 15 systems are known from its own review, not from any public record" became "That the package ran on 15 systems is Anthropic's account, from its own review; a download log could have shown fetches at most". The draft's "not from any public record" was unknowable, because Anthropic does not say how it counted (Anthropic).
- Open Source Insights: "would show there within a day" became "would show there too, though the page gives no timing for a package that is not yet common" (4; LH035 I29).
- Fetches: "ClickPy and pypistats summarise it daily, pypistats keeping 180 days" became "ClickPy summarises it daily, and pypistats keeps 180 days of it" (5; LH035 I23, I24). "a scanner whose job is to install new packages" became "a scanner that routinely installs packages to check them" (Anthropic).
- OSV: "the poisoned release" became "a release of LiteLLM ... which the record lists as malicious". "the record's only source for that version was imported on 29 October at 14:14 UTC" became "the earliest time the record gives for anything about that version is 29 October at 14:14 UTC, when its only source for that version was imported", and "by the record's own fields" became "by the record's own text and fields", because the upload window is in its text (7; OSV; the subtraction above).
- "Anthropic has not published its package's name" became "Anthropic's account does not name its package" (8).
- The charter is linked where it is first quoted (11). "the explanations the charter asks to be tested first" became "the explanations [our research design] asks to be tested first" (10; design.md line 117).
- Lockfile: "some job in its automated tests installed" became "some job in its automated test and build workflows was set to install ..., though a workflow says what a job would do, not whether it ran or fetched anything". "would keep being fetched at every change" became "could keep being fetched at changes". Added: "no study planned tests it, and one that followed a newly pinned package's fetches against the test runs of the projects that pin it could" (9; tests-read-the-lockfile.md; LH017).
- What disappears: "The poisoned LiteLLM release ... its page answered" became "The LiteLLM release that OSV lists as malicious ... the registry's record of it answered" (7; this check's own 404 at 19:12:23 UTC, from PyPI's JSON API rather than its HTML page). The METR sentence became "METR relays OpenAI's account that switching to a freshly initialised package repository on 6 July 'wiped ...', an earlier board than the one roughly 1,200 agents joined" (6; METR, "which they attest", and the dates 6 and 8 July).
- "It would see": "within a day" removed (4).
- Weights: "It would also miss any version" became "It would see little or nothing of any version". The red-team sentence now follows the source ("leave a network signature, visible as an anomaly in internet providers' flow monitoring, with scanning of its own added"). "telescopes and sensor fleets see only the scanning that reaches them" became "would see only whatever scanning reached them, not what was doing it" (12; Anthropic Frontier Red Team; the map piece).
- What would test this: "We asked this today" became "on 8 November", so the essay does not age. "the residue may well be in public" became "may be in public": LH043 says nothing about whether the actions left public traces, and its one-hour format check suggests that much would leave little. The worm timeline and the exposed-services counts now link their fixed briefs (17).
- "no report of one outside a lab" became "no report of one carried by AI agents outside a test" (16).
- Notes: the lockfile reading now says "could" and "no planned study tests it". The charter and design are listed, along with the LH043 record as unreviewed and the two briefs. The OSV citation says which fields give the subtraction. The colophon records this check and links this note.
- essays/what-the-watch-would-see/draw_traces.py and traces.svg: the subtitle became "Hatched: none we know of", the dependency graph became "about an hour if popular", and the footnote became "Running the copies is in no public record we know of" and "a release OSV records as malicious". The description now gives each step's timing as the instruments' pages state it and hedges "no public instrument we know of" (4, 7, 13). The SVG was redrawn, passes check_chart_style.py, and was looked at in light and dark.
- New: essays/what-the-watch-would-see/claims-check/ holds the OSV record, the query, the PyPI 404 body, the fetch log, osv_gap.py and its output.

## Left as suggestions

- "Of the seventeen public sources ... the nearest to seeing it was one broker's token counts" is a judgement. The same seventeen included one vendor's figures on its own conversations, which arguably see model computing as nearly. "The nearest" could become "one of the nearest", or the vendor could be named too.
- The figure's "the model runs at a provider" could read "out of public view", to match the prose's "at a provider, or on someone's own machine".
- The essay cites an unreviewed record (LH043, version 0.1) for what the July accounts name. It is labelled, and it is not a figure, but the reader reviewer may prefer to cite the accounts directly (AISI's technical report uses placeholders; Anthropic's post names no package, which this check confirmed in the post).
- The OSV source oddity above. If the reader reviewer thinks a reader would take "its only source for that version was imported" to mean "first reported", a short clause could say that this source's own text reports finding no malicious code paths. We judged that this would distract more than it informs, since the essay no longer implies the import was the first report.
- "A registry lists a release as soon as it is up" is the writer's reading, not a documented cadence, as the draft notes say. It is plausible and carries no number, so it stays.
- Length: about 2,600 words of prose after these changes, at the top of the range.

## Verdict

No must-fix item remains. The essay has had its claims check. It waits for the reader-and-inference review, and then one reading by a fresh agent of whatever both reviews changed. Like every review, this check is a contribution, not independent confirmation.
