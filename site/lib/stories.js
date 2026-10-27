import { headerField } from './header.js';
import { combinedThread } from './updates.js';
export function buildStories(pages,byPath,bodies) {
  return pages.filter(p=>p.story && !p.draft).map(page=>{
    const field=name=>headerField(page.header,name)?.value || '';
    const account=byPath[field('account')],log=byPath[field('log')];
    if(!account || account.draft || account.status !== 'released' || account.section!=='articles' || account.short || !log || headerField(log.header, 'status')?.value.toLowerCase() === 'draft') throw new Error(`${page.path}: a developing story needs a released full account and an existing log`);
    const entries=combinedThread(bodies.get(account.path),bodies.get(log.path)).map(entry=>({...entry,
      sourcePath:entry.reviewed?account.path:log.path,sourceUrl:entry.reviewed?account.url:log.url,
      url:page.url+'#'+entry.id,title:`${entry.reviewed ? entry.label : 'Unreviewed daily log'}: ${entry.iso}`,
    }));
    const story={path:page.path,url:page.url,title:page.title,account,log,entries,investigationId:field('investigation')};
    page.storyData=story;return story;
  }).filter(Boolean);
}
