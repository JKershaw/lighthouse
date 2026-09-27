#!/usr/bin/env python3
"""LH010 reanalysis of retained evidence, for version 0.3 of the record (27 September 2026). New; no network access;
standard library only. It reads the tables in data/ (and studies/LH009/data/fix_texts.csv and fix_reads.csv for the
twelve events whose class LH010 took from LH009) and writes data/reanalysis/, or the directory given by --out.

This is an OUTCOME-AWARE reanalysis, designed after every move and every rate in version 0.2 was known. It is not a
preregistered comparison, and nothing here changes the brief's rules, the events, the classes or the committed
tables. Case selection (which events, fixes and pairs are in, and their class) is the brief's, unchanged; what is
varied is (1) the clock that ends the window "before the advisory" and (2) whether an event is kept, by whether
notes for its fixed release could be read at release time. The pooled rates, windows, at-risk rule, library rates,
medians and permutation test are analyse.py's own functions, imported, so each addition's effect can be told apart
from the original definitions. With the original clock and every event, the comparisons reproduce
data/library_unit.csv and data/hazard_by_class.csv (test_reanalyse.py checks this).

Clocks (per frame; data/reanalysis/clocks.csv):
  event_advisory      the event advisory's OSV `published` time (the brief's rule 4; version 0.2's clock).
  earliest_reviewed   the earliest OSV `published` time among the RETAINED records that name the frame's fixed
                      release. Records searched: data/osv_advisories.csv, the OSV records for the 500 projects as read
                      on 27 September 2026 at 09:53 to 09:56 UTC, as they stood then. A record counts if its project is
                      the library, its id begins `GHSA-`, its github_reviewed field is `True`, its withdrawn field is
                      empty, and the frame's fixed release is, as an exact string, one of the `fixed` versions in its
                      ECOSYSTEM ranges for the package (any range, not only the highest; PEP 440 equality gives the
                      same matches in these data). No publication window and no rule 3 (fix a day earlier) apply.
  earliest_public     the earliest of `published` and `nvd_published_at` over the same counted records (analyse.py's
                      "first public record", GHSA or NVD, widened from the event advisory to every counted record).
Neither is the first warning anywhere: mailing lists, NVD searched directly, vendor posts, the projects' own notes
and commit messages were not searched as a clock; records carry their fields as read on 27 September, not as first
published, so a record published before the fix was released cannot have named the fix then; PYSEC and other
unreviewed OSV records are listed in advisories_naming_fix.csv but not counted.

Notes evidence (per fixed release; data/reanalysis/notes_evidence.csv), the rule fixed in the record's section
"Reanalysis of retained evidence, version 0.3" before it was applied:
  a  announcement observed: the fix's class under the brief's rule is announced.
  b  notes inspected, no announcement found: class silent (or announced late), and at least one text for the
     version, from a source the rule read (changelog entry at the tag, the PyPI description's part for the version,
     the tag's annotation, or a changelog entry dated from the file's history), is dated no later than 24 hours
     after the first upload (the classification rule's own allowance) and is substantive (SUBSTANTIVE below).
  c  insufficient accessible notes: neither; no such text existed in a read source at release time, or the only
     such text is a bare label (a version-bump, "Release x", "sig" or signature-only annotation).
GitHub release pages were not requested in LH010 and were refused (403) in LH009; they are named as missing in
every c case. The judgements on ambiguous cases are in AMBIGUOUS below and data/reanalysis/notes_ambiguous.csv;
none overrides the code's state.

Outputs (data/reanalysis/):
  advisories_naming_fix.csv  every retained OSV record naming each frame's fixed release, counted or not, and why.
  clocks.csv                 per frame, every clock: event advisory, its github_reviewed_at and nvd_published_at,
                             analyse.py's first_public_time, earliest_reviewed and earliest_public.
  notes_evidence.csv         per fix (43 events, 5 within-library second fixes): state a, b or c and the reason.
  notes_ambiguous.csv        the ambiguous cases and the judgement made.
  library_rates.csv          each library's moves, repository-days and rate, by clock and window.
  comparisons.csv            by clock, case set, grouping and window: libraries, pairs, moves and repository-days
                             kept and lost, pooled rates and their ratio with a library-clustered bootstrap
                             interval, library medians with the permutation p and a bootstrap interval for their
                             difference, leave-one-library-out ranges, and moves before the clock.
"""
import argparse, csv, datetime, os, random, re, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyse as A  # the committed definitions (load, hazard, perm_test, windows, seed); reads data/ only
from common import read_csv, ts, iso, DATA

