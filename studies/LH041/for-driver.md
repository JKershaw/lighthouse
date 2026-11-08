# LH041: what shared files should gain (for the driving session)

Brief committed at 147e953 before any record was read; read 1 and tables at 1cccfb2; record version 0.1 (unreviewed) in the commit that adds this file.

## schedule/due.csv rows

```
LH041-read-1,LH041,"Read 1 under studies/LH041/brief.md (collect.py --read <label>), tabulate.py with and without --posthoc, draw_figure.py, interim record 0.1",2026-11-08,2026-11-08,done,2026-11-08,"research subagent for the driving session 2026-11-08 (Claude Code, Anthropic cloud)","studies/LH041/LH041.md (0.1, not reviewed); read 2026-11-08T1910Z",
LH041-reviews,LH041,"Evidence review (reproduce the per-wave counts and clusters from data/2026-11-08T1910Z with replay.sh; check each vendor claim against data/prebrief/web; look at figure-reach.svg in light and dark), then the reader-and-inference review; both before any public line",2026-11-09,2026-11-16,open,2026-11-08,,,"the record carries two post hoc readings, labelled; check that no private maintainer is named"
LH041-read-2,LH041,"Read 2: python3 -I studies/LH041/scripts/collect.py --read <UTC label>, then replay.sh <label>; report records OSV added or changed and versions removed since read 1, and whether the post hoc view holds",2026-12-07,2026-12-21,open,2026-11-08,,,"brief: stops after read 2; an amendment adding the vendors' package lists as a second join route (record, Next 3) must be committed before this read if taken"
LH041-record,LH041,"Record version 1.0 after read 2 and the reviews",2026-12-07,2026-12-31,open,2026-11-08,,,
```

## Investigation page, "Where the evidence stands" (investigations/ai-cost-and-spread.md)

> Question 3, the registry worms (LH041, interim and unreviewed, 8 November 2026): of thirteen worm waves security firms name since September 2025, OSV's public malware records identify seven by the firms' own indicators and two more by date. By npm's own clock the two largest reached many separate groups of maintainers within hours, Shai-Hulud 2.0 88 groups in under 15 hours on 24 November 2025 and ChainDrop 13 in under 4 hours on 4 August 2026, while the AntV wave stayed mostly inside one account's 316 packages. Those counts are upper bounds on spread without a person's new act: the records cannot say whether an operator published by hand in between. Every report read says people run these worms. [The record](../studies/LH041/LH041.md).

(Replace "Nothing measured yet." Keep the closing web as the first study.)

## programme.md, Next

> ### Checkpoint, 8 November 2026: the registry worms, dated (LH041 0.1)
>
> LH041 dated thirteen named waves of the token-stealing registry worms from OSV's malicious-package records and npm's publish times, under a brief fixed before any record was read. Interim, unreviewed: seven waves are found by the vendors' indicators and two by date; Shai-Hulud 2.0 and ChainDrop reached 88 and 13 maintainer groups within hours, the AntV wave was mainly one account, and PyPI's clock is gone entirely. Two readings were made after the counts (versions outside a wave's window left out; window joins by ecosystem) and are labelled. Three options: continue with read 2 in December; repair the join for the waves OSV's text does not name (April's two and July's) with the vendors' package lists, by an amendment before read 2; or an outward question, dated counts of the worms' public exfiltration repositories, in aggregate and naming no account. The repair goes first if the reviews agree, because it is cheap and changes what read 2 can say; the outward question goes to proposals.md. No new literature search was run beyond the brief's nineteen sources (sources.md of the study), because the checkpoint changes no design yet.

## sources.md, proposed entries

- **OpenSSF malicious-packages.** OpenSSF's repository of malicious-package reports in OSV format (MAL- ids), merged from sources such as GitHub's malware advisories (`ghsa-malware`), Amazon Inspector, Google's open source security team, kam193, ReversingLabs and OpenSSF Package Analysis; each record names its origins and import times; OSV serves the same records in its exports. Records are one per package, so a package compromised twice holds both episodes' versions. LH041 read the README, contributing guide, schema additions and config on 8 November 2026 and spot-checked 20 records (all matched OSV's copies). https://github.com/ossf/malicious-packages (raw files via raw.githubusercontent.com).
- **The npm registry's package documents.** registry.npmjs.org/<package>: per-version publish times (`time`), which LH041 found kept for many removed malicious versions, the current maintainers, dist-tags and surviving version documents. Read anonymously; deleted packages answer 404. LH041 read 2,198 on 8 November 2026 (84 answered 404).
- **S26 OSV**, add: the exports at osv-vulnerabilities.storage.googleapis.com/<ecosystem>/all.zip carry a GCS generation per version; LH041 read the npm and PyPI exports on 8 November 2026 (223,208 and 12,013 MAL- records). Some MAL- records carry a `published` time at bare midnight (date precision).

## proposals.md, a backlog lead

- The worms' public exfiltration repositories as a dated count: how many public repositories carry each wave's published description ("Sha1-Hulud: The Second Coming", "Shai-Hulud: Here We Go Again" and others the vendors print), by creation date, in aggregate only, naming no account and identifying no victim (the keeper's caution of 8 November 2026). Would date the worms' reach on developer machines and CI, which the registry records cannot see. From LH041's Next.

## Notes for the driver

- The collector's first attempt crashed on a null field after downloading; it was fixed and re-run on the same bytes (record, Method).
- Email addresses were withheld under the keeper's new rule; the vendor pages in 147e953 held addresses and were redacted in 1cccfb2 (history keeps the earlier bytes).
- Model spend of this subagent: price it with `harbour/hb tokens --latest`.
