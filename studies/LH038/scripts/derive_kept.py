#!/usr/bin/env python3
"""Replace LH038's kept pages from git.kernel.org and oss-security.openwall.org with derived files (the keeper's
decision of 21 November 2026, notes/keeper/2026-11-21-robots-intent.md: both sites' robots.txt refuse
AI-training crawlers by name; git.kernel.org refuses all bots under `*` too).

Each derived file (<name>.derived.json beside the body) holds the URL, read times, HTTP status, size and SHA-256
from that directory's read_log.json, and only what the record and its checks use:
  kernel_security_bugs, kernel_cve (policies of 4 November): bot challenge pages, so only that fact and the title;
    the record reads the docs.kernel.org renderings instead (policies-2026-11-04T1416Z, kept);
  linux_distros (P4 in brief.md): the page's "Last modified" line and the short phrases and figures P4 quotes,
    each checked against the page's visible text;
  openwall_distros_stats (read of 17 November): its "Last modified" line, whether it names CVE-2026-98432, and
    the wiki paths it links under distros/stats (review/r0091_check.py; checkpoints/2026-11-17.md).
It never deletes anything. Offline, standard library only. Usage: python3 -I studies/LH038/scripts/derive_kept.py
"""
from pathlib import Path
import gzip, html, json, re

DATA = Path(__file__).resolve().parents[1] / 'data'
CVE = 'CVE-2026-98432'
NOTE = ("Body removed on 21 November 2026 under the keeper's decision (notes/keeper/2026-11-21-robots-intent.md): "
        "the site's robots.txt refuses AI-training or archiving crawlers, or all bots, so Lighthouse keeps the "
        "URL, read time, status, SHA-256 of the bytes received and the facts its records use, not the page.")
KERNEL = 'A+: AI-training token named and refused; * refuses too'
OPENWALL = 'A: AI-training token named and refused; * allows'
P4 = ["notify the kernel security team first, wait for the fix, and only then notify linux-distros or oss-security",
      "The maximum acceptable embargo period for issues disclosed to these lists is 14 days",
      "embargo periods shorter than 7 days are preferable", "1 to 30 days"]
TARGETS = [
    ('policies-2026-11-04T1415Z', 'kernel_security_bugs', KERNEL,
     "P2 candidate: git.kernel.org's plain text of Documentation/process/security-bugs.rst; a bot challenge page (unavailable); the record uses the docs.kernel.org rendering."),
    ('policies-2026-11-04T1415Z', 'kernel_cve', KERNEL,
     "P3 candidate: git.kernel.org's plain text of Documentation/process/cve.rst; a bot challenge page (unavailable); the record uses the docs.kernel.org rendering."),
    ('policies-2026-11-04T1415Z', 'linux_distros', OPENWALL, "P4: the linux-distros list's policy (brief.md, Policies)."),
    ('read-2026-11-17T1419Z', 'openwall_distros_stats', OPENWALL,
     "T7: whether Openwall's linux-distros statistics list the issue; the page read is an index (checkpoints/2026-11-17.md, review/r0091_check.py)."),
]


def text(h):  # as review/r0091_check.py
    h = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S | re.I)
    h = html.unescape(re.sub(r"<[^>]+>", " ", h))
    h = h.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", h).strip()


def main():
    n = 0
    for d, name, robots, used in TARGETS:
        p = DATA / d / (name + '.raw.gz')
        if not p.exists():
            continue
        row = next(r for r in json.loads((DATA / d / 'read_log.json').read_text()) if r['name'] == name)
        h = gzip.open(p).read().decode('utf-8', 'replace')
        t = text(h)
        title = re.search(r'(?s)<title>(.*?)</title>', h)
        lm = re.search(r'Last modified: [\d/]+', t)
        ext = {'challenge_page': 'not a bot' in h[:2000], 'title': title.group(1).strip() if title else None,
               'last_modified_line': lm.group(0) if lm else None}
        if name == 'linux_distros':
            ext['quoted_phrases'] = {q: q in t for q in P4}
        if name == 'openwall_distros_stats':
            ext['names_' + CVE] = CVE in t
            ext['distros_stats_links'] = sorted(set(re.findall(r'href="(/wiki/mailing-lists/distros/stats[^"?]*)"', h)))
        rec = {'url': row['url'], 'read_utc': row.get('start_utc'), 'finish_utc': row.get('finish_utc'),
               'http_status': row.get('status'), 'final_url': row.get('final_url'), 'bytes': row.get('bytes'),
               'sha256': row.get('sha256'), 'robots_class': robots, 'body_removed': NOTE, 'used_for': used, 'extracted': ext}
        (DATA / d / (name + '.derived.json')).write_text(json.dumps(rec, indent=1, ensure_ascii=False) + '\n')
        n += 1
    print('derived files written:', n)


if __name__ == '__main__':
    main()
