# Lighthouse Harbour Workspace Plan

North star, budget rule, seed tickets and periodicals

Founding edition 0.2 (draft) | 25 September 2026 | LH F06

This plan opens a Lighthouse workspace in Harbour. It is an operational draft: the tickets below are text to file, the budget is a decision record to adopt, and the periodicals are a schedule to configure. Nothing here is filed, funded or scheduled until the steward does it. The cost figures it quotes come from Harbour's own papers and are planning assumptions until the ledger replaces them.

## What the workspace is

The Lighthouse workspace is Harbour's coordination layer for Lighthouse work. It is also the first contained instance of the phenomenon Lighthouse studies: an autopilot that files, works and closes tickets toward a north star, within a budget, leaving residue that enables its next run. Every study that uses this workspace's records discloses that overlap. The workspace's own consumption is recorded from the first ticket, split by involvement class, so that autonomous work and human-steered sessions are never confused.

## North star

**Title.** Lighthouse publishes one reproducible observation of a known workflow and an honest account of its limits.

**Body.** The first durable contribution named in LH F01. Work under this north star produces instruments with known limits, one calibrated observation of a Harbour workflow, and publications a reader can trace to evidence. Task completion is not progress; the completion evidence below is.

**Completion evidence.** All three must hold.

1. **Content worth reading.** At least one Lighthouse publication that the steward reads to the end and would forward to someone outside the project. The release record carries the date it was read.
2. **Real phenomena.** At least one instrument calibrated against a known event, with detection and timing error reported, and at least one result reproduced by someone other than the analyst, as LH F04's completion criteria require.
3. **Wider research.** Every published study positions its finding against at least one external source, from the LH F02 list or beyond, and says what it adds, confirms or contradicts.

Until all three hold, the budget stays in its starting band. When they hold, the steward records the next band in a new decision record.

## Budget rule

```
decision: D-0001                  date: 2026-09-25      owner: founding steward
question: How much may the Lighthouse workspace spend on autonomous work,
  and what happens at the limit?
options considered: hard ceiling; open budget with periodic review;
  target band with a tripwire
choice: target band with a tripwire
  target: 1 to 10 USD per day of autonomous work, judged as a seven-day
    total of 7 to 70 USD
  tripwire: 70 USD in any seven days pauses autopilot through Harbour's
    halt signal; resumption needs a new decision record
  excluded from the target: pilot and flight companion sessions, which the
    ledger records under their involvement class but does not budget here
  unit: whatever Harbour's per-issue cost endpoint reports, so the ledger
    is Harbour's usage entries plus Lighthouse's weekly export and nothing else
reason: research needs flexibility as instruments improve, but flexibility
  that is not recorded is silent extension, which LH F03 forbids
kind: provisional implementation choice
revisit when: the north star's completion evidence holds, or the tripwire
  fires twice in one month
```

## What the band buys

| Item | Harbour's figure | Where it comes from |
| --- | --- | --- |
| One cheap-tier implementation task | About 2 to 3 USD in tokens plus a few cents of compute | Harbour papers, runner-for-strangers |
| One review round on a strong model | About 5 USD; twenty rounds cost 99.81 USD | Harbour papers, README |

At the bottom of the band the workspace can afford one cheap task every two or three days. At the top it can afford two or three cheap tasks a day, or one strong-model review round and one task. Periodicals are scripted wherever possible so they cost cents rather than dollars, and their real cost is the first thing the ledger measures. The variable allowance is weighted toward instrument tickets, because an autopilot will otherwise find documents easier to improve than sensors.

## Autopilot boundaries

The autopilot may draft studies, build and calibrate instruments, run analyses, file question-register entries, update the ledger, and propose tickets for triage.

The autopilot may not release a publication, change the budget or this decision record, change Harbour's configuration or retention, dispatch work outside this workspace, or turn a periodical's output directly into a ticket. These follow Harbour's own human-only line and LH F03's release check.

## Seed tickets

