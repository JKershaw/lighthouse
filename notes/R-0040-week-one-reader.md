# R-0040: reader stage for "A week after two fixes"

## What a reader would believe, written before reading the record

**Principal finding, said back.** PHP and Node.js both shipped security fixes on 21 October 2026. A week later, on 28 October, the fixed version (or something newer) made up more than half of the counts for every fixed Node.js line and every fixed PHP branch. For Node.js this was 54, 72 and 65 per cent of downloads; for PHP, Censys counted 52 to 79 per cent of version-showing services as patched, with 8.4 and 8.5 ahead of 8.2 and 8.3. Separately, 24.4 million PHP services, 54 per cent of those showing a version, ran branches that no longer get fixes.

**Observed:** daily download shares from nodejs.org and Censys's daily patched shares, plus how many days each took to pass half (two days for Node.js and PHP 8.4/8.5, six for PHP 8.2/8.3). Also the unfixed tail: Packagist's 10 per cent from PHP 8.1 or older, and 12 to 16 per cent of Node.js downloads from lines that got no fix. **Explained:** a Censys jump in versionless services on 23 October, put down to a change in how it detects PHP; W3Techs's low figures, put down to it visiting sites only about once a month. **Caused:** nothing is claimed. The piece says outright that it does not know why October beat July for Node.js, or which software's users are quicker.

**Limits a reader would notice:** downloads are requests, not installs. Censys's shares are floors, both from rescan lag and from distributions that patch without changing the version number. Most PHP services hide their version. The July comparison was picked after seeing the data. The Python numbers come from a different count. It is one week of data, and the piece is a draft to be revised at a month.

## What the round establishes

The figures in both pieces match the records (LH033.md, LH034.md) and R-0039's recomputation from the raw reads. I checked whether the PHP shares could be right while the reading of them as spread is wrong. My checks are in studies/LH034/review/R-0040_checks.py and its .txt.

- **Day 2 is not a detection artefact.** Censys's total jumped on 23 October, but the services it counts in the fixed branches grew only from 18.33 to 18.87 million that day. The jump came in versionless services, and on days 1 and 2 each branch's patched count rose as its unpatched count fell, by 0.6 to 1.3 million a day.
- **The late rise is not mainly new services.** From day 4 on, about two thirds of each day's patched gain is matched by growth in the branch rather than by a fall in unpatched services. Censys's stated rule ("seen on an affected version and later on a fixed one") makes those day-to-day changes consistent with real moves from affected to fixed, while newly seen services join the branch as affected.
- **A plainer measure agrees.** Censys's current snapshot, as of 29 October, puts 56.8 per cent of 8.2 services and 56.0 per cent of 8.3 services on the fixed release itself. That is above the day-7 figures, so "passed half" holds on this measure too.

The Node.js figures follow the brief's rule. The piece also discloses the dip in line 22 and v26.13.0's 18 points in line 26. Neither piece claims a cause.

## Material claim problems

1. **The July comparison leaves out the line that went the other way.**
   - **Passage:** articles/a-week-after-two-fixes.md, "lines 22 and 24 were higher in October's first week than in July's. We do not know why." The record's Answer leaves line 26 out in the same way.
   - **Evidence:** LH034.md, July table and the post-hoc alignment. Line 26 stood at 89.0 per cent on July's day 7 (89.4 aligned by posting day) against 64.7 per cent on October's day 7. The record says line 26 "was lower by day 7".
   - **What a reader takes away:** that October's release spread faster than July's on this instrument. That holds for two of the three lines.
   - **Resolution:** add "line 26, the smallest, was lower (65 per cent against 89)", in the piece and in the record's Answer.

2. **The short form and the summaries drop the backport caveat for the unfixed tail, while keeping it for the patched shares.**
   - **Passage:** articles/short/a-week-after-two-fixes.md, "24.4 million PHP services, more than half of those showing a version, ran branches PHP no longer fixes". The same statement appears in both summary lines and the headline.
   - **Evidence:** LH033.md, Limits ("Status is based on reported versions, so counts are an upper bound"). The full piece itself says "Some may be protected by a Linux distribution". In R-0040_checks.txt, 6.64 of 7.85 million 7.4 services (84.6 per cent) report 7.4.33, the last upstream 7.4 release, which is also a version distributions ship. Whether they carry fixes is unmeasured.
   - **What a reader takes away:** 24.4 million services left exposed.
   - **Resolution:** add to the short form, "as their versions report them; some may be patched by distributions under the old number, which we have not measured".

## Readability

- The short form asks how far a fix spreads and says the counts "gave an answer", then says neither count measures protection. "Gave two partial views" would match the rest of the piece.
- In the figure, the labels for Node.js 22 and the Python median crowd each other. The piece's text never explains the Python median line.
- The parenthetical on v26.13.0 would read more easily as: "the fixed release itself was 46 of line 26's 65".

## Next step

Continue as the records plan:
- reads on Mondays and Thursdays;
- the day-30 reads on 21 and 22 November, including the Node.js re-read of days 0 to 7, which tests for revisions;
- W3Techs on 1 November and 1 December.

These reads will show where the shares level off, and whether the older PHP branches close the gap. Two questions are out of their reach:
- whether Censys's population changes or its rescan lag shape its curves;
- how much of the unfixed tail distributions protect.

The July comparison cannot be tested again, since both releases are past.

Two additions would help, neither of which needs a change of direction:
- at each read, set the current snapshot's share on the fixed release (from `branch_versions`, already kept in the retained data) beside `branch_history`;
- ask Censys, or read its methods, for how it counts a service first seen already fixed.

Waiting for the 21 and 22 November reads is the right course, and no new study is needed now.

## Resolution, by the driving session

Both material problems fixed. (1) The piece now adds that line 26, the smallest, was lower by the seventh day than after July's release, 65 per cent against 89, and LH034's Answer says the same (64.7 against 89.0). (2) The summary of the full piece, the short form and LH033's Answer now say the 24.4 million run unfixed branches "as their versions report them; some may be patched by Linux distributions under the old number, which we have not measured"; the full piece's body already said so. The title keeps "ran branches PHP no longer fixes", which is what the versions report, with the caveat beside it in the summary. Readability suggestions not taken in this round. The next-step advice (set the snapshot's fixed-release share beside the history; ask how Censys counts a service first seen fixed) goes to the continuation plan; asking Censys would be contact with a third party and waits for the keeper.
