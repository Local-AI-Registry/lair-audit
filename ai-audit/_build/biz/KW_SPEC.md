# Local cannabis search volume: build the full keyword set (one business)

Goal: the monthly Google searches in the store's own trade area for EVERYTHING a cannabis shopper might search,
not just "dispensary <town>". Real numbers only, from Google Ads volume via DataForSEO.

Tool: mcp__DataForSEO__kw_data_google_ads_search_volume (load it with ToolSearch "select:mcp__DataForSEO__kw_data_google_ads_search_volume").
Set location_name to each trade-area CITY (format "City,State,Country", e.g. "Dubuque,Iowa,United States"),
language_code "en". The tool may only show about 10 keywords per response, so send keywords in batches of 10.
If a city location is rejected, try the nearest supported city or the county/DMA name the tool accepts; record what you used.

Note: Google hides volume for many cannabis "near me" phrases (Google Ads cannabis policy). Still send them;
record null when no volume comes back. Never fill gaps with guesses.

## Keyword list (send ALL of these for EACH trade-area city)
Generic: dispensary, dispensaries, weed dispensary, cannabis dispensary, marijuana dispensary, recreational dispensary,
weed store, weed shop, pot shop, cannabis store, cannabis shop, marijuana store, weed, cannabis, marijuana, thc, cbd,
dispensary near me, dispensaries near me, weed near me, weed store near me, cannabis store near me, pot shop near me,
best dispensary, best dispensary near me, cheap dispensary, cheap weed, dispensary deals, dispensary specials,
dispensary deals near me, dispensary open now, dispensary open late, dispensary hours, 24 hour dispensary,
weed delivery, cannabis delivery, dispensary delivery, dispensary pickup, dispensary menu, online dispensary,
first time dispensary, dispensary rewards
Products: edibles, edibles near me, thc gummies, gummies near me, thc chocolate, thc drinks, thc seltzer, pre rolls,
pre rolls near me, joints, blunts, flower, weed flower, cannabis flower, ounce of weed, eighth of weed, vape, thc vape,
vape pen, carts, thc carts, disposable vape, cartridges, concentrates, wax, shatter, live resin, rosin, hash, dabs,
thc tincture, topicals, thc lotion, cbd gummies, cbd oil, delta 8, delta 9, thca, thca flower, hemp, kratom,
smoke shop, smoke shop near me, head shop, bongs, glass pipes, rolling papers
Town modified: for each town name T in the trade area: "dispensary T", "T dispensary", "dispensaries T",
"weed T", "weed store T", "cannabis T", "T weed", "edibles T", "smoke shop T", "dispensary near T"

## Output
Write ai-audit/_build/biz/kwfull_<slug>.json :
{"locations_used":[...], "rows":[{"q":"keyword","loc":"City,State,Country","v":number_or_null}, ...],
 "notes":[...]}
Include every keyword you sent (null when no data). Do not change any other file.
Finish with a 6-line summary: locations used, number of keywords with volume, total monthly volume per location,
top 10 keywords by volume, anything odd.
