import path from "node:path";

// The Atom feed: released pieces, short forms and essays, newest first by
// publication date. Drafts, records and notes are left out.

const KINDS = {
  piece: "Piece",
  "short-form": "Short form",
  essay: "Essay",
  correction: "Correction",
  "later-evidence": "Later evidence",
  "unreviewed-log": "Unreviewed daily log",
};

export function escapeXml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

// RFC 3339, in UTC: 2026-09-26T00:00:00Z.
export const rfc3339 = (time) => new Date(time).toISOString().replace(/\.\d{3}Z$/, "Z");

const kindOf = (p) => (p.essay ? "essay" : p.short ? "short-form" : "piece");

// The entries, newest first: on the same day, the one added last.
export function feedEntries(repo) {
  return [...repo.pieces, ...repo.releasedEssays]
    .filter((p) => !p.draft)
    .sort((a, b) => b.pubTime - a.pubTime || b.added - a.added || a.path.localeCompare(b.path))
    .map((p) => ({
      title: p.title,
      summary: p.summary,
      url: (repo.siteUrl || "") + p.url,
      published: rfc3339(p.pubTime),
      // The latest revision or dated notice, else the publication.
      updated: rfc3339(Math.max(p.pubTime, p.revisedTime || 0)),
      kind: kindOf(p),
      status: p.displayState || "Released",
      nextRevision: p.nextRevision || "",
    }));
}

export function atomFeed(repo, { title = "Lighthouse", entries = feedEntries(repo), feedPath = "/feed.xml", homePath = "/" } = {}) {
  const base = repo.siteUrl || "";
  const updated = entries.length ? entries.map((e) => e.updated).sort().pop() : rfc3339(Date.now());
  const lines = [
    '<?xml version="1.0" encoding="utf-8"?>',
    '<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en-GB">',
    `  <title>${escapeXml(title)}</title>`,
    repo.strap ? `  <subtitle>${escapeXml(repo.strap)}</subtitle>` : "",
    `  <id>${escapeXml(base + (feedPath === "/feed.xml" ? "/" : feedPath))}</id>`,
    `  <link rel="alternate" type="text/html" href="${escapeXml(base + homePath)}"/>`,
    `  <link rel="self" type="application/atom+xml" href="${escapeXml(base + feedPath)}"/>`,
    `  <updated>${updated}</updated>`,
    "  <author><name>Lighthouse</name></author>",
  ];
  for (const e of entries) {
    lines.push(
      "  <entry>",
      `    <title>${escapeXml(e.title)}</title>`,
      `    <id>${escapeXml(e.id || e.url)}</id>`,
      `    <link rel="alternate" type="text/html" href="${escapeXml(e.url)}"/>`,
      `    <published>${e.published}</published>`,
      `    <updated>${e.updated}</updated>`,
      `    <category term="${e.kind}" label="${KINDS[e.kind]}"/>`,
      e.status ? `    <category scheme="https://lighthouse.harbour.cat/publication-state" term="${escapeXml(e.status.toLowerCase())}" label="${escapeXml(e.status)}"/>` : "",
      e.summary ? `    <summary>${escapeXml(e.summary + (e.nextRevision ? " Next revision: " + e.nextRevision : ""))}</summary>` : "",
      "  </entry>",
    );
  }
  lines.push("</feed>");
  return lines.filter(Boolean).join("\n") + "\n";
}

function citesInvestigation(body, from, investigation) {
  for (const match of String(body || '').matchAll(/\]\(([^)\s]+)\)/g)) {
    const target = match[1].replace(/[#?].*$/, '');
    const relative = path.posix.normalize(target.startsWith('/') ? target.slice(1) : path.posix.join(path.posix.dirname(from), target));
    if (relative === investigation.path || relative === investigation.url.replace(/^\//, '').replace(/\/$/, '')) return true;
  }
  return false;
}
const plain = (markdown) => String(markdown || '').replace(/!\[([^\]]*)\]\([^)]*\)/g, '$1').replace(/\[([^\]]*)\]\([^)]*\)/g, '$1').replace(/[*_`>#]/g, '').replace(/\s+/g, ' ').trim();
export function feedCatalog(repo) {
  const base = repo.siteUrl || '', all = feedEntries(repo);
  const notices = repo.pieces.filter(p => !p.draft).flatMap(p => (p.notices || []).map(n => ({
    title: `${n.label}: ${p.title}`, summary: plain(n.markdown), url: base + p.url + '#' + n.id,
    published: rfc3339(n.time), updated: rfc3339(n.time), kind: n.kind,
  }))).sort((a,b) => b.published.localeCompare(a.published) || a.url.localeCompare(b.url));
  const feeds = [
    { id:'all', title:'Lighthouse: pieces and essays', feedPath:'/feed.xml', homePath:'/', entries:all },
    { id:'findings', title:'Lighthouse: findings', feedPath:'/feeds/findings.xml', homePath:'/articles/', entries:all.filter(e => e.kind !== 'essay') },
    { id:'essays', title:'Lighthouse: essays and interpretation', feedPath:'/feeds/essays.xml', homePath:'/essays/', entries:all.filter(e => e.kind === 'essay') },
    { id:'watch', title:'Lighthouse: reviewed watch notices', feedPath:'/feeds/watch.xml', homePath:'/watch/', entries:notices },
  ];
  for (const inv of repo.investigations) {
    const members = new Set(inv.pieces.map(p => p.path));
    const selected = [...repo.pieces, ...repo.releasedEssays].filter(p => !p.draft && (members.has(p.path) || p.investigationId === inv.id || p.context?.investigation?.url === inv.url || (p.essay && citesInvestigation(repo.sourceBodies?.[p.path],p.path,inv))));
    feeds.push({ id:`investigation-${inv.id}`, title:`Lighthouse: ${inv.title}`, feedPath:`/feeds/investigations/${inv.id}.xml`, homePath:inv.url,
      entries:feedEntries({...repo,pieces:selected.filter(p => !p.essay),releasedEssays:selected.filter(p => p.essay)}) });
  }
  for (const story of repo.stories || []) feeds.push({
    id:`story-${story.path}`,title:`Lighthouse: ${story.title} (reviewed notices and unreviewed daily logs)`,feedPath:story.url+'feed.xml',homePath:story.url,
    entries:story.entries.map(entry => ({ title:entry.title,summary:(entry.reviewed?'Reviewed notice. ':'Unreviewed working log, not a finding. ')+plain(entry.markdown),url:base+entry.url,
      published:rfc3339(entry.time),updated:rfc3339(entry.time),kind:entry.kind })),
  });
  return feeds;
}
export function relevantFeeds(repo, doc, section = '') {
  const ids = new Set(['all']);
  const name = doc?.section || section;
  if (name === 'articles') ids.add('findings');
  if (name === 'essays') ids.add('essays');
  if (name === 'watch') ids.add('watch');
  const investigation = doc?.investigationId || doc?.investigation?.id || doc?.storyData?.investigationId;
  if (investigation) ids.add(`investigation-${investigation}`);
  if (doc?.storyData) ids.add(`story-${doc.path}`);
  return (repo.feeds || []).filter(feed => ids.has(feed.id));
}
