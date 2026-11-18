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

// A piece's illustration: the first image in its body, if the image is in the
// repository, with the italic caption that follows it. Used for the lead and
// for the front page's cards.
export function leadFigure(leadPath, body, images, preferred = '') {
  // A piece may name the image it shows on the front (`front figure:` in its
  // header, a path as written in its body); else its first image.
  const all = [...body.matchAll(/!\[([^\]]*)\]\(([^)\s]+)\)/g)];
  const image = (preferred && all.find((m) => m[2] === preferred)) || all[0];
  if (!image) return null;
  const imagePath = path.posix.normalize(path.posix.join(path.posix.dirname(leadPath), image[2]));
  if (!images.includes(imagePath)) return null;
  const following = body.slice(image.index + image[0].length);
  const caption = following.match(/^\s*\*([^\n]+)\*/)?.[1] || '';
  return { url: `/${imagePath}`, alt: image[1], caption };
}

export function frontInfo({ source = '', config = '', byPath, bodies, images, pieces, essays, investigations, watch, now = new Date() }) {
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

  // The lead story, decided by rule (the keeper, 18 November 2026): the
  // newest released finding or essay, by publication or correction (the
  // Latest order), unless README.md pins one with `lead:` and `lead until:
  // YYYY-MM-DD`, which holds through that day (UTC) and then lapses, so a pin
  // can't go stale unnoticed. A pin's `deck` replaces the piece's summary.
  const full = (p) => eligible(p) && !p.short && (p.section === 'articles' || p.essay);
  const until = /^\d{4}-\d{2}-\d{2}$/.test(headerValue('lead until')) ? new Date(`${headerValue('lead until')}T23:59:59.999Z`) : null;
  const pinned = until && now <= until && full(byPath[headerValue('lead')]) ? byPath[headerValue('lead')] : null;
  const newest = [...pieces, ...essays].filter(full)
    .sort((a, b) => currentAt(b) - currentAt(a) || (b.pubTime || 0) - (a.pubTime || 0) || a.path.localeCompare(b.path))[0];
  const leadPage = pinned || newest || null;
  const lead = leadPage ? {
    ...entry(leadPage),
    pinned: Boolean(pinned),
    deck: (pinned && headerValue('deck')) || summaries.get(leadPage.path) || leadPage.summary,
    figure: leadFigure(leadPage.path, bodies.get(leadPage.path) || '', images, leadPage.frontFigure),
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
export function thisWeek(source = '', now = new Date(), staleDays = 8, leadCount = 3) {
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
  // `date | kind | sentence`, or `date | kind | front | sentence` for an item
  // the editor picks for the front page.
  const items = (headerField(header.fields, 'items')?.items || []).map((item) => {
    const m = item.match(/^([^|]*)\|([^|]*)\|(?:\s*(front)\s*\|)?([\s\S]*)$/i) || [];
    const [when, kind, sentence] = [m[1], m[2], m[4]].map((x) => (x || '').trim());
    const date = day(when);
    const label = ITEM_LABELS[kind.toLowerCase()];
    return date && label && sentence ? { iso: when, day: short.format(date), kind: kind.toLowerCase(), label, sentence, front: Boolean(m[3]) } : null;
  }).filter(Boolean);
  const [from, to] = value('week').split(/\s+to\s+/).map(day);
  // Items from before the week are left out, whatever the file still holds.
  const current = from ? items.filter((item) => item.iso >= value('week').slice(0, 10)) : items;
  if (!current.length) return null;
  const span = from && to
    ? (from.getUTCMonth() === to.getUTCMonth() && from.getUTCFullYear() === to.getUTCFullYear()
      ? `${from.getUTCDate()} to ${long.format(to)}` : `${long.format(from).replace(/ \d{4}$/, from.getUTCFullYear() === to.getUTCFullYear() ? '' : '$&')} to ${long.format(to)}`)
    : '';
  // The front page's few: the editor's picks first (at most `leadCount`), the
  // newest others filling any places left, shown newest first.
  const picked = current.filter((item) => item.front).slice(0, leadCount);
  const fill = current.filter((item) => !item.front).slice(0, leadCount - picked.length);
  const lead = current.filter((item) => picked.includes(item) || fill.includes(item));
  // The full page, a day at a time, newest first.
  const dayName = new Intl.DateTimeFormat('en-GB', { weekday: 'long', day: 'numeric', month: 'long', timeZone: 'UTC' });
  const days = [];
  for (const item of [...current].sort((a, b) => b.iso.localeCompare(a.iso))) {
    if (days.at(-1)?.iso !== item.iso) days.push({ iso: item.iso, day: dayName.format(day(item.iso)).replace(',', ''), items: [] });
    days.at(-1).items.push(item);
  }
  const earliest = days.at(-1).iso;
  return { span, fromIso: from ? value('week').slice(0, 10) : '', toIso: to ? value('week').slice(-10) : '', updated: long.format(updated), updatedIso: value('updated'), items: current, lead, days,
    earliest: new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'long', timeZone: 'UTC' }).format(day(earliest)) };
}

