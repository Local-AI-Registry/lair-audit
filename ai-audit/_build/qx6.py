import sys,re
src,dst=sys.argv[1],sys.argv[2]
s=open(src).read()
def R(a,b,n=1):
    global s
    c=s.count(a); assert c==n,(a[:80],c); s=s.replace(a,b)
def span(start):
    tag=re.match(r'<([a-z]+)',s[start:]).group(1);d=0
    for m in re.finditer(r'<(/?)'+tag+r'\b[^>]*>',s[start:]):
        d+= -1 if m.group(1) else 1
        if d==0: return start+m.end()
def cut_at(st):
    global s
    e=span(st);h=s[st:e];s=s[:st]+s[e:];return h
def cut(marker):
    i=s.find(marker);assert i>=0 and s.count(marker)==1,marker;return cut_at(i if s[i]=='<' else s.rfind('<',0,i))
def main_end(mid): i=s.find('id="'+mid+'"');return s.find('</main>',i)
def before_main_cta(mid,html):
    global s
    j=main_end(mid);k=s.rfind('<button class="cta go"',s.find('id="'+mid+'"'),j);assert k>0,mid;s=s[:k]+html+'\n'+s[k:]

R("+pth+'#solution'","+pth+'#status'")
# ---------- flow: AI Score, Worth, Audit, Our system, Why us, Proposal ----------
R("const ORDER=['find','solution','cost','status','value','cac','expert','why','experts','steve','proposal'],STEP={find:-1,solution:0,cost:1,status:2,value:3,cac:4,expert:5,why:6,experts:5,steve:5,proposal:7};",
  "const ORDER=['find','status','value','audit','solution','why','proposal','cost','cac','expert','experts','steve'],STEP={find:-1,status:0,value:1,audit:2,solution:3,why:4,proposal:5,cost:5,cac:5,expert:5,experts:4,steve:4};")
R("' of 8'","' of 6'")
nav=s[s.find('<nav class="stp" aria-label="Steps">'):];nav=nav[:nav.find('</nav>')+6]
R(nav,'<nav class="stp" aria-label="Steps"><button data-go="status">1<em> AI Score</em></button><button data-go="value">2<em> What it&rsquo;s worth</em></button><button data-go="audit">3<em> Audit</em></button><button data-go="solution">4<em> Our system</em></button><button data-go="why">5<em> Why us</em></button><button data-go="proposal">6<em> Proposal</em></button></nav>')
R('<button class="bk go" data-go="status">Dashboard</button>','<button class="bk go" data-go="status">AI Score</button>')
R("const C={status:[","const C={audit:['Audit','The 11 issues we found','Maybe we can help','solution'],status:[")

R('family=Cormorant:wght@600;700','family=Cormorant:ital,wght@0,600;0,700;1,500;1,600')
# ---------- 1. AI Score: score, traffic, where you show up, competitors on one page ----------
R("['s-status','s-value'].forEach(id=>","[].forEach(id=>")
R('data-go="cac" type="button">See cost per customer','data-go="audit" type="button">See what it would take')
st0=s.find('id="s-status"')
hero=cut('class="card hero"')
i=s.find('<div class="ch2"',st0);traffic=cut_at(s.rfind('<section',0,i))
i=s.find('Where you show up',st0);where=cut_at(s.rfind('<section class="card"',0,i))
comp=cut('class="card cgc"')
st0=s.find('id="s-status"');k=s.find('>',st0)+1
s=s[:k]+'\n'+hero+'\n'+traffic+'\n'+where+'\n'+comp+'\n'+s[k:]

# ---------- 3. Audit: the 11 issues, one long list, no selling ----------
AUD='''<main class="scr" id="s-audit" hidden>
<div class="sh"><p class="k">Audit</p><h2 class="sh2">The 11 things AI checks before it recommends&nbsp;you</h2><p class="sub">Here&rsquo;s what we found for each&nbsp;one.</p></div>
<div class="au-list" id="au11"></div>
<button class="cta go" data-go="solution">Maybe we can help</button>
</main>
'''
R('<main class="scr" id="s-cost"','\n'+AUD+'<main class="scr" id="s-cost"')

# ---------- 4. Our system: the hub, nothing else ----------
R('<h2 class="ah-h">One Record fixes all <span class="ahn">11</span>&nbsp;issues</h2><p class="sub ah-sub">We checked <span class="ahn">11</span> things AI looks at before it recommends a business. Your Record on the Local AI Registry is built to fix every one of them. Tap any one to see what we&nbsp;found.</p>',
  '<h2 class="ah-h">Maybe we can&nbsp;help</h2><p class="sub ah-sub">Our proprietary system: one Record on the Local AI Registry, connected to all <span class="ahn">11</span>. Tap any one to see how we fix&nbsp;it.</p>')
R('<p class="k" style="color:var(--ok)">Audit results</p><h2 class="ah-h">','<p class="k" style="color:var(--blue)">Our system</p><h2 class="ah-h">')

