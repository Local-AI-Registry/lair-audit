import re
def lum(h):
    h=h.lstrip('#')
    if len(h)==3:h=''.join(c*2 for c in h)
    r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    return .2126*r+.7152*g+.0722*b
PANEL='#0C1828';PANEL2='#11223A';PANEL3='#162B47';TXT='#D7E2F2';TXT2='#9FB0C8'
def bgmap(h):
    L=lum(h)
    if L>.92:return PANEL
    if L>.8:return PANEL2
    if L>.62:return PANEL3
    return h
def txtmap(h):
    L=lum(h)
    if L<.12:return TXT
    if L<.3:return TXT2
    return h
def brmap(h):
    L=lum(h)
    return '#1E3350' if L>.7 else h
HEX=r'#(?:[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b'
# protect base64 blobs
blobs=[]
def keep(m):
    blobs.append(m.group(0));return '\x00%d\x00'%(len(blobs)-1)
def convert(s):
    blobs.clear()
    s=re.sub(r'data:[a-z/+]+;base64,[A-Za-z0-9+/=]+',keep,s)
    s=re.sub(r'(background(?:-color)?\s*:\s*)('+HEX+')',lambda m:m.group(1)+bgmap(m.group(2)),s)
    s=re.sub(r'((?<![-\w])color\s*:\s*)('+HEX+')',lambda m:m.group(1)+txtmap(m.group(2)),s)
    s=re.sub(r'(border(?:-[a-z]+)?\s*:\s*[^;"}]*?)('+HEX+')',lambda m:m.group(1)+brmap(m.group(2)),s)
    s=re.sub(r'((?:fill|stop-color)\s*[:=]\s*["\']?)('+HEX+')',lambda m:m.group(1)+(bgmap(m.group(2)) if lum(m.group(2))>.8 else txtmap(m.group(2))),s)
    s=re.sub(r'(stroke\s*[:=]\s*["\']?)('+HEX+')',lambda m:m.group(1)+(PANEL3 if lum(m.group(2))>.85 else txtmap(m.group(2))),s)
    s=re.sub(r'(background(?:-color)?\s*:\s*)(#fff\b|white\b)',lambda m:m.group(1)+PANEL,s,flags=re.I)
    def rg(m):
        r,g,b=int(m.group(2)),int(m.group(3)),int(m.group(4))
        L=(.2126*r+.7152*g+.0722*b)/255
        return m.group(1)+('rgba(8,18,32,'+m.group(5)+')' if L>.75 else m.group(0)[len(m.group(1)):])
    s=re.sub(r'(background(?:-color)?\s*:\s*)rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)',rg,s)
    s=re.sub(r'rgba\(255,\s*255,\s*255,\s*\.(9\d*|8\d*)\)','rgba(12,24,40,.9)',s)
    s=re.sub('\x00(\\d+)\x00',lambda m:blobs[int(m.group(1))],s)

    return s
