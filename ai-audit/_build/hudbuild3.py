"""Build the dark HUD audit for any business.
usage: python3 hudbuild2.py quiktox OUT.html
       python3 hudbuild2.py biz/<slug>.json OUT.html"""
import json, os, re, sys, os
D = __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '/'
out = sys.argv[1]
SRCS = sys.argv[2:]
qs = open(D + 'quiktox-audit.html').read()
def arr(s, tok):
    i = s.find(tok); assert i >= 0, tok
    k = s.find('[', i); v, _ = json.JSONDecoder().raw_decode(s[k:]); return v
QCT = arr(qs, 'const CT=[')
ex = json.load(open(D + 'extract.json'))
common = {'ex': ex, 'art': json.load(open(D + 'art.json')), 'vo': json.load(open(D + 'vouch.json')), 'rate': 0.023}
q6 = open(D + 'qx6.py').read(); a = q6.find('const AUD='); b = q6.find('};\n', a) + 1
QAUD = q6[a + len('const AUD='):b]
AISHARE = 1.0

def make(src):
    if src == 'quiktox':
        S = []
        for m in re.finditer(r"\{n:'([^']+)',c:'[^']*',(?:me:1,)?(?:on:1,)?v:\[([\d,\s.]+)\]\}", qs):
            S.append({'n': m.group(1), 'v': [float(x) for x in m.group(2).split(',')], 'me': m.group(1) == 'QUIKTOX'})
        sc = re.search(r'Your score (\d+), area average (\d+), top business (\d+)', qs)
        data = dict(common, biz={'name': 'QUIKTOX', 'full': 'QUIKTOX™ Aesthetic Med Spa', 'city': 'Costa Mesa, CA', 'addr': '1815 Newport Blvd #12, Costa Mesa, CA 92627', 'phone': '(949) 229-2275', 'site': 'quiktox.com', 'rating': 4.9, 'reviews': 58},
                    score={'you': int(sc.group(1)), 'avg': int(sc.group(2)), 'top': int(sc.group(3))},
                    ct=QCT, cr=arr(qs, 'const CR=['), rd=arr(qs, ',R=[{'), vp=arr(qs, 'window.VP=['), S=S, useEV=True,
                    hit={'name': 'QUIKTOX™ Aesthetic Med Spa', 'sub': '1815 Newport Blvd #12, Costa Mesa, CA', 'match': r'quik\s*tox', 'short': 'Quiktox', 'rt': 4.9, 'n': 58, 'area': ['Costa Mesa', 'Newport Boulevard, in the County of Orange'], 'loc': [-117.9202318, 33.6403935], 'cq': 'botox med spa', 'qs': ['best botox near me', 'same day botox near me', 'med spa near me open now', 'who has the best reviews?'], 'hours': [[540, 1020], [1980, 2460], [3420, 3900], [4860, 5340], [6300, 6780], [7740, 8220]]},
                    priceNote='DRAG TO MATCH YOUR BUSINESS. EACH PROMPT STARTS AT THE NATIONAL AVERAGE FEE FOR ITS TREATMENT (<a href="https://plasticsurgery.org/Documents/News/Statistics/2023/cosmetic-procedures-average-cost-2023.pdf" target="_blank" rel="noopener">ASPS 2023</a>).',
                    volNote='VOLUME: SEMRUSH US, NOV 2026, WITH 45% COUNTED AS AI SEARCHES (BRIGHTLOCAL 2026).')
        aud_js = QAUD
    else:
        J = json.load(open(src)); b = J['biz']
        words = [w for w in re.sub(r'[^a-z0-9 ]', ' ', b['short'].lower()).split() if len(w) > 2][:2]
        match = r'\b' + r'[\s\-_]*'.join(words) if words else re.escape(b['short'].lower())
        if J.get('match'): match = J['match']
        ff = D + 'biz/kwfull_' + J['slug'] + '.json'
        KF = json.load(open(ff))['rows'] if os.path.exists(ff) else None
        V2f0 = D + 'biz/vol2_' + J['slug'] + '.json'
        V20 = {r['q']: r['v'] for r in json.load(open(V2f0))['rows']} if os.path.exists(V2f0) else {}
        def lv(q, v):
            if q in V20: return round(V20[q] * AISHARE)
            if KF is None: return None if v is None else round(v * AISHARE)
            t = [r['v'] for r in KF if r['q'] == q and r.get('v')]
            return round(sum(t) * AISHARE) if t else None
        rd = []
        for r in J['rd']:
            r = dict(r); r['v'] = lv(r['q'], r['v'])
            if J.get('aio_unread', True): r['r'] = r['r'][:4] + [None] + r['r'][5:]
            rd.append(r)
        cr = [dict(r, v=lv(r['q'], r['v'])) for r in J['cr']]
        price = J.get('price') or {}
        pv = price.get('value') or 50
        slug = J['slug']; V2f = D + 'biz/vol2_' + slug + '.json'
        V2 = json.load(open(V2f)) if os.path.exists(V2f) else None
        kf = D + 'biz/kwlocal_' + slug + '.json'
        KL = json.load(open(kf)) if os.path.exists(kf) else []
        multi = len(set(r['loc'] for r in KL)) > 1
        if V2: vp = [[r['q'] + (' (est. local share)' if r['loc'] == 'est' else ''), round(r['v'] * AISHARE), 1, pv] for r in V2['rows']]
        elif KL: vp = [[r['q'] + (' · ' + r['loc'].split(',')[0] if multi else ''), round(r['v'] * AISHARE), 1, pv] for r in KL]
        elif J.get('vp_keywords'): vp = [[r['q'][:1].lower() + r['q'][1:], r['v'], 1, pv] for r in J['vp_keywords'] if r.get('v')]
        else: vp = [[r['q'], r['v'], 1, pv] for r in rd + cr if r.get('t') != 'Brand' and r['v']]
        vp.sort(key=lambda x: -x[1])
        hidden = 'GOOGLE HIDES THE VOLUME FOR MOST CANNABIS SEARCHES (LIKE "DISPENSARY NEAR ME" AND "WEED"), SO THE REAL NUMBER IS HIGHER. '
        PKA = json.load(open(D + 'biz/packs_all.json'))
        PKf = D + 'biz/packs_' + J['slug'] + '.json'
        PKL = PKA.get(J['slug']) or (json.load(open(PKf)) if os.path.exists(PKf) else [])
        nq = lambda t: re.sub(r'[^a-z0-9]+', ' ', t.lower()).strip()
        VQ = {nq(r['q']): r['v'] for r in (J.get('vp_keywords') or [])}
        PK = [dict(x, v=(V20.get(x['q'].split(' (')[0]) and round(V20[x['q'].split(' (')[0]] * AISHARE)) or VQ.get(nq(x['q']))) for x in PKL]
        DF = D + 'biz/dir_' + J['slug'] + '.json'
        if os.path.exists(DF):
            DR = json.load(open(DF)); rows = []
            for d in DR['dirs']:
                if not d.get('found'):
                    rows.append([d['d'], 'Not listed', 'bad']); continue
                bad = [k for k, lab in [('name_ok', 'name'), ('addr_ok', 'address'), ('phone_ok', 'phone'), ('hours_ok', 'hours')] if d.get(k) is False]
                rows.append([d['d'], ('Wrong ' + ', '.join(lab for k, lab in [('name_ok', 'name'), ('addr_ok', 'address'), ('phone_ok', 'phone'), ('hours_ok', 'hours')] if d.get(k) is False)) if bad else ('Matches Google' if all(d.get(k) for k in ('name_ok', 'addr_ok', 'phone_ok')) else (', '.join(l for k, l in [('name_ok', 'Name'), ('addr_ok', 'address'), ('phone_ok', 'phone')] if not d.get(k)).capitalize() + ' not confirmed')), 'warn' if (bad or not all(d.get(k) for k in ('name_ok', 'addr_ok', 'phone_ok'))) else 'ok'])
            rows.sort(key=lambda r: {'bad': 1, 'warn': 0, 'ok': 2}[r[2]])
            sm = DR['summary']; nf = sum(1 for d in DR['dirs'] if d.get('found'))
            mm = sum(1 for r in rows if r[2] == 'warn'); okn = sum(1 for r in rows if r[2] == 'ok')
            for c in J['checks']:
                if c['c'] == 'Directory listings':
                    c['st'] = DR['status']; c['issue'] = DR['issue']
                    c['found'] = {'h': ['Directory', 'What we found'], 'r': rows, 'ch': {'t': 'pie', 'a': okn, 'b': len(rows) - okn, 'la': 'MATCH GOOGLE', 'lb': 'WRONG, MISSING OR UNCONFIRMED', 'cap': str(len(rows)) + ' DIRECTORIES CHECKED'}}
            N9 = {'Leafly', 'Weedmaps', 'Yelp', 'Facebook', 'Yellow Pages', 'MapQuest', 'Foursquare', "Where's Weed"}
            def m9(dd, ninth):
                n = 0
                for d in dd:
                    nm = d['d']
                    if CANN and not (nm in N9 or nm.startswith(ninth) or nm.startswith('MapQuest (Key')): continue
                    if d.get('found') and d.get('name_ok') and d.get('addr_ok') and d.get('phone_ok') and d.get('hours_ok') is not False: n += 1
                return n
            slug = os.path.basename(src)[:-5]
            CANN = any(d['d'] in ('Leafly', 'Weedmaps') for d in DR['dirs'])
            ninth = 'Best Bang' if 'spiritleaf' in slug else 'Bing'
            cf = D + 'biz/dirc_' + ('spiritleaf-sherwood-park' if 'spiritleaf' in slug else slug) + '.json'
            meas = []
            if os.path.exists(cf):
                CC = {x['n']: x['match'] for x in json.load(open(cf))['comps']}
                v = [m9(DR['dirs'], ninth)] + [CC.get(c['n']) for c in J['comps'][:3]]
                meas = [{'m': 'Directories where your name, address and phone match Google (of 9)', 't': 'num', 'v': v, 'good': 7, 'ok': 4}]
            J['aud']['Directory listings'] = meas
        ct = []
        for c in J['checks']:
            q = next(x for x in QCT if x['c'] == c['c'])
            ct.append({'c': c['c'], 't': q.get('t'), 'sc': q.get('sc'), 'n': '', 'i': c['issue'], 'd': q['d'], 'dl': q.get('dl', ''), 'st': c['st']})
        def short(n):
            n = re.split(r'\s[-|–]\s|\s\|\s', n)[0]
            return n if len(n) <= 24 else n[:23].rsplit(' ', 1)[0].rstrip(' +&·-,')
        who = [b['name']] + [short(c['n']) for c in J['comps']]
        S = []
        for i, t in enumerate(J.get('traffic_dfs') or J['traffic']):
            S.append({'n': b['name'] if i == 0 else short(t['n']), 'v': [float(x or 0) for x in t['v']], 'me': i == 0})
        loc_words = J.get('cq', b.get('svc', 'store'))
        data = dict(rate=0.023, biz={k: b[k] for k in ['name', 'full', 'city', 'addr', 'phone', 'site', 'rating', 'reviews']},
                    score=J['score'], ct=ct, cr=cr, rd=rd, vp=vp, S=S, months=J['months'], useEV=False,
                    aud2=J['aud'], found={c['c']: c['found'] for c in J['checks']}, packs=PK,
                    hit={'name': b['full'], 'sub': b['addr'], 'match': match, 'short': b['short'], 'rt': b['rating'], 'n': b['reviews'], 'area': b['area'], 'loc': [b['lng'], b['lat']], 'cq': loc_words, 'qs': J.get('movie_qs', ['best %s near me' % b['svc'], '%s open now' % b['svc'], '%s near me with deals' % b['svc'], 'who has the best reviews?']), 'hours': b['hours']},
                    tr={'k': 1, 'lab': 'WEBSITE VISITS FROM GOOGLE · / MO', 'note': J.get('trafficNote', 'Estimated visits to each whole website, all locations combined (DataForSEO).')},
                    scanNote=J.get('scanNote', 'Google AI Overviews could not be read in this scan, so they are not counted.'),
                    priceNote=J['priceNote'], volNote=('VOLUME: SEMRUSH, NOV 2026. TOWN SEARCHES (LIKE "' + V2['rows'][0]['q'].upper() + '") ARE COUNTED IN FULL. NATIONWIDE SEARCHES LIKE "DISPENSARY NEAR ME" ARE COUNTED BY POPULATION SHARE: ' + V2['label'].upper() + ' OUT OF ' + ('36,991,981 IN CANADA (2021)' if V2['cc']=='CA' else '331,449,281 IN THE U.S. (2020)') + '. 45% COUNTED AS AI SEARCHES (BRIGHTLOCAL 2026).') if V2 else hidden + 'VOLUME: GOOGLE ADS, NOV 2026, MONTHLY SEARCHES FROM ' + ', '.join(sorted(set(r['loc'].split(',')[0].upper() for r in KL))) + ', WITH 45% COUNTED AS AI SEARCHES (BRIGHTLOCAL 2026).')
        aud_js = json.dumps({'who': who})

    # Rule: Google hides most search volume for high-risk categories (cannabis and similar),
    # so their volumes are shown at 4x the measured number and labeled as estimates.
    svc = (J.get('biz', {}).get('svc', '') + ' ' + J.get('cq', '')).lower() if src != 'quiktox' else ''
    if re.search(r'dispens|cannabis|marijuana|weed|\bcbd\b|\bthc\b|vape|smoke shop|hemp|kratom|delta.?8', svc):
        VX = 4; data['volx'] = VX
        for r in data['rd'] + data['cr']:
            if r.get('v') is not None: r['v'] = r['v'] * VX
        for r in data['vp']: r[1] = r[1] * VX
        for r in data.get('packs') or []:
            if r.get('v') is not None: r['v'] = r['v'] * VX
    return data, aud_js