Each ticket carries its study or instrument identifier at the head of the prompt, as LH F03's integration contract proposes. Model choice follows Harbour's finding that cheap tiers pass bounded implementation work; strong models are reserved for review.

**LH000. Observe one dispatch in this workspace end to end.**
Kind research. Target cli. Effort medium. Fill the LH F05 study brief, then observe a single dispatch (this one will do) with whatever instruments exist, export Harbour's records for it, and write the study skeleton with every unfillable field left visibly blank. Stop after one dispatch and one write-up. Done when the skeleton exists and lists which template fields could not be filled and why.

**I-0001. Harbour record exporter.**
Kind implementation. Target cli. Effort low. A script that pulls this workspace's dispatch items, feedback entries, usage entries and proxy audit entries through a labelled read token and writes them to the protected store with a collection timestamp. Fill the LH F05 instrument record, including what the export cannot see. Done when one export has run by hand and its instrument record is complete.

**I-0002. Host process sampler.**
Kind implementation. Target cli. Effort low. A sampler for the machine that claims dispatches, recording process activity, busy core seconds and per-destination request counts at a declared interval, tagged as Lighthouse traffic. Fill the instrument record with its overhead measured. Done when it has captured one idle baseline and one dispatch.

**Q-bootstrap. Populate the question register.**
Kind research. Target cli. Effort low. Enter LH F04's follow-up questions and the north star's open questions into the register using the LH F05 form, each with a reason it matters. Score nothing yet. Done when the register exists and has no empty reasons.

**Ledger. Consumption ledger by study and involvement class.**
Kind implementation. Target cli. Effort low. A table built from the weekly export: cost per study, split into autonomous initiation, delegated autonomy, approved execution and advice, with pilot and flight companion sessions visible but outside the budget total. Done when the first week's figures exist and the tripwire check can be computed from them.

## Periodicals

Periodicals produce records, never tickets. If a periodical finds something that needs work, it writes a register entry or a status record, and triage decides.

| Periodical | Cadence | Does | Produces | Cost class |
| --- | --- | --- | --- | --- |
| Export | Every 7 days | Runs I-0001 for the whole workspace | Observation files in the protected store, each with a collection time | Scripted, cents |
| Ledger | Every 7 days, after export | Rebuilds the consumption table and checks the tripwire | Ledger row per study; status record if the tripwire fires | Cheap tier |
| Triage | Every 7 days | Scores new register entries against LH F04's five criteria | Scored entries; a shortlist for the steward | Cheap tier |
| Source check | Every 30 days | Fetches every source in LH F02 and every instrument's upstream documentation | Check notes; a register entry for anything moved or changed | Scripted, cents |
| Reproduction | On study close | Files the methods-review task for that study | A reproduction record or an explanation of why reproduction was not possible | Strong model |
| Programme review | At week 12 | Runs LH F04's review questions over the ledger, register and releases | A review record and a proposed next programme | Steward, with agent support |

The Export and Source check periodicals are known, scheduled workloads. They are calibration events for I-0002: a miss is an instrument failure with a timestamp. They are also scheduled automation, which LH F02 lists as a competing explanation for propagation, so every reading they generate carries the Lighthouse traffic flag.

## Asks of Harbour

1. **A study marker.** A `[study] LHnnn` marker alongside the existing ticket markers, so the Observation view and the cost endpoint can join runs to studies. Until it exists, the study identifier at the head of the prompt serves.
2. **A labelled read token** for I-0001, so Lighthouse's own collection traffic is distinguishable in the audit log.
3. **An export endpoint** for a whole workspace's records. Not blocking, since the weekly Export periodical stays inside the thirty-day retention window with margin, but it would make I-0001 trivial.

## First fortnight

1. File the north star and the five seed tickets. Adopt D-0001.
2. Configure the Export, Ledger and Triage periodicals at the bottom of the band.
3. The steward claims LH000 in a pilot session and runs I-0001 once by hand, so the first export exists before any autopilot run.
4. Enable autopilot with the remaining seeds available to claim.
5. At the end of week two, read the ledger. If the tripwire logic cannot be computed from it, that is the first finding.
