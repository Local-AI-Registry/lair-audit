import sys
s=open(sys.argv[1]).read()
def R(a,b,n=1):
    global s
    c=s.count(a);assert c>=1,a[:70];s=s.replace(a,b) if n==0 else s.replace(a,b,n)
R("var INK='#4A2F1B', PAPER='#EEDDB8', BLUE='#1F4FE0';","var INK='#2A4670', PAPER='#050B15', BLUE='#5B8CFF';")
R("0,'#F2E3BE',30,'#E9D3A2'],","0,'#0E2038',30,'#1D3C69'],")
R("'fill-extrusion-opacity':.96","'fill-extrusion-opacity':.94")
R("l.paint['fill-color']='#D6C394';l.paint['fill-outline-color']=INK;","l.paint['fill-color']='#02060D';l.paint['fill-outline-color']='#0B1A2E';")
R("l.paint['fill-color']='#E6D3A6';l.paint['fill-opacity']=.55;","l.paint['fill-color']='#0A1A2C';l.paint['fill-opacity']=.6;")
R("else if(id==='building'){l.paint={'fill-pattern':'hatch','fill-opacity':1};}","else if(id==='building'){l.paint={'fill-color':'#0C1C33','fill-opacity':1};}")
R("else {l.paint['fill-color']='#E9D7AE';l.paint['fill-opacity']=.6;}","else {l.paint['fill-color']='#08121F';l.paint['fill-opacity']=.6;}")
R("l.paint['line-color']='#F3E5C0';}","l.paint['line-color']='#1A2E4B';}")
R("else if(has(id,['water'])){l.paint['line-color']='#B8A06E';}","else if(has(id,['water'])){l.paint['line-color']='#0E2240';}")
R("l.layout['text-font']=['Noto Sans Italic'];","l.layout['text-font']=['Noto Sans Regular'];l.layout['text-letter-spacing']=.12;l.layout['text-transform']='uppercase';")
R("l.paint['text-color']=INK; l.paint['text-halo-color']=PAPER;","l.paint['text-color']='#5F7698'; l.paint['text-halo-color']=PAPER;")
R("paint:{'line-color':INK,'line-width':['interpolate',['linear'],['zoom'],15,.6,19,1.6],'line-opacity':.9}","paint:{'line-color':'#3A6BC4','line-width':['interpolate',['linear'],['zoom'],15,.4,19,1],'line-opacity':.45}")
R("g.fillStyle='#F1E2BC';","g.fillStyle='#0C1C33';")
R("#mvveil{background:#F4F1EA}","#mvveil{background:#050B15}")
s=s.replace("background:#EEDDB8","background:#050B15")

for a,b in [("ctx.font='italic 13px \"IM Fell English\", Georgia, serif';","ctx.font='500 10px \"JetBrains Mono\", monospace';"),
 ("ctx.font='700 11px \"Hanken Grotesk\", Arial, sans-serif';","ctx.font='600 10px \"JetBrains Mono\", monospace';"),
 ("ctx.font='700 8px \"Hanken Grotesk\", Arial, sans-serif';","ctx.font='600 8px \"JetBrains Mono\", monospace';"),
 ("ctx.font='600 11.5px \"Hanken Grotesk\", Arial, sans-serif';","ctx.font='500 10.5px \"JetBrains Mono\", monospace';"),
 ("ctx.fillStyle=(w.ai||w.col)?'#FFFFFF':'#F6EBD0';","ctx.fillStyle='rgba(6,14,26,.9)';"),
 ("ctx.fillStyle='rgba(255,255,255,.95)';","ctx.fillStyle='rgba(6,14,26,.9)';"),
 ("ctx.fillStyle='#fff';","ctx.fillStyle='rgba(6,14,26,.9)';"),
 ("ctx.fillStyle='#FFFFFF';","ctx.fillStyle='rgba(6,14,26,.9)';"),
 ("ctx.strokeStyle='#fff';","ctx.strokeStyle='rgba(120,160,230,.35)';"),
 ("ctx.fillStyle=w.col||INK;","ctx.fillStyle=w.col||'#C9D6EA';"),
 ("ctx.fillStyle=w.col||(w.ai?BLUE:INK);","ctx.fillStyle=w.col||(w.ai?'#8FB0FF':'#C9D6EA');"),
 ("ctx.fillStyle=p.col||(p.ai?BLUE:INK);","ctx.fillStyle=p.col||(p.ai?'#8FB0FF':'#C9D6EA');"),
 ("ctx.strokeStyle=w.col||(w.ai?BLUE:INK);","ctx.strokeStyle=w.col||(w.ai?'rgba(91,140,255,.7)':'rgba(255,181,71,.55)');")]:
    assert s.count(a)>=1,a
    s=s.replace(a,b)
sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from darkcolors import convert
s=convert(s)
CSS=open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'darkmap.css')).read()
s=s.replace('family=IM+Fell+English','family=JetBrains+Mono:wght@300;400;500;600&family=Inter:wght@300;400;600&family=IM+Fell+English',1)
i=s.rfind('</head>');s=s[:i]+'<style id="hud">'+CSS+'</style>'+s[i:]
open(sys.argv[2],'w').write(s);print('ok')
