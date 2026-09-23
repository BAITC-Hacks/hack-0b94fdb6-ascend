import test from 'node:test';
import assert from 'node:assert/strict';
import {events,nodes,selectEvents,colors} from './data.mjs';
import {copy} from './i18n.mjs';
import {paths,icon} from './icons.mjs';
test('all UI languages cover the same keys',()=>{
  for(const lang of ['kk','en']) assert.deepEqual(Object.keys(copy[lang]).sort(),Object.keys(copy.ru).sort());
  for(const dictionary of Object.values(copy)) assert.ok(Object.values(dictionary).every(value=>typeof value==='string'&&value.length>0));
});
test('synthetic connections reference valid nodes and translated explanations',()=>{
  assert.equal(new Set(events.map(e=>e.id)).size,events.length);
  for(const event of events){assert.ok(event.id.startsWith('DEMO-'));assert.ok(nodes.some(n=>n.gid===event.src));assert.ok(nodes.some(n=>n.gid===event.dst));assert.ok(colors[event.level]);assert.ok(paths[event.level]);assert.ok(copy.ru[event.pattern]);assert.ok(event.score>=0&&event.score<=100);}
});
test('priority, search and review filters combine',()=>{
  assert.equal(selectEvents().length,5);
  assert.equal(selectEvents({filter:'high'}).length,2);
  assert.equal(selectEvents({query:'192831'}).length,2);
  assert.equal(selectEvents({query:' demo-003 '})[0].id,'DEMO-003');
  assert.equal(selectEvents({query:'does-not-exist'}).length,0);
  const reviewed=new Set(['DEMO-001','DEMO-005']);
  assert.equal(selectEvents({filter:'reviewed',reviewed}).length,2);
  assert.equal(selectEvents({filter:'reviewed',query:'862019',reviewed}).length,1);
});
test('icons are accessible decorative SVG with no remote resources',()=>{
  for(const name of Object.keys(paths)){const svg=icon(name);assert.ok(svg.includes('aria-hidden="true"'));assert.ok(!svg.includes('https:'));assert.ok(svg.includes('currentColor'));}
});
