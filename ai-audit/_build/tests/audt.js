const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({args:['--use-gl=swiftshader']});const p=await b.newPage({viewport:{width:1440,height:1000}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
const D=__dirname+'/shots/';
for(const s of ['spiritleaf-sherwood-park','spiritleaf-salisbury','elevate-cannabis-belton','bridge-city-east-dubuque','quiktox']){
await p.goto('http://localhost:9314/ai-audit/?b='+s+'#audit');await p.waitForTimeout(1500);
const n=await p.$$eval('#au-l li[data-i]',e=>e.length);let out=[];
for(let i=0;i<n;i++){await p.click('#au-l li[data-i="'+i+'"]');await p.waitForTimeout(120);
 out.push(await p.evaluate(()=>{const r=document.querySelector('#au-r');return [r.querySelectorAll('.fch').length,r.querySelectorAll('.fch .bars').length,(r.innerText.match(/closest competitors/ig)||[]).length]}))}
console.log(s,JSON.stringify(out));
if(s==='spiritleaf-sherwood-park'){await p.click('#au-l li[data-i="0"]');await p.waitForTimeout(300);await (await p.$('#au-r')).screenshot({path:D+'au0.png'});await p.click('#au-l li[data-i="3"]');await p.waitForTimeout(300);await (await p.$('#au-r')).screenshot({path:D+'au3.png'});
 await p.goto('http://localhost:9314/ai-audit/?b='+s+'#solution');await p.waitForTimeout(1500);await p.evaluate(()=>document.querySelector('#sysl .sp[data-i="10"]').click());await p.waitForTimeout(3000);await p.screenshot({path:D+'sol10.png'})}}
console.log('errors',errs.join(';')||'none');await b.close()})();
