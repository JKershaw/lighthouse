// Where an investigation stands, for its card on the front page and the top
// of its own page (notes/reader-experience-plan-2026-11-13.md): its current
// answer and that answer's status, what is running, the latest activity and
// the next read due. Built from the repository and the schedule; nothing here
// is written by hand, so a card is never staler than the table.
const long = new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'long', timeZone: 'UTC' });
const dayLabel = (iso) => (iso ? long.format(new Date(`${iso.slice(0, 10)}T00:00:00Z`)) : '');
const RUNNING = ['due', 'upcoming', 'running', 'overdue'];

export function investigationNow(inv, repo, schedule) {
  if (!inv) return null;
  const ids = new Set((inv.studies || []).map((s) => s.study).filter(Boolean));
  const studies = (repo.studies || []).filter((s) => ids.has(s.id));
  const rows = (schedule && schedule.rows) || [];
  const today = (schedule && schedule.today) || new Date().toISOString().slice(0, 10);
  const open = rows.filter((r) => ids.has(r.study) && RUNNING.includes(r.state));
  const runningIds = new Set(open.map((r) => r.study));
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

  // The latest activity: the newest checkpoint among its studies, or its newest piece.
  const reads = studies.filter((s) => s.checkpoints[0]).map((s) => ({ iso: s.checkpoints[0].key.slice(0, 10), title: repo.studyLabels?.[s.id] || s.lead.title, url: s.url }));
  // A finished row in the schedule is a read too, whether or not it wrote a checkpoint page.
  for (const r of rows) if (ids.has(r.study) && r.state === 'done' && /^\d{4}-\d{2}-\d{2}/.test(r.updated || '')) {
    const s = studies.find((x) => x.id === r.study);
    if (s) reads.push({ iso: r.updated.slice(0, 10), title: repo.studyLabels?.[s.id] || s.lead.title, url: s.url });
  }
  const latestRead = reads.sort((a, b) => b.iso.localeCompare(a.iso))[0] || null;
  const next = open.filter((r) => r.earliest >= today || r.state === 'due' || r.state === 'overdue')
    .sort((a, b) => (a.earliest || '').localeCompare(b.earliest || ''))[0] || null;

  return {
    answer,
    reading,
    running: runningIds.size,
    studies: studies.length,
    pieces: pieces.length,
    latestRead: latestRead ? { ...latestRead, day: dayLabel(latestRead.iso) } : null,
    next: next ? { day: next.earliest <= today ? 'today' : dayLabel(next.earliest), study: repo.studyLabels?.[next.study] || '' } : null,
    // Each study with whether it is running and its latest read, newest first.
    studyList: studies.map((s) => ({
      title: repo.studyLabels?.[s.id] || s.lead.title, url: s.url, id: s.id,
      running: runningIds.has(s.id),
      latest: s.checkpoints[0] ? { day: dayLabel(s.checkpoints[0].key), url: s.checkpoints[0].url, recent: s.checkpoints[0].recent } : null,
      key: s.checkpoints[0] ? s.checkpoints[0].key : '',
    })).sort((a, b) => Number(b.running) - Number(a.running) || b.key.localeCompare(a.key) || b.id.localeCompare(a.id, 'en', { numeric: true })),
  };
}
