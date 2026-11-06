import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = name => JSON.parse(fs.readFileSync(path.join(root, name), 'utf8'));
const data = read('data.json'), manifest = read('texts/index.json');
const ids = new Set(data.entries.map(x => x.id)), places = new Set(data.places.map(x => x.id));
assert.equal(ids.size, data.entries.length, 'Entity IDs must be unique');
const books = new Map(Object.keys(manifest).map(id => [id, read(`texts/${id}.json`)]));
let referenceCount = 0;
function checkRef(ref, owner) {
  referenceCount++;
  const b = books.get(ref.book);
  assert(b, `${owner}: missing reading text ${ref.book}`);
  const chapter = b.chapters[String(ref.chapter)];
  assert(chapter, `${owner}: missing chapter ${ref.book} ${ref.chapter}`);
  if (ref.verses && b.format === 'verses') {
    for (const part of ref.verses.split(',')) {
      const [a, end] = part.trim().split(/[-–]/).map(Number), z = end || a;
      assert(a > 0 && z >= a, `${owner}: malformed verse range`);
      for (let n = a; n <= z; n++) assert(chapter[String(n)], `${owner}: missing verse ${ref.book} ${ref.chapter}:${n}`);
    }
  }
}
for (const e of data.entries) {
  assert(e.summary.trim().length > 50, `${e.id}: substantive summary required`);
  assert(e.refs.length, `${e.id}: primary reference required`);
  assert(data.eras.some(x => x.id === e.era), `${e.id}: unknown era`);
  for (const id of e.related) assert(ids.has(id) && id !== e.id, `${e.id}: invalid connection ${id}`);
  for (const id of e.places) assert(places.has(id), `${e.id}: unknown place ${id}`);
  for (const ref of e.refs) checkRef(ref,e.id);
  if (['beginnings','patriarchs','exodus','land'].includes(e.era)) assert(e.bce === null, `${e.id}: early narrative must not acquire a fabricated BCE date`);
  if (e.reign) assert(e.reign.start >= e.reign.end, `${e.id}: reversed reign`);
}
for (const f of data.families) {
  const nodes = new Set(f.nodes.map(n=>n.id));
  assert.equal(nodes.size,f.nodes.length,`${f.id}: duplicate person in tree`);
  for(const id of nodes) assert(ids.has(id),`${f.id}: person missing`);
  const children = new Map();
  for(const edge of f.edges) {
    assert(nodes.has(edge.source) && nodes.has(edge.target),`${f.id}: dangling relationship`);
    assert(['parent','spouse','descendant'].includes(edge.kind));
    if(edge.kind !== 'spouse') children.set(edge.source,[...(children.get(edge.source)||[]),edge.target]);
  }
  function walk(id, trail = new Set()) {
    assert(!trail.has(id),`${f.id}: ancestry cycle at ${id}`);
    const next = new Set([...trail,id]);
    for(const child of children.get(id)||[]) walk(child,next);
  }
  for(const id of nodes) walk(id);
  for(const ref of f.refs) checkRef(ref,f.id);
}
for(const t of data.trails) for(const id of t.steps) assert(ids.has(id),`${t.id}: broken stop`);
for(const p of data.prophetWindows) assert(ids.has(p.id) && p.start>=p.end,`Bad prophet window ${p.id}`);
for(const p of data.places) assert(p.lon>=24 && p.lon<=49 && p.lat>=25 && p.lat<=40,`${p.id}: pin outside map`);
assert.equal(Object.keys(books.get('ENO').chapters).length,108);
assert.equal(Object.keys(books.get('JUB').chapters).length,50);
assert(books.get('ENO').chapters['6'].includes('Hermon'));
assert(books.get('JUB').chapters['10'].includes('Mastema'));
assert(!books.get('ENO').chapters['108'].includes('Transcriber'));
assert(books.get('ENO').chapters['91'].includes('the eighth week'), 'The relocated 91:12–17 fragment must be assigned to chapter 91');
assert(!books.get('ENO').chapters['93'].includes('the eighth week'), 'Do not silently misnumber the relocated fragment');
assert(!books.get('JUB').chapters['50'].includes('Wesley Center'));
assert.equal(books.get('GEN').chapters['1']['1'],'In the beginning, God created the heavens and the earth.');
assert.equal(books.get('REV').chapters['22']['21'],'The grace of the Lord Jesus Christ be with all the saints. Amen.');
assert(books.get('ACT').textualNotes?.['8']?.['37']?.includes('TR adds'), 'Footnote-only verses must retain their edition note');
for(const [code,book] of books) {
  assert.deepEqual(Object.keys(book.chapters).map(Number).sort((a,b)=>a-b),manifest[code].chapters,`${code}: manifest mismatch`);
  for(const [chapter,text] of Object.entries(book.chapters)) {
    if(book.format==='verses') for(const [verse,value] of Object.entries(text)) assert(value.trim(),`${code} ${chapter}:${verse} is empty`);
    else assert(text.trim().length>20,`${code} ${chapter} is empty`);
  }
}
for(const file of ['index.html','sources.html']) {
  const html=fs.readFileSync(path.join(root,file),'utf8');
  for(const match of html.matchAll(/(?:src|href)="([^"#]+)"/g)) {
    const url=match[1];if(/^[a-z]+:/i.test(url))continue;
    assert(fs.existsSync(path.resolve(root,url)),`${file}: broken local asset/link ${url}`);
  }
}
assert(fs.readFileSync(path.join(root,'../index.html'),'utf8').includes('href="timeline/"'),'Homepage link missing');
console.log(`PASS: ${data.entries.length} entries, ${referenceCount} primary references, ${data.families.length} acyclic family trees, ${data.places.length} map locations, ${data.trails.length} complete trails, ${books.size} reading texts, and local asset paths.`);
