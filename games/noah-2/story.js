/* Noah's Ark 2.0 — original SVG art and a dependency-free rescue game.
   The original /games/noah/ is deliberately independent and preserved. */
(() => {
'use strict';
const $ = id => document.getElementById(id);
const canvas=$('game'),ctx=canvas.getContext('2d'),stage=$('stage');
const SPECIES=[['elephant','Elephants'],['giraffe','Giraffes'],['sheep','Sheep'],['rabbit','Rabbits'],['lion','Lions'],['zebra','Zebras'],['tortoise','Tortoises'],['pig','Pigs']].map(([id,name])=>({id,name,img:new Image()}));
const noah=new Image();noah.src='art/noah.svg';
SPECIES.forEach(s=>{s.img.src=`art/${s.id}.svg`;});
const quiet=matchMedia('(prefers-reduced-motion: reduce)');
const clamp=(n,a,b)=>Math.max(a,Math.min(b,n));
const mix=(a,b,t)=>a+(b-a)*t;
const smooth=t=>{t=clamp(t,0,1);return t*t*(3-2*t);};
let w=800,h=650,u=1,mode='intro',state=null,last=0,scene=null,frame=0,ambient=0,soundOn=false,audioCtx=null,noticeTimer=0,lastPaint=0,dirty=true;
const keys=new Set();
function note(message){$('notice').textContent=message;$('notice').classList.add('show');clearTimeout(noticeTimer);noticeTimer=setTimeout(()=>$('notice').classList.remove('show'),2600);}
function hideNotice(){clearTimeout(noticeTimer);$('notice').classList.remove('show');}
function tone(f,d=.15,volume=.035,delay=0){
 if(!soundOn)return;
 try{audioCtx??=new (window.AudioContext||window.webkitAudioContext)();audioCtx.resume();const o=audioCtx.createOscillator(),g=audioCtx.createGain(),t=audioCtx.currentTime+delay;o.type='sine';o.frequency.value=f;g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(volume,t+.025);g.gain.exponentialRampToValueAtTime(.0001,t+d);o.connect(g).connect(audioCtx.destination);o.start(t);o.stop(t+d+.02);}catch{/* Sound is optional. */}
}
function chime(kind){if(kind==='board'){[392,494,587,784].forEach((f,i)=>tone(f,.4,.045,i*.1));}else if(kind==='pair'){tone(440,.18);tone(660,.28,.04,.11);}else tone(330,.16);}
$('sound').onclick=()=>{soundOn=!soundOn;$('sound').textContent=soundOn?'Sound on':'Sound off';$('sound').setAttribute('aria-pressed',String(soundOn));$('sound').setAttribute('aria-label',soundOn?'Turn sound off':'Turn sound on');if(soundOn)tone(523,.18);};
function fit(){
 const oldW=w,oldH=h;w=Math.max(240,stage.clientWidth);h=Math.max(190,stage.clientHeight);u=clamp(Math.min(w/720,h/640),.68,1.25);
 const dpr=Math.min(devicePixelRatio||1,1.5);canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);
 if(state){for(const a of state.animals){a.x=a.x/oldW*w;a.y=a.y/oldH*h;}state.noah.x=state.noah.x/oldW*w;state.noah.y=state.noah.y/oldH*h;if(state.target){state.target.x*=w/oldW;state.target.y*=h/oldH;}state.trails=[];}
 buildScene();dirty=true;
}
new ResizeObserver(fit).observe(stage);
function ellipse(c,x,y,rx,ry,color){c.fillStyle=color;c.beginPath();c.ellipse(x,y,Math.max(.01,rx),Math.max(.01,ry),0,0,Math.PI*2);c.fill();}
function path(c,points,fill){c.beginPath();points(c);c.fillStyle=fill;c.fill();}
function buildScene(){
 scene=document.createElement('canvas');scene.width=Math.ceil(w);scene.height=Math.ceil(h);const c=scene.getContext('2d');
 const sky=c.createLinearGradient(0,0,0,h*.65);sky.addColorStop(0,'#86b1b2');sky.addColorStop(1,'#d8d8b4');c.fillStyle=sky;c.fillRect(0,0,w,h);
 ellipse(c,w*.78,h*.16,42*u,42*u,'#f4e6ad');
 for(let i=0;i<5;i++){const x=w*(.04+i*.24),y=h*(.13+(i%2)*.07);ellipse(c,x,y,43*u,12*u,'#edf0d4aa');ellipse(c,x-12*u,y-9*u,22*u,16*u,'#edf0d4aa');}
 path(c,p=>{p.moveTo(0,h*.4);p.bezierCurveTo(w*.18,h*.19,w*.24,h*.43,w*.44,h*.35);p.bezierCurveTo(w*.7,h*.12,w*.83,h*.34,w,h*.25);p.lineTo(w,h);p.lineTo(0,h);},'#77978a');
 path(c,p=>{p.moveTo(0,h*.47);p.bezierCurveTo(w*.22,h*.28,w*.32,h*.5,w*.56,h*.41);p.bezierCurveTo(w*.78,h*.3,w*.8,h*.51,w,h*.36);p.lineTo(w,h);p.lineTo(0,h);},'#8caa83');
 const field=c.createLinearGradient(0,h*.39,0,h);field.addColorStop(0,'#c0be86');field.addColorStop(1,'#8da06f');
 path(c,p=>{p.moveTo(0,h*.54);p.bezierCurveTo(w*.3,h*.39,w*.72,h*.4,w,h*.53);p.lineTo(w,h);p.lineTo(0,h);},field);
 // A real destination: the path meets the Ark's door, not a random sky position.
 path(c,p=>{p.moveTo(w*.485,h*.36);p.bezierCurveTo(w*.4,h*.56,w*.62,h*.65,w*.31,h);p.lineTo(w*.59,h);p.bezierCurveTo(w*.75,h*.65,w*.54,h*.5,w*.525,h*.36);},'#cebb87');
 c.strokeStyle='#e0d09e77';c.lineWidth=2;for(let i=0;i<17;i++){const x=w*((i*.173+.03)%1),y=h*(.52+((i*.137)%1)*.4);c.beginPath();c.moveTo(x,y);c.lineTo(x-3*u,y-7*u);c.moveTo(x,y);c.lineTo(x+4*u,y-5*u);c.stroke();}
 // Quiet meadow details, drawn once rather than recomputed every frame.
 for(let i=0;i<44;i++){const x=w*((i*.618+.07)%1),y=h*(.5+((i*.383)%1)*.46);if(Math.abs(x-w*.5)<w*.08)continue;ellipse(c,x,y,1.6*u,2*u,i%3?'#ecdca4':'#f3e9cf');}
 for(const side of [-1,1]){const x=side<0?w*.025:w*.975;path(c,p=>{p.moveTo(x,h*.68);p.lineTo(x+side*18*u,h*.45);p.lineTo(x+side*34*u,h*.45);p.lineTo(x+side*16*u,h*.78);},'#476f57');for(let i=0;i<4;i++)ellipse(c,x+side*(4+i*6)*u,h*(.43+i*.027),28*u,36*u,'#648568');}
 // Corner vignette gives the scene a printed-storybook edge.
 const vignette=c.createRadialGradient(w*.5,h*.55,w*.25,w*.5,h*.55,Math.max(w,h)*.8);vignette.addColorStop(0,'#143e3000');vignette.addColorStop(1,'#143e302b');c.fillStyle=vignette;c.fillRect(0,0,w,h);
}
function doorway(){return {x:w*.5,y:h*.405};}
function drawArk(progress=0,closed=false){
 const aw=Math.min(w*.65,420*u),ah=aw*.47,x=w*.5-aw*.5,y=h*.405-ah*1.06-progress*18*u;
 ctx.save();ctx.translate(x,y);
 // A curved timber hull and a little shelter; warm edges give it volume.
 path(ctx,p=>{p.moveTo(0,ah*.53);p.quadraticCurveTo(aw*.45,ah*.7,aw,ah*.43);p.bezierCurveTo(aw*.96,ah*1.08,aw*.74,ah*1.1,aw*.22,ah*1.06);p.quadraticCurveTo(aw*.08,ah,0,ah*.53);},'#926344');
 ctx.strokeStyle='#694c39';ctx.lineWidth=3*u;ctx.stroke();
 for(let i=0;i<4;i++){ctx.strokeStyle=i===0?'#e0b777':'#ba8a58';ctx.lineWidth=(i===0?5:2)*u;ctx.beginPath();ctx.moveTo(aw*(.025+i*.028),ah*(.59+i*.11));ctx.quadraticCurveTo(aw*.55,ah*(.78+i*.11),aw*(.98-i*.035),ah*(.5+i*.11));ctx.stroke();}
 ctx.fillStyle='#b08757';ctx.fillRect(aw*.23,ah*.13,aw*.53,ah*.48);ctx.strokeStyle='#71543d';ctx.lineWidth=2*u;ctx.strokeRect(aw*.23,ah*.13,aw*.53,ah*.48);
 path(ctx,p=>{p.moveTo(aw*.18,ah*.17);p.lineTo(aw*.44,-ah*.02);p.lineTo(aw*.8,ah*.1);p.lineTo(aw*.76,ah*.18);p.lineTo(aw*.45,ah*.07);p.lineTo(aw*.22,ah*.25);},'#655340');
 ctx.strokeStyle='#d0a66c';ctx.beginPath();ctx.moveTo(aw*.22,ah*.22);ctx.lineTo(aw*.45,ah*.04);ctx.lineTo(aw*.78,ah*.14);ctx.stroke();
 for(let i=0;i<4;i++){ctx.fillStyle='#3b4540';ctx.fillRect(aw*(.3+i*.105),ah*.29,aw*.055,ah*.13);ctx.strokeStyle='#d1aa70';ctx.strokeRect(aw*(.3+i*.105),ah*.29,aw*.055,ah*.13);}
 // Door position maps exactly to the ramp's upper endpoint.
 const door=doorway(),dx=door.x-x,dBottom=closed?ah*.99:door.y-y;
 ctx.fillStyle=closed?'#875f43':'#f0d59a';ctx.fillRect(dx-16*u,ah*.64,32*u,Math.max(12*u,dBottom-ah*.64));
 ctx.strokeStyle='#624b39';ctx.lineWidth=3*u;ctx.strokeRect(dx-16*u,ah*.64,32*u,Math.max(12*u,dBottom-ah*.64));
 if(!closed){path(ctx,p=>{p.moveTo(dx-17*u,dBottom);p.lineTo(dx+17*u,dBottom);p.lineTo(dx+26*u,dBottom+26*u);p.lineTo(dx-26*u,dBottom+26*u);},'#d8b77b');ctx.strokeStyle='#987349';ctx.lineWidth=1.2*u;for(let i=0;i<4;i++){const yy=dBottom+4*u+i*6*u;ctx.beginPath();ctx.moveTo(dx-20*u,yy);ctx.lineTo(dx+20*u,yy);ctx.stroke();}}
 ctx.restore();
}
function image(c,img,x,y,width,height,alpha=1){if(!img.complete||!img.naturalWidth)return;c.save();c.globalAlpha=alpha;c.drawImage(img,x-width/2,y-height*.8,width,height);c.restore();}
function drawAnimal(a,t){
 if(a.safe)return;
 const size=47*u,bob=quiet.matches?0:Math.sin(t*2+a.seed)*1.2*u;
 ellipse(ctx,a.x,a.y+4*u,17*u,4*u,'#294d3226');image(ctx,a.species.img,a.x,a.y+bob,size,size*.92);
}
function marker(x,y,r,color){ctx.strokeStyle=color;ctx.lineWidth=2*u;ctx.beginPath();ctx.ellipse(x,y+7*u,r,r*.42,0,0,Math.PI*2);ctx.stroke();}
function init(){
 hideNotice();keys.clear();$('intro').hidden=true;$('ending').hidden=true;$('pausePanel').hidden=true;$('skip').hidden=true;$('hud').hidden=false;$('pause').disabled=false;
 const peaceful=document.querySelector('input[name="journey"]:checked').value==='peaceful';
 const animals=[],slots=[];
 for(let row=0;row<4;row++)for(let col=0;col<4;col++)slots.push({x:w*(.12+col*.25+(row%2)*.015),y:mix(h*.49,h*.77,row/3)});
 // Shuffle placement, never species identities: every animal always has one mate.
 for(let i=slots.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[slots[i],slots[j]]=[slots[j],slots[i]];}
 SPECIES.forEach((species,i)=>{for(let j=0;j<2;j++){const pos=slots[i*2+j];animals.push({...pos,species,seed:i*7+j*2,held:false,safe:false,vx:(Math.random()-.5)*4,vy:(Math.random()-.5)*3});}});
 state={animals,noah:{x:w*.5,y:h*.64},target:null,lead:null,mate:null,rescued:new Set(),seconds:90,peaceful,elapsed:0,inactive:0,boarding:[],trails:[],phase:'find',pickupCooldown:0,endStarted:0,won:false};
 mode='play';dirty=true;ambient=0;refreshTask();refreshHUD();$('collection').replaceChildren(...SPECIES.map(s=>{const img=document.createElement('img');img.src=s.img.src;img.alt=`${s.name}: waiting`;img.dataset.id=s.id;return img;}));
 $('footerHelp').textContent='Find a pair. Walk them to the ramp.';canvas.focus({preventScroll:true});tone(294,.2);tone(392,.3,.035,.15);
}
function refreshTask(){
 if(!state)return;const s=state;const img=$('taskAnimal');img.hidden=!s.lead;
 if(s.lead)img.src=s.lead.species.img.src;
 if(s.phase==='escort'){$('taskLabel').textContent='BRING THEM HOME';$('taskText').textContent=`Guide both ${s.lead.species.name.toLowerCase()} to the glowing ramp.`;}
 else if(s.lead){$('taskLabel').textContent='FIND THE PARTNER';const singular={elephant:'elephant',giraffe:'giraffe',sheep:'sheep',rabbit:'rabbit',lion:'lion',zebra:'zebra',tortoise:'tortoise',pig:'pig'};$('taskText').textContent=`Find the other ${singular[s.lead.species.id]}.`;}
 else{$('taskLabel').textContent='TWO BY TWO';$('taskText').textContent=s.rescued.size?'Choose another animal. Every pair matters.':'Walk to any animal to begin.';}
}
function refreshHUD(){
 if(!state)return;const s=state;$('count').textContent=s.rescued.size;
 $('clock').textContent=s.peaceful?'No rush':`${Math.floor(Math.ceil(s.seconds)/60)}:${String(Math.ceil(s.seconds)%60).padStart(2,'0')}`;
 $('weatherLabel').textContent=s.peaceful?'A peaceful gathering':s.seconds>65?'The gathering':s.seconds>30?'Rain on the horizon':'The storm is near';
 $('timeFill').style.width=(s.peaceful?100:s.seconds/90*100)+'%';$('timeFill').style.background=s.seconds<20&&!s.peaceful?'#efb38c':'#e5ca8c';
}
function returnIntro(){mode='intro';dirty=true;state=null;keys.clear();hideNotice();$('intro').hidden=false;$('ending').hidden=true;$('pausePanel').hidden=true;$('hud').hidden=true;$('skip').hidden=true;$('pause').disabled=true;$('footerHelp').textContent='A little story. A little adventure.';$('start').focus({preventScroll:true});}
function pause(){if(mode!=='play')return;mode='paused';dirty=true;keys.clear();state.target=null;hideNotice();$('pausePanel').hidden=false;$('resume').focus({preventScroll:true});}
function resume(){if(mode!=='paused')return;mode='play';last=performance.now();$('pausePanel').hidden=true;canvas.focus({preventScroll:true});}
$('start').onclick=init;$('pause').onclick=pause;$('resume').onclick=resume;$('restartPause').onclick=returnIntro;$('again').onclick=init;
window.addEventListener('keydown',e=>{
 if((e.key==='Escape'||e.key==='p'||e.key==='P')&&!e.repeat){if(mode==='play'){e.preventDefault();pause();}else if(mode==='paused'){e.preventDefault();resume();}else if(mode==='cinematic'&&e.key==='Escape')finishEnding();return;}
 const key=e.key.toLowerCase();if(mode==='play'&&['arrowup','arrowdown','arrowleft','arrowright','w','a','s','d'].includes(key)){e.preventDefault();keys.add(key);state.target=null;}
});
window.addEventListener('keyup',e=>keys.delete(e.key.toLowerCase()));
window.addEventListener('blur',()=>{keys.clear();if(mode==='play')pause();});
document.addEventListener('visibilitychange',()=>{if(document.hidden&&mode==='play')pause();});
function setTarget(e){if(mode!=='play')return;const r=canvas.getBoundingClientRect();state.target={x:clamp(e.clientX-r.left,24*u,w-24*u),y:clamp(e.clientY-r.top,h*.405,h*.79)};}
canvas.addEventListener('pointerdown',e=>{if(mode!=='play')return;e.preventDefault();canvas.focus({preventScroll:true});canvas.setPointerCapture(e.pointerId);setTarget(e);});
canvas.addEventListener('pointermove',e=>{if(e.buttons||e.pointerType==='touch'&&canvas.hasPointerCapture(e.pointerId))setTarget(e);});
canvas.addEventListener('pointercancel',()=>{if(state)state.target=null;});
function boardPair(){
 const s=state,door=doorway(),species=s.lead.species;
 for(const a of [s.lead,s.mate]){a.held=false;a.safe=true;s.boarding.push({species,x:a.x,y:a.y,t:0,door});}
 s.rescued.add(species.id);s.lead=null;s.mate=null;s.phase='find';s.pickupCooldown=.6;s.inactive=0;
 const icon=$('collection').querySelector(`[data-id="${species.id}"]`);icon.classList.add('rescued');icon.alt=`${species.name}: safe aboard`;
 refreshTask();refreshHUD();chime('board');note(`${species.name} are safe aboard. ${s.rescued.size} of 8 pairs!`);
 if(s.rescued.size===8)beginEnding(true);
}
function beginEnding(won){
 if(mode!=='play')return;state.won=won;state.endStarted=performance.now();state.target=null;mode='cinematic';keys.clear();hideNotice();$('hud').hidden=true;$('pause').disabled=true;$('skip').hidden=false;
 if(won)[262,330,392,523].forEach((f,i)=>tone(f,1.8,.035,i*.18));else{tone(262,1.2,.025);tone(294,1.2,.018,.3);}
}
function finishEnding(){
 if(mode!=='cinematic')return;mode='ended';dirty=true;$('skip').hidden=true;$('ending').hidden=false;
 const s=state,won=s.won;
 $('endEyebrow').textContent=won?'SAFE IN THE ARK':'THE RAIN HAS ARRIVED';
 $('endTitle').textContent=won?'Every pair. A new beginning.':'Every rescue mattered.';
 $('endSummary').textContent=won?'Eight pairs, sixteen animals, and one faithful journey. You brought them all home.':`${s.rescued.size} of 8 pairs made it safely aboard. Try again, or choose a peaceful gathering with no clock.`;
 $('endVerse').textContent=won?'“and the LORD shut him in.”':'“But with thee will I establish my covenant;”';
 $('endRef').textContent=won?'Genesis 7:16 · KJV':'Genesis 6:18 · KJV';
 $('endNote').textContent=won?'After the Flood, the rainbow recalls God’s covenant. · Genesis 9:13':'There’s still a place for every pair. Take a breath, and open the gates again.';
 $('endAnimals').replaceChildren(...SPECIES.map(species=>{const img=document.createElement('img');img.src=species.img.src;const safe=s.rescued.has(species.id);img.alt=species.name+(safe?' rescued':' waiting');if(!safe)img.className='missing';return img;}));
 $('again').textContent=won?'Gather again →':'Try another journey →';
 // Return unsuccessful rounds to the journey choices, so peaceful mode is reachable.
 $('again').onclick=won?init:returnIntro;$('footerHelp').textContent=won?'Two by two. All aboard.':'A new journey is waiting.';$('again').focus({preventScroll:true});
}
$('skip').onclick=finishEnding;
function update(dt){
 const s=state;if(mode!=='play'||!s)return;
 s.elapsed+=dt;s.inactive+=dt;s.pickupCooldown=Math.max(0,s.pickupCooldown-dt);
 if(!s.peaceful)s.seconds=Math.max(0,s.seconds-dt);
 let dx=(keys.has('arrowright')||keys.has('d')?1:0)-(keys.has('arrowleft')||keys.has('a')?1:0),dy=(keys.has('arrowdown')||keys.has('s')?1:0)-(keys.has('arrowup')||keys.has('w')?1:0);
 const n=s.noah,speed=clamp(Math.min(w,h)*.49,155,320)*(s.phase==='escort'?.92:1);
 if(dx||dy){const len=Math.hypot(dx,dy);n.x+=dx/len*speed*dt;n.y+=dy/len*speed*dt;s.inactive=0;}
 else if(s.target){dx=s.target.x-n.x;dy=s.target.y-n.y;const dist=Math.hypot(dx,dy),travel=Math.min(dist,speed*dt);if(dist>1){n.x+=dx/dist*travel;n.y+=dy/dist*travel;s.inactive=0;}else s.target=null;}
 n.x=clamp(n.x,24*u,w-24*u);n.y=clamp(n.y,h*.405,h*.79);
 // The meadow stays bounded above the task panel; animals never hide under the UI.
 for(const a of s.animals){if(a.safe||a.held)continue;a.x=clamp(a.x+a.vx*dt,28*u,w-28*u);a.y=clamp(a.y+a.vy*dt,h*.48,h*.77);if(a.x<=28*u||a.x>=w-28*u)a.vx*=-1;if(a.y<=h*.48||a.y>=h*.77)a.vy*=-1;}
 if(s.lead){const follow=(a,tx,ty)=>{const k=1-Math.exp(-dt*9);a.x=mix(a.x,tx,k);a.y=mix(a.y,ty,k);};follow(s.lead,n.x-27*u,n.y+19*u);if(s.mate)follow(s.mate,n.x+25*u,n.y+28*u);}
 if(s.phase!=='escort'&&s.pickupCooldown===0){
 const close=s.animals.filter(a=>!a.safe&&!a.held&&(!s.lead||a.species.id===s.lead.species.id)).sort((a,b)=>Math.hypot(a.x-n.x,a.y-n.y)-Math.hypot(b.x-n.x,b.y-n.y))[0];
 if(close&&Math.hypot(close.x-n.x,close.y-n.y)<28*u){close.held=true;s.inactive=0;if(!s.lead){s.lead=close;s.phase='partner';chime('pick');}else{s.mate=close;s.phase='escort';chime('pair');note('A perfect pair! Guide them up the glowing ramp.');}refreshTask();}
 }
 const d=doorway();if(s.phase==='escort'&&Math.hypot(n.x-d.x,n.y-d.y)<35*u)boardPair();
 for(const a of s.boarding)a.t+=dt;s.boarding=s.boarding.filter(a=>a.t<1.1);
 refreshHUD();
 if(mode==='play'&&s.seconds===0&&!s.peaceful)beginEnding(false);
}
function drawRain(intensity,t){
 if(intensity<=0||quiet.matches)return;
 ctx.save();ctx.strokeStyle=`rgba(218,233,227,${.16+intensity*.14})`;ctx.lineWidth=1*u;ctx.beginPath();
 const count=Math.floor(30+intensity*55);for(let i=0;i<count;i++){const x=((i*.618033*w+t*(20+intensity*25))%(w+25))-25,y=(i*71+t*(160+intensity*180))%(h+25)-25;ctx.moveTo(x,y);ctx.lineTo(x-4*u,y+10*u);}ctx.stroke();ctx.restore();
}
function drawWater(t,won){
 const p=mode==='ended'?1:smooth(t/(quiet.matches?1:5));
 const waterY=mix(h*1.1,h*.385,p);ctx.fillStyle=won?'#5e9399':'#487e8a';
 ctx.beginPath();ctx.moveTo(0,h);ctx.lineTo(0,waterY);for(let x=0;x<=w+20;x+=20)ctx.lineTo(x,waterY+Math.sin(x*.018+(quiet.matches?0:t))*(4*u));ctx.lineTo(w,h);ctx.closePath();ctx.fill();
 ctx.strokeStyle='#c4d9ca44';ctx.lineWidth=1.6*u;for(let i=0;i<7;i++){const yy=waterY+(h-waterY)*(i+.7)/8;ctx.beginPath();for(let x=0;x<=w;x+=10){const y=yy+Math.sin(x*.024+i+t*.4)*3*u;x?ctx.lineTo(x,y):ctx.moveTo(x,y);}ctx.stroke();}
 if(won){ctx.save();ctx.globalAlpha=p*.65;ctx.lineWidth=7*u;const colors=['#e1a187','#e5c486','#e4d99f','#a8c6a2','#95bfc3'];colors.forEach((color,i)=>{ctx.strokeStyle=color;ctx.beginPath();ctx.ellipse(w*.5,h*.47,w*.38-i*8*u,h*.39-i*8*u,0,Math.PI,Math.PI*2);ctx.stroke();});ctx.restore();}
}
function render(t){
 ctx.clearRect(0,0,w,h);if(scene)ctx.drawImage(scene,0,0,w,h);
 const s=state,cin=mode==='cinematic'||mode==='ended';
 const storm=s&&!s.peaceful?clamp(s.elapsed/90,0,1):0;
 // Weather alters the landscape, not animal legibility. No lightning flashes.
 if(storm>0){ctx.fillStyle=`rgba(25,53,69,${storm*.34})`;ctx.fillRect(0,0,w,h);}
 if(cin){const elapsed=mode==='ended'?8:(performance.now()-s.endStarted)/1000;drawWater(elapsed,s.won);drawArk(smooth(elapsed/5),true);if(s.won){const dh=Math.min(w*.65,420*u)*.47;image(ctx,noah,w*.49,h*.405-dh*.66-18*u,35*u,46*u);}drawRain(s.won?0:.7,t);return;}
 drawArk();
 if(s){
 const d=doorway();
 if(s.phase==='escort'){
 const pulse=quiet.matches?1:.8+Math.sin(t*2)*.15;
 ellipse(ctx,d.x,d.y+24*u,34*u,12*u,`rgba(255,232,165,${pulse*.55})`);
 ctx.fillStyle='#fff1b7';ctx.font=`600 ${11*u}px system-ui`;ctx.textAlign='center';ctx.fillText('THIS WAY',d.x,d.y-10*u);
 ctx.setLineDash([4*u,7*u]);ctx.strokeStyle='#f7e7b388';ctx.lineWidth=2*u;ctx.beginPath();ctx.moveTo(s.noah.x,s.noah.y);ctx.lineTo(d.x,d.y+24*u);ctx.stroke();ctx.setLineDash([]);
 }
 if(s.target&&mode==='play'){marker(s.target.x,s.target.y,8*u,'#f4e4aeaa');}
 const mate=s.lead&&!s.mate?s.animals.find(a=>!a.held&&!a.safe&&a.species.id===s.lead.species.id):null;
 if(mate){marker(mate.x,mate.y,23*u,'#f5e5a8');ctx.fillStyle='#fff5ce';ctx.font=`bold ${12*u}px system-ui`;ctx.textAlign='center';ctx.fillText('PARTNER',mate.x,mate.y-29*u);}
 const actors=s.animals.filter(a=>!a.safe).map(a=>({y:a.y,draw:()=>drawAnimal(a,t)}));actors.push({y:s.noah.y,draw:()=>{
 ellipse(ctx,s.noah.x,s.noah.y+5*u,18*u,5*u,'#294d3240');const bob=!quiet.matches&&(s.target||keys.size)?Math.sin(t*12)*1.1*u:0;image(ctx,noah,s.noah.x,s.noah.y+bob,58*u,76*u);
 }});actors.sort((a,b)=>a.y-b.y).forEach(a=>a.draw());
 for(const a of s.boarding){const k=smooth(a.t/1.1);image(ctx,a.species.img,mix(a.x,d.x,k),mix(a.y,d.y-12*u,k),47*u*(1-k*.65),43*u*(1-k*.65),1-k);}
 }else{
 image(ctx,SPECIES[0].img,w*.25,h*.72,75*u,69*u);image(ctx,SPECIES[0].img,w*.18,h*.77,68*u,62*u);image(ctx,SPECIES[1].img,w*.77,h*.64,70*u,64*u);image(ctx,SPECIES[2].img,w*.82,h*.78,66*u,61*u);
 }
 drawRain(storm>.25?(storm-.25)/.75:0,t);
}
function loop(now){frame=requestAnimationFrame(loop);if(!w||!h)return;const dt=Math.min((now-(last||now))/1000,.05);last=now;if(mode!=='paused'){ambient+=dt;if(mode==='play')update(dt);if(mode==='cinematic'&&(now-state.endStarted)/1000>(quiet.matches?1.2:6.5))finishEnding();}
 if(dirty||((mode==='play'||mode==='cinematic')&&now-lastPaint>=32)){render(ambient);lastPaint=now;dirty=false;}
}
fit();frame=requestAnimationFrame(loop);
// Keep the story playable even if an optional illustration fails to load.
Promise.allSettled([...SPECIES.map(s=>s.img.decode()),noah.decode()]).then(results=>{
 dirty=true;
 if(results.some(r=>r.status==='rejected'))note('Some artwork could not load. Refresh to try again.');
});
})();
