"""Light copy of the 3D map (mapbg.html) for the main ai-audit page: same streets and roaming people,
recolored to the white Local AI Registry brand (cream ground, white streets, navy ink).
usage: python3 lightmap.py mapbg.html ../map-light.html"""
import sys
s = open(sys.argv[1]).read()
def R(a, b):
    global s
    assert s.count(a) >= 1, a[:70]
    s = s.replace(a, b)
R("var INK='#4A2F1B', PAPER='#EEDDB8', BLUE='#1F4FE0';", "var INK='#3E4C63', PAPER='#F1ECE2', BLUE='#1F4FE0';")
R("0,'#F2E3BE',30,'#E9D3A2'],", "0,'#F3EEE5',30,'#E9E3D7'],")
R("l.paint['fill-color']='#D6C394';l.paint['fill-outline-color']=INK;", "l.paint['fill-color']='#E2DCCF';l.paint['fill-outline-color']='#CFC7B6';")
R("l.paint['fill-color']='#E6D3A6';l.paint['fill-opacity']=.55;", "l.paint['fill-color']='#DDE7D4';l.paint['fill-opacity']=.7;")
R("else if(id==='building'){l.paint={'fill-pattern':'hatch','fill-opacity':1};}", "else if(id==='building'){l.paint={'fill-color':'#E6E0D4','fill-opacity':1};}")
R("else {l.paint['fill-color']='#E9D7AE';l.paint['fill-opacity']=.6;}", "else {l.paint['fill-color']='#ECE6DA';l.paint['fill-opacity']=.6;}")
R("l.paint['line-color']='#F3E5C0';}", "l.paint['line-color']='#FFFFFF';}")
R("else if(has(id,['water'])){l.paint['line-color']='#B8A06E';}", "else if(has(id,['water'])){l.paint['line-color']='#B9CFDD';}")
R("l.layout['text-font']=['Noto Sans Italic'];", "l.layout['text-font']=['Noto Sans Regular'];")
R("l.paint['text-color']=INK; l.paint['text-halo-color']=PAPER;", "l.paint['text-color']='#7A8597'; l.paint['text-halo-color']=PAPER;")
R("g.fillStyle='#F1E2BC';", "g.fillStyle='#EEE8DC';")
R("ctx.font='italic 13px \"IM Fell English\", Georgia, serif';", "ctx.font='600 12px \"Hanken Grotesk\", Arial, sans-serif';")
s = s.replace("background:#EEDDB8", "background:#F1ECE2")
# brand fonts and navy ink instead of the vintage serif and brown
R('--f-map:"IM Fell English",Georgia,"Times New Roman",serif;', '--f-map:"Hanken Grotesk",Arial,sans-serif;')
R('--f-sc:"IM Fell English SC",Georgia,serif;', '--f-sc:"Bricolage Grotesque","Hanken Grotesk",Arial,sans-serif;')
R('--paper:#EEDDB8; --ink:#4A2F1B;', '--paper:#F1ECE2; --ink:#2C3A4F;')
R('#pinrt{font:700 10.5px var(--f-ui)!important;color:#4A2F1B!important', '#pinrt{font:700 10.5px var(--f-ui)!important;color:#2C3A4F!important')
# the poster image was never added to the repo; skip the request
R('<img id="poster" src="map-poster.jpg"', '<img id="poster" src="data:image/gif;base64,R0lGODlhAQABAAAAACw="')
# let the page say how much room its own panels take, so the business lands in the open part of the screen
R("map.setPadding({top:TOPP,bottom:BOT,left:0,right:0});", "map.setPadding(LAIR.pad||{top:TOPP,bottom:BOT,left:0,right:0});")
# fonts: the same self-hosted files the audit page already loaded (cached), instead of Google Fonts and the unused serif
import re
s, n = re.subn(r'<link rel="preconnect" href="https://fonts\.(googleapis|gstatic)\.com"[^>]*>\n?', '', s)
s, m = re.subn(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?[^"]*">',
    '<style>@font-face{font-family:"Hanken Grotesk";font-weight:100 900;font-display:swap;src:url(../home/assets/fonts/hanken.woff2) format("woff2")}'
    '@font-face{font-family:"Bricolage Grotesque";font-weight:200 800;font-display:swap;src:url(../home/assets/fonts/bricolage.woff2) format("woff2")}</style>', s)
assert n == 2 and m == 1, (n, m)
open(sys.argv[2], 'w').write(s); print('ok', sys.argv[2])
