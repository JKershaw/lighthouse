// Where an investigation stands, for its card on the front page and the top
// of its own page (notes/reader-experience-plan-2026-11-13.md): its current
// answer and that answer's status, what is running, the latest activity and
// the next read due. Built from the repository and the schedule; nothing here
// is written by hand, so a card is never staler than the table.
const long = new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'long', timeZone: 'UTC' });
const dayLabel = (iso) => (iso ? long.format(new Date(`${iso.slice(0, 10)}T00:00:00Z`)) : '');
const FINISHED = ['done', 'missed', 'cancelled'];
const WAITING = ['dependency_wait', 'blocked', 'keeper', 'recovery'];

export function investigationNow(inv, repo, schedule) {
  if (!inv) return null;
  const ids = new Set((inv.studies || []).map((s) => s.study).filter(Boolean));
  const studies = (repo.studies || []).filter((s) => ids.has(s.id));
  const rows = (schedule && schedule.rows) || [];
  const today = (schedule && schedule.today) || new Date().toISOString().slice(0, 10);
  const open = rows.filter((r) => ids.has(r.study) && r.readiness !== 'invalid' && !FINISHED.includes(r.state));
  const runningIds = new Set(open.filter((r) => r.state === 'running').map((r) => r.study));
  const pieces = (inv.pieces || []).filter((p) => !p.draft && !p.short).map((p) => repo.byPath[p.path]).filter(Boolean);
  const newestPiece = [...pieces].sort((a, b) => (b.pubTime || 0) - (a.pubTime || 0))[0] || null;

  // Where it stands: the current account if there is one (Reviewed); otherwise
  // no reviewed finding yet (Provisional). The newest released piece or essay is
  // shown beside it as reading, never as the investigation's answer.
  const current = inv.current ? repo.byPath[inv.current.path] : null;
  const answer = current
    ? { title: current.title, url: current.url, status: 'reviewed', kind: 'Current account' }
    : { title: 'No reviewed finding yet; working records only', url: '', status: 'provisional', kind: '' };
  const reading = !current && newestPiece ? { title: newestPiece.title, url: newestPiece.url, kind: newestPiece.essay ? 'Latest essay' : 'Latest piece' } : null;

  // Only completed observation work establishes a read. A checkpoint can be
  // analysis or maintenance, and an untyped historical row remains unknown.
  const reads = rows.filter((r) => ids.has(r.study) && r.kind === 'observe' && r.state === 'done' && /^\d{4}-\d{2}-\d{2}/.test(r.updated || ''))
    .map((r) => {
      const study = studies.find((s) => s.id === r.study);
      const checkpoint = study?.checkpoints?.find((c) => (r.ref || '').includes(c.path || c.key));
      return {
        iso: r.updated.slice(0, 10), id: r.id, study: r.study,
        title: repo.studyLabels?.[r.study] || study?.lead?.title || r.task,
        url: r.href || checkpoint?.url || study?.url || '',
      };
    }).sort((a, b) => b.iso.localeCompare(a.iso) || b.id.localeCompare(a.id));
  const latestRead = reads[0] || null;
  const next = open.filter((r) => r.kind === 'observe')
    .sort((a, b) => (a.earliest || '').localeCompare(b.earliest || '') || a.id.localeCompare(b.id))[0] || null;
  const nextWaits = next && WAITING.includes(next.state);
  const nextDay = next ? (next.earliest && next.earliest > today ? dayLabel(next.earliest) : 'today') : '';
  const waiting = open.filter((r) => WAITING.includes(r.state)).map((r) => ({
    id: r.id, study: r.study, task: r.task, href: r.href,
    reasons: r.reasons || [], unmet_dependencies: r.unmet_dependencies || [],
  }));

  return {
    answer,
    reading,
    running: runningIds.size,
    studies: studies.length,
    pieces: pieces.length,
    latestRead: latestRead ? { ...latestRead, day: dayLabel(latestRead.iso) } : null,
    next: next ? { id: next.id, day: nextWaits ? (nextDay === 'today' ? 'waiting' : `${nextDay} (waiting)`) : nextDay, study: repo.studyLabels?.[next.study] || '', reasons: next.reasons || [], waiting: nextWaits, reason: nextWaits ? (next.reasons || []).join('; ') : '' } : null,
    waiting,
    // Each study with whether it is running and its latest read, newest first.
    studyList: studies.map((s) => {
      const read = reads.find((r) => r.study === s.id);
      return {
        title: repo.studyLabels?.[s.id] || s.lead.title, url: s.url, id: s.id,
        running: runningIds.has(s.id),
        waiting: waiting.filter((r) => r.study === s.id),
        latest: read ? { day: dayLabel(read.iso), url: read.url, recent: Boolean(s.checkpoints?.find((c) => c.key.slice(0, 10) === read.iso)?.recent) } : null,
        key: read?.iso || '',
      };
    }).sort((a, b) => Number(b.running) - Number(a.running) || b.key.localeCompare(a.key) || b.id.localeCompare(a.id, 'en', { numeric: true })),
  };
}
