// The Atom feed: released pieces, short forms and essays, newest first by
// publication date. Drafts, records and notes are left out.

const KINDS = {
  piece: "Piece",
  "short-form": "Short form",
  essay: "Essay",
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
    }));
}

export function atomFeed(repo, { title = "Lighthouse" } = {}) {
  const base = repo.siteUrl || "";
  const entries = feedEntries(repo);
  const updated = entries.length ? entries.map((e) => e.updated).sort().pop() : rfc3339(Date.now());
  const lines = [
    '<?xml version="1.0" encoding="utf-8"?>',
    '<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en-GB">',
    `  <title>${escapeXml(title)}</title>`,
    repo.strap ? `  <subtitle>${escapeXml(repo.strap)}</subtitle>` : "",
    `  <id>${escapeXml(base + "/")}</id>`,
    `  <link rel="alternate" type="text/html" href="${escapeXml(base + "/")}"/>`,
    `  <link rel="self" type="application/atom+xml" href="${escapeXml(base + "/feed.xml")}"/>`,
    `  <updated>${updated}</updated>`,
    "  <author><name>Lighthouse</name></author>",
  ];
  for (const e of entries) {
    lines.push(
      "  <entry>",
      `    <title>${escapeXml(e.title)}</title>`,
      `    <id>${escapeXml(e.url)}</id>`,
      `    <link rel="alternate" type="text/html" href="${escapeXml(e.url)}"/>`,
      `    <published>${e.published}</published>`,
      `    <updated>${e.updated}</updated>`,
      `    <category term="${e.kind}" label="${KINDS[e.kind]}"/>`,
      e.summary ? `    <summary>${escapeXml(e.summary)}</summary>` : "",
      "  </entry>",
    );
  }
  lines.push("</feed>");
  return lines.filter(Boolean).join("\n") + "\n";
}
