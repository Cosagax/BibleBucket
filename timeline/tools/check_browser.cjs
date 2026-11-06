/* Offline UI regression: renders authorized repository files; all network blocked.
   BB_PLAYWRIGHT=/path/to/playwright-core BB_CHROMIUM=/usr/bin/chromium node this-file
   Screenshots and a JSON report go to BB_QA_DIR or /tmp/biblebucket-timeline-qa. */
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const {chromium}=require(process.env.BB_PLAYWRIGHT||'playwright-core');
const root=path.resolve(__dirname,'..');
const out=process.env.BB_QA_DIR||'/tmp/biblebucket-timeline-qa';
fs.mkdirSync(out,{recursive:true});
const files={};
for(const name of ['data.json','assets/land.json',...fs.readdirSync(path.join(root,'texts')).filter(x=>x.endsWith('.json')).map(x=>'texts/'+x)]) files[name]=fs.readFileSync(path.join(root,name),'utf8');
const css=fs.readFileSync(path.join(root,'styles.css'),'utf8'),js=fs.readFileSync(path.join(root,'app.js'),'utf8');
function documentHtml(name='index.html'){
 let html=fs.readFileSync(path.join(root,name),'utf8').replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi,'').replace(/<link\b[^>]*>/gi,'');
 html=html.replace(/src="([^"]+)"/g,(match,src)=>{
  const file=path.resolve(root,src);if(!fs.existsSync(file))return match;
  return `src="data:${src.endsWith('.svg')?'image/svg+xml':'image/png'};base64,${fs.readFileSync(file).toString('base64')}"`;
 });return html;
}
const results=[],errors=[];
function check(name,condition){assert(condition,name);results.push(name);}
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.BB_CHROMIUM||'/usr/bin/chromium',args:['--disable-dev-shm-usage']});
 try{
  async function open(viewport,name='index.html'){
   const context=await browser.newContext({viewport,reducedMotion:'reduce',offline:true,serviceWorkers:'block'});
   const page=await context.newPage();page.on('pageerror',e=>errors.push(String(e)));
   await page.route('**/*',route=>route.abort());
   await page.setContent(documentHtml(name));await page.addStyleTag({content:css});
   if(name==='index.html'){
    await page.evaluate(files=>{window.fetch=async input=>{const name=String(input).replace(/^\.\//,'');if(!(name in files))throw new Error('Unprovided local resource: '+name);return new Response(files[name],{status:200,headers:{'Content-Type':'application/json'}});};},files);
    await page.addScriptTag({content:js});await page.waitForSelector('.event-card');
   }
   return{page,context};
  }
  const desktop=await open({width:1440,height:1000}),p=desktop.page;
  check('Desktop starts with Genesis and local data',await p.locator('#detail-panel h3').innerText()==='In the beginning');
  check('Desktop has no page-level horizontal overflow',await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await p.screenshot({path:path.join(out,'desktop-hero.png')});
  await p.locator('#explore').scrollIntoViewIfNeeded();await p.screenshot({path:path.join(out,'desktop-story.png')});
  await p.locator('[data-filter="ethiopian"]').click();
  check('Ethiopian filter exposes Watchers in the main story',await p.locator('.event-card[data-select="watchers"]').count()===1);
  await p.locator('.event-card[data-select="watchers"]').click();
  check('Watchers opens a sourced detail',/Mount Hermon/.test(await p.locator('#detail-panel').innerText()));
  await p.locator('#detail-panel [data-read="ENO"][data-chapter="6"]').click();
  await p.waitForFunction(()=>document.querySelector('#reader-content').getAttribute('aria-busy')==='false');
  check('Enoch chapter loads in the reading room',/Hermon/.test(await p.locator('#reader-content').innerText()));
  await p.locator('#reader-next').click();await p.waitForFunction(()=>document.querySelector('#reader-title').textContent==='1 Enoch 7'&&document.querySelector('#reader-content').getAttribute('aria-busy')==='false');
  check('Reading room advances chapters',/wives/.test(await p.locator('#reader-content').innerText()));
  await p.locator('#reader-book').selectOption('ACT');await p.locator('#reader-chapter').selectOption('8');
  await p.waitForFunction(()=>document.querySelector('#reader-title').textContent==='Acts 8'&&document.querySelector('#reader-content').getAttribute('aria-busy')==='false');
  check('Footnote-only verses retain clearly labeled edition notes',/Edition note at verse 37/.test(await p.locator('#reader-content').innerText()));
  await p.keyboard.press('Escape');check('Escape closes the modal',!(await p.locator('#reader').evaluate(e=>e.open)));
  await p.locator('#search').fill('Ahab');await p.waitForTimeout(200);
  await p.locator('.event-card[data-select="ahab"]').click();
  check('Search includes rulers outside the active era',await p.locator('#detail-panel h3').innerText()==='Ahab');
  await p.locator('[data-view="kings"]').click();
  check('Year lens shows contemporary northern and southern kings',/Ahab/.test(await p.locator('#year-summary').innerText())&&/Jehoshaphat/.test(await p.locator('#year-summary').innerText()));
  await p.locator('[data-year="701"]').click();check('Year preset changes the synchronized kingdoms',/Hezekiah/.test(await p.locator('#year-summary').innerText()));
  await p.locator('#year-range').focus();await p.keyboard.press('ArrowRight');
  check('Year slider supports keyboard changes',await p.locator('#year-output').innerText()!=='701 BCE');
  await p.screenshot({path:path.join(out,'desktop-kings.png')});
  await p.locator('[data-view="families"]').click();await p.locator('#family-select').selectOption('david-line');
  await p.locator('g[data-select="ruth"]').click();check('Family diagram opens the selected person',await p.locator('#detail-panel h3').innerText()==='Ruth chooses to stay');
  check('Tree has a text alternative',await p.getByText('Text version of these relationships',{exact:true}).count()===1);
  await p.locator('.diagram-scroll').scrollIntoViewIfNeeded();await p.screenshot({path:path.join(out,'desktop-family.png')});
  await p.locator('[data-view="map"]').click();await p.locator('#place-select').selectOption('jerusalem');
  check('Atlas place selector exposes linked stories',/Jerusalem/.test(await p.locator('#place-card h4').innerText())&&await p.locator('#place-card [data-select]').count()>5);
  await p.locator('[data-map-zoom="0.25"]').click();check('Map zoom changes the drawing size',(await p.locator('.map-svg').getAttribute('style')).includes('125%'));
  await p.screenshot({path:path.join(out,'desktop-map.png')});
  await p.locator('[data-trail="watchers"]').click();await p.locator('[data-trail-step="1"]').click();
  check('Guided trail advances to the next connection',/Watchers/.test(await p.locator('#detail-panel h3').innerText()));
  await p.locator('[data-save="watchers"]').click();await p.locator('[data-saved-only]').click();
  check('Saved entries can be retrieved during a visit',await p.locator('.event-card[data-select="watchers"]').count()===1);
  await p.locator('#search').fill('zzq-no-such-story-8821');await p.waitForTimeout(200);check('Search has a useful empty state',await p.locator('.empty-state').count()===1);
  await p.locator('[data-reset-search]').click();check('Empty search can be reset',await p.locator('.event-card').count()>1);
  const mobile=await open({width:390,height:844}),m=mobile.page;
  await m.screenshot({path:path.join(out,'mobile-hero.png')});
  for(const view of ['story','kings','families','map']){
   await m.locator(`[data-view="${view}"]`).click();
   check(`Mobile ${view} view has no page-level horizontal overflow`,await m.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   if(view==='map')await m.screenshot({path:path.join(out,'mobile-map.png')});
  }
  await m.locator('[data-view="story"]').click();await m.locator('[data-era="beginnings"]').click();
  await m.locator('.event-card[data-select="watchers"]').click();
  check('Mobile selection brings the detail into view',await m.locator('#detail-panel').evaluate(e=>e.getBoundingClientRect().top>=0&&e.getBoundingClientRect().top<150));
  check('Mobile save and share controls remain reachable',await m.locator('#detail-panel .tool-row').evaluate(e=>{const r=e.getBoundingClientRect();return r.width>=60&&r.left>=0&&r.right<=innerWidth;}));
  await m.screenshot({path:path.join(out,'mobile-detail.png')});
  await m.locator('#detail-panel [data-read="JUB"]').click();await m.waitForFunction(()=>document.querySelector('#reader-content').getAttribute('aria-busy')==='false');
  check('Jubilees opens in the mobile reading room',/Jubilees/.test(await m.locator('#reader-title').innerText()));
  check('Mobile reader fits the screen',await m.locator('#reader').evaluate(e=>e.getBoundingClientRect().width<=innerWidth));
  await m.screenshot({path:path.join(out,'mobile-reader.png')});
  await m.locator('#close-reader').click();
  await m.setViewportSize({width:320,height:720});
  for(const view of ['story','kings','families','map']){
   await m.locator(`[data-view="${view}"]`).click();
   check(`Small-phone ${view} view has no page-level horizontal overflow`,await m.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  }
  const source=await open({width:390,height:844},'sources.html');
  check('Source notes fit a phone',await source.page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  check('Source notes disclose the exact-edition gap',/not represented as a verified complete 88-book Bible/.test(await source.page.locator('main').innerText()));
  check('No JavaScript runtime exceptions',errors.length===0);
  const report={passed:results.length,checks:results,errors,screenshots:fs.readdirSync(out).filter(n=>n.endsWith('.png'))};
  fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