SETS = {}; AUDS = []
for src in SRCS:
    d, aj = make(src)
    slug = 'quiktox' if src == 'quiktox' else json.load(open(src))['slug']
    SETS[slug] = d; AUDS.append(json.dumps(slug) + ':' + aj)
t = open(D + 'hud.tpl.html').read()
ev = json.load(open(D + 'hud_ev.json')); lg = json.load(open(D + 'logos.json'))
lg['ChatGPT'] = lg['ChatGPT'].replace('fill="#111"', 'fill="#E3ECF8"').replace('fill="#fff"', 'fill="#050B15"')
t = t.replace('/*__EVCSS__*/', ev['css'])
t = t.replace('/*__DATA__*/', 'const SETS=' + json.dumps(SETS, ensure_ascii=False) + ';const AUDS={' + ','.join(AUDS) + '};const QP=new URLSearchParams(location.search),CUR=SETS[QP.get("b")]?QP.get("b"):"quiktox",DATA=SETS[CUR],AUD=AUDS[CUR];["ex","art","vo","rate"].forEach(k=>{if(DATA[k]==null)DATA[k]=SETS.quiktox[k]});if(QP.has("concept")){const f=+QP.get("concept")||4,m=v=>v==null?v:Math.round(v*f);(DATA.rd||[]).forEach(r=>r.v=m(r.v));(DATA.cr||[]).forEach(r=>r.v=m(r.v));(DATA.vp||[]).forEach(r=>r[1]=m(r[1]));(DATA.packs||[]).forEach(r=>r.v=m(r.v))}const EV=' + json.dumps({'ev': ev['ev'], 'ill': ev['ill'], 'fix': {x['c']: x['html'] for x in json.load(open(D + 'hud_fix.json'))}}, ensure_ascii=False) + ';const LOGOS=' + json.dumps(lg) + ';')
open(out, 'w').write(t); print('ok', out, len(t), list(SETS))
