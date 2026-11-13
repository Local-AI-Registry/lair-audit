# AI visibility audit: data spec (one business)

Goal: gather REAL data for one business and write ONE JSON file matching the schema below.
Every number must come from a tool result. Never invent, estimate or round up to look better or worse.
If something can't be measured, use null and say so in "notes". Keep tool outputs small (low depth/limit)
and when a result is saved to a file, parse it with python3 instead of reading it all.

Tools: DataForSEO MCP tools (load with ToolSearch, e.g. "select:mcp__DataForSEO__serp_organic_live_advanced").
Useful: business_data_business_listings_search, serp_organic_live_advanced (use location_coordinate "lat,lng,10000"
and depth 20; look for local_pack, organic and ai_overview items), ai_optimization_llm_response
(llm_type chat_gpt / gemini / perplexity / claude, web_search true; models: chat_gpt "gpt-4.1-mini",
gemini "gemini-2.5-flash", perplexity "sonar", claude "claude-haiku-4-5"; if a model name fails call the
models tool), kw_data_google_ads_search_volume, dataforseo_labs_google_domain_rank_overview,
dataforseo_labs_google_historical_rank_overview, backlinks_summary, on_page_instant_pages,
serp_youtube_organic_live_advanced, WebSearch/WebFetch for the website and press.
Semrush is out of units; do not use it.

## Steps
1. Confirm the business listing (name, address, phone, site, rating, review count, photos, categories,
   hours, description). The listing tool data can be stale (check last_updated_time); confirm with a live
   SERP local pack or the business website. If the location moved or closed, say so in notes.
2. Pick 3 closest competitors: same category, nearby, that show in the Google local pack for the main
   searches. Get each one's domain, rating and review count.
