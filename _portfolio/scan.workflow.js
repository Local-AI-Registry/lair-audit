export const meta = {
  name: 'portfolio-scan',
  description: 'Portfolio AI-visibility scan of every location of a multi-location account, plus brand web data, trends and search volumes',
  whenToUse: 'Scanning all locations of a multi-location aesthetics or medical group. args: {account:{name,short,source}, out_dir, locations:[[slug,name,brand,address,city,state,zip,phone,website,lat,lng],...]}',
  phases: [
    { title: 'Locations', detail: 'one agent per location: Google listing, 3 Google searches, 3 prompts x 4 AI tools' },
    { title: 'Brands', detail: 'domain traffic, rankings, backlinks for each brand website' },
    { title: 'Trends', detail: 'Google Trends + YouTube for treatments and brands' },
    { title: 'Volumes', detail: 'local search volumes per location (state + city level)' },
  ],
}

const RAW = args.out_dir
const ACC = args.account  // {name, short, source}
const L = args.locations.map(a => ({slug:a[0],name:a[1],brand:a[2],address:a[3],city:a[4],state:a[5],zip:a[6],phone:a[7],website:a[8],lat:a[9],lng:a[10]}))

const LOC_SCHEMA = {type:'object',properties:{
  slug:{type:'string'}, svc:{type:'string'},
  listing:{type:'object'},
  searches:{type:'array',items:{type:'object'}},
  notes:{type:'array',items:{type:'string'}}
},required:['slug','listing','searches']}

function locPrompt(l){return `You are collecting REAL data for one location of ${ACC.name} (${ACC.short}). Every value must come from a tool result; never guess. Use null when unknown.
Load tools with ToolSearch "select:mcp__DataForSEO__business_data_business_listings_search,mcp__DataForSEO__serp_organic_live_advanced,mcp__DataForSEO__ai_optimization_llm_response,mcp__DataForSEO__ai_optimization_llm_models".

Location (from ${ACC.source}): ${l.name} | brand ${l.brand} | ${l.address}, ${l.city}, ${l.state} ${l.zip} | source-listed phone ${l.phone} | source-listed site ${l.website} | source map pin ${l.lat},${l.lng}

STEP 1 Google listing: business_data_business_listings_search with title set to the business name (try brand name + city if needed), location_coordinate "${l.lat},${l.lng},15", limit 3. Pick the listing that is this location (match address). If none, try without is_claimed filter, then record found=false.
From it record: title, google_phone, phone_matches_source (compare digits with ${l.phone}; true/false), address (Google), distance_km between Google lat/lng and the source map pin (compute, 1 decimal), site_url (Google link), site_matches_source (same registrable domain as ${l.website}), category, categories (list), rating, reviews, stars {"1":n,...,"5":n}, photos (total_photos), claimed, has_description, attributes_count (count of available attributes), last_updated, topics (place_topics as [{t,n}] top 8), services_count, prices (up to 10 [{title,category,price_usd}] with price>0 only), also_search ([{name,rating,reviews}] up to 5), weekly_open_hours (sum of open hours in work_time timetable).
Also save popular_times exactly as returned into the raw file (step 4), but do not analyze it.

STEP 2 Decide svc: "plastic surgeon" if the primary category is plastic surgeon/cosmetic surgeon; "dermatologist" if dermatologist; otherwise "med spa".
Searches (use exactly these):
 S1 query "${'${svc}'} ${l.city} ${l.state}"  (replace svc)
 S2 query "botox ${l.city} ${l.state}"
 S3 query "best ${'${svc}'} near me"
For each search run serp_organic_live_advanced with location_coordinate "${l.lat},${l.lng},10000"? -> NOTE: that tool takes location_name; use location_name "${l.city},${stateName(l.state)},United States" (if it errors, use "${stateName(l.state)},United States" and note it), language_code "en", depth 10.
Record google: map_pos (1-3 if this business is in the local_pack, else null), map_pack (names in local_pack, up to 3), organic_pos (rank_group of first organic result that is this business's own site or Google listing, else null), aio: "named" if an ai_overview item's text names the business, "not_named" if text exists without it, "unreadable" if asynchronous with no text, "none" if no ai_overview.

STEP 3 Ask AI. Prompts: S1 and S2 use the query text; S3 uses "best ${'${svc}'} in ${l.city}, ${l.state}". For each prompt call ai_optimization_llm_response with web_search true for: chat_gpt "gpt-4.1-mini", gemini "gemini-2.5-flash" (if rate limited twice, use "gemini-3.6-flash" and note it), perplexity "sonar", claude "claude-haiku-4-5". 12 calls. You may run calls in parallel.
For each answer: named = 1 if it names this business (brand name; for multi-location brands the brand name counts), 0 if not, null if failed/no text; others = other aesthetic businesses named (names only, up to 8).

STEP 4 Write ONE file ${RAW}/${l.slug}.json (create directory if missing) with {"slug","run_date":"2026-11-20","source":{the location fields given above},"listing":{...,"popular_times":<raw>},"svc","searches":[{"key":"S1","q","prompt","google":{...},"llm":{"chat_gpt":{named,others},"gemini":{...},"perplexity":{...},"claude":{...}}},...],"notes":[...]}. Do not write any other files and do not commit.

Return the same object WITHOUT popular_times (keep it compact). notes: anything odd (closed, moved, duplicate listings, wrong phone, model substitutions).`}

