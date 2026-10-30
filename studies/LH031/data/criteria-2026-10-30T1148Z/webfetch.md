# LH031 amendment 3: web-reader renderings, 30 October 2026

Each page below refused this container's direct reader at 11:48 UTC with Akamai's "Access Denied" (HTTP 403; bytes, times and hashes in read_log.json). Under amendment 3 each was then requested once through the session's web-fetch tool at about 11:50 UTC. What follows is that tool's output: a small model's rendering of the page, answering a fixed prompt, with quotations it says it truncated to 125 characters and some sentences it paraphrased. It is not the page's bytes, it cannot be re-read, and it is never merged with a direct read. Text in quotation marks is the tool's quotation; the rest is its paraphrase.

## criteria: https://www.cisa.gov/known-exploited-vulnerabilities

Prompt: quote every sentence stating the criteria for adding a vulnerability, including any definition of active exploitation and any mention of attempted exploitation, honeypots, proof of concept or scanning; give the page's date.

Rendering, verbatim:

> **Date:** The page shows no separate last-updated date. It states that CISA updated the page to reference BOD 26-04, which was issued June 10, 2026.
>
> **Three inclusion thresholds**
> - "The vulnerability has an assigned Common Vulnerabilities and Exposures (CVE) ID."
> - "There is reliable evidence that the vulnerability has been actively exploited in the wild."
> - "There is a clear remediation action for the vulnerability, such as a vendor-provided update."
>
> **CVE ID:** The page says a vulnerability's exploitability is not a criterion for inclusion. Exploitation status is the main factor.
>
> **Active exploitation:** The page defines it as "reliable evidence that execution of malicious code was performed by an actor" "on a system without permission of the system owner." The page treats "active exploitation" and "exploited" as synonyms. Attempts and successful attacks both count.
>
> **Attempted exploitation:** The page says it occurs when "an attacker executes code on a target system" but the code does not run because the system isn't vulnerable. Successful code execution on a honeypot is also counted as attempted exploitation, since the attacker gets no real target information.
>
> **Key test:** The actor must intend to succeed, and the attack must occur "in the wild."
>
> **Not active exploitation:** The page lists scanning, security research on an exploit, and proof-of-concept (PoC) code as events that do not count.
>
> **Proof of concept:** The page says a public PoC does not automatically mean a vulnerability has been or will be exploited. A public PoC is also not required for inclusion.
>
> **Remediation requirement:** The page says CISA adds vulnerabilities when "there is a clear action for the affected organization to take." For federal agencies under BOD 26-04, this means applying the vendor's update or removing end-of-life products. Mitigations and workarounds are temporary and do not replace a patch.

## alert: https://www.cisa.gov/news-events/alerts/2026/10/21/critical-vulnerabilities-php-require-immediate-patching

Prompt: title and date; quote every sentence on whether CISA has observed, is aware of, or has no evidence of exploitation; CVEs, versions and requested actions.

Rendering, verbatim:

> **Title:** Critical Vulnerabilities in PHP Require Immediate Patching
>
> **Date:** Last Revised October 26, 2026. The page does not label a separate original publication date, but its URL contains "2026/10/21."
>
> **Exploitation:** The page contains no sentence stating that CISA has observed exploitation or has no evidence of it. The only exploitation-related statement is the KEV addition: "CISA added CVE-2026-109618 and CVE-2026-109619 to its KEV Catalog on Oct. 26, 2026."
>
> - **CVEs:** "CISA strongly urges organizations to immediately patch the recently disclosed critical vulnerabilities in PHP, CVE-2026-109618"
> - **Affected:** "The vulnerabilities affect all PHP installations serving web requests, including Apache with mod_php"
> - **Fixed versions:** "Organizations should immediately update to PHP 8.5.12, 8.4.27, 8.3.36, or 8.2.35 to fix these vulnerabilities."
> - **Actions:** "Identify and inventory systems running any version of PHP across your organization." "Apply the patch immediately, prioritizing internet-facing systems." "Organizations that cannot update immediately, or that continue to use PHP 8.1 or earlier unsupported versions" "A web application firewall may provide some protection until systems are updated or patched." "Monitor for suspicious activity, including PHP worker processes launching shells or downloading tools."

## guidance: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk

Prompt: title and date; quote every sentence stating the criteria for adding a vulnerability (definition of exploitation, attempted exploitation, honeypots, proof of concept) and every sentence defining "Forensics Triage Requirements" or the forensicTriage flag.

Rendering, verbatim:

> **Title:** BOD 26-04: Implementation Guidance for Prioritizing Security Updates Based on Risk
> **Date:** June 10, 2026 (page marked "Updated: August 25, 2026")
>
> **KEV addition criteria** (FAQ "How does CISA decide what goes in the KEV Catalog?"): "CISA adds vulnerabilities to the catalog when our team identifies a vulnerability that meeting the following conditions:" "Has an assigned CVE ID." "Has reliable evidence of active exploitation in the wild." "Has clear remediation or mitigation available, such as a vendor-provided update." "Carries significant risk to U.S. government information systems."
>
> **Active exploitation** (FAQ "How did CISA determine Active Exploitation?"): "CISA relies on several trusted sources to identify active exploitation" "CISA only adds verifiable information to the KEV Catalog." "CISA internally tracks unconfirmed reports until more evidence emerges." "CISA also uses commercial threat intelligence platforms that provide data (i.e., honeypot detections and malware activity)." "These sources go through the same review process to validate active exploitation" "Vulnerabilities found during CISA's own incident response work are also included."
>
> **Proof of concept:** "an available POC is not a requirement for addition to the KEV Catalog."
>
> **Other qualifying statement:** "A vulnerability may qualify for inclusion in the KEV Catalog at any time, regardless of its age," and "if it meets the four conditions noted above."
>
> **Forensic triage:** The page does not define "Forensic Triage Requirements" or a "forensicTriage" flag. The closest statements are: "This implementation guidance establishes forensic triage steps for agencies to execute prompt vulnerability response actions" "The requirement of BOD 26-04 is that an adequate forensic triage analysis is performed"
