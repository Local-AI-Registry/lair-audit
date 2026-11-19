// The first screen ships as plain HTML (_build/find-shell.html, captured from vFind) so its headline paints before the script
// runs. This fails if that HTML no longer matches what the script draws: then re-capture it (see the note printed below).
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();let bad=0;
for(const vp of [{width:1440,height:900},{width:390,height:844}]){const p=await b.newPage({viewport:vp});
 await p.goto('http://localhost:9314/ai-audit/');await p.waitForTimeout(900);
 const r=await p.evaluate(()=>{const norm=h=>h.replace(/\s+/g,' ').trim(),pick=root=>['.home2','.seen2'].map(s=>{const e=root.querySelector(s);return e?norm(e.outerHTML):''}).join('');
  const t=document.createElement('div');t.innerHTML=document.getElementById('fshell').innerHTML;return {shell:pick(t),live:pick(document.getElementById('stage'))}});
 if(r.shell!==r.live){bad++;let i=0;while(i<r.shell.length&&r.shell[i]===r.live[i])i++;
  console.log('DRIFT at',vp.width+'px: shell "…'+r.shell.slice(Math.max(0,i-60),i+80)+'…"\n  live  "…'+r.live.slice(Math.max(0,i-60),i+80)+'…"')}
 await p.close()}
if(bad)console.log('Re-capture: open /ai-audit/ (no team key, no query), copy #stage innerHTML into _build/find-shell.html, rebuild.');
console.log(bad?'shell: DRIFTED':'shell: matches');await b.close();process.exit(bad?1:0)})();