function stateName(s){return {AL:'Alabama',AZ:'Arizona',CA:'California',CT:'Connecticut',DC:'District of Columbia',FL:'Florida',GA:'Georgia',IN:'Indiana',MA:'Massachusetts',MD:'Maryland',MI:'Michigan',MO:'Missouri',NC:'North Carolina',NJ:'New Jersey',NY:'New York',OK:'Oklahoma',OR:'Oregon',PA:'Pennsylvania',SC:'South Carolina',TN:'Tennessee',TX:'Texas',UT:'Utah',WA:'Washington'}[s]||s}

phase('Locations')
const locP = pipeline(L, l => agent(locPrompt(l).split("${'${svc}'}").join('<svc>'), {label:`loc:${l.slug}`, phase:'Locations', schema:LOC_SCHEMA}))

// brand domains
const domains = [...new Set(L.map(l => l.website.replace(/^https?:\/\//,'').replace(/^www\./,'').split('/')[0]))]
const groups = []; for (let i=0;i<domains.length;i+=6) groups.push(domains.slice(i,i+6))
const BR_SCHEMA = {type:'object',properties:{domains:{type:'array',items:{type:'object'}}},required:['domains']}
const brP = parallel(groups.map((g,gi) => () => agent(`Collect REAL web data (every number from a tool result; null if unavailable) for these brand website domains: ${g.join(', ')}.
Load tools with ToolSearch "select:mcp__DataForSEO__dataforseo_labs_google_domain_rank_overview,mcp__DataForSEO__backlinks_summary,mcp__DataForSEO__dataforseo_labs_google_historical_rank_overview".
For each domain: domain_rank_overview (United States, en) -> keywords_total (organic count), top3 (pos_1 + pos_2_3), top10 (top3 + pos_4_10), etv, is_new, is_up, is_down; historical_rank_overview (United States) -> monthly organic etv and keyword count for the last 12 months [{month:"YYYY-MM", etv, keywords}]; backlinks_summary -> referring_domains, backlinks, broken_backlinks, broken_pages, spam_score (backlinks_spam_score), rank.
If a domain returns nothing try with www. Write results to ${RAW}/_domains_${gi}.json and return {domains:[{domain,...}]}. Do not commit.`, {label:`brands:${gi}`, phase:'Brands', schema:BR_SCHEMA})))

const TR_SCHEMA = {type:'object',properties:{treatments:{type:'array',items:{type:'object'}},by_state:{type:'array',items:{type:'object'}},youtube:{type:'array',items:{type:'object'}},notes:{type:'array',items:{type:'string'}}},required:['treatments']}
const brands = [...new Set(L.map(l=>l.brand))]
const trP = agent(`Collect REAL search-trend data (every number from a tool result) for an aesthetics portfolio (${ACC.name}). Load tools with ToolSearch "select:mcp__DataForSEO__kw_data_google_trends_explore,mcp__DataForSEO__kw_data_dfs_trends_subregion_interests,mcp__DataForSEO__kw_data_google_ads_search_volume,mcp__DataForSEO__serp_youtube_organic_live_advanced".
A) Treatments: botox, lip filler, morpheus8, semaglutide, laser hair removal, hydrafacial, microneedling, coolsculpting, sculptra, daxxify (Google Trends allows up to 5 terms per call; include "botox" in every call as the anchor so groups are comparable). Location United States, past 12 months (and if available past 5 years for direction). For each term return {term, avg_interest_12m (relative to botox=100 anchor scale), change_pct (last 3 months vs same 3 months a year earlier, if computable), peak_month}.
B) Also get US monthly Google search volume for the same 10 terms (kw_data_google_ads_search_volume, United States) and include volume + 12-month monthly_searches trend direction.
C) By state: using dfs trends subregion interests (or google trends regional data) for botox, morpheus8, semaglutide, lip filler: interest by US state for these states: ${[...new Set(L.map(l=>l.state))].join(', ')}. Return [{term, state, interest}].
D) YouTube: for each brand name + "med spa" where helpful, run serp_youtube_organic_live_advanced (United States, depth 20) for these brands: ${brands.join('; ')}. Return {brand, videos_about_brand_top20 (count of results clearly about this brand), newest_video_age (from timestamps, e.g. "3 months"), top_channel}.
Write everything to ${RAW}/_trends.json. Return the object. Do not commit.`, {label:'trends', phase:'Trends', schema:TR_SCHEMA})

// volumes by state group
const byState = {}; L.forEach(l => (byState[l.state] = byState[l.state] || []).push(l))
const stateKeys = Object.keys(byState)
const vgroups = []; for (let i=0;i<stateKeys.length;i+=6) vgroups.push(stateKeys.slice(i,i+6))
const VOL_SCHEMA = {type:'object',properties:{locations:{type:'array',items:{type:'object'}}},required:['locations']}
const volP = parallel(vgroups.map((sg,vi) => () => agent(`Collect REAL Google Ads monthly search volumes (DataForSEO kw_data_google_ads_search_volume; load with ToolSearch "select:mcp__DataForSEO__kw_data_google_ads_search_volume,mcp__DataForSEO__kw_data_google_ads_locations"). Never estimate; record null when no volume.
For each location below:
 Town searches at STATE level (location_name "<State>,United States"), batch up to 10 keywords per call across locations in the same state: "med spa <city>", "botox <city>", "lip filler <city>", "laser hair removal <city>".
 Near-me searches at CITY level (location_name "<City>,<State>,United States"; if the city is not a valid Google Ads location, find the nearest valid one with kw_data_google_ads_locations and note it): "med spa near me", "botox near me", "lip filler near me", "laser hair removal near me". Locations sharing a city share one call.
Locations: ${sg.map(s => byState[s].map(l => `${l.slug} | ${l.city}, ${stateName(l.state)}`).join('\n')).join('\n')}
Return {locations:[{slug, town:{kw:vol,...}, near_me:{kw:vol,...}, near_me_location, notes}]} and write it to ${RAW}/_volumes_${vi}.json. Do not commit.`, {label:`volumes:${vi}`, phase:'Volumes', schema:VOL_SCHEMA})))

const [locs, br, tr, vol] = await Promise.all([locP, brP, trP, volP])
const ok = locs.filter(Boolean)
log(`Locations scanned: ${ok.length}/${L.length}`)
const missing = L.filter((l,i) => !locs[i]).map(l => l.slug)
if (missing.length) log(`Missing: ${missing.join(', ')}`)
return { locations: ok, missing, brands: br.filter(Boolean).flatMap(b => b.domains||[]), trends: tr, volumes: vol.filter(Boolean).flatMap(v => v.locations||[]) }
