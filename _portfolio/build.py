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


# ---------------------------------------------------------------- per location
ENGINES = ["chat_gpt", "gemini", "claude", "perplexity"]
ENGINE_LABEL = {"chat_gpt": "ChatGPT", "gemini": "Gemini", "claude": "Claude", "perplexity": "Perplexity"}


def score_location(loc, raw):
    lst = raw.get("listing") or {}
    searches = raw.get("searches") or []
    brand_key = norm(loc["brand"])
    self_keys = {brand_key, norm(loc["name"]), norm(lst.get("title"))} - {""}

    def is_self(name):
        n = norm(name)
        return bool(n) and any(k and (k in n or n in k) for k in self_keys if len(k) >= 4)

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
    out = []
    scored = [l for l in L if l["score"] is not None]

    def eng_line(l):
        return ", ".join(f"{ENGINE_LABEL[e]} {l['eng'][e][0]}/{l['eng'][e][1]}" for e in ENGINES if l["eng"][e][1])

    # 1. Strong on Google reviews, weak in AI
    cands = [l for l in scored if l["llm_total"] and l["llm_named"] / l["llm_total"] <= 0.34 and l["reviews"]]
    if cands:
        l = max(cands, key=lambda x: x["reviews"])
        r = l["rivals"][0] if l["rivals"] else None
        out.append({"k": "invisible", "tag": "Loved by patients, missing in AI", "loc": l["name"], "slug": l["slug"],
                    "big": f"{l['llm_named']} of {l['llm_total']}",
                    "text": f"{l['name']} has {l['reviews']:,} Google reviews at {l['rating']}★, yet AI named it in only {l['llm_named']} of {l['llm_total']} answers ({eng_line(l)})."
                            + (f" The business AI named most instead: {r['name']} ({r['n']} times)." if r else "")})
    # 2. Google ranks it, AI ignores it
    cands = [l for l in scored if l["map_hits"] >= 2 and l["llm_total"] and l["llm_named"] / l["llm_total"] <= 0.5 and l["slug"] not in {o.get("slug") for o in out}]
    if cands:
        l = min(cands, key=lambda x: x["llm_named"] / x["llm_total"])
        out.append({"k": "map_not_ai", "tag": "Wins on Google Maps, loses in AI", "loc": l["name"], "slug": l["slug"],
                    "big": f"Map {l['map_hits']}/3 · AI {l['llm_named']}/{l['llm_total']}",
                    "text": f"{l['name']} is in Google's map pack for {l['map_hits']} of 3 searches, but AI tools named it in only {l['llm_named']} of {l['llm_total']} answers. Ranking on Google no longer guarantees being AI's answer."})
    # 3. AI champion
    if scored:
        l = max(scored, key=lambda x: (x["score"], x["reviews"]))
        out.append({"k": "champion", "tag": "The model to copy", "loc": l["name"], "slug": l["slug"], "big": f"{l['score']}/100",
                    "text": f"{l['name']} scores {l['score']}: named in {l['llm_named']} of {l['llm_total']} AI answers ({eng_line(l)}) and on Google for {l['google_hits']} of {l['google_total']} searches. What it does right is the playbook for the rest of the portfolio."})
    # 4. Phone mismatches
    mm = [l for l in L if l["phone_ok"] is False and l["g_phone"]]
    if mm:
        l = mm[0]
        out.append({"k": "phones", "tag": "Two phone numbers, one practice", "loc": l["name"], "slug": l["slug"], "big": f"{len(mm)} locations",
                    "text": f"{l['name']}: Google lists {l['g_phone']}, while {acc_short}'s own site lists {l['src_phone']}. {len(mm)} of {len(L)} locations have a phone on Google that differs from the parent site. AI treats conflicting numbers as a reason to doubt the listing."})
    # 5. Shared phone numbers on the parent site
    by_phone = defaultdict(list)
    for l in L:
        if digits(l["src_phone"]):
            by_phone[digits(l["src_phone"])].append(l)
    shared = sorted([v for v in by_phone.values() if len(v) > 1], key=len, reverse=True)
    if shared:
        v = shared[0]
        out.append({"k": "shared_phone", "tag": "One number, many locations", "loc": v[0]["brand"], "slug": v[0]["slug"], "big": f"{len(v)} locations",
                    "text": f"{v[0]['brand']} lists the same number, {v[0]['src_phone']}, for {len(v)} locations ({', '.join(x['city'] for x in v)}). Search engines and AI can't tell those locations apart. {sum(len(x) for x in shared)} locations share a phone number across {len(shared)} brands."})
    # 6. Map pin off
    off = sorted([l for l in L if l["pin_km"] and l["pin_km"] >= 2], key=lambda x: -x["pin_km"])
    if off:
        l = off[0]
        out.append({"k": "pin", "tag": "Pinned in the wrong place", "loc": l["name"], "slug": l["slug"], "big": f"{l['pin_km']:.1f} km off",
                    "text": f"{acc_short}'s location map puts {l['name']} {l['pin_km']:.1f} km from where Google has it. {len(off)} location pins are 2 km or more off."})
    # 7. Broken website links on the parent site
    bad = [l for l in L if l["src_site"] and not re.search(r"\.[a-z]{2,}(/|$)", l["src_site"].lower())]
    if bad:
        l = bad[0]
        out.append({"k": "bad_url", "tag": "A link that goes nowhere", "loc": l["name"], "slug": l["slug"], "big": l["src_site"].replace("https://", ""),
                    "text": f"The website link {acc_short} lists for {l['name']} is \"{l['src_site']}\", which is not a working address."})
    # 8. Price spread for the same service
    by_svc = defaultdict(list)
    for l in L:
        for p in l["prices"]:
            s = service_of(p["t"])
            if s:
                by_svc[s].append((p["p"], l["name"], p["t"]))
    spreads = [(s, v) for s, v in by_svc.items() if len(v) >= 3 and max(x[0] for x in v) >= 1.5 * min(x[0] for x in v)]
    if spreads:
        s, v = max(spreads, key=lambda x: len(x[1]))
        lo, hi = min(v), max(v)
        out.append({"k": "price", "tag": "Same treatment, different price", "loc": s, "slug": None, "big": f"{money(lo[0])} to {money(hi[0])}",
                    "text": f"{s} is listed on Google from {money(lo[0])} at {lo[1]} to {money(hi[0])} at {hi[1]} ({len(v)} price listings across the portfolio). AI quotes these prices to patients."})
    # 9. Engine split
    splits = []
    for l in scored:
        r = {e: (l["eng"][e][0] / l["eng"][e][1]) for e in ENGINES if l["eng"][e][1]}
        if len(r) >= 3:
            hi_e, lo_e = max(r, key=r.get), min(r, key=r.get)
            splits.append((r[hi_e] - r[lo_e], l, hi_e, lo_e))
    if splits:
        d, l, hi_e, lo_e = max(splits, key=lambda x: (x[0], x[1]["reviews"]))
        if d >= 0.66:
            out.append({"k": "split", "tag": "The AI tools disagree", "loc": l["name"], "slug": l["slug"], "big": f"{ENGINE_LABEL[hi_e]} {l['eng'][hi_e][0]}/{l['eng'][hi_e][1]} · {ENGINE_LABEL[lo_e]} {l['eng'][lo_e][0]}/{l['eng'][lo_e][1]}",
                        "text": f"For {l['name']}, {ENGINE_LABEL[hi_e]} named it {l['eng'][hi_e][0]} of {l['eng'][hi_e][1]} times; {ENGINE_LABEL[lo_e]} named it {l['eng'][lo_e][0]} of {l['eng'][lo_e][1]}. Each AI reads different sources, so one strong channel isn't enough."})
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
    for loc in locs:
        raw = load(os.path.join(raw_dir, loc["slug"] + ".json"))
        if not raw:
            missing.append(loc["slug"]); continue
        L.append(score_location(loc, raw))

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
    for l in L:
        v = vols.get(l["slug"]) or {}
        town = sum(int(num(x) or 0) for x in (v.get("town") or {}).values())
        near = sum(int(num(x) or 0) for x in (v.get("near_me") or {}).values())
        l["vol"] = town + near
        l["vol_town"], l["vol_near"] = town, near
        l["worth"] = round(l["vol"] * RATE * price["value"])
        if l["vol"]:
            worth_rows.append([f"local {l['svc']}, Botox, lip filler and laser hair searches", l["vol"], l["name"]])

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
            if s:
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
        "eng": eng_tot,
    }
    data = {
        "account": acc, "prepared_for": cfg.get("prepared_for"), "date": cfg.get("date"), "price": price,
        "kpi": kpi, "locations": L, "brands": brands, "states": states,
        "rivals": [{"name": n, "n": c, "where": sorted(set(riv_where[n]))[:6]} for n, c in riv.most_common(15)],
        "services": services, "topics": topics.most_common(12), "trends": trends,
        "spotlights": spotlights(L, acc.get("short") or acc.get("name")),
        "audits": cfg.get("audits") or {},
    }

    # "What being AI's answer is worth" section via _template/worth.py (house rule)
    worth_html = ""
    if worth_rows:
        wj = {"client": acc.get("name"), "rows": worth_rows, "price": price,
              "vol_source": cfg.get("vol_source", "DataForSEO, Google Ads search volume; town searches at state level, 'near me' at city level"),
              "left_out": "One row per location: the sum of its town searches (med spa, Botox, lip filler, laser hair removal + town) and the same four 'near me' searches in its city. Searches with no volume are left out."}
        wpath = os.path.join(base, "worth.json")
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
