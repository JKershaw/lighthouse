# R-0139: reader review of the week-one revision, stage one

## What a reader would believe, written before reading the record

**Principal finding, said back.** After PHP and Node.js shipped security fixes on 21 October 2026, both public counts rose fast and then mostly stopped rising after about two weeks. By 20 November, Censys counted roughly three quarters to nine tenths of versioned PHP services in each fixed branch as patched. On nodejs.org, about two thirds to almost all of each line's downloads were at the fix or newer, but only if three November releases count as fixed. Below all of this, over half of versioned PHP services, 22.5 million, ran branches PHP no longer fixes.

**Observed.** Daily Censys tallies by branch and daily nodejs.org download counts by version; three new Node.js security releases on 11 November; one Google bulletin saying some Apigee portals had no packaged fix.

**Explained.** The late PHP rise in three branches came mostly from fewer services counted, not more patched. The late Node.js rise came mostly from more downloads at or above the fix, not fewer old downloads. A reader takes both as counting effects, not people updating late. The crossing with Python is put down to how the two kinds of count behave, labelled as untested.

**Caused.** Nothing is claimed as caused. The PHP 7.3/7.4 portals are unfixable only on the vendor's word.

**Limits a reader would notice.** Patched shares are floors (distributions backport). Downloads are requests, not machines. The Node.js headline depends on a rule chosen after seeing the data and an unchecked assumption. Where the missing PHP services went is unknown. The July comparison flips with the rule. Collection has closed, so the post hoc readings won't be tested.

## Stage two: against the records

Read: studies/LH033/ and studies/LH034/ (records, briefs and amendments, record_v1.json, review/ outputs, studies/LH034/oneoff-2026-11-25/ note, log and kept bodies), investigations/software-updates.md, programme.md's Next, proposals.md P-0045, studies/LH037/brief.md and LH037's checkpoint of 2 November for GCP-2026-072. Calculation kept as studies/LH033/review/R-0139_not_patched.py with its output, R-0139_not_patched.txt (from data/record_v1.json only).

Combined disclosure check (schedule/research-safety.md): clears. Aggregate public counts, public advisories and release notes; no hosts, accounts, people or mechanism detail; the figure and captions add nothing beyond the records.

### What the round establishes

Every figure I checked in the piece, the short form and the figure matches the records (LH033 1.2, LH034 1.1), and the Apigee quotation matches LH037's checkpoint of 2 November. The measurements and the explanations line up. PHP's late rise in 8.2, 8.3 and 8.5 is mostly a smaller branch count. Node.js's late rise under the amended rule is mostly added downloads at or above the fix. Both are labelled as worked out after the counts were seen, and neither claims a cause. The pieces carry the floor, the request-not-machine limit and the post hoc rule with its assumption, as the records state them. The announcements read on 25 November confirm that the three versions are real security releases of 11 November and leave carry-forward unstated. The piece says exactly that, and says the read is unreviewed. So the stage-one reading is supported, with one exception.

### Material claim problems

1. **"Not from fewer left behind" is wrong for PHP.**
   - **Passages.** The short form's summary (a-week-after-two-fixes-rev-short.md, front matter): "what rose after came mostly from fewer PHP services counted and more Node.js downloads of newer versions, not from fewer left behind". The revision line in a-week-after-two-fixes-rev.md says the same: "what rose after came mostly from fewer PHP services counted in three branches and more Node.js downloads at or above the fix, more than from fewer left behind".
   - **Evidence.** From day 14 to day 30, services not counted patched fell in every PHP branch: by 367,170 in 8.2 (21.8 per cent), 476,341 in 8.3 (20.1), 169,375 in 8.4 (25.8) and 101,466 in 8.5 (26.0). See review/R-0139_not_patched.txt, from LH033 record_v1.json `m1_counts`. Arithmetically, the services that left the three shrinking branches were not-patched ones. In PHP the late rise is exactly fewer left behind *in the count*: not more patched services. Where those services went is unknown. The clause is right only for Node.js, where downloads below the fix fell 4.0 to 6.5 per cent.
   - **Resolution.** Split the clause. PHP: "mostly from fewer services counted in three branches, nearly all of them ones not counted patched, rather than more patched ones; where they went is unknown". Node.js: "mostly more downloads at or above the fix rather than fewer below it". Optionally add one clause to the body paragraph saying that the services leaving the count were ones not counted patched.

No other material problem.

### Readability

1. Node.js paragraph, "downloads of the October releases fell far more than downloads of older versions". Under the rule as written, the listed versions at or above the fix include v24.22.2 and v26.13.0, which are not October releases (LH034, Answer). Say "listed releases at or above the fix".
2. The late-rise paragraph says the added downloads arrived "with the new versions". The reader learns only two paragraphs later that these were November security releases. One clause there would let the reader see the rise as a new release being fetched, not October's fix spreading.
3. Figure, top panel. From about day 13, line 22's solid line and the Python median overlap, and the right-hand labels are packed tight. Spacing the labels or lightening the median would help. It reads acceptably in both light and dark themes.

### Next step

Release after the one wording fix, with the usual single fresh reading of that change. Then let the week-one line rest, apart from what is already scheduled.
- **P-0045 (WordPress) and LH033's measure 6.** These test how much W3Techs's monthly survey lag explains. That matters for any W3Techs or WordPress-against-PHP sentence. It cannot tell apart the explanations this piece relies on: Censys's shrinking branches, and Node.js's counting rule. The 1 December point arrives 1 to 3 December. Doing it is worthwhile, but it doesn't bear on this piece.
- **LH037.** Vendor statements to 3 December can name branches that vendors carry or backport, as Apigee did. They can't size the backport floor or say where Censys's services went.
- **The step that would most improve the PHP explanation** is the one LH033 itself names and doesn't make: comparing the branch-by-version tables across the retained reads of day 14 and day 30. It is available now, offline and cheap. It would show which versions lost services. My approximate post hoc check points the same way: all PHP services Censys counted fell by about 5 million (about 4 per cent, from about 120.6 to 115.2 million) while the share with no version stayed at 62.0 to 62.3. That is more consistent with services dropping out of the scan or going offline than with services hiding their version. Any such analysis is post hoc. Collection has closed, so nothing can test it on fresh data, and it should be labelled that way. It doesn't need to hold up release.
- **Node.js carry-forward.** Another read of release notes would not settle whether the November releases carry October's fix. It is ordinary practice, and the pieces already label it unchecked, so it isn't worth a further step.
