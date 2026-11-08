# LH041: The registry worms, dated. How far did each wave of the token-stealing worms spread by itself between a person's actions, as far as the public malware records can say, and what did it leave behind?

**In short** (added 8 November 2026; not part of the protocol). Since September 2025 a family of worms has spread through the npm and PyPI package registries by stealing the tokens that let developers publish, then publishing poisoned versions of the victims' other packages. Every report read so far says people write and launch these worms, whatever tools they use. We'll date thirteen waves named in security firms' write-ups from the public malware records (OSV's malicious-package entries, which come from the OpenSSF project) and the registries' own publish times, and ask how many separate maintainer accounts each wave reached after its first publish and over how long. We have read the firms' own counts, which differ widely, but no OSV count. The first collection follows this brief on 8 November 2026.

**Protocol 0.1, fixed 8 November 2026, before this study read any OSV, OpenSSF or registry record of any of the waves, and before any Lighthouse study counted them, as far as the writer knows.** Writer: a research subagent in Claude Code (Claude Opus 5.5) for the driving session, from proposals.md lead L-0004 and question 3 of [What AI activity costs the shared internet](../../investigations/ai-cost-and-spread.md). Before the brief the writer read: the horizon scout file notes/horizon/2026-11-07T0853Z/scout-3-supply-chain.md; nineteen vendor and press pages, sixteen of which answered (listed in [sources.md](sources.md), kept gzipped under [data/prebrief/web/](data/prebrief/web/) with [the fetch log](data/prebrief/web-log.psv)); OpenSSF malicious-packages' README, contributing guide, schema additions and ingestion config (structure only, [data/prebrief/](data/prebrief/)); one 2023 OSV record unrelated to any wave (MAL-2023-1, for the record's shape); and one npm registry read of that record's package, which answered 404 (structure only). The waves, indicators, seeds and windows are in [scripts/waves.py](scripts/waves.py) and the collector in [scripts/collect.py](scripts/collect.py); both are committed with this brief and neither had been run.

## Question

For each wave of the token-stealing registry worm family named below, from public records only:

1. **When**: when did its first and last malicious versions go up, by the registry's own publish times where they survive, against when OSV first recorded them and when the vendors said it began?
2. **How far by itself**: after the wave's first malicious publish, how many separate maintainer accounts, as far as the registry's current maintainer lists can group packages, published malicious versions, and over what span of time? Each later account is a reach the sources' mechanism attributes to the worm, which publishes with tokens it stole from the earlier victims, rather than a fresh act by the operator; the records cannot tell the two apart (below).
3. **What it left**: how many malicious package versions and packages the public records hold for it, by ecosystem.

The unit is the package version for residue, the package for coverage and the maintainer cluster for reach. Waves are the comparison; this is a description of thirteen named events, not a sample of anything.

## Keeping the strands apart

This study is the investigation's "spread run by people" strand. By every source read, these worms are written, launched and steered by people. Two sources say AI tools appear in them: Unit 42 assessed "with moderate confidence" that an LLM helped write the September 2025 worm's script (w16), and StepSecurity and Unit 42 report the 2026 waves forging commits as an AI coding assistant's bot identity and planting start-up hooks in AI coding tools (w01, w07). Neither is AI activity spreading itself, and the study does not count them as such. "Spread by itself" here means software running without a person's new act at each step, as the sources describe it; it says nothing about AI.

## What is already known of the outcome

All are vendors' or press claims read before the brief, none checked, and none says it was counted from OSV:

