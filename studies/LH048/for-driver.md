# LH048: for the driving session

Brief written 9 November 2026 by a research subagent; not committed. Nothing outside studies/LH048/ was edited. Commit the brief before the discovery read.

## Rows for schedule/due.csv

```
id,study,task,earliest,latest,status,updated,by,ref,note
LH048-discover,LH048,"Discovery read: collect.py --discover --read <label>; apply the brief's selection rule by hand to the two linked pages, fill selection.json (class, cves, candidates, quoted evidence, rule_applied_at) and commit it before any other source is read for these flaws",2026-11-09,2026-11-12,open,2026-11-09,driving session 2026-11-09,studies/LH048/brief.md,after the brief is on main
LH048-baseline,LH048,"Baseline read: collect.py --read <label> --full, checkpoint",2026-11-09,2026-11-12,open,2026-11-09,driving session 2026-11-09,,after LH048-discover's selection commit
LH048-2026-11-16,LH048,"Monday read: collect.py --read <label>, checkpoint (any rating change, CISA ADP container, EPSS step, KEV listing or changed page, said so in the commit message)",2026-11-16,2026-11-17,open,2026-11-09,driving session 2026-11-09,,
LH048-2026-11-23,LH048,"Monday read: collect.py --read <label>, checkpoint (any rating change, CISA ADP container, EPSS step, KEV listing or changed page, said so in the commit message)",2026-11-23,2026-11-24,open,2026-11-09,driving session 2026-11-09,,
LH048-2026-11-30,LH048,"Monday read: collect.py --read <label>, checkpoint (any rating change, CISA ADP container, EPSS step, KEV listing or changed page, said so in the commit message)",2026-11-30,2026-12-01,open,2026-11-09,driving session 2026-11-09,,
LH048-2026-12-07,LH048,"Monday read: collect.py --read <label>, checkpoint (any rating change, CISA ADP container, EPSS step, KEV listing or changed page, said so in the commit message)",2026-12-07,2026-12-08,open,2026-11-09,driving session 2026-11-09,,
LH048-interim,LH048,"Interim checkpoint after the read of 7 December: measures 1 to 4 to date, model disclosure beside the model line",2026-12-07,2026-12-11,open,2026-11-09,driving session 2026-11-09,,
LH048-2026-12-14,LH048,"Monday read: collect.py --read <label>, checkpoint (any rating change, CISA ADP container, EPSS step, KEV listing or changed page, said so in the commit message)",2026-12-14,2026-12-15,open,2026-11-09,driving session 2026-11-09,,
LH048-2026-12-21,LH048,"Monday read: collect.py --read <label>, checkpoint (any rating change, CISA ADP container, EPSS step, KEV listing or changed page, said so in the commit message)",2026-12-21,2026-12-22,open,2026-11-09,driving session 2026-11-09,,
LH048-2026-12-28,LH048,"Monday read: collect.py --read <label>, checkpoint (any rating change, CISA ADP container, EPSS step, KEV listing or changed page, said so in the commit message)",2026-12-28,2026-12-29,open,2026-11-09,driving session 2026-11-09,,
LH048-2027-01-04,LH048,"Last Monday read: collect.py --read <label> --full, checkpoint; the study stops here",2027-01-04,2027-01-05,open,2026-11-09,driving session 2026-11-09,,end date fixed in the brief
LH048-record,LH048,"Record (version 1.0): measures 1 to 4 per flaw and per chain, unknowns kept unknown, the linked set apart; model disclosure on the record; a piece only if it earns one, with its reviews",2027-01-05,2027-01-15,open,2026-11-09,driving session 2026-11-09,,
```

Also mark the row `five-chains-brief` done with ref studies/LH048/brief.md.

## Line for investigations/model-found-bugs.md, question 3

Replace "Brief to come." with:

([LH048](../studies/LH048/brief.md), brief fixed 9 November 2026.) The post names only two flaws by number, CVE-2026-33096 (Windows) and CVE-2026-98432 (Linux); the Chrome and Safari flaws are matched, by a rule fixed before reading, to the release notes the post links, and the Android chain has no identifier. Mondays to 4 January 2027, the record by 15 January.

(Also add `- studies/LH048/brief.md` to the page's `studies:` list.)
