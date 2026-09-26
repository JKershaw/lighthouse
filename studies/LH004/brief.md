# LH004 study brief

Following the study brief block in LH F05 (Lighthouse_Study_Templates.md).

**study:** LH004
**edition:** 0.1
**date opened:** 2026-09-26

**owner:** the keeper (unnamed)
**methods reviewer:** (blank; none assigned)
**editor:** (blank; none assigned)
**initiated by:** unknown. This task was handed to the writing subagent as ticket text only, exactly as Harbour issued it (LH004, kind `research`, priority 2, from `harbour/tickets.json`). The subagent was not given the underlying dispatch's `take` record, so no `dispatchedBy` identifier or claim time is available to say whether a person or Harbour's autopilot loop queued it; the driver session holds that record, not this study.

**question:** As set by Lighthouse_Initial_Research_Programme.md (LH F04, the LH004 section): what would Lighthouse's three layers have shown during a documented propagation event, and which layer carried the first detectable signal?

**scope (systems, population, period):** One documented case, the xz-utils/liblzma backdoor (CVE-2024-3094), as it appears in the public record. Population is a sample of one, chosen as LH F04's first choice for this ticket; no claim is made about propagation events generally. Period covered by the sources: 29 October 2021 (Jia Tan's first mailing-list contact, per the timeline reconstruction cited below) through 26 September 2026 (the date every source below was read); the events analysed are concentrated in February and March 2024.

**evidence available:** The two sources already carrying S numbers in Lighthouse_Research_Design.md, S14 (Andres Freund's oss-security disclosure) and S15 (the NVD CVE-2024-3094 record), plus additional public pages fetched today with WebFetch and WebSearch: the upstream project's own account, a widely cited timeline reconstruction, a community technical write-up, one vendor advisory, one distribution's own incident post, and one distribution's security tracker. Full list with dates read in reading-list.md.

**evidence needed and access status:** Any non-public record, such as internal build-farm logs, private messages among the identities involved, GitHub's own account-moderation log, or distributions' internal incident timestamps beyond what each has published, would help fix some dates more precisely; none of it is accessible to this study, which used only public pages reachable from this container. Lighthouse operated no instrument of its own during the events described, so nothing beyond the public record can be added on that side either.

**readings and instruments (by instrument id):** None of Lighthouse's registered instruments (registers/instruments.md holds only I-0001, the export reader) observed this case; it happened before Lighthouse existed and outside any system Lighthouse watches. This study instead reads LH F02's measurement-surfaces table against the public record and states, for each layer, which surface or named instrument would have applied had one been watching at the relevant observation point, and says plainly where none would.

**comparators and known events:** The two alternative cases LH F04 names for this ticket, Log4Shell (S16) and the left-pad removal (S17), are noted for contrast but not analysed in depth; this study followed LH F04's first choice, xz. Lighthouse's own proposed host sampler, ticket I-0002 ("Sample the host," still `todo` in tickets.json), is used as a comparator for what a running Lighthouse instrument could versus could not have caught.

**competing explanations to test:** Whether the pre-disclosure anomalies (valgrind errors, a slower ssh login) could be read as an ordinary performance regression or a benign upstream mistake rather than a deliberate backdoor, before the disclosure settled the question; whether the near-simultaneous uptake across several rolling-release distributions reflects a coordinated push or the ordinary, uncoordinated cadence by which each distribution happened to package a new upstream point release within the same few weeks.

**pre-specified analyses:** The per-layer breakdown LH F04 specifies for this ticket: for activity, residue and propagation, what was observable, from where, by whom, at what delay, and which F02 instrument would have recorded it.

**exploratory analyses (labelled):** Distinguishing two separate activity-layer signals in the record, one noticed and correctly diagnosed (Andres Freund's), one noticed earlier and not diagnosed at the time (valgrind errors reported from Fedora's build and test infrastructure), was not asked for by LH F04's per-layer template in so many words; it follows from trying to answer "which layer carried the first detectable signal" precisely, and is treated as exploratory. See the essay's Findings and Limits.

**intended output (study, dataset, instrument revision):** An essay, `LH004.md`, in the Harbour standard's essay form, with an annotated reading list, `reading-list.md`. No dataset and no instrument revision; no new physical observation record was created, since this study reads only published secondary and primary accounts of a past event.

**discovery allowance:** (blank; not set for this dispatch)
**execution ceiling:** (blank; not set for this dispatch)

**stopping condition:** The essay exists with its reading list, per the ticket's own wording.

**retention and sharing rules:** Every source used is a public web page; none is Harbour's own store, and nothing under `harbour/.session/` was read. Web pages can change or move after the date each was read; the essay states each source's read date for that reason, following LH F02's instruction that documentation changes and studies must preserve the version they used. No token, session id or credential appears anywhere in this study.

**Harbour dispatch identifiers (if coordinated through Harbour):** Not available to this study; see "initiated by" above. Ticket id `LH004` in `harbour/tickets.json` is the only identifier this study was given.

**overlaps and interests to disclose:** This case is external to Harbour; no Harbour evidence is used or relied on. The preparation of this essay is itself Lighthouse research activity, being web fetches and inference run by this subagent; per the charter's commitment to account for Lighthouse's own presence, that activity is disclosed here but is not tagged as Lighthouse traffic at the collection points it used (the pages fetched have no way to distinguish this call from any other reader), and it is not measured within this task, since a subagent cannot see its own token usage or cost (CLAUDE.md; the driver posts that separately as a usage entry, outside this study).

**protocol amendments (date, change, reason):** None. Edition 0.1 is the first.
