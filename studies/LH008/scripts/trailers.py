#!/usr/bin/env python3
"""LH008: the Co-authored-by trailers naming an AI system or a bot on each moving commit (and, for a merge,
on the merged branch's tip), read from the local clones. No network access (the clones are in
LH008_SCRATCH). Writes data/trailers.csv; analyse.py takes its ai_coauthor column from here."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv, git, SCRATCH

AI = re.compile(r'(?i)claude|anthropic|copilot|cursor|codex|openai|chatgpt|devin|gemini|aider|sweep|jules')
rows = []
for m in read_csv('moves.csv'):
    if not m['move_commit']:
        continue
    d = os.path.join(SCRATCH, 'repos', m['repo'].replace('/', '__'))
    revs = [m['move_commit']] + ([m['move_commit'] + '^2'] if m['merge'] == 'yes' else [])
    names = []
    for rev in revs:
        msg = git(['log', '-1', '--format=%B', rev], cwd=d, check=False)
        for l in msg.splitlines():
            if l.lower().startswith('co-authored-by:'):
                n = re.sub(r'<[^>]*>', '', l.split(':', 1)[1]).strip()
                if AI.search(n) or '[bot]' in n:
                    names.append(n)
    rows.append(dict(frame=m['frame'], package=m['package'], repo=m['repo'], move_commit=m['move_commit'],
                     ai_or_bot_coauthors='; '.join(dict.fromkeys(names)),
                     ai_coauthor='yes' if any(AI.search(n) for n in names) else ''))
write_csv('trailers.csv', rows)
print(sum(r['ai_coauthor'] == 'yes' for r in rows), [r['ai_or_bot_coauthors'] for r in rows if r['ai_or_bot_coauthors']])
