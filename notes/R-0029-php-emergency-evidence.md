# R-0029: PHP emergency account, evidence review

22 October 2026. Produced by a separate Codex evidence-review agent in the driving session. Scope: the draft long and short accounts, both SVGs and the README lead, against AGENTS.md's release-review rule, LH018–LH028 and the retained primary sources. This is a second reading, not independent confirmation of the publishers' observations. No article was edited by this reviewer; no commit or push was made.

## Findings and resolution

Two changes were required in the initial draft and were made by the driving agent during review:

1. **Do not call 14:00 a verified patch-publication instant.** PHP's retained advance notice schedules 14:00 UTC; its advisory dates the release to 21 October. CERT-EU's retained notice reports fixes at 13:30, while Amazon describes the embargo lifting at 14:00. The timeline and its article alt text now distinguish the reported fixes from the embargo clock and name CERT-EU. This preserves LH018/LH020's explicit warning against substituting a schedule for independently measured first availability.
2. **Do not imply AI itself coordinated the response.** The retained OpenAI account attributes a finding to Calif using GPT-5.6 Sol and coordination to OpenAI and partners, with PHP maintainers leading fixes. The summary and closing paragraph now distinguish AI-assisted discovery from human coordination.

The final working-tree reading found no remaining must-fix evidence finding in these public surfaces. The timeline also now labels overlapping windows and keeps its source line within the image. Reader-and-inference review and the required fresh reading of review-driven revisions remain separate release steps.

## Checks

- Independently opened the [Amazon first-party article](https://aws.amazon.com/blogs/security/amazon-threat-intelligence-identifies-php2shell-exploitation-prior-to-public-disclosure-in-madpot/) through the web reader on 22 October. It supports the 17 October attempt, 21 October publication, 02:00–08:00 attempts, later attempts and uncertainty about knowledge and real-system success. It supplies no episode-wide request series or attribution of the observed requests to AI. This access does not repair the offline archive: LH028's 195-byte `Site Unavailable` response remains the retained direct observation.
- Read retained PHP notices, Cloudflare, OpenAI, NCSC, CERT-EU, Fastly blog/changelog and Akamai content. Confirmed the CVE identifiers; four fixed branches; 20 October 19:33:47 announcement field; Cloudflare's retrospective 03:02 default-WAF statement, customer scope and changing-payload claim; optional Fastly activation; Akamai rule release; and the agencies' conditional isolation advice. The source distinction between AI-assisted discovery and offensive attribution is sound after correction.
- Replayed LH019: all four moving-tag manifests and configs verify and equal the selected fixed counterparts. Replayed LH025: five selected derivative manifests/configs verify and declare 8.2.35, 8.3.36 or 8.5.12. Replayed LH026: 12 base layers are the prefix of 17 derivative layers in both compressed digests and uncompressed diff IDs. Existing scripts and regenerated outputs retain these calculations; no new numerical analysis was introduced.
- Replayed LH024: 13 panel entries and 17 attempted reads, primary hashes and four HTTP-200 access placeholders verified. Checked the ten-institution/six-readable/four-unknown classifications and three media entries against the selected-source/event records. Incomplete search retention and discarded media bodies correctly prevent stronger coverage/replay claims.
- Replayed LH028: AWS 195 bytes, Cloudflare 301,730 and OpenAI 454,180 all match retained hashes. The long account explicitly distinguishes AWS web access from the direct placeholder. The short form preserves this qualification.
- Read LH018–LH028 records for selection and clock boundaries. Failed Nextcloud recipe coverage and failed exact Drupal selection are not converted into negatives or successful preselected cases. The later selected Drupal layer comparison is not represented as a rate. The article, short form and README consistently stop at published artifacts rather than pulls, deployments or compromise.
- Rendered both SVGs using Sharp against white and dark (`#151a1d`) surrounding backgrounds and inspected all four images; rerendered and inspected the corrected timeline in both. Text fits and remains legible at their native 900-pixel width. The fixed opaque light canvas makes internal colours identical in both themes. No browser/mobile integration check was made.

Replay commands, all successful:

```sh
python studies/LH019/scripts/analyse.py
python studies/LH024/scripts/replay.py
python studies/LH025/scripts/analyse.py --snapshot 2026-10-22
python studies/LH026/scripts/replay.py
python studies/LH028/scripts/replay.py --snapshot 2026-10-22
```

## Not verified

No independent sensor validates Amazon's or Cloudflare's attack observations, actual historical rule activation, discovery precedence or precise first-public patch availability. No executable, deployment, pull population or successful compromise was tested. The AWS article is still not replayable offline; the original complete ranked search output and media article bodies are unavailable. This review verifies the attribution and retained evidence boundaries, not the underlying publishers' operational claims. The stated rapid-watch cadence is a protocol intention, not proof that future scheduled readings will occur.
