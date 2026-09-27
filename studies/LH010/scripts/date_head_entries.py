#!/usr/bin/env python3
"""LH010 step 2b (new; LH009 did this by hand for the one case it met): for each fix whose changelog entry at the
head holds a security word that its entry at the tag does not (or that has no entry at the tag), find the first
first-parent commit on the default branch, from the release's upload onward, whose version of that changelog file
holds the version's entry with a security word, as LH009's brief says ("its history decides when the entry was
written"). No network access; reads the library clones classify.py made.

Appends one row per such fix to data/fix_texts.csv with source 'changelog after the tag (history)', dated at that
commit's committer time, so classes.py can call the fix announced late (words before the advisory) or silent."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv, git, SCRATCH, ts, iso
from classify import entry, words

T = read_csv('fix_texts.csv')
T = [t for t in T if t['source'] != 'changelog after the tag (history)']
out = []
for r in read_csv('fix_reads.csv'):
    k = (r['library'], r['version'])
    m = [t for t in T if (t['library'], t['version']) == k]
    head = [t for t in m if t['source'] == 'changelog at head' and t['security_words']]
    tag_sec = [t for t in m if t['source'] == 'changelog at tag' and t['security_words']]
    if not head or tag_sec:
        continue
    d = os.path.join(SCRATCH, 'libs', r['repo'].replace('/', '__'))
    found = None
    for h in head:
        revs = git(['log', '--first-parent', '--reverse', '--format=%H %cI', f"--since={iso(ts(r['uploaded']))}", 'HEAD', '--', h['where']], cwd=d).split('\n')
        for line in filter(None, revs):
            c, t = line.split()
            txt = git(['show', f"{c}:{h['where']}"], cwd=d, check=False)
            e = entry(txt, r['version'], r['library'])
            if e and words(e):
                if not found or ts(t) < ts(found[1]):
                    found = (c, t, h['where'], e)
                break
    if found:
        c, t, p, e = found
        out.append(dict(library=r['library'], version=r['version'], source='changelog after the tag (history)',
                        where=f'{p} at {c[:12]}', dated=iso(ts(t)), chars=len(e), security_words=words(e), text=e[:3000]))
        print(r['library'], r['version'], 'first with a security word:', c[:12], iso(ts(t)), p, 'upload', r['uploaded'], 'advisory', r['first_advisory'])
write_csv('fix_texts.csv', T + out, ['library', 'version', 'source', 'where', 'dated', 'chars', 'security_words', 'text'])
