// Main page at several window sizes: desktop sizes must fit with nothing cut off; phones must not scroll sideways.
const {chromium,devices}=require('playwright');(async()=>{const b=await chromium.launch();const errs=[];let bad=0;
const U='http://localhost:9314/ai-audit/',D=__dirname+'/shots/';const slugs=process.argv.slice(2);
const CH=[['scan',1],['score',3],['ask',2],['checks',2],['why',1],['plan',3]];
for(const [w,h] of [[1440,900],[1920,1080],[1366,768],[1280,1024],[2560,1080]]){const p=await b.newPage({viewport:{width:w,height:h}});p.on('pageerror',e=>errs.push(e.message));
 for(const s of slugs)for(const [ch,n] of CH){await p.goto(U+'?b='+s+'&w='+w+'#'+ch);await p.waitForTimeout(ch==='scan'?2600:450);
  for(let k=0;k<n;k++){await p.waitForTimeout(400);const o=await p.evaluate(()=>{const r=[];document.querySelectorAll('#stage .card,#stage .body,#stage .sp').forEach(c=>{if(c.scrollHeight>c.clientHeight+3&&!c.classList.contains('track'))r.push((c.className||'').slice(0,30)+':'+(c.scrollHeight-c.clientHeight))});const W=innerWidth,H=innerHeight;document.querySelectorAll('#stage *').forEach(e=>{const q=e.getBoundingClientRect();if(q.width&&(q.right>W+2||q.bottom>H+2)&&!e.closest('.track,.map,.feed,.pan,.tblw,.fwrap'))r.push('out:'+e.tagName+'.'+String(e.className.baseVal??e.className).slice(0,24))});return r.slice(0,4)});
   if(o.length){bad++;console.log(w+'x'+h,s,ch,k,o)}if(s===slugs[0]&&(w===1920||w===1280)&&k===n-1)await p.screenshot({path:D+'r-'+w+'-'+ch+'.png'});if(k<n-1)await p.keyboard.press('ArrowRight')}}
 await p.close()}
const m=await b.newPage({...devices['iPhone 13']});m.on('pageerror',e=>errs.push(e.message));
await m.goto(U);await m.waitForTimeout(600);await m.screenshot({path:D+'m-home.png'});
for(const s of slugs)for(const [ch,n] of CH){await m.goto(U+'?b='+s+'&m=1#'+ch);await m.waitForTimeout(ch==='scan'?2600:500);
 for(let k=0;k<n;k++){await m.waitForTimeout(350);const sw=await m.evaluate(()=>document.documentElement.scrollWidth-innerWidth);if(sw>1){bad++;console.log('phone',s,ch,k,'scrolls sideways by',sw)}
  if(s===slugs[0])await m.screenshot({path:D+'m-'+ch+k+'.png',fullPage:true});if(k<n-1)await m.evaluate(()=>document.querySelector('[data-nav="next"]').click())}}
console.log('problems',bad,'errors',errs.length?errs:'none');await b.close();process.exit(bad||errs.length?1:0)})();
