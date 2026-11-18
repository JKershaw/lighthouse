import { test } from 'node:test';
import assert from 'node:assert/strict';
import { frontInfo, homeContent, withoutTitle, thisWeek, linkWeekItems, firstSentence, cardKicker, LATEST_COUNT, LATEST_ORDER, todayLine } from '../lib/front.js';
const finding = {path:'articles/finding.md',url:'/articles/finding/',title:'A finding',section:'articles',status:'released',published:'1 October 2026',summary:'A complete summary with a limit.'};
const draft = {...finding,path:'articles/draft.md',draft:true,status:'draft'};
const essay = {...finding,path:'essays/reading.md',section:'essays',essay:true};
const log = {path:'notes/log.md',url:'/notes/log/',title:'Daily log',section:'notes',changed:'2 October 2026'};
const data = () => ({byPath:{[finding.path]:finding,[draft.path]:draft,[essay.path]:essay,[log.path]:log},bodies:new Map([[finding.path,'# A finding\n\n![The measured boundary](figure.svg)\n\n*The caption preserves the limit.*']]),images:['articles/figure.svg'],pieces:[draft,finding],essays:[essay],investigations:[],watch:{path:log.path}});
test('the lead: the newest released finding or essay, unless README pins one until a date',()=>{
  const now=new Date('2026-11-18T12:00:00Z');
  const newer={...essay,path:'essays/newer.md',pubTime:5};
  const d=()=>({...data(),byPath:{...data().byPath,[newer.path]:newer},essays:[essay,newer],now});
  // Nothing pinned: the newest, essays included, never a draft.
  assert.equal(frontInfo(d()).lead.path,newer.path);
  assert.equal(frontInfo(d()).lead.pinned,false);
  assert.equal(frontInfo(d()).lead.deck,newer.summary);
  // A pin holds through its day, with its deck and its own illustration.
  const pin='lead: articles/finding.md\nlead until: 2026-11-18\ndeck: A cautious deck.\n\n# Home';
  const front=frontInfo({...d(),source:pin});
  assert.equal(front.lead.path,finding.path);assert.equal(front.lead.pinned,true);assert.equal(front.lead.deck,'A cautious deck.');
  assert.equal(front.lead.figure.url,'/articles/figure.svg');assert.equal(front.lead.figure.alt,'The measured boundary');assert.equal(front.lead.figure.caption,'The caption preserves the limit.');
  // It lapses after that day, and a pin without an end date, or of a draft or a missing page, is ignored.
  assert.equal(frontInfo({...d(),source:pin,now:new Date('2026-11-19T00:00:01Z')}).lead.path,newer.path);
  for(const src of ['lead: articles/finding.md\ndeck: D\n\n# Home','lead: articles/draft.md\nlead until: 2026-12-01\n\n# Home','lead: missing.md\nlead until: 2026-12-01\n\n# Home'])assert.equal(frontInfo({...d(),source:src}).lead.path,newer.path);
  const missing=d();missing.images=[];assert.equal(frontInfo({...missing,source:pin}).lead.figure,null);
  // A piece can name which of its images the front shows.
  const two=d();two.bodies=new Map([[finding.path,'![First](a.svg)\n\n![Second](figure.svg)']]);two.byPath={...two.byPath,[finding.path]:{...finding,frontFigure:'figure.svg'}};two.pieces=[draft,two.byPath[finding.path]];
  assert.equal(frontInfo({...two,source:pin}).lead.figure.alt,'Second');
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

test('the day\'s line is a dateline with its weekday, never "today", and hides two days after its date', () => {
  const src = 'title: This week\ntoday: 2026-11-18 | We read things.\n';
  assert.deepEqual(todayLine(src, new Date('2026-11-18T18:10:00Z')), { iso: '2026-11-18', day: 'Wednesday 18 November', sentence: 'We read things.' });
  assert.equal(todayLine(src, new Date('2026-11-19T23:59:00Z')).day, 'Wednesday 18 November');
  assert.equal(todayLine(src, new Date('2026-11-20T00:00:01Z')), null);
  assert.equal(todayLine('title: This week\ntoday: soon | x\n', new Date('2026-11-18T12:00:00Z')), null);
});

test('this week: the editor picks the front page few, the rest fill by date, the full page goes a day at a time',()=>{
  const head=['title: This week','week: 2026-11-12 to 2026-11-18','updated: 2026-11-18','items:'];
  const items=['- 2026-11-18 | reported | A.','- 2026-11-18 | lighthouse | B.','- 2026-11-17 | lighthouse | C.','- 2026-11-16 | reported | front | D | with a pipe.','- 2026-11-12 | lighthouse | FRONT | E.'];
  const now=new Date('2026-11-18T20:00:00Z');
  const week=thisWeek([...head,...items].join('\n'),now);
  assert.deepEqual(week.lead.map(i=>i.sentence),['A.','D | with a pipe.','E.']);
  assert.deepEqual(week.items.map(i=>i.front),[false,false,false,true,true]);
  assert.deepEqual(week.days.map(d=>[d.day,d.items.length]),[['Wednesday 18 November',2],['Tuesday 17 November',1],['Monday 16 November',1],['Thursday 12 November',1]]);
  assert.equal(week.earliest,'12 November');
  // No picks: the newest three. More than three picks: the first three.
  assert.deepEqual(thisWeek([...head,...items.map(l=>l.replace(/\| front \||\| FRONT \|/,'|'))].join('\n'),now).lead.map(i=>i.sentence),['A.','B.','C.']);
  assert.deepEqual(thisWeek([...head,...items.map(l=>l.replace(/^(- [\d-]+ \| \w+ \|)(?! front| FRONT)/,'$1 front |'))].join('\n'),now).lead.map(i=>i.sentence),['A.','B.','C.']);
});

test('this week links: a study brief or record goes to the study page, with its investigation beside it',()=>{
  const week=thisWeek(['title: This week','week: 2026-11-12 to 2026-11-18','updated: 2026-11-18','items:',
    '- 2026-11-18 | reported | Firms report it; we\'ll [count](studies/LH056/brief.md).',
    '- 2026-11-17 | lighthouse | [Our record](studies/LH055/LH055.md) and [the day\'s read](studies/LH055/checkpoints/2026-11-17.md).',
    '- 2026-11-13 | lighthouse | [A study](studies/LH050/brief.md) for [the investigation](investigations/physical-authority.md).',
    '- 2026-11-12 | reported | [Unlisted](studies/LH999/brief.md) and [a note](notes/x.md).'].join('\n'),new Date('2026-11-18T20:00:00Z'));
  const linked=linkWeekItems(week,{studyHome:{LH056:{title:'Updates',url:'/investigations/u/'},LH055:{title:'Cost',url:'/investigations/c/'},LH050:{title:'Robots',url:'/investigations/r/'}},siteDirs:new Set(['studies/LH056','studies/LH055','studies/LH050'])});
  assert.deepEqual(linked.items.map(i=>[i.sentence,i.home&&i.home.title]),[
    ['Firms report it; we\'ll [count](studies/LH056/).','Updates'],
    ['[Our record](studies/LH055/) and [the day\'s read](studies/LH055/checkpoints/2026-11-17.md).','Cost'],
    ['[A study](studies/LH050/) for [the investigation](investigations/physical-authority.md).',null],
    ['[Unlisted](studies/LH999/brief.md) and [a note](notes/x.md).',null]]);
  assert.equal(linked.lead[0].sentence,linked.items[0].sentence);
  assert.equal(linked.days[1].items[0].home.title,'Cost');
  assert.equal(linkWeekItems(null),null);
});

test('front cards: a first sentence that ignores stops inside links, and a short kicker',()=>{
  assert.equal(firstSentence('Firms ([A.](https://a.example/x.y), [B](b.md)) report it. We count.'),'Firms ([A.](https://a.example/x.y), [B](b.md)) report it.');
  assert.equal(firstSentence('When was it reported? No source says.'),'When was it reported?');
  assert.equal(firstSentence('Version 1.26.1 shipped. Then more.'),'Version 1.26.1 shipped.');
  assert.equal(firstSentence('No stop at all'),'No stop at all');
  assert.deepEqual(cardKicker({essay:true,displayState:'Revised',revised:'8 November 2026',published:'8 November 2026',revisionHistory:[{iso:'2026-11-08'}]}),{kind:'Essay',essay:true,state:'Revised',date:'8 Nov',iso:'2026-11-08'});
  assert.equal(cardKicker({displayState:'Released',published:'30 October 2026',publishedIso:'2026-10-30'}).date,'30 Oct');
  assert.equal(cardKicker(null),null);
});