STUDY = os.path.dirname(HERE)
LH009_DATA = os.path.join(os.path.dirname(STUDY), 'LH009', 'data')
OUT_DEFAULT = os.path.join(DATA, 'reanalysis')
NBOOT, BSEED = 10000, 20260927
td = datetime.timedelta
UNIT_WINDOWS = A.UNIT_WINDOWS  # release to the advisory; release +2 to +7 days stopping at the advisory
CLOCKS = ['event_advisory', 'earliest_reviewed', 'earliest_public']
CASE_SETS = ['all events (version 0.2)', 'sufficient notes (states a and b)']


# ---------- 1. records naming the fix, and the clocks ----------

def counted(rec):
    """(counts, reason) for one retained OSV record: GitHub-reviewed, unwithdrawn GHSA records only."""
    if not rec['id'].startswith('GHSA-'):
        return False, 'not a GHSA record'
    if rec.get('github_reviewed') != 'True':
        return False, 'not GitHub-reviewed'
    if rec.get('withdrawn'):
        return False, 'withdrawn'
    return True, 'counted'


def records_naming_fix(osv, library, version):
    """Every retained record against `library` whose fixed versions include `version` exactly."""
    return [r for r in osv if r['project'] == library and version in r['fixed'].split()]


def earliest_reviewed(osv, library, version):
    """The counted record naming the fix with the earliest `published` time, or None."""
    rs = [r for r in records_naming_fix(osv, library, version) if counted(r)[0]]
    return min(rs, key=lambda r: (ts(r['published']), r['id'])) if rs else None


def earliest_public(osv, library, version):
    """(time, record id, which field) of the earliest `published` or `nvd_published_at` among counted records."""
    best = None
    for r in records_naming_fix(osv, library, version):
        if not counted(r)[0]:
            continue
        for field in ('published', 'nvd_published_at'):
            if r.get(field):
                c = (ts(r[field]), r['id'], field)
                if best is None or c < best:
                    best = c
    return best


def days(a, b):
    return round((a - b).total_seconds() / 86400, 2)


def build_clocks(frames, osv):
    rows, recs = [], []
    by_id = {}
    for r in osv:
        by_id.setdefault((r['project'], r['id']), r)
    for f in frames:
        lib, fx, up = f['library'], f['fixed_release'], ts(f['fixed_uploaded'])
        adv = ts(f['advisory_published'])
        ev = by_id.get((lib, f['advisory']), {})
        first_public = min([adv] + ([ts(f['nvd_published_at'])] if f['nvd_published_at'] else []))
        er = earliest_reviewed(osv, lib, fx)
        ep = earliest_public(osv, lib, fx)
        named = records_naming_fix(osv, lib, fx)
        others = sorted((r for r in named if not counted(r)[0]), key=lambda r: ts(r['published']))
        rows.append(dict(
            frame=f['frame'], library=lib, kind=f['kind'], fixed_release=fx, fixed_uploaded=iso(up), cls=f['cls'],
            event_advisory=f['advisory'], event_advisory_published=iso(adv),
            event_advisory_github_reviewed_at=ev.get('github_reviewed_at', ''),
            event_advisory_nvd_published_at=f['nvd_published_at'],
            first_public_time_as_in_lags=iso(first_public),
            reviewed_records_naming_fix=sum(counted(r)[0] for r in named),
            earliest_reviewed_id=er['id'] if er else '', earliest_reviewed_severity=er['severity'] if er else '',
            earliest_reviewed=iso(ts(er['published'])) if er else '',
            earliest_reviewed_differs='yes' if er and er['id'] != f['advisory'] and ts(er['published']) < adv else 'no',
            earliest_reviewed_before_release='yes' if er and ts(er['published']) <= up else 'no',
            earliest_public=iso(ep[0]) if ep else '', earliest_public_from=f'{ep[1]} {ep[2]}' if ep else '',
            days_release_to_event_advisory=days(adv, up),
            days_release_to_earliest_reviewed=days(ts(er['published']), up) if er else '',
            days_release_to_earliest_public=days(ep[0], up) if ep else '',
            earliest_uncounted_record=f"{others[0]['id']} {iso(ts(others[0]['published']))}" if others else '',
        ))
        for r in sorted(named, key=lambda r: (ts(r['published']), r['id'])):
            ok, why = counted(r)
            recs.append(dict(frame=f['frame'], library=lib, fixed_release=fx, id=r['id'], aliases=r['aliases'],
                             severity=r['severity'], github_reviewed=r['github_reviewed'], withdrawn=r['withdrawn'],
                             published=iso(ts(r['published'])), github_reviewed_at=r['github_reviewed_at'],
                             nvd_published_at=r['nvd_published_at'], modified=r['modified'], fixed=r['fixed'],
                             is_event_advisory='yes' if r['id'] == f['advisory'] else 'no',
                             days_from_release=days(ts(r['published']), up), counted_in_clock=ok, reason=why))
    return rows, recs


