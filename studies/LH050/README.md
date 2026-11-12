# Recording claims about armed robots

**In short.** These empty ledgers are the instruments for the first study, not results. Each future claim and event must point to a readable source and a passage. The brief fixes the cases, comparisons, access rules and stopping conditions.

## Workflow

1. Claim the due row on main only after the commissioning branch lands. Read [the brief](brief.md) and [source register](sources.md).
2. Before any source request, set the actual `LIGHTHOUSE_PROVIDER`, check the URL through `scripts/robots_gate.py`, and retain the decision. Follow the current access and redaction rules in AGENTS.md. This study has no collector yet; direct or connector reads must meet the same rules and log their route and limits. If a route cannot meet them, record the source unavailable through that route.
3. Retain permitted source text, read metadata, passage locators and hashes; update the ledgers by source family. Never label a search excerpt as an opened document.
4. Build the case matrix from individual claims, leaving unknowns visible. Write `LH050.md` as the baseline record once collection earns it, with a header including period, writer/model, protocol commit and record/review status. Do not create a finding from these empty templates.
5. Lock `panel.csv` at the scheduled checkpoint. For each later read retain the current version and compare it with the previous readable version. Write a dated checkpoint in `checkpoints/` and a line in the [working log](../../notes/physical-authority-watch-log.md).

## Ledger fields

- `reads.csv`: `read_id` unique; `observed_at` actual UTC time; `source_id` from the register; `url`; `provider`; `route` direct/connector/manual; `access_status` readable/unavailable/withheld; `robots_ref` retained decision path; `received_sha256` when received bytes are available; `retained_sha256` for the redacted artifact; `retained_path`; `note`. Blank hashes mean unavailable, not an empty document's hash.
- `claims.csv`: unique `claim_id`; `case_id` (`foundation`, `armed-comparison`, `changi`); `configuration`; `context`; `dimension` capability/authority/maturity/civilian/economics/policy; `function` where applicable; `statement` a source-attributed description; `value` and `unit` only as warranted; `evidence_kind` supplier-claim/official-account/third-party-report/reproducible-artifact; `evidence_status` supported-by-source/not-established/conflicting/unavailable/not-applicable; `source_id`; `read_id` identifying the exact readable snapshot in reads.csv; `source_family`; `passage_ref`; `event_date`; `publication_date`; `observed_at`; `supersedes`; `note`. Supported-by-source means the source says it, not that Lighthouse verified the event. For civilian cases, use distinct claims for harm, operator/platform attribution and AI-function attribution.
- `events.csv`: unique `event_id`; `case_id`; `configuration`; `institution`; `context`; `event_type` from the brief's maturity list or policy/authority-change/civilian-report; `event_date`; `publication_date`; `observed_at`; `claim_ids`; `note`. Semicolon-separate multiple IDs. A claim can support an event description without verifying the event occurred.
- `panel.csv`: unique `panel_id`; `source_id`; `url` the exact endpoint; `purpose`; `selection_rationale`; `locked_at`. No entries before the baseline-selection checkpoint. A policy document that cannot change need not be fetched weekly.

No ledger is populated from commissioning prose. Stable local IDs do not assert that an allegation is true. Keep source revision and date precision in notes where date-only fields cannot express them; never invent a day from a month or year.