- **W01** (September 2025): "hundreds of software packages" (Unit 42, w16).
- **W02** (November 2025): "over 25,000 malicious repositories across about 350 unique users" on GitHub (Unit 42, w16); no package count read.
- **W03** CanisterSprawl (April 2026): "at least 16" packages or versions (search summaries of Socket and StepSecurity; THN w15 and CSA w17 retained).
- **W05 and W06**: "172 packages across 404 malicious versions" for 29 April to 12 May (CSA, w09); TanStack's own post-mortem as quoted by StepSecurity, "84 malicious versions across 42 @tanstack/* packages" (w01); "373 malicious versions across 169 npm packages plus compromised PyPI packages" by the end of 11 May (Unit 42, w07); "1,069 artifacts across 507 packages" for the Mini wave (a search summary, not opened).
- **W07** AntV (19 May 2026): "639 malicious package versions ... across 323 unique packages" in about an hour (Unit 42, w07); "more than 300 malicious package versions across 323 packages in a 22-minute automated burst", from one compromised account that "maintained 547 packages" (Snyk, w10).
- **W08 and W09**: at least 32 packages in the Red Hat namespace (Unit 42, w07); "at least 57 NPM packages and over 300 malicious package versions" by 5 June, "an initial wave of 19" PyPI packages then "at least 29", and "471 malicious artifacts" across both (SecurityWeek, w02, citing others).
- **W10** AsyncAPI (14 July 2026): five packages (Unit 42, w07), which also reports a hard-coded limit of four generations in the worm's own configuration.
- **W11** ChainDrop (4 August 2026): "444 packages and 2,212 versions in under four hours", split by StepSecurity into 11 "initial compromise" carriers and "433 victim packages (2,201 versions), republished automatically using harvested CI credentials" (w19); "at least 868 packages (across 1381 versions)" (Aikido, quoted by BleepingComputer, w03); "more than 1,300 packages" (BleepingComputer, w03); "over 400" (Unit 42, w18). Elastic says a payload file name marks packages trojanized "during worm propagation to other maintainers" (w13).
- **W12** MemTensor (September 2026): three npm versions and one PyPI version; "unclear if there are packages other than MemTensor that are impacted" (THN, w04).
- **W13** Tensorlake (8 October 2026): one version (Aikido, w14), and six platform packages from the same run (a search summary, not opened).

The writer has not seen any OSV count, record text or record list for any wave, and does not know whether OSV's records name any of the indicators below.

## The waves, and how a record joins one

Thirteen waves are named in sources read before the brief, each with a source date and indicators the source prints (file names, repository descriptions, domains, file hashes, marker strings). The full list, with the source for each, is [scripts/waves.py](scripts/waves.py); in brief:

| Wave | Name | Vendor clock (as stated) | Ecosystems |
|---|---|---|---|
| W01 | Shai-Hulud | September 2025 | npm |
| W02 | Shai-Hulud 2.0 ("Sha1-Hulud: The Second Coming") | November 2025 | npm |
| W03 | CanisterSprawl | 21 April 2026, 22:14 UTC | npm, PyPI |
| W04 | "The Third Coming" (Bitwarden CLI, Checkmarx) | 22 April 2026, 17:57 "EST" | npm |
| W05 | Mini Shai-Hulud, SAP | 29 April 2026 | npm |
| W06 | Mini Shai-Hulud, TanStack | 11 May 2026, 19:20 UTC | npm, PyPI |
| W07 | Mini Shai-Hulud, AntV | 19 May 2026, 01:39 UTC | npm |
| W08 | Miasma | 1 June 2026 | npm |
| W09 | Hades (PyPI branch of Miasma) | June 2026 | PyPI |
| W10 | miasma-train-p1 (AsyncAPI) | 14 July 2026 | npm |
| W11 | ChainDrop | 4 August 2026, 09:38:13 UTC | npm |
| W12 | MemTensor (sckit) | September 2026 | npm, PyPI |
| W13 | Tensorlake | 8 October 2026 | npm |