# ---------- 2. notes evidence at release time ----------

PRIMARY = ('changelog at tag', 'tag annotation', 'PyPI description', 'changelog after the tag (history)')
AT_RELEASE = td(hours=24)
_SIG = re.compile(r'-----BEGIN [A-Z ]+-----.*', re.S)
_URL = re.compile(r'https?://\S+|\S+\.(?:com|org|io)/\S*')
_VER = re.compile(r'\bv?\d+(?:[.\-]\w+)*\b')
_LABEL = {'release', 'released', 'releases', 'version', 'bump', 'bumped', 'tagging', 'tag', 'this', 'is', 'rel', 'sig',
          'on', 'new', 'what', 's', 'whats', 'revision', 'changes', 'changelog', 'full', 'compare', 'v', 'in', 'the',
          'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'sept', 'oct', 'nov', 'dec', 'january',
          'february', 'march', 'april', 'june', 'july', 'august', 'september', 'october', 'november', 'december',
          'st', 'nd', 'rd', 'th', 'date', 'rc'}


def substantive(text, library=''):
    """True if the text says something beyond a label: after signature blocks, URLs, version numbers, dates, the
    library's name and label words (release, version, bump, tagging, sig ...) are removed, some line keeps at least
    two words of two or more letters. "Bump version: 1.2.1 -> 1.2.2", "Release 26.1", "sig" and a signed
    "46.0.6 release" are not substantive; "Update for type hints." is."""
    if not text:
        return False
    t = _SIG.sub('', text)
    name = {w for w in re.split(r'[-_.\s]+', library.lower()) if w}
    for line in t.splitlines():
        line = _VER.sub(' ', _URL.sub(' ', line))
        ws = [w for w in re.findall(r"[a-z]+", line.lower()) if len(w) >= 2 and w not in _LABEL and w not in name]
        if len(ws) >= 2:
            return True
    return False


def has_text(t):
    """A read source held a text for the version (a description with no part for it, or a lightweight tag, holds none)."""
    return t['chars'] not in ('', '0') and not t['text'].startswith('(no part of the description')


def notes_state(cls, texts, uploaded, library=''):
    """(state, at-release texts that count, notes). `texts` are fix_texts rows for one fixed release."""
    up = ts(uploaded)
    usable, notes = [], []
    for t in texts:
        if t['source'] not in PRIMARY:
            continue
        if not has_text(t):
            continue
        when = ts(t['dated']) if t['dated'] else None
        if when is None or when > up + AT_RELEASE:
            notes.append(f"{t['source']} {t['where']} dated {t['dated'] or 'undated'}, after the 24 hours: not at release")
            continue
        if not substantive(t['text'], library):
            notes.append(f"{t['source']} {t['where']}: a bare label ({t['text'][:40].strip()!r}), cannot bear on the question")
            continue
        usable.append(t)
    if cls == 'announced':
        return 'a', usable, notes
    return ('b' if usable else 'c'), usable, notes


