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

// How current a piece is, for the Latest list: the later of its publication
// and its latest dated Correction, which changes what the piece said. A Later
// evidence notice or a `revised` item is shown beside the piece but does not
// lift it, so a confirming notice on an old piece does not sit above new work.
export const LATEST_ORDER = 'Newest first, by the date each was published or last corrected; other later notices are shown beside each.';
export const currentAt = (p) => Math.max(p.pubTime || 0, ...(p.revisionHistory || []).filter((r) => r.kind === 'correction').map((r) => r.time || 0));

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
  const topicLabels = parseSummaries(headerField(settings?.fields, 'labels')?.items);

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

  // Latest: released findings and essays, newest first by publication or
  // correction (LATEST_ORDER says so on the page), leaving out the lead so
  // that nothing on the page appears twice.
  const latest = [...pieces, ...essays]
    .filter((p) => eligible(p) && p.path !== lead?.path)
    .sort((a, b) => currentAt(b) - currentAt(a) || (b.pubTime || 0) - (a.pubTime || 0) || a.path.localeCompare(b.path))
    .slice(0, LATEST_COUNT)
    .map(entry);

  // Investigations: active ones first, each group in the order given (by title),
  // with a line of facts about each.
  const isActive = (inv) => inv.attention === 'active';
  const count = (n, one, many) => (n ? `${n} ${n === 1 ? one : many}` : '');
  const investigationCards = [...investigations]
    .sort((a, b) => Number(isActive(b)) - Number(isActive(a)))
    .map((inv) => ({
      ...inv,
      facts: [
        inv.attention && `Attention: ${inv.attention}`,
        inv.started && `since ${inv.started}`,
        count(inv.studies.length, 'study', 'studies'),
        count(inv.pieces.filter((p) => !p.draft && !p.short).length, 'piece', 'pieces'),
      ].filter(Boolean),
    }));

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

  return { lead, latest, latestOrder: LATEST_ORDER, investigations: investigationCards, sections, labels: Object.fromEntries(summaries), summaries, topicLabels };
}

// Rendered Markdown without its leading h1, for a layout that sets the title itself.
export function withoutTitle(html = '') {
  return html.replace(/^\s*<h1[^>]*>[\s\S]*?<\/h1>\s*/, '');
}

// README.md rendered: its title is dropped, its first paragraph becomes the
// front page's visible introduction, and the rest stays behind the page's
// "Background and qualifications" disclosure.
export function homeContent(html = '') {
  const body = withoutTitle(html);
  const first = body.match(/^\s*(<p[\s>][\s\S]*?<\/p>)\s*/);
  return first ? { intro: first[1], background: body.slice(first[0].length) } : { intro: '', background: body };
}

