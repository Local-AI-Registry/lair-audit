#!/usr/bin/env python3
"""Build a portfolio AI-visibility report for any multi-location account.

Usage:
    python3 _portfolio/build.py <account>/portfolio.config.json

The config names the location list, the raw scan folder written by the portfolio-scan
workflow, and where to write the report. See _portfolio/README.md.

Every number in the report comes from the raw scan files. Nothing is estimated except the
revenue math, which is labeled as an estimate (searches x 2.3% x average spend).
"""
import json, os, re, sys, glob, math, html, subprocess
from collections import Counter, defaultdict

RATE = 0.023
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def load(p, default=None):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def norm(s):
    s = (s or "").lower().replace("·", "").replace("&", "and")
    s = re.sub(r"\b(med ?spa|medspa|medical spa|aesthetics?|medaesthetics|wellness|clinic|center|centre|llc|pllc|inc|the)\b", " ", s)
    return re.sub(r"[^a-z0-9]", "", s)


def digits(s):
    d = re.sub(r"\D", "", s or "")
    return d[-10:] if len(d) >= 10 else d


def num(v):
    try:
        if v is None or v == "":
            return None
        return float(v)
    except Exception:
        return None


def g(d, *keys, default=None):
    for k in keys:
        if isinstance(d, dict) and d.get(k) is not None:
            return d[k]
    return default


def money(n):
    return "$" + f"{round(n):,}"


# ---------------------------------------------------------------- sister overlap
def _km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, [a["lat"], a["lng"], b["lat"], b["lng"]])
    return 6371 * 2 * math.asin(math.sqrt(math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))


def sister_overlap(L, raw_dir, radius=30):
    """Where locations of the same account sit close together, and where AI or Google names one in the other's answers."""
    import unicodedata
    an = lambda x: norm(unicodedata.normalize("NFKD", x or "").encode("ascii", "ignore").decode())
    geo = [l for l in L if l.get("lat") is not None and l.get("lng") is not None]
    bkeys = {}
    for l in geo:
        ks = {an(l["brand"])} | {an(l.get("title") or "")[:max(len(an(l["brand"])), 6)]}
        bkeys.setdefault(l["brand"], set()).update(k for k in ks if len(k) >= 4)
    def brand_of(name):
        n = an(name)
        hit = [b for b, ks in bkeys.items() if any(k in n for k in ks)]
        return max(hit, key=lambda b: max(len(k) for k in bkeys[b])) if hit else None
    pairs = []
    for i, a in enumerate(geo):
        for b in geo[i + 1:]:
            d = _km(a, b)
            if d <= radius:
                pairs.append({"a": a["slug"], "b": b["slug"], "km": round(d, 1), "same_brand": a["brand"] == b["brand"],
                              "a_named_b": {"ai_instead": 0, "ai_both": 0, "map": 0, "also": 0},
                              "b_named_a": {"ai_instead": 0, "ai_both": 0, "map": 0, "also": 0}})
    by = {(p["a"], p["b"]): p for p in pairs}
    S = {l["slug"]: l for l in geo}
    for l in geo:
        raw = load(os.path.join(raw_dir, l["slug"] + ".json")) or {}
        near = {}
        for p in pairs:
            o = p["b"] if p["a"] == l["slug"] else p["a"] if p["b"] == l["slug"] else None
            if o and not p["same_brand"]:
                near.setdefault(S[o]["brand"], []).append((p, "a_named_b" if p["a"] == l["slug"] else "b_named_a"))
        if not near:
            continue
        def credit(name, kind):
            b = brand_of(name)
            for p, side in near.get(b, [])[:1]:
                p[side][kind] += 1
        for q in raw.get("searches") or []:
            for n in (q.get("google") or {}).get("map_pack") or []:
                credit(n, "map")
            for e, a in (q.get("llm") or {}).items():
                a = a or {}
                if a.get("named") is None:
                    continue
                seen = {brand_of(n) for n in a.get("others") or []} - {None, l["brand"]}
                for b in seen:
                    for p, side in near.get(b, [])[:1]:
                        p[side]["ai_both" if a.get("named") in (1, True, "1") else "ai_instead"] += 1
        for x in (raw.get("listing") or {}).get("also_search") or []:
            credit(x.get("name") if isinstance(x, dict) else x, "also")
    pairs.sort(key=lambda p: (-(sum(p["a_named_b"].values()) + sum(p["b_named_a"].values())), p["km"]))
    within = lambda r, cross=False: sum(1 for a in geo if any(b is not a and (not cross or b["brand"] != a["brand"]) and _km(a, b) <= r for b in geo))
    return {"radius_km": radius, "pairs": pairs, "near5": within(5), "near10": within(10), "near15": within(15),
            "cross10": within(10, True), "cross15": within(15, True)}


