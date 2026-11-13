const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({args:['--use-gl=swiftshader']});const errs=[];
for(const s of ['spiritleaf-sherwood-park','spiritleaf-salisbury','elevate-cannabis-belton','bridge-city-east-dubuque','quiktox']){const p=await b.newPage({viewport:{width:1440,height:900}});p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:9314/ai-audit/?b='+s+'&concept=4#value');await p.waitForTimeout(1500);console.log(s,await p.evaluate(()=>[window.VALUE&&Math.round(window.VALUE()),window.CUST&&Math.round(window.CUST())]),(await p.innerText('#s-value')).replace(/\n+/g,' | ').slice(0,260));await p.close()}
console.log('errors',errs.join(';')||'none');await b.close()})();