// Where each This week item sends a reader, settled at build so it never
// depends on the editor remembering. A link to a study's brief, record or
// README goes to the study's own page instead (/studies/LHnnn/, which opens
// with its plain "In short" and links the full record); a link to a
// checkpoint or data file is left alone, since it means that day's read. An
// item that links a study also gets `home`, the investigation the study
// belongs to, unless the item already links an investigation page.
export function linkWeekItems(week, { studyHome = {}, siteDirs = new Set() } = {}) {
  if (!week) return week;
  const LINK = /\]\(([^)\s]+)\)/g;
  const fix = (item) => {
    const targets = [...item.sentence.matchAll(LINK)].map((m) => m[1].replace(/^\/+/, ''));
    const sentence = item.sentence.replace(LINK, (whole, target) => {
      const m = target.replace(/^\/+/, '').match(/^studies\/(LH\d+)\/(?:brief|LH\d+|README)\.md$/);
      return m && siteDirs.has(`studies/${m[1]}`) ? `](studies/${m[1]}/)` : whole;
    });
    const study = targets.map((t) => (t.match(/^studies\/(LH\d+)(?:\/|$)/) || [])[1]).find((id) => id && studyHome[id]);
    const linksInvestigation = targets.some((t) => /^investigations\/[^/]+\.md(?:#|$)/.test(t));
    return { ...item, sentence, home: study && !linksInvestigation ? studyHome[study] : null };
  };
  const items = week.items.map(fix);
  const same = (list) => list.map((x) => items[week.items.indexOf(x)]);
  return { ...week, items, lead: same(week.lead), days: week.days.map((d) => ({ ...d, items: same(d.items) })) };
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
  // Shown as a dateline ("Wednesday 18 November"), never "today": the page is
  // static and read in every timezone, so only an absolute day stays true.
  return { iso: m[1], day: new Intl.DateTimeFormat('en-GB', { weekday: 'long', day: 'numeric', month: 'long', timeZone: 'UTC' }).format(day).replace(',', ''), sentence: m[2].trim() };
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

// The first sentence of a line of Markdown, for a one-line "latest" on a
// card: up to the first full stop or question mark outside a link that is
// followed by a capital letter or the end, else the whole line.
export function firstSentence(md = '') {
  let depth = 0;
  for (let i = 0; i < md.length; i += 1) {
    const c = md[i];
    if (c === '[' || c === '(') depth += 1;
    else if ((c === ']' || c === ')') && depth > 0) depth -= 1;
    else if (depth === 0 && (c === '.' || c === '?') && (i === md.length - 1 || /\s[A-Z\[]/.test(md.slice(i + 1, i + 3)))) return md.slice(0, i + 1);
  }
  return md;
}

// What a front-page card shows above its headline: what kind of piece it is
// (a finding, or an essay, which is interpretation), its status and the date
// it was published, revised or corrected, whichever is latest.
export function cardKicker(p) {
  if (!p) return null;
  const date = p.revised || p.published || '';
  const short = date.replace(/^(\d+) (\w{3})\w* \d{4}$/, '$1 $2');
  return { kind: p.essay ? 'Essay' : 'Finding', essay: Boolean(p.essay), state: p.displayState || '', date: short, iso: (p.revisionHistory?.[0]?.iso) || p.publishedIso || '' };
}

// An investigation page's plain opening, lifted from its rendered body so it
// can stand right under the question, before the studies and the queue: the
// first paragraph that starts "In short.", and the body without it.
export function takeInShort(html = '') {
  const m = String(html).match(/<p>\s*<strong>In short\.<\/strong>[\s\S]*?<\/p>/);
  return m ? { lead: m[0], rest: html.slice(0, m.index) + html.slice(m.index + m[0].length) } : { lead: '', rest: html };
}
