# Research safety

**In short.** Lighthouse checks what its own work could make easier before it starts, as it works and before it shares results. Most work proceeds in the ordinary queue. If the risk cannot be reduced within the approved scope and available controls, the work waits.

## Before work

Ask whether the planned collection, analysis or sharing could materially reduce the effort, expertise or uncertainty needed to cause harm. Include what Lighthouse would add by selecting, joining, interpreting or pointing to public sources. Check before recording a potentially sensitive lead, fixing or amending a brief, or starting a claim that changes the sources, method or synthesis. Apply the check before exploratory source reads that go beyond discovery, even before a brief or claim exists. Existing briefs get the same check when their work next comes up. Reuse an assessment while its scope and circumstances still apply.

- **Proceed** when the planned work raises no material concern. Use the ordinary brief, queue and review, without another form or reviewer.
- **Narrow** when a useful answer can be obtained safely. Fix the safe question and allowed collection and retention in the existing brief or amendment. Prefer aggregate or minimum derived fields. If a source body is unnecessary, use a collector that only retains those approved fields. Include filenames, metadata, source pointers and logs in the retention decision. Ask the existing proposal gate or fresh review to check the narrowed scope when judgement is material.
- **Defer** when material uncertainty remains or the proposed handling needs a boundary the harness cannot provide. Keep the lead out of the public record if even its description would disclose too much. For commissioned work, use the existing queue hold below. Urgency and keeper agreement to a topic do not clear this check.

Horizon can identify and triage leads from public reporting. Outcome collection waits for a safe, fixed brief. Watch follows the brief's collection and retention limits. Research applies the same test to analysis and review, including cross-study synthesis. Editor applies it to new summaries and connections between records. These limits also apply to the all-purpose run.

## If a concern emerges

Stop the affected collection, analysis and handoffs. Do not investigate the concern further to explain it. Keep sensitive material out of commits, issues, review notes, console output, logs, artifacts and handovers. Do not print or pass it to another agent. Use approved, minimum safe data for work that can continue. If material reached a local file, index or commit, exclude it and any affected commits from every push. Rebuild safe changes from a clean checkout if needed. A later deletion commit leaves the earlier content in history. Do not create a private evidence archive to handle a hold. If material has already left the checkout, stop further disclosure and alert the keeper without repeating it.

For already public queue work, set the owned row to `blocked` with the generic note `Work deferred pending a scope review.` Clear any new outcome reference and preserve the last safe public record. Refresh main and publish only the safe queue change from a clean checkout if needed. For an LH study this note also pauses new claims on sibling rows, including those with no dependency on the affected row. Other work uses individual blocked rows and existing dependencies. Use the generic disposition for a necessary run summary only if safe. Omit the reason, affected sources, detail and reconstruction clues. Queue IDs and timing can also disclose information. Where even the ordinary hold would disclose too much, stop without adding a public marker or pushing the affected work, and give the keeper a generic operational alert if that is safe.

A hold never expires into permission to resume. A later run clears it only after the existing gate or fresh review can clear a safe scope using safe inputs alone. Keep any amended brief and queue change together and respect the original observation window. If the work cannot be made safe, leave it deferred or close it without a finding.

## Before any public handoff

A branch, PR, GitHub issue, action log or artifact can disclose material before the website does. Before any push or other public handoff, check the outgoing material together with what is already public, including what filenames, adjacent records and omissions let a reader infer. If a hold for the study appeared after the claim, stop before sharing results. The claim only establishes ownership. Apply the same checks to findings in records and notes even when no article is planned.

Use the existing evidence and reader reviews before release. Check the actual version and what it adds to the public record, including data, illustrations, captions, links, summaries, metadata, related studies and the shape of the gaps. Generalise or remove risky joins and pointers, or withhold the result. State safe methodological limits and narrow claims to evidence that can support them at the stated level. A claim that cannot safely be substantiated stays out of the release. Review notes and rechecks use the same disclosure rules.

## What the environment enforces

The queue checker and claim helper refuse new claims on held rows and their affected study siblings. This is scheduling enforcement through the helper, with no revocation of an in-flight claim. The runner still uses a direct push for claims and results. Research roles select work and the assessment depends on judgement. A session with repository write access can bypass the helper, push another public branch, or change the rules. A fresh reviewer or local hook has no separate authority over those writes.

The Pages build has a read-only GitHub token. Only the deployment job gets Pages write and OIDC permissions. The `github-pages` environment controls which refs may deploy. These controls protect the deployment path. Public Git objects, issues and workflow output have their own access paths.

Keep material that needs stronger controls out of the current write-enabled runs. To take on such work, first verify an externally restricted harness that cannot publish, change the rules or pass material to a write-enabled session, including through inherited Git, GitHub or Harbour tools and retained transcripts. Keep any eventual release authority outside that session. A main-only rule cannot protect public branches or issues, and requiring PRs on main would change how the current queue claims work.
