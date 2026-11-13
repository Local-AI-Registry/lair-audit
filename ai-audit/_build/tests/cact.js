const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({args:['--use-gl=swiftshader']});const errs=[];const D=__dirname+'/shots/';
let p=await b.newPage({viewport:{width:1440,height:900}});p.on('pageerror',e=>errs.push(e.message));
for(const s of ['spiritleaf-sherwood-park','bridge-city-east-dubuque']){await p.goto('http://localhost:9314/ai-audit/?b='+s+'#proposal');await p.waitForTimeout(1500);await p.evaluate(()=>window.PTAB('Cost per customer'));await p.waitForTimeout(300);await p.screenshot({path:D+'cac_'+s.slice(0,6)+'.png'})}
await p.goto('http://localhost:9314/ai-audit/?b=spiritleaf-sherwood-park#solution');await p.waitForTimeout(2500);await (await p.$('#sys3')).screenshot({path:D+'rec3.png'});
console.log('errors',errs.join(';')||'none');await b.close()})();
