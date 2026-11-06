/* A small, static, source-led atlas. No accounts, trackers, or remote runtime. */
(() => {
  'use strict';
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const normalize = s => String(s).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const motion = () => matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth';
  const mobile = () => matchMedia('(max-width: 720px)').matches;
  const kindNames = {story:'Story',person:'Person',king:'Ruler',prophet:'Prophet',battle:'Battle',vision:'Vision'};
  const icons = {star:'✦',temple:'⌂',branch:'⑂',crown:'♜',city:'▥'};
  let data, books, land, byId, placeById, eraById, visibleIds = [], readerToken = 0;
  const bookCache = new Map();
  const state = {view:'story',era:'beginnings',selected:'creation',filter:'all',query:'',savedOnly:false,showAllTrails:false,trail:null,year:855,family:'before-flood',mapPlace:'jerusalem',mapZoom:1,familyZoom:1,realm:'all'};
  let saved = [], persistentStorage = true;
  try { const value = JSON.parse(localStorage.getItem('bb-atlas-saved-v1') || '[]'); if (Array.isArray(value)) saved = value.filter(x => typeof x === 'string'); } catch { persistentStorage = false; }

  async function getJson(url) {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`Could not load ${url} (${response.status})`);
    return response.json();
  }
  function announce(text) { $('#live-status').textContent = text; }
  function eraName(id) { return eraById.get(id)?.title || ''; }
  function refLabel(ref) { return `${books[ref.book]?.title || ref.book} ${ref.chapter}${ref.verses ? ':' + ref.verses : ''}`; }
  function referenceButtons(refs) {
    return `<div class="reference-list">${refs.map(r => `<button class="reference-button" data-read="${esc(r.book)}" data-chapter="${r.chapter}" data-verses="${esc(r.verses)}" aria-label="Read ${esc(refLabel(r))}">${esc(refLabel(r))} <span aria-hidden="true">↗</span></button>`).join('')}</div>`;
  }
  function badge(e) {
    const enoch = e.refs.some(r => r.book === 'ENO'), jub = e.refs.some(r => r.book === 'JUB');
    return enoch || jub ? `<span class="source-pill">${enoch && jub ? 'ENOCH + JUBILEES' : enoch ? '1 ENOCH' : 'JUBILEES'}</span>` : '';
  }
  function searchText(e) {
    return normalize([e.title,e.summary,e.note,eraName(e.era),kindNames[e.kind],...e.refs.map(refLabel),...e.places.map(p=>placeById.get(p)?.name || '')].join(' '));
  }
  function readHash() {
    const p = new URLSearchParams(location.hash.slice(1));
    if (['story','kings','families','map'].includes(p.get('view'))) state.view = p.get('view');
    if (byId.has(p.get('entry'))) state.selected = p.get('entry');
    state.era = eraById.has(p.get('era')) || p.get('era') === 'all' ? p.get('era') : byId.get(state.selected).era;
    if (data.families.some(f=>f.id === p.get('family'))) state.family = p.get('family');
    if (placeById.has(p.get('place'))) state.mapPlace = p.get('place');
    const year = Number(p.get('year'));
    if (year >= 560 && year <= 1050) state.year = year;
    state.trail = data.trails.some(t=>t.id === p.get('trail')) ? p.get('trail') : null;
  }
  function writeHash(replace = false) {
    const p = new URLSearchParams({view:state.view,entry:state.selected,era:state.era});
    if (state.view === 'kings') p.set('year',String(state.year));
    if (state.view === 'families') p.set('family',state.family);
    if (state.view === 'map') p.set('place',state.mapPlace);
    if (state.trail) p.set('trail',state.trail);
    history[replace ? 'replaceState' : 'pushState'](null,'',`#${p}`);
  }
  function renderTrails() {
    const trails = state.showAllTrails ? data.trails : data.trails.slice(0,3);
    $('#trails').innerHTML = trails.map(t=>`<button class="trail-card" data-trail="${t.id}"><span class="trail-icon" aria-hidden="true">${icons[t.icon]}</span><span><strong>${esc(t.title)}</strong><small>${esc(t.subtitle)}</small></span><span class="trail-arrow" aria-hidden="true">↗</span></button>`).join('');
    $('#show-trails').setAttribute('aria-expanded',String(state.showAllTrails));
    $('#show-trails').innerHTML = `${state.showAllTrails ? 'Fewer journeys' : 'All six journeys'} <span aria-hidden="true">${state.showAllTrails ? '↑' : '↗'}</span>`;
  }
  function renderTrailBanner() {
    const target = $('#trail-active'), trail = data.trails.find(t=>t.id === state.trail);
    target.hidden = !trail;
    if (!trail) { target.innerHTML = ''; return; }
    const index = trail.steps.indexOf(state.selected);
    target.innerHTML = `<div class="trail-banner"><div><strong>${esc(trail.title)}</strong><small>${esc(trail.subtitle)}</small></div><div class="trail-nav"><button class="icon-button" data-trail-step="-1" aria-label="Previous stop in journey" ${index <= 0 ? 'disabled' : ''}>←</button><span>${index >= 0 ? `Stop ${index+1} of ${trail.steps.length}` : 'Exploring a side connection'}</span><button class="icon-button" data-trail-step="1" aria-label="Next stop in journey" ${index === trail.steps.length-1 ? 'disabled' : ''}>→</button><button class="icon-button" data-end-trail aria-label="End guided journey">✕</button></div></div>`;
  }
  function storyEntries() {
    const terms = normalize(state.query.trim()).split(/\s+/).filter(Boolean);
    let candidates = data.entries.filter(e => {
      if (state.savedOnly && !saved.includes(e.id)) return false;
      if (terms.length && !terms.every(t => searchText(e).includes(t))) return false;
      if (!terms.length && state.era !== 'all' && e.era !== state.era) return false;
      if (state.filter === 'people' && !['person','prophet','king'].includes(e.kind)) return false;
      if (state.filter === 'events' && !['story','battle','vision'].includes(e.kind)) return false;
      if (state.filter === 'ethiopian' && !e.refs.some(r=>['ENO','JUB'].includes(r.book))) return false;
      if (!terms.length && !state.savedOnly && state.filter === 'all' && !e.primary && e.id !== state.selected) return false;
      return true;
    });
    if (state.trail && !terms.length && !state.savedOnly) {
      const trail = data.trails.find(t=>t.id === state.trail);
      candidates = trail.steps.map(id=>byId.get(id));
    }
    return candidates;
  }
  function eventCard(e) {
    return `<button class="event-card${e.id === state.selected ? ' selected' : ''}" data-select="${e.id}" aria-pressed="${e.id === state.selected}"><span class="card-top"><span class="kind-label">${kindNames[e.kind]}</span>${badge(e)}</span><h4>${esc(e.title)}</h4><p>${esc(e.summary)}</p><span class="card-foot"><span>${esc(refLabel(e.refs[0]))}${e.refs.length > 1 ? ` + ${e.refs.length-1} more` : ''}</span><span class="card-arrow" aria-hidden="true">↗</span></span></button>`;
  }
  function renderStory() {
    const entries = storyEntries(); visibleIds = entries.map(e=>e.id);
    const era = eraById.get(state.era), searching = Boolean(state.query.trim());
    const heading = searching ? 'Follow your curiosity.' : state.savedOnly ? 'Your saved connections' : state.trail ? data.trails.find(t=>t.id===state.trail).title : era?.title || 'The whole journey';
    const subtitle = searching ? `Results for “${state.query.trim()}” across the collection.` : state.savedOnly ? (persistentStorage ? 'Saved on this browser. No account needed.' : 'Saved for this visit only; this browser has disabled persistent storage.') : era?.subtitle || 'From beginnings to the last scene of Kings.';
    return `<div class="story-layout"><aside class="era-rail" aria-label="Story eras"><p class="rail-label">CHAPTERS OF THE STORY</p><div class="era-buttons">${data.eras.map(e=>`<button class="era-button" data-era="${e.id}" aria-pressed="${state.era===e.id && !searching && !state.trail}"><span class="era-number">${e.number}</span><span>${esc(e.title)}<small>${esc(e.books.split(' · ')[0])}</small></span></button>`).join('')}</div><div class="rail-actions"><button data-era="all" aria-pressed="${state.era==='all' && !state.savedOnly}">☷ &nbsp; All eras</button><button data-saved-only aria-pressed="${state.savedOnly}">☆ &nbsp; Saved (${saved.length})</button></div></aside><div class="story-main"><header class="story-header"><h3>${esc(heading)}</h3><p>${esc(subtitle)}</p>${!searching && !state.savedOnly ? `<div class="date-note">${esc(era?.dating || 'Story order and calendar dates are kept distinct')}</div>` : ''}</header><div class="filter-row" role="group" aria-label="Filter entries">${[['all','Story highlights'],['people','People'],['events','Events & visions'],['ethiopian','Enoch & Jubilees']].map(([id,name])=>`<button data-filter="${id}" aria-pressed="${state.filter===id}">${name}</button>`).join('')}</div><p class="result-note">${entries.length} ${entries.length===1 ? 'entry' : 'entries'}${state.trail ? ' on this journey' : ''} · tap a card to follow its connections</p>${entries.length ? `<div class="event-list">${entries.map(eventCard).join('')}</div>` : `<div class="empty-state"><h3>No threads here yet.</h3><p>${state.savedOnly ? 'Use the star on a story to save it here.' : 'Try another name, a broader era, or a different filter.'}</p><button class="outline-button" data-reset-search>Show the story</button></div>`}</div></div>`;
  }
  function connectionLink(e) {
    return `<button class="connection-link" data-select="${e.id}"><span>${esc(e.title)}<small>${kindNames[e.kind]} · ${esc(eraName(e.era))}</small></span><span aria-hidden="true">↗</span></button>`;
  }
  function renderDetail() {
    const e = byId.get(state.selected), related = [...new Set([...e.related,...data.entries.filter(x=>x.related.includes(e.id)).map(x=>x.id)])].filter(id=>id!==e.id).map(id=>byId.get(id)).slice(0,14);
    const index = visibleIds.indexOf(e.id);
    return `<aside class="detail-panel" id="detail-panel" aria-label="Selected story" tabindex="-1"><div class="detail-mast"><div class="detail-tools"><p class="eyebrow">${kindNames[e.kind].toUpperCase()} · ${esc(eraName(e.era).toUpperCase())}</p><div class="tool-row"><button class="icon-button" data-save="${e.id}" aria-label="${saved.includes(e.id)?'Unsave':'Save'} ${esc(e.title)}" aria-pressed="${saved.includes(e.id)}">${saved.includes(e.id)?'★':'☆'}</button><button class="icon-button" data-share aria-label="Copy a link to this entry">↗</button></div></div><h3>${esc(e.title)}</h3>${badge(e)}<div class="date-note">${esc(e.date)}</div></div><div class="detail-body"><p class="detail-summary">${esc(e.summary)}</p>${e.note ? `<p class="context-note">${esc(e.note)}</p>` : ''}<section class="detail-section"><h4>OPEN THE TEXT</h4>${referenceButtons(e.refs)}</section>${related.length ? `<section class="detail-section"><h4>FOLLOW A CONNECTION</h4><div>${related.map(connectionLink).join('')}</div></section>` : ''}${e.places.length ? `<section class="detail-section"><h4>FIND IT ON THE MAP</h4><div class="place-chips">${e.places.map(id=>`<button class="place-chip" data-map-place="${id}">⌖ ${esc(placeById.get(id).name)}</button>`).join('')}</div></section>` : ''}<div class="detail-bottom"><button data-entry-step="-1" ${index<=0?'disabled':''}>← Previous</button><button data-entry-step="1" ${index<0 || index>=visibleIds.length-1?'disabled':''}>Next connection →</button></div><button class="text-button mobile-detail-link" data-back-list>↑ Back to the explorer</button></div></aside>`;
  }
  function rulerAt(realm, year) {
    return data.entries.filter(e=>e.reign && e.reign.realm===realm && e.reign.start>=year && e.reign.end<=year);
  }
  function kingdomCard(realm,title,year,empty) {
    const entries = rulerAt(realm,year);
    return `<section class="kingdom-card ${realm==='judah'?'south':''}"><p class="eyebrow">${title}</p>${entries.length ? entries.map(e=>`<h4>${esc(e.title)}</h4><p>${esc(e.date)}</p>${connectionLink(e)}`).join('') : `<h4>${esc(empty)}</h4><p>The year lens uses approximate display dates. It does not fill gaps by inventing a reign.</p>`}</section>`;
  }
  function yearSummary() {
    const y = state.year;
    const columns = y>931 ? kingdomCard('united','THE UNITED MONARCHY',y,'Before the conventional monarchy dates') + `<section class="kingdom-card south"><p class="eyebrow">BEFORE THE DIVISION</p><h4>A shared royal story</h4><p>The parallel Israel and Judah tracks begin with the split after Solomon, conventionally around 931 BCE. David’s early reign also overlaps Ish-bosheth’s contested rule.</p>${connectionLink(byId.get('kingdom-split'))}</section>` : kingdomCard('israel','ISRAEL · NORTHERN KINGDOM',y,y<722?'After Samaria’s fall':'A transition in the north') + kingdomCard('judah','JUDAH · SOUTHERN KINGDOM',y,y<586?'After Jerusalem’s fall':'A transition in Judah');
    const prophets = data.prophetWindows.filter(p=>p.start>=y && p.end<=y);
    return `<div class="kingdom-columns">${columns}</div><section class="prophet-strip"><h4>PROPHETS IN THE WIDER PERIOD</h4><div class="prophet-tags">${prophets.length ? prophets.map(p=>`<button data-select="${p.id}">${esc(byId.get(p.id).title)}</button>`).join('') : '<span class="muted">No prophet assigned to this display window.</span>'}</div><p>Prophetic windows are broad contextual estimates, not precise ministry dates. Reign boundaries and co-regencies are debated. <a href="sources.html#dates">How dates work ↗</a></p></section>`;
  }
  function chronologyChart() {
    const pct = y => (1050-y)/490*100;
    return `<div class="chronology-wrap" aria-label="Scrollable overview of royal reigns"><div class="chronology"><div class="year-axis">${[1050,1000,950,900,850,800,750,700,650,600,560].map(y=>`<span style="left:${pct(y)}%">${y}</span>`).join('')}</div>${[['united','United'],['israel','Israel'],['judah','Judah']].map(([realm,name])=>`<div class="realm-row ${realm==='judah'?'south':realm}"><span>${name}</span><div class="reign-track">${data.entries.filter(e=>e.reign?.realm===realm).map(e=>`<button class="reign-bar${e.id===state.selected?' selected':''}${e.id==='tibni'?' rival':''}" style="left:${pct(e.reign.start)}%;width:${Math.max(.6,(e.reign.start-e.reign.end)/490*100)}%" data-select="${e.id}" title="${esc(e.title+' · '+e.date)}" aria-label="${esc(e.title+' · '+e.date)}">${e.reign.start-e.reign.end >= 13 ? esc(e.title) : ''}</button>`).join('')}</div></div>`).join('')}<div class="year-needle" style="left:calc(90px + ${pct(state.year)} * 9.5px)"></div></div></div>`;
  }
  function rulerList() {
    const entries=data.entries.filter(e=>e.reign && (state.realm==='all' || e.reign.realm===state.realm));
    visibleIds=entries.map(e=>e.id);
    return entries.map(e=>`<button class="ruler-row${e.id===state.selected?' selected':''}${e.reign.start>=state.year && e.reign.end<=state.year?' current':''}" data-select="${e.id}"><span><strong>${esc(e.title)}</strong><small>${esc(e.date)}</small></span><span class="realm-dot ${e.reign.realm}" aria-label="${e.reign.realm==='israel'?'Israel':e.reign.realm==='judah'?'Judah':'United monarchy'}"></span></button>`).join('');
  }
  function renderKings() {
    return `<header class="view-title"><p class="eyebrow">TWO KINGDOMS. ONE SHARED HORIZON.</p><h3>Who was there at the same time?</h3><p>Move through the years, then open a ruler or prophet to follow the people and events around them.</p></header><div class="year-lens"><div class="year-title"><label for="year-range">THE YEAR LENS</label><output id="year-output" for="year-range">${state.year} BCE</output></div><input id="year-range" type="range" min="560" max="1050" step="1" value="${state.year}" dir="rtl" aria-label="Explore a year before the common era" aria-valuetext="${state.year} BCE"><div class="range-labels"><span>1050 BCE</span><span>560 BCE</span></div><div class="year-presets"><button data-year="855">Ahab’s world</button><button data-year="701">The Assyrian crisis</button><button data-year="586">Jerusalem’s fall</button></div></div><div id="year-summary">${yearSummary()}</div>${chronologyChart()}<div class="ruler-list-head"><h4>The royal succession</h4><label><span class="sr-only">Filter royal succession by kingdom</span><select id="realm-select">${[['all','All kingdoms'],['united','United monarchy'],['israel','Israel'],['judah','Judah']].map(([id,label])=>`<option value="${id}" ${state.realm===id?'selected':''}>${label}</option>`).join('')}</select></label></div><div class="ruler-list" id="ruler-list">${rulerList()}</div>`;
  }
  function updateYear(year, saveHash = true) {
    state.year=Math.max(560,Math.min(1050,Number(year)));
    const range=$('#year-range');
    if (!range) return;
    range.value=state.year;range.setAttribute('aria-valuetext',`${state.year} BCE`);
    $('#year-output').textContent=`${state.year} BCE`;
    $('#year-summary').innerHTML=yearSummary();
    $('#ruler-list').innerHTML=rulerList();
    const needle=$('.year-needle');if(needle)needle.style.left=`calc(90px + ${(1050-state.year)/490*100} * 9.5px)`;
    if(saveHash)writeHash(true);
  }
  function svgLabel(title,x,y) {
    if(title.length<=20)return `<text x="${x}" y="${y+5}" text-anchor="middle">${esc(title)}</text>`;
    const words=title.split(' ');let first='';
    while(words.length && first.length+words[0].length<21)first+=(first?' ':'')+words.shift();
    return `<text x="${x}" y="${y-3}" text-anchor="middle"><tspan x="${x}">${esc(first)}</tspan><tspan x="${x}" dy="17">${esc(words.join(' '))}</tspan></text>`;
  }
  function renderFamily() {
    const f=data.families.find(x=>x.id===state.family),nodes=new Map(f.nodes.map(n=>[n.id,n])),height=Math.max(...f.nodes.map(n=>n.y))+75;
    visibleIds=f.nodes.map(n=>n.id);
    const edges=f.edges.map(edge=>{
      const a=nodes.get(edge.source),b=nodes.get(edge.target);let d;
      if(Math.abs(a.y-b.y)<30)d=`M${a.x+(a.x<b.x?78:-78)} ${a.y}L${b.x+(a.x<b.x?-78:78)} ${b.y}`;
      else {const y=(a.y+b.y)/2;d=`M${a.x} ${a.y+23}C${a.x} ${y},${b.x} ${y},${b.x} ${b.y-23}`;}
      return `<path class="tree-edge ${edge.kind}" d="${d}"><title>${esc(byId.get(a.id).title)} → ${esc(byId.get(b.id).title)}: ${edge.kind==='parent'?'parent to child':edge.kind==='spouse'?'marriage':'later descendant; generations omitted'}</title></path>`;
    }).join('');
    return `<header class="view-title"><p class="eyebrow">BEHIND EVERY KINGDOM, A FAMILY.</p><h3>Meet the people inside the promise.</h3><p>${esc(f.description)}</p></header><div class="diagram-toolbar"><label>Family<select id="family-select">${data.families.map(x=>`<option value="${x.id}" ${x.id===f.id?'selected':''}>${esc(x.title)}</option>`).join('')}</select></label><div class="diagram-actions"><button class="icon-button" data-family-zoom="-0.25" aria-label="Zoom out of family tree">−</button><button class="icon-button" data-family-zoom="0.25" aria-label="Zoom into family tree">+</button><button class="icon-button" data-family-reset aria-label="Reset family tree zoom">↺</button></div></div><div class="diagram-scroll" data-diagram="${f.id}" tabindex="0" aria-label="Family diagram. Scroll to explore; select a person to read their story."><svg class="family-svg" viewBox="0 0 1220 ${height}" style="width:${state.familyZoom*100}%;max-width:none" role="group" aria-label="${esc(f.title)} family tree"><title>${esc(f.title)}</title>${edges}${f.nodes.map(n=>`<g class="tree-node${n.id===state.selected?' selected':''}" data-select="${n.id}" role="button" tabindex="0" aria-label="Open ${esc(byId.get(n.id).title)}"><rect x="${n.x-78}" y="${n.y-23}" width="156" height="46" rx="8"/>${svgLabel(byId.get(n.id).title,n.x,n.y)}</g>`).join('')}</svg></div><div class="diagram-legend"><span>Parent → child</span><span class="spouse">Marriage</span><span class="descendant">Generations omitted</span></div><p class="map-note">These are selected genealogies, not exhaustive family records. ${f.id==='tribes'?'Each column groups children under their named mother; Jacob is the father of every child shown.':''} Use + to enlarge, and scroll within the diagram.</p>${referenceButtons(f.refs)}<details class="detail-section"><summary>Text version of these relationships</summary><ul>${f.edges.map(e=>`<li class="map-note">${esc(byId.get(e.source).title)} ${e.kind==='parent'?'is a parent of':e.kind==='spouse'?'is married to':'is an ancestor, with intervening generations, of'} ${esc(byId.get(e.target).title)}.</li>`).join('')}</ul></details>`;
  }
  const project = p => [(p.lon-24)*40,(40-p.lat)*40];
  function mapSvg() {
    const selected=byId.get(state.selected),related=new Set(selected.places),major=['egypt','jerusalem','samaria','nineveh','babylon','ur','haran'];
    const route=selected.places.map(id=>project(placeById.get(id)).join(',')).join(' ');
    return `<svg class="map-svg" viewBox="0 0 1000 600" style="width:${state.mapZoom*100}%;max-width:none" role="group" aria-label="Map of the eastern Mediterranean and Near East; select a place to explore its stories"><title>The Scripture atlas</title><defs><clipPath id="map-clip"><rect width="1000" height="600"/></clipPath></defs><g clip-path="url(#map-clip)"><rect width="1000" height="600" fill="#172d35"/>${Array.from({length:11},(_,i)=>`<path class="map-grid" d="M${i*100} 0V600M0 ${i*100}H1000"/>`).join('')}${land.map(d=>`<path class="map-land" d="${esc(d)}"/>`).join('')}<text class="map-water-label" x="95" y="240" transform="rotate(-18 95 240)">MEDITERRANEAN SEA</text><text class="map-region" x="650" y="275" transform="rotate(25 650 275)">MESOPOTAMIA</text><text class="map-region" x="470" y="480">ARABIAN DESERT</text>${selected.places.length>1?`<polyline class="map-route" points="${route}"/>`:''}${data.places.map(p=>{
      const [x,y]=project(p),active=p.id===state.mapPlace,connected=related.has(p.id),label=active||major.includes(p.id);
      return `<g class="map-pin${active?' active':''}${connected?' related':''}" data-place="${p.id}" tabindex="0" role="button" aria-label="Explore ${esc(p.name)}${p.uncertain?', approximate or debated location':''}"><title>${esc(p.name)}${p.uncertain?' · approximate / debated':''}</title><circle class="pin-halo" cx="${x}" cy="${y}" r="${active?17:12}"/><circle cx="${x}" cy="${y}" r="${active?6:connected?4.5:3.5}"/>${label?`<text x="${x+10}" y="${y+(p.id==='samaria'?-12:4)}">${esc(p.name)}</text>`:''}</g>`;
    }).join('')}<g transform="translate(930 62)" stroke="#cfbc8b" opacity=".8"><circle r="24" fill="#172d35"/><path d="M0-30V30M-30 0H30M0-18L5 0L0 18L-5 0Z"/><text x="0" y="-36" text-anchor="middle" fill="#cfbc8b" stroke="none" font-size="11">N</text></g></g></svg>`;
  }
  function placeCard() {
    const p=placeById.get(state.mapPlace),entries=data.entries.filter(e=>e.places.includes(p.id));
    visibleIds=entries.map(e=>e.id);
    return `<section class="map-place-card"><p class="eyebrow">${p.uncertain?'APPROXIMATE / DEBATED LOCATION':'A PLACE IN THE STORY'}</p><h4>${esc(p.name)}</h4><p>${esc(p.description)}</p><div class="connection-list">${entries.map(connectionLink).join('') || '<p>No linked entry yet.</p>'}</div></section>`;
  }
  function renderMap() {
    const e=byId.get(state.selected);
    return `<header class="view-title"><p class="eyebrow">THE STORY HAS A LANDSCAPE.</p><h3>Put a place to the name.</h3><p>Explore the lands around the biblical story. Green pins belong to the selected entry; gold pins open other places.</p></header><div class="diagram-toolbar"><label>Place<select id="place-select">${[...data.places].sort((a,b)=>a.name.localeCompare(b.name)).map(p=>`<option value="${p.id}" ${p.id===state.mapPlace?'selected':''}>${esc(p.name)}${p.uncertain?' ≈':''}</option>`).join('')}</select></label><div class="diagram-actions"><button class="icon-button" data-map-zoom="-0.25" aria-label="Zoom out of map">−</button><button class="icon-button" data-map-zoom="0.25" aria-label="Zoom into map">+</button><button class="icon-button" data-map-reset aria-label="Reset map zoom">↺</button></div></div><div class="diagram-scroll" data-diagram="map" id="map-scroll" tabindex="0" aria-label="Scrollable map">${mapSvg()}</div><div class="map-footer"><span>≈ Approximate or debated identification</span><span>Base map: Natural Earth</span></div><p class="map-note">${e.places.length>1?`Dashed lines connect places named in “${esc(e.title)}.” They are not reconstructed travel routes.`:e.places.length===0?`“${esc(e.title)}” has no securely mapped place in this atlas. Explore another story through the pins.`:'Select a pin to see the stories connected with it.'} No modern political borders are shown.</p><div id="place-card">${placeCard()}</div>`;
  }
  function render() {
    const oldDiagram=$('.diagram-scroll'),oldScroll=oldDiagram?{key:oldDiagram.dataset.diagram,left:oldDiagram.scrollLeft,top:oldDiagram.scrollTop}:null;
    $$('.view-switch button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===state.view)));
    $('#entry-count').textContent=`${data.entries.length} entries · ${data.places.length} places`;
    const primary={story:renderStory,kings:renderKings,families:renderFamily,map:renderMap}[state.view]();
    $('#workspace').innerHTML=`<div class="primary-pane">${primary}</div>${renderDetail()}`;
    $('#workspace').setAttribute('aria-busy','false');
    const newDiagram=$('.diagram-scroll');
    if(oldScroll && newDiagram && newDiagram.dataset.diagram===oldScroll.key){newDiagram.scrollLeft=oldScroll.left;newDiagram.scrollTop=oldScroll.top;}
    renderTrailBanner();
  }
  function selectEntry(id,{scroll=true,history=true}={}) {
    if(!byId.has(id))return;
    state.selected=id;
    const e=byId.get(id);
    if(state.view==='kings' && e.reign && !(e.reign.start>=state.year && e.reign.end<=state.year))state.year=Math.round((e.reign.start+e.reign.end)/2);
    if(state.view==='story' && !state.query && !state.trail){state.era=e.era;state.filter='all';state.savedOnly=false;}
    render();if(history)writeHash();
    announce(`${e.title}. ${kindNames[e.kind]} in ${eraName(e.era)}. Details and passages opened.`);
    if(scroll && mobile()){
      const panel=$('#detail-panel');panel.scrollIntoView({behavior:motion(),block:'start'});panel.focus({preventScroll:true});
    }else if(scroll)$('#detail-panel').focus({preventScroll:true});
  }
  function setView(view) {
    state.view=view;state.query='';$('#search').value='';state.savedOnly=false;
    if(view==='map'){
      const p=byId.get(state.selected).places;
      if(p.length)state.mapPlace=p[0];
    }
    render();writeHash();announce(`${view==='story'?'Story':view==='kings'?'Kings and prophets':view==='families'?'Family trees':'Atlas'} view opened.`);
  }
  function startTrail(id) {
    const t=data.trails.find(x=>x.id===id);if(!t)return;
    state.trail=id;state.view='story';state.query='';state.savedOnly=false;state.filter='all';$('#search').value='';state.selected=t.steps[0];state.era=byId.get(state.selected).era;
    render();writeHash();$('#explore').scrollIntoView({behavior:motion(),block:'start'});announce(`${t.title}. A guided journey with ${t.steps.length} stops.`);
  }
  function moveTrail(delta) {
    const t=data.trails.find(x=>x.id===state.trail);if(!t)return;
    const current=t.steps.indexOf(state.selected),i=Math.max(0,Math.min(t.steps.length-1,current+delta));
    selectEntry(t.steps[i]);
  }
  function updatePlace(id, push=true) {
    if(!placeById.has(id))return;
    state.mapPlace=id;
    const scroll=$('#map-scroll'),left=scroll?.scrollLeft||0,top=scroll?.scrollTop||0;
    if(scroll){scroll.innerHTML=mapSvg();scroll.scrollLeft=left;scroll.scrollTop=top;}
    if($('#place-select'))$('#place-select').value=id;
    if($('#place-card'))$('#place-card').innerHTML=placeCard();
    if(push)writeHash();announce(`Map: ${placeById.get(id).name}. Connected stories are listed below the map.`);
  }
  function originalUrl(code,chapter) {
    if(code==='ENO')return 'https://www.gutenberg.org/ebooks/77935';
    if(code==='JUB')return 'https://wesley.nnu.edu/sermons-essays-books/noncanonical-literature/noncanonical-literature-ot-pseudepigrapha/the-book-of-jubilees/';
    return `https://ebible.org/eng-web/${code}${String(chapter).padStart(2,'0')}.htm`;
  }
  function verseInRange(verse,range) {
    if(!range)return false;
    return range.split(',').some(part=>{const [a,b]=part.trim().split(/[-–]/).map(Number);return Number(verse)>=a&&Number(verse)<=(b||a);});
  }
  async function openReader(code='GEN',chapter=1,verses='') {
    if(!books[code])return;
    if(!books[code].chapters.includes(Number(chapter)))chapter=books[code].chapters[0];
    const token=++readerToken,dialog=$('#reader');
    $('#reader-book').value=code;
    $('#reader-chapter').innerHTML=books[code].chapters.map(c=>`<option value="${c}" ${c===Number(chapter)?'selected':''}>${c}</option>`).join('');
    const i=books[code].chapters.indexOf(Number(chapter));
    $('#reader-prev').disabled=i===0;$('#reader-next').disabled=i===books[code].chapters.length-1;
    $('#reader-title').textContent=refLabel({book:code,chapter,verses});
    $('#reader-edition').textContent=books[code].edition;
    $('#reader-original').href=originalUrl(code,chapter);
    $('#reader-content').innerHTML='<p class="reader-help">Opening the text…</p>';
    $('#reader-content').setAttribute('aria-busy','true');
    if(!dialog.open)dialog.showModal();
    dialog.scrollTop=0;
    try {
      if(!bookCache.has(code))bookCache.set(code,getJson(`texts/${code}.json`));
      const book=await bookCache.get(code);if(token!==readerToken)return;
      const content=book.chapters[String(chapter)];
      if(content===undefined)throw new Error('This chapter is not present in the reading text.');
      let markup;
      if(book.format==='verses'){
        const notes=book.textualNotes?.[String(chapter)]||{};
        const numbers=[...new Set([...Object.keys(content),...Object.keys(notes)])].sort((a,b)=>Number(a)-Number(b));
        markup=numbers.map(number=>content[number] ? `<p class="verse${verseInRange(number,verses)?' highlight':''}" id="reader-v${esc(number)}"><span class="verse-num">${esc(number)}</span>${esc(content[number])}</p>` : `<aside class="reader-help edition-variant"><strong>Edition note at verse ${esc(number)}</strong><p>${esc(notes[number])}</p></aside>`).join('');
      }else{
        markup=`<p class="reader-help">Full chapter in the named historical translation. Inline numbers and critical marks follow that edition; they are not modern commentary.</p><div class="prose-text">${esc(content)}</div>`;
      }
      $('#reader-content').innerHTML=markup;
      $('#reader-content').setAttribute('aria-busy','false');
      if(verses && book.format==='verses')requestAnimationFrame(()=>$('.verse.highlight')?.scrollIntoView({block:'center',behavior:'auto'}));
    }catch(error){
      bookCache.delete(code);
      if(token!==readerToken)return;
      $('#reader-content').innerHTML=`<div class="reader-error"><p>This text could not be opened. You can retry or read the source edition.</p><button class="outline-button" data-read="${esc(code)}" data-chapter="${Number(chapter)}" data-verses="${esc(verses)}">Try again</button> <a href="${esc(originalUrl(code,chapter))}" target="_blank" rel="noopener">Open source edition ↗</a></div>`;
      $('#reader-content').setAttribute('aria-busy','false');
    }
  }
  function stepReader(delta) {
    const code=$('#reader-book').value,chapters=books[code].chapters,index=chapters.indexOf(Number($('#reader-chapter').value));
    if(chapters[index+delta])openReader(code,chapters[index+delta]);
  }
  async function share() {
    writeHash(true);
    try{await navigator.clipboard.writeText(location.href);announce('Link copied. It will reopen this entry and view.');const b=$('[data-share]');if(b){b.textContent='✓';b.setAttribute('aria-label','Link copied');}}
    catch{announce('The address bar now contains the link to this entry. Copy it to share this view.');const b=$('[data-share]');if(b){b.textContent='URL';b.title='Copy the page address to share this entry';}}
  }
  function bind() {
    document.addEventListener('click',event=>{
      const button=event.target.closest('button,[data-select],[data-place]');if(!button)return;
      const d=button.dataset;
      if(d.view)return setView(d.view);
      if(d.select)return selectEntry(d.select);
      if(d.trail)return startTrail(d.trail);
      if(d.trailStep)return moveTrail(Number(d.trailStep));
      if('endTrail' in d){state.trail=null;render();writeHash();return;}
      if(d.era){state.era=d.era;state.query='';$('#search').value='';state.savedOnly=false;state.trail=null;state.filter='all';render();writeHash();return;}
      if(d.filter){state.filter=d.filter;state.trail=null;render();announce(`${visibleIds.length} entries shown.`);return;}
      if('savedOnly' in d){state.savedOnly=!state.savedOnly;state.era='all';state.trail=null;state.query='';$('#search').value='';state.filter='all';render();return;}
      if(d.save){
        saved=saved.includes(d.save)?saved.filter(x=>x!==d.save):[...saved,d.save];
        try{localStorage.setItem('bb-atlas-saved-v1',JSON.stringify(saved));}catch{persistentStorage=false;}
        render();announce(`${byId.get(d.save).title} ${saved.includes(d.save)?(persistentStorage?'saved':'saved for this visit only; persistent storage is unavailable'):'removed from saved entries'}.`);return;
      }
      if('share' in d)return void share();
      if(d.read)return void openReader(d.read,Number(d.chapter),d.verses||'');
      if(d.mapPlace){state.view='map';state.mapPlace=d.mapPlace;state.query='';$('#search').value='';render();writeHash();$('#explore').scrollIntoView({behavior:motion(),block:'start'});return;}
      if(d.place)return updatePlace(d.place);
      if(d.year)return updateYear(d.year);
      if(d.entryStep){const i=visibleIds.indexOf(state.selected)+Number(d.entryStep);if(visibleIds[i])selectEntry(visibleIds[i]);return;}
      if('resetSearch' in d){state.query='';state.filter='all';state.savedOnly=false;state.trail=null;state.era='beginnings';$('#search').value='';render();return;}
      if('backList' in d){$('#explore').scrollIntoView({behavior:motion(),block:'start'});return;}
      if('mapZoom' in d || 'mapReset' in d){state.mapZoom='mapReset' in d?1:Math.max(.75,Math.min(3,state.mapZoom+Number(d.mapZoom)));const s=$('.map-svg');if(s)s.style.width=`${state.mapZoom*100}%`;return;}
      if('familyZoom' in d || 'familyReset' in d){state.familyZoom='familyReset' in d?1:Math.max(.75,Math.min(2.5,state.familyZoom+Number(d.familyZoom)));const s=$('.family-svg');if(s)s.style.width=`${state.familyZoom*100}%`;return;}
    });
    document.addEventListener('change',event=>{
      if(event.target.id==='family-select'){state.family=event.target.value;state.familyZoom=1;render();writeHash();}
      if(event.target.id==='place-select')updatePlace(event.target.value);
      if(event.target.id==='realm-select'){state.realm=event.target.value;$('#ruler-list').innerHTML=rulerList();}
      if(event.target.id==='reader-book')void openReader(event.target.value,books[event.target.value].chapters[0]);
      if(event.target.id==='reader-chapter')void openReader($('#reader-book').value,Number(event.target.value));
    });
    document.addEventListener('input',event=>{if(event.target.id==='year-range')updateYear(event.target.value);});
    let searchTimer;
    $('#search').addEventListener('input',event=>{
      clearTimeout(searchTimer);const value=event.target.value;
      searchTimer=setTimeout(()=>{state.query=value;state.view='story';state.trail=null;state.savedOnly=false;render();announce(`${visibleIds.length} search results.`);},150);
    });
    $('#show-trails').addEventListener('click',()=>{state.showAllTrails=!state.showAllTrails;renderTrails();});
    $('#open-library').addEventListener('click',()=>void openReader('GEN',1));
    $('#close-reader').addEventListener('click',()=>$('#reader').close());
    $('#reader-prev').addEventListener('click',()=>stepReader(-1));
    $('#reader-next').addEventListener('click',()=>stepReader(1));
    $('#reader').addEventListener('click',event=>{if(event.target===$('#reader')){const rect=event.target.getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)event.target.close();}});
    $('#reader').addEventListener('close',()=>{readerToken++;});
    document.addEventListener('keydown',event=>{
      const typing=event.target.closest('input,select,textarea,[contenteditable=true]');
      if(event.key==='/'&&!typing&&!$('#reader').open){event.preventDefault();$('#search').focus();}
      if((event.key==='Enter'||event.key===' ')&&event.target.matches('g[data-select],g[data-place]')){event.preventDefault();event.target.dispatchEvent(new MouseEvent('click',{bubbles:true}));}
    });
    window.addEventListener('popstate',()=>{state.query='';state.filter='all';state.savedOnly=false;$('#search').value='';readHash();render();});
  }
  async function init() {
    try {
      [data,books,land]=await Promise.all([getJson('data.json'),getJson('texts/index.json'),getJson('assets/land.json')]);
      byId=new Map(data.entries.map(e=>[e.id,e]));placeById=new Map(data.places.map(p=>[p.id,p]));eraById=new Map(data.eras.map(e=>[e.id,e]));
      saved=saved.filter(id=>byId.has(id));
      $('#reader-book').innerHTML=Object.entries(books).sort(([a,x],[b,y])=>{if(a==='ENO')return -1;if(b==='ENO')return 1;if(a==='JUB')return -1;if(b==='JUB')return 1;return x.title.localeCompare(y.title);}).map(([code,b])=>`<option value="${esc(code)}">${esc(b.title)}</option>`).join('');
      readHash();renderTrails();render();bind();
      if(location.hash.includes('entry='))$('#explore').scrollIntoView({block:'start',behavior:'auto'});
    }catch(error){
      $('#workspace').setAttribute('aria-busy','false');
      $('#workspace').innerHTML='<div class="loading-card"><h3>The atlas could not be opened.</h3><p>Please reload to try again. The Bible index and source notes are still available.</p><button class="gold-button" id="reload-atlas">Reload the atlas</button> <a href="../bibleindex/">Open Bible index</a></div>';
      $('#reload-atlas').addEventListener('click',()=>location.reload());
      console.error('BibleBucket atlas startup:',error);
    }
  }
  void init();
})();
