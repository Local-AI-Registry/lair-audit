# Competitor directory listings check (name, address, phone, hours vs. Google)

For EACH competitor store given (the specific location named, not the chain), find its listing on these 9 directories
and compare it to that store's own Google Business Profile (the "truth"):
Leafly, Weedmaps, Yelp, Facebook, Yellow Pages, MapQuest, Foursquare, Where's Weed, and the 9th directory named in your task.

Tools: WebSearch, WebFetch, and mcp__DataForSEO__serp_organic_live_advanced (load with ToolSearch "select:mcp__DataForSEO__serp_organic_live_advanced"),
e.g. queries like "<store name> <town> site:leafly.com". First get the Google truth (name, address, phone, hours) from a Google/Maps result or DataForSEO.
A directory counts as "match" only if found AND name, address and phone agree with Google (hours too when shown).
Use only what you actually saw. Never invent. If a page can't be read, mark found:null (unknown) rather than guessing.

Write the EXACT path given in your task:
{"comps":[{"n":"<competitor name as given>","truth":{"name":"","address":"","phone":"","hours":""},
  "dirs":[{"d":"Leafly","found":true,"url":"","name_ok":true,"addr_ok":true,"phone_ok":true,"hours_ok":null,"note":"short"}],
  "match":n_matching,"listed":n_found,"checked":9}]}
Do not change other files. Reply with a 4-line summary: each competitor's match / listed / checked.
