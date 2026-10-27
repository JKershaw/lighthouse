import { test } from 'node:test';
import assert from 'node:assert/strict';
import { frontInfo } from '../lib/front.js';
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
