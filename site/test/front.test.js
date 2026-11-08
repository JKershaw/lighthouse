import { test } from 'node:test';
import assert from 'node:assert/strict';
import { frontInfo, homeContent, withoutTitle, thisWeek, LATEST_COUNT, LATEST_ORDER } from '../lib/front.js';
const finding = {path:'articles/finding.md',url:'/articles/finding/',title:'A finding',section:'articles',status:'released',published:'1 October 2026',summary:'A complete summary with a limit.'};
const draft = {...finding,path:'articles/draft.md',draft:true,status:'draft'};
const essay = {...finding,path:'essays/reading.md',section:'essays',essay:true};
const log = {path:'notes/log.md',url:'/notes/log/',title:'Daily log',section:'notes',changed:'2 October 2026'};
const data = () => ({byPath:{[finding.path]:finding,[draft.path]:draft,[essay.path]:essay,[log.path]:log},bodies:new Map([[finding.path,'# A finding\n\n![The measured boundary](figure.svg)\n\n*The caption preserves the limit.*']]),images:['articles/figure.svg'],pieces:[draft,finding],essays:[essay],investigations:[],watch:{path:log.path}});
test('README selects only a released full finding and its own retained illustration',()=>{
  const front=frontInfo({...data(),source:'lead: articles/finding.md\ndeck: A cautious deck.\n\n# Home'});
  assert.equal(front.lead.path,finding.path);assert.equal(front.lead.figure.url,'/articles/figure.svg');assert.equal(front.lead.figure.alt,'The measured boundary');assert.equal(front.lead.figure.caption,'The caption preserves the limit.');
  for(const path of [draft.path,essay.path,'missing.md'])assert.equal(frontInfo({...data(),source:`lead: ${path}\ndeck: D\n\n# Home`}).lead,null);
  const missing=data();missing.images=[];assert.equal(frontInfo({...missing,source:'lead: articles/finding.md\ndeck: D\n\n# Home'}).lead.figure,null);
});
test('section choices come from Markdown, drafts stay out and watch logs stay labelled',()=>{
  const front=frontInfo({...data(),config:'title: Sections\nfindings lead: articles/finding.md\nfindings lede: Checked against sources.\nsummaries:\n- articles/finding.md | A short signpost with a limit.\n\n# Notes'});
  assert.deepEqual(front.sections.map(s=>s.url),['/watch/','/articles/','/essays/','/map/']);
  const findings=front.sections.find(s=>s.id==='findings');assert.equal(findings.lead.compactSummary,'A short signpost with a limit.');assert.equal(findings.lede,'Checked against sources.');assert.equal(findings.entries.length,0);
  assert.equal(front.sections[0].entries[0].entryKind,'Unreviewed log');assert.equal(front.sections[2].lead.entryKind,'Essay · interpretation');assert.equal(front.sections[2].entries.length,0);
  assert.ok(!JSON.stringify(front.sections).includes(draft.path));assert.equal(finding.summary,'A complete summary with a limit.');
});

test('configured findings and essay leads cannot mislabel a record or the other kind',()=>{
  for(const config of ['title: S\nfindings lead: notes/log.md\nessays lead: articles/finding.md\n\n# Notes','title: S\nfindings lead: essays/reading.md\n\n# Notes']){
    const front=frontInfo({...data(),config});assert.equal(front.sections[1].lead,null);assert.ok(front.sections[2].lead.essay);assert.equal(front.sections[2].lead.path,essay.path);
  }
});

