const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({args:['--use-gl=swiftshader']});const p=await b.newPage({viewport:{width:1440,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:9314/ai-audit/?b=spiritleaf-sherwood-park#why');await p.waitForTimeout(2500);
const D=__dirname+'/shots/';
for(let i=0;i<4;i++){const t=await p.textContent('#next');const lab=await p.textContent('#why .lab');
 let mv='';if(i<3){const tr=async()=>p.$$eval('#why .mq',e=>e.map(x=>Math.round(new DOMMatrix(getComputedStyle(x).transform).m41)));await p.mouse.move(700,450);const a=await tr();await p.waitForTimeout(800);const c=await tr();mv=JSON.stringify([a,c])}
 console.log(i,lab,'|',t,'|',mv);await p.screenshot({path:D+'why'+i+'.png'});await p.click('#next');await p.waitForTimeout(700)}
console.log('cur',await p.evaluate(()=>location.hash),'errors',errs.join(';')||'none');await b.close()})();
