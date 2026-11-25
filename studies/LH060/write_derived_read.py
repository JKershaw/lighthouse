#!/usr/bin/env python3
"""LH060 search-read: write the derived file for each document read (no body was kept: none of the
fifteen states a redistribution licence; see fetchlog.csv, body_kept). Facts are as read on
25 November 2026 from text extracted in memory by fetch_read.py; quotations are short and attributed.
Run: python3 -I studies/LH060/write_derived_read.py studies/LH060/data/read-2026-11-25T1414Z
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'scripts'))
from lh_fetch import write_derived  # noqa: E402

REASON = 'no redistribution licence stated in the document'

FACTS = {
 'C01': {'title': 'NDSS 2018 notification study (known document, brief: "the ... NDSS 2018 notification studies")',
         'read': 'not read: HTTP 404 at a URL constructed from the venue\'s file pattern (not from a search result)',
         'decision': 'excluded: full text unavailable (wall: HTTP 404)'},
 'C02': {'title': "You've Got Vulnerability: Exploring Effective Vulnerability Notifications",
         'authors': 'Li, Durumeric, Czyz, Karami, Bailey, McCoy, Savage, Paxson', 'venue': '25th USENIX Security Symposium, 2016 (peer reviewed)',
         'population': 'abuse contacts and CERTs responsible for hosts with three exposures found by IPv4/IPv6 scans: misconfigured IPv6 firewall policies, DDoS amplifiers, publicly accessible ICS services; ICS scan 22 to 24 January 2016',
         'outcome': 'remediation (host no longer vulnerable on daily rescans) after notification, by message, channel, language, country, protocol and device type',
         'breakdowns_seen': ['notification route and message', 'country / national CERT', 'protocol', 'device type: servers versus routers ("network administrators respond to vulnerabilities in servers and routers about equally")'],
         'size_fragment': '"30% of groups with 100% remediation were only responsible for fixing one or two hosts" (a description of full remediators, not the outcome broken down by size)',
         'type_fragment': 'no DNP3 system patched within 10 days; "these five contact groups belonged to Internet service providers—not individual organizations" (five contacts, one protocol, no comparison group)',
         'decision': 'excluded: fails criterion 2 (no breakdown of the outcome by operator size, capacity or type; device type and country are not operator size or type under the brief). Borderline, flagged for review.'},
 'C03': {'title': 'Hey, You Have a Problem: On the Feasibility of Large-Scale Web Vulnerability Notification',
         'authors': 'Stock, Pellegrino, Rossow, Johns, Backes', 'venue': '25th USENIX Security Symposium, 2016 (peer reviewed)',
         'population': 'WordPress sites with a known flaw (Alexa top 1 million) and sites with client-side XSS (Alexa top 10,000), notified through direct and indirect channels',
         'outcome': 'fixed domains after notification, by channel; reachability and report views',
         'size_fragment': 'popularity is discussed only for bounce and reach: "As popular Web sites may have a more structured staff, they may tend to adhere to standards like RFC-2142" (authors\' interpretation of bounce rates, not of fixes)',
         'decision': 'excluded: fails criterion 2 (outcome broken down by channel, not by operator size, capacity or type)'},
 'C04': {'title': '2025 Data Breach Investigations Report', 'publisher': 'Verizon', 'venue': 'report (listed publisher)',
         'outcome_seen': 'edge-device vulnerabilities (17 CISA KEV entries across seven vendors): "only about 54% of those were fully remediated throughout the year, and it took a median of 32 days"; whole KEV catalogue median 38 days; data from vulnerability management contributors covering "10,000 companies"',
         'size_sections': 'the SMB focus section and size tables concern incidents, breaches, actors and ransomware; no vulnerability remediation outcome is broken down by organisation size in the text read',
         'decision': 'excluded: fails criterion 2 (remediation reported overall, not by size, capacity or type)'},
 'C05': {'title': 'Prioritization to Prediction, Vol. 3: Winning the Remediation Race (publisher\'s summary page)', 'publisher': 'Cyentia Institute, partner Kenna Security',
         'read': 'the GET returned the publisher\'s summary page, not the report; the report PDF it links was not fetched (one GET per document)',
         'summary_page_says': ['"nearly 300 organizations" ... "Kenna Security customers"', '"smaller firms tend to fix faster than larger ones"', '"Whatever their size, firms close about one in 10 open vulnerabilities per month"'],
         'decision': 'excluded: full text not retrieved. The summary page\'s statements are context only, vendor sample, asserted on the page without method or period; nothing counted.'},
 'C06': {'title': 'Prioritization to Prediction, Vol. 2: Getting Real About Remediation (publisher\'s summary page)', 'publisher': 'Cyentia Institute, partner Kenna Security',
         'read': 'the GET returned the publisher\'s summary page, not the report; the report PDF was not fetched',
         'summary_page_says': ['"more than 3 billion vulnerabilities managed across 500+ organizations on the Kenna Security platform"', 'no size breakdown on the summary page'],
         'decision': 'excluded: full text not retrieved'},
 'C07': {'title': 'Empirical Study of Post-Quantum Cryptography Adoption Status in SSH Infrastructure', 'arxiv': '2611.09703v1, 6 November 2026',
         'authors': 'Haque, Vinberg, Edwards, Cruz (Bitsight Technologies)', 'venue': 'arXiv preprint (no publication stated)',
         'population': '1,523,998 SSH services on port 22 in the authors\' company\'s scan data for one scan day, 16 February 2026, mapped to 27,012 entities (organisations) by the company\'s attribution engine',
         'outcome': 'entity offers a post-quantum key exchange on at least one SSH server; share of an entity\'s IPs offering one',
         'measures': 'revenue and employee count (firmographic data "from our service providers"); SSL active count and IPv4 count (company pipelines); sector (23); region',
         'headline': '45.2% of hosts and 39.9% of entities (10,788 of 27,012) offer a post-quantum key exchange',
         'claims': [
           {'id': 'C07-a', 'measure': 'revenue, employees', 'direction': 'no difference', 'quote': '"Both small-scale organizations and multi-billion dollar enterprises show similar median distributions"', 'class': 'measured; vendor', 'note': 'read from box plots; no test stated'},
           {'id': 'C07-b', 'measure': 'SSL active count', 'direction': 'larger more (adoption)', 'quote': '"entities with more mature web presences (i.e., higher SSL active counts) show a slightly higher propensity to initiate PQC deployment"', 'class': 'measured; vendor', 'note': 'no test stated'},
           {'id': 'C07-c', 'measure': 'IPv4 count', 'direction': 'larger less (share of an entity\'s IPs)', 'quote': '"adoption density thins as network size increases"', 'class': 'measured; vendor', 'note': 'authors read it as a "complexity penalty"; that reading is asserted'},
           {'id': 'C07-d', 'measure': 'sector (type)', 'direction': 'differs by sector', 'quote': '"Adoption maturity is currently driven by research-oriented and infrastructure-heavy sectors like \'Education\' and \'Telecommunications\'"', 'class': 'measured; vendor'}],
         'data_public': 'not stated (company scan and firmographic data)', 'interest': 'authors employed by a security ratings company whose scan data are used',
         'note_feature': 'the authors suggest many entities are "unintentionally PQC-ready" through an SSH server upgrade with the algorithm on by default',
         'decision': 'included (all three criteria)'},
 'C08': {'title': 'Towards Zero Trust Architecture: A Pilot Study on Information Systems Security Readiness amongst Small and Medium Enterprises', 'arxiv': '2605.18901',
         'authors': 'Deng, Inthiran (University of Canterbury)', 'venue': 'arXiv preprint; the PDF carries "Pacific-Asia Conference on Information Systems, Jakarta 2026" (not a listed venue; entered as an arXiv preprint)',
         'population': '64 IT and security professionals in the Asia-Pacific region, purposive convenience sample (34 SME, 30 large enterprise); online questionnaire 20 March to 5 May 2025',
         'outcome': 'security model in use, as reported: perimeter, zero trust, hybrid',
         'claims': [
           {'id': 'C08-a', 'measure': 'employees (<50, 50 to 250, 250 to 500, >500)', 'direction': 'no difference (test); descriptively smaller report zero trust more often', 'quote': '"a cross-tabulation of security model in use by organisation size shows no statistically significant association (χ² = 4.27, df = 6, p = .64)"', 'table': 'zero trust row shares: small 0.500 (n=10), medium 0.417 (n=24), large 0.250 (n=12), very large 0.231 (n=13)', 'class': 'self-reported'}],
         'data_public': 'not stated', 'interest': 'not stated',
         'decision': 'included (all three criteria; whether a security model in use counts as a deployed security feature is a judgement, flagged for review)'},
 'C09': {'title': 'Behind the Curtain: How Shared Hosting Providers Respond to Vulnerability Notifications', 'arxiv': '2512.01891v1, 1 December 2025',
         'authors': 'Stivala, Mrowczynski, Hellenthal, Pellegrino (CISPA)', 'venue': 'arXiv preprint (IEEE S&P 2026 per prior knowledge, not stated in metadata used)',
         'method': 'semi-structured interviews with 24 hosting provider organisations, August 2024 to June 2025; company sizes from fewer than 10 employees (nine) to over 1,000 (three)',
         'context': 'protection "implementation varies widely based on provider size and whether hosting is in-house or outsourced" (interview account); providers serving large businesses or public administration "demonstrated significantly greater attention to security" (interview account)',
         'decision': 'excluded: fails criterion 1 (interviews alone, no deployment outcome measured); kept as context, nothing counted. Interviewees are not identified here.'},
 'C10': {'title': "Don't Get Hijacked: Prevalence, Mitigation, and Impact of Non-Secure DNS Dynamic Updates", 'arxiv': '2405.19871v1, 30 May 2024',
         'authors': 'Nosyk, Korczyński, Gañán, Król, Lone, Duda', 'venue': 'arXiv preprint (no publication stated in the text read)',
         'population': 'nameservers accepting non-secure dynamic updates found in a February to March 2017 scan; Phase 1 notified 44 CSIRTs of the Trusted Introducer community (7 September to 19 October 2017), compared with 36 non-notified CSIRTs; Phase 2 national CSIRTs in 2018; rescan in 2022',
         'outcome': 'nameserver and domain remediation on rescans, Kaplan-Meier survival from notification',
         'claims': [
           {'id': 'C10-a', 'measure': 'CSIRT constituency type (CIIP, government, military, national, non-commercial, research and education)', 'direction': 'differs by type', 'quote': '"Military CSIRTs are particularly fast and efficient in remediation, contrary to research and educational entities that exhibit the slowest and worst patching rates"', 'stat': 'Gehan-Breslow-Wilcoxon test, p = 0.00076 (figure 5)', 'class': 'measured', 'note': 'type is the CSIRT\'s constituency, read here as the operators it serves; a judgement, flagged'}],
         'other': 'Phase 1: notified CSIRTs remediated 20.4% of nameservers and 14.24% of domains, similar to non-notified; average per-CSIRT rate 26.2%. Figure 3 relates vulnerable counts per national CSIRT to IPv4 addresses (prevalence, not remediation; not counted).',
         'data_public': 'not stated in the text read', 'interest': 'academic; one author at RIPE NCC',
         'decision': 'included (all three criteria; operator type via CSIRT constituency, flagged)'},
 'C11': {'title': 'Why, How and Where of Delays in Software Security Patch Management: An Empirical Investigation in the Healthcare Sector', 'arxiv': '2202.09016v2; Proc. ACM HCI 6 CSCW2, November 2022',
         'method': '132 delayed patching tasks over four years (October 2016 to May 2021) and patch meetings of eight teams in two organisations, a state health agency and the multinational to which it outsourced OS patching (anonymised in the source)',
         'context': 'coordination delays named the most prominent cause; most delays in the deployment phase; longest average delay 3.6 months',
         'decision': 'excluded: fails criterion 2 (one operator and its contractor; breakdown by team, phase and reason, not by operator size, capacity or type)'},
 'C12': {'title': 'Snail Mail Beats Email Any Day: On Effective Operator Security Notifications in the Internet', 'arxiv': '2106.08024v1; ARES 2021 (not a listed venue; entered as arXiv)',
         'outcome': 'remediation of exposed files and status pages on .de sites within one month after notification: 39.3% (email) to 64.3% (letter) against 4.3% control',
         'decision': 'excluded: fails criterion 2 (breakdown by channel and issue type, not operator size, capacity or type)'},
 'C13': {'title': 'A Mixed-method Study on Security and Privacy Practices in Danish Companies', 'arxiv': '2104.04030v1',
         'method': 'survey of 107 (60 SME, 47 large; June to November 2020) and interviews (September to November 2020)',
         'context': 'by SME and large: security measurement approaches, stage of security in development, training, GDPR changes, remote work (self-reported)',
         'decision': 'excluded: fails criterion 1 (no deployment outcome of an available security fix or feature); context only'},
 'C14': {'title': 'Software Security Patch Management - A Systematic Literature Review of Challenges, Approaches, Tools and Practices', 'arxiv': '2012.00544v3',
         'method': 'review of 72 studies published 2002 to March 2020',
         'decision': 'excluded: fails criteria 1 and 2 (a review of challenges and solutions; no outcome by operator size, capacity or type reported in the text read)'},
 'C15': {'title': 'Herding Vulnerable Cats: A Statistical Approach to Disentangle Joint Responsibility for Web Security in Shared Hosting', 'arxiv': '1708.06693v1, 22 August 2017',
         'population': '1,259 shared hosting providers, indicators from 442,684 domains',
         'outcome_seen': 'patched or unpatched versions of CMS, admin panels, web servers, PHP, SSH and SSL per domain and per provider; size (shared IP and domain counts) used as a control in abuse regressions; "the combined model explains 19% of the variance for phishing prevalence and 10% for malware prevalence among providers, beyond the baseline of 71%"',
         'decision': 'excluded: fails criterion 2 (patching is described across providers, not broken down by provider size or type; size enters as a control for abuse, the outcome of the regressions). Borderline, flagged for review. Providers named in the source are not named here.'},
}


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    rows = {}
    with open(os.path.join(HERE, 'fetchlog.csv')) as f:
        for r in csv.DictReader(f):
            rows[r['candidate']] = r
    for cid, facts in FACTS.items():
        r = rows[cid]
        write_derived(os.path.join(out_dir, cid + '.derived.json'), r['final_url'] or r['url'],
                      REASON if r['http_status'] == '200' else 'no body received (%s)' % r['outcome'],
                      facts, requested_url=r['url'], read_utc=r['start_utc'], finish_utc=r['finish_utc'],
                      http_status=r['http_status'], content_type=r['content_type'], bytes=r['bytes'],
                      sha256=r['sha256'], used_for='LH060 search-read: inclusion and claim classes')


if __name__ == '__main__':
    main(sys.argv[1])
