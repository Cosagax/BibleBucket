/* Release invariants: preserve the first atlas and distinguish the new layers. */
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const data=JSON.parse(fs.readFileSync(path.join(root,'data.json'),'utf8'));
// Hashes of the unchanged arrays in first release ecae063.
const original={
  eras:[7,'424f27a3dfb5b5206568bb8cdb6f2ffeb949de93482cee9d31130ce9302c3a06'],
  entries:[188,'951b275d44ba70e280031020ffac7c14ad87265baa04134b6b5ce5ac4a71c4f8'],
  places:[34,'efa09704253db5e8aa5829c16fa09fc56c07d2a51aa731869c7327ed00fbc85d'],
  families:[5,'7c71c010c8bdc68958d42ddb380bc7b773ed6c7fd56675593faf16f20d2eb650'],
  trails:[6,'9c6e0f5ad2d1187b014a59855e7050bb55e34b171cc402ab6738501f9d4cbb42'],
  prophetWindows:[17,'6c5e4bd5fc96aaca588b9a31f5eeb531e688c74ed6aaa0e54100ff600099c3b0']
};
for(const [key,[count,hash]] of Object.entries(original)){
  assert.equal(createHash('sha256').update(JSON.stringify(data[key].slice(0,count))).digest('hex'),hash,`Original ${key} changed`);
}
for(const key of ['eras','entries','places','families','trails'])assert.equal(new Set(data[key].map(e=>e.id)).size,data[key].length,`Duplicate ${key} IDs`);
const nt='MAT MRK LUK JHN ACT ROM 1CO 2CO GAL EPH PHP COL 1TH 2TH 1TI 2TI TIT PHM HEB JAS 1PE 2PE 1JN 2JN 3JN JUD REV'.split(' ');
const cited=new Set(data.entries.slice(188).flatMap(e=>e.refs.map(r=>r.book)));
for(const book of nt)assert(cited.has(book),`New Testament book not represented: ${book}`);
const jesusEras=['arrival','ministry','passion'];
assert(data.entries.filter(e=>jesusEras.includes(e.era)&&e.primary).length>=50,'Jesus must have substantial narrative coverage');
for(const e of data.entries.filter(e=>e.era==='revelation')){
  assert.equal(e.bce,null,'Visions cannot be assigned calendar dates');
  assert(e.refs.some(r=>r.book==='REV'),`${e.id}: Revelation passage needed`);
  assert.equal(e.reign,undefined,'Do not force visionary kingship onto the historical monarchy chart');
}
const family=data.families.find(f=>f.id==='jesus-household');
assert(family.edges.some(e=>e.source==='mary-jesus'&&e.target==='jesus'&&e.kind==='parent'));
assert(family.edges.some(e=>e.source==='joseph-nazareth'&&e.target==='jesus'&&e.kind==='guardian'));
assert(!family.edges.some(e=>e.source==='joseph-nazareth'&&e.target==='jesus'&&e.kind==='parent'));
const echoes=data.entries.filter(e=>e.echoes?.length);
assert(echoes.length>=20,'The textual-connection feature must have substantive coverage');
assert(data.entries.find(e=>e.id==='jude-enoch').refs.some(r=>r.book==='ENO'),'Do not lose the Enoch/New Testament link');
assert(data.places.some(p=>p.id==='rome'&&p.lon<24),'Mediterranean reach must include Rome');
assert(fs.existsSync(path.join(root,'assets/mediterranean-land.json')));
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
assert(html.includes('data-trail="jesus-story"'),'Jesus must be directly reachable from the landing page');
assert(html.includes('data-trail="revelation-echoes"'),'Revelation must be directly reachable from the landing page');
console.log(`PASS: first-release arrays unchanged; all 27 New Testament books cited; ${echoes.length} sourced echo panels; Jesus-centered coverage, genealogy distinctions, and undated visions preserved.`);
