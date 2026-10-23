# Independent evidence review of the LH032 measurement repair

23 October 2026. Reviewer: a separate Codex agent (GPT-6.1 Sol), asked to review the source, history interpretation and repaired instrument. This review uses the pinned NCSC-NL source commit `2fdc314ded280d18868d13d2f33d092a15e5a231`, not a new daily observation. No vendor page was requested by this reviewer. Model spend is unknown. The writer's repair and this review deliberately reuse the original outcomes; agreement is a review, not independent observation of product or vendor behaviour.

## Independent reproduction

The retained [check_source.py](check_source.py) does not import the production analyser or execute upstream code. It independently reads the source graph, checks source-fragment and compiled-inventory equality, projects source package names into the published Markdown representation, and checks every package's identity, two statuses and URL presence against the alphabetized tables. It then scans the mainline's first-parent history and compares the result with the original LH032 output. Its table scanner counts preceding backslashes rather than splitting every pipe.

Replay, from the repository root, choosing an output file that does not already exist:

```sh
python3 studies/LH032/review/check_source.py /path/to/php2shell /tmp/lh032-independent-check.json
```

The retained [independent-check.json](independent-check.json) reproduces:

- Fourteen source fragments, 2,286 graph elements, semantic equality with the compiled inventory, and 751 package identities matching the Markdown tables.
- CVE-2026-109618: 109 Fix, 222 Vulnerable, 389 Investigation, 30 Not vuln and one blank. CVE-2026-109619: 109 Fix, 220 Vulnerable, 390 Investigation, 31 Not vuln and one blank.
- **749 entries linking an HTTP(S) URL**, and 202 entries with an HTTP(S) reference typed by the source as `securityAdvisory`.
- Sixty-five first-parent commits, 66 changed first-listed clocks, 117 changed first-resolution clocks, and 308 surviving entries with a status change.
- First recorded Fix or Not vuln for 141 surviving identities: 50 in the first twelve hours after the source-reported PHP release, 18 in hours twelve to twenty-four, one in hours twenty-four to thirty-six, and 72 in hours thirty-six to forty-eight. None is before that release clock under this history rule.

**Correction to this reviewer's initial report:** I initially repeated 737 entries with any URL from the original summary without independently verifying that figure. The separate source check establishes 749. The original pipe splitter shifts columns in twelve rows containing escaped pipes before the links column. The retained independent output names all twelve corrected URL-presence flags. This correction does not change the status totals.

## Findings and required interpretation

Walking every reachable commit as one sequential history crosses merged side branches. A side-branch status can precede the mainline merge, and switching between branch trees can manufacture reversions. The first-parent repair is appropriate for the chosen mainline-list clock. It changes the reported interval evidence and removes the original apparent pre-release Not vuln observation.

The repaired clock is a **mainline committer timestamp**. Git objects do not establish when a commit or branch became publicly readable, so neither the original nor repaired result measures first public notice, vendor release, deployment, exposure or compromise. The 65 mainline commit timestamps at this pinned revision have no reversals; that fact does not guarantee clocks in future source history.

The original script also omitted the notes and full links fields, omitted last-change clocks for fields other than statuses, silently accepted supplier/product collisions and permitted same-label overwrites. The repair retains those fields and clocks, checks source identities and per-package statuses and versions, pins a revision, and refuses existing read output paths. Original baseline outputs must remain unchanged. Supplier/product identity is the protocol unit; a rename can appear as a new identity and must not be interpreted as a newly added real-world product.

Any URL, a source-typed advisory URL, and a source-checked vendor claim are three different measurements. The source's `securityAdvisory` type makes the late deterministic sample feasible but does not establish that the link is an actual advisory or that its content supports the list's classification. The sample selection is explicitly after known list outcomes, covers five entries sharing four pages, and cannot retroactively verify past vendor states.

## Review status

**Final review: no material must-fix finding remains.** I read the final production scripts, amendment, study version 0.2, programme/log/continuation changes and the late advisory findings. I reran all four regression tests and the pinned replay successfully. The parser now handles delimiters following both odd and even backslash runs; the fixture also covers the merged-branch clock, pinned-head replay, notes/link-only changes, per-package status disagreement, conflicting identities and overwrite refusal. The pinned replay reconstructs all four corrected outputs and verifies the original retained list files against git objects.

I independently decompressed all four retained late responses, verified their compressed and response SHA-256 values and lengths against the read log (464,810 response bytes total), and read the visible text of the three intended source pages. AWS is a placeholder. Arch's notice supports the two PHP package fix versions. BookStack's notice describes repairing the hosting PHP runtime, gives the four upstream fixed versions, and qualifies its discussion of the related configuration issue. Their source dates and BookStack's stated 23 October 13:00 UTC last update match the findings. These are statements checked against bytes, not confirmation of the software's behaviour. I did not classify the unintended Bref issue or make any external GET.

The case-sensitive selection bug is a real protocol deviation, explicitly preserved in the final amendment and findings: aaPanel remains unattempted and the late sample incomplete. The final text clearly distinguishes three supported entries from two readable notices, the inaccessible intended entry, the unattempted intended entry, and the unclassified unintended response. No further request is needed to establish what this failed selection actually observed. The review plan's git commit `4be567e` precedes the late source checks.

The repair author reports the site tests (15 passing) and Eleventy build passed; those are the author's validation, rather than tests rerun by this reviewer. The revised record and working summaries state the measurement correction at the same certainty. I requested explicit attribution of version 0.2's repair to Codex beside the original Claude author; that is an authorship clarification, not a changed finding. No article revision is proposed by this measurement review.
