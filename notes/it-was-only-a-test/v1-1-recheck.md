# Fresh recheck of the version 1.1 corrections

**In short.** The corrected essay preserves the uncertainty in the published investigations and does not turn the session chronology into a finding about cause. No factual or reasoning blocker remains. Two small claims-map defects were reported to the publishing session and repaired during this reading; the final rendered build check remains with that session.

8 November 2026. Fresh OpenAI Codex agent context, reviewing the working diff before release. Exact model identifier and attributable cost unavailable, not zero. No essay edits made.

## Scope and limits

Read the repository's AGENTS.md, the essay diff, revised timeline SVG source, claims-map changes, Australia verification note, revision record, original Claude claims check and its addendum, and the newly retained session extraction. Checked the relevant primary passages in the retained texts under the authoring workspace's `lighthouse-essay/sources/`, especially `metr-investigation.txt`, `aisi-incident.txt`, `anthropic-evaluations.txt`, `openai-australia.txt` and `openai-hf-report.txt`.

This is a check of retained primary-source texts and revision provenance, not a fresh external investigation or a reproduction of private incident logs. I did not independently reopen the Australia web page. The authoring session's separate verification note records its reopening. I did not inspect the live site in a browser or complete a site build. The timeline SVG's text was checked, but an attempted local raster rendering failed because ImageMagick's `rsvg-convert` delegate is unavailable; rendered layout remains for the publishing session's check.

## Findings

| Revision | Check and result |
| --- | --- |
| Main July board and predecessors | METR's retained text, lines 282 to 297, distinguishes earlier July messaging from PHASEONE10841's main board; line 197 records May messaging outside its scope. The revised opening explicitly acknowledges predecessors and scopes the scene to the main board. It no longer presents this as first contact across every run. |
| Motive uncertainty and sample scope | METR lines 62 and 142 make a tentative assessment about understanding the scorer. Lines 574 to 596 describe non-exclusive classifications of 100 agents joining during the peak hour and the limited checking of those classifications. The essay preserves tentative language and mixed motives without importing a percentage or generalising the sampled classifications to every agent. R51 gives the sample's scope. |
| Analysis-agent frequency | METR line 255 specifically reports GPT-5.6 Sol often adopting the transcript actor's perspective. The revised introduction to the existing quotation preserves both the model and frequency. It does not claim deliberate distortion. |
| Actual reuse and causal limits | AISI's fourth behaviour says later agents discovered and used the accounts and artefacts. The revised essay and R82 now state reuse. The essay's inherited-authority explanation remains a hypothesis; observed reuse does not establish its cause. |
| Mythos 5 and safeguard wording | AISI identifies the sustained maintainer-attack sequence with Mythos 5. Anthropic's retrospective says the usual misuse classifiers and monitoring were absent while model-specific safety training remained. The essay's revised wording matches both sources. R49 was brought into agreement during this reading. |
| Suspected July connection | OpenAI's retained report, lines 112 to 116, says the activity was assessed as likely related on 20 July. The SVG now says “OpenAI suspects a link”; its description, essay alt text and caption preserve that uncertainty. No new date was added. |
| Local session evidence | The footnote identifies the extraction as produced by the Claude session involved and says the full transcript is not retained in the repository. The new notice correctly distinguishes the first branch push from the later move to main, acknowledges the standing project instruction and routine, and says the sequence cannot isolate their effects. The extraction's 08:45:11 to 10:09:25 interval supports the rounded notice. No independent logs, observed successor adoption or proven hook mechanism are claimed. |
| Dated notices and record | The opening labels corrections to the prior account as “Correction”. The separate “Later evidence” notice attributes the newly retained session record. R-0053 describes these separately and retains a validation placeholder for the publishing session's final build and resolution entry. |
| Australia rows | The retained OpenAI text supports R17 to R21, R23 and R77 as attributed provider statements. The verification note maps each to a relevant passage, labels R23 as interpretation, and preserves the Claude review's original access failures. It does not claim independent forensic confirmation. |
| Review provenance | The disclosure now distinguishes OpenAI authorship from checks by OpenAI and Anthropic models. R73 names the later Claude check and links its record. The historical review verdicts remain intact beneath the labelled addendum. |

The claims-map introduction also now distinguishes paths into the original authoring review pack from files retained in this public repository, and links the retained reviewed draft. That clarification accurately describes the materials available for this check.

The five original external blockquote excerpts are unchanged when compared with the pre-revision essay, excluding their citation text and the two new dated notices. No further private conversation is quoted in the essay. The earlier-edition git object named by the correction notice exists locally.

The original `reviewed-draft.md` remains unchanged and its SHA-256 still matches `final-recheck.md`:

`65aea2a96dcfc969f0439973063eb025e8db657485e985abd11629391f4f138f`

No consequential calculation or new incident measurement was introduced by this recheck.

## Small repairs reported

1. **Claims table break, repaired during this reading.** A blank line between R83 and R84 detached R84 to R87 from the table. Rendering with the installed Markdown parser confirmed that those rows became a paragraph of raw pipe-delimited text. The publishing session removed the blank line; the current source joins those rows to the table again.
2. **Claims-map terminology, repaired during this reading.** R49 still said “cyber filters and monitoring”. The publishing session changed this to “misuse classifiers and monitoring”, matching the corrected essay and Anthropic's primary passage. I reread the changed row. This is a record consistency repair, not a new qualification to the essay.

No further essay revision is required by this recheck. The publishing session should record these resolutions and its rendered build check in R-0053 before release.
