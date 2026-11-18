title: Kinds for historical schedule rows
kind: working note
date: 2026-11-18

# Kinds for historical schedule rows

**In short.** On 18 November 2026, at the keeper's request, the 136 schedule rows without a kind (129 done, 7 cancelled) were given one, so the site counts their reads and stages. 57 took the kind of later rows of the same dated task; 79 were classified by hand from their task text, a row whose main act is a read being `observe`. By kind: 72 observe, 24 plan, 16 maintain, 11 analyse, 10 review, 3 publish.

The row-by-row result is [kind-backfill-2026-11-18.csv](kind-backfill-2026-11-18.csv) (id, status, kind, rule) and the script that produced and applied it is [kind_backfill_2026_11_18.py](kind_backfill_2026_11_18.py). Only the kind column changed, apart from two references the checker validates once a row is typed, spelled out to the same evidence. Effect seen on the site: the physical-authority investigation now shows its latest read, 13 November.

Correction: the commit that applied this (446a821) gives the split as 60 and 76; the mapping holds 57 by later rows and 79 by hand.