test('latest lists released findings and essays newest first by publication or correction, without the lead, up to its limit',()=>{
  // A revision or later-evidence notice is shown beside a piece but does not lift it; a correction does.
  const older={...finding,path:'articles/older.md',pubTime:1,revisedTime:5,revisionHistory:[{kind:'later-evidence',time:5}]};
  const corrected={...finding,path:'articles/corrected.md',pubTime:0,revisedTime:6,revisionHistory:[{kind:'correction',time:6}]};
  const newer={...finding,path:'articles/newer.md',pubTime:4};
  const lead={...finding,path:'articles/lead.md',pubTime:9};
  const read={...essay,pubTime:3};
  const byPath={...data().byPath,[older.path]:older,[newer.path]:newer,[lead.path]:lead,[read.path]:read,[corrected.path]:corrected};
  const front=frontInfo({...data(),byPath,pieces:[lead,newer,older,corrected,draft],essays:[read],source:'lead: articles/lead.md\ndeck: D\n\n# Home'});
  assert.deepEqual(front.latest.map(p=>p.path),['articles/corrected.md','articles/newer.md','essays/reading.md','articles/older.md']);
  assert.equal(front.latest[2].entryKind,'Essay · interpretation');
  assert.equal(front.latestOrder,LATEST_ORDER);
  const many=Array.from({length:LATEST_COUNT+3},(_,i)=>({...finding,path:`articles/p${i}.md`,pubTime:i}));
  assert.equal(frontInfo({...data(),pieces:many,essays:[]}).latest.length,LATEST_COUNT);
});

test('this week: dated items labelled reported or Lighthouse, items before the week left out, nothing when stale',()=>{
  const file=['<!--','How to keep this file.','-->','title: This week','week: 2026-11-02 to 2026-11-08','updated: 2026-11-08','items:',
    '- 2026-11-08 | lighthouse | We published [an essay](essays/x.md) | with a pipe.','- 2026-11-03 | Reported | CISA listed a flaw.',
    '- 2026-10-30 | lighthouse | Before the week.','- 2026-11-04 | rumour | Not a label.','- someday | reported | No date.'].join('\n');
  const week=thisWeek(file,new Date('2026-11-08T18:00:00Z'));
  assert.equal(week.span,'2 to 8 November 2026');
  assert.equal(week.updated,'8 November 2026');
  assert.deepEqual(week.items.map(i=>[i.day,i.label,i.sentence]),[['8 Nov','Lighthouse','We published [an essay](essays/x.md) | with a pipe.'],['3 Nov','Reported','CISA listed a flaw.']]);
  assert.equal(thisWeek(file,new Date('2026-11-17T00:00:00Z')),null);
  assert.equal(thisWeek(file.replace('2026-10-30','2026-10-29').replace(/- 2026-11-0[38][^\n]*\n?/g,''),new Date('2026-11-08T18:00:00Z')),null);
  assert.equal(thisWeek('',new Date()),null);
  assert.equal(thisWeek(file.replace('week: 2026-11-02 to 2026-11-08','week: 2026-10-28 to 2026-11-03'),new Date('2026-11-08T18:00:00Z')).span,'28 October to 3 November 2026');
});

test('investigations put active ones first, keeping their title order, each with a line of facts',()=>{
  const inv=(title,attention,more={})=>({title,attention,started:'',studies:[],pieces:[],...more});
  const investigations=[inv('A active','active',{started:'1 November 2026',studies:[{}]}),inv('B resting','resting'),inv('C active','active',{pieces:[{},{draft:true},{short:true}]}),inv('D unlabelled','')];
  const cards=frontInfo({...data(),investigations}).investigations;
  assert.deepEqual(cards.map(i=>i.title),['A active','C active','B resting','D unlabelled']);
  assert.deepEqual(cards[0].facts,['Attention: active','since 1 November 2026','1 study']);
  assert.deepEqual(cards[1].facts,['Attention: active','1 piece']);
  assert.deepEqual(cards[3].facts,[]);
});

test('README splits into a visible introduction and the background behind the disclosure',()=>{
  assert.deepEqual(homeContent('<h1>Lighthouse</h1>\n<p>Why.</p>\n<p>More.</p>\n<h2>Where</h2>'),{intro:'<p>Why.</p>',background:'<p>More.</p>\n<h2>Where</h2>'});
  assert.deepEqual(homeContent('<h1>Lighthouse</h1>\n<h2>Only headings</h2>'),{intro:'',background:'<h2>Only headings</h2>'});
  assert.equal(homeContent('<h1>L</h1><p class="x">Why.</p>').intro,'<p class="x">Why.</p>');
  assert.equal(withoutTitle('<h1 id="t">Title</h1>\n<p>Body.</p>'),'<p>Body.</p>');
});
