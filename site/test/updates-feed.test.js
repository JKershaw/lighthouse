import { test } from 'node:test';
import assert from 'node:assert/strict';
import { datedDay, datedNotices, dailyEntries, combinedThread } from '../lib/updates.js';
import { buildStories } from '../lib/stories.js';
import { feedCatalog, atomFeed, relevantFeeds } from '../lib/feed.js';
const day=Date.UTC(2026,9,27),account='> **Later evidence, 27 October 2026.** A source says X, not our observation.\n>\n> Its limits stay attached.\n\n> **Correction, 23 October 2026.** Corrected.\n';
const log='## 27 October 2026\n\n- Source says Y, unverified.\n\n## 26 October 2026\n\n- Earlier.\n';
test('date-only notices and log days retain full source text with stable IDs',()=>{
  assert.equal(datedDay('31 February 2026'),null);
  const notices=datedNotices(account);assert.equal(notices.length,2);assert.equal(notices[0].id,'notice-2026-10-27-later-evidence');assert.match(notices[0].markdown,/Its limits stay attached/);
  assert.equal(datedNotices(account+"\n"+account)[2].id,'notice-2026-10-27-later-evidence-1');
  assert.equal(dailyEntries(log).length,2);
  const entries=combinedThread(account,log);assert.deepEqual(entries.map(e=>e.kind),['later-evidence','unreviewed-log','unreviewed-log','correction']);assert.equal(entries[0].time,entries[1].time);assert.ok(!entries[1].reviewed);
});
const piece={path:'articles/p.md',url:'/articles/p/',title:'Finding & limit',summary:'Summary < limit',pubTime:day-86400000,revisedTime:day,added:0,notices:datedNotices(account),investigationId:'one'};
const essay={...piece,path:'essays/e.md',url:'/essays/e/',title:'Interpretation',essay:true,investigationId:'',notices:[]};
const draft={...piece,path:'articles/draft.md',url:'/articles/draft/',title:'DRAFT EXCLUDED',draft:true};
function repo(){return {siteUrl:'https://example.test',strap:'A watch',pieces:[piece,draft],releasedEssays:[essay],investigations:[{id:'one',title:'Question',path:'investigations/one.md',url:'/investigations/one/',pieces:[]}],sourceBodies:{[essay.path]:'See [the inquiry](../investigations/one.md).'},stories:[{path:'watch/one.md',url:'/watch/one/',title:'Story',entries:combinedThread(account,log).map(e=>({...e,title:(e.reviewed?'Reviewed':'Unreviewed daily log')+': '+e.iso,url:'/watch/one/#'+e.id}))}]};}
test('section and investigation feeds separate kinds, retain citing essays and exclude drafts',()=>{
  const r=repo();r.feeds=feedCatalog(r);assert.equal(r.feeds.length,6);
  assert.ok(r.feeds.find(f=>f.id==='findings').entries.every(e=>e.kind==='piece'));
  assert.ok(r.feeds.find(f=>f.id==='essays').entries.every(e=>e.kind==='essay'));
  const inv=r.feeds.find(f=>f.id==='investigation-one');assert.equal(inv.entries.length,2);
  const watch=r.feeds.find(f=>f.id==='watch');assert.deepEqual(new Set(watch.entries.map(e=>e.kind)),new Set(['correction','later-evidence']));
  const story=r.feeds.find(f=>f.id.startsWith('story-'));assert.ok(story.entries.filter(e=>e.kind==='unreviewed-log').every(e=>e.title.startsWith('Unreviewed daily log:') && e.summary.startsWith('Unreviewed')));
  for(const feed of r.feeds){const xml=atomFeed(r,feed);assert.ok(!xml.includes('DRAFT EXCLUDED'));assert.match(xml,/xmlns="http:\/\/www.w3.org\/2005\/Atom"/);for(const entry of feed.entries){assert.match(entry.published,/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$/);assert.match(entry.updated,/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$/);assert.ok(entry.kind);}}
  assert.match(atomFeed(r,r.feeds[1]),/Finding &amp; limit/);
  assert.deepEqual(relevantFeeds(r,{section:'articles',investigationId:'one'}).map(f=>f.id),['all','findings','investigation-one']);
});

test('story declarations reject unreleased accounts and draft logs rather than labelling them reviewed',()=>{
  const declaration={path:'watch/test.md',url:'/watch/test/',title:'Story',story:true,header:[{key:'account',value:'articles/a.md'},{key:'log',value:'notes/l.md'}]};
  const account={path:'articles/a.md',url:'/articles/a/',section:'articles',status:'released'};
  const workingLog={path:'notes/l.md',url:'/notes/l/'};
  const paths={'articles/a.md':account,'notes/l.md':workingLog};
  const bodies=new Map([[account.path,'> **Correction, 27 October 2026.** Fixed.'],[workingLog.path,'## 27 October 2026\n\n- An attributed report.']]);
  assert.equal(buildStories([declaration],paths,bodies)[0].entries.length,2);
  assert.throws(()=>buildStories([declaration],{...paths,'articles/a.md':{...account,status:'draft',draft:true}},bodies),/released full account/);
  assert.throws(()=>buildStories([declaration],{...paths,'notes/l.md':{...workingLog,header:[{key:'status',value:'draft'}]}},bodies),/released full account/);
  assert.equal(buildStories([{...declaration,draft:true}],paths,bodies).length,0);
});
