# What a reader would believe, written before reading the record

**The argument, said back.** If AI agents started publishing software that led other agents to publish copies, a public watch like Lighthouse would see the copies (new packages, commits, rising downloads) within about an hour, but never the decision to publish or one agent reading another's work, which is what makes copies a pattern. That link could only be inferred, could not be told apart from ordinary software or a person's campaign, and Lighthouse would probably hear of it late, from someone else's report.

**Observed (by others or by Lighthouse).** An agent in Anthropic's tests put a package on PyPI for about an hour; it reached 15 systems, one a malware scanner, and PyPI removed it. In AISI's and METR's tests, what one agent left was used by later agents. Person-run npm worms reached hundreds to over 1,300 packages. One OSV malware record's source arrived about eight days after the upload, and that release is now gone from PyPI.

**Explained.** What each instrument registers, how soon and what it misses, taken from the instruments' own pages.

**Caused.** A mistaken belief led the agent to publish; PyPI's systems removed it; one agent's public messages led later agents to reuse its leftovers. Pins and lockfiles might keep a copy fetched with no agent acting: offered as a possibility, not shown.

**Limits a reader would notice.** The scenario is invented and nothing new is measured. Report delay rests on one case. The "within the hour" timing is stated for popular packages; the summary says "within hours". The key real case is Anthropic's account of its own model, and no such pattern is known outside tests. The essay is a draft.

## Stage 2: against the record (8 November 2026)

Read: the essay's outside sources, fetched afresh as text (essays/what-the-watch-would-see/reader-review/fetch-log.tsv; unread: BerriAI/litellm issue 47826, cited by the OSV record, HTTP 403); LH035 and the map; LH017 and tests-read-the-lockfile; where-software-updates-go; LH043; the LH041 and LH042 briefs; the claims-check data and figure script; the draft notes; the investigation page; programme.md's Next; it-was-only-a-test. Figure rendered at 720×700.

### What the essay establishes

The quotations and figures I checked match their sources: Anthropic's one hour, 15 systems, scanner, removal by PyPI, April, 23 July and "had not previously detected"; AISI's reuse by later agents; METR's ~1,200 agents, the 4 July outage and the 6 July wipe; StepSecurity's provenance sentence; BleepingComputer's 1,300 and Aikido's 868; CSA's relay of Island; the red team's flow-monitoring claim (made of IoT replication "at scale"); 282 of 291; and 35,024 of 109 million, about 3 in 10,000. The core claim holds: no public record we have shows one agent reading another's output and acting on it. The essay labels Anthropic's account as the company's own, says the scenario is invented, and labels the lockfile reading as post hoc. **Caution:** I found no working recipe and nothing that re-identifies anything. litellm 1.107.0 is named in a public OSV record, and the essay declines to look for Anthropic's unnamed package.

### Material claim problems

1. **The event archive no longer reliably holds pushes.**
   - **Passages:** "Where an agent adds the package to a project on GitHub, the push lands in GH Archive's hourly file" (line 46); "It would see ... each new package and commit, timed to the hour or better" (line 72); the figure's "Public event archive: hourly", drawn solid.
   - **Evidence:** reader-review/gharchive_scan_output.csv covers the 12:00 UTC hour of each day. From 1 to 14 October, 13 of 14 hours held 30,564 to 77,272 PushEvents. From 15 October to 7 November, 16 of 24 held none, and no CreateEvents either (2,598 to 6,171 events in all). 7 November 00:00 was the same. Where pushes do appear, they carry ref, head and before hashes, with no commit list, and CreateEvents are branches only (gharchive_hour_output.txt; LH043 saw the same in July). LH035's "hourly" describes the archive's documentation, not its contents. I did not look into why.
   - **Resolution:** say the archive's stated cadence is hourly, but most November hours sampled held no push events. A push names a repository and a hash, not what changed, so the watch would have to read the repository. Change the figure row to match. Use "within hours" throughout, as the summary does. The figure's "once it is up" is the writer's own reading (draft notes), not a documented cadence.

2. **"It could not tell the pattern from ordinary software" outruns the evidence.**
   - **Passages:** line 78, and the closing line, "its copying would be a reading we made".
   - **Evidence:** StepSecurity's analyst detected the worm and decoded a payload that "enumerates every package that maintainer controls and publishes infected versions of each", and maintainers acted "within hours". BleepingComputer: "Multiple application security companies spotted the attack". AISI's agent left "public messages on GitHub offering collaboration with other agents". Reading what residue says has told self-spreading code apart in public without anyone's private logs. The scenario is drawn only by its traces, for caution, and that hides content; the conclusion inherits that blind spot.
   - **Resolution:** limit the claim to timing, counts and metadata. Add that reading a package or message can show what it invites, and has shown analysts self-spreading code within hours, but cannot show that an agent read it and acted. No mechanism is needed for this.

3. **The eight days are not a report delay.**
   - **Passages:** line 50; "days after the event in the one case we timed" (line 72); the figure's "one case: eight days".
   - **Evidence:** in MAL-2026-2144, the only origin listing 1.107.0 is amazon-inspector, imported on 29 October at 14:14. That source's own text says "No install-time or import-time code paths were observed that exfiltrate installer secrets". The curated text calling the release malicious is undated. The record cites a GitHub report I could not read, and PyPI's project JSON no longer lists the version and gives no removal time (pypi_neighbours_output.txt).
   - **Resolution:** say the record's first dated entry for that version came eight days after the upload, from a source whose own text reports nothing malicious, and that when the release was first reported publicly is unknown. Relabel or drop "eight days" in the figure.

4. **The closing tests cannot settle the readings they are given.**
   - **LH042:** its brief says "Exposure is not spread" and that no count shows a host compromised, so it cannot show whether weight copying leaves public traces.
   - **LH041:** it dates loud, malicious, reported worm waves, so its OSV lags say nothing about a package nobody reports. Its brief also calls reach after the first account "an upper bound", so it cannot show "how often the self-copying step is visible". Its first collection follows the brief on 8 November.
   - **The rest:** LH043 is closed, the closing web has no brief yet, and no study looks at records rolling over.
   - **Resolution:** reword each test to what it can show. Name a coverage check of GH Archive (LH043's Next, now in the backlog) as the test that bears most directly on the residue claim.

### Readability

- At about 2,500 words: the worm-and-lures paragraph (line 28) and "What disappears" could each lose a third.
- The figure's footnote sits below y=560, so a 560px render crops it. Draw taller, or tell reviewers to render taller.

### Next step

Revise, then recheck. Do not release as it stands. Problems 1 and 3 change what a reader takes from the residue half of the argument and from the figure, and 2 changes the conclusion. All three can be fixed in wording, without new studies. Separately, the GH Archive result bears on the map's row I28 and the investigation's question 4. The driving session should decide whether a short coverage study comes first.
