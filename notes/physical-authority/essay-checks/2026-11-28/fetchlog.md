# Essay fact-check reads, 28 November 2026

**In short.** Four one-off checks of the commissioning essay's own citations, for the revised essay (row LH050-essay-draft), not LH050 collection: they enter no matrix cell and count against none of the study's bounds. Two URLs were refused by robots.txt and not requested; the Financial Times answered HTTP 403, a wall, not retried; San Francisco's legislative record answered and was kept, but on that page doesn't say what the votes did about robots. Four of the eight allowed reads used.

Run by a Claude Opus 5.5 subagent (claude-opus-5-5) under Claude Code, `LIGHTHOUSE_PROVIDER=anthropic`, every check, fetch and keep decision with `access='oneoff'` through scripts/lh_fetch.py ([collector.py](collector.py), run once). Robots decisions are in [robots/](robots/); the machine log is [fetchlog.jsonl](fetchlog.jsonl). Bodies are kept only where `save_body` allowed, with email addresses withheld (none found).

| UTC | URL | Robots (one-off rule) | HTTP | Bytes | SHA-256 of bytes received | Kept |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-28T15:14:35Z | https://www.ft.com/content/8117b912-ebc7-46b2-90cd-a1ec32e12c5a | allowed (`*` group) | 403 | 270395 | 185401b7547b2e388267fe6da71cc981ad6725c61d39e5cdaa63d43101932e1f | no: a wall or error; not retried, no other route tried |
| 2026-11-28T15:14:37Z | https://www.wired.com/story/humanoid-robot-soldier-eric-trump-foundation-future-industries/ | refused (Claude-User group, `Disallow: /`) | not requested | 0 | | no: not requested |
| 2026-11-28T15:14:38Z | https://www.reuters.com/business/eric-trump-backed-foundation-partners-with-amd-develop-humanoid-robots-2026-07-23/ | refused (`*` group, `Disallow: /`) | not requested | 0 | | no: not requested |
| 2026-11-28T15:14:38Z | https://sfgov.legistar.com/LegislationDetail.aspx?ID=5664065&GUID=71062664-A857-437A-8C49-97D48CF9F2A2 | allowed (robots.txt 404, no rules) | 200 | 176689 | fa551269746476be6bb8d9c2955057b273bd549cafba1517c134f4d832cb5925 | yes: [bodies/E4_sfbos_220641.html](bodies/E4_sfbos_220641.html) |

## What each read gave

- **Financial Times (claims 1, 2, 6 and 12 in the [claim table](../../essay-claims.md)).** HTTP 403. Nothing of the article was seen. The essay attributes the Gaza report to the commissioning essay's account of it and says we couldn't read it.
- **WIRED (claim 3) and Reuters (claim 7).** Refused by robots.txt under the one-off rule for the provider running this session, so not requested. Both claims are cut from the essay.
- **San Francisco Board of Supervisors, File No. 220641** ("Administrative Code - Funding, Acquisition, and Use of Certain Police Department Equipment"; claim 9). The page's history lists, for the Board of Supervisors: on 11/29/2022 three amendments passed, one failed, the file "DIVIDED" and "PASSED ON FIRST READING AS AMENDED"; on 12/6/2022 "AMENDED, AN AMENDMENT OF THE WHOLE BEARING SAME TITLE", "DUPLICATED" and "PASSED ON FIRST READING AS AMENDED"; on 12/13/2022 "FINALLY PASSED"; the Mayor "APPROVED" on 12/22/2022 (enactment 257-22). The page's text has no occurrence of "robot" or "deadly force": what each amendment did sits behind "Action details" links, not read. So the Board's own record, as read, confirms a sequence of votes but not what they decided about robots. Under the plan's one read for this claim, the claim is cut. Leads seen only as search results and not opened: the Board's minutes of 29 November and 6 December 2022 at sfbos.archive.sf.gov (bag112922_minutes.pdf, bag120622_minutes.pdf), the final ordinance PDF on sf.gov, and a Public Defender letter on Legistar.

Two searches were made to find the San Francisco record (WebSearch connector, 28 November 2026, domains limited to sfgov.legistar.com, sfbos.org, sf.gov and sfbos.archive.sf.gov); only the Legistar page above was opened. The connector's written summaries are not evidence and nothing in the essay rests on them.

The ICRC FAQ was not re-read: Lighthouse's retained copy of 13 November 2026 (studies/LH050/data/2026-11-13T1454Z/bodies/S11_icrc_faq.html) holds every passage the essay uses. The conference's final document was not re-read either: the essay quotes the copy retained on 27 November 2026 (studies/LH050/data/2026-11-27T1415Z/bodies/S44_crp1_rev3.pdf, SHA-256 725afe2f...6ffe, rechecked 28 November), extracted with pdftotext.
