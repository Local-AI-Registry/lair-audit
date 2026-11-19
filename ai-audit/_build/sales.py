"""Build the main ai-audit page (ai-audit/index.html), the sales-call version of the audit.
usage: python3 sales.py ../index.html biz/<slug>.json [biz/<slug>.json ...]
Reuses make() from hudbuild3.py so the numbers match the current tool exactly."""
import json, os, re, sys
D = os.path.dirname(os.path.abspath(__file__)) + '/'
out, SRCS = sys.argv[1], sys.argv[2:]
src = open(D + 'hudbuild3.py').read()
ns = {'__file__': D + 'hudbuild3.py'}
argv = sys.argv; sys.argv = ['hudbuild3.py', '/dev/null']
exec(src[:src.index('SETS = {}; AUDS = []')], ns)
sys.argv = argv
KEEP = ['biz', 'hit', 'score', 'rd', 'cr', 'vp', 'S', 'months', 'aud2', 'volx', 'packs', 'found']
SETS = {}
for s in SRCS:
    J = json.load(open(D + s if not os.path.isabs(s) else s))
    d, aud_js = ns['make'](D + s)
    p = {k: d[k] for k in KEEP if k in d}
    p['biz'] = dict(p['biz'], svc=J['biz'].get('svc', ''), short=J['biz'].get('short'))
    p['ct'] = [{'c': c['c'], 'st': c['st'], 'i': c['i']} for c in d['ct']]
    p['who'] = json.loads(aud_js)['who']
    p['scan'] = J.get('scan')
    pr = J.get('price') or {}
    if pr.get('value'):
        cur = '' if pr.get('currency') in (None, 'USD') else pr['currency'] + ' '
        p['priceLabel'] = 'Starts at the %s: %s$%s (%s)' % (pr.get('label', 'average spend'), cur, round(pr['value']), pr.get('source', ''))
    SETS[J['slug']] = p
VO = {v['n']: v for v in json.load(open(D + 'vouch.json'))}
PICK = ['Dr. Sachin Shridharani', 'Dr. Doris Day', 'Dr. Deepak Dugar', 'Dr. Tess Mauricio', 'Naomi Barrett, NP-C', 'Linda Rank, PA-C',
        'Dr. Mariano Busso', 'Dr. Ashish Bhatia', 'Dr. Marie Hayag', 'Dr. Roberta Del Campo']
FACES = []
import base64, os
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(out)), 'faces'), exist_ok=True)
for k, n in enumerate(n for n in PICK if n in VO and VO[n].get('f')):
    f = VO[n]['f']
    m = re.match(r'data:image/(\w+);base64,(.*)', f, re.S)
    if m:  # written next to the page as faces/<k>.<ext>, so the page stays small
        ext = 'jpg' if m.group(1) == 'jpeg' else m.group(1)
        open(os.path.join(os.path.dirname(os.path.abspath(out)), 'faces', '%d.%s' % (k, ext)), 'wb').write(base64.b64decode(m.group(2)))
        f = 'faces/%d.%s' % (k, ext)
    FACES.append({'n': n, 'f': f})
PRESS = []
for a in json.load(open(D + 'art.json')):
    m = re.sub(r'<[^>]+>', '', a['m']).strip()
    m = {'IPSNEWS': 'IPS News', 'THE SILICON REVIEW': 'The Silicon Review'}.get(m, m)
    if m not in PRESS: PRESS.append(m)
# shared proposal content from the classic page: the agency comparison and the 12-month plan
EX = json.load(open(D + 'extract.json'))
CMP = EX['cmp']
L = EX['plan'].split('\n'); i = L.index('NOV') + 1; PLAN12 = []
for j in range(i, len(L) - 1, 2):
    if re.match(r'^(Year-in-review|Work streams)', L[j]): break
    PLAN12.append([L[j], L[j + 1]])
t = open(D + 'sales.tpl.html').read()
# the verified business record is called the Blueprint on this page
def blueprint(x):
    if isinstance(x, list):
        return [blueprint(y) for y in x]
    return re.sub(r'\b(?:Registry )?[Rr]ecord\b', 'Blueprint', x) if isinstance(x, str) else x
CMP, PLAN12 = blueprint(CMP), blueprint(PLAN12)
data = 'const SETS=' + json.dumps(SETS, ensure_ascii=False) + ';const FACES=' + json.dumps(FACES) + ';const PRESS=' + json.dumps(PRESS) + ';const CMP=' + json.dumps(CMP, ensure_ascii=False) + ';const PLAN12=' + json.dumps(PLAN12) + ';'
t = t.replace('/*__DATA__*/', data.replace('</', '<\\/'))
os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
# the 11 "how we fix it" illustrations (from the classic page) go in their own file, loaded only when the Blueprint slide opens
def blueprint_ill(h):  # the classic drawings say "record"; this page calls it the Blueprint
    # matches the motion files the team shared (LAIR-11-checks-animations): BLUEPRINT tile, "Your Blueprint(TM)"
    h = h.replace('fill="#fff">RECORD<', 'fill="#fff">BLUEPRINT<')
    return h.replace('>Your record<', '>Your Blueprint\u2122<').replace('Your record', 'Your Blueprint').replace('your record', 'your Blueprint')
json.dump({x['c']: blueprint_ill(x['html']) for x in json.load(open(D + 'hud_fix.json'))},
          open(os.path.join(os.path.dirname(os.path.abspath(out)), 'fix-ill.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
open(out, 'w').write(t); print('ok', out, len(t), list(SETS))
