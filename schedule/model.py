"""Offline, standard-library readiness model for Lighthouse's committed queue.

Calendar eligibility is independent of evidence readiness. Nothing in this module
claims work, reads external sources, or interprets a scientific review verdict.
"""
from __future__ import annotations

import csv
from datetime import date, datetime, timedelta, timezone
from io import StringIO
from pathlib import Path
import re
from urllib.parse import urlsplit

SCHEMA_VERSION = 1
FIELDS = ['id', 'study', 'task', 'earliest', 'latest', 'status', 'updated',
          'by', 'ref', 'note', 'kind', 'depends_on', 'run_id']
STATUSES = {'open', 'running', 'done', 'missed', 'blocked', 'keeper', 'cancelled'}
KINDS = {'plan', 'observe', 'analyse', 'review', 'publish', 'maintain'}
TERMINAL = {'done', 'missed', 'cancelled'}
SCOPE_HOLD = 'Work deferred pending a scope review.'
STALE = timedelta(hours=6)
UTC = timezone.utc


CLOCK_TOLERANCE = timedelta(minutes=5)


def canonical_date(value: str) -> date:
    """Accept exactly the public YYYY-MM-DD representation."""
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise ValueError('expected YYYY-MM-DD')
    return date.fromisoformat(value)


def aware_instant(value: str) -> datetime:
    """Read an ISO timestamp with an explicit offset and normalise to UTC."""
    if not re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}', value):
        raise ValueError('expected a timezone-aware ISO timestamp')
    result = datetime.fromisoformat(value[:-1] + '+00:00' if value.endswith('Z') else value)
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError('timestamp requires a timezone offset')
    return result.astimezone(UTC)


