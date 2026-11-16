// Clicks through every chapter of ai-audit/v2 for each business: no script errors, nothing spilling out of its card.
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:810}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error'&&!/fonts|ERR_/.test(m.text()))errs.push(m.text())});
const D=__dirname+'/shots/';const U='http://localhost:9314/ai-audit/v2/';let bad=0;
const over=()=>p.evaluate(()=>{const o=[];document.querySelectorAll('#stage .card,#stage .body,#stage .sp').forEach(c=>{if(c.scrollHeight>c.clientHeight+3&&getComputedStyle(c).overflowY!=='auto'&&!c.classList.contains('track'))o.push((c.className||'').slice(0,40)+':'+(c.scrollHeight-c.clientHeight))});const s=document.querySelector('#stage').getBoundingClientRect();document.querySelectorAll('#stage *').forEach(e=>{const r=e.getBoundingClientRect();if(r.width&&(r.right>s.right+2||r.bottom>s.bottom+2)&&!e.closest('.track,.map,.feed,.scan4 .pan'))o.push('out:'+e.tagName+'.'+(e.className.baseVal??e.className).toString().slice(0,30))});return o.slice(0,5)});
await p.goto(U);await p.waitForTimeout(800);await p.fill('#q','spirit');await p.waitForTimeout(300);console.log('home sug',await p.$$eval('#sug li',l=>l.length));await p.screenshot({path:D+'v2-home.png'});await p.click('#sug li[data-i="0"]');await p.waitForTimeout(600);console.log('picked',await p.evaluate(()=>location.search+location.hash),await p.$eval('.sp',e=>e.innerText.split('\n')[2]));
const slugs=process.argv.slice(2);
for(const s of slugs){
 await p.goto(U+'?b='+s+'#scan');await p.waitForTimeout(2600);let o=await over();if(o.length){bad++;console.log(s,'scan',o)}
 if(s===slugs[0])await p.screenshot({path:D+'v2-scan.png'});
 for(const [ch,n] of [['score',3],['ask',2],['checks',2],['why',1],['plan',1]]){
  await p.goto(U+'?b='+s+'&t='+ch+'#'+ch);await p.waitForTimeout(500);
  for(let k=0;k<n;k++){await p.waitForTimeout(450);o=await over();if(o.length){bad++;console.log(s,ch,k,o)}if(s===slugs[0]||s==='esthetixmd-bend')await p.screenshot({path:D+'v2-'+s.split('-')[0]+'-'+ch+k+'.png'});if(k<n-1)await p.keyboard.press('ArrowRight')}
 }
 await p.goto(U+'?b='+s+'&t=x#checks');await p.waitForTimeout(300);await p.keyboard.press('ArrowRight');for(let i=0;i<11;i++){await p.$eval('#stage .nd[data-i="'+i+'"]',n=>n.dispatchEvent(new MouseEvent('click',{bubbles:true})));await p.waitForTimeout(80);const o2=await over();if(o2.length){bad++;console.log(s,'check',i,o2)}}
 await p.goto(U+'?b='+s+'&t=y#score');await p.waitForTimeout(300);await p.click('#stage [data-info]');await p.waitForTimeout(300);if(s===slugs[0]||s==='esthetixmd-bend')await p.screenshot({path:D+'v2-'+s.split('-')[0]+'-pop.png'});
}
await p.goto(U+'?b='+slugs[0]+'#score');await p.waitForTimeout(300);for(let i=0;i<9;i++)await p.keyboard.press('ArrowRight');console.log('after 9 → :',await p.evaluate(()=>location.hash));
console.log('overflow issues',bad,'errors',errs.length?errs:'none');await b.close();process.exit(errs.length?1:0)})();
