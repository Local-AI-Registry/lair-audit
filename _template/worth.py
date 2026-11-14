#!/usr/bin/env python3
"""Build the "What being AI's answer is worth" section for a proposal page.

Same math as Steve's ai-audit "What it's worth" screen:
    searches a month x 2.3% average conversion rate (Ruler Analytics) x average price per customer

Usage:
    python3 _template/worth.py <client>/worth.json > /tmp/worth.html
Then paste the output into <client>/index.html (and _template/worth.css into its <style>).

worth.json:
{
  "client": "Laser & Cosmetic Center",          # used in the intro sentence
  "rows": [["botox stroudsburg pa", 20, ""],     # [search, monthly volume, place label or ""]
           ["botox near me", 20, "Stroudsburg"]],
  "price": {"value": 527, "label": "average spend per US med spa visit",
            "source": "American Med Spa Association, 2024 Medical Spa State of the Industry report",
            "url": "https://..."},           # url "" for the client's own number
  "vol_source": "DataForSEO, Google Ads search volume, Pennsylvania and city level, November 13, 2026",
  "left_out": "optional sentence about searches deliberately left out"
}
Every volume must come from DataForSEO (never estimated). Searches with no volume are left out.
"""
import json, sys, html

RATE = 0.023
RULER = "https://www.ruleranalytics.com/wp-content/uploads/Lead-conversion-rates-by-industry.pdf"

def money(n):
    return "$" + f"{round(n):,}"

def build(d):
    rows = sorted([r for r in d["rows"] if r[1]], key=lambda r: -r[1])
    price = d["price"]["value"]
    searches = sum(r[1] for r in rows)
    cust = searches * RATE
    total = cust * price
    e = html.escape
    trs = []
    for i, (q, v, loc) in enumerate(rows, 1):
        c = v * RATE
        label = e(q) + (f' <span class="small">· {e(loc)}</span>' if loc else "")
        trs.append(
            f'<tr data-v="{v}"><td class="ix">{i:02d}</td><td>{label}</td><td class="r">{v:,}</td>'
            f'<td class="r">{c:.1f}</td><td class="r w-p">{money(price)}</td><td class="r w-r">{money(c * price)}</td></tr>')
    left = f'<p class="small">{e(d["left_out"])}</p>' if d.get("left_out") else ""
    return f'''<section class="worth" id="worth">
  <div class="wrap">
    <h2>What being AI&rsquo;s answer is worth</h2>
    <p class="sub">Searches &times; average conversion rate &times; average price. Move the slider to your own average price.</p>
    <div class="w-calc">
      <p class="lab">Added revenue</p>
      <p class="w-big"><span id="w-total">{money(total)}</span><small>/mo</small></p>
      <div class="w-row">
        <div><p class="lab">Searches a month</p><b>{searches:,}</b></div>
        <div><p class="lab">&times; Conversion</p><b>2.3<small>%</small></b></div>
        <div><p class="lab">= Customers</p><b>{round(cust):,}</b></div>
      </div>
      <p class="small">Average conversion rate. Source: <a href="{RULER}">Ruler Analytics</a></p>
      <p class="lab" style="margin-top:18px">Average price per customer</p>
      <p class="w-price" id="w-price">{money(price)}</p>
      <input type="range" id="w-slider" min="50" max="2500" step="5" value="{price}" aria-label="Average price per customer">
      <p class="small">Starts at {money(price)}, the {e(d["price"]["label"])}. Source: {f'<a href="{e(d["price"]["url"])}">{e(d["price"]["source"])}</a>' if d["price"].get("url") else e(d["price"]["source"])}</p>
    </div>
    <div class="tw"><table class="demand w-tbl">
      <caption>Your searches, {len(rows)} in all</caption>
      <thead><tr><th>#</th><th>Search</th><th class="r">Searches/mo</th><th class="r">Cust</th><th class="r">Price</th><th class="r">Rev/mo</th></tr></thead>
      <tbody>
        {chr(10).join("        " + t for t in trs).lstrip()}
      </tbody>
    </table></div>
    <p class="small">Search volumes: {e(d["vol_source"])}. Customers and revenue are estimates.</p>
    {left}
  </div>
  <script>
  (function(){{var s=document.getElementById('w-slider');if(!s)return;var R={RATE},f=function(n){{return '$'+Math.round(n).toLocaleString('en-US')}};
   s.addEventListener('input',function(){{var p=+s.value,t=0;document.getElementById('w-price').textContent=f(p);
    document.querySelectorAll('.w-tbl tr[data-v]').forEach(function(r){{var c=+r.dataset.v*R;t+=c*p;r.querySelector('.w-p').textContent=f(p);r.querySelector('.w-r').textContent=f(c*p)}});
    document.getElementById('w-total').textContent=f(t)}})}})();
  </script>
</section>'''

if __name__ == "__main__":
    d = json.load(open(sys.argv[1]))
    print(build(d))
