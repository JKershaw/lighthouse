#!/usr/bin/env python3
"""LH002: headline figures computed from the published tables, so that every number in LH002.md
traces to a retained file. Usage: python3 summarise.py <study_dir>"""
import csv, json, os, sys
STUDY = sys.argv[1]; D = os.path.join(STUDY, 'data')
rd = lambda n: list(csv.DictReader(open(os.path.join(D, n))))
days, summ, rels = rd('repo_day.csv'), rd('repo_summary.csv'), rd('pypi_releases_in_window.csv')
gha = json.load(open(os.path.join(D, 'gharchive_2026-04-02-14_summary.json')))
swh = json.load(open(os.path.join(D, 'software_heritage_coverage.json')))
obs = [r for r in days if r['status'] == 'observed']
f = []
def add(name, value, basis): f.append(dict(figure=name, value=value, basis=basis))
tot = sum(int(r['commits']) for r in obs); od = len(obs); act = sum(1 for r in obs if int(r['commits']) > 0)
add('observed repository-days', od, 'repo_day.csv status=observed')
add('missing repository-days (no GitHub history yet)', 280 - od, 'repo_day.csv, R04 before 2026-04-04')
add('active repository-days', act, 'observed days with at least one commit')
add('commits in window', tot, 'repo_day.csv')
add('commits per observed repository-day', round(tot / od, 2), 'commits / observed days')
ex = [r for r in obs if r['repo'] != 'R06']; te = sum(int(r['commits']) for r in ex)
add('commits in window excluding R06', te, 'repo_day.csv')
add('commits per observed repository-day excluding R06', round(te / len(ex), 2), '')
for cls in ('bot', 'human_account', 'unknown'):
    n = sum(int(r[f'commits_{cls}']) for r in obs)
    add(f'commits by author class: {cls}', n, f'share {n/tot:.3f} of all; excluding R06 {sum(int(r[f"commits_{cls}"]) for r in ex)}')
add('additions outside lockfiles and vendored paths', sum(int(r['additions_other']) for r in obs), '')
add('deletions outside lockfiles and vendored paths', sum(int(r['deletions_other']) for r in obs), '')
add('additions in lockfiles', sum(int(r['additions_lock']) for r in obs), '')
add('deletions in lockfiles', sum(int(r['deletions_lock']) for r in obs), '')
add('additions in vendored paths', sum(int(r['additions_vendored']) for r in obs), '')
add('commits naming an AI tool in a trailer', sum(int(r['commits_with_ai_tool_trailer']) for r in obs), 'self-declared; not an authorship measure')
add('manifest dependency changes', sum(int(r['manifest_dependency_changes']) for r in obs), 'per package per file per commit')
add('PyPI releases of cohort packages in window', len(rels), 'pypi_releases_in_window.csv')
add('git tags created in window', len(rd('tags_in_window.csv')), 'creatordate; a lightweight tag carries its commit date')
add('GH Archive hour: events', gha['events'], gha['file'])
add('GH Archive hour: compressed bytes', gha['bytes'], gha['file'])
add('GH Archive hour: cohort events', sum(c['events'] for c in gha['cohort']), '')
add('GH Archive window estimate: files', 28 * 24, '28 days x 24 hours')
add('GH Archive window estimate: compressed bytes if every hour matched this one', 28 * 24 * gha['bytes'], 'scenario, not a measurement')
s = gha['parse_seconds']
add('GH Archive hour: parse seconds on this container', s, 'gharchive_hour.py, one run')
add('GH Archive window estimate: parse hours at that rate', round(28 * 24 * s / 3600, 2), 'scenario, not a measurement')
add('Software Heritage: GitHub origins archived', sum(1 for r in swh['repositories'] if r['github_origin_archived'] == 'yes'), 'of 10')
add('Software Heritage: window-end heads archived', sum(1 for r in swh['repositories'] if r['window_end_head_in_archive'] == 'yes'), 'of archived origins')
for r in summ:
    add(f"{r['repo']} commits per observed day", r['commits_per_observed_day'], f"{r['commits']} commits over {r['observed_days']} days, {r['active_days']} active")
with open(os.path.join(D, 'headline_figures.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=['figure', 'value', 'basis']); w.writeheader(); w.writerows(f)
for x in f: print(x['figure'], '=', x['value'], '|', x['basis'])