# ---------- 5. Why us: news, track record, vouches, safe with us ----------
wi=s.find('class="wy-s wy-rec"');recold=cut_at(s.rfind('<div',0,wi)).replace('class="wy-s wy-rec"','class="wy-recold"',1)
safe=cut('class="card safe"')
R('<button type="button" data-w="4" aria-label="The Record"></button>','<button type="button" data-w="4" aria-label="You&rsquo;re safe with us"></button>')
wv=s.find('class="wy-s wy-vouch"');we=span(s.rfind('<div',0,wv))
s=s[:we]+'\n<div class="wy-s wy-safe" data-w="3"><div class="wys-in">'+safe+'</div></div>'+s[we:]
j=main_end('s-why');s=s[:j]+'<div hidden>'+recold+'</div>'+s[j:]

# ---------- 6. Proposal: how we compare, the usual way, cost per customer ----------
xc=cut('<section class="card xcmp"')
cst=cut('class="card cst" id="cstb"').replace('<section class="card cst" id="cstb">','<section class="card cst cst2"><p class="k">The usual way</p><h3 class="h3s">What fixing this would cost the usual&nbsp;way</h3><div id="cstb"></div>',1)
cac=cut('class="card cac"')
pi=s.find('id="s-proposal"');bk=s.find('class="card bld"',pi);bst=s.rfind('<section',0,bk)
s=s[:bst]+xc+'\n'+cac+'\n'+s[bst:]
pi=s.find('id="s-proposal"');ck=s.find('class="card co co2"',pi);cst_at=s.rfind('<section',0,ck)
s=s[:cst_at]+cst.replace('<p class="k">The usual way</p>','<p class="k">All in one</p>',1)+'\n'+s[cst_at:]