# Ambiguous cases: the judgement made. None changes the state the code gives; each says why that state stands.
AMBIGUOUS = {
    ('fastmcp', '3.2.0'): 'c. The only entry with security words was first written into docs/changelog.mdx on 3 June 2026 '
        '(commit dae11bbc40fd), 64 days after the release and 63 after the advisory; at the tag the file names 3.2.0 '
        'nowhere, the tag is lightweight and the PyPI description has no part for it. The later entry links a GitHub '
        'release page, which was not requested, so whether notes were there at release is unknown: insufficient, not silent.',
    ('idna', '3.15'): 'a under the rule. Its only security words say CVE-2026-45409 is now referenced for the 3.14 '
        'advisory, and the changelog entry at the tag is headed 3.15rc0 (the tag annotation carries the same list). '
        'Read as not announcing this fix it would be b; either way the notes were inspected, so the sufficient-notes '
        'restriction keeps it. The incidental-words grouping in analyse.py carries the other reading.',
    ('aiohttp', '3.13.4'): 'a under the rule. Its only security words concern 3.13.3 ("decompression bomb security fix", '
        '"to maintain security protections"). Read as not announcing this fix it would be b; kept by the restriction '
        'either way.',
    ('python-dotenv', '1.2.2'): 'b. The tag annotation is a bare "Bump version: 1.2.1 -> 1.2.2" and alone would be '
        'insufficient, but the changelog entry at the tag and the PyPI description part are real entries (Added, '
        'Changed, Breaking Changes) with no security word; "used to follow symlinks in some situations" was judged not '
        'to name the flaw (flaw_judgements.csv).',
    ('snowflake-sqlalchemy', '1.11.0'): 'b. The only text is a banner at the top of the PyPI description naming v1.11.0 '
        '("Sensitive connection parameters ... can no longer be supplied through the URL query string"); there is no '
        'changelog entry at the tag. It describes the release\'s change and carries no security word; judged not to '
        'name the flaw. A stricter reading of "notes" (a changelog entry) would make it c.',
    ('snowflake-connector-python', '4.7.1'): 'b. The only text is the PyPI description\'s release-notes part for v4.7.1; '
        '"Improved verification of TLS connections" was judged to name the change, not a flaw.',
    ('joserfc', '1.6.7'): 'b. The changelog entry is one line, "Update for type hints.", which does not mention the fix; it '
        'is an entry for the version and says nothing of security, so b, though a reader might treat it as no notes.',
    ('awscli', '1.44.78'): 'b. The entry is a machine-written list of api-change lines, one of them "Tighten file permissions '
        'for CodeDeploy configuration file", judged to name the change, not a flaw.',
    ('transformers', '5.0.0rc3'): 'c. A release candidate; no changelog entry at the tag, a lightweight tag, and no part of '
        'the description for it; the project writes its notes on GitHub release pages, which were not requested.',
    ('nbconvert', '7.17.1'): 'c. PyPI names no repository for it, so no changelog or tag was read; the description has no '
        'part for the version.',
    ('mako', '1.3.11'): 'a on the flaw named alone (a borderline judgement recorded in amendment 1); b under the strict '
        'class. Sufficient either way.',
    ('uv', '0.11.6'): 'a on the flaw named alone (borderline); b under the strict class. Sufficient either way; no pairs.',
    ('authlib', '1.7.1'): 'a on the flaw named alone (borderline); b under the strict class. Sufficient either way.',
    ('mistune', '3.2.1'): 'a on the flaw named alone; b under the strict class. Sufficient either way.',
    ('pip', '26.1.2'): 'a on the flaw named alone (borderline; a within-library second fix); b under the strict class.',
}


