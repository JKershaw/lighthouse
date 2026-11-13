// The reader's content model (notes/reader-experience-plan-2026-11-13.md):
// every released piece and essay carries a topic label, a one-line summary,
// a status, a home (its investigation, else a section front) and what to read
// next. Templates only display these; site/test/model.test.js checks every
// released piece has them, so a later run fills a field rather than inventing
// layout. Labels and summaries are editorial signposts kept in site/sections.md
// ("labels:" and "summaries:", each "path | text"), never a piece's own prose.

// The three statuses a reader meets, one badge each, the same everywhere.
export const STATUS = {
  reviewed: { label: 'Reviewed', title: 'Checked against its sources by fresh agents before release' },
  provisional: { label: 'Provisional', title: 'A working record: not yet reviewed, and may change' },
  live: { label: 'Live', title: 'Unreviewed, read today or recently, and dated' },
};

// A released piece or essay is reviewed (AGENTS.md: nothing is released
// without its reviews); a draft, record or checkpoint is provisional.
export function statusOf(p) {
  if (!p) return 'provisional';
  if ((p.section === 'articles' || p.essay) && !p.draft && (!p.status || p.status === 'released')) return 'reviewed';
  return 'provisional';
}

const homeFronts = { articles: { title: 'Findings', url: '/articles/' }, essays: { title: 'Essays', url: '/essays/' } };

// Apply the model to the released pieces and essays. `labels` and `summaries`
// are Maps from path to text; `essays` is newest first.
export function applyModel({ pieces = [], essays = [], investigations = [], labels = new Map(), summaries = new Map(), twinOf = new Map(), warnings = null }) {
  const released = (p) => p && !p.draft && (!p.status || p.status === 'released');
  const all = [...pieces, ...essays].filter(released);
  for (const p of all) {
    const full = p.short ? twinOf.get(p.path) : p;
    const key = full ? full.path : p.path;
    const ctx = { ...(p.context || {}) };
    // An essay has no piece context; an investigation that lists it is its home,
    // and the next item in that investigation's order follows it.
    if (!ctx.investigation) {
      const inv = investigations.find((i) => (i.pieces || []).some((x) => x.path === key));
      if (inv) {
        const order = inv.pieces.filter((x) => !x.draft);
        const at = order.findIndex((x) => x.path === key);
        ctx.investigation = { title: inv.title, url: inv.url };
        if (at >= 0 && order[at + 1]) ctx.next = order[at + 1];
      }
    }
    const home = ctx.investigation || ctx.section || (p.essay ? homeFronts.essays : homeFronts.articles);
    let next = ctx.next || null;
    if (!next && p.essay && !ctx.investigation) {
      const list = essays.filter(released);
      const at = list.findIndex((e) => e.path === p.path);
      const older = at >= 0 ? list[at + 1] : null;
      if (older) next = { title: older.title, url: older.url };
    }
    if (warnings && !p.short && !labels.get(key) && !labels.get(p.path)) warnings.push(`${key}: no topic label in site/sections.md (labels:); showing "${home.title}"`);
    p.reader = {
      // Without a label in site/sections.md, the piece's home names it, and the
      // build warns, so a new piece never shows a blank label or blocks a deploy.
      label: labels.get(key) || labels.get(p.path) || home.title.replace(/\?$/, ''),
      summary: summaries.get(key) || summaries.get(p.path) || p.summary || '',
      status: statusOf(p),
      home: { title: home.title, url: home.url, investigation: Boolean(ctx.investigation) },
      // When nothing follows in order, the next step is the piece's home.
      next: next ? { title: next.title, url: next.url, kind: 'piece' } : { title: home.title, url: home.url, kind: 'home' },
    };
  }
  return all;
}
