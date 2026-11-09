# LH048: How were the flaws behind Anthropic's five attack chains of 27 October 2026 scored, and do the signals of exploitation move?

**In short** (written 9 November 2026; not part of the protocol). On 27 October Anthropic described five attack chains its unreleased model built, in Chrome, Safari, Android, Windows and Linux, but named only two flaws by number: one in Windows and one in Linux. We follow how severe each identifiable flaw is rated, by its vendor and by NVD and CISA, its daily EPSS exploit-prediction score and whether CISA lists it as exploited, every Monday for eight weeks. So far only the Linux flaw's signals are known, from the core watch: rated 9.8 out of 10 by the kernel, a low EPSS score and no CISA listing on 1 November. The exploit and the post are Anthropic's, and Lighthouse runs on Anthropic's models.

**Protocol 0.1, fixed 9 November 2026, before this study read any outcome for any flaw in it.** Writer: a research subagent (Claude Code, Claude Opus 5.5) of a driving session, from schedule row `five-chains-brief`. Question 3 of the investigation [When a model finds the bug](../../investigations/model-found-bugs.md). The brief, [panel.json](panel.json) (every route), [selection.json](selection.json) (the units, with the rule's pending steps) and the [collector](scripts/collect.py) are committed together, before any read under this protocol. What was read to write it is in [sources.md](sources.md).

## Model disclosure

The exploits and the post are Anthropic's, and every agent that writes or reviews for Lighthouse in this study runs on an Anthropic model. The keeper chose disclosure over a reviewer from another provider for this investigation on 1 November 2026. Every record and piece from this study states this beside its model line, and its reviews are asked to look for wording easier on Anthropic, or on the chains' significance, than the sources allow, in either direction.

## Question

For each flaw that Anthropic's post of 27 October 2026, "Discovering and exploiting vulnerabilities in critical, real-world software with Claude", uses in one of its five attack chains: how is it rated for severity by its vendor and, where present, by NVD and by CISA's enrichment of the CVE record; what is its daily EPSS score; and is it in CISA's Known Exploited Vulnerabilities (KEV) catalogue; and how do these move from the post's publication through 4 January 2027? The set is chosen by the post, not by Lighthouse: five chains, not a sample.

## What the writer already knows of the outcome

- **The post** (read from LH036's retained copy of 5 November 2026, S1; its text is the same as LH036's copy of 1 November, with dateModified 2026-10-30T15:24:16Z in both). It names two CVEs: CVE-2026-33096 for the Windows chain and CVE-2026-98432 for the Linux chain, each linked to its NVD page. For Chrome it says "62 CVEs have been assigned and patched as of Chrome 156, with all of them rated critical or high severity", linking one Chrome release note; that is the post's own claim about vendor severity for a set larger than the chain, and the writer has not checked it. For Safari it says Apple "implemented a fix promptly. That fix is available to users", linking one Apple support note. For Android it says "This issue has been addressed by Google", with no CVE and no link. It gives no severity, EPSS or KEV figure for any flaw.
- **The Linux flaw** (from LH036's brief and the investigation page, both public in the repository; read 1 November 2026 at 08:07 to 08:30 UTC by LH036): the kernel CNA's CVSS 3.1 score 9.8 (`AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`); no CISA ADP container; NVD vulnStatus Received with no NVD score seen; EPSS 0.00457, percentile 0.39673, dated 31 October; not in the KEV catalogue as read. The writer has not read LH036's checkpoints of 2 and 5 November or any of its signal data after 1 November, and so does not know whether any of these has since changed.
- **The Windows flaw, the Chrome and Safari pages, and Android:** nothing. The writer has not opened the Chrome release note, the Apple note, NVD, the CVE record, Microsoft's Security Update Guide, EPSS or KEV for any of them. A filename search of the repository for the Chrome page's address, the Apple note's number and the Windows CVE's number matched two files under studies/LH044/data/statements-2026-11-08T1920Z/ (0013.b and 0019.b) and several unrelated download tables; none was opened.
- **Feasibility, on unrelated CVEs, 9 November 2026:** EPSS's API returned a 30-day series for two CVEs in one request (CVE-2024-4577, CVE-2024-38063); Microsoft's Security Update Guide API returned, for CVE-2024-38063, fields named `severity`, `impact`, `baseScore`, `vectorString`, `exploited`, `publiclyDisclosed`, `releaseDate` and `latestRevisionDate` (S3, S4).

## Population and unit

The population is the five chains of the post, as the post divides them. The unit is a **flaw**: a step the post describes as a vulnerability in one chain. The post describes these steps (selection.json lists them):

- **Chrome (C1 to C4):** V8 heap corruption; a V8 sandbox escape that defeats ASLR; a race in CacheStorage; a use-after-free in FedCM.
- **Safari (S1 to S3):** a use-after-free in JavaScriptCore; Gigacage variables used to index other memory; a vulnerability in the WebContent sandbox's IPC mechanism. (The post's fourth step reuses the use-after-free, and it says some of the weaknesses "are not vulnerabilities on their own but intended behaviors"; S2 is kept as a step because the post describes it as something Claude "discovered", and it may well have no CVE.)
- **Android (A):** "three of them" chained, with four bypasses described; the post names none.
- **Windows (W):** CVE-2026-33096, named.
- **Linux (L):** CVE-2026-98432, named.

Each unit is classed once, at the discovery read, by the selection rule below, and the class never changes afterwards except by a dated amendment:

- **named**: the post gives the CVE identifier (W and L).
- **identified**: exactly one entry on the page the post links for that chain meets the rule.
- **ambiguous**: more than one entry meets it; all are kept as the unit's **candidates**, measured, and reported apart from identified flaws, never pooled with them.
- **unidentified**: no entry meets it. The flaw's signals are **unknown**, not low, not unlisted.
- **no identifier**: the post gives neither a CVE nor a link (Android). Recorded as such, with no search for one; its signals are unknown.

**Selection rule** (applied by hand to the discovery read's copies of the two linked pages, before any other source is read for these flaws, and recorded in selection.json with the quoted entry text). An entry on the linked page meets the rule for a step if both: (a) its credit names Anthropic, Claude, or one of the seven contributors the post lists (Nicholas Carlini, David Dworken, Xinyang Ge, Ben Morris, Milad Nasr, Chris Rohlf, Luna Tong); and (b) its description names the step's component and, where the post gives one, its bug class: C1 and C2, "V8" (C2 also "sandbox" where the entry says it); C3, "CacheStorage" or "Cache Storage" with "race"; C4, "FedCM" with "use after free" or "use-after-free"; S1, "JavaScriptCore" or "WebKit" with "use after free" or "use-after-free"; S2, "Gigacage", or a WebKit entry whose description says out-of-bounds access through an index; S3, a WebKit, WebContent, Safari or Sandbox entry whose description or impact mentions the sandbox, IPC or reading files. Where C1 and C2 share candidates, each candidate goes to the step whose wording it matches, and to both as ambiguous if it matches either. Severity on a page plays no part in the rule. Every entry that meets (a) but is assigned to no step joins the **linked set**: flaws the post's links credit to Anthropic, measured descriptively as context for the post's "62 CVEs" claim, never counted among the chains. The Chrome page covers one release; CVEs the post counts but that page does not list are outside the study.

Chrome's and Apple's severity words become visible at the discovery read, at the same moment as the credits. The rule is fixed here so that the selection cannot depend on them; the record says who applied the rule and when.

## Sources, events and clocks

Each read takes one copy of each source (panel.json fixes the routes):

1. **Vendor severity.** Chrome: the severity word Google's release note gives each entry (Critical, High, Medium, Low). Apple: whatever rating Apple's note gives (a note that gives none is recorded as "no vendor rating given", which is a reading, not a missing one). Microsoft: the Security Update Guide's `severity`, `impact`, `baseScore`, `vectorString`, and its `exploited` and `publiclyDisclosed` assessments, with `releaseDate` and `latestRevisionDate`. Linux: the kernel CNA's CVSS in the CVE record.
2. **The CVE record** (CVE Program API): the CNA container's metrics (every CVSS version present, and any other metric), and each ADP container by provider, with CISA's ADP container's CVSS and its SSVC values (Exploitation, Automatable, Technical Impact) as given; datePublished and each container's dateUpdated.
3. **NVD** (API 2.0): vulnStatus; each CVSS metric with its `source` and `type` (Primary, Secondary); lastModified; any `cisaExploitAdd` fields.
4. **EPSS** (FIRST's API, `scope=time-series`, batched): the score and percentile for every date returned, each date's value taken from the earliest read holding it.
5. **KEV** (CISA's JSON feed): listed or not, and if listed `dateAdded`, `dueDate`, `knownRansomwareCampaignUse` and notes; the catalogue's own version and date.
6. **Pages:** the post and the two linked pages, by SHA-256 of the body and any modified date they give; what changed, described.

Named events, each by its source's own date: **E2**, the post's publication, 27 October 2026 (datePublished, a day without a time), as in LH036, and its last modification 2026-10-30T15:24:16Z. For each flaw: **P**, the CVE record's datePublished; **V**, the vendor's own release date for the fix (the Chrome note's date, the Apple note's date, Microsoft's releaseDate; for Linux, LH036's E0, 15 October 2026); **K**, a KEV dateAdded if one comes. Lighthouse's observation clock for any change is an interval: after the last read that did not show it and at or before the first that did. A source's own date is recorded beside it and never substituted.

## Measures

1. **Severity, per flaw:** each source's rating at each read, and each CVSS score's qualitative band under the CVSS specification (Low below 4.0, Medium to 6.9, High to 8.9, Critical 9.0 and above). Vendor words are reported as given; Microsoft's scale (Critical, Important, Moderate, Low) is not mapped to CVSS bands. Whether the vendor's or CNA's CVSS band and NVD's or CISA's band agree at the last read, and any change of rating with its interval.
2. **EPSS, per flaw:** the series from P (or from the earliest date returned), the value on each read date, the first date scored, the highest value, whether the percentile was ever above 0.5, and every **step** (a day-on-day change in score by a factor of two or more, up or down) with its date and its distance in days from E2, V and K. A step near an event is a coincidence of dates; no cause is claimed.
3. **KEV, per flaw:** listed or not at each read; if listed, K and the interval.
4. **The gap**, per identified or named flaw at the last read: rated High or Critical by at least one source, EPSS percentile at or below 0.5 on the last date held, and not in KEV. Reported as a list of flaws, with each part shown.

## The comparison that matters

Within each flaw, across sources: vendor against NVD and CISA, and severity against the exploitation signals (measure 4), at each read and against E2. Across the five chains, side by side: which chains have a flaw that can be scored at all, and how each scored one stands. Five chains, and at most a dozen or so identifiable flaws, cannot support a rate: nothing here says how AI-found flaws are scored in general, or whether they are scored differently from others, and no comparison group is drawn. An EPSS percentile is already a comparison with every scored CVE, and is the only reference the study uses. The linked set is described alongside, never pooled with the chains.

## Missing evidence

A missed read stays missed. At a read, a body under 200 bytes, a refusal, a challenge, a timeout or a URL the robots.txt gate refuses is **unavailable** for that source; a 404 from the CVE record or NVD, or an empty EPSS answer for a CVE, is **no record at that read** (for EPSS, "not scored at that read"). A record that was read but lacks a field is "not given at that read". Absence from a KEV catalogue that was read is "not listed at that read", a statement about the catalogue, not about exploitation. Unidentified and no-identifier units are unknown in every measure. Unknown is never no.

## Overlap

The Linux flaw, CVE-2026-98432, is LH036's core watch, which reads the same KEV feed, EPSS, the CVE record and NVD for it on Mondays and Thursdays, and LH038's subject. LH048 reads its own copies and does not reuse LH036's data, but on Mondays both studies read the same sources for this CVE within hours, so their readings of it are not independent evidence, and agreement between them is not confirmation. Its prior state, above, comes from LH036. LH031 and LH037 read the KEV catalogue for other CVEs; no read is counted in two studies. The post's text comes from LH036's retained copy; LH048 reads the post afresh at each read only to see whether it changes.

## Reads and schedule

- **Discovery** (`collect.py --discover`), as soon as this protocol is on main, 9 to 12 November 2026: the post and the two linked pages, once. The rule is then applied and selection.json filled and committed, before the baseline.
- **Baseline** (`collect.py --read <label> --full`), straight after the selection commit, in the same window. Its EPSS series reaches back 30 days, which covers E2.
- **Monday reads** (`collect.py --read <label>`), aligned with the PHP watch's Monday reads, in the scheduled run's window: 16, 23 and 30 November, 7, 14, 21 and 28 December 2026, and **4 January 2027** (with `--full`), the end date, eight weeks after this brief. Each read is followed by a short checkpoint (any rating change, CISA ADP container, EPSS step, KEV listing or changed page, said so in the commit message).
- **Interim checkpoint** after the read of 7 December: measures 1 to 4 to date.
- **Record** (version 1.0) by **15 January 2027**.

The collector is the only reader; it asks scripts/robots_gate.py before every request, carries Lighthouse's User-Agent, withholds email addresses with redact_bytes before saving a body, keeps raw bytes up to 4 MiB gzipped under `data/<discover|read>-<UTC label>/` with UTC start and finish, status, content type, Last-Modified, length and SHA-256 of the bytes received, and skips anything already held. No search, crawl, login or paid service; no test of any system for any flaw; nothing is downloaded beyond the listed routes. A tabulator written after the baseline implements the measures above as written and changes nothing here.

## Ceiling, stopping and what would leave it inconclusive

At most 3 GETs for discovery, 40 for a Monday read and 220 for the baseline and the last read, and 60 MiB per read, besides one robots.txt per host per run; about 10 reads in all. NVD requests are spaced 6.5 seconds apart, to stay within NVD's published limit for requests without a key as the writer understands it (five in a rolling 30 seconds); NVD's developer page, read on 9 November, returned only a script shell, so the figure was not confirmed there. Collection needs no subagent; the record is written and reviewed on Opus 5.5 or stronger. The study stops after the read of 4 January 2027. A KEV listing does not stop it early.

It is inconclusive for a chain whose flaws are unidentified, ambiguous or have no identifier (Android certainly, and S2 likely); for EPSS if the API stops returning these CVEs; for a source unavailable at most reads; and for the timing of any change whose surrounding reads were missed. It cannot say whether anyone has exploited any flaw, why any score moved, how many systems are affected, or whether the post's "62 CVEs ... all rated critical or high severity" is true beyond the one page it links. It makes no claim that harm is happening or that a system is compromised; a third party's published report of exploitation would be recorded as that party's claim, with what it rests on.
