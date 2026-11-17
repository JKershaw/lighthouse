# LH054: How do the public signals and distribution fixes for NoisyTCP (CVE-2026-99288), a Linux kernel TCP flaw not credited to a model, move from its disclosure, read on the same days and clocks as LH036?

**In short** (not part of the protocol). Our main kernel watch follows the signals defenders rely on, and where the fix has landed, for one Linux kernel flaw whose exploit a model wrote, but it has nothing to compare its timings with. This study reads the same signals and the same four distribution trackers, with the same collector on the same days, for a second kernel TCP flaw disclosed on 15 November 2026 at the end of a coordinated embargo, whose finder is a named person and no model. Nothing about its fix states has been read under this brief yet, though a scout saw Debian's tracker list fixed builds two days after disclosure. Reads are on Mondays and Thursdays from 19 November until that watch stops, at the latest 11 January 2027; one case chosen after a scout read it is a comparison, not a sample.

**Protocol 0.1, fixed 17 November 2026, before any fix state for this CVE was read under it.** Writer: a Claude Code research subagent (Claude Opus 5.5) in the scheduled run of 17 November 2026, under the gate of that day (notes/horizon/2026-11-17T1414Z.md, Gate, conditions on P-0038) and proposals.md P-0038. A study in the investigation [When a model finds the bug](../../investigations/model-found-bugs.md), separate from LH036: LH036's brief, measures, schedule and stop are untouched by anything here. The frame, the [panel](panel.json) and the [collector](scripts/collect.py) are fixed together.

## Credit check (done before this brief)

The gate required that, before any brief, only the oss-security post and the CVE record's credit and reference fields be read, to learn whether a model or AI tool is credited with the find. Both were read once, under scripts/robots_gate.py with `LIGHTHOUSE_PROVIDER=anthropic`, at 2026-11-17T14:40:21Z to 14:40:24Z, and are kept in [data/credit-2026-11-17T1440Z/](data/credit-2026-11-17T1440Z/read_log.json) with read times, statuses and SHA-256 of the bytes received; [credit_fields.json](data/credit-2026-11-17T1440Z/credit_fields.json) extracts the fields read from the record.

