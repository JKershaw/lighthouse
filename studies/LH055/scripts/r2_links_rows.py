#!/usr/bin/env python3
"""LH055 round 2: writes links_r2.csv (round 2 link codings, by campaign as well as by link).

Usage (from the repository root): python3 -I studies/LH055/scripts/r2_links_rows.py
Round 1's links.csv is left unchanged. Links L3 to L6 are coded for acquired credentials, as in round 1.
"""
import csv, os

STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINKS = {"L1": "credential acquisition", "L2": "demonstrated credential validity or access",
         "L3": "integration into an inference gateway", "L4": "actual inference consumption",
         "L5": "further hunting enabled by that consumption", "L6": "acquisition of additional usable resources"}
S = "supported by the stated evidence"
C = "claimed without sufficient disclosed support"
U = "unknown"
NO = "no: a different campaign; cannot confirm or contradict Campaign 1"
MS = "Microsoft's GitHub secret-hunting activity and Entra and Azure follow-on (suspected ARTEX use)"
ROWS = [
 ("S08", MS, NO, "L1", S, "Microsoft's own telemetry shows agents searching GitHub for AI inference-related keys and focusing on AI service credentials, and its AI threat protection identified compromised Azure AI services among the stolen resources. Access to AI resources came through stolen application credentials; no count of AI provider keys obtained is given.", "LH055-C130; LH055-C131; LH055-C133; LH055-C136"),
 ("S08", MS, NO, "L2", S, "Successful service principal sign-ins on dozens of applications are Microsoft's own observation; with that access the actor enumerated AI model deployments (R01 line 54) and attempted to validate stolen Azure resources, including compromised Azure AI services. The validation's outcome is not stated, so this is supported for access, not for a tested AI key.", "LH055-C132; LH055-C133"),
 ("S08", MS, NO, "L3", U, "No gateway, pool or proxy is described.", ""),
 ("S08", MS, NO, "L4", C, "A summary paragraph lists 'abuse of Azure AI services' without hedge; the detailed section says observed activity 'suggests' the actor 'might have attempted' to abuse compromised AI resources. No token, spend or billing figure.", "LH055-C135; LH055-C134"),
 ("S08", MS, NO, "L5", C, "The only assertion is hedged and wider than this link: observed activity 'suggests' the actor 'might have attempted' to abuse compromised AI resources 'to facilitate their broader attack activity', which isn't said to be further credential hunting. The other cited sentence is a general relay of unnamed public reports of AI credentials used 'sometimes to run the same agentic AI workflow' (written before Amazon's post), not about this campaign.", "LH055-C134; LH055-C137"),
 ("S08", MS, NO, "L6", U, "Further credentials were targeted, and Key Vault secrets exfiltrated in some cases, by Microsoft's observation, but nothing ties them to hunting powered by acquired inference.", "LH055-C140"),
 ("S09", "framework description (ARTEX v0.3.15 code, GitGuardian)", "no: a design reading, not a campaign", "L1", U, "The published code ships no secret hunting (its one GitHub API call is the self-updater); that says nothing about acquisition in the wild, which the model can assemble at runtime.", "LH055-C141; LH055-C142"),
 ("S09", "framework description (ARTEX v0.3.15 code, GitGuardian)", "no: a design reading, not a campaign", "L2", U, "Not addressed for ARTEX.", ""),
 ("S09", "framework description (ARTEX v0.3.15 code, GitGuardian)", "no: a design reading, not a campaign", "L3", U, "The catalogue entry is silent on any model gateway or key pool, so it does not resolve what 'the framework's own model gateway' is.", "LH055-C141"),
 ("S09", "framework description (ARTEX v0.3.15 code, GitGuardian)", "no: a design reading, not a campaign", "L4", U, "Not addressed.", ""),
 ("S09", "framework description (ARTEX v0.3.15 code, GitGuardian)", "no: a design reading, not a campaign", "L5", U, "Not addressed.", ""),
 ("S09", "framework description (ARTEX v0.3.15 code, GitGuardian)", "no: a design reading, not a campaign", "L6", U, "Not addressed.", ""),
 ("S10", "CrowdStrike's South Korean finance case", NO, "L1", U, "No theft of AI credentials is described.", ""),
 ("S10", "CrowdStrike's South Korean finance case", NO, "L2", U, "Not addressed for AI credentials.", ""),
 ("S10", "CrowdStrike's South Korean finance case", NO, "L3", U, "No gateway is described; the model was likely reached through a likely reseller, by CrowdStrike's assessment.", "LH055-C146"),
 ("S10", "CrowdStrike's South Korean finance case", NO, "L4", U, "Inference use is shown by recovered configuration (a DeepSeek model as primary backend), but its likely route is a reseller, not acquired keys; whether the reseller access was paid for, or itself rested on stolen capacity, is not stated. Not contradicted either.", "LH055-C145; LH055-C146"),
 ("S10", "CrowdStrike's South Korean finance case", NO, "L5", U, "Not addressed.", ""),
 ("S10", "CrowdStrike's South Korean finance case", NO, "L6", U, "Not addressed.", ""),
 ("S11", "Check Point's and CrowdStrike's cases, relayed by Equixly (secondary)", "no: different campaigns; and a secondary relay", "L1", U, "No AI credential theft is described; Amazon's Campaign 1 is not among its ten cases.", "LH055-C152"),
 ("S11", "Check Point's and CrowdStrike's cases, relayed by Equixly (secondary)", "no: different campaigns; and a secondary relay", "L2", U, "Not addressed for AI credentials.", ""),
 ("S11", "Check Point's and CrowdStrike's cases, relayed by Equixly (secondary)", "no: different campaigns; and a secondary relay", "L3", U, "Not addressed.", ""),
 ("S11", "Check Point's and CrowdStrike's cases, relayed by Equixly (secondary)", "no: different campaigns; and a secondary relay", "L4", U, "Not addressed.", ""),
 ("S11", "Check Point's and CrowdStrike's cases, relayed by Equixly (secondary)", "no: different campaigns; and a secondary relay", "L5", U, "Not addressed.", ""),
 ("S11", "Check Point's and CrowdStrike's cases, relayed by Equixly (secondary)", "no: different campaigns; and a secondary relay", "L6", U, "Not addressed.", ""),
 ("S12", "Amazon's Campaign 1, repeated by The Stack (secondary)", "repetition only: adds no evidence for or against Campaign 1", "L1", C, "Quotes Amazon's sentence on large-scale theft of AI credentials; cites no evidence of its own.", "LH055-C153"),
 ("S12", "Amazon's Campaign 1, repeated by The Stack (secondary)", "repetition only: adds no evidence for or against Campaign 1", "L2", U, "Not addressed.", ""),
 ("S12", "Amazon's Campaign 1, repeated by The Stack (secondary)", "repetition only: adds no evidence for or against Campaign 1", "L3", U, "Its sentence that the agents assumed the sensors gave free inference is its own reading of the decoys, not a statement about stolen keys and not Amazon's.", "LH055-C154"),
 ("S12", "Amazon's Campaign 1, repeated by The Stack (secondary)", "repetition only: adds no evidence for or against Campaign 1", "L4", C, "Repeats Amazon's 'stolen keys paid for the LLM inference'; no evidence of its own.", "LH055-C153"),
 ("S12", "Amazon's Campaign 1, repeated by The Stack (secondary)", "repetition only: adds no evidence for or against Campaign 1", "L5", C, "Repeats Amazon's 'powering further credential hunting'; no evidence of its own.", "LH055-C153"),
 ("S12", "Amazon's Campaign 1, repeated by The Stack (secondary)", "repetition only: adds no evidence for or against Campaign 1", "L6", U, "Not addressed.", ""),
 ("S13", "ARTEX activity surveyed by Talos", "no: Talos does not mention Campaign 1", "L1", U, "Relays Microsoft's GitHub hunting for AI keys (counted under S08, not here); describes no AI credential theft of its own.", "LH055-C160"),
 ("S13", "ARTEX activity surveyed by Talos", "no: Talos does not mention Campaign 1", "L2", U, "Not addressed for AI credentials.", ""),
 ("S13", "ARTEX activity surveyed by Talos", "no: Talos does not mention Campaign 1", "L3", U, "Says only that ARTEX can use different LLMs.", "LH055-C156"),
 ("S13", "ARTEX activity surveyed by Talos", "no: Talos does not mention Campaign 1", "L4", U, "Not addressed.", ""),
 ("S13", "ARTEX activity surveyed by Talos", "no: Talos does not mention Campaign 1", "L5", U, "Not addressed.", ""),
 ("S13", "ARTEX activity surveyed by Talos", "no: Talos does not mention Campaign 1", "L6", U, "Not addressed.", ""),
 ("S14", "Datadog's AWS sightings and its analysis of ARTEX distributions", "no: a different activity, and a design description", "L1", U, "Its own telemetry shows compromised long-term AWS keys used and further secrets hunted, but no AI or model service use is reported; not AI credentials.", "LH055-C164"),
 ("S14", "Datadog's AWS sightings and its analysis of ARTEX distributions", "no: a different activity, and a design description", "L2", U, "Not addressed for AI credentials; one sign-up case's discovery calls all failed.", "LH055-C166"),
 ("S14", "Datadog's AWS sightings and its analysis of ARTEX distributions", "no: a different activity, and a design description", "L3", U, "Describes ARTEX holding user-supplied provider keys and moving to the next when one is banned or cut off, and lists an /llm/pool route: a built-in feature that Amazon's 'framework's own model gateway' may refer to (post hoc reading). It shows no acquired key loaded into it.", "LH055-C161; LH055-C162; LH055-C163"),
 ("S14", "Datadog's AWS sightings and its analysis of ARTEX distributions", "no: a different activity, and a design description", "L4", U, "Not addressed for acquired credentials.", ""),
 ("S14", "Datadog's AWS sightings and its analysis of ARTEX distributions", "no: a different activity, and a design description", "L5", U, "Not addressed.", ""),
 ("S14", "Datadog's AWS sightings and its analysis of ARTEX distributions", "no: a different activity, and a design description", "L6", U, "Not addressed.", ""),
]


def main():
    p = os.path.join(STUDY, "links_r2.csv")
    w = csv.writer(open(p, "w", newline=""), lineterminator="\n")
    w.writerow(["source_id", "campaign", "bears_on_amazon_campaign1", "link_id", "link", "status", "reason", "claim_ids"])
    for s, camp, bear, lid, st, reason, ids in ROWS:
        w.writerow([s, camp, bear, lid, LINKS[lid], st, reason, ids])
    print(len(ROWS), "rows written to links_r2.csv")


if __name__ == "__main__":
    main()
