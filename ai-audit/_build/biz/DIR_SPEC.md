# Directory listings check (name, address, phone, hours match across directories)

For the business given, find its listing on these directories and compare to its Google Business Profile
(the "truth"): Leafly, Weedmaps, Yelp, Facebook, Bing Places/Bing Maps, Apple Maps (if findable), Yellow Pages,
MapQuest, Foursquare, Where's Weed, Best Bang for Your Bud (Canada) / Dutchie or Jane menus, and any other cannabis
directory that shows up when you search the business name + town.

Tools: mcp__DataForSEO__serp_organic_live_advanced (load via ToolSearch) with queries like
"<name> <town> site:leafly.com" or "<name> <address>" (depth 20; parse saved files with python3), WebSearch, WebFetch.
For each directory record: found (yes/no), name shown, address shown, phone shown, hours shown (if any),
and whether each matches Google ("match" / "different: <what>" / "missing"). Use only what you actually saw.

Write ai-audit/_build/biz/dir_<slug>.json — EXACT path:
ai-audit/_build/biz/dir_<slug>.json
{"truth":{"name":"","address":"","phone":"","hours":""},
 "dirs":[{"d":"Leafly","found":true,"url":"","name":"...","name_ok":true,"addr_ok":true,"phone_ok":true,"hours_ok":null,"note":"short plain note"}],
 "summary":{"found":n,"checked":n,"exact_match":n,"mismatches":n},
 "status":"Passed|Needs work|Failed",
 "issue":"one plain sentence, e.g. 'Your name, phone or hours differ on 4 of 9 directories, so AI can't tell which is right.'"}
Status: Passed if found on most and all match; Needs work if a few mismatches or missing; Failed if many.
Do not change other files. Never invent. Reply with a 5-line summary.
