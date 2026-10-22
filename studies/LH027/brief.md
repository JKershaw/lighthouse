# LH027: What does one operator's precautionary outage notice establish?

**Protocol 0.1, fixed 22 October 2026 UTC before direct reading of the selected notice.** Writer: Codex, GPT-6 Sol in ChatGPT Work Mode. A web search result already showed that The National Archives published a notice on 21 October saying some services were unavailable because of a potential PHP vulnerability and had been taken offline. This is outcome knowledge and the reason for choosing this case. The web reader's attempted direct open returned HTTP 403 before this protocol, so no page body was read. This purposive positive case cannot give the prevalence of preventive shutdowns.

## Question and rule

Read exactly `https://www.nationalarchives.gov.uk/news/issues-with-the-national-archives-website/`, the institution's own notice. Preserve its response and identify the publication and update dates, the exact named services, the operator's stated reason and action, and any stated restoration condition or timing. Class each as a statement by the operator at the page's observation time. Compare no other operator. A HTTP error, challenge or placeholder is an unavailable page, not evidence the notice was retracted or the services resumed. A page saying services are offline is evidence of an operator statement, not an independent availability probe, compromise or a causal measure of the patch's effectiveness.

## Sources, bounds and stop

One direct GET with a normal user agent, at most 1 MiB retained response body; record UTC request and completion times, URL, final URL, HTTP status, content type, byte count and SHA-256. No crawling, no login, no probing service endpoints. Retain the whole page if within ceiling, otherwise record failure and no partial interpretation. The search result lead and failed web open are prior context; this read tests what the directly retrieved notice actually says. Stop after the one attempt and offline extraction. If unavailable, leave the question inconclusive. Revisit only as a dated, explicitly new observation. No article or population claim follows from this one case.

## Relationship to prior work

LH024 fixed a panel of agencies, edge providers and media, but not individual site operators; this new selected case does not enlarge that fixed panel or repair its coverage rate. LH023 to LH026 describe upstream, images and content identity; none establishes a running site's status. Cost ceiling is one small HTTP request and local replay; model spend is unknown.
