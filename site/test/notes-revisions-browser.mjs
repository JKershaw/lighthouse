// Run after build. Verifies controls, fallback layout and publication metadata.
import assert from 'node:assert/strict';import fs from 'node:fs';import path from 'node:path';import http from 'node:http';import {fileURLToPath} from 'node:url';
const {chromium}=await import(process.env.PLAYWRIGHT_MODULE||'playwright');
const site=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'),output=path.join(site,'_site'),shots=path.join(site,'test/screenshots/notes-revisions-37-39');fs.mkdirSync(shots,{recursive:true});
const mime={'.html':'text/html','.xml':'application/atom+xml','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.woff2':'font/woff2'};
const server=http.createServer((req,res)=>{let file=path.join(output,new URL(req.url,'http://localhost').pathname);try{if(fs.statSync(file).isDirectory())file=path.join(file,'index.html');if(!file.startsWith(output+path.sep))throw Error();res.setHeader('Content-Type',mime[path.extname(file)]||'application/octet-stream');res.end(fs.readFileSync(file));}catch{res.writeHead(404);res.end();}});await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH,headless:true,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage']});
try{
 const origin=`http://127.0.0.1:${server.address().port}`,draft='/articles/drafts/reading-one-trace/',account='/articles/php-emergency-first-reading/';
 for(const theme of ['light','dark']){
  const context=await browser.newContext({viewport:{width:390,height:844},colorScheme:theme}),page=await context.newPage();
  await page.goto(origin+draft);await page.evaluate(()=>document.fonts.ready);
  assert.equal(await page.locator('.side-note').count(),2);
  const toggle=page.locator('.side-note-toggle').first(),body=page.locator('.side-note-body').first();
  assert.equal(await toggle.getAttribute('aria-expanded'),'false');assert.equal(await body.isVisible(),false);
  assert.equal(await toggle.getAttribute('aria-controls'),await body.getAttribute('id'));
  await toggle.focus();await page.keyboard.press('Enter');assert.equal(await toggle.getAttribute('aria-expanded'),'true');assert.ok(await body.isVisible());
  assert.ok(await body.locator('a[href="/articles/what-a-download-shows/"]').count()>0);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth),390);
  await page.screenshot({path:path.join(shots,`note-${theme}-390.png`),fullPage:true});
  await page.keyboard.press('Space');assert.equal(await toggle.getAttribute('aria-expanded'),'false');
  await page.setViewportSize({width:1600,height:1000});await page.waitForFunction(()=>[...document.querySelectorAll('.side-note-body')].every(el=>!el.hidden));
  const boxes=await page.locator('.side-note-body').evaluateAll(es=>es.map(el=>{const r=el.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom};}));assert.ok(boxes.every(b=>b.left>=0 && b.right<=1600));assert.ok(boxes[1].top>=boxes[0].bottom,'margin notes do not overlap');assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth),1600);
  await page.screenshot({path:path.join(shots,`note-${theme}-1600.png`)});
  await page.setViewportSize({width:1600,height:500});await page.evaluate(()=>scrollTo(0,300));await page.setViewportSize({width:1601,height:500});await page.waitForTimeout(50);const scrolledOffset=await page.locator(".side-note").first().evaluate(el=>el.querySelector(".side-note-body").getBoundingClientRect().top-el.querySelector("button").getBoundingClientRect().top);assert.ok(Math.abs(scrolledOffset)<2,"resize while scrolled keeps the first note at its sentence");
  await page.setViewportSize({width:390,height:844});await page.goto(origin+account);await page.evaluate(()=>document.fonts.ready);
  assert.equal(await page.locator('.byline').evaluate(el=>el.nextElementSibling.classList.contains('piece-status')),true);
  const status=page.locator('.piece-status');assert.match(await status.textContent(),/Developing/);assert.match(await status.textContent(),/(Revised|Corrected|Later evidence) \d{1,2} [A-Za-z]+ \d{4}/);assert.match(await status.textContent(),/Next revision: As reviewed fixed-source evidence changes/);
  await page.locator('.byline').evaluate(el=>el.scrollIntoView({block:'start'}));await page.screenshot({path:path.join(shots,`status-${theme}-390.png`)});
  const history=page.locator('.revision-history');assert.ok(await history.locator('details').count()>0);assert.equal(await history.locator('details[open]').count(),0);
  await history.locator('summary').first().focus();await page.keyboard.press('Enter');assert.equal(await history.locator('details[open]').count(),1);assert.ok(await history.locator('a[href="'+account+'#what-changed-after-22-october"]').count()>0);
  await history.evaluate(el=>el.scrollIntoView({block:'start'}));await page.screenshot({path:path.join(shots,`history-${theme}-390.png`)});
  const ids=await page.locator('[id]').evaluateAll(es=>es.map(el=>el.id));assert.equal(ids.length,new Set(ids).size,'rendered account IDs stay unique');
  await page.goto(origin+'/articles/two-days-for-most/');assert.match(await page.locator('.piece-status').textContent(),/Revised/);assert.ok((await page.locator('.revision-history summary').allTextContents()).some(text=>text.includes('Revised')),'header revisions are retained');
  const xml=await(await context.request.get(origin+'/feed.xml')).text();const publication=await page.evaluate(({xml,account})=>{const doc=new DOMParser().parseFromString(xml,'application/xml');const entry=[...doc.querySelectorAll('entry')].find(el=>el.querySelector('link')?.getAttribute('href').endsWith(account));return {error:doc.querySelector('parsererror')?.textContent,state:entry?.querySelector('category[scheme$="publication-state"]')?.getAttribute('term'),summary:entry?.querySelector('summary')?.textContent};},{xml,account});assert.equal(publication.error,undefined);assert.equal(publication.state,'developing');assert.match(publication.summary,/Next revision:/);assert.ok(!xml.includes('Reading one trace'));
  await context.close();
 }
 for(const width of [390,1600]){
  const context=await browser.newContext({viewport:{width,height:1000},javaScriptEnabled:false}),page=await context.newPage();await page.goto(origin+draft);
  for(const note of await page.locator('.side-note-body').all()){assert.ok(await note.isVisible());const box=await note.boundingBox();assert.ok(box.x>=0 && box.x+box.width<=width);}
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth),width);assert.equal(await page.locator('.side-note-toggle:visible').count(),0);await context.close();
 }
 console.log('Chromium: mobile keyboard side notes, wide non-overlapping margins, no-JS 390/1600 fallback, byline status, collapsed revision history, header revisions, source fragments and feed publication-state category passed in both themes.');
}finally{await browser.close();await new Promise(r=>server.close(r));}
