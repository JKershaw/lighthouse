#!/usr/bin/env python3
"""LH007 step 5b: who moved each project's pin or lock to 1.28.x: the first commit in
data/first_new.csv's project_first_128 column, with the commit's author recorded only as the kind of
account (a bot account's name, or 'a person') and any co-author trailer naming a bot or an AI model.
Personal names and addresses are not recorded. Local git only. Writes data/pin_movers.csv."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv, git, SCRATCH
from collect_builds import REPO

import datetime
ADV = datetime.datetime(2026, 7, 16, 20, 14, 34, tzinfo=datetime.timezone.utc)  # GHSA-vj7q-gjh5-988w published (data/osv_mcp_1_28_0.csv)
REL = datetime.datetime(2026, 6, 16, 21, 37, 16, tzinfo=datetime.timezone.utc)
out = []
for r in read_csv('first_new.csv'):
    if not r['project_first_128'] or r['project_first_128'].startswith('none'):
        continue
    repo = REPO[r['image']][0]
    sha = r['project_first_128'].split()[0]
    d = os.path.join(SCRATCH, 'repos', repo.replace('/', '__'))
    a = git(['show', '-s', '--format=%an', sha], cwd=d).strip()
    subj = git(['show', '-s', '--format=%s', sha], cwd=d).strip()
    body = git(['show', '-s', '--format=%b', sha], cwd=d)
    kind = a if re.search(r'bot\b|\[bot\]|renovate|dependabot', a, re.I) else 'a person'
    if kind == 'a person' and re.search(r'dependabot/|renovate/', subj):
        kind = 'a person, merging a branch opened by ' + re.search(r'(dependabot|renovate)', subj).group(1)
    co = sorted({m.strip() for m in re.findall(r'(?im)^co-authored-by:\s*([^<\n]*?(?:bot|claude|copilot|gpt|gemini|cursor)[^<\n]*)', body)})
    out.append(dict(image=r['image'], repo=repo, commit=sha, when=r['project_first_128'].split()[1],
                    file_and_value=' '.join(r['project_first_128'].split()[2:]), author_kind=kind,
                    bot_or_ai_coauthor='; '.join(co), subject=subj[:100],
                    days_after_release=round((datetime.datetime.fromisoformat(r['project_first_128'].split()[1].replace('Z', '+00:00')) - REL).total_seconds() / 86400, 2),
                    hours_after_advisory=round((datetime.datetime.fromisoformat(r['project_first_128'].split()[1].replace('Z', '+00:00')) - ADV).total_seconds() / 3600, 1)))
write_csv('pin_movers.csv', out)
for o in out:
    print(o['repo'].split('/')[-1], o['when'][:16], o['days_after_release'], o['hours_after_advisory'], o['author_kind'][:30])
