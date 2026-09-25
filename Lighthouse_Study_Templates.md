# Lighthouse Study Templates

Editable records for questions, studies, instruments, observations, claims, decisions and releases

Draft | 25 September 2026 | LH F05

These templates are the editable source bundle that LH F02, F03 and F04 refer to. Copy the relevant block into a new file, fill it in, and keep the file under version control with the study. Every field is filled or marked unknown unless it is labelled optional. Example values are illustrative, not observed.

## Question register entry

```
id: Q-0001
title:
why it matters:
proposed by:                      date:
evidence likely needed:
status: open | in study LHnnn | closed (reason)
```

## Study brief (LHnnn)

```
study: LHnnn                      edition: 0.1          date opened:
owner:                            methods reviewer:     editor:
initiated by: person | autopilot
question:
scope (systems, population, period):
evidence available:
evidence needed and access status:
readings and instruments (by instrument id):
comparators and known events:
competing explanations to test:
pre-specified analyses:
exploratory analyses (labelled):
intended output (study, dataset, instrument revision):
discovery allowance:              execution ceiling:
stopping condition:
retention and sharing rules:
Harbour dispatch identifiers (if coordinated through Harbour):
overlaps and interests to disclose:
protocol amendments (date, change, reason):
```

## Instrument record

```
instrument: I-0001                version:              owner:
what it detects:
what it misses:
observation point and boundary:
sampling rule and interval:
calibration (known events, dates, result):
expected overhead and how measured:
changes that would invalidate comparisons:
source retention window (if reading an external source):
retired on and reason (optional):
```

## Observation record

One row per reading. Store as a table or a line-delimited file and keep the field names.

| Field | Meaning |
| --- | --- |
| observation_id | Stable identifier for this reading |
| study | LHnnn |
| instrument, instrument_version | Which sensor produced it |
| source_ref | Underlying record or its controlled location |
| entity_id or connection_id | What was measured, at the declared level of detail |
| event_start, event_end | Event interval, with timezone |
| collected_at | When Lighthouse captured it |
| clock_uncertainty | Known or estimated clock error |
| metric, unit | Name and native unit |
| value | The reading; empty if missing |
| status | observed, derived, unknown, unavailable, not applicable |
| kind | counter, gauge or event |
| attribution_basis | How the entity was identified |
| missingness_flag | Reason the value is absent, if any |
| lighthouse_traffic | true if the reading is Lighthouse's own activity |

Illustrative row, not observed:

```
OBS-000001, LH001, I-0003 v0.2, harbour-export-2026-10-14.json#item42, dispatch:42,
2026-10-14T10:02:11Z, 2026-10-14T10:02:11Z, 2026-10-14T18:00:00Z, 1s,
dispatched_at, timestamp, 2026-10-14T10:02:11Z, observed, event, dispatch id, none, false
```

## Claim record

```
claim: C-0001                     study: LHnnn          date:
statement:
kind: observation | derived measurement | interpretation | scenario
evidence (observation ids, datasets):
method version:
scope (population, period, boundary):
competing explanations considered:
what would change the conclusion:
confidence and rationale:
status: candidate | reviewed | published in <release> | corrected in <release> | withdrawn (reason)
```

## Decision record

```
decision: D-0001                  date:                 owner:
question:
options considered:
choice:
reason:
kind: founding scope | provisional implementation choice
revisit when:
```

## Release record

```
release:                          publication id and edition:
form: note | study | report | article | essay | dataset | instrument
responsible person:               methods reviewer:     editor:
evidence versions:                method versions:
publication date:                 evidence cutoff:
observation period covered:
roles combined (state which checks were not independent):
restrictions on supporting material:
authority for release:
review trigger or expiry:
```

## Correction record

```
publication id:                   corrected edition:
date:
what changed:
why:
did the conclusions change: yes | no (explain)
earlier edition retained at:
```

## Study publication skeleton

Follows Harbour's paper standard [S13 in LH F02] with Lighthouse additions.

```
title: (the question)
kind: paper | essay
version:                          date:
authors:                          model (if an agent contributed):
grounded_at: (commit or data snapshot the numbers were taken from)
observation period:               instruments and versions:
cites: (verifiable references: DOI, URL, or path@sha:line)
overlaps disclosed:

## Answer
One paragraph. Label a sentence's kind wherever a reader could confuse
observation, derived measurement, interpretation and scenario.

## Findings
Bold lead sentences, each followed by its evidence and observation ids.

## Method
Enough for someone else to reproduce the important calculation.
Retained runs and queries listed.

## Limits
Blind spots, missingness, collection overhead, competing explanations
not excluded, retention and access restrictions.

## Next
Follow-up questions, each entered in the question register.

## Corrections
Empty on first release.
```
