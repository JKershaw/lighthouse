// Real browser acceptance against the built site; all requests stay local.
import { createServer } from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { chromium } from 'playwright';
const root=path.resolve('site/_site');
const prefix=(process.env.PATH_PREFIX||'').replace(/\/$/,'');
const server=createServer((req,res)=>{
 let p=decodeURIComponent(new URL(req.url,'http://local').pathname);
 if(prefix){if(!p.startsWith(prefix+'/')){res.writeHead(404);res.end();return;}p=p.slice(prefix.length);}
 let file=path.resolve(root,'.'+p);if(!file.startsWith(root+path.sep)&&file!==root){res.writeHead(403);res.end();return;}
 if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
 if(!fs.existsSync(file)){res.writeHead(404);res.end();return;}
 const type={'.html':'text/html','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.woff2':'font/woff2','.json':'application/json'}[path.extname(file)]||'application/octet-stream';res.setHeader('content-type',type);res.end(fs.readFileSync(file));
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
 browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_PATH?{executablePath:process.env.CHROMIUM_PATH}:{})});
 const base=`http://127.0.0.1:${server.address().port}${prefix}`;
 const report=[];
 for(const width of [390,768,1280])for(const theme of ['light','dark']){
  const page=await browser.newPage({viewport:{width,height:900},colorScheme:theme,javaScriptEnabled:false});
  await page.route('**/*',route=>route.request().url().startsWith('http://127.0.0.1:')?route.continue():route.abort());
  const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  await page.goto(base+'/');
  const working=page.getByRole('contentinfo').getByRole('link',{name:'Working files',exact:true});
  assert.ok(await working.isVisible(),'Working files must be reachable from the homepage');
  assert.equal(await page.locator('.front-knowledge').count(),0,'The homepage must not promote the map as a feature');
  await working.click();
  const mapEntry=page.locator('main').getByRole('link',{name:'Knowledge map',exact:true});
  assert.ok(await mapEntry.isVisible(),'The knowledge map must be reachable through Working files');
  await mapEntry.click();
  assert.equal(await page.locator('h1').innerText(),'A map of what we know.');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`Overflow ${width} ${theme}`);
  const current=JSON.parse(fs.readFileSync('site/.generated/knowledge-map.json'));
  const drawing=page.locator(width<1072?'.knowledge-phone-drawing':'.knowledge-wide-drawing');
  if(!current.history.stale){assert.equal(await drawing.locator('svg a').count(),8);assert.ok(await drawing.isVisible());}else{assert.ok((await page.locator('main').innerText()).includes('awaits checking'));}
  if(!current.history.stale)assert.ok(await page.evaluate(()=>document.querySelector('.knowledge-history').compareDocumentPosition(document.querySelector('.knowledge-questions'))&Node.DOCUMENT_POSITION_FOLLOWING),'The visual history must come before the question cards');
  const disclosure=page.locator('#catalogue-software-updates summary');await disclosure.focus();await page.keyboard.press('Enter');
  assert.equal(await page.locator('#catalogue-software-updates').getAttribute('open'),'');
  await page.screenshot({path:`site/test/screenshots/knowledge-${width}-${theme}.png`,fullPage:true});
  const map=JSON.parse(fs.readFileSync('site/.generated/knowledge-map.json'));
  const studies=map.nodes.filter(n=>n.kind==='study');assert.ok(studies.length>=49);
  for(const n of studies){
   const response=await page.goto(base+'/map/knowledge-lineage/records/'+n.path.split('/')[1]+'/');
   assert.equal(response.status(),200,n.id);
   if(n.explanation){assert.equal(await page.locator('h2',{hasText:'What the record says'}).count(),1,n.id);assert.ok((await page.locator('main').innerText()).includes(n.explanation.summary),n.id);}
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),n.id);
  }
  await page.goto(base+'/articles/old-versions-new-pythons/');
  await page.locator('.knowledge-record-entry a').click();
  assert.ok(page.url().includes('/map/knowledge-lineage/records/finding-old-versions-new-pythons/'));
  assert.equal(errors.length,0);report.push({width,theme,studies:studies.length,homepageEntry:true,articleEntry:true,keyboardDisclosure:true,noJavaScript:true});await page.close();
 }
 fs.writeFileSync('site/test/screenshots/knowledge-browser-results.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
}finally{await browser?.close();server.close();}
