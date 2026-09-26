# LH003 study brief

Following the study brief block in LH F05 (Lighthouse_Study_Templates.md).

**study:** LH003
**edition:** 0.2 (corrected 2026-09-26; see LH003.md's Corrections)
**date opened:** 2026-09-26

**owner:** the keeper (unnamed)
**methods reviewer:** (blank; none assigned)
**editor:** (blank; none assigned)
**initiated by:** unknown from inside this subagent. It was handed the dispatch prompt's text directly by the driver session and was not given Harbour's take record for this dispatch (unlike LH000, whose subagent had `take.json`), so no `dispatchedBy` identifier or queueing role can be reported here. This is a gap in what this study can fill, not a claim that the identifier does not exist.

**question:** Who already observes the computational world, which layer does each observatory see, and where does its coverage end? (LH F04's own wording for LH003.)

**scope (systems, population, period):** Reading only, no collection. The population is public documentation pages for existing third-party data sources that could show some part of AI-related activity on the internet, as those pages read on 26 September 2026. The period covered is one day of reading; no historical trend in any source is analysed.

**evidence available:** Lighthouse_Research_Design.md's existing Sources section (S1 to S19), Lighthouse_Founding_Charter.md, Lighthouse_Initial_Research_Programme.md's LH003 design section, Lighthouse_Study_Templates.md, and public web pages fetched with WebFetch and WebSearch on 26 September 2026, listed with their read status in sources.md.

**evidence needed and access status:** None beyond what was fetched. Several fetches failed or returned thin content; each is recorded in sources.md's fetch log and reflected as a blank cell or a stated caveat in the row it would have filled, not as a stopped study.

**readings and instruments (by instrument id):** None. This study reads external sources directly; it does not itself become a Lighthouse instrument, and no reading here is registered in registers/instruments.md. LH F04's own design section for LH003 asks for "a register entry for each source that could serve as a Lighthouse instrument," but this dispatch's own rules restrict this task to writing under studies/LH003/ only; registers/instruments.md is out of scope for this dispatch. That gap is carried to Next below as a follow-up ticket rather than filled by editing a file this task was told not to touch.

**comparators and known events:** None; this is a documentation survey, not a collection run, so LH001's calibration apparatus (idle baseline, repetitions, a non-LLM comparator) does not apply.

**competing explanations to test:** None in the causal sense. LH F04's own interpretation boundary for LH003 states this directly: "A survey of surveys describes the luminous fraction as others have measured it. It establishes no phenomenon and estimates no total."

**pre-specified analyses:** One row per candidate in the column order the dispatch prompt specified (source, layer seen, population, boundary, unit, cadence, licence, what it cannot see, S number or URL), plus a second table of excluded candidates with a reason each. Both are in sources.md, referenced from LH003.md's Findings.

**exploratory analyses (labelled):** The cross-source Findings in LH003.md, about where populations overlap, where a claim rests on a WebSearch summary rather than a direct fetch, and what stays invisible across every source read, are exploratory: they were not specified before reading began and follow from what turned up while filling the table.

**intended output (study, dataset, instrument revision):** A study (LH003.md), its brief (this file) and the survey table (sources.md), all in studies/LH003/.

**discovery allowance:** (blank; not set for this dispatch)
**execution ceiling:** (blank; not set for this dispatch)

**stopping condition:** Every candidate this study found has a row in the included table or a reason in the excluded table, per the dispatch prompt's own stopping rule.

**retention and sharing rules:** No Harbour data was read. No file under harbour/.session/ was opened, no credential or token was read from the environment, and no harbour/hb subcommand was run, per this dispatch's own rules. Every source here is already public.

**Harbour dispatch identifiers (if coordinated through Harbour):** Ticket LH003 in harbour/tickets.json. No take record, item id or issue id was available to this subagent (see "initiated by" above); the driver session holds those, if they exist, and can add them when it posts feedback.

**overlaps and interests to disclose:** None beyond LH000's general disclosure that Lighthouse and Harbour share a keeper. This study touches no Harbour data and observes no Harbour workflow.

**protocol amendments (date, change, reason):** 2026-09-26, edition 0.2: the included table in sources.md gains two columns, publication date and observation window, beside a last column giving each row's date read. Reason: AGENTS.md's rule for records, that each source's publication date and observation window stand beside the date read, and finding 4 of notes/review-2026-09-26-first-articles.md. The same edition amends the study's headline interpretation, its Anthropic Economic Index row and its statement on propagation; LH003.md's Corrections records each.
