#!/usr/bin/env python3
"""LH010 step 2: read the project's own words for each distinct fixed release behind a qualifying advisory of a
library with an event (data/qualifying_advisories.csv, data/events.csv), by LH009's classification rule as brief.md
restates it. No dependent is read here. Copied from LH009's classify.py and changed as follows: the fixes come
from LH010's qualifying advisories, not LH008's; the events that are the same release as LH008's (whose class
LH009 recorded) are skipped, since classes.py takes their class from studies/LH009/data/fix_classes.csv; GitHub's
release pages are not requested (every one was refused in LH009); fix_reads.csv records which fixes are events;
the library clones go in LH010_SCRATCH/libs and may be deleted once classes.py has run.

Writes data/fix_texts.csv and data/fix_reads.csv."""
import csv, html, json, os, re, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import jget, http, write_csv, read_csv, git, SCRATCH, now, log, ts, iso, norm

LH008 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'LH008', 'data')
SECW = re.compile(r'(?i)security|vulnerab|CVE-\d|GHSA-|PYSEC-|CWE-\d|advisory|advisories|exploit|attacker')
q = lambda s: urllib.parse.quote(s, safe='')
CAP = 8 * 1024 ** 3  # brief.md: 8 GB for everything in LH010_SCRATCH, checked before each clone


def du(path):
    import subprocess
    p = subprocess.run(['du', '-sb', path], capture_output=True, text=True)
    return int(p.stdout.split()[0]) if p.returncode == 0 and p.stdout else 0
TEXT_EXT = ('', '.md', '.rst', '.txt', '.markdown', '.mdx')
DIRS = {'changelog', 'changes', 'news', 'release-notes', 'release_notes', 'releasenotes', 'releases', 'whatsnew'}


REUSED = {(e['library'], e['fixed_release']) for e in csv.DictReader(open(os.path.join(LH008, 'events.csv')))}


def fixes():
    ev = {(e['library'], e['fixed_release']) for e in read_csv('events.csv')}
    out = {}
    for r in read_csv('qualifying_advisories.csv'):
        if r['qualifies'] != 'yes':
            continue
        k = (r['project'], r['fixed_release'])
        e = out.setdefault(k, dict(library=r['project'], rank=r['rank'], version=r['fixed_release'], event='yes' if k in ev else 'no',
                                   uploaded=r['fixed_uploaded'], advisories=[], summaries=[], first_advisory=r['published']))
        e['advisories'].append(r['id'])
        e['summaries'].append(r['summary'])
        if ts(r['published']) < ts(e['first_advisory']):
            e['first_advisory'] = r['published']
    return sorted([e for k, e in out.items() if not (e['event'] == 'yes' and k in REUSED)],
                  key=lambda e: (int(e['rank']), ts(e['uploaded'])))


def repo_of(pj):
    urls = list((pj['info'].get('project_urls') or {}).items()) + [('home_page', pj['info'].get('home_page') or '')]
    order = lambda kv: next((i for i, w in enumerate(('source', 'repository', 'code', 'homepage', 'home')) if w in kv[0].lower()), 9)
    urls.sort(key=order)
    for _, u in urls:
        u = (u or '').rstrip('/')
        for host in ('github.com/', 'gitlab.com/'):
            if host in u.lower():
                parts = u.split(host if host in u else host.capitalize())[-1].split('/')
                if len(parts) >= 2 and parts[1]:
                    return host + parts[0] + '/' + parts[1].removesuffix('.git').split('#')[0]
    return ''


def tok(v):
    return r'(?<![\d.])' + re.escape(v) + r'(?![\d]|\.\d)'


def verline(name):
    n = re.escape(name).replace(r'\-', '[-_ ]?')
    return re.compile(r'(?i)^[\s#*`\[=\-_>|:]*(?:(?:version|release|revision|:version:)\s*:?\s*|' + n + r'[\s=\-]*)?v?(\d+(?:\.\d+)+[a-z0-9.\-]*)')


