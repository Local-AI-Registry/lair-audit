const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({args:['--use-gl=swiftshader']});const errs=[];const D=__dirname+'/shots/';
for(const q of ['?b=spiritleaf-sherwood-park&news=preview','?b=spiritleaf-sherwood-park']){const p=await b.newPage({viewport:{width:1440,height:900}});p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:9314/ai-audit/'+q+'#why');await p.waitForTimeout(2000);
console.log(q,await p.$$eval('#why .nw .m',e=>[...new Set(e.map(x=>x.textContent))].join(' | ')));if(q.includes('preview'))await p.screenshot({path:D+'news.png'})}
await (async()=>{const p=await b.newPage({viewport:{width:1440,height:900}});await p.goto('http://localhost:9314/ai-audit/?b=spiritleaf-sherwood-park#solution');await p.waitForTimeout(2500);await p.evaluate(()=>document.querySelector('#sysl .sp[data-i="0"]').click());await p.waitForTimeout(3000);await p.screenshot({path:D+'sol0.png'})})();
console.log('errors',errs.join(';')||'none');await b.close()})();
