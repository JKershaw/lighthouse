# LH045: for the driving session

What the shared files should gain from LH045 (brief: [brief.md](brief.md), protocol 0.1 with amendment 0.2; first checkpoint: [checkpoints/2026-11-08.md](checkpoints/2026-11-08.md)). Written 8 November 2026. Commits c08091c (brief, collectors, pre-brief reads), 5a6251a (amendment 0.2, Epoch read 0, census 0a) and the commit carrying this file (census 0, checkpoint).

## schedule/due.csv rows

```
id,study,task,earliest,latest,status,updated,by,ref,note
LH045-census-1,LH045,"IETF census 1, the last before IETF 127: python3 -I studies/LH045/scripts/collect_ietf.py --read <UTC label>; check completeness only (all 200, no unread page); a line in the next checkpoint",2026-11-12,2026-11-13,open,2026-11-08,,,brief: census rule 0.2; no analysis of the census
LH045-census-2,LH045,"IETF census 2, once after IETF 127 ends on 20 November: python3 -I studies/LH045/scripts/collect_ietf.py --read <UTC label>",2026-11-23,2026-11-27,open,2026-11-08,,,brief: the last census; no census after it
LH045-epoch-2026-11-15,LH045,"Epoch weekly read 1: python3 -I studies/LH045/scripts/collect_epoch.py --read <UTC label>",2026-11-15,2026-11-17,open,2026-11-08,,,brief: weekly to 3 January 2027 at most
LH045-epoch-2026-11-22,LH045,"Epoch weekly read 2: python3 -I studies/LH045/scripts/collect_epoch.py --read <UTC label>",2026-11-22,2026-11-24,open,2026-11-08,,,
LH045-epoch-2026-11-29,LH045,"Epoch weekly read 3: python3 -I studies/LH045/scripts/collect_epoch.py --read <UTC label>",2026-11-29,2026-12-01,open,2026-11-08,,,
LH045-epoch-2026-12-06,LH045,"Epoch weekly read 4: python3 -I studies/LH045/scripts/collect_epoch.py --read <UTC label>",2026-12-06,2026-12-08,open,2026-11-08,,,
LH045-epoch-2026-12-13,LH045,"Epoch weekly read 5: python3 -I studies/LH045/scripts/collect_epoch.py --read <UTC label>",2026-12-13,2026-12-15,open,2026-11-08,,,
LH045-epoch-2026-12-20,LH045,"Epoch weekly read 6: python3 -I studies/LH045/scripts/collect_epoch.py --read <UTC label>",2026-12-20,2026-12-22,open,2026-11-08,,,
LH045-epoch-2026-12-27,LH045,"Epoch weekly read 7: python3 -I studies/LH045/scripts/collect_epoch.py --read <UTC label>",2026-12-27,2026-12-29,open,2026-11-08,,,
LH045-epoch-2027-01-03,LH045,"Epoch weekly read 8, the last: python3 -I studies/LH045/scripts/collect_epoch.py --read <UTC label>",2027-01-03,2027-01-05,open,2026-11-08,,,brief: no read after this without a new brief or the keeper's extension
LH045-checkpoint-2,LH045,"Checkpoint 2 after census 2: completeness of censuses 0 to 2 and Epoch reads 0 to 3 (what was kept and what failed, not what it shows); studies/LH045/checkpoints/<date>.md with an In short opening",2026-11-27,2026-12-01,open,2026-11-08,,,
LH045-checkpoint-3,LH045,"Closing checkpoint after the last Epoch read: completeness, then hand the archive and the named questions E1 to E4 and I1 to I4 to a proposal for a later study that fixes its own brief before reading the captures",2027-01-04,2027-01-09,open,2026-11-08,,,brief: the study ends here
```

Done today and not needing rows: the brief (c08091c), Epoch read 0, census 0a and census 0, and the first checkpoint. If the schedule records done work, add `LH045-capture-0` as done on 2026-11-08 with ref `studies/LH045/checkpoints/2026-11-08.md`.

A read is cheap (8 GETs to epoch.ai, about 42 to datatracker.ietf.org) and needs no analysis: run the command, check the read log is all 200, commit `studies/LH045/data/`. A read that finds robots.txt or terms changed to forbid it stops that part (brief, Resources and stop).

## The investigation page (investigations/ai-cost-and-spread.md)

Under "Where the evidence stands", or a new short "Records being kept" section:

> **Records being kept, from 8 November 2026** ([LH045](../studies/LH045/brief.md)). Two public records that overwrite themselves are being kept so a later study can read them: Epoch AI's openly licensed estimates of AI data centres (96 sites, with the update log it still serves back to March 2026), weekly to 3 January 2027, and a dated census of IETF drafts on agents, agent discovery, bot authentication and AI preferences, taken on 8 November (604 drafts by a fixed name and group rule), again before IETF 127 opens on 14 November and once after it ends. Daily compute prices were dropped: the free series checked (Silicon Data's H100 index, DRAMeXchange's memory spot prices, Shanghai Metals Market's Chinese GPU rental indices) all forbid keeping or republishing their figures, so the cost strand still has no price instrument. An estimate of a data centre's compute is not load on shared infrastructure, and a draft is not adoption.

