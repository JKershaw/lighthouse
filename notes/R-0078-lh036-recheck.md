# R-0078: LH036 interim, recheck of the resolution of R-0077

The one fresh reading (AGENTS.md step 4) of what the driving session wrote to resolve notes/R-0077-lh036-interim.md. Reader: Claude Opus 5.5 (claude-opus-5-5), subagent, 16 November 2026, no network. Cost: unknown, not measured; unknown is not zero. The study follows an Anthropic post and this reader runs on an Anthropic model; a review contribution, not independent confirmation.

Version read: git HEAD 9f1de7d775962e046d26ae762ec836752fdb7aea; studies/LH036/LH036.md sha256 05cfc04bdd2eb9edaa8dbf8ed0cf850a89729a3bc419baf0b7cec47043231084. After this recheck's changes (below): sha256 1d2784c66200d57447b3b7c50c778e88d03b34f3bc7a988de31a391dcc270ef7, uncommitted.

Read: the In short, the Answer's Signals sentence and the last Corrections paragraph as changed in 9f1de7d; studies/LH036/brief.md measure 1 (the step definition); studies/LH036/review/check_signals-output.txt, which R-0077 computed from the raw EPSS, KEV, CVE and NVD bodies in studies/LH036/data/read-*/.

## Figures

- EPSS factors: 0.00445/0.00388 = 1.147 (30 October) and 0.0076/0.00457 = 1.663 (3 November): 1.15 and 1.66 hold. 25 October: 0.00165 to 0.00388, factor 2.352, the only day-on-day factor of two or more; no fall anywhere.
- KEV: the 16 November read holds catalogue 2026.11.13, dateReleased 2026-11-13T20:24:18Z, CVE not listed: "latest catalogue read, 13 November" holds.
- NVD: Undergoing Analysis at the 12 November read (14:17Z), Analyzed at 16 November with lastModified 2026-11-12T18:23:34Z; "12 November, by NVD's clock" holds.

## Use of "step"

The brief defines a step as a day-on-day change by a factor of two or more. The Answer's "rose without a step" is correct. The In short's plain-words "only rise by a factor of two came on 25 October" was not: read without "day-on-day", it is false, because after the post the score went from 0.00388 (27 October) to 0.00777 (13 November), a factor of 2.003 (python3 arithmetic on the values above). The Answer also gave only the two larger rises without the cumulative effect, which understated the post-E2 movement the R-0077 finding was about.

## Other overreach

"no CISA container or NVD score appeared" could be read as no score on NVD's record, which shows the CNA's 9.8 (Secondary) at every read; the next sentence says "no score of its own", so the shorthand was ambiguous rather than wrong. No other new overreach; the Corrections paragraph matches what changed and "No figure changed" is true.

## Changes made (studies/LH036/LH036.md)

1. In short: "only rise by a factor of two ... rose again, by smaller factors, after it" became "only one-day rise by a factor of two or more ... after the post smaller daily rises together about doubled it by 13 November"; "latest catalogue read (13 November)" became "latest catalogue read, of 13 November".
2. Answer, Signals: states the brief's rule (day-on-day, factor of two or more), calls 1.15 and 1.66 the two larger daily rises, and adds that with two smaller ones they took the score from 0.00388 on 27 October to 0.00777 on 13 November, a factor of 2.00 over 17 days (derived); "NVD score" became "score of NVD's own".
3. Corrections: a paragraph recording these changes and that the main claim now reads narrower (no step after the post, but a doubling over the weeks after it).

## Verdict

Cleared, with the changes above made by this reader; per step 4 they are listed here rather than sent to another reader. The piece goes on to the reader-and-inference review.
