# For the driver: Amendment 1 rows

**In short.** The brief's Amendment 1 (P-0031) schedules one more read, of the ministry's next monthly ground-robot notice, ending with the pilot. Add the row below to schedule/due.csv and close the amendment's own row. Nothing here is committed; the amendment must be committed before the panel lock on 18 November.

Add:

```
LH050-ukraine-notice-dec,LH050,"Under Amendment 1: gate and retain Ukraine's Ministry of Defence next monthly ground-robot mission notice (November figure) in English and Ukrainian as published; log reads.csv; compare each month with the October notice (PA-S30, PA-S31) and record revisions without resolving them; each count the ministry's claim of missions, not armed use, autonomy or civilian effect; working-log line; at most two document reads",2026-12-01,2026-12-24,open,2026-11-13,"keeper-requested follow-up to the 13 November run (Claude Code, Anthropic cloud)",studies/LH050/brief.md,"Amendment 1 (P-0031, agreed by the keeper 13 November 2026); ends with the pilot; if no notice is readable by 24 December record the read as missing, not as no notice"
```

Update the existing row `LH050-amend-ukraine` when the amendment is committed:

```
LH050-amend-ukraine,LH050,"Dated amendment to LH050 admitting Ukraine's Ministry of Defence monthly ground-robot mission notices as a panel candidate, under the gate's conditions in notes/horizon/2026-11-13T1452Z.md; keep the two notices as published; committed before the panel lock",2026-11-13,2026-11-17,done,<commit time UTC>,"keeper-requested follow-up to the 13 November run (Claude Code, Anthropic cloud)",studies/LH050/brief.md,"Amendment 1 written about 15:30 UTC; October notice (English, Ukrainian) and August notice kept at read label 2026-11-13T1530Z (reads LH050-R037 to R039, claims LH050-C062 to C078); outside the 30-document baseline bound, 3 of the amendment's 5 reads; unreviewed"
```

Panel lock (row `LH050-panel-lock`, by 18 November): the amendment allows at most two endpoints for this series (English and Ukrainian), inside the 12-endpoint cap. Whether to include them, and which index or notice URL, is the lock's choice; the gate decision for each must be taken then.