def entry(text, v, name):
    """The part of text from the first version line naming v to the next version line naming another."""
    if not text:
        return None
    vl = verline(name)
    lines = text.splitlines()
    start = None
    for i, l in enumerate(lines):
        m = vl.match(l)
        if m and re.match(tok(v), m.group(1)):
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        m = vl.match(lines[j])
        if m and not re.match(tok(v), m.group(1)) and re.fullmatch(r'\d+(\.\d+)+.*', m.group(1)):
            # a heading-like line: short, or followed by an underline, or starting with markup
            if len(lines[j].strip()) < 90:
                end = j
                break
    # an rst heading's underline belongs to the next heading; drop a trailing underline-less anchor line
    return '\n'.join(lines[start:end]).strip()


def words(t):
    if not t:
        return ''
    hits = []
    for m in SECW.finditer(t):
        a, b = max(0, m.start() - 80), min(len(t), m.end() + 80)
        hits.append(t[a:b].replace('\n', ' '))
    return ' | '.join(dict.fromkeys(hits))[:1500]


def find_tag(d, name, v):
    tags = git(['tag', '-l'], cwd=d).split()
    low = {t.lower(): t for t in tags}
    for c in (f'v{v}', v, f'{name}-{v}', f'{name}-v{v}', f'{name}=={v}', f'release-{v}',
              f'{norm(name)}-{v}', f"{name.replace('-', '_')}-{v}",
              'rel_' + v.replace('.', '_')):  # SQLAlchemy's form (mako), added by brief.md amendment 1
        if c.lower() in low:
            return low[c.lower()], 'named form'
    cands = [t for t in tags if re.search(tok(v), t)]
    if cands:
        return min(cands, key=len), 'shortest tag containing the version'
    return '', ''


def changelog_files(d, rev, v):
    try:
        paths = git(['ls-tree', '-r', '--name-only', rev], cwd=d).splitlines()
    except Exception:
        return []
    out = []
    for p in paths:
        if p.count('/') > 4:
            continue
        b = p.rsplit('/', 1)[-1]
        ext = os.path.splitext(b)[1].lower()
        if ext not in TEXT_EXT:
            continue
        dirs = {x.lower() for x in p.split('/')[:-1]}
        if re.match(r'(?i)(change|history|news|release|whatsnew)', b) or (dirs & DIRS and re.search(tok(v), p)):
            out.append(p)
    return sorted(out, key=lambda p: (p.count('/'), p))


def read_changelog(d, rev, v, name):
    """[(path, entry)] for changelog files at rev that hold an entry for v."""
    got = []
    for p in changelog_files(d, rev, v):
        try:
            t = git(['show', f'{rev}:{p}'], cwd=d, timeout=300)
        except Exception:
            continue
        e = entry(t, v, name)
        if e is None and re.search(tok(v), p):
            e = t.strip()  # a per-release notes file: the whole file is the entry
        if e:
            got.append((p, e))
    return got


def release_page(repo, tag):
    if not repo.startswith('github.com/') or not tag:
        return None, ''
    url = f'https://{repo}/releases/tag/{q(tag)}'
    r = http('GitHub release page (HTML, not the API)', f'release page {repo} {tag}', url)
    if r.status_code != 200:
        return None, str(r.status_code)
    m = re.search(r'<div[^>]*class="markdown-body[^"]*"[^>]*>(.*?)</div>\s*(?:</div>|<div)', r.text, re.S)
    body = m.group(1) if m else ''
    txt = html.unescape(re.sub(r'<[^>]+>', ' ', body))
    txt = re.sub(r'[ \t]+', ' ', txt)
    txt = re.sub(r'\n\s*\n+', '\n', txt).strip()
    return txt, '200' if m else '200, no release body found'