# ---------------------------------------------------------------- per location
ENGINES = ["chat_gpt", "gemini", "claude", "perplexity"]
ENGINE_LABEL = {"chat_gpt": "ChatGPT", "gemini": "Gemini", "claude": "Claude", "perplexity": "Perplexity"}


def score_location(loc, raw, family=frozenset()):
    lst = raw.get("listing") or {}
    searches = raw.get("searches") or []
    brand_key = norm(loc["brand"])
    self_keys = {brand_key, norm(loc["name"]), norm(lst.get("title"))} - {""}

    def is_self(name):
        # the location itself, or any other location of the same account (rivals are local competitors only)
        n = norm(name)
        return bool(n) and any(k and (k in n or n in k) for k in (self_keys | family) if len(k) >= 4)

    hits = slots = 0
    llm_named = llm_total = 0
    eng = {e: [0, 0] for e in ENGINES}
    g_hits = g_total = 0
    map_hits = 0
    aio_named = aio_seen = 0
    rivals = Counter()
    rival_names = {}
    per_search = []
    for s in searches:
        gg = s.get("google") or {}
        mp = num(gg.get("map_pos"))
        op = num(gg.get("organic_pos"))
        if gg:
            hit = 1 if (mp is not None or (op is not None and op <= 10)) else 0
            hits += hit; slots += 1; g_hits += hit; g_total += 1
            if mp is not None:
                map_hits += 1
        aio = (gg.get("aio") or "").lower()
        if aio in ("named", "not_named"):
            aio_seen += 1; slots += 1
            if aio == "named":
                aio_named += 1; hits += 1
        for name in gg.get("map_pack") or []:
            if not is_self(name):
                k = norm(name); rivals[k] += 1; rival_names.setdefault(k, name)
        llm = s.get("llm") or {}
        row = {"q": s.get("q") or s.get("prompt"), "map": mp, "org": op, "aio": aio or None, "e": {}}
        for e in ENGINES:
            a = llm.get(e) or {}
            v = a.get("named")
            if v is None:
                row["e"][e] = None
                continue
            v = 1 if v in (1, True, "1") else 0
            row["e"][e] = v
            llm_total += 1; llm_named += v; slots += 1; hits += v
            eng[e][1] += 1; eng[e][0] += v
            for name in a.get("others") or []:
                if not is_self(name):
                    k = norm(name)
                    if k:
                        rivals[k] += 1; rival_names.setdefault(k, name)
        per_search.append(row)

    top_rivals = [{"name": rival_names[k], "n": n} for k, n in rivals.most_common(5)]
    stars = lst.get("stars") or {}
    phone_ok = g(lst, "phone_matches_source", "phone_matches_amp")
    if phone_ok is None and lst.get("google_phone"):
        phone_ok = digits(lst.get("google_phone")) == digits(loc.get("phone"))
    site_ok = g(lst, "site_matches_source", "site_matches_amp")
    prices = []
    for p in lst.get("prices") or []:
        v = num(g(p, "price_usd", "price"))
        if v and v > 0:
            prices.append({"t": p.get("title"), "c": p.get("category"), "p": v})
    return {
        "slug": loc["slug"], "name": loc["name"], "brand": loc["brand"], "city": loc["city"], "state": loc["state"],
        "lat": loc.get("lat"), "lng": loc.get("lng"), "src_phone": loc.get("phone"), "src_site": loc.get("website"),
        "found": lst.get("found", bool(lst.get("title"))),
        "title": lst.get("title"), "g_phone": lst.get("google_phone"), "phone_ok": phone_ok, "site_ok": site_ok,
        "site_url": lst.get("site_url"), "pin_km": num(lst.get("distance_km")),
        "category": lst.get("category"), "n_cats": len(lst.get("categories") or []),
        "rating": num(lst.get("rating")), "reviews": int(num(lst.get("reviews")) or 0),
        "one_star": int(num(stars.get("1")) or 0) if stars else None,
        "photos": int(num(lst.get("photos")) or 0), "claimed": lst.get("claimed"), "has_desc": lst.get("has_description"),
        "attrs": lst.get("attributes_count"), "topics": (lst.get("topics") or [])[:8],
        "services_count": lst.get("services_count"), "prices": prices,
        "also": (lst.get("also_search") or [])[:5], "hours": num(lst.get("weekly_open_hours")),
        "svc": raw.get("svc") or "med spa",
        "score": round(100 * hits / slots) if slots else None, "slots": slots, "hits": hits,
        "llm_named": llm_named, "llm_total": llm_total,
        "eng": {e: eng[e] for e in ENGINES},
        "google_hits": g_hits, "google_total": g_total, "map_hits": map_hits,
        "aio_named": aio_named, "aio_seen": aio_seen,
        "rivals": top_rivals, "searches": per_search, "notes": raw.get("notes") or [],
    }


