#!/usr/bin/env python3
"""Turn a built portfolio (data.json) into the numbers a pitch deck's portfolio slides use.

Usage: python3 _portfolio/deck_data.py <account>/portfolio/data.json > /tmp/pf.js
Prints `var PF={...};` for the deck's inline script. Every value comes from data.json.
"""
import json, math, sys, statistics as st
from collections import defaultdict

d = json.load(open(sys.argv[1], encoding="utf-8"))
L, K = d["locations"], d["kpi"]


def corr(a, b):
    p = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    mx, my = st.mean(x for x, _ in p), st.mean(y for _, y in p)
    sx, sy = math.sqrt(sum((x - mx) ** 2 for x, _ in p)), math.sqrt(sum((y - my) ** 2 for _, y in p))
    return round(sum((x - mx) * (y - my) for x, y in p) / (sx * sy), 2) if sx and sy else 0


ai = [l["llm_named"] / l["llm_total"] if l["llm_total"] else None for l in L]
q = sorted(L, key=lambda x: -x.get("worth", 0)); n = len(q) // 4
quart = [round(st.mean(l["score"] for l in q[i * n:(i + 1) * n if i < 3 else len(q)])) for i in range(4)]
qworth = [sum(l.get("worth", 0) for l in q[i * n:(i + 1) * n if i < 3 else len(q)]) for i in range(4)]
nonlead = [l for l in q if l["h2h"] != "lead"]
prize = nonlead[:6]
close = sorted([l for l in L if -3 <= l["margin"] < 0], key=lambda x: -x.get("worth", 0))
w1 = {l["slug"] for l in q[:n] if l["h2h"] != "lead"}
w2 = [l for l in close if l["slug"] not in w1]
trust = sorted([l for l in L if l.get("review_x") and 2 <= l["review_x"] <= 12 and l["llm_total"] and l["llm_named"] <= 4], key=lambda x: -x["reviews"])[:6]
states = defaultdict(lambda: [0, 0])
for l in L:
    states[l["state"]][1] += 1
    if l["h2h"] == "lead":
        states[l["state"]][0] += 1
markets = defaultdict(lambda: [0, 0, []])
for l in L:
    k = f"{l['city']}, {l['state']}"
    markets[k][0] += l.get("worth", 0); markets[k][1] += 1; markets[k][2].append(l["h2h"])
mk = sorted(markets.items(), key=lambda x: -x[1][0])
bb = sum((b.get("domain") or {}).get("broken_backlinks") or 0 for b in d["brands"])
bl = sum((b.get("domain") or {}).get("backlinks") or 0 for b in d["brands"])
row = lambda l: [l["name"], l["own_n"], l["rival"], l["rival_n"], l.get("worth", 0)]
PF = {
    "kpi": {"n": K["locations"], "lead": K["lead"], "tie": K["tie"], "trail": K["trail"], "trail_worth": K["trail_worth"],
            "nonlead_worth": sum(l.get("worth", 0) for l in nonlead), "worth": K["worth"], "reach": K["reach"], "reach_worth": K["reach_worth"],
            "review_adv": K["review_adv"], "review_cmp": K["review_cmp"], "any_price": K["any_price"], "phone": K["phone_mm"],
            "ai": K["ai_rate"], "inv": K["invisible"], "vol": sum(l.get("vol", 0) for l in L), "broken": bb, "backlinks": bl, "groups": len(d["brands"])},
    "quart": quart, "qworth": qworth, "prize": [row(l) for l in prize],
    "close": [row(l) for l in close[:8]],
    "trust": [[l["name"], l["reviews"], round(l["comp_reviews"]), l["review_x"], l["llm_named"], l["llm_total"], l["rival"]] for l in trust],
    "states": {k: v for k, v in states.items()},
    "markets": [[k, v[0], v[1], v[2].count("lead")] for k, v in mk[:8]], "markets_rest": [len(mk) - 8, sum(v[0] for _, v in mk[8:])],
    "rivals": d["rivals"][:8],
    "groups": [[b["brand"], b["score"], b["n"], sum(1 for l in L if l["brand"] == b["brand"] and l["h2h"] == "lead")] for b in d["brands"]],
    "corr": [["Google map pack presence", corr([l["map_hits"] for l in L], ai)], ["Google rating", corr([l["rating"] for l in L], ai)],
             ["Photos on the listing", corr([math.log1p(l["photos"]) for l in L], ai)], ["Number of reviews", corr([math.log1p(l["reviews"]) for l in L], ai)],
             ["Local search demand", corr([math.log1p(l.get("vol") or 0) for l in L], ai)]],
    "phone": [round(100 * st.mean(a for a, l in zip(ai, L) if l["phone_ok"] and a is not None)), round(100 * st.mean(a for a, l in zip(ai, L) if l["phone_ok"] is False and a is not None))],
    "eng": {e: round(100 * v[0] / v[1]) for e, v in K["eng"].items()},
    "products": [[p["b"], p["us_vol"], p["change"], p["priced"], p["mentions"]] for p in d["products"] if p["us_vol"]],
    "waves": {"w1": [row(l) for l in q[:n] if l["h2h"] != "lead"], "w1worth": sum(l.get("worth", 0) for l in q[:n] if l["h2h"] != "lead"),
              "w2": [row(l) for l in w2], "w2worth": sum(l.get("worth", 0) for l in w2),
              "w3": [row(l) for l in sorted([l for l in L if l["h2h"] == "lead"], key=lambda x: x["margin"])][:4], "w3n": K["lead"]},
    "pts": [[l["name"], l["brand"], l["city"], l["state"], l.get("review_x"), l["margin"], l["llm_named"], l["llm_total"], l.get("vol", 0), l.get("worth", 0), l["h2h"], l["reviews"], l["rival"], l["own_n"], l["rival_n"]] for l in L],
    "quad": {"trusted_trailing": sum(1 for l in L if (l.get("review_x") or 0) > 1 and l["margin"] < 0),
             "trusted_trailing_worth": sum(l.get("worth", 0) for l in L if (l.get("review_x") or 0) > 1 and l["margin"] < 0),
             "trusted_leading": sum(1 for l in L if (l.get("review_x") or 0) > 1 and l["margin"] >= 0),
             "with_rx": sum(1 for l in L if l.get("review_x")), "no_vol": sum(1 for l in L if not l.get("vol"))},
    "sis": {k: v for k, v in (d.get("sisters") or {}).items() if k != "pairs"},
    "sispairs": [[p["a"], p["b"], p["km"], p["same_brand"], p["a_named_b"], p["b_named_a"]] for p in (d.get("sisters") or {}).get("pairs", [])],
    "slugs": {l["slug"]: [l["name"], l["brand"], l["city"], l["state"], l["h2h"], l["rival"], l["own_n"], l["rival_n"], l["llm_named"], l["llm_total"], l["reviews"]] for l in L},
}
print("var PF=" + json.dumps(PF, ensure_ascii=False) + ";")