def main():
    base = os.path.join(SCRATCH, 'libs')
    os.makedirs(base, exist_ok=True)
    texts, reads = [], []
    repos = {}
    for f in fixes():
        lib, v = f['library'], f['version']
        pj = jget('PyPI JSON API', f'PyPI {lib} {v}', f'https://pypi.org/pypi/{q(lib)}/{q(v)}/json')
        name = pj['info']['name'] if pj else lib
        repo = repos.get(lib) or (repo_of(pj) if pj else '')
        repos[lib] = repo
        d = os.path.join(base, repo.replace('/', '__'))
        if repo and not os.path.exists(os.path.join(d, 'HEAD')) and du(SCRATCH) < CAP:
            t = now()
            try:
                git(['clone', '-q', '--filter=blob:none', '--no-checkout', '--bare', f'https://{repo}.git', d], timeout=1800)
                st = 'cloned'
            except Exception as ex:
                st = 'failed: ' + str(ex)[:160]
            log(read_utc=t, source='git over HTTPS', label=f'library clone {lib}', method='git clone --bare --filter=blob:none',
                endpoint=f'https://{repo}.git', note=st)
        tag, how = find_tag(d, name, v) if repo and os.path.exists(os.path.join(d, 'HEAD')) else ('', '')
        row = dict(library=lib, rank=f['rank'], version=v, event=f['event'], uploaded=f['uploaded'], first_advisory=f['first_advisory'],
                   advisories=' '.join(f['advisories']), advisory_summaries=' || '.join(dict.fromkeys(f['summaries'])),
                   repo=repo, tag=tag, tag_found_by=how, tag_type='', tag_commit='', tag_commit_time='', tagger_time='',
                   head_commit='', head_time='')
        if tag:
            row['tag_type'] = git(['cat-file', '-t', f'refs/tags/{tag}'], cwd=d).strip()
            row['tag_commit'] = git(['rev-parse', f'refs/tags/{tag}^{{commit}}'], cwd=d).strip()[:12]
            row['tag_commit_time'] = iso(ts(git(['show', '-s', '--format=%cI', f'refs/tags/{tag}^{{commit}}'], cwd=d).strip()))
            if row['tag_type'] == 'tag':
                raw = git(['cat-file', '-p', f'refs/tags/{tag}'], cwd=d)
                hdr, _, msg = raw.partition('\n\n')
                m = re.search(r'^tagger .* (\d+) ([+-]\d{4})$', hdr, re.M)
                if m:
                    import datetime
                    row['tagger_time'] = iso(datetime.datetime.fromtimestamp(int(m.group(1)), datetime.timezone.utc))
                msg = re.sub(r'-----BEGIN (PGP|SSH) SIGNATURE-----.*', '', msg, flags=re.S).strip()
                texts.append(dict(library=lib, version=v, source='tag annotation', where=tag, dated=row['tagger_time'],
                                  chars=len(msg), security_words=words(msg), text=msg[:3000]))
            else:
                texts.append(dict(library=lib, version=v, source='tag annotation', where=tag + ' (lightweight tag: no annotation)',
                                  dated='', chars=0, security_words='', text=''))
            for p, e in read_changelog(d, f'refs/tags/{tag}', v, name):
                texts.append(dict(library=lib, version=v, source='changelog at tag', where=p, dated=row['tag_commit_time'],
                                  chars=len(e), security_words=words(e), text=e[:3000]))
        if repo and os.path.exists(os.path.join(d, 'HEAD')):
            row['head_commit'] = git(['rev-parse', 'HEAD'], cwd=d).strip()[:12]
            row['head_time'] = iso(ts(git(['show', '-s', '--format=%cI', 'HEAD'], cwd=d).strip()))
            for p, e in read_changelog(d, 'HEAD', v, name):
                texts.append(dict(library=lib, version=v, source='changelog at head', where=p, dated=row['head_time'],
                                  chars=len(e), security_words=words(e), text=e[:3000]))
        desc = (pj or {}).get('info', {}).get('description') or ''
        de = entry(desc, v, name)
        texts.append(dict(library=lib, version=v, source='PyPI description', where=f'info.description ({len(desc)} chars)',
                          dated=f['uploaded'], chars=len(de or ''), security_words=words(de),
                          text=(de or '(no part of the description names this version)')[:3000]))
        reads.append(row)
        print(lib, v, f['event'], repo, tag or '(no tag)', [(t['source'][:12], bool(t['security_words'])) for t in texts if t['library'] == lib and t['version'] == v], flush=True)
    write_csv('fix_reads.csv', reads)
    write_csv('fix_texts.csv', texts, ['library', 'version', 'source', 'where', 'dated', 'chars', 'security_words', 'text'])


if __name__ == '__main__':
    main()
