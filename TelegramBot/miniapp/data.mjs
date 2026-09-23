// Entirely synthetic UI fixtures. Never client records or Telegram identity data.
export const events = [
  { id:'DEMO-001', src:'192831', dst:'240518', score:94, level:'critical', cluster:3, time:'15:42', pattern:'consolidation', incoming:14, outgoing:2 },
  { id:'DEMO-002', src:'305712', dst:'192831', score:82, level:'high', cluster:3, time:'15:36', pattern:'transit', incoming:8, outgoing:7 },
  { id:'DEMO-003', src:'740291', dst:'305712', score:67, level:'medium', cluster:7, time:'15:21', pattern:'distribution', incoming:2, outgoing:11 },
  { id:'DEMO-004', src:'240518', dst:'518204', score:42, level:'low', cluster:3, time:'14:58', pattern:'terminal', incoming:4, outgoing:1 },
  { id:'DEMO-005', src:'518204', dst:'862019', score:18, level:'minimal', cluster:7, time:'14:40', pattern:'peripheral', incoming:1, outgoing:1 },
];
export const nodes = [
  {gid:'192831',x:280,y:170,r:28,level:'critical'},
  {gid:'305712',x:140,y:112,r:20,level:'high'},
  {gid:'740291',x:100,y:260,r:19,level:'medium'},
  {gid:'240518',x:433,y:105,r:22,level:'low'},
  {gid:'518204',x:455,y:270,r:19,level:'minimal'},
  {gid:'862019',x:290,y:327,r:16,level:'minimal'},
];
export function selectEvents({filter='all',query='',reviewed=new Set()}={}) {
  const term = query.trim().toLowerCase();
  return events.filter(e => (filter==='all' || (filter==='high' && e.score>=80) || (filter==='reviewed' && reviewed.has(e.id))) &&
    (!term || [e.src,e.dst,e.id].some(v=>v.toLowerCase().includes(term))));
}
export const colors = {critical:'#ed7e91',high:'#e9aa70',medium:'#d7c775',low:'#74b49b',minimal:'#72bace'};
