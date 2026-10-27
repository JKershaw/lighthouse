// Editorial choices live in Markdown; lists and dates come from the repository.
import path from 'node:path';
import { headerField, parseHeader } from './header.js';
export function frontInfo({ source = '', config = '', byPath, bodies, images, pieces, essays, investigations, watch }) {
  const header = parseHeader(source), settings = parseHeader(config);
  const field = (name) => headerField(settings?.fields, name);
  const value = (name) => field(name)?.value || '';
  const summaries = new Map((field('summaries')?.items || []).map((item) => { const at = item.indexOf('|'); return at < 0 ? [item.trim(), ''] : [item.slice(0, at).trim(), item.slice(at + 1).trim()]; }));
  const entry = (p) => p ? { ...p, compactSummary: summaries.get(p.path) || p.summary || '', entryKind: p.path === watch?.path ? 'Unreviewed log' : p.essay ? 'Essay · interpretation' : p.section === 'articles' ? 'Finding' : p.label || 'Record', entryDate: p.published || p.changed } : null;
  const eligible = (p) => p && !p.draft && (!p.status || p.status === 'released');
  const chosen = (name, accepts = () => true) => { const page = byPath[value(`${name} lead`)]; return eligible(page) && accepts(page) ? entry(page) : null; };
  const sections = [
    { id:'watch', title:'The watch', url:'/watch/', lede:value('watch lede'), lead:chosen('watch'), entries:[entry(watch && byPath[watch.path]), ...investigations.filter(i=>i.attention==='active').map(i=>entry(byPath[i.path]))].filter(Boolean) },
    { id:'findings', title:'Findings', url:'/articles/', lede:value('findings lede'), lead:chosen('findings', p => p.section === 'articles' && !p.short), entries:pieces.filter(eligible).map(entry) },
    { id:'essays', title:'Essays', url:'/essays/', lede:value('essays lede'), lead:chosen('essays', p => p.essay) || entry(essays.filter(eligible)[0]), entries:essays.filter(eligible).map(entry) },
    { id:'map', title:'The map', url:'/map/', lede:value('map lede'), lead:chosen('map'), entries:[entry(byPath['observations.md']), ...investigations.map(i=>entry(byPath[i.path]))].filter(Boolean) },
  ];
  for (const section of sections) section.entries = section.entries.filter(p=>p.path!==section.lead?.path);
  const leadPath = headerField(header?.fields,'lead')?.value || '', leadPage = byPath[leadPath];
  let lead = null;
  if (eligible(leadPage) && leadPage.section==='articles' && !leadPage.short) {
    const image = (bodies.get(leadPath)||'').match(/!\[([^\]]*)\]\(([^)\s]+)\)/);
    const imagePath = image && path.posix.normalize(path.posix.join(path.posix.dirname(leadPath),image[2]));
    const following = image ? (bodies.get(leadPath) || '').slice(image.index + image[0].length) : '';
    const caption = following.match(/^\s*\*([^\n]+)\*/)?.[1] || '';
    const figure = image && images.includes(imagePath) ? {url:'/'+imagePath,alt:image[1],caption} : null;
    lead = {...entry(leadPage),deck:headerField(header?.fields,'deck')?.value || summaries.get(leadPath) || leadPage.summary,figure};
  }
  return {lead,sections,summaries:Object.fromEntries(summaries)};
}