def build_notes(fix_classes, texts10, texts9, reads10, reads9, frames):
    kinds = {(f['library'], f['fixed_release']): f['kind'] for f in frames}
    out = []
    for r in fix_classes:
        k = (r['library'], r['version'])
        if k not in kinds:
            continue
        reused = r['reused_from_LH009'] == 'yes'
        texts = [t for t in (texts9 if reused else texts10) if (t['library'], t['version']) == k]
        rd = next((x for x in (reads9 if reused else reads10) if (x['library'], x['version']) == k), {})
        state, usable, notes = notes_state(r['class'], texts, r['uploaded'], r['library'])
        pages = [t for t in texts if t['source'].startswith('GitHub release page')]
        page = ('requested in LH009, refused (' + pages[0]['where'] + ')') if pages else 'not requested'
        if not rd.get('repo'):
            where = 'no repository named on PyPI: no changelog or tag read'
        elif not rd.get('tag'):
            where = f"repository {rd['repo']}, no tag found for the version"
        else:
            where = f"repository {rd['repo']}, tag {rd['tag']} ({'annotated' if rd.get('tag_type') == 'tag' else 'lightweight'})"
        if state == 'a':
            if r['basis'] == 'security word':
                reason = f"class announced: a security word in {r['security_word_in']}, dated {r['deciding_text_dated']}"
            else:
                reason = f"class announced on the flaw named in the changelog entry at the tag, dated {r['deciding_text_dated']} (strict class {r['strict_class']})"
        elif state == 'b':
            reason = 'an entry for the version at release time, no announcement under the rule: ' + '; '.join(
                f"{t['source']} {t['where'].split(' (')[0]} ({t['chars']} chars)" for t in usable)
        else:
            src = lambda n: [t for t in texts if t['source'] == n]
            missing = []
            if not rd.get('repo'):
                missing.append('no changelog or tag read (no repository named)')
            else:
                if not any(has_text(t) for t in src('changelog at tag')):
                    missing.append('no changelog entry for the version at the tag')
                ann = src('tag annotation')
                if not ann or not any(has_text(t) for t in ann):
                    missing.append('lightweight tag, no annotation' if ann else 'no tag annotation read')
            if not any(has_text(t) for t in src('PyPI description')):
                missing.append('no part of the PyPI description names the version')
            missing += notes
            missing.append('GitHub release page ' + page)
            reason = 'no substantive text for the version in any read source at release time: ' + '; '.join(missing)
        out.append(dict(library=r['library'], version=r['version'], kind=kinds[k], rank=r['rank'], cls=r['class'],
                        strict_class=r['strict_class'], state=state,
                        state_label={'a': 'announcement observed', 'b': 'notes inspected, no announcement found',
                                     'c': 'insufficient accessible notes'}[state],
                        texts_read_from='LH009 (reused)' if reused else 'LH010', where_read=where,
                        github_release_page=page, reason=reason, other_notes='; '.join(notes) if state != 'c' else '',
                        ambiguous='yes' if k in AMBIGUOUS else 'no'))
    return out


# ---------- 3. the comparisons ----------

def with_clock(rows, clock_of_frame):
    """Copies of analyse.py's pair rows with advisory_time replaced by the frame's clock."""
    out = []
    for r in rows:
        x = dict(r)
        x['advisory_time'] = clock_of_frame[r['frame']]
        out.append(x)
    return out


def lib_table(rows, window):
    """{library: (moves, repo-days)} for libraries with repository-days at risk in the window, in analyse.py's order."""
    lo, hi = A.W[window][1], A.W[window][2]
    out = {}
    for lib in dict.fromkeys(r['library'] for r in rows):
        n, at = A.hazard([r for r in rows if r['library'] == lib], lo, hi)
        if at > 0:
            out[lib] = (n, at)
    return out


def pct(xs, q):
    xs = sorted(xs)
    i = min(len(xs) - 1, max(0, int(q * len(xs)) - (1 if q > 0.5 else 0)))
    return xs[i]


def bootstrap(a, s, rng, n=NBOOT):
    """Library-clustered bootstrap, stratified by class: resample each class's libraries with replacement (keeping its
    size), n times. Returns the 2.5 and 97.5 percentiles of the pooled rate ratio announced/silent (inf where the
    silent resample has no move) and of the difference of library medians."""
    ratios, diffs = [], []
    for _ in range(n):
        ra = [a[rng.randrange(len(a))] for _ in a]
        rs = [s[rng.randrange(len(s))] for _ in s]
        pa = sum(m for m, _ in ra) / sum(d for _, d in ra)
        ps = sum(m for m, _ in rs) / sum(d for _, d in rs)
        ratios.append(pa / ps if ps else float('inf'))
        diffs.append(statistics.median(100 * m / d for m, d in ra) - statistics.median(100 * m / d for m, d in rs))
    return (pct(ratios, 0.025), pct(ratios, 0.975)), (pct(diffs, 0.025), pct(diffs, 0.975))