// The front page's "This week" block, from site/this-week.md: a comment, then
// a header with `week` (the first and last day, YYYY-MM-DD to YYYY-MM-DD),
// `updated` (YYYY-MM-DD) and `items`, each "YYYY-MM-DD | reported or
// lighthouse | one plain sentence in Markdown". The block is left out when the
// file is missing, has no items in the week, or was last updated more than `staleDays`
// before the build, so a missed update shows nothing rather than an old week.
const ITEM_LABELS = { reported: 'Reported', lighthouse: 'Lighthouse' };
export function thisWeek(source = '', now = new Date(), staleDays = 8) {
  const text = String(source || '').replace(/^\uFEFF/, '').replace(/^\s*<!--[\s\S]*?-->\s*/, '');
  const header = parseHeader(text);
  if (!header) return null;
  const value = (name) => headerField(header.fields, name)?.value || '';
  const day = (iso) => {
    const d = /^\d{4}-\d{2}-\d{2}$/.test(iso) ? new Date(`${iso}T00:00:00Z`) : null;
    return d && !Number.isNaN(d.getTime()) ? d : null;
  };
  const updated = day(value('updated'));
  if (!updated || now.getTime() - updated.getTime() > staleDays * 86400000) return null;
  const long = new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' });
  const short = new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'short', timeZone: 'UTC' });
  const items = (headerField(header.fields, 'items')?.items || []).map((item) => {
    const m = item.match(/^([^|]*)\|([^|]*)\|([\s\S]*)$/) || [];
    const [when, kind, sentence] = [m[1], m[2], m[3]].map((x) => (x || '').trim());
    const date = day(when);
    const label = ITEM_LABELS[kind.toLowerCase()];
    return date && label && sentence ? { iso: when, day: short.format(date), kind: kind.toLowerCase(), label, sentence } : null;
  }).filter(Boolean);
  const [from, to] = value('week').split(/\s+to\s+/).map(day);
  // Items from before the week are left out, whatever the file still holds.
  const current = from ? items.filter((item) => item.iso >= value('week').slice(0, 10)) : items;
  if (!current.length) return null;
  const span = from && to
    ? (from.getUTCMonth() === to.getUTCMonth() && from.getUTCFullYear() === to.getUTCFullYear()
      ? `${from.getUTCDate()} to ${long.format(to)}` : `${long.format(from).replace(/ \d{4}$/, from.getUTCFullYear() === to.getUTCFullYear() ? '' : '$&')} to ${long.format(to)}`)
    : '';
  return { span, fromIso: from ? value('week').slice(0, 10) : '', toIso: to ? value('week').slice(-10) : '', updated: long.format(updated), updatedIso: value('updated'), items: current };
}

// The day's line from site/this-week.md's header (`today: YYYY-MM-DD |
// sentence`): what the watch read that day, unreviewed and shown as Live.
// Hidden when more than `maxDays` old at build, so a missed day shows nothing
// rather than a stale line (the plan's designed empty state).
export function todayLine(source = '', now = new Date(), maxDays = 2) {
  const text = String(source || '').replace(/^﻿/, '').replace(/^\s*<!--[\s\S]*?-->\s*/, '');
  const header = parseHeader(text);
  const raw = header ? headerField(header.fields, 'today')?.value || '' : '';
  const m = raw.match(/^(\d{4}-\d{2}-\d{2})\s*\|\s*([\s\S]+)$/);
  if (!m) return null;
  const day = new Date(`${m[1]}T00:00:00Z`);
  if (Number.isNaN(day.getTime()) || now.getTime() - day.getTime() > maxDays * 86400000) return null;
  return { iso: m[1], day: new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'long', timeZone: 'UTC' }).format(day), sentence: m[2].trim() };
}

// "What we've learned so far", from site/learned.md: a header with `date`,
// `status` (draft or reviewed), `reviews`, `items` ("path | headline |
// sentence", each retelling one released piece or essay) and `question` (the
// closing line on the charter's question). Only a reviewed block is shown; a
// draft only in a preview build (LIGHTHOUSE_PREVIEW=drafts), marked as one.
export function learnedInfo(source = '', preview = false) {
  const text = String(source || '').replace(/^\uFEFF/, '').replace(/^\s*<!--[\s\S]*?-->\s*/, '');
  const header = parseHeader(text);
  if (!header) return null;
  const value = (name) => headerField(header.fields, name)?.value || '';
  const status = value('status').toLowerCase();
  if (status !== 'reviewed' && !(preview && status === 'draft')) return null;
  const items = (headerField(header.fields, 'items')?.items || []).map((item) => {
    const [path, headline, ...rest] = item.split('|').map((x) => x.trim());
    return path && headline && rest.length ? { path, headline, sentence: rest.join('|').trim() } : null;
  }).filter(Boolean);
  if (!items.length) return null;
  const d = /^\d{4}-\d{2}-\d{2}$/.test(value('date')) ? new Date(`${value('date')}T00:00:00Z`) : null;
  return {
    status, draft: status !== 'reviewed', items, question: value('question'),
    iso: value('date'), day: d ? new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' }).format(d) : '',
    reviews: headerField(header.fields, 'reviews')?.items || [],
  };
}