**Named in sources but not waves here:** the March 2026 Axios compromise (Unit 42 cites it for "wormable propagation"; no source read describes it spreading between accounts), CanisterWorm of March 2026 (named by CSA; no source on it read), Megalodon (commits to GitHub repositories, no registry residue), the s1ngularity/Nx compromise of August 2025 and the LiteLLM releases of March and October 2026 (credential theft, not described as worms; LiteLLM is LH040's), a RubyGems package and a Cursor marketplace extension (scout 3; not read).

**Matching rule.** The text searched is each OSV MAL- record serialised as JSON, lower-cased, with defanging undone. A record:

- joins wave W by **indicator** if it contains any of W's specific indicators and no other wave's;
- is **ambiguous** if it contains specific indicators of two or more waves, and is counted in none;
- joins wave W by **window** if it contains only lineage markers (Shai-Hulud, Sha1-Hulud, Mini Shai, Miasma, ChainDrop, CanisterSprawl, CanisterWorm, TeamPCP, Hades) or indicators the file marks as shared, and its date falls in W's window and in no other window it could belong to. Its date is the earliest registry publish time of its versions if any survives, else the OSV record's `published` time. A window runs from the day before the vendor clock to 14 days after (month-only clocks: the month plus 14 days), and is in waves.py;
- is **lineage, unassigned** otherwise.

Indicator and window joins are reported separately and summed only with that said. **Seeds** (packages a source names as a wave's first or headline victims) are a coverage check and never assign a record. No package outside the OSV records is added to a wave, and the vendors' package lists are not used to assign records; they are what the OSV records are set beside.

## Sources, events and clocks

- **OSV exports** (S26), `npm/all.zip` and `PyPI/all.zip` from osv-vulnerabilities.storage.googleapis.com, read once per read, with their generation headers and sha256. Only MAL- records count. OSV takes these from OpenSSF's malicious-packages repository; each record's `database_specific.malicious-packages-origins` names the reporting sources (for example `ghsa-malware`, `amazon-inspector`, `ossf-package-analysis`) and their import times. Up to 20 selected records are compared with OpenSSF's own copies on raw.githubusercontent.com.
- **npm registry** packuments (registry.npmjs.org), one GET per npm package among the selected records: the `time` object (publish time per version, which may survive the removal of a version), the current maintainer list, and, where the record's version document survives, its publisher and whether it carries an attestation. Usernames are kept only as salted hashes. No tarball, script or package code is fetched, installed or run.
- **PyPI** release JSON (pypi.org/pypi/<p>/<v>/json), one GET per (package, version): file upload times where the release still exists.
- **Clocks.** *Registry clock*: a version's npm `time` entry or its earliest PyPI file upload. *OSV clock*: the record's `published` and the earliest origin `import_time`. *Vendor clock*: the source's stated first publish or start, as in the table, at the precision the source gives. The registry clock counts for "when"; the other two are set beside it as differences. For each wave: first and last registry time, span, the lag from first registry time to first OSV `published`, and the median per-version lag.
- **Maintainer clusters.** Packages in a wave are linked when their current npm maintainer lists share any account; a cluster is a connected group. Packages with no surviving packument, or replaced by a registry placeholder (a sole version ending `-security`), are "maintainers unknown". The **seed cluster** is the cluster holding the wave's earliest registry-dated malicious publish. **Reach after the seed** is the number of other clusters with a registry-dated malicious publish later than the seed's first, with the time from the wave's first publish to each cluster's first. For W11 and W13 only, records naming `math_init.js` and records naming `Math_Symbol.js` without it are also counted, because Elastic states the first marks packages infected by the worm's propagation (w13), and StepSecurity's tier split (w19) is set beside them.

## What "spread by itself" can and cannot mean here

- **Can:** that malicious versions in one wave were published, by the registry's clock, under maintainer clusters other than the first, after the first, which is what the sources say the worm does with stolen tokens; how many such clusters; over how long; and whether a wave stayed inside one cluster (one account publishing its own packages, as Snyk describes for AntV, is a burst, not spread between accounts).
- **Cannot:** whether a person acted between those publishes (an operator holding stolen tokens can publish by hand, and the sources describe manual steps in several waves), so reach after the seed is an upper bound on spread without a person's new act, not a measurement of it; generations or who infected whom; installs, infections, or which tokens were stolen; private or deleted packages that OSV never recorded; accounts at the time (maintainer lists are today's, and co-maintainers of company packages join clusters that may be one organisation or several).
- **Between waves:** a later wave reusing tokens stolen in an earlier one is recorded only where a source read says so. Packages appearing in more than one wave are counted as a description, not as evidence of reuse.

## Missing evidence

- A request that errs, times out or is refused is **unavailable**; one retry. A wall (challenge, rate limit, login) is recorded as seen and not worked around.
- A version with no npm `time` entry or PyPI upload is **registry time unknown**, never "not published". A package whose packument is 404 is **no registry record**.
- A record whose versions are given only as ranges counts as a record and a package, with versions **not enumerated**.
- A wave with no record by indicator is **not identified in OSV's records**, which is not "did not happen" or "had no residue": OSV text may simply not name the indicators. The seed check says which.
- A withdrawn OSV record (false positive) is reported and not counted.
- Unknown is never no.

## Overlap

No earlier Lighthouse study reads OSV's malicious-package records, npm packuments or these waves. LH040 reads the OSV record MAL-2026-2144 (LiteLLM), which is not a wave here unless its text matches an indicator; if it does, that is reported. S26 (OSV) was read by LH007 for an ordinary vulnerability. The study's own requests are labelled with a generic Lighthouse User-Agent and are a few thousand metadata reads of a registry that serves far more for a single large install.

## Model disclosure

Lighthouse runs on Anthropic's models. Several 2026 waves are reported to plant hooks in Claude Code, to forge commits under a Claude bot identity, and to steal AI tool configuration (w01, w07, w19). None of this is measured here; it is disclosed so reviews can look for wording easier or harder on Anthropic or on AI tools than the sources allow.

## Safety

Nothing from a malicious-package record, registry or vendor page is installed, imported or run; OSV records and packuments are parsed as JSON data, and no payload is read. Retained vendor pages are kept gzipped as the sources published them. Prose describes mechanisms at the level a reader needs, names no private maintainer whose package was hijacked (counts only; package names where a source names them and they matter), and does not try to identify anyone a source anonymised (the keeper, 8 November 2026).

## Resource ceiling

Two export downloads per read (about 220 MB for npm); at most 3,000 npm packuments (above that, a seeded random sample, seed 41), at most 300 PyPI release reads and 20 OpenSSF spot checks, paced at least 0.3 seconds apart, one retry each; no account, key or paid service; no contact with anyone. Retained data under about 30 MB. Model spend about $40 at list rates for the read, tabulation and record, before reviews.

## Reads, schedule and stopping

- **Read 1**, 8 November 2026, right after this brief is committed: `python3 -I studies/LH041/scripts/collect.py --read <UTC label>`. Then a tabulator, written after the read to implement the measures above without changing them, and the record version 0.1.
- **Read 2**, recommended for 7 to 21 December 2026: the same collector, to see records OSV adds late and versions the registry removes, and record version 1.0 after reviews.
- **Stopping:** after read 2, or after read 1 if no wave is identified by indicator. Question, waves, indicators, windows and measures do not change after any record is read; a later change is a dated amendment, labelled post hoc if made after records were seen.

## What would leave it inconclusive

- Fewer than three waves identified by indicator: the record reports what was found and says the OSV text does not carry the sources' indicators.
- For a wave, fewer than half its npm packages with both a registry time and known maintainers: its reach is reported as **unknown**, with the counts that exist.
- The OpenSSF spot check disagrees with OSV's copy on any matched indicator or version list: counts are reported as OSV's, with the disagreement.
- Seeds largely absent from OSV's records for a wave: that wave's counts are reported as a floor of unknown depth.

In any case the study cannot say how many machines installed or ran a malicious version, whether any operator acted between publishes, or anything about packages OSV never recorded.
