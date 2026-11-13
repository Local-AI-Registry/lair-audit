const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({args:['--use-gl=swiftshader']});const errs=[];const D=__dirname+'/shots/';
const p=await b.newPage({viewport:{width:1440,height:900}});p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:9314/ai-audit/?b=spiritleaf-sherwood-park#proposal');await p.waitForTimeout(2000);
await p.click('#pct');await p.fill('#ccp','kody25');await p.click('#pca');await p.waitForTimeout(1300);
console.log(await p.innerText('#pcm'),'|',await p.innerText('#cd'));
await p.screenshot({path:D+'pr0.png'});
for(const n of ['12-month plan','Old way vs new way','Calculator']){await p.evaluate(n=>window.PTAB(n),n);await p.waitForTimeout(500);await p.screenshot({path:D+'pr_'+n.slice(0,3)+'.png'})}
const box=await p.$eval('#cp2',e=>{const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height]});const a=await p.innerText('#prv');await p.mouse.move(box[0]+box[2]*.3,box[1]+box[3]/2);await p.mouse.down();await p.mouse.move(box[0]+box[2]*.7,box[1]+box[3]/2,{steps:8});await p.mouse.up();console.log('drag',a,'->',await p.innerText('#prv'));
console.log('errors',errs.join(';')||'none');await b.close()})();
