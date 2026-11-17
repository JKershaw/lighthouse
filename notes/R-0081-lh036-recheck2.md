# R-0081: LH036 interim, recheck of the resolution of R-0079

**In short.** The one fresh reading of what the driving session wrote into the LH036 interim record to resolve its reader-and-inference review (R-0079). Every changed or added sentence holds against the retained data, and both of R-0079's must-fix findings are met: the record no longer calls itself unreviewed, and its opening now carries the no-cause caveat and the state of the fixes at the first read after the post. I made four small wording changes, listed below, and no figure changed. Cleared.

Row LH036-interim-recheck. Reader: Claude Opus 5.5 (claude-opus-5-5), subagent, 17 November 2026, no network. The exploit and the post this study follows are Anthropic's, and this reader runs on an Anthropic model; a review contribution, not independent confirmation. Cost: unknown, not measured; unknown is not zero.

**Version checked:** studies/LH036/LH036.md version 0.2 as it stands at commit aab5945 (HEAD 43253d1, unchanged in between), sha256 b666931dc14f0020603347a27a70303f6a3a70880159f71f09ef79e6e5f125be, against version 0.1 at f677d6f (`git diff f677d6f aab5945 -- studies/LH036/LH036.md`). After this recheck's changes: sha256 2f94f761d668eede92e27279e256231d2b0b0ea6d9ebdbde750954bd1d3fc5e4, uncommitted.

**A note on the commits, for the driver.** The 0.2 text did not land in aab5945, whose message names it. It landed in 38bac6c, whose message is "LH051 checkpoint of 17 November", and aab5945 itself changes studies/LH049/LH049.md. The two messages look swapped. The file at aab5945 and at 38bac6c is identical, so the diff above is the right one. History should not be rewritten; a line in the next commit message is enough.

## What was checked

Each changed sentence, against studies/LH036/data/tables.json, recounted by my own script (scratchpad, output reproduced below), and where the claim is about the first read, against the raw bodies in studies/LH036/data/read-2026-11-01T0830Z/:

- **"only one-day rise by a factor of two or more came on 25 October, a day after [E1] and two days before the post"**: `epss_steps` has one step, 2026-10-25, 0.00165 to 0.00388 (factor 2.352), `days_after_event` E1 +1, E2 -2. E1 is the CNA container's dateUpdated, 2026-10-24T14:08Z (brief, Named events). Holds.
- **"the dates do not say why the score moved"**: the brief's measure 1 rule, carried into the opening. Meets R-0079 finding 2.
- **"which does not say whether anyone has exploited it"**: matches the brief ("It cannot say whether anyone has exploited the bug"). Holds.
- **First read, five days after the post**: read 2026-11-01T0830Z, post 27 October. Debian: bookworm (security) and trixie (security), forky and sid fixed; bookworm and trixie point releases vulnerable. SUSE: 112 products with a main kernel package (kernel-default, kernel-source, kernel-rt, kernel-64kb), 19 with a Released one. Red Hat: raw body has no `affected_release` field at all; every RHEL 8, 9, 10 kernel row Affected. Ubuntu: raw body, no codename other than upstream released in any kernel package (linux: four pending, three needed, trusty not affected). Holds.
- **"no tracker dates a fix on or before the post"**: Red Hat's earliest fixed release is dated 2026-11-01 (RHSA-2026:93412 to 93415, first shown at the read of 2 November); Ubuntu lists no notices until the read of 12 November; Debian's and SUSE's pages give no dates. True as written, but read alone it suggests no fix existed before the post, which the record does not know (Answer: "when their earliest fixes landed is not known here"). Changed, below.
- **"the kernels of Red Hat's Enterprise Linux 8, 9 and 10"**: at 16 November RHEL 8 kernel and kernel-rt, RHEL 9 kernel, RHEL 10 kernel each have a fixed release; RHEL 9 kernel-rt has left the Affected list without one under that name. "The kernels of" is accurate.
- **SUSE 42 of 121; "(131 products in all)" dropped**: recount 131 named, 121 with a main kernel package, 42 with a Released one, 73 only Affected. The 131 is still in measure 4's note. Holds.
- **Answer, the factor of 2.00 labelled a post hoc summary**: 0.00777/0.00388 = 2.0026; 13 November is the series' last change to 15 November (factor 1.022). The label is correct and answers R-0079's first suggestion.
- **Next, the 73 SUSE products and the three Real Time products**: recount at 16 November, the products outside the count that list kernel-source-rt as Affected are SLE Real Time 15 SP5 and the Real Time Module 15 SP4 and SP5, three. Holds.
- **Header, Answer and Limits review labels**: R-0077 and R-0078 exist and name Opus 5.5 (claude-opus-5-5), so "All were run on Anthropic's model" holds. Meets R-0079 finding 1, except that each label said a recheck was still to follow, which this note makes stale; changed, below, so the record does not repeat version 0.1's stale label.
- **Corrections paragraph for 0.2**: matches the diff; "No figure changed" is true (no number in the diff differs from 0.1 or from tables.json).

Recount output (tables.json): SUSE named / main / Released / only Affected per read: 124/112/19/81, 124/112/19/81, 127/115/36/73, 127/115/38/73, 131/119/38/77, 131/121/42/73. EPSS day-on-day factors other than 1: 25 Oct 2.352, 30 Oct 1.147, 31 Oct 1.027, 3 Nov 1.663, 13 Nov 1.022. KEV not listed at every read, latest catalogue 2026.11.13. NVD Analyzed at 16 November, lastModified 2026-11-12T18:23:34.890. ADP providers at every read: CVE only.

## Reading the In short as a newcomer

Someone who has never heard of Lighthouse learns: a lab says its AI wrote an exploit for a serious, already fixed Linux flaw; the US list of exploited flaws has not listed it, which does not mean nobody has exploited it; a prediction score jumped once before the post and drifted up to double after it, and the dates do not explain either; and fixes were out from Debian and some SUSE products, but not Red Hat or Ubuntu, at the first look five days after the post, with most now fixed. That is what the record supports, and in neither direction is it easier on Anthropic or on the exploit than the sources allow. Two things snagged: "the CNA" is jargon a newcomer cannot decode, and "reviewed for evidence and for reading" is house language. Both are changed.

Not blocking: the opening is now six sentences against the house guide of two to four, and leans on CISA, NVD and "exploit-prediction score" without saying what they are (these predate 0.2 and were reviewed). Version 1.0's opening could be shortened by moving the SUSE and Ubuntu detail to the Answer, as R-0079 suggested.

## Changes made (studies/LH036/LH036.md)

1. In short: "a day after the CNA's update to the CVE record" became "a day after the kernel's CVE team updated the flaw's official record" (the Linux CNA is the kernel's CVE team; brief, Question and What is already known).
2. In short: "no tracker dates a fix on or before the post." became "no tracker dates a fix on or before the post, though Debian's and SUSE's pages give no dates." This keeps the opening from being read as saying no fix existed before the post.
3. Review labels: the header, the In short ("reviewed against the data and for how it reads, and rechecked"), the Answer and the Limits bullet no longer say a recheck is to follow; they name this recheck (R-0081) as having cleared the resolution.
4. Corrections: a dated paragraph recording these changes; no figure changed.

## Verdict

**Cleared.** Both of R-0079's must-fix findings are met, every changed sentence holds against tables.json and the raw reads, and no must-fix is outstanding. Under AGENTS.md this reading is one, not a chain: the four changes above are listed here and go to no further reader.