CSS=r'''
/* ===== quiktox flow v6: dashboard ===== */
.au-list{display:grid;gap:18px;margin:6px 0 24px}
.au-box{background:#fff;border:1px solid var(--rule);border-radius:20px;padding:26px 28px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr);gap:28px;align-items:center}
.au-n{font:800 12px/1 var(--fu);letter-spacing:.08em;color:var(--muted);text-transform:uppercase;margin:0 0 10px;display:flex;align-items:center;gap:10px}
.au-st{font:800 11px/1 var(--fu);letter-spacing:.04em;text-transform:none;padding:6px 10px;border-radius:999px}
.au-st.bad{background:#FDECEA;color:#C8281E}.au-st.warn{background:#FBF1DC;color:#8A5A00}.au-st.ok{background:#E6F5EC;color:#0E7A4E}
.au-box h3{font:800 24px/1.2 var(--fu);color:var(--ink);margin:0 0 10px}
.au-i{font:500 15.5px/1.55 var(--fb);color:var(--body);margin:0}
.au-parts{list-style:none;margin:14px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:6px}.au-parts li{font:600 12.5px var(--fu);padding:6px 10px;border-radius:999px;background:#F4F1EA;color:var(--ink)}.au-parts li b{font-weight:800}.au-parts li.bad b{color:#C8281E}.au-parts li.warn b{color:#8A5A00}.au-parts li.ok b{color:#0E7A4E}
.au-ev .stage{margin:0;border-radius:14px;overflow:hidden}
@media (max-width:860px){.au-box{grid-template-columns:1fr;padding:20px 18px;gap:16px}.au-box h3{font-size:20px}}
.wy-safe{display:grid;place-items:center;padding:28px}.wys-in{width:min(640px,100%)}.wys-in .card{margin:0}

/* dashboard: locked left panel, the right side is the screen */
#dash{display:none}
@media (min-width:1000px){
 body.dash #dash{display:flex;flex-direction:column;position:fixed;z-index:70;left:0;top:0;bottom:0;width:280px;background:#0B1A2E;color:#fff;padding:26px 22px 22px;box-sizing:border-box;overflow:auto}
 #dash .lockup{width:170px;height:auto;color:#fff}
 #dash .dk{font:700 11px/1 var(--fu);letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.55);margin:30px 0 8px}
 #dash .dbiz{font:400 30px/1.1 var(--fh,"Cormorant",serif);margin:0;color:#fff}
 #dash .dloc{font:500 13px/1.4 var(--fb);color:rgba(255,255,255,.6);margin:6px 0 0}
 #dash nav{margin:30px 0 0;display:flex;flex-direction:column}
 #dash nav button{all:unset;cursor:pointer;display:flex;align-items:center;gap:12px;padding:10px 0;font:600 14px/1.2 var(--fu);color:rgba(255,255,255,.6);position:relative}
 #dash nav button:before{content:attr(data-n);flex:none;display:grid;place-items:center;width:28px;height:28px;border-radius:50%;border:1.5px solid rgba(255,255,255,.25);font:700 12px var(--fu);background:#0B1A2E;position:relative;z-index:1}
 #dash nav button:not(:last-child):after{content:"";position:absolute;left:14px;top:calc(50% + 14px);height:calc(100% - 28px);width:1.5px;background:rgba(255,255,255,.18)}
 #dash nav button.done{color:#fff}#dash nav button.done:before{background:#fff;color:#0B1A2E;border-color:#fff}
 #dash nav button.cur{color:#fff;font-weight:800}#dash nav button.cur:before{background:#1F4FE0;border-color:#1F4FE0;color:#fff;box-shadow:0 0 0 4px rgba(31,79,224,.3)}
 #dash .dfoot{margin-top:auto;padding-top:20px;border-top:1px solid rgba(255,255,255,.12)}
 #dash .dfoot button{all:unset;cursor:pointer;font:700 13px var(--fu);color:rgba(255,255,255,.75)}
 html body.dash .w,html body.dash.railon .w,html body.dash.hasbar.onst .w,html body.dash.hasbar.onval .w,html body.dash.hasbar.onsol .w,html body.dash.hasbar.onprop .w,html body.dash.hasbar.onexp .w,html body.dash.hasbar .w{max-width:none!important;width:auto!important;margin:0 0 0 280px!important;padding:28px 44px 60px!important;box-sizing:border-box}
 body.dash .w>.top,body.dash .who,body.dash .w>.when,body.dash #fl .stp,body.dash #fl .bk,body.dash .t4-rail{display:none!important}
 body.dash.railon .fl .stp{display:none!important}
 body.dash #fl{position:fixed!important;top:18px;right:28px;left:auto;z-index:65;background:none!important;padding:0!important;margin:0!important}
 body.dash #fl .flt2{justify-content:flex-end}
 body.dash .scr>.sh:first-child{padding-right:240px}
 /* Why us fills the whole right side */
 body.dash #s-why{margin:-28px -44px -60px}
 body.dash #s-why .card.wy{margin:0;border-radius:0;border:0;padding:0;min-height:100vh;background:#0B1A2E}
 body.dash #s-why .wy-top,body.dash #s-why .wy-nav{display:none!important}
 body.dash #s-why .wy-vp{height:100vh!important}
 body.dash #s-why .wy-s{min-height:100vh;position:relative}
 body.dash #s-why .wyn-bg,body.dash #s-why .wyv-wall,body.dash #s-why .wyt-res{position:absolute;inset:0}
 body.dash #s-why .wy-s:not(.wy-safe):after{content:"";position:absolute;inset:0;background:rgba(11,26,46,.62);z-index:1;pointer-events:none}
 body.dash #s-why .wyn-fg,body.dash #s-why .wyt-fg{position:absolute!important;inset:0!important;z-index:2;display:flex!important;flex-direction:column;align-items:center;justify-content:center;text-align:center;background:none!important;box-shadow:none!important;border:0!important;transform:none!important;width:auto!important;max-width:none!important;padding:0 8%}
 body.dash #s-why .wy-h{font:800 clamp(40px,5vw,68px)/1.05 var(--fu)!important;color:#fff!important;letter-spacing:-.01em;margin:0!important;text-wrap:balance}
 body.dash #s-why .wyn-fg .wy-p,body.dash #s-why .wyt-fg p{color:rgba(255,255,255,.8)!important;font-size:17px!important;margin:14px 0 0!important}
 body.dash #s-why .wyn-fg .wy-logos,body.dash #s-why .wyn-list{display:none!important}
 body.dash #s-why .wy-safe{background:var(--bg)}
 .wy-go{appearance:none;border:0;cursor:pointer;margin:30px 0 0;background:#fff;color:#0B1A2E;font:800 15px/1 var(--fu);padding:15px 0;width:min(340px,80%);border-radius:999px}
 body.dash #s-why .wy-safe .wy-go{background:var(--blue);color:#fff}
}
.wy-go{display:none}body.dash .wy-go{display:inline-block}
#s-status>section{grid-column:1/-1!important}.gap2 .cta{display:none!important}
#s-proposal .xcmp{overflow-x:auto}.calc-tg .ct-a{white-space:normal}
@media (max-width:999px){.stp button em{display:none!important}}
/* why us, SEO Aesthetic style */
@media (min-width:1000px){
 body.dash #s-why .wyn-fg,body.dash #s-why .wyt-fg{backdrop-filter:none!important;-webkit-backdrop-filter:none!important}
 body.dash #s-why .wy-s:not(.wy-safe):after{background:rgba(6,12,24,.74)}
 body.dash #s-why .wy-s{overflow:hidden}
 body.dash #s-why .wy-track .svres{height:100%;margin:0;display:flex;flex-direction:column;justify-content:center;background:none;border:0;box-shadow:none;padding:0}
 body.dash #s-why .wy-track .vwrap{transform:scale(1.75);transform-origin:50% 50%}
 body.dash #s-why .wyn-bg{-webkit-mask:none;mask:none;justify-content:space-between;gap:18px;padding:0;inset:-10px 0}
 body.dash #s-why .wyn-row{gap:18px;margin-left:-120px}
 body.dash #s-why .wyn-row.r2{margin-left:-300px}
 body.dash #s-why .wna{width:440px!important;height:280px!important;border-radius:10px;box-shadow:0 12px 30px rgba(0,0,0,.35)}
 body.dash #s-why .wna-m{padding:12px 16px!important;font-size:17px!important}
 body.dash #s-why .wna-b{padding:14px 18px}
 body.dash #s-why .wna-c{font-size:10px}
 body.dash #s-why .wna-h{font-size:24px;line-height:1.18;-webkit-line-clamp:3;margin:6px 0 8px}
 body.dash #s-why .wna-p{font-size:14px;-webkit-line-clamp:3}
 body.dash #s-why .wy-safe{background:#0B1A2E!important}
 body.dash #s-why .wy-safe .wys-in{display:flex;flex-direction:column;align-items:center;gap:26px}
 body.dash #s-why .wy-safe .wys-in>.card{width:min(560px,100%)}
 body.dash #s-why .wy-safe .wy-go{background:#fff!important;color:var(--ink)!important}
 body.dash #s-why .wy-go{min-width:330px;justify-content:center}
}
.wy-h.wy-h2{display:flex!important;flex-direction:column;align-items:center;text-align:center;gap:0}
.wy-h.wy-h2 em{font:italic 600 clamp(40px,5.2vw,76px)/1 Cormorant,Georgia,serif!important;letter-spacing:-.005em;text-transform:none}
.wy-h.wy-h2 b{font:800 clamp(38px,5vw,72px)/.98 var(--fu)!important;text-transform:uppercase;letter-spacing:-.01em}
body.dash #s-why .wy-h.wy-h2{color:#fff!important}
@media (max-width:999px){.wy-h.wy-h2 em{font-size:30px!important}.wy-h.wy-h2 b{font-size:28px!important}}
/* multiple locations toggle */
.mloc{margin:14px 0 0;border-top:1px solid var(--rule);padding-top:12px}
.mloc summary{list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;font:700 13.5px var(--fu);color:var(--ink)}
.mloc summary::-webkit-details-marker{display:none}
.mloc summary i{width:34px;height:20px;border-radius:999px;background:#D9DDE5;position:relative;transition:background .2s}
.mloc summary i:after{content:"";position:absolute;top:2px;left:2px;width:16px;height:16px;border-radius:50%;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.25);transition:transform .2s}
.mloc[open] summary i{background:var(--blue)}.mloc[open] summary i:after{transform:translateX(14px)}
.mloc table{width:100%;border-collapse:collapse;margin:12px 0 6px;font:500 12.5px var(--fb)}
.mloc th{text-align:left;font:700 10.5px var(--fu);color:var(--muted);padding:0 4px 6px 0;border-bottom:1px solid var(--rule)}
.mloc td{padding:7px 4px 7px 0;border-bottom:1px solid var(--rule);color:var(--ink);font-variant-numeric:tabular-nums}
.mloc td:last-child{color:var(--ok);font-weight:700}
.mloc p{margin:6px 0 0;font:400 11.5px/1.45 var(--fb);color:var(--muted)}
/* global header: back + title top left, one CTA top right */
.qbk{all:unset;cursor:pointer;display:inline-flex;align-items:center;gap:6px;font:700 13px/1 var(--fu);color:var(--muted);margin:0 0 14px;padding:6px 0}
.qbk:hover{color:var(--blue)}
#s-solution .solh,#ahub .ah-hd{display:none!important}
#s-value .cta.coral,#s-audit .cta,#s-solution .ah-foot{display:none!important}
#s-why .qsh{position:absolute;z-index:6;left:44px;top:24px;margin:0;pointer-events:auto}
#s-why .qsh .qbk{color:rgba(255,255,255,.7)}#s-why .qsh .qbk:hover{color:#fff}
#s-why .qsh .k{display:none}#s-why .qsh .sh2{color:#fff!important;font-size:clamp(22px,2.4vw,30px)!important;margin:0!important}
#s-why{position:relative}
@media (max-width:999px){#s-why .qsh{position:relative;left:auto;top:auto;margin:0 0 12px}#s-why .qsh .qbk{color:var(--muted)}#s-why .qsh .sh2{color:var(--ink)!important}}
#s-status>.qsh{grid-column:1/-1}#s-status>.qsh .sh2{max-width:none}
@media (max-width:999px){#s-status>.qsh{display:none}body:not(.dash) .bk.go[data-go="status"]{visibility:hidden}}
/* audit: PageSpeed-style, plain */
#au11.au-list{display:block;background:#fff;border:1px solid var(--rule);border-radius:12px;padding:6px 26px 10px}
.ps-sum{display:flex;flex-wrap:wrap;align-items:center;gap:8px 22px;padding:16px 0;border-bottom:1px solid var(--rule);font:600 13px/1 var(--fb);color:var(--ink)}
.ps-sum span{display:inline-flex;align-items:center;gap:7px}.ps-sum em{margin-left:auto;font-style:normal;color:var(--muted);font-size:12px}
.pi{width:12px;height:12px;flex:none}.pi.bad{fill:#E03C31}.pi.warn{fill:#F2A33A}.pi.ok{fill:#1E9E58}
.ps-row{padding:22px 0;border-bottom:1px solid var(--rule)}.ps-row:last-child{border-bottom:0}
.ps-h{display:flex;align-items:center;gap:10px}.ps-h b{font:700 17px/1.2 var(--fb);color:var(--ink)}
.ps-st{margin-left:auto;font:600 12px/1 var(--fb)}.ps-st.bad{color:#C8281E}.ps-st.warn{color:#9A5B00}.ps-st.ok{color:#0E7A4E}
.ps-i{margin:6px 0 12px 22px;font:400 14px/1.5 var(--fb);color:var(--body);max-width:760px}
.ps-m{display:flex;align-items:baseline;justify-content:space-between;gap:12px;margin:0 0 8px 22px;font:500 13.5px var(--fb);color:var(--ink)}
.ps-m b{font:600 24px/1 var(--fb)}.ps-m b.bad{color:#C8281E}.ps-m b.warn{color:#B86E00}.ps-m b.ok{color:#0E7A4E}
.ps-bar{position:relative;display:flex;gap:2px;height:6px;margin:0 0 14px 22px}.ps-bar i{height:100%}.ps-bar i.ok{background:#1E9E58}.ps-bar i.warn{background:#F2A33A}.ps-bar i.bad{background:#E03C31}
.ps-bar u{position:absolute;top:-5px;width:2px;height:16px;background:#202124;transform:translateX(-1px)}
.ps-cmp{width:calc(100% - 22px);margin:0 0 8px 22px;border-collapse:collapse;font:400 13px var(--fb);color:var(--ink)}
.ps-cmp caption{text-align:left;font:600 11.5px var(--fb);color:var(--muted);padding:0 0 6px}
.ps-cmp th{width:190px;text-align:left;font-weight:400;padding:4px 10px 4px 0;white-space:nowrap}.ps-cmp tr.me th{font-weight:700}
.ps-cmp td{padding:4px 0}.ps-cmp td i{display:block;height:10px;min-width:2px}.ps-cmp td i.ok{background:#1E9E58}.ps-cmp td i.warn{background:#F2A33A}.ps-cmp td i.bad{background:#E03C31}
.ps-cmp td.v{width:84px;text-align:right;font-variant-numeric:tabular-nums;padding-left:10px}
.ps-src{margin:4px 0 0 22px;padding:8px 12px;background:#F1F3F4;border-radius:4px;font:400 12px/1.4 var(--fb);color:#5F6368}
@media (max-width:640px){#au11.au-list{padding:4px 14px}.ps-cmp th{width:110px;white-space:normal}.ps-i,.ps-m,.ps-bar,.ps-cmp,.ps-src{margin-left:0;width:auto}.ps-cmp{width:100%}.ps-sum em{margin-left:0}}
/* audit: static, no motion */
#au11 *,#au11 *::before,#au11 *::after{animation:none!important;transition:none!important}
#au11 .fi,#au11 .ffl{opacity:1!important;transform:none!important}
#au11 .fdraw{stroke-dashoffset:0!important}
#au11 .fgrow,#au11 .frot{transform:none!important}
#ahub .wr2-real{position:absolute;inset:0;background:#fff;display:flex;flex-direction:column;text-align:left}
#ahub .rr-url{display:flex;align-items:center;gap:5px;padding:8px 10px;background:#F4F1EA;border-bottom:1px solid #E6E1D6}
#ahub .rr-url i{width:7px;height:7px;border-radius:50%;background:#D8D2C4}
#ahub .rr-url span{margin-left:6px;font:600 10px/1 var(--fu);color:var(--muted);background:#fff;border-radius:999px;padding:4px 9px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#ahub .rr-b{padding:14px 16px}
#ahub .rr-hd{display:flex;align-items:center;gap:10px}
#ahub .rr-lg{width:34px;height:34px;border-radius:9px;background:#0B1A2E;color:#fff;display:grid;place-items:center;font:800 15px/1 var(--fu)}
#ahub .rr-hd b{display:block;font:800 16px/1.15 var(--fu);color:var(--ink)}
#ahub .rr-hd small{display:block;font:500 11.5px/1.3 var(--fb);color:var(--muted)}
#ahub .rr-v{margin:10px 0 8px;font:700 11px/1 var(--fu);color:#0B6B35}
#ahub .rr-row{display:grid;grid-template-columns:62px 1fr;align-items:center;gap:8px;padding:6px 0;border-top:1px solid #F0ECE3}
#ahub .rr-row span{font:700 10.5px/1 var(--fu);color:var(--ink)}
#ahub .rr-row i{height:6px;border-radius:3px;background:#E9EDF7}
#ahub .rr-row{padding:5px 0}#ahub .rr-ph em{display:flex;gap:4px}#ahub .rr-ph u{width:22px;height:18px;border-radius:3px;background:#E2E5EC}
#ahub .ah-rec2 .wr2-stage{height:310px!important}
/* our system: no status, the real Record in the middle */
#ahub .ah-n small,#ahub .ah-n .qd,#ahub .ah-lg{display:none!important}
#ahub .ah-n{padding:9px 14px}
#ahub .ah-lines line{animation:none}
#ahub .ah-rec2{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:3;width:300px;display:flex;flex-direction:column;align-items:center;gap:12px}
#ahub .ah-rec2 .wr2-stage{width:300px;height:260px;border-radius:14px;box-shadow:0 18px 44px rgba(31,79,224,.22);cursor:pointer}
#ahub .ah-ai{display:flex;flex-wrap:wrap;justify-content:center;gap:6px 12px;background:#fff;border:1px solid #DCE4FD;border-radius:12px;padding:8px 12px;box-shadow:0 6px 18px rgba(20,20,40,.08)}
#ahub .ah-ai>span{display:flex;align-items:center;gap:5px;font:700 11px/1 var(--fu);color:var(--ink);white-space:nowrap}
#ahub .ah-ai .lg3{width:16px;height:16px;display:inline-block}#ahub .ah-ai .lg3 svg{width:16px;height:16px;display:block}
#ahub .ah-ai>em{flex-basis:100%;text-align:center;font:800 10px/1 var(--fu);letter-spacing:.08em;text-transform:uppercase;font-style:normal;color:var(--muted)}
@media (min-width:900px){#ahub .ah-stage{height:660px!important}}
@media (max-width:899px){#ahub .ah-rec2{position:relative;left:auto;top:auto;transform:none;margin:8px auto 14px;grid-column:1/-1;width:100%}#ahub .ah-rec2 .wr2-stage{width:100%;max-width:340px}}
'''
s=s.replace('</style>',CSS+'</style>',1)