## programme.md, Next

> **LH045, keeping records before they roll over (started 8 November 2026 under the keeper's assignment at the review).** Captures only: Epoch AI's data-centre records weekly to 3 January 2027, and an IETF draft census on 8 and 12 or 13 November and once between 23 and 27 November, with checkpoints by 1 December and 9 January. The brief names eight questions (E1 to E4 on whether Epoch's log rolls over and how its estimates move; I1 to I4 on what IETF 127 changed among the drafts) for a later study to test on captures nobody has analysed. The compute-price lead was dropped on its sources' terms; whether to seek a publisher's consent is the keeper's call (below).

## sources.md entries (numbers to be assigned by the driving session)

> ### S__ Epoch AI, AI data centers
>
> Epoch AI's hub of estimated AI data-centre construction, power, compute (H100 equivalents), cost and chips, drawn by Epoch from satellite imagery, permits and public documents, with an update log and CSV and ZIP downloads. CC BY 4.0: "free to use, distribute, and reproduce provided the source and authors are credited"; credit Epoch AI, 'AI data centers', published online at epoch.ai. On 8 November 2026 the hub covered 96 sites, the downloads were stamped 6 November 2026, and the log page's data carried entries from 14 March 2026; earlier versions of the CSVs are not offered. robots.txt allows the data paths and disallows /assets/. LH045 keeps it weekly to 3 January 2027 (studies/LH045/brief.md). Read 8 November 2026.
>
> https://epoch.ai/data/data-centers
> https://epoch.ai/data/ai-data-centers/updates

> ### S__ IETF Datatracker API
>
> The IETF's read-only API over Datatracker's database (Internet-Drafts, groups, states, authors, meetings), anonymous and in JSON, described at datatracker.ietf.org/api/. A draft is filed under a working group only once the group adopts it; until then it is an individual draft whose name may carry the target group's acronym. Author records carry affiliations as authors state them, and email addresses, which LH045 does not keep. robots.txt disallows only /doc/pdf/. Internet-Drafts are governed by the IETF Trust Legal Provisions (5.0). IETF 127 runs 14 to 20 November 2026, with the draft cutoff 13 days before. LH045 takes a census from it (studies/LH045/brief.md). Read 8 November 2026.
>
> https://datatracker.ietf.org/api/

> ### S__ Compute and memory price pages whose terms forbid keeping their figures
>
> Recorded so later sessions need not re-read them: Silicon Data's GPU rental indices (silicondata.com; terms forbid storing site contents "in a database or retrieval system" or reproducing them without written consent; about 30 days public, full history paid), DRAMeXchange's DRAM and NAND spot prices (TrendForce; terms forbid reproducing or publishing any materials without written consent; current session only), Shanghai Metals Market's computing-power indices (metal.com; its notice forbids copying "single prices" for any purpose without written consent), Vast.ai's GPU marketplace (terms forbid automated retrieval and any index or benchmark built from it) and Microsoft's Azure Retail Prices API (the Microsoft APIs Terms of Use forbid building databases or copies of API data). A single attributed figure may be quoted in a dated sentence; no series may be kept. Read 8 November 2026 (studies/LH045/brief.md, Part A).

## proposals.md

- Under L-0011, L-0019 and L-0012 in the leads list: "Taken up 8 November 2026 as LH045 (studies/LH045/brief.md), started under the keeper's assignment at the review. L-0011 dropped on its sources' terms (none permits keeping a series); L-0019 and L-0012 being kept, to 3 January 2027 and 27 November respectively."
- **A new proposal, waiting for the keeper:** *A price for compute that Lighthouse may keep.* The cost strand has no price instrument because every free daily series checked forbids retention. Two routes, both outside what a session may do alone: ask one publisher (Silicon Data's public index is the closest fit) for written consent to keep and publish its daily index with attribution, which is contacting a third party; or find an openly licensed price series (none found in this bounded check: five sources read, 8 November 2026). Kind: repair of an instrument for an active investigation. Cost: small once permitted. Why: the charter names "the compute behind them", and price is the one daily public trace of it the sweep found.
- **For the later study, at the closing checkpoint:** a proposal to test E1 to E4 and I1 to I4 on the LH045 archive, drafted at checkpoint 3 (row LH045-checkpoint-3).

## For a reviewer to look at first

- Part A's drop rests on reading each source's terms as forbidding a public archive. Silicon Data's and Shanghai Metals Market's clauses are explicit; DRAMeXchange's forbids publishing and distributing rather than private storage, which is decisive only because Lighthouse's repository is public. Microsoft's API terms may not be meant to bind the unauthenticated price API; it was treated as a wall under the keeper's caution of 8 November.
- Amendment 0.2 changed the census rule after census 0a's per-query counts were seen (no dates, states or abstracts were looked at); census 0a is kept.
- Author emails are redacted at capture, a deliberate departure from raw retention; the read log's hash is of the bytes received.
- The update log parser reads Epoch's page data (an Astro component's props); if Epoch changes its site, `updates.csv` will be marked partial and the raw page still kept.
