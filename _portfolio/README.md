# Portfolio AI-visibility kit

Scan every location of a multi-location group (MSO, franchise, roll-up) and build one owner-level
report: AI visibility per location, brand league table, who AI recommends instead, identity and
data consistency, services and prices, treatment demand, websites, revenue at stake, and
recommendations backed by real examples from the scan.

First used for AMP: `amp-partnership/portfolio/` (77 locations, 22 brands).

## Files
- `scan.workflow.js`: the data collection workflow (also saved as `.claude/workflows/portfolio-scan.js`,
  so it can be run by name). One agent per location plus brand, trends and volume agents.
- `build.py`: reads the raw scan files and writes the report page and its `data.json`.
- `report.tpl.html`: the report template (self-contained page, data inlined at build time).
- `locations_from_csv.py`: turns a CSV of locations into the location list.

## Run it for a new account
1. **Location list.** Make `<account>/data/<account>-locations.json`: a list of
   `{slug, name, brand, address, city, state, zip, phone, website, lat, lng}`.
   From a spreadsheet: `python3 _portfolio/locations_from_csv.py locations.csv <account>/data/<account>-locations.json`.
   From the group's own site: many "find a location" pages embed this list as JSON (AMP's did); keep
   the phones and links exactly as the group publishes them, because the scan checks them against Google.
2. **Scan.** Run the `portfolio-scan` workflow with
   `args = {account: {name, short, source}, out_dir: "<account>/data/portfolio", locations: [[slug, name, brand, address, city, state, zip, phone, website, lat, lng], ...]}`.
   Cost: about 16 DataForSEO calls per location (1 listing, 3 Google searches, 3 prompts x 4 AI tools),
   plus about 3 per brand website, about 30 for trends and about 1 per city for volumes.
   Each location's raw results are saved to `<out_dir>/<slug>.json`, so a later full audit only adds
   the missing checks; nothing is collected twice.
   Locations run 2 at a time on a 4-CPU session (about 2 to 3 minutes each).
3. **Config.** Copy `amp-partnership/portfolio.config.json` to `<account>/portfolio.config.json` and edit:
   account, prepared_for, date, locations_file, raw_dir, out, and `audits` (links to any full audits).
   `price` is optional (defaults to the American Med Spa Association $527 average visit).
4. **Build.** `python3 _portfolio/build.py <account>/portfolio.config.json`
   It also writes `<account>/worth.json` and inlines the "What being AI's answer is worth" section
   from `_template/worth.py` (house rule for every audit).
5. **Check** the page in a browser (desktop and phone), read the real-example cards, then publish.

## What is measured
- **AI score (0 to 100):** share of checks naming the location across 3 searches: Google map pack or
  organic top 10, Google AI Overview (left out when unreadable), and ChatGPT, Gemini, Claude, Perplexity.
- **Named instead:** businesses named in the same answers and map packs, counted per location.
- **Identity checks:** Google phone vs the group's published phone, shared phones across locations,
  the group's map pin vs Google's, Google's website link vs the published one, claimed status, description.
- **Services and prices:** from each Google Business Profile.
- **Demand:** Google Trends (national and by state) and Google Ads volumes; YouTube presence per brand.
- **Not measured:** foot traffic (only relative "popular times" exist in our tools; they are saved in
  the raw files but not presented), TikTok and Instagram.

## Real examples
`build.py` picks specific locations for the example cards automatically: the best-reviewed location
AI ignores, a location that wins on Google Maps but not in AI, the top performer, phone mismatches,
phones shared across locations, misplaced map pins, broken links on the group's site, price gaps for
the same treatment, and locations where the AI tools disagree. Every card quotes the location, the
numbers and the competitor named instead. Recommendations reuse the same examples.
