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
for(const name of ['data.json','assets/land.json','assets/mediterranean-land.json',...fs.readdirSync(path.join(root,'texts')).filter(x=>x.endsWith('.json')).map(x=>'texts/'+x)]) files[name]=fs.readFileSync(path.join(root,name),'utf8');
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
    await page.evaluate(files=>{window.fetch=async input=>{const name=String(input).replace(/^\.\//,'').split('?')[0];if(!(name in files))throw new Error('Unprovided local resource: '+name);return new Response(files[name],{status:200,headers:{'Content-Type':'application/json'}});};},files);
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
  await p.locator('.christ-focus').scrollIntoViewIfNeeded();
  await p.screenshot({path:path.join(out,'desktop-jesus-gateway.png')});
  await p.locator('.christ-focus [data-trail="jesus-story"]').click();
  check('Jesus gateway starts the full guided story',/Jesus/.test(await p.locator('#detail-panel h3').innerText())&&/Stop 1 of 18/.test(await p.locator('#trail-active').innerText()));
  await p.locator('[data-trail-step="1"]').click();
  check('Jesus journey moves into the annunciation',/Let it be/.test(await p.locator('#detail-panel h3').innerText()));
  await p.locator('#detail-panel [data-read="LUK"]').first().click();
  await p.waitForFunction(()=>document.querySelector('#reader-content').getAttribute('aria-busy')==='false');
  check('New Gospel reference opens and highlights its verses',await p.locator('#reader-book').inputValue()==='LUK'&&await p.locator('.verse.highlight').count()>0);
  await p.locator('#close-reader').click();
  await p.locator('[data-open-entry="nativity"]').click();
  check('Free exploration clears a guided trail and opens the selected story',/Good news in a manger/.test(await p.locator('#detail-panel h3').innerText())&&await p.locator('#trail-active').isHidden());
  await p.locator('#era-select').selectOption('threshold');
  await p.locator('[data-next-era="arrival"]').click();
  check('The historical bridge continues directly into Jesus',await p.locator('#era-select').inputValue()==='arrival'&&/Jesus/.test(await p.locator('#detail-panel h3').innerText()));
  await p.locator('.echo-card summary').click();
  check('Scripture echoes distinguish the connection and expose its sources',/Explicit genealogy/.test(await p.locator('.scripture-echoes').innerText())&&await p.locator('.echo-card [data-read="GEN"]').count()===1);
  await p.locator('[data-view="families"]').click();await p.locator('#family-select').selectOption('jesus-household');
  check('Jesus genealogy distinguishes Joseph’s household role',await p.locator('.tree-edge.guardian').count()===1&&/not.*biological/.test(await p.locator('.view-title').innerText()));
  await p.locator('g[data-select="jesus"]').focus();await p.keyboard.press('Enter');
  check('New family nodes support keyboard selection',/Jesus/.test(await p.locator('#detail-panel h3').innerText()));
  await p.locator('.diagram-scroll').scrollIntoViewIfNeeded();await p.screenshot({path:path.join(out,'desktop-jesus-family.png')});
  await p.locator('[data-view="map"]').click();await p.locator('#place-select').selectOption('rome');
  check('Rome automatically opens the wider Mediterranean map',await p.locator('#map-region').inputValue()==='mediterranean'&&await p.locator('#place-card h4').innerText()==='Rome');
  check('Rome pin is inside the visible map',await p.locator('g[data-place="rome"] circle.pin-halo').evaluate(e=>Number(e.getAttribute('cx'))>0&&Number(e.getAttribute('cx'))<1000&&Number(e.getAttribute('cy'))>0&&Number(e.getAttribute('cy'))<600));
  await p.locator('#map-scroll').scrollIntoViewIfNeeded();await p.screenshot({path:path.join(out,'desktop-mediterranean.png')});
  await p.locator('#map-region').selectOption('heartlands');
  check('Original heartlands map remains available without invisible selected pins',await p.locator('#place-select').inputValue()==='jerusalem'&&await p.locator('g[data-place="rome"]').count()===0);
  await p.locator('#place-select').selectOption('philippi');
  check('Northern places also open the wider map',await p.locator('#map-region').inputValue()==='mediterranean');
  await p.locator('#map-region').selectOption('heartlands');
  await p.locator('#place-select').selectOption('tarsus');
  await p.locator('#place-card [data-select="paul"]').click();
  await p.locator('#detail-panel [data-select="rome-witness"]').click();
  check('Following a western story while in the map widens its frame',await p.locator('#map-region').inputValue()==='mediterranean'&&await p.locator('#place-select').inputValue()==='rome');
  await p.locator('[data-view="story"]').click();await p.locator('#era-select').selectOption('revelation');
  check('Revelation exposes eight image trails and its reading boundaries',await p.locator('.symbol-links button').count()===8&&/Vision sequence/.test(await p.locator('.story-header').innerText()));
  await p.locator('.symbol-links [data-select="rev-number"]').focus();await p.keyboard.press('Enter');
  check('Revelation symbols are keyboard-selectable and name disputed readings',/666/.test(await p.locator('#detail-panel h3').innerText())&&/616/.test(await p.locator('#detail-panel .context-note').innerText()));
  await p.locator('.echo-card summary').click();
  check('The mark’s echo opens the contrasting names in Revelation 14',await p.locator('.echo-card [data-read="REV"][data-chapter="14"]').count()===1);
  await p.locator('.echo-card [data-read="REV"][data-chapter="14"]').click();
  await p.waitForFunction(()=>document.querySelector('#reader-content').getAttribute('aria-busy')==='false');
  check('Revelation comparison loads the local text with highlighting',await p.locator('#reader-book').inputValue()==='REV'&&await p.locator('.verse.highlight').count()===5);
  await p.locator('#close-reader').click();
  await p.locator('#explore').scrollIntoViewIfNeeded();await p.screenshot({path:path.join(out,'desktop-revelation.png')});
  await p.locator('[data-save="rev-number"]').click();await p.locator('[data-saved-only]').click();
  check('New and old saved entries coexist',await p.locator('.event-card[data-select="rev-number"]').count()===1&&await p.locator('.event-card[data-select="watchers"]').count()===1);
  await p.locator('#show-trails').click();
  check('All fifteen journeys retain the original six in order',await p.locator('.trail-card').count()===15&&await p.locator('.trail-card').nth(0).getAttribute('data-trail')==='watchers'&&await p.locator('.trail-card').nth(5).getAttribute('data-trail')==='exile');
  for(const id of ['jesus-story','last-week','homecoming','lamb-thread','ends-earth','revelation-echoes','seven-churches','creation-new','women-witness']){
   await p.locator(`.trail-card[data-trail="${id}"]`).click();
   const count=Number((await p.locator('.trail-nav').innerText()).match(/of (\d+)/)[1]);
   for(let i=1;i<count;i++)await p.locator('[data-trail-step="1"]').click();
   check(`New journey ${id} reaches its final stop`,await p.locator('[data-trail-step="1"]').isDisabled()&&new RegExp(`Stop ${count} of ${count}`).test(await p.locator('#trail-active').innerText()));
   if(id==='creation-new')check('Cross-era journey keeps chapter context synchronized',await p.locator('#era-select').inputValue()==='revelation');
  }
  await m.setViewportSize({width:390,height:844});
  await m.locator('.christ-focus').scrollIntoViewIfNeeded();await m.screenshot({path:path.join(out,'mobile-jesus-gateway.png')});
  await m.locator('[data-open-entry="empty-tomb"]').click();
  check('Phone gateway opens the actual resurrection detail',/He has risen/.test(await m.locator('#detail-panel h3').innerText())&&await m.locator('#detail-panel').evaluate(e=>e.getBoundingClientRect().top>=0&&e.getBoundingClientRect().top<150));
  await m.screenshot({path:path.join(out,'mobile-resurrection.png')});
  for(const width of [390,320,768]){
   await m.setViewportSize({width,height:844});
   for(const era of ['arrival','ministry','passion','revelation']){
    await m.locator('[data-view="story"]').click();await m.locator('#era-select').selectOption(era);
    check(`${width}px ${era} chapter fits the page`,await m.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   }
   await m.locator('.symbol-links [data-select="rev-river"]').click();await m.locator('.echo-card summary').click();
   check(`${width}px open echo panels fit the page`,await m.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   await m.locator('[data-view="map"]').click();await m.locator('#place-select').selectOption('rome');
   check(`${width}px Mediterranean map controls fit the page`,await m.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  }
  await m.setViewportSize({width:390,height:844});await m.locator('[data-view="story"]').click();await m.locator('#era-select').selectOption('revelation');
  await m.locator('.vision-key').scrollIntoViewIfNeeded();await m.screenshot({path:path.join(out,'mobile-revelation.png')});
  const source=await open({width:390,height:844},'sources.html');
  check('Source notes fit a phone',await source.page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  check('Source notes disclose the exact-edition gap',/not represented as a verified complete 88-book Bible/.test(await source.page.locator('main').innerText()));
  check('No JavaScript runtime exceptions',errors.length===0);
  const report={passed:results.length,checks:results,errors,screenshots:fs.readdirSync(out).filter(n=>n.endsWith('.png'))};
  fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