- **The oss-security post** (https://www.openwall.com/lists/oss-security/2026/11/15/2, HTTP 200, 8,796 bytes, SHA-256 01dda3ca...3a54c), read in full. Dated Mon, 16 Nov 2026 01:00:04 +0900, that is 2026-11-15T16:00:04Z. It calls NoisyTCP a vulnerability "reported and patched by Hyunwoo Kim (@v4bel)", the post's author, and says "The embargo agreed with the maintainers of linux-distros ... has expired". It names no model, AI system or tool as finder or helper.
- **The CVE record** (https://cveawg.mitre.org/api/cve/CVE-2026-99288, HTTP 200, 6,502 bytes, SHA-256 94bf8014...0f764f). Neither the Linux CNA's container nor the CVE Program's ADP container has a `credits` field. References: four git.kernel.org stable commits (CNA) and the oss-security post (ADP).

So no model is credited in what was read, and the study goes ahead as a comparison case. Whether any tool was used and not mentioned is not known.

## What is already known of the outcome

Disclosed in full, since one case chosen after a scout read it is chosen with some of its outcome in view.

- **Scout 2** (notes/horizon/2026-11-17T1414Z/scout-2-security.md, read at about 14:18 UTC on 17 November 2026, two days after the post): Debian's tracker page for this CVE listed fixed builds for bookworm (6.1.192) and trixie (6.12.117), linked a proof of concept (not opened) and showed the impact as a crash. The scout's body was not kept, so this is a reported sight, not one of this study's reads. Which suites those builds were in (the security suites or others) was not recorded. The scout also read KEV (catalogue 2026.11.13) and EPSS for other CVEs, not this one.
- **From the credit check**, beyond the credit and reference fields, the following were displayed and are disclosed: the record's `cveMetadata` (reserved 2026-09-25T10:25:14Z, published 2026-11-10T18:19:08Z by the Linux CNA, updated 2026-11-16T00:15:22Z), the CNA container's own dateUpdated (2026-11-13T14:17:22Z) and the ADP container's (2026-11-16T00:15:22Z), and the names of the CNA container's fields (it has `affected` and `cpeApplicability`, whose contents were not read). The post gives the fix as upstream commit 4e2b3ef19e0e dated 2026-11-03 (the post's date for the commit; git.kernel.org is disallowed by its robots.txt and was not read), the flaw's introduction in 2015, two trigger paths (a remote crash, and a use-after-free it calls hard to trigger), trigger times its author measured in test setups, and two interim mitigations. It also says its author used a proof of concept; no proof of concept was opened.
- **So the CVE was public five days before the embargo's end.** The record was published on 10 November and the detailed report on 15 November. A coordinated embargo exists to let distributions prepare fixes before the details are public, so fixes on or before the disclosure day are expected and say nothing by themselves about speed.
- Nothing else about this CVE was read: not NVD, OSV, EPSS, KEV for this CVE, or the Ubuntu, Red Hat or SUSE trackers.

## Question

**Signals:** how do the public signals of exploitation and severity for CVE-2026-99288 move from its publication, as each source dates itself and as Lighthouse's reads bound it: EPSS's daily score, CISA's KEV catalogue, the CVE record's scoring and enrichment, NVD's status, and the references the records gather? **Fixes:** when does each named distribution release's security channel carry a fixed kernel, by its tracker? **Comparison:** set against LH036's CVE-2026-98432 on matched clocks, read on the same days with the same collector. The unit is the CVE for the signals and a distribution release, as each tracker names it, for the fixes.

## Named events and clocks, matched to LH036

Each by its source's own date. The two cases' events differ in kind and order, and the comparison names which pair it uses.

| This study | Date (source) | LH036's matching event |
| --- | --- | --- |
| **F**, the upstream fix commit 4e2b3ef19e0e | 2026-11-03, a day (the post; not read from git) | the stable fixes, public with the CVE on 15 October (LH036's E0) |
| **E0**, the CVE record's publication | 2026-11-10T18:19:08Z (CVE record) | E0, 2026-10-15T12:08Z (CVE record) |
| **D**, the detailed public report at embargo expiry | 2026-11-15T16:00:04Z (the oss-security post's Date header) | E2, Anthropic's post, 27 October 2026 (a day) |
| **E4**, a KEV listing of this CVE, if one comes | its `dateAdded` | E4 |

In LH036 the fix and the CVE were public on the same day and the detailed account came 12 days later; here the fix commit came first, the CVE a week later and the detailed report five days after that, at the end of an embargo. Lighthouse's observation clock for any change is an interval: after the last read that did not show it and at or before the first that did. A source's own date is recorded beside it and never substituted.

## Measures

As LH036's, applied to this CVE:

1. **EPSS.** The daily score and percentile for every date the API returns from E0 on, each date's value from the earliest read holding it. A **step** is a day-on-day change by a factor of two or more, up or down. Reported: the first date scored, the series, and every step with its date and its distance in days from F, E0 and D.
2. **KEV.** At each read: listed or not; if listed, `dateAdded`, `dueDate`, `knownRansomwareCampaignUse` and the notes field. Read from the KEV catalogue body kept by LH036's read of the same day (see Overlap), not fetched again.
3. **The record's scoring and enrichment.** At each read: any CNA CVSS vector and score; any ADP container by provider, and for CISA's its SSVC values as given; NVD's vulnStatus and any score of NVD's own; and the references in the CVE record and in OSV, each new one listed with the first read that showed it.
4. **Fixes.** At each read, per distribution release as each tracker names it: Debian (each suite's status and version), Ubuntu (each codename's status and version, `linux` package), Red Hat (each listed product's state or fixed release, with advisory and date where given) and SUSE (each listed product's status). SUSE's products are summarised as LH036's interim record did after its baseline (a product counted by the states of its main kernel packages kernel-default, kernel-source, kernel-rt and kernel-64kb, live patches left out), a rule fixed here in advance for this study; the full per-package states are kept too. For each release that turns fixed: the observation interval, and the tracker's own advisory id and date where given. Whether a fixed package was installed or a machine rebooted into it is not observable.
5. **The page.** At each read: whether the oss-security post changed (SHA-256 of the body and of its extracted text), described if it did.

## The comparison that matters

Descriptive, two cases, one each side, so no rate or test:

- **Fixes, the main comparison.** For each distribution release named by the same tracker in both studies (for instance Debian bookworm's security suite, Ubuntu noble, RHEL 9's kernel, a SUSE product with a main kernel package): the days from E0, and from D (here) or E2 (LH036), to the release's first fixed state, by the tracker's own date where it gives one and otherwise as an observation interval from the reads. And at the first read on or after 7, 14, 28 and 56 days after D, and the same days after E2 in LH036's reads, how many of each tracker's named releases carry a fix. LH036's reads sit 5, 6, 9, 13, 16 and 20 days after E2 so far and this study's will sit about 4, 8, 11, 15 days after D and on, so the offsets do not line up exactly; each count is given with its read's own day offset.
- **Signals.** EPSS's first date, its steps and its series in days from E0 and from D, against LH036's in days from E0 and E2; whether and when KEV lists either; whether CISA adds an ADP container or NVD a score of its own to either.

What a difference would mean is limited. One case chosen after a scout read it is not a sample of kernel flaws not found by models, and the two flaws differ in more than how they were found: the disclosure route (an embargo through linux-distros here; a CVE published with its fixes there), the reachable configuration (default TCP listeners here, a Multipath TCP listener there), the stated impact, and the order of fix, CVE and detail. A coordinated embargo can put fixes out on day zero, so fixes at or before D are what an embargo is for. A difference in timing is a description; a cause needs its own evidence, and none is sought here.

## Reads and schedule

One read on each of LH036's Monday and Thursday read days from Thursday 19 November 2026, in the window of the scheduled run and on the same day as LH036's read: 19, 23, 26 and 30 November; 3, 7, 10, 14, 17, 21, 24, 28 and 31 December; 4, 7 and 11 January 2027 (16 reads, if LH036 runs to its hard end). The first read is the baseline; there is no separate baseline group. Each read runs `LIGHTHOUSE_PROVIDER=anthropic python3 studies/LH054/scripts/collect.py --read <UTC label>` once: a copy of LH036's collector whose only changes are its docstring, the removal of the baseline option and a ceiling of 12 URLs (the diff against studies/LH036/scripts/collect.py shows them). It makes one robots-gated GET per URL in [panel.json](panel.json) (nine: the CVE record, NVD, OSV, EPSS's time series, the Debian, Ubuntu, Red Hat and SUSE trackers, and the oss-security post), raw bytes up to 4 MiB each kept gzipped and email-redacted under `data/read-<UTC label>/` with start and finish times, status, content type, `Last-Modified`, length and SHA-256. No retry around a wall, no search, crawl, login or paid service. The kernel CVE team's announcement is left out of the panel because git.kernel.org's robots.txt disallows it (LH036's amendment of 8 November). A tabulator written after the baseline implements the measures as written and changes nothing here; it may reuse LH036's tabulate.py. Each read writes a short checkpoint, studies/LH054/checkpoints/<date>.md. A missed read stays missed.

Never: open or fetch the proof of concept or any exploit, probe or scan any host, send anyone crafted packets, run anything from a download, or contact anyone. Lighthouse makes no claim in its own voice that the flaw is exploited or that any system is compromised; a third party's published report of exploitation that appears in a panel source is recorded as that party's claim, with what it rests on.

## Missing evidence

A body under 200 bytes, a refusal, a challenge, a rate limit or a robots refusal is **unavailable** at that read; a 404 from a tracker is **no record** at that read (Ubuntu's and Red Hat's JSON endpoints may answer 404 until they have a record). Unknown is never no: an unavailable tracker is not an unfixed one, and an undated fixed state is not a late one.

## Overlap

- **LH036**: the same instruments, the same days and the same trackers' pages for another CVE. This study takes its KEV status from the KEV catalogue body LH036 keeps on the same read day, so the two studies always see the same catalogue version and the 1.8 MB feed is fetched once; a missing LH036 KEV body makes KEV unavailable here for that read. No other data is shared.
- **LH048** reads NVD, EPSS and KEV for LH036's CVE, not this one; **LH038** follows LH036's advisories. Neither overlaps this CVE.
- The pre-brief reads (the credit check and scout 2's sight) are disclosed above and are not the baseline.

## Ceiling, stopping and what would leave it inconclusive

At most 12 URLs and 40 MiB per read, 16 reads at most, no subagent needed for collection; about $20 at list rates for the brief, reads, checkpoints and record together. The study stops with LH036's stop: its last read is LH036's last read, and never later than LH036's read of 11 January 2027. If a KEV listing of LH036's CVE brings LH036's stop earlier, this study stops at the same read and later rows are cancelled with that reason. A KEV listing of this CVE does not by itself change the stop. The record follows the stop, with an evidence review, a reader-and-inference review and a recheck; any piece needs its own reviews.

Inconclusive, and named as such:

- **Debian's and SUSE's pages give no dates.** Releases already fixed at the first read (Debian's bookworm and trixie builds the scout saw, at least) are fixed at or before 19 November with no lower bound here; their days from E0 or D cannot be compared with LH036's, whose Debian suites and 19 SUSE products were also undated at its first read. Both comparisons for those trackers may end left-censored on both sides.
- **The embargo.** Fixes prepared under embargo and released on or before D measure the embargo's arrangements, not a response to disclosure; LH036 had no embargo in the same sense. A fix dated before D is reported, not read as speed.
- **Different first-read offsets.** This study's first read is about 4 days after D and 9 after E0; LH036's was 5 after E2 and 17 after E0. A release fixed before either first read gives an upper bound only.
- **EPSS** if the API stops returning this CVE's history; **any tracker** unavailable at most reads; **any change** whose surrounding reads were missed; **a release** named by one study's tracker and not the other's, which is reported and not compared.
- It cannot say whether anyone has exploited either flaw, how many machines run an affected kernel, whether a fixed package was installed, why any score moved, or whether a model's involvement made any difference: two cases cannot carry that.