JS=r'''
<script>
/* --- quiktox flow v6 --- */
(()=>{const $=(q,r)=>(r||document).querySelector(q),$$=(q,r)=>[...(r||document).querySelectorAll(q)];const X=t=>String(t==null?'':t).replace(/[<&]/g,'');
 const setGo=(scr,go,txt)=>{const s=document.getElementById(scr);if(!s)return;const d=[...s.children].filter(e=>e.matches('.cta.go'));const b=d[d.length-1];if(b){b.dataset.go=go;b.textContent=txt}};
 setGo('s-status','value','See what it’s worth');setGo('s-value','audit','See what it would take');
 const hb=$('#ahub .ah-foot .cta.go');if(hb){hb.dataset.go='why';hb.textContent='See why us'}
 /* the audit: plain, PageSpeed-style rows. Every competitor number is real (DataForSEO / Google, Nov 12, 2026) */
 const AUD={who:['QUIKTOX','MySkin','Iconique','Beauty With A Mission'],
  'Directory listings':{m:'Google name matches the real business name',t:'bool',v:[0,1,1,0],note:'Yours on Google: “QUIKTOX™ | Botox Same Day Appointments - SMS / Text To Book”',src:'Google Maps'},
  'PR':{m:'Articles about you on real news outlets',t:'num',v:[0,0,0,0],good:3,ok:1,note:'Your 6 “news” links are paid placements on sites like Sacramento News Post and Las Vegas News Herald, not real outlets',src:'DataForSEO backlink index'},
  'Video':{m:'Videos about you on YouTube',t:'num',v:[0,1,0,2],good:5,ok:1,src:'YouTube search, top 20 results'},
  'SEO':{m:'Google searches you rank for',t:'num',v:[8,94,310,186],good:100,ok:30,src:'DataForSEO, US'},
  'Web management':{m:'Homepage load time',t:'num',u:'s',v:[7.8,5.1,2.7,0.7],good:2.5,ok:4,low:1,src:'DataForSEO page test'},
  'Reputation management':{m:'Google reviews',t:'num',v:[58,102,159,158],good:150,ok:75,src:'Google Maps'},
  'Google profile':{m:'Photos on your Google profile',t:'num',v:[162,3,40,36],good:50,ok:20,src:'Google Maps'},
  'Photo codifying':{m:'Image file names say who you are',t:'bool',v:[0,0,0,1],note:'Yours: image_2024_06_06T03_32_25_584Z.png',src:'Homepage sharing image'},
  'Independent articles':{m:'Other websites linking to you',t:'num',v:[115,87,119,126],good:150,ok:75,src:'DataForSEO backlink index'},
  'Independent guides':{m:'Shows up for “best botox costa mesa”',t:'bool',v:[0,0,1,0],src:'Google, Costa Mesa, top 20'},
  'AI monitoring':{m:'Named by AI in the 8 searches where it skipped you',t:'num',v:[0,4,3,2],good:4,ok:2,src:'Our AI scan'}};
 const LB={'Reputation management':'Reputation','Independent articles':'3rd-party articles','Independent guides':'Best-of guides'};
 const ICN={bad:'<svg viewBox="0 0 12 12" class="pi bad"><path d="M6 1l5 9H1z"/></svg>',warn:'<svg viewBox="0 0 12 12" class="pi warn"><rect x="2" y="2" width="8" height="8"/></svg>',ok:'<svg viewBox="0 0 12 12" class="pi ok"><circle cx="6" cy="6" r="4.5"/></svg>'};
 const lvl=(a,x)=>a.low?(x<=a.good?'ok':x<=a.ok?'warn':'bad'):(x>=a.good?'ok':x>=a.ok?'warn':'bad');
 const fmt=(a,x)=>a.t==='bool'?(x?'Yes':'No'):(Number.isInteger(x)?x.toLocaleString('en-US'):x.toFixed(1))+(a.u?' '+a.u:'');
 const build=()=>{const box=document.getElementById('au11');if(!box)return true;const CT=window.CTD||[];if(!CT.length)return false;
  const st=s=>/pass/i.test(s)?'ok':/weak|needs/i.test(s)?'warn':'bad';
  const n={ok:0,warn:0,bad:0};CT.forEach(c=>n[st(c.st)]++);
  let h='<div class="ps-sum"><span>'+ICN.bad+n.bad+' failed</span><span>'+ICN.warn+n.warn+' need work</span><span>'+ICN.ok+n.ok+' passed</span><em>Checked Nov 12, 2026 · compared with your 3 closest competitors</em></div>';
  CT.forEach(c=>{const a=AUD[c.c],k=st(c.st),name=LB[c.c]||c.c;h+='<section class="ps-row"><div class="ps-h">'+ICN[k]+'<b>'+X(name)+'</b><span class="ps-st '+k+'">'+X(c.st==='Weak'?'Needs work':c.st)+'</span></div><p class="ps-i">'+X(c.i||'')+'</p>';
   if(a){const me=a.v[0],mk=a.t==='bool'?(me?'ok':'bad'):lvl(a,me);
    h+='<div class="ps-m"><span>'+X(a.m)+'</span><b class="'+mk+'">'+fmt(a,me)+'</b></div>';
    if(a.t==='num'){const mx=Math.max(...a.v,a.low?a.ok*1.4:a.good*1.25)||1,g=(a.low?a.good:a.ok)/mx*100,o=(a.low?a.ok:a.good)/mx*100,p=Math.min(99,me/mx*100);
     h+='<div class="ps-bar"><i class="'+(a.low?'ok':'bad')+'" style="width:'+g+'%"></i><i class="warn" style="width:'+(o-g)+'%"></i><i class="'+(a.low?'bad':'ok')+'" style="width:'+(100-o)+'%"></i><u style="left:'+p+'%"></u></div>'}
    h+='<table class="ps-cmp"><caption>You vs. competitors</caption>'+AUD.who.map((w,i)=>{const x=a.v[i],kk=a.t==='bool'?(x?'ok':'bad'):lvl(a,x),wd=a.t==='bool'?(x?100:4):Math.max(2,x/(Math.max(...a.v)||1)*100);return '<tr'+(i?'':' class="me"')+'><th>'+X(w)+'</th><td><i class="'+kk+'" style="width:'+wd+'%"></i></td><td class="v">'+fmt(a,x)+'</td></tr>'}).join('')+'</table>';
    h+='<p class="ps-src">'+(a.note?X(a.note)+' · ':'')+'Source: '+X(a.src)+'</p>'}
   h+='</section>'});
  box.innerHTML=h;return true};
 const tryB=()=>{if(!build())setTimeout(tryB,300)};tryB();
 /* why us: SEO Aesthetic style headlines, an italic lead-in over a heavy caps line */
 {const HL={'wy-news':['We’ve been talked','about in the news'],'wy-track':['Our record','speaks for itself'],'wy-vouch':['Others will','vouch for us'],'wy-safe':['You’re','safe with us']};
  Object.entries(HL).forEach(([c,t])=>{const sl=$('#s-why .wy-s.'+c);if(!sl)return;let h=$('.wy-h',sl);
   if(!h){h=document.createElement('h2');h.className='wy-h';const w=$('.wys-in',sl);if(w)w.insertBefore(h,w.firstChild)}
   h.classList.add('wy-h2');h.innerHTML='<em>'+t[0]+'</em><b>'+t[1]+'</b>'})}
 /* proposal: volume pricing for groups, under the checkout */
 {const co=$('#s-proposal .co.co2');if(co&&!$('.mloc',co)){const T=[[1,5000,0],[3,4000,20],[5,3600,28],[10,3000,40],[50,1650,67],[75,1300,74],['100+',1050,79]],M=n=>'$'+n.toLocaleString('en-US');
  const d=document.createElement('details');d.className='mloc';
  d.innerHTML='<summary><span>Multiple locations?</span><i aria-hidden="true"></i></summary><table><thead><tr><th>Locations</th><th>Per location</th><th>Monthly</th><th>Savings</th></tr></thead><tbody>'+T.map(r=>{const n=typeof r[0]==='number'?r[0]:100;return '<tr><td>'+r[0]+'</td><td>'+M(r[1])+'</td><td>'+M(n*r[1])+(typeof r[0]==='number'?'':'+')+'</td><td>'+(r[2]?r[2]+'%':'&ndash;')+'</td></tr>'}).join('')+'</tbody></table><p>Savings compared with $5,000 for a single location. Every location gets the same plan, guarantee and exclusivity.</p>';
  co.appendChild(d)}}
 /* every screen: back to the previous screen and a title, top left; the only CTA is top right */
 {const HD={status:['find','New search','AI Score','Your AI visibility'],value:['status','AI Score'],audit:['value','What it’s worth'],solution:['audit','Audit','Our system','Maybe we can help','Our proprietary system: one Record on the Local AI Registry, connected to all 11. Tap any one to see how we fix it.'],why:['solution','Our system','Why us','Why us'],proposal:['why','Why us']};
  Object.entries(HD).forEach(([id,h])=>{const m=document.getElementById('s-'+id);if(!m)return;let sh=[...m.children].find(e=>e.classList&&e.classList.contains('sh'));
   if(!sh||h[2]){sh=document.createElement('div');sh.className='sh qsh';sh.innerHTML='<p class="k">'+h[2]+'</p><h2 class="sh2">'+h[3]+'</h2>'+(h[4]?'<p class="sub">'+h[4]+'</p>':'');m.insertBefore(sh,m.firstChild)}
   const b=document.createElement('button');b.type='button';b.className='qbk';b.dataset.go=h[0];b.innerHTML='&larr; '+h[1];sh.insertBefore(b,sh.firstChild)})}
 /* our system: the real Record, peelable, with the AI apps under it */
 {const rec=$('#ahstage .ah-rec'),st=document.getElementById('wr2stage');if(rec&&st){const c=document.createElement('div');c.className='ah-rec2';c.appendChild(st);
  const ai=document.createElement('div');ai.className='ah-ai';ai.innerHTML='<em>Read by every AI</em>'+$$('#s-status .pk3 .pkc').map(x=>'<span>'+x.innerHTML+'</span>').join('');c.appendChild(ai);rec.replaceWith(c);
  const real=()=>{const pg=$('.ah-rec2 .wr2-pg');if(!pg)return setTimeout(real,200);if($('.wr2-real',pg))return;const sv=$(':scope>svg',pg);if(sv)sv.style.display='none';
   const wh=document.querySelector('.who'),wn=document.querySelector('.when'),nm=X((wh&&wh.textContent.split('·')[0].trim())||'Your business'),city=X((wn&&wn.textContent.split('·')[0].trim())||''),sl=nm.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
   const r=document.createElement('div');r.className='wr2-real';
   r.innerHTML='<div class="rr-url"><i></i><i></i><i></i><span>localairegistry.com/biz/'+sl+'</span></div><div class="rr-b"><div class="rr-hd"><span class="rr-lg">'+nm.charAt(0)+'</span><div><b>'+nm+'</b><small>'+city+'</small></div></div><p class="rr-v">&#10003; Verified business</p>'+[['License','52%'],['Services','78%'],['Team','60%'],['Hours','54%'],['Location','66%'],['Reviews','48%']].map(x=>'<div class="rr-row"><span>'+x[0]+'</span><i style="width:'+x[1]+'"></i></div>').join('')+'<div class="rr-row rr-ph"><span>Photos</span><em><u></u><u></u><u></u><u></u><u></u></em></div>'+'</div>';
   pg.insertBefore(r,pg.firstChild)};real()}}
 /* our system: a check opens straight to how we fix it */
 const hub=$('#ahub'),D=window.AHDRILL;if(D)window.AHDRILL=function(){const r=D.apply(this,arguments);setTimeout(()=>{const f=$('.dr-fix',hub);if(f&&!/back/i.test(f.textContent))f.click()},60);return r};
 /* why us: a continue button on every full-screen slide */
 $$('#s-why .wyn-fg, #s-why .wyt-fg, #s-why .wys-in').forEach((f,i,a)=>{const b=document.createElement('button');b.type='button';b.className='wy-go';b.textContent=f.classList.contains('wys-in')?'See your proposal →':'Continue →';b.onclick=()=>{const n=document.getElementById('wynext');if(n)n.click()};f.appendChild(b)});
 /* dashboard shell */
 const top=$('.w>.top'),lk=top&&$('svg.lockup',top),who=(($('.who')||{}).textContent||'').split('·')[0].trim(),when=(($('.w>.when')||{}).textContent||'').split('·')[0].trim();
 const dash=document.createElement('aside');dash.id='dash';
 dash.innerHTML=(lk?lk.outerHTML:'')+'<p class="dk">AI Visibility Audit</p><h2 class="dbiz"></h2><p class="dloc"></p><nav></nav><div class="dfoot"><button type="button">← Search another business</button></div>';
 const bz=(window.AUDITS&&0)||'';$('.dbiz',dash).textContent=(document.querySelector('#rcn')||{}).textContent&&document.querySelector('#rcn').textContent!=='Your business'?document.querySelector('#rcn').textContent:who;$('.dloc',dash).textContent=when;
 const nav=$('nav',dash);$$('.stp button').forEach((b,i)=>{const x=document.createElement('button');x.type='button';x.dataset.n=i+1;x.textContent=(b.querySelector('em')||b).textContent.trim();x.onclick=()=>b.click();nav.appendChild(x)});
 $('.dfoot button',dash).onclick=()=>{const t=$('.tback');if(t)t.click()};
 document.body.appendChild(dash);
 const sync=()=>{const f=document.getElementById('s-find'),on=f&&f.hidden&&innerWidth>=1000;document.body.classList.toggle('dash',!!on);const bs=$$('.stp button'),ds=$$('nav button',dash);bs.forEach((b,i)=>{if(ds[i]){ds[i].classList.toggle('cur',b.classList.contains('cur'));ds[i].classList.toggle('done',b.classList.contains('done'))}});
  const n=$('#rcn');if(n&&n.textContent&&n.textContent!=='Your business')$('.dbiz',dash).textContent=n.textContent};
 setInterval(sync,300);sync();
})();
</script>
'''
s=s.rstrip()+'\n'+JS
open(dst,'w').write(s);print('ok',len(s))
