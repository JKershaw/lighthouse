title: Email addresses withheld from retained sources, 8 November 2026
kind: working note

# Email addresses withheld from retained sources, 8 November 2026

**In short.** At the keeper's request ("Let's redact the email addresses. Feels polite, and we've not much need to share them."), every email address in the text files retained on 8 November 2026 is replaced with `[email withheld by Lighthouse]`, and the collectors that will read again withhold them as they save. Nothing a study measures depends on an address.

- Tool: [scripts/redact_emails.py](../scripts/redact_emails.py), applied to studies/LH043, studies/LH045 and essays/what-the-watch-would-see/claims-check; the per-file log, with each file's SHA-256 before and after, is [redaction-2026-11-08.tsv](redaction-2026-11-08.tsv). Binary files (PDF, ZIP) are skipped; their text conversions are redacted.
- Fetch logs keep the SHA-256 of the bytes received, so a refetch can still be compared; a retained file no longer matches that hash where an address was withheld, and the log above says which.
- studies/LH045's two collectors now call the same function before writing a body. Studies still being written this evening (LH041, LH042, LH044) are redacted when they are committed.
- The earlier commits of this branch still hold the addresses in git history; history is not rewritten on a shared branch.
