#!/usr/bin/env python3
"""LH037 mention counts: the protocol's original rule beside the rule of the amendment of 12 November 2026.

A count is a prompt to open a body, never a finding.

- Original rule (protocol 0.1, kept so the series stays comparable): each CVE id counted exactly as written
  in upper case (`bytes.count`), and `PHP` counted case-sensitive as a whole word (`\\bPHP\\b`).
- Amended rule (12 November 2026, made after the 12 November read, when D-Link's listing naming the flaws only
  as "PHP2Shell" scored 0): `php` in any case at the start of a word, so that PHP, PHP2Shell, php-fpm, PHP-FPM,
  php_admin_value, phpinfo and /php/ path segments count; not when the letters sit inside a longer word
  (`aphp`, `cephp`) or straight after a dot (`index.php`, `www.php.net`), which is a file suffix or a host
  name, not a name for PHP or its flaws. Each CVE id is also counted in any case (`cve-2026-109618` in URLs).

Run `python3 -I studies/LH037/scripts/mentions.py` to run the self-test.
"""
import re

OLD_PHP = re.compile(rb'\bPHP\b')
NEW_PHP = re.compile(rb'(?i)(?<![a-z0-9.])php')


def counts(body: bytes, cves) -> dict:
    """The original keys (each CVE id and 'PHP') unchanged, plus the amended rule's counts under new keys."""
    result = {c: body.count(c.encode()) for c in cves}
    result['PHP'] = len(OLD_PHP.findall(body))
    result['php_prefix'] = len(NEW_PHP.findall(body))
    result['cve_any_case'] = {c: len(re.findall(re.escape(c.encode()), body, re.I)) for c in cves}
    return result


def flagged_old(m: dict, cves) -> bool:
    return m['PHP'] > 0 or any(m[c] > 0 for c in cves)


def flagged_new(m: dict, cves) -> bool:
    return m['php_prefix'] > 0 or any(v > 0 for v in m['cve_any_case'].values())


def _selftest():
    cves = ['CVE-2026-109618', 'CVE-2026-109619', 'CVE-2026-115560']
    caught = [b'PHP', b'the PHP2Shell flaws', b'PHP2shell.', b'php-fpm', b'PHP-FPM', b'(php)', b'"php_admin_value',
              b'/php/php-src/', b'_php-core-rce', b'phpinfo()', b'Php 8.2']
    missed = [b'aphp', b'cephpx', b'index.php', b'https://www.php.net/', b'load.php?lang=en', b'graph', b'P H P']
    for s in caught:
        assert NEW_PHP.search(s), s
    for s in missed:
        assert not NEW_PHP.search(s), s
    m = counts(b'D-Link ... Regarding the PHP2Shell Critical Vulnerabilities', cves)
    assert m['PHP'] == 0 and m['php_prefix'] == 1 and not flagged_old(m, cves) and flagged_new(m, cves)
    m = counts(b'href="/advisory/cve-2026-109618"', cves)
    assert m['CVE-2026-109618'] == 0 and m['cve_any_case']['CVE-2026-109618'] == 1 and flagged_new(m, cves)
    m = counts(b'PHP php PHP2Shell', cves)
    assert (m['PHP'], m['php_prefix']) == (1, 3)
    print('mentions.py self-test: %d caught, %d not caught, 3 count checks: ok' % (len(caught), len(missed)))


if __name__ == '__main__':
    _selftest()
