// The front page and the section fronts. Editorial choices (the lead, its
// deck, the section ledes and short summaries) live in Markdown: README.md's
// header and site/sections.md. Lists and dates come from the repository.
import path from 'node:path';
import { headerField, parseHeader } from './header.js';

// How many items the front page's Latest list shows.
export const LATEST_COUNT = 6;

// A summaries item reads "path | short summary".
function parseSummaries(items = []) {
  return new Map(items.map((item) => {
    const at = item.indexOf('|');
    return at < 0 ? [item.trim(), ''] : [item.slice(0, at).trim(), item.slice(at + 1).trim()];
  }));
}

// A piece's most recent activity: its publication, revision or dated notice.
const lastActivity = (p) => Math.max(p.pubTime || 0, p.revisedTime || 0);

// The lead's illustration: the first image in its body, if the image is in the
// repository, with the italic caption that follows it.
function leadFigure(leadPath, body, images) {
  const image = body.match(/!\[([^\]]*)\]\(([^)\s]+)\)/);
  if (!image) return null;
  const imagePath = path.posix.normalize(path.posix.join(path.posix.dirname(leadPath), image[2]));
  if (!images.includes(imagePath)) return null;
  const following = body.slice(image.index + image[0].length);
  const caption = following.match(/^\s*\*([^\n]+)\*/)?.[1] || '';
  return { url: `/${imagePath}`, alt: image[1], caption };
}

export function frontInfo({ source = '', config = '', byPath, bodies, images, pieces, essays, investigations, watch }) {
  const header = parseHeader(source);
  const settings = parseHeader(config);
  const value = (name) => headerField(settings?.fields, name)?.value || '';
  const headerValue = (name) => headerField(header?.fields, name)?.value || '';
  const summaries = parseSummaries(headerField(settings?.fields, 'summaries')?.items);

  const kindOf = (p) => {
    if (p.path === watch?.path) return 'Unreviewed log';
    if (p.essay) return 'Essay · interpretation';
    if (p.section === 'articles') return 'Finding';
    return p.label || 'Record';
  };
  const entry = (p) => p ? {
    ...p,
    compactSummary: summaries.get(p.path) || p.summary || '',
    entryKind: kindOf(p),
    entryDate: p.published || p.changed,
  } : null;
  const eligible = (p) => p && !p.draft && (!p.status || p.status === 'released');
  const chosen = (name, accepts = () => true) => {
    const page = byPath[value(`${name} lead`)];
    return eligible(page) && accepts(page) ? entry(page) : null;
  };

  // The lead: a released full piece named in README.md's header.
  const leadPath = headerValue('lead');
  const leadPage = byPath[leadPath];
  const lead = eligible(leadPage) && leadPage.section === 'articles' && !leadPage.short ? {
    ...entry(leadPage),
    deck: headerValue('deck') || summaries.get(leadPath) || leadPage.summary,
    figure: leadFigure(leadPath, bodies.get(leadPath) || '', images),
  } : null;

  // Latest: released findings and essays by their most recent activity,
  // leaving out the lead so that nothing on the page appears twice.
  const latest = [...pieces, ...essays]
    .filter((p) => eligible(p) && p.path !== lead?.path)
    .sort((a, b) => lastActivity(b) - lastActivity(a) || a.path.localeCompare(b.path))
    .slice(0, LATEST_COUNT)
    .map(entry);

  // Investigations: active ones first, each with its question.
  const isActive = (inv) => inv.attention === 'active';
  const investigationCards = [...investigations]
    .sort((a, b) => Number(isActive(b)) - Number(isActive(a)) || a.title.localeCompare(b.title));

  // The section fronts (/watch/, /articles/, /essays/, /map/).
  const sections = [
    { id: 'watch', title: 'The watch', url: '/watch/', lede: value('watch lede'), lead: chosen('watch'),
      entries: [entry(watch && byPath[watch.path]), ...investigations.filter(isActive).map((i) => entry(byPath[i.path]))].filter(Boolean) },
    { id: 'findings', title: 'Findings', url: '/articles/', lede: value('findings lede'),
      lead: chosen('findings', (p) => p.section === 'articles' && !p.short), entries: pieces.filter(eligible).map(entry) },
    { id: 'essays', title: 'Essays', url: '/essays/', lede: value('essays lede'),
      lead: chosen('essays', (p) => p.essay) || entry(essays.filter(eligible)[0]), entries: essays.filter(eligible).map(entry) },
    { id: 'map', title: 'The map', url: '/map/', lede: value('map lede'), lead: chosen('map'),
      entries: [entry(byPath['observations.md']), ...investigations.map((i) => entry(byPath[i.path]))].filter(Boolean) },
  ];
  for (const section of sections) section.entries = section.entries.filter((p) => p.path !== section.lead?.path);

  return { lead, latest, investigations: investigationCards, sections, summaries: Object.fromEntries(summaries) };
}

// README.md rendered: its title is dropped, its first paragraph becomes the
// front page's visible introduction, and the rest stays behind the page's
// "Background and qualifications" disclosure.
export function homeContent(html = '') {
  const body = html.replace(/^\s*<h1[^>]*>[\s\S]*?<\/h1>\s*/, '');
  const first = body.match(/^\s*(<p>[\s\S]*?<\/p>)\s*/);
  return first ? { intro: first[1], background: body.slice(first[0].length) } : { intro: '', background: body };
}