def iso_utc(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace('+00:00', 'Z')


def _check_quotes(text: str) -> None:
    """Reject bare quotes as well as the malformed quoted fields csv rejects."""
    state = 'start'
    for char in text:
        if state == 'quoted':
            if char == '"':
                state = 'closed'
        elif state == 'closed':
            if char == '"':
                state = 'quoted'
            elif char == ',':
                state = 'start'
            elif char in '\r\n':
                state = 'start'
            else:
                raise ValueError('unexpected character after closing CSV quote')
        elif char in ',\r\n':
            state = 'start'
        elif char == '"':
            if state != 'start':
                raise ValueError('quote inside an unquoted CSV field')
            state = 'quoted'
        else:
            state = 'unquoted'
    if state == 'quoted':
        raise ValueError('unterminated quoted CSV field')


def _read_rows(root: Path, diagnostics: list[str]) -> list[dict]:
    table = root / 'schedule' / 'due.csv'
    try:
        content = table.read_text(encoding='utf-8')
        _check_quotes(content)
        reader = csv.reader(StringIO(content, newline=''), strict=True)
        header = next(reader, None)
        if header != FIELDS:
            diagnostics.append(f'schedule/due.csv: columns are {header!r}, expected {FIELDS!r}')
            return []
        result = []
        for values in reader:
            line = reader.line_num
            if len(values) != len(FIELDS):
                diagnostics.append(f'line {line}: {len(values)} cells, expected {len(FIELDS)}')
                continue
            row = dict(zip(FIELDS, values))
            row['_line'] = line
            result.append(row)
        return result
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        diagnostics.append(f'schedule/due.csv: cannot read valid CSV: {exc}')
        return []


def _validate_run_registry(root: Path, diagnostics: list[str]) -> None:
    """Validate public identity uniqueness without requiring an in-flight log."""
    registry = root / 'schedule' / 'runs.csv'
    try:
        if not registry.exists():
            return
        content = registry.read_text(encoding='utf-8')
        _check_quotes(content)
        reader = csv.reader(StringIO(content, newline=''), strict=True)
        header = next(reader, None)
        base = ['started', 'by', 'did', 'commit']
        accepted = [base + ['run_id'], base + ['plain', 'run_id'], base + ['run_id', 'plain']]
        if header not in accepted:
            diagnostics.append('schedule/runs.csv: expected started,by,did,commit,run_id with optional plain immediately before or after run_id')
            return
        seen = set()
        for values in reader:
            if len(values) != len(header):
                diagnostics.append(f'schedule/runs.csv line {reader.line_num}: {len(values)} cells, expected {len(header)}')
                continue
            identity = values[header.index('run_id')].strip()
            if identity:
                if identity in seen:
                    diagnostics.append(f'schedule/runs.csv line {reader.line_num}: duplicate run_id {identity!r}')
                seen.add(identity)
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        diagnostics.append(f'schedule/runs.csv: cannot read valid CSV: {exc}')


def _reference_errors(root: Path, row: dict) -> list[str]:
    """Check local existence only, retaining historical annotation and commits.

    Existing terminal references sometimes append versions or narrative after a
    file, or contain a bare commit hash. Those are historical metadata, not new
    evidence gates. Local file tokens still receive containment checks.
    """
    errors = []
    for part in row['ref'].split(';'):
        part = part.strip()
        if not part:
            continue
        try:
            scheme = urlsplit(part).scheme
        except ValueError:
            errors.append(f'ref {part!r} is malformed')
            continue
        if scheme in {'http', 'https'}:
            continue
        if scheme:
            errors.append(f'ref {part!r} has unsupported URL scheme {scheme!r}')
            continue
        token = part.split()[0].rstrip(',')
        if re.fullmatch(r'[0-9a-fA-F]{7,40}', token):
            continue
        if row['status'] in TERMINAL and not row['kind'] and not ('/' in token or re.search(r'\.[A-Za-z0-9]+(?:#.*)?$', token)):
            continue
        local = token.split('#', 1)[0]
        if not local:
            continue
        try:
            target = (root / local).resolve()
            target.relative_to(root)
        except (ValueError, OSError, RuntimeError):
            errors.append(f'ref {token!r} is outside the repository root')
            continue
        if not target.exists():
            # Old terminal notes retain a unique review-number shorthand.
            # Do not expand or rewrite that historical source field.
            if row['status'] in TERMINAL and not row['kind'] and re.fullmatch(r'notes/R-\d{4}', local):
                matches = [path for path in target.parent.glob(target.name + '-*.md') if path.is_file()]
                if len(matches) == 1:
                    try:
                        matches[0].resolve().relative_to(root)
                    except (ValueError, OSError, RuntimeError):
                        errors.append(f'ref {token!r} is outside the repository root')
                    continue
                if len(matches) > 1:
                    errors.append(f'historical ref {token!r} is ambiguous locally')
                    continue
            errors.append(f'ref {token!r} does not exist locally')
    return errors


def _validate(root: Path, rows: list[dict], diagnostics: list[str]) -> dict[str, dict]:
    by_id = {}
    for row in rows:
        where = f'line {row["_line"]} ({row["id"] or "no id"})'
        row['_where'] = where
        if not row['id']:
            diagnostics.append(f'{where}: no id')
        elif any(char.isspace() for char in row['id']):
            diagnostics.append(f'{where}: id must contain no whitespace')
        elif row['id'] in by_id:
            diagnostics.append(f'{where}: duplicate id {row["id"]!r}')
        else:
            by_id[row['id']] = row
        if row['status'] not in STATUSES:
            diagnostics.append(f'{where}: unknown status {row["status"]!r}')
        if row['kind'] not in KINDS and (row['kind'] or row['status'] not in TERMINAL):
            diagnostics.append(f'{where}: kind must be one of {", ".join(sorted(KINDS))}')
        for field in ('earliest', 'latest'):
            row['_' + field] = None
            if row[field]:
                try:
                    row['_' + field] = canonical_date(row[field])
                except ValueError:
                    diagnostics.append(f'{where}: {field} {row[field]!r} is not a canonical YYYY-MM-DD date')
        if row['_earliest'] and row['_latest'] and row['_latest'] < row['_earliest']:
            diagnostics.append(f'{where}: latest before earliest')
        row['_claimed_at'] = None
        if row['status'] == 'running':
            if not row['run_id'].strip():
                diagnostics.append(f'{where}: running claim requires a public run_id')
            if not row['by'].strip():
                diagnostics.append(f'{where}: running claim requires by attribution')
            try:
                row['_claimed_at'] = aware_instant(row['updated'])
            except ValueError:
                diagnostics.append(f'{where}: running updated must be a timezone-aware ISO timestamp')
        if row['status'] == 'done' and not any(part.strip() for part in row['ref'].split(';')):
            diagnostics.append(f'{where}: done with no ref (a retained local file, directory, URL or commit)')
        diagnostics.extend(f'{where}: {problem}' for problem in _reference_errors(root, row))
        raw_dependencies = row['depends_on'].split(';') if row['depends_on'] else []
        row['_dependencies'] = [value.strip() for value in raw_dependencies if value.strip()]
        if raw_dependencies and any(not value.strip() for value in raw_dependencies):
            diagnostics.append(f'{where}: empty dependency ID')
        if len(set(row['_dependencies'])) != len(row['_dependencies']):
            diagnostics.append(f'{where}: duplicate dependency ID')
    for row in rows:
        for dependency in row['_dependencies']:
            if dependency == row['id']:
                diagnostics.append(f'{row["_where"]}: self-dependency')
            elif dependency not in by_id:
                diagnostics.append(f'{row["_where"]}: missing dependency {dependency!r}')
    # Kahn's algorithm avoids recursion limits on a long valid work pipeline.
    indegree = {identity: 0 for identity in by_id}
    children = {identity: [] for identity in by_id}
    for identity, row in by_id.items():
        for dependency in set(row['_dependencies']):
            if dependency in by_id:
                indegree[identity] += 1
                children[dependency].append(identity)
    frontier = [identity for identity, count in indegree.items() if count == 0]
    index = 0
    while index < len(frontier):
        identity = frontier[index]
        index += 1
        for child in children[identity]:
            indegree[child] -= 1
            if indegree[child] == 0:
                frontier.append(child)
    if len(frontier) != len(by_id):
        cycle = ', '.join(sorted(identity for identity, count in indegree.items() if count))
        diagnostics.append(f'dependency cycle (including downstream rows): {cycle}')
    return by_id


def _coverage(root: Path, rows: list[dict], by_id: dict[str, dict], today: date | None = None) -> tuple[list[dict], list[str], list[str]]:
    coverage, gaps, warnings = [], [], []
    active_studies = {row['study'] for row in rows if row['status'] not in TERMINAL}
    for brief in sorted(root.glob('studies/LH*/brief.md')):
        study = brief.parent.name
        record = brief.parent / f'{study}.md'
        try:
            interim = record.exists() and bool(re.search(r'^version:.*interim', record.read_text(encoding='utf-8'), re.M | re.I))
        except (OSError, UnicodeError):
            interim = True
        if study not in active_studies and (not record.exists() or interim):
            identity = f'continuation:{study}'
            coverage.append({'id': identity, 'study': study,
                             'message': f'{study}: a brief with no record or an interim record, and no unfinished continuation; audit whether a promised stage is missing'})
            gaps.append(identity)
            warnings.append(identity)
    for row in rows:
        if row['kind'] != 'publish' or row['status'] in TERMINAL:
            continue
        if not any(by_id.get(dep, {}).get('kind') == 'review' for dep in row['_dependencies']):
            identity = f'review-predecessor:{row["id"]}'
            coverage.append({'id': identity, 'study': row['study'], 'row_id': row['id'],
                             'message': f'{row["id"]}: publication has no declared review predecessor; audit the release checks'})
            warnings.append(identity)
    if today is not None:
        _flow(rows, by_id, today, coverage, warnings)
    return coverage, gaps, warnings


# Flow warnings (the keeper, 26 November 2026). On that day 25 studies held 73 reads collected
# since their last write-up, while records waited on not-before dates no brief had set, on
# blocked stop gates nobody re-tested and on closures weeks away. These advisories name each
# kind of avoidable wait so the next run clears it; none of them changes readiness.
WRITE_UP_KINDS = {'analyse', 'review', 'publish'}
HELD_READS = 2
HELD_HORIZON = timedelta(days=14)
NO_INTERIM_REASON = re.compile(r'no-interim:', re.I)
NOT_BEFORE_REASON = re.compile(r'not-before:', re.I)


def _effective_start(identity: str, by_id: dict[str, dict], today: date, memo: dict) -> date | None:
    """Earliest day a row could start under the queue as written; None means no date at all."""
    if identity in memo:
        return memo[identity]
    memo[identity] = None  # cycles are diagnosed elsewhere
    row = by_id.get(identity)
    if row is None or row['status'] in {'missed', 'cancelled'}:
        return None
    if row['status'] == 'done':
        memo[identity] = today
        return today
    if row['status'] in {'blocked', 'keeper'}:
        start = row['_latest']
        if start is None:
            return None
    else:
        start = row['_earliest'] or today
    start = max(start, today)
    for dependency in row['_dependencies']:
        upstream = _effective_start(dependency, by_id, today, memo)
        if upstream is None:
            return None
        start = max(start, upstream)
    memo[identity] = start
    return start


def _flow(rows: list[dict], by_id: dict[str, dict], today: date, coverage: list[dict], warnings: list[str]) -> None:
    for row in rows:
        if row['status'] == 'open' and row['kind'] in WRITE_UP_KINDS and row['_earliest'] and row['_earliest'] > today \
                and all(by_id.get(dep, {}).get('status') == 'done' for dep in row['_dependencies']) \
                and not NOT_BEFORE_REASON.search(row['note']):
            identity = f'date-only-wait:{row["id"]}'
            coverage.append({'id': identity, 'study': row['study'], 'row_id': row['id'],
                             'message': f'{row["id"]}: everything it depends on is done, but it waits for {row["_earliest"].isoformat()}; clear the date unless the brief sets it, and then say why in the note ("not-before: ...")'})
            warnings.append(identity)
        if row['status'] == 'blocked' and row['note'] != SCOPE_HOLD and row['_latest'] is None:
            identity = f'gate-without-deadline:{row["id"]}'
            coverage.append({'id': identity, 'study': row['study'], 'row_id': row['id'],
                             'message': f'{row["id"]}: blocked with no deadline, so nothing after it can ever be scheduled; give it the date by which a run must re-test its condition'})
            warnings.append(identity)
    memo: dict = {}
    studies: dict[str, list[dict]] = {}
    for row in rows:
        if re.fullmatch(r'LH[0-9]+', row['study']):
            studies.setdefault(row['study'], []).append(row)
    for study, members in sorted(studies.items()):
        writes = [r for r in members if r['kind'] in WRITE_UP_KINDS and r['status'] != 'done' and r['status'] not in TERMINAL]
        analyses = [r for r in writes if r['kind'] == 'analyse']
        if not analyses or any(NO_INTERIM_REASON.search(r['note']) for r in analyses):
            continue
        last = max((day for r in members if r['status'] == 'done' and r['kind'] in WRITE_UP_KINDS
                    and (day := _day(r['updated'])) is not None), default=None)
        held = [r for r in members if r['status'] == 'done' and r['kind'] == 'observe'
                and (day := _day(r['updated'])) is not None and (last is None or day > last)]
        if len(held) < HELD_READS:
            continue
        starts = [_effective_start(r['id'], by_id, today, memo) for r in analyses]
        known = [s for s in starts if s is not None]
        soonest = min(known) if known else None
        if soonest is not None and soonest <= today + HELD_HORIZON:
            continue
        identity = f'held-reads:{study}'
        when = soonest.isoformat() if soonest else 'no date'
        coverage.append({'id': identity, 'study': study,
                         'message': f'{study}: {len(held)} reads done since its last write-up and no write-up allowed before {when}; add an interim checkpoint if the new evidence could change the answer, or say why not in the next analysis row\'s note ("no-interim: ...")'})
        warnings.append(identity)


def _day(value: str) -> date | None:
    try:
        return date.fromisoformat((value or '')[:10])
    except ValueError:
        return None


def evaluate(root: Path | str, now: datetime) -> dict:
    """Load, validate and classify one queue against a single explicit instant."""
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError('evaluation time requires a timezone offset')
    now = now.astimezone(UTC)
    today = now.date()
    try:
        root = Path(root).resolve()
    except (OSError, RuntimeError, ValueError) as exc:
        groups = {key: [] for key in ('ready', 'overdue', 'upcoming', 'stale', 'gaps', 'warnings')}
        return dict(schema_version=SCHEMA_VERSION, evaluated_at=iso_utc(now), today=today.isoformat(),
                    valid=False, diagnostics=[f'repository root cannot be resolved: {exc}'],
                    rows=[], groups=groups, coverage=[], **groups)
    diagnostics: list[str] = []
    rows = _read_rows(root, diagnostics)
    _validate_run_registry(root, diagnostics)
    by_id = _validate(root, rows, diagnostics)
    valid = not diagnostics
    groups = {key: [] for key in ('ready', 'overdue', 'upcoming', 'stale', 'gaps', 'warnings')}
    held_studies = {
        row['study'] for row in rows
        if row['status'] == 'blocked' and row['note'] == SCOPE_HOLD
        and re.fullmatch(r'LH[0-9]+', row['study'])
    }
    public_rows = []
    for row in rows:
        earliest, latest = row['_earliest'], row['_latest']
        if latest and latest < today:
            calendar = 'overdue'
        elif not earliest or earliest <= today:
            calendar = 'due'
        elif earliest <= today + timedelta(days=7):
            calendar = 'upcoming'
        else:
            calendar = 'future'
        unmet = [dep for dep in row['_dependencies'] if by_id.get(dep, {}).get('status') != 'done']
        reasons = [f'Waiting for {dep} to be done (currently {by_id.get(dep, {}).get("status", "missing")})' for dep in unmet]
        stale = row['status'] == 'running' and (row['_claimed_at'] is None or now - row['_claimed_at'] > STALE)
        status = row['status']
        if status in TERMINAL:
            state = status
            reasons = [f'Historical outcome: {status}']
        elif status in {'blocked', 'keeper'}:
            state = status
            reasons.insert(0, row['note'] or ('Waiting for the keeper' if status == 'keeper' else 'Manually blocked'))
        elif status == 'running':
            state = 'recovery' if stale else 'running'
            if row['study'] in held_studies:
                reasons.append(SCOPE_HOLD)
            reasons.insert(0, 'Claim needs reconciliation before reopening; elapsed time does not authorise duplicate work' if stale else 'Owned by a running claim')
        elif status != 'open':
            state = 'invalid'
        elif row['study'] in held_studies:
            state = 'blocked'
            reasons.insert(0, SCOPE_HOLD)
        elif unmet:
            state = 'dependency_wait'
        elif earliest and earliest > today:
            state = 'calendar_wait'
        else:
            state = 'ready'
        if earliest and earliest > today and status not in TERMINAL:
            reasons.append(f'Not before {earliest.isoformat()} UTC')
        if calendar == 'overdue' and status not in TERMINAL:
            reasons.append('Deadline elapsed; the brief decides whether late work is admissible')
        actionable = valid and state == 'ready'
        if not valid:
            reasons.append('Queue validation failed; no work is actionable')
        item = {field: row[field] for field in FIELDS}
        item.update(state=state, readiness=state if valid else 'invalid', actionable=actionable,
                    reasons=reasons, unmet_dependencies=unmet, calendar_state=calendar, stale=stale)
        public_rows.append(item)
        if actionable:
            groups['overdue' if calendar == 'overdue' else 'ready'].append(row['id'])
        if status == 'open' and calendar == 'upcoming' and row['study'] not in held_studies:
            groups['upcoming'].append(row['id'])
        if stale:
            groups['stale'].append(row['id'])
    try:
        coverage, groups['gaps'], groups['warnings'] = _coverage(root, rows, by_id, today)
    except (OSError, RuntimeError, ValueError) as exc:
        identity = 'coverage:unavailable'
        coverage = [{'id': identity, 'message': f'Pipeline coverage audit could not read local metadata: {exc}'}]
        groups['warnings'] = [identity]
    # A time written by hand can run ahead of the clock (the run of 17 November 2026 wrote
    # several up to forty minutes early); flag any updated instant after the evaluation time.
    for row in rows:
        try:
            written = aware_instant(row['updated'])
        except (ValueError, TypeError):
            continue
        if written - now > CLOCK_TOLERANCE:
            identity = f'clock:{row["id"]}'
            coverage.append({'id': identity, 'message': f'{row["_where"]}: updated {row["updated"]} is later than the evaluation time {iso_utc(now)}; take times from the clock'})
            groups['warnings'].append(identity)
    order = {row['id']: (row['latest'] or '9999-12-31', row['earliest'] or '', index)
             for index, row in enumerate(rows)}
    for key in ('ready', 'overdue', 'upcoming', 'stale'):
        groups[key].sort(key=lambda identity: order[identity])
    return dict(schema_version=SCHEMA_VERSION, evaluated_at=iso_utc(now), today=today.isoformat(),
                valid=valid, diagnostics=diagnostics, rows=public_rows, groups=groups,
                coverage=coverage, **groups)


# Descriptive alias for callers that prefer to name the load as well as evaluation.
load_queue = evaluate