def fmt(x, nd=2):
    if x == float('inf'):
        return 'unbounded'
    return f'{x:.{nd}f}'


def compare(rows, key, window, base=None):
    """One comparison cell. rows: pair rows (event frames) with the clock applied; key: the grouping's column."""
    lt = lib_table(rows, window)
    lab = {r['library']: r[key] for r in rows}
    out = {}
    cls_libs = {c: [l for l in lt if lab[l] == c] for c in ('announced', 'silent')}
    for c in ('announced', 'silent'):
        rs = [r for r in rows if r[key] == c]
        n, at = A.hazard(rs, A.W[window][1], A.W[window][2])
        mv = [r for r in rs if r['outcome'] == 'moved']
        before = sum(ts(r['committer_time']) < ts(r['advisory_time']) for r in mv)
        out.update({f'{c}_libraries_with_pairs': len({r['library'] for r in rs}),
                    f'{c}_libraries_with_time': len(cls_libs[c]), f'{c}_pairs': len(rs),
                    f'{c}_moves': n, f'{c}_repo_days': round(at, 1), f'{c}_repo_days_raw': at, f'{c}_pooled': A.rate(n, at),
                    f'{c}_all_moves': len(mv), f'{c}_moves_before_clock': before})
        libs = cls_libs[c]
        if libs:
            out[f'{c}_median'] = round(statistics.median(100 * lt[l][0] / lt[l][1] for l in libs), 2)
            out[f'{c}_libraries_no_move'] = sum(lt[l][0] == 0 for l in libs)
        pooled, meds = [], []
        for l in libs:
            k, d = A.hazard([r for r in rs if r['library'] != l], A.W[window][1], A.W[window][2])
            pooled.append(100 * k / d if d else float('nan'))
            rest = [100 * lt[m][0] / lt[m][1] for m in libs if m != l]
            if rest:
                meds.append(statistics.median(rest))
        if pooled:
            out[f'{c}_pooled_leave_one_out'] = f'{min(pooled):.2f} to {max(pooled):.2f}'
        if meds:
            out[f'{c}_median_leave_one_out'] = f'{min(meds):.2f} to {max(meds):.2f}'
    raw = {c: (out[f'{c}_moves'], out[f'{c}_repo_days_raw']) for c in ('announced', 'silent')}
    if raw['announced'][1] and raw['silent'][1]:
        ps = raw['silent'][0] / raw['silent'][1]
        out['pooled_ratio'] = round(raw['announced'][0] / raw['announced'][1] / ps, 2) if ps else 'unbounded'
    for c in ('announced', 'silent'):
        del out[f'{c}_repo_days_raw']
    a = [lt[l] for l in cls_libs['announced']]
    s = [lt[l] for l in cls_libs['silent']]
    if len(a) >= 5 and len(s) >= 5:
        obs, p = A.perm_test([100 * m / d for m, d in a], [100 * m / d for m, d in s], random.Random(A.SEED))
        out.update(difference_of_medians=round(obs, 2), permutation_p=round(p, 4))
        (r_lo, r_hi), (d_lo, d_hi) = bootstrap(a, s, random.Random(BSEED))
        out.update(pooled_ratio_95=f'{fmt(r_lo)} to {fmt(r_hi)}', difference_of_medians_95=f'{fmt(d_lo)} to {fmt(d_hi)}')
    if base:
        for c in ('announced', 'silent'):
            out[f'{c}_libraries_lost'] = ' '.join(sorted(base['libs'][c] - {r['library'] for r in rows if r[key] == c}))
            for m in ('pairs', 'moves', 'repo_days'):
                out[f'{c}_{m}_lost'] = round(base[c][m] - out[f'{c}_{m}'], 1)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--out', default=os.environ.get('LH010_REANALYSIS_OUT') or OUT_DEFAULT,
                    help='output directory (default data/reanalysis/)')
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    def write(name, rows, fields=None):
        fields = fields or list(dict.fromkeys(k for r in rows for k in r))
        with open(os.path.join(args.out, name), 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n', extrasaction='ignore')
            w.writeheader()
            for r in rows:
                w.writerow(r)

    frames = read_csv('frame_defs.csv')
    osv = read_csv('osv_advisories.csv')
    clocks, recs = build_clocks(frames, osv)
    write('clocks.csv', clocks)
    write('advisories_naming_fix.csv', recs)

    def rd9(name):
        with open(os.path.join(LH009_DATA, name)) as f:
            return list(csv.DictReader(f))
    notes = build_notes(read_csv('fix_classes.csv'), read_csv('fix_texts.csv'), rd9('fix_texts.csv'),
                        read_csv('fix_reads.csv'), rd9('fix_reads.csv'), frames)
    write('notes_evidence.csv', notes)
    amb = []
    for n in notes:
        k = (n['library'], n['version'])
        if k in AMBIGUOUS:
            amb.append(dict(library=n['library'], version=n['version'], kind=n['kind'], cls=n['cls'], state=n['state'],
                            judgement=AMBIGUOUS[k]))
    write('notes_ambiguous.csv', amb)
    state = {(n['library'], n['version']): n['state'] for n in notes}

    rows = A.load()
    ev = [r for r in rows if r['kind'] == 'event']
    fix_of = {f['frame']: (f['library'], f['fixed_release']) for f in frames}
    cmap = {c: {x['frame']: (x['event_advisory_published'] if c == 'event_advisory' else x[c]) for x in clocks} for c in CLOCKS}
    sufficient = lambda r: state[fix_of[r['frame']]] in ('a', 'b')

    LR, CMP = [], []
    for clock in CLOCKS:
        crow = with_clock(ev, cmap[clock])
        for window in UNIT_WINDOWS:
            for lib, (n, at) in lib_table(crow, window).items():
                r0 = next(r for r in crow if r['library'] == lib)
                LR.append(dict(clock=clock, window=window, library=lib, cls=r0['cls'], strict_class=r0['strict_class'],
                               notes_state=state[fix_of[r0['frame']]], moves=n, repo_days_at_risk=round(at, 1),
                               per100=round(100 * n / at, 2)))
            for gname, key in A.GROUPINGS:
                base = None
                for cs in CASE_SETS:
                    rs = crow if cs == CASE_SETS[0] else [r for r in crow if sufficient(r)]
                    cell = compare(rs, key, window, base)
                    if base is None:
                        base = {'libs': {c: {r['library'] for r in rs if r[key] == c} for c in ('announced', 'silent')}}
                        for c in ('announced', 'silent'):
                            base[c] = {m: cell[f'{c}_{m}'] for m in ('pairs', 'moves', 'repo_days')}
                    CMP.append(dict(clock=clock, case_set=cs, grouping=gname, window=window, **cell))
    write('library_rates.csv', LR)
    write('comparisons.csv', CMP)

    for c in CMP:
        if c['grouping'] == 'class':
            print(c['clock'], '|', c['case_set'][:18], '|', c['window'][:26], '| libs', c['announced_libraries_with_time'],
                  c['silent_libraries_with_time'], '| med', c.get('announced_median'), c.get('silent_median'), 'p',
                  c.get('permutation_p'), '| pooled', c['announced_pooled'], f"({c['announced_moves']}/{c['announced_repo_days']})",
                  c['silent_pooled'], f"({c['silent_moves']}/{c['silent_repo_days']})", 'ratio', c.get('pooled_ratio'),
                  c.get('pooled_ratio_95'), '| before', c['announced_moves_before_clock'], c['announced_all_moves'],
                  c['silent_moves_before_clock'], c['silent_all_moves'])
    print({s: sum(n['state'] == s for n in notes if n['kind'] == 'event') for s in 'abc'}, 'events by notes state')


if __name__ == '__main__':
    main()