# ---------------------------------------------------------------- helpers for aggregates
def avg(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def pct(a, b):
    return round(100 * a / b) if b else None


PRODUCT_BRANDS = [  # product and treatment brands patients search by name
    ("Botox", r"botox"), ("Dysport", r"dysport"), ("Xeomin", r"xeomin"), ("Jeuveau", r"jeuveau"), ("Daxxify", r"daxx"),
    ("Juvederm", r"juv[eé]derm"), ("Restylane", r"restylane"), ("Sculptra", r"sculptra"), ("Kybella", r"kybella"),
    ("HydraFacial", r"hydra ?facial"), ("DiamondGlow", r"diamond ?glow"), ("Morpheus8", r"morpheus"),
    ("CoolSculpting", r"cool ?sculpt"), ("Emsculpt", r"emsculpt"), ("Semaglutide / GLP-1", r"semaglut|tirzepat|glp|wegovy|ozempic"),
    ("Microneedling", r"microneedl|skinpen"), ("Laser hair removal", r"laser hair|hair removal|\blhr\b"),
]
TREND_KEY = {"Botox": "botox", "Daxxify": "daxxify", "Sculptra": "sculptra", "HydraFacial": "hydrafacial", "Morpheus8": "morpheus8",
             "CoolSculpting": "coolsculpting", "Semaglutide / GLP-1": "semaglutide", "Microneedling": "microneedling", "Laser hair removal": "laser hair removal"}


SERVICE_KEYS = [
    ("Botox / neurotoxin", r"botox|dysport|xeomin|jeuveau|daxxify|neurotox|tox\b|wrinkle relax"),
    ("Dermal filler", r"filler|juvederm|restylane|rha|lip"),
    ("HydraFacial", r"hydrafacial|hydra ?facial"),
    ("Microneedling", r"microneedl|morpheus|rf micro|skinpen"),
    ("Laser hair removal", r"laser hair|lhr|hair removal|hair reduction"),
    ("Body contouring", r"coolsculpt|emsculpt|body contour|sculpsure|fat"),
    ("Weight loss (GLP-1)", r"semaglut|tirzepat|weight|glp"),
    ("Chemical peel", r"peel"),
    ("IV therapy", r"\biv\b|drip|infusion"),
]


def service_of(title):
    t = (title or "").lower()
    for name, rx in SERVICE_KEYS:
        if re.search(rx, t):
            return name
    return None


# ---------------------------------------------------------------- spotlights: specific, real examples
def spotlights(L, acc_short):
    """Specific, real examples framed as opportunities. Each names a location, its numbers and its local rival."""
    out, used = [], set()
    scored = [l for l in L if l["score"] is not None]

    def eng_line(l):
        return ", ".join(f"{ENGINE_LABEL[e]} {l['eng'][e][0]}/{l['eng'][e][1]}" for e in ENGINES if l["eng"][e][1])

    def add(card, l=None):
        if l is not None:
            used.add(l["slug"])
        out.append(card)

    # 1. Biggest prize: highest-value market where a rival leads
    tr = [l for l in scored if l.get("h2h") == "trail" and l.get("worth")]
    if tr:
        l = max(tr, key=lambda x: x["worth"])
        add({"k": "prize", "tag": "The biggest prize", "loc": l["name"], "slug": l["slug"], "big": f"{money(l['worth'])}/mo",
             "text": f"{l['name']} sits in the portfolio's most valuable market: about {money(l['worth'])} a month in local searches. Today AI names {l['rival']} {l['rival_n']} times and {l['name']} {l['own_n']}. Every share point won here is worth more than anywhere else."}, l)
    # 2. Earned trust, not yet credited by AI
    c = [l for l in scored if l.get("review_x") and l["review_x"] >= 2 and l["llm_total"] and l["llm_named"] / l["llm_total"] <= 0.34 and l["slug"] not in used]
    if c:
        l = max(c, key=lambda x: x["review_x"])
        add({"k": "trust", "tag": "Trust already earned", "loc": l["name"], "slug": l["slug"], "big": f"{l['review_x']}× the reviews",
             "text": f"{l['name']} has {l['reviews']:,} Google reviews, {l['review_x']}× the local competitors Google pairs it with (median {int(l['comp_reviews']):,}). AI named it in only {l['llm_named']} of {l['llm_total']} answers and named {l['rival']} {l['rival_n']} times. The reputation is there; AI just can't see it yet."}, l)
    # 3. Closest race
    c = [l for l in scored if l.get("margin") == -1 and l["slug"] not in used] or [l for l in scored if l.get("margin", 0) in (-2, -3) and l["slug"] not in used]
    if c:
        l = max(c, key=lambda x: x.get("worth", 0))
        add({"k": "close", "tag": "One step from the top", "loc": l["name"], "slug": l["slug"], "big": f"{l['own_n']} vs {l['rival_n']}",
             "text": f"{l['name']} trails {l['rival']} by {-l['margin']} mention{'s' if l['margin'] < -1 else ''} across AI answers and Google's map pack. A handful of fixes moves it to first in its market."}, l)
    # 4. Already the local answer
    c = [l for l in scored if l.get("h2h") == "lead" and l["slug"] not in used]
    if c:
        l = max(c, key=lambda x: (x["margin"], x["reviews"]))
        add({"k": "champion", "tag": "Already the local answer", "loc": l["name"], "slug": l["slug"], "big": f"{l['own_n']} vs {l['rival_n']}",
             "text": f"{l['name']} is named {l['own_n']} times against {l['rival_n']} for its closest rival, {l['rival']} ({eng_line(l)}). This is what every AMP location can look like, and it's worth defending."}, l)
    # 5. Ready for AI: wins Google maps, not AI
    c = [l for l in scored if l["map_hits"] >= 2 and l["llm_total"] and l["llm_named"] / l["llm_total"] <= 0.5 and l["slug"] not in used]
    if c:
        l = min(c, key=lambda x: x["llm_named"] / x["llm_total"])
        add({"k": "ready", "tag": "Winning Google, ready for AI", "loc": l["name"], "slug": l["slug"], "big": f"Map {l['map_hits']}/3 · AI {l['llm_named']}/{l['llm_total']}",
             "text": f"{l['name']} already holds Google's map pack for {l['map_hits']} of 3 searches. AI tools name it in {l['llm_named']} of {l['llm_total']} answers. The local authority exists; it needs to reach the sources AI reads."}, l)
    # 6. Phones
    mm = [l for l in L if l["phone_ok"] is False and l["g_phone"]]
    if mm:
        l = mm[0]
        add({"k": "phones", "tag": f"One fix, {len(mm)} locations", "loc": "Phone numbers", "slug": l["slug"], "big": f"{len(mm)} of {len(L)}",
             "text": f"{len(mm)} of {len(L)} locations show a different phone on Google than on {acc_short}'s own site (for example {l['name']}: {l['g_phone']} on Google, {l['src_phone']} on the site). Many are call-tracking numbers. Setting one main number per location, everywhere, removes a doubt AI applies to every one of them."})
    # 7. Shared phones
    by_phone = defaultdict(list)
    for l in L:
        if digits(l["src_phone"]):
            by_phone[digits(l["src_phone"])].append(l)
    shared = sorted([v for v in by_phone.values() if len(v) > 1], key=len, reverse=True)
    if shared:
        v = shared[0]
        add({"k": "shared_phone", "tag": "Give every location its own voice", "loc": v[0]["brand"], "slug": v[0]["slug"], "big": f"{len(v)} locations, 1 number",
             "text": f"{v[0]['brand']} lists {v[0]['src_phone']} for {len(v)} locations ({', '.join(x['city'] for x in v)}). Search engines and AI can't tell them apart, so they compete for one identity instead of winning five markets. {sum(len(x) for x in shared)} locations share a number today."})
    # 8. One AI tool away
    splits = []
    for l in scored:
        r = {e: (l["eng"][e][0] / l["eng"][e][1]) for e in ENGINES if l["eng"][e][1]}
        if len(r) >= 3 and l["slug"] not in used:
            hi_e, lo_e = max(r, key=r.get), min(r, key=r.get)
            splits.append((r[hi_e] - r[lo_e], l, hi_e, lo_e))
    if splits:
        d_, l, hi_e, lo_e = max(splits, key=lambda x: (x[0], x[1]["reviews"]))
        if d_ >= 0.66:
            add({"k": "split", "tag": "One AI tool away", "loc": l["name"], "slug": l["slug"], "big": f"{ENGINE_LABEL[hi_e]} {l['eng'][hi_e][0]}/{l['eng'][hi_e][1]} · {ENGINE_LABEL[lo_e]} {l['eng'][lo_e][0]}/{l['eng'][lo_e][1]}",
                 "text": f"{ENGINE_LABEL[hi_e]} already recommends {l['name']} every time; {ENGINE_LABEL[lo_e]} hasn't yet. Each AI reads different sources, so closing this gap is a targeted job, not a rebuild."}, l)
    # 9. Prices AI can quote
    no_price = [l for l in L if not l["prices"]]
    if no_price:
        add({"k": "price", "tag": "Prices AI can quote", "loc": "Google profiles", "slug": None, "big": f"{len(L) - len(no_price)} of {len(L)}",
             "text": f"Only {len(L) - len(no_price)} of {len(L)} {acc_short} Google profiles show any price. When a patient asks AI what a treatment costs nearby, it quotes the competitors that publish one."})
    return out


# ---------------------------------------------------------------- build
def main(cfg_path):
    cfg = load(cfg_path)
    base = os.path.dirname(os.path.abspath(cfg_path))
    rp = lambda p: p if os.path.isabs(p) else os.path.join(ROOT, p)
    locs = load(rp(cfg["locations_file"]))
    raw_dir = rp(cfg["raw_dir"])
    acc = cfg["account"]
    L, missing = [], []
    family = set()
    for loc in locs:
        family |= {norm(loc["brand"]), norm(loc["name"])}
        rr = load(os.path.join(raw_dir, loc["slug"] + ".json")) or {}
        family.add(norm((rr.get("listing") or {}).get("title")))
    family = frozenset(k for k in family if k and len(k) >= 4)
    for loc in locs:
        raw = load(os.path.join(raw_dir, loc["slug"] + ".json"))
        if not raw:
            missing.append(loc["slug"]); continue
        L.append(score_location(loc, raw, family))

    # head-to-head with the top local rival, and reviews against local competitors
    own_names = {norm(l["title"] or l["name"]) for l in L} | {norm(l["name"]) for l in L}
    for l in L:
        own = l["llm_named"] + l["map_hits"]
        r = l["rivals"][0] if l["rivals"] else {"name": None, "n": 0}
        l["own_n"], l["rival"], l["rival_n"] = own, r["name"], r["n"]
        l["margin"] = own - r["n"]
        l["h2h"] = "lead" if l["margin"] > 0 else "tie" if l["margin"] == 0 else "trail"
        comps = [a for a in l["also"] if isinstance(a, dict) and a.get("reviews") and norm(a.get("name")) not in own_names]
        if comps:
            rv = sorted(num(a["reviews"]) for a in comps)
            l["comp_reviews"] = rv[len(rv) // 2]
            l["comp_rating"] = round(avg([num(a.get("rating")) for a in comps]) or 0, 2)
            l["review_x"] = round(l["reviews"] / l["comp_reviews"], 1) if l["comp_reviews"] else None
        else:
            l["comp_reviews"] = l["comp_rating"] = l["review_x"] = None

    # domains, trends, volumes
    domains = {}
    for f in sorted(glob.glob(os.path.join(raw_dir, "_domains_*.json"))):
        d = load(f, {})
        for x in (d.get("domains") if isinstance(d, dict) else d) or []:
            if x.get("domain"):
                domains[x["domain"].replace("www.", "")] = x
    trends = load(os.path.join(raw_dir, "_trends.json"), {}) or {}
    vols = {}
    for f in sorted(glob.glob(os.path.join(raw_dir, "_volumes_*.json"))):
        d = load(f, {})
        for x in (d.get("locations") if isinstance(d, dict) else d) or []:
            if x.get("slug"):
                vols[x["slug"]] = x

    price = cfg.get("price") or {"value": 527, "label": "average spend per US med spa visit",
                                  "source": "American Med Spa Association, 2024 Medical Spa State of the Industry report",
                                  "url": "https://www.americanmedspa.org/news/2024-medical-spa-state-of-the-industry-executive-report-recap/"}
    worth_rows = []
    # locations of the same account in the same city share that city's searches (no double counting)
    share_near, share_town = Counter(), Counter()
    for l in L:
        v = vols.get(l["slug"]) or {}
        share_near[(v.get("near_me_location") or f"{l['city']},{l['state']}").lower()] += 1
        share_town[(l["city"].lower(), l["state"])] += 1
    for l in L:
        v = vols.get(l["slug"]) or {}
        nk = (v.get("near_me_location") or f"{l['city']},{l['state']}").lower()
        l["shared_with"] = max(share_near[nk], share_town[(l["city"].lower(), l["state"])]) - 1
        town = sum(int(num(x) or 0) for x in (v.get("town") or {}).values()) / share_town[(l["city"].lower(), l["state"])]
        near = sum(int(num(x) or 0) for x in (v.get("near_me") or {}).values()) / share_near[nk]
        town, near = round(town), round(near)
        l["vol"] = town + near
        l["vol_town"], l["vol_near"] = town, near
        l["worth"] = round(l["vol"] * RATE * price["value"])
        if l["vol"]:
            worth_rows.append([f"local {l['svc']}, Botox, lip filler and laser hair searches" + (f" (city split {l['shared_with'] + 1} ways)" if l["shared_with"] else ""), l["vol"], l["name"]])

    # brands
    brands = []
    for b in sorted({l["brand"] for l in L}):
        bl = [l for l in L if l["brand"] == b]
        dom = None
        for l in bl:
            dd = re.sub(r"^https?://(www\.)?", "", l["src_site"] or "").split("/")[0]
            if dd in domains:
                dom = domains[dd]; break
        brands.append({
            "brand": b, "n": len(bl), "states": sorted({l["state"] for l in bl}),
            "score": round(avg([l["score"] for l in bl]) or 0), "ai": pct(sum(l["llm_named"] for l in bl), sum(l["llm_total"] for l in bl)),
            "map": pct(sum(l["map_hits"] for l in bl), sum(l["google_total"] for l in bl)),
            "rating": round(avg([l["rating"] for l in bl]) or 0, 2), "reviews": sum(l["reviews"] for l in bl),
            "phone_mm": sum(1 for l in bl if l["phone_ok"] is False), "worth": sum(l.get("worth", 0) for l in bl),
            "domain": dom,
        })
    brands.sort(key=lambda x: -x["score"])

    # states
    states = []
    for st in sorted({l["state"] for l in L}):
        sl = [l for l in L if l["state"] == st]
        states.append({"st": st, "n": len(sl), "score": round(avg([l["score"] for l in sl]) or 0)})

    # rivals across portfolio (business AI names instead, counted once per location)
    riv = Counter(); riv_where = defaultdict(list)
    for l in L:
        for r in l["rivals"][:3]:
            riv[r["name"]] += r["n"]; riv_where[r["name"]].append(l["city"])

    # services coverage
    cov = Counter(); price_by = defaultdict(list)
    for l in L:
        seen = set()
        for p in l["prices"]:
            s = service_of(p["t"])
            if s and not (s in ("Botox / neurotoxin", "Dermal filler") and p["p"] < 50):  # per-unit prices
                price_by[s].append(p["p"])
                if s not in seen:
                    cov[s] += 1; seen.add(s)
    services = [{"s": s, "locations": cov[s], "min": min(price_by[s]), "max": max(price_by[s]), "median": sorted(price_by[s])[len(price_by[s]) // 2]} for s in cov]
    services.sort(key=lambda x: -x["locations"])

    topics = Counter()
    for l in L:
        for t in l["topics"]:
            if isinstance(t, dict) and t.get("t"):
                topics[t["t"].lower()] += int(num(t.get("n")) or 1)

    pb_rows = []
    trend_by = {t.get("term"): t for t in (trends.get("treatments") or [])}
    for name, rx in PRODUCT_BRANDS:
        priced = mentioned = mentions = 0
        for loc in locs:
            raw = load(os.path.join(raw_dir, loc["slug"] + ".json")) or {}
            li = raw.get("listing") or {}
            pt = " ".join(f"{p.get('title') or ''} {p.get('category') or ''}" for p in li.get("prices") or [] if (num(g(p, "price_usd", "price")) or 0) > 0).lower()
            tps = [t for t in (li.get("topics") or []) if isinstance(t, dict)]
            if re.search(rx, pt): priced += 1
            hit = [t for t in tps if re.search(rx, (t.get("t") or "").lower())]
            if hit: mentioned += 1; mentions += sum(int(num(t.get("n")) or 0) for t in hit)
        t = trend_by.get(TREND_KEY.get(name, ""), {})
        if priced or mentioned or t:
            pb_rows.append({"b": name, "priced": priced, "mentioned": mentioned, "mentions": mentions,
                            "us_vol": t.get("us_search_volume"), "change": t.get("change_pct")})
    pb_rows.sort(key=lambda x: -(x["us_vol"] or 0))
    any_price = sum(1 for l in L if l["prices"])

    eng_tot = {e: [sum(l["eng"][e][0] for l in L), sum(l["eng"][e][1] for l in L)] for e in ENGINES}
    sc = [l["score"] for l in L if l["score"] is not None]
    kpi = {
        "locations": len(L), "brands": len(brands), "states": len(states), "missing": missing,
        "avg_score": round(avg(sc) or 0), "median_score": sorted(sc)[len(sc) // 2] if sc else None,
        "ai_rate": pct(sum(l["llm_named"] for l in L), sum(l["llm_total"] for l in L)),
        "map_rate": pct(sum(l["map_hits"] for l in L), sum(l["google_total"] for l in L)),
        "reviews": sum(l["reviews"] for l in L), "rating": round(avg([l["rating"] for l in L]) or 0, 2),
        "phone_mm": sum(1 for l in L if l["phone_ok"] is False), "phone_checked": sum(1 for l in L if l["phone_ok"] is not None),
        "pin_off": sum(1 for l in L if (l["pin_km"] or 0) >= 2),
        "site_mm": sum(1 for l in L if l["site_ok"] is False),
        "unclaimed": sum(1 for l in L if l["claimed"] is False),
        "no_desc": sum(1 for l in L if l["has_desc"] is False),
        "worth": sum(l.get("worth", 0) for l in L), "vol": sum(l.get("vol", 0) for l in L),
        "invisible": sum(1 for l in L if l["llm_total"] and l["llm_named"] == 0),
        "lead": sum(1 for l in L if l["h2h"] == "lead"), "tie": sum(1 for l in L if l["h2h"] == "tie"), "trail": sum(1 for l in L if l["h2h"] == "trail"),
        "trail_worth": sum(l.get("worth", 0) for l in L if l["h2h"] == "trail"),
        "reach": sum(1 for l in L if -3 <= l["margin"] < 0), "reach_worth": sum(l.get("worth", 0) for l in L if -3 <= l["margin"] < 0),
        "review_adv": sum(1 for l in L if l["review_x"] and l["review_x"] > 1), "review_cmp": sum(1 for l in L if l["review_x"]),
        "any_price": any_price,
        "eng": eng_tot,
    }
    # owner-level cuts of the data
    def pearson(xs, ys):
        pts = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
        if len(pts) < 5:
            return None
        mx = sum(p[0] for p in pts) / len(pts); my = sum(p[1] for p in pts) / len(pts)
        sx = math.sqrt(sum((p[0] - mx) ** 2 for p in pts)); sy = math.sqrt(sum((p[1] - my) ** 2 for p in pts))
        return sum((p[0] - mx) * (p[1] - my) for p in pts) / (sx * sy) if sx and sy else None
    ins = []
    k_lead = sum(1 for l in L if l["h2h"] == "lead"); k_trail = [l for l in L if l["h2h"] != "lead"]
    tw = sum(l.get("worth", 0) for l in L); trw = sum(l.get("worth", 0) for l in k_trail)
    ins.append({"big": f"{k_lead} of {len(L)}", "h": "Markets where AI already picks " + (acc.get("short") or "you") + " first",
                "p": f"In {k_lead} markets the {acc.get('short')} location is named more often than its closest local rival. The other {len(k_trail)} are the growth opportunity: they hold {money(trw)} of the {money(tw)} a month in local searches at stake."})
    reach = sorted([l for l in L if -3 <= l["margin"] < 0], key=lambda x: -x.get("worth", 0))
    if reach:
        ins.append({"big": f"{len(reach)}", "h": "Close races, ready to win",
                    "p": f"{len(reach)} locations trail their local leader by 3 mentions or fewer, worth {money(sum(l.get('worth', 0) for l in reach))} a month together: " + ", ".join(f"{l['name']} (vs {l['rival']}, {l['own_n']}–{l['rival_n']})" for l in reach[:3]) + "."})
    rx = [l for l in L if l["review_x"]]
    if rx:
        adv = [l for l in rx if l["review_x"] > 1]
        gap = sorted([l for l in adv if l["llm_total"] and l["llm_named"] / l["llm_total"] <= 0.34], key=lambda x: -x["review_x"])
        ins.append({"big": f"{len(adv)} of {len(rx)}", "h": "The reputation is already earned",
                    "p": f"In {len(adv)} of {len(rx)} markets, the {acc.get('short')} location has more Google reviews than the local competitors Google pairs it with. AI doesn't credit it yet: " + "; ".join(f"{l['name']} has {l['reviews']:,} reviews ({l['review_x']}× local) and is named in {l['llm_named']} of {l['llm_total']} answers" for l in gap[:3]) + "."})
    wsorted = sorted(L, key=lambda x: -x.get("worth", 0))
    if tw:
        t10 = sum(l.get("worth", 0) for l in wsorted[:10])
        ins.append({"big": f"{round(100 * t10 / tw)}%", "h": "Where the growth is concentrated",
                    "p": f"The 10 busiest markets hold {round(100 * t10 / tw)}% of the value: " + ", ".join(f"{l['name']} ({money(l['worth'])}/mo, named {l['own_n']}× vs {l['rival'] or 'rivals'} {l['rival_n']}×)" for l in wsorted[:3]) + "."})
    np_ = sum(1 for l in L if not l["prices"])
    ins.append({"big": f"{len(L) - np_} of {len(L)}", "h": "Google profiles that show a price",
                "p": f"AI answers cost questions with published prices. {np_} {acc.get('short')} profiles show none, so AI quotes competitors instead. Adding a price menu is one of the fastest wins available."})
    data = {
        "account": acc, "prepared_for": cfg.get("prepared_for"), "date": cfg.get("date"), "price": price,
        "kpi": kpi, "locations": L, "brands": brands, "states": states,
        "rivals": [{"name": n, "n": c, "where": sorted(set(riv_where[n]))[:6]} for n, c in riv.most_common(15)],
        "services": services, "topics": topics.most_common(12), "trends": trends,
        "spotlights": spotlights(L, acc.get("short") or acc.get("name")), "insights": ins, "products": pb_rows,
        "audits": cfg.get("audits") or {}, "sisters": sister_overlap(L, raw_dir),
    }

    # "What being AI's answer is worth" section via _template/worth.py (house rule)
    worth_html = ""
    if worth_rows:
        wj = {"client": acc.get("name"), "rows": worth_rows, "price": price,
              "vol_source": cfg.get("vol_source", "DataForSEO, Google Ads search volume; town searches at state level, 'near me' at city level"),
              "left_out": "One row per location: the sum of its town searches (med spa, Botox, lip filler, laser hair removal + town) and the same four 'near me' searches in its city. Where several locations share a city, that city's searches are split evenly between them. Searches with no volume are left out."}
        wdir = os.path.dirname(rp(cfg["out"])); os.makedirs(wdir, exist_ok=True)
        wpath = os.path.join(wdir, "worth.json")
        with open(wpath, "w", encoding="utf-8") as f:
            json.dump(wj, f, indent=1, ensure_ascii=False)
        worth_html = subprocess.run([sys.executable, os.path.join(ROOT, "_template", "worth.py"), wpath], capture_output=True, text=True).stdout
    worth_css = open(os.path.join(ROOT, "_template", "worth.css"), encoding="utf-8").read()

    tpl = open(os.path.join(HERE, "report.tpl.html"), encoding="utf-8").read()
    out = (tpl.replace("{{TITLE}}", html.escape(cfg.get("title") or f"{acc.get('short')} Portfolio AI Report"))
              .replace("{{ACCOUNT}}", html.escape(acc.get("name", "")))
              .replace("/*{{WORTH_CSS}}*/", worth_css)
              .replace("<!--{{WORTH}}-->", worth_html)
              .replace("/*{{DATA}}*/null", json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")))
    op = rp(cfg["out"])
    os.makedirs(os.path.dirname(op), exist_ok=True)
    with open(op, "w", encoding="utf-8") as f:
        f.write(out)
    with open(os.path.join(os.path.dirname(op), "data.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"Built {op}: {len(L)} locations scored, {len(missing)} missing, {len(data['spotlights'])} spotlights, worth {money(kpi['worth'])}/mo")


if __name__ == "__main__":
    main(sys.argv[1])
