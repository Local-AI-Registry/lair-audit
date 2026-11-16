// Live map behind home and scan, plus checkout. Map tiles are often blocked in test sandboxes, so this serves the
// map library from a local copy if MAPLIBRE_DIST is set (path to maplibre-gl/dist/) and stubs the tile style.
const {chromium,devices}=require('playwright');(async()=>{const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']});
const D=__dirname+'/shots/',U='http://localhost:9314/ai-audit/',ML=process.env.MAPLIBRE_DIST,errs=[];let bad=0;
const ok=(c,m)=>{if(!c){bad++;console.log('FAIL',m)}else console.log('ok  ',m)};
async function page(opt){const ctx=await b.newContext(opt);if(ML){await ctx.route('https://unpkg.com/**',r=>{const f=r.request().url().split('/dist/')[1];r.fulfill({path:ML+f,contentType:f.endsWith('.css')?'text/css':'application/javascript'})});
 await ctx.route('https://tiles.openfreemap.org/styles/**',r=>r.fulfill({contentType:'application/json',body:JSON.stringify({version:8,sources:{},layers:[{id:'bg',type:'background',paint:{'background-color':'#F1ECE2'}}]})}))}
 const p=await ctx.newPage();p.on('pageerror',e=>errs.push(e.message));return p}
for(const [name,opt] of [['desk',{viewport:{width:1440,height:900}}],['mob',devices['iPhone 13']]]){
 const p=await page(opt);await p.goto(U);await p.waitForTimeout(ML?6000:3000);
 const live=await p.evaluate(()=>document.body.classList.contains('maplive'));console.log(name,'live map:',live);
 if(ML){ok(live,name+' map loads behind the home screen');
  ok(await p.evaluate(()=>{const d=document.querySelector('#mapbg iframe').contentDocument;return ['#ldr','#fx','#fxtop'].every(s=>{const e=d.querySelector(s);return !e||getComputedStyle(e).display==='none'})}),name+' map\'s own panels are hidden')}
 await p.screenshot({path:D+'map-'+name+'-home.png'});
 await p.goto(U+'?b=spiritleaf-sherwood-park#scan');await p.waitForTimeout(ML?9000:4000);await p.screenshot({path:D+'map-'+name+'-scan.png'});
 if(ML){ok(await p.evaluate(()=>document.body.classList.contains('maptracked')),name+' radar follows the business marker');
  ok(await p.evaluate(()=>{const s=document.querySelector('.scan4 .sweep').getBoundingClientRect(),w=document.querySelector('#mapbg iframe').contentWindow,L=w.LAIR,q=L.map.project(L.mk.getLngLat());return Math.abs(s.left+s.width/2-q.x)<3&&Math.abs(s.top+s.height/2-q.y)<3}),name+' radar is centered on the marker')}
 ok(await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth)<=1,name+' no sideways scroll');
 await p.goto(U+'?b=spiritleaf-sherwood-park#score');await p.waitForTimeout(1800);
 ok(await p.evaluate(()=>getComputedStyle(document.getElementById('mapbg')).opacity==='0'),name+' map hidden behind result screens');
 // checkout
 await p.goto(U+'?b=spiritleaf-sherwood-park#plan');await p.waitForTimeout(800);
 await p.click('[data-ckx="open"]');await p.waitForTimeout(500);ok(await p.isVisible('#ckf'),name+' Get started opens checkout');
 await p.click('#ck-go');ok(/fill in/.test(await p.textContent('#ck-msg')),name+' empty card is refused');
 await p.click('#pc-open');await p.fill('#ccp','nope');await p.click('#pc-apply');ok(/isn't valid/.test(await p.textContent('#pc-msg')),name+' bad promo code is refused');
 await p.fill('#ccp','kody25');await p.click('#pc-apply');await p.waitForTimeout(300);
 ok((await p.textContent('#ck-price'))==='$3,750'&&(await p.textContent('[data-price]'))==='$3,750'&&(await p.textContent('[data-save]'))==='$10,500',name+' KODY25 takes 25% off everywhere');
 ok(await p.isVisible('#ck-cd'),name+' countdown shows');await p.screenshot({path:D+'map-'+name+'-checkout.png'});
 await p.fill('#ccname','Pat Tester');await p.fill('#ccn','4242424242424242');await p.fill('#cce','1230');await p.fill('#ccv','123');await p.fill('#ccz','90210');
 ok((await p.inputValue('#ccn'))==='4242 4242 4242 4242'&&(await p.inputValue('#cce'))==='12 / 30',name+' card number and expiry format as you type');
 await p.click('#ck-go');ok(/nothing was charged/.test(await p.textContent('#ck-msg')),name+' valid card shows the not-live message');
 await p.keyboard.press('Escape');await p.waitForTimeout(400);ok(!(await p.isVisible('#ckf')),name+' Escape closes checkout');
 await p.context().close()}
console.log('failures',bad,'errors',errs.length?errs:'none');await b.close();process.exit(bad||errs.length?1:0)})();
