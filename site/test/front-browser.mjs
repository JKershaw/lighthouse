// Run after npm run build. Supports PLAYWRIGHT_MODULE and CHROMIUM_PATH.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { fileURLToPath } from 'node:url';
const {chromium}=await import(process.env.PLAYWRIGHT_MODULE || 'playwright');
const site=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const output=path.join(site,'_site'), shots=path.join(site,'test/screenshots/front-32-33');fs.mkdirSync(shots,{recursive:true});
const types={'.html':'text/html','.svg':'image/svg+xml','.css':'text/css','.js':'text/javascript','.woff2':'font/woff2'};
const server=http.createServer((req,res)=>{let file=path.join(output,decodeURIComponent(new URL(req.url,'http://localhost').pathname));try{if(fs.statSync(file).isDirectory())file=path.join(file,'index.html');if(!file.startsWith(output+path.sep))throw Error();res.setHeader('Content-Type',types[path.extname(file)]||'application/octet-stream');res.end(fs.readFileSync(file));}catch{res.writeHead(404);res.end();}});await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH,headless:true,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage']});
try{
  const origin=`http://127.0.0.1:${server.address().port}`;
  for(const theme of ['light','dark']){
    const context=await browser.newContext({viewport:{width:390,height:844},colorScheme:theme});
    // Remote font availability must not determine layout or verification.
    await context.route('https://fonts.googleapis.com/**',r=>r.abort());await context.route('https://fonts.gstatic.com/**',r=>r.abort());
    const page=await context.newPage();await page.goto(origin,{waitUntil:'domcontentloaded'});
    assert.equal(await page.locator('main h1').count(),1);assert.equal(await page.locator('.front-door').count(),4);
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth),390);
    assert.match(await page.locator('.front-lead figcaption').textContent(),/not a count of attacks/);
    assert.equal(await page.locator('.front-background').getAttribute('open'),null);
    await page.locator('.front-background summary').focus();await page.keyboard.press('Enter');
    assert.notEqual(await page.locator('.front-background').getAttribute('open'),null);
    assert.match(await page.locator('.front-background').textContent(),/a classification by criteria the catalogue does not state/);
    await page.locator('.front-background summary').click();
    for(const target of await page.locator('.compact-entry h3 a,.section-link').all())assert.ok((await target.boundingBox()).height>=44);
    await page.screenshot({path:path.join(shots,`home-${theme}-390.png`),fullPage:true});
    for(const [route,title] of [['watch','The watch'],['articles','Findings'],['essays','Essays'],['map','The map']]){
      await page.goto(`${origin}/${route}/`,{waitUntil:'domcontentloaded'});assert.equal(await page.locator('main h1').textContent(),title);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth),390);
      if(route==='watch'){assert.match(await page.locator('main').textContent(),/unreviewed/);assert.match(await page.locator('.compact-entry').first().textContent(),/Unreviewed log/);}
      if(route==='essays')assert.match(await page.locator('main').textContent(),/interpretation/);
      await page.screenshot({path:path.join(shots,`${route}-${theme}-390.png`)});
    }
    await page.setViewportSize({width:1280,height:960});await page.goto(origin,{waitUntil:'domcontentloaded'});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth),1280);
    await page.screenshot({path:path.join(shots,`home-${theme}-1280.png`),fullPage:true});await context.close();
  }
  console.log('Front/section Chromium checks passed in both themes: 390px, 1280px, keyboard disclosure, retained qualifications, labelled log, and 44px entry targets.');
}finally{await browser.close();await new Promise(r=>server.close(r));}