3. Searches (7): 6 non-brand local searches people really use (e.g. "dispensary <city>", "best dispensary
   near me", "weed delivery <city>", "cannabis store near me", "dispensary open now", "dispensary deals
   <city>"), plus 1 brand search (the business name). Get monthly Google volume for each
   (kw_data_google_ads_search_volume at the city or state level; Canada: use "Alberta,Canada" or
   "Canada"). Keep only searches with volume > 0 if you can, otherwise keep them and record 0.
4. For each of the 7 searches:
   - Google: run serp_organic_live_advanced at the business coordinates. Record the business's position
     (local pack or organic, top 20) or null. Record the local pack names. Record whether an AI Overview
     exists and whether it names the business.
   - Ask ChatGPT, Gemini, Perplexity and Claude (web_search true). Prompt: turn "near me" into
     "in <City>, <State/Province>". Brand search prompt: "What can you tell me about <Name> in <City>,
     <State>? Is it a good choice?". Record 1 if the answer names the business, else 0. Record which
     competitor businesses each answer names instead (names only).
5. Measures for the business AND the 3 competitors (same order): see "aud" below.
6. Site checks on the business website (location page if it has one, plus homepage): load time, server
   wait, on-page score (on_page_instant_pages), copyright year in footer, server software header if
   visible, number of images and how many have useful alt text / descriptive file names (give 3 example
   bad file names), schema on page, review link, blog/news posts and date of latest post.
7. Traffic: monthly organic traffic (etv) for the last 12 full months for the business domain and each
   competitor domain (historical_rank_overview, location = country). For chains on one domain, say so in
   notes (the domain number covers all locations).
8. Price: a cited average spend per customer visit for this category and country (e.g. average dispensary
   basket from Headset, BDSA, Statistics Canada or a state regulator). Give the number, currency, source
   name and URL. If none can be found, null.

## Output: write ai-audit/_build/biz/<slug>.json
{
 "slug": "...",
 "biz": {"name":"SHORT UPPERCASE NAME for headings, max 16 chars","full":"Google listing name","short":"Name in title case",
   "city":"City, ST","addr":"full address","phone":"(xxx) xxx-xxxx","site":"domain/path of location page or homepage",
   "domain":"domain.com","rating":4.9,"reviews":272,"lat":0,"lng":0,"place_id":"...","svc":"dispensary",
   "area":["City","Region line for the map cartouche"], "hours":[[open_minute_of_week, close_minute_of_week], ...]  (Monday 00:00 = 0)},
 "comps": [{"n":"Competitor name","d":"domain.com","rating":4.7,"reviews":159}, x3],
 "rd": [ {"q":"search text","v":monthly_volume,"t":"Transaction|Commercial|Informational|Brand","g":"#7 or null",
          "r":[google_top20, chatgpt, gemini, perplexity, google_ai_overview, claude]  (each 0/1)} , ... only searches where r has at least one 1 ],
 "cr": [ {"q":"search","v":vol,"t":"type","c":["competitor names AI or Google named instead, max 3"]} , ... searches where the business is named nowhere ],
 "scan": {"searches": 7, "answers_naming_you": n, "answers_total": 7*5, "brand_searches": 1},
 "traffic": [{"n":"BUSINESS","me":true,"v":[12 monthly etv numbers oldest->newest]}, {"n":"Comp 1","v":[...]}, ...],
 "months": ["Dec","Jan",... 12 labels matching traffic],
 "score": {"you": 0-100, "avg": 0-100, "top": 0-100}   (share of the 6 slots x non-brand searches where each is named; avg = mean of the 3 competitors; top = best competitor),
 "price": {"value": 55, "currency":"USD", "label":"average dispensary basket", "source":"Headset", "url":"https://..."},
 "checks": [  // exactly these 11, in this order, each with real findings
   {"c":"Directory listings","st":"Passed|Needs work|Failed","parts":[["Business record","..."],["Directory listings","..."]],
    "issue":"one plain sentence about what we found",
    "found":{"h":["Where","What we found"],"r":[["label","value","ok|warn|bad"], ...4-7 rows],
             "ch": optional chart {"t":"bar","u":"","cap":"CAPTION IN CAPS","d":[["NAME",number],...]} or {"t":"pie","a":n,"b":n,"la":"LABEL","lb":"LABEL","cap":"CAPTION"} }},
   {"c":"PR",...},{"c":"Video",...},{"c":"SEO",...},{"c":"Web management",...},{"c":"Reputation management",...},
   {"c":"Google profile",...},{"c":"Photo codifying",...},{"c":"Independent articles",...},{"c":"Independent guides",...},{"c":"AI monitoring",...}
 ],
 "aud": { // you + 3 competitors, same order as comps. v = [you, c1, c2, c3]; null if unknown
   "Directory listings":[{"m":"Google name matches the real business name","t":"bool","v":[..],"src":"Google Maps"},{"m":"Categories on your Google profile","t":"num","v":[..],"good":5,"ok":3,"src":"Google Maps"},{"m":"Business description on Google","t":"bool","v":[..],"src":"Google Maps"}],
   "PR":[{"m":"Articles about you on real news outlets","t":"num","v":[..],"good":3,"ok":1,"src":"Google News"}],
   "Video":[{"m":"Videos about you on YouTube","t":"num","v":[..],"good":5,"ok":1,"src":"YouTube search, top 20"}],
   "SEO":[{"m":"Google searches you rank for","t":"num","v":[..],"good":100,"ok":30,"src":"DataForSEO"},{"m":"Searches where you rank in the top 10","t":"num","v":[..],"good":20,"ok":5,"src":"DataForSEO"}],
   "Web management":[{"m":"Homepage load time","t":"num","u":"s","v":[..],"good":2.5,"ok":4,"low":1,"src":"DataForSEO page test"},{"m":"On-page health score","t":"num","v":[..],"good":95,"ok":85,"src":"DataForSEO page test"}],
   "Reputation management":[{"m":"Google reviews","t":"num","v":[..],"good":<set from local norms>,"ok":..,"src":"Google Maps"},{"m":"Google rating","t":"num","u":"★","v":[..],"good":4.8,"ok":4.5,"src":"Google Maps"}],
   "Google profile":[{"m":"Photos on your Google profile","t":"num","v":[..],"good":50,"ok":20,"src":"Google Maps"},{"m":"Profile details filled in","t":"num","v":[..],"good":15,"ok":8,"src":"Google Maps attributes"}],
   "Photo codifying":[{"m":"Homepage images with useful alt text (%)","t":"num","u":"%","v":[..],"good":80,"ok":50,"src":"DataForSEO page test"}],
   "Independent articles":[{"m":"Other websites linking to you","t":"num","v":[..],"good":150,"ok":75,"src":"DataForSEO backlink index"},{"m":"Spam score of the sites linking to you","t":"num","u":"%","v":[..],"good":10,"ok":25,"low":1,"src":"DataForSEO backlink index"}],
   "Independent guides":[{"m":"Shows up for “best <svc> <city>”","t":"bool","v":[..],"src":"Google, top 20"}],
   "AI monitoring":[{"m":"AI answers that name each business (non-brand searches)","t":"num","v":[..],"good":<n>,"ok":<n>,"src":"Our AI scan"}]
 },
 "notes": ["anything unusual, stale data, chain-domain caveats, failures"]
}
Status rules: "Passed" only when clearly good vs the thresholds and competitors; otherwise "Needs work" or "Failed".
Use plain words, no jargon, no em dashes. Do not name white-label vendors.
Finish by printing a 10-line summary: listing confirmed?, competitors, AI answers naming you x/35, score, price source, notes.
