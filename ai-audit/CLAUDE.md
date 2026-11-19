# ai-audit: the one-link AI visibility audit

Live at https://audit.localairegistry.com/ai-audit/ (search box loads any business in it).
This is the sales-call version: a light, 16:9 screen-share flow for walking a prospect through the audit on a call:
Find → Scan → Your score (3 steps) → Customers ask AI (2 steps) → 11 checks (Our system, then Your results; the verified business record is called the Blueprint on this page) → Why us → Plan.
← → keys step through everything; 1 to 6 jump to a chapter; `?b=<slug>#<chapter>` links straight in.
The older dark version stays at https://audit.localairegistry.com/ai-audit/classic.html. `v2/index.html` only forwards to the main page.

`index.html`, `classic.html`, `map-bg.html`, `map-light.html`, `three.min.js`, `fix-ill.json` and `sets/` here are BUILT files. Never hand-edit them.
Edit the source in `_build/` and run `_build/build.sh`, which rewrites them.

## Source (`_build/`)
- `sales.tpl.html` + `sales.py`: the main page. `sales.py` reuses `make()` from `hudbuild3.py`, so every number matches.
- `hud.tpl.html`: the classic page template (all screens, styles, scripts).
- `hudbuild3.py`: merges the classic template with every business's data into `../classic.html`.
- `build.sh`: the one command to rebuild both. It lists every business included.
- `biz/<slug>.json`: one business's scan (score, AI answers, 11 checks, competitors, traffic, volumes).
  Optional sidecars: `dir_<slug>.json` (directory check), `dirc_<slug>.json` (competitors' directories),
  `packs_<slug>.json` (Google map pack), `vol2_`/`kwlocal_`/`kwfull_` (keyword volumes).
- `biz/SPEC.md`, `DIR_SPEC.md`, `DIRC_SPEC.md`, `KW_SPEC.md`: how a new business scan is done. Follow them exactly.
  Their output paths are relative to the repo root.
- `mapbg.html` + `darkmap.py` + `darkmap.css`: the classic page's 3D map, converted to dark by build.sh.
- `lightmap.py`: makes `../map-light.html`, the same map recolored to the white brand. The main page shows it behind
  the home screen and the scan (real streets and roaming people), and falls back to a drawn map if it can't load.
- `quiktox-audit.html`, `qx6.py`, `extract.json`, `art.json`, `vouch.json`, `hud_ev.json`, `hud_fix.json`, `logos.json`: shared content (Quiktox demo data, news, references, illustrations, logos).
- `tests/`: Playwright checks, run from `_build`. Main page: `tests/serve.sh node tests/v2.js <slug> [<slug> ...]`
  (every chapter, errors and overflow). Classic page: `tests/serve.sh node tests/audt.js` and the others.

## Speed (first load)
- Each demo business's data is its own file, `sets/<slug>.json`, fetched when that demo opens (`loadSet()`); the page keeps only
  their names (`DEMOS`, for the search box). A `?b=` link starts fetching its file from the `<head>` while the page loads.
- The first screen ships as plain HTML (`_build/find-shell.html`, captured from `vFind()`), so the headline paints before the
  script runs; links to an audit or demo (`?b=`, `?audit=`, `?id=`, `?q=`) keep the small loader instead.
  `tests/serve.sh node tests/shell.js` fails if that HTML drifts from what the script draws: re-capture it as the test says.
- sales.py strips comments and indentation from the styles and the main script. Fonts are self-hosted (no Google Fonts, also
  in `map-light.html`, which reuses the page's cached font files). The map loads only after the page has finished loading.

## Main page notes
- Plan has 3 steps: the overview, the full agency comparison (`extract.json` "cmp") and the month-by-month plan
  (`extract.json` "plan"). In the 11 checks, "What we found" shows each check's chart and findings table (`found` in biz JSON).
- Checkout (Get started, or the proposal's payment link): step 1 takes name, email, phone and a promo code (checked by
  `/billing/promo`), then `/billing/subscribe` creates the subscription and step 2 shows Stripe's Payment Element inside
  the popup (Stripe.js from js.stripe.com; card numbers never touch our servers). Prices and codes live in Stripe.
  Next never opens checkout. Reps (team key) also get "Send follow-ups" on the proposal, which calls `/leads`.
- Tests: `tests/v2map.js` checks the live map and the checkout. Set `MAPLIBRE_DIST` to a local maplibre-gl/dist/ folder
  to test the live map where map tiles are blocked.
- Look: matches the new website (/home/drafts/home-2/): self-hosted fonts from home/assets/fonts, regular-weight Hanken headlines in grey then ink, Bricolage eyebrows, blue pill buttons (a trailing arrow becomes a chevron chip via chipify()), hairline cards on white. It lives in the "2026 site look" block at the end of the stylesheet.
- Phones and tablets (in person): a bottom bar (`dock()`: Back, chapter and step, Next) replaces the top buttons; swipe left or
  right anywhere outside tables, sliders and side-scrolling rows moves a step; the screen stays awake (Wake Lock) once
  touched; Add to Home Screen opens it full screen. Why us shows the case studies as a swipeable row with a counter. On small
  phones the agency comparison has a Basic / Intermediate / Advanced picker, and each 12-month row puts its months on a
  full-width line. The test scripts click `#dock [data-nav="next"]` on phones.
- Status names and colors are the same on every screen: Passed (green), Needs work (amber), Failed (red), in that order.
- Why us: only the plastic surgery (New York) chart has real monthly data. The other cards have real start and end visits;
  the months between are a seeded path with its own shape per card (`shape` in `CARDS`, `cseries()`; flat year with a
  seasonal ripple, a lag, a climb with small pullbacks), drawn as a smooth line (`spath()`), labeled
  "Illustrative path; real start and end" until their monthly visits are added to `CARDS` in `sales.tpl.html`.
- Blueprint slide (11 checks, Our system): each check shows its "how we fix it" drawing from the classic page
  (`hud_fix.json`), written by sales.py to `../fix-ill.json` with "record" renamed Blueprint ("Your Blueprint™", same as the
  team's LAIR-11-checks-animations files), loaded only when the slide opens, and replayed every 7 seconds while on screen.
- Assurances follow the business type (`trustMed()`): medical practices
  show $750K insured / HIPAA BAA / US-based team; everyone else (dispensaries, shops, vets, unknown types, and the first screen before a business is picked) shows Guaranteed
  by day 90 / Month to month / US-based team, the Why us panel reads "Easy to say yes to", the plan and proposal cards drop
  the badge row (their list already says it), and Why us is titled "Our clients' results" (all case studies are medical).
- Proposal: the rep's send button reads "Email or text this proposal" (it calls `/leads`), so nothing says "rep only" on screen.
- Area exclusivity is described without a set distance ("one business like yours per area").

## Live scans (lair-api)
- API: https://lair-api-hps5or6egq-uw.a.run.app (`/places/autocomplete`, `/audit` streams NDJSON, `/audits/<id>` returns a saved scan).
  Its `d` result has the same shape as one `SETS` entry, so a live scan loads straight into this page.
- Scans and live search need a team key (`X-Team-Key` header). Open any page once with `?team=<key>`: it is stored in that
  browser's localStorage as `lair-team` and removed from the URL. Never commit the key.
- Flow, one screen: picking a live search result (or `?id=<place id>` / `?q=<name>`) runs the scan on the Scan chapter's map
  as it happens (about 3 to 4 minutes): the progress follows the API's real steps and the pop-ups are its `find` facts
  (`liveScan()`, `LSTEP` in `sales.tpl.html`). When it finishes the URL becomes `?audit=<id>#scan` and "Your audit is ready"
  shows. Saved `?audit=` links open the scan already finished (no replay) and need no key. `/a/` only forwards here.
  `?b=<slug>` demo businesses still play the timed scan. The API only allows https://audit.localairegistry.com (CORS).
- No self-service for the public: scans are run by our team. A visitor without a key who picks a business gets a lead card on
  the Scan screen (no API calls): "Book my audit call" → Bridgette's Calendly (`BOOK` in `sales.tpl.html`), or text us.
  The business name is prefilled with `?a1=`, so the event's first question must be the business name.
- Reps sign in once per browser and device: "Team sign-in" under the home search box (it checks the key with the API, then says
  "Team mode: picking a business runs the live scan", with Sign out), the "Team member? Run the live scan" link on the lead card,
  or a `?team=<key>` link. Without a key, picking a business always shows the lead card, never a scan.
- Later (see `_build/PARKING_LOT.md`): a shared team password, then maybe Google sign-in. Both are built and reverted.

## Questions during the scan (rep only)
- With a team key, the Scan screen asks the owner up to 8 optional questions (`QDEF` in `sales.tpl.html`): who they lose
  customers to, services to grow (up to 3, or their own), spend (quick picks or a typed amount), how often they come back,
  new customers a month, where most find them, marketing spend a month, and what matters most right now.
  The next question shows as soon as one is answered or skipped. Live scans wait (up to 20s) for the business type so the
  wording fits; "who they lose to" waits for the competitors and "services" waits for the services list.
  "← Back" reopens the previous one with its answer filled in; each has "Not sure" (or similar) and "Skip".
  On desktop the card sits on the map; on phones, or once the scan is done, it moves into the side panel.
- Services choices (`svcList()`): one list from the business's website and the searches the scan ran. Live audits get it from
  the API (`{services}` event after the website step, saved with the audit as `services`, each `{n, src:["site","scan"]}`;
  the API keeps only names written on the page). Demo audits use the services named in their own searches. The business
  type's list only tops it up when both give fewer than 4. The card says where the list came from.
- Wording and choices follow the business type (`CATS` → `qcat()`): patients for clinics, customers for dispensaries and
  shops, clients for vets and therapists; each type has its own services (`SVCO`) and spend quick picks (`QSPEND`).
  Dispensaries and shops get "a typical order" and "how often a regular comes back". Unknown types get generic choices.
- Answers are saved in the browser and, for live audits, with the audit (`PUT /audits/<id>/answers`; `GET /audits/<id>`
  returns `answers`). They change later pages and are always tagged "From you": spend replaces the cited price,
  visits add first-year value to the plan's full potential, services move those searches to the top of Customers ask AI,
  and the rival is tagged on the leaderboard and on "Who shows up when it isn't you". New customers a month shows under
  the worth page's full potential; new customers, where they find you and marketing spend show as "What you told us" on the
  proposal, and the goal leads its "What we'll do" card.
- What it's worth, with no usable search numbers (none for the area, or only nationwide): instead of dashes, the card shows
  what one new customer is worth (spend, times visits a year when answered) and says why there's no monthly figure.

## Customers ask AI
- Step 1: three summary numbers, then one grid: a row per search, a column per AI assistant, the result on the right.
- Step 2: "Who takes your spot" (ranked) beside a table of the searches where they're missing: Google's map top 3 and what AI says.
- Tapping a search (either step) opens "How AI decided" (`flowOpen()`), a five-stage path for that one search, from this
  audit's own data only: the question and its volume; each assistant (named you / left you out / couldn't be read); what AI
  reads about you (Google profile, website, directories, news, with each check's status); how you compare with the business
  AI named instead (or the closest competitor), from the "you vs. competitors" measures, gaps first; who AI recommended and
  Google's map top 3. "See your 11 checks" goes to the results. Modeled on /ai-flow/ (an illustrative explainer).

## Add a business
1. Run the scan per `biz/SPEC.md` (plus DIR_SPEC and DIRC_SPEC), writing `biz/<slug>.json` and its sidecars.
2. Add `biz/<slug>.json` to both lists in `build.sh`, run it, run the tests, check it at `?b=<slug>` (and `classic.html?b=<slug>`).

## Rules from Steve (always)
- Audit findings follow ONE template, 11 times: status, issue sentence, a visual of only this business's own data,
  the findings table, then exactly ONE "You vs. your 3 closest competitors" measure. No "How we fix it", no sources, no extra notes.
- Never invent numbers. Every figure comes from a tool result; unknown = null (shows as "–").
- High-risk categories (dispensary, cannabis, CBD, vape, smoke shop, hemp, kratom) show 4x the measured search volume,
  labeled "Est. searches" (Google hides most of that volume). `?concept=N` multiplies volumes for internal concepting only.
- `?news=preview` shows the scheduled press stories; the normal link shows only live coverage.
- Plain language, no em dashes, no orphan words on their own line, no new unverified claims or stats in subtext.
- Template copy stays industry-neutral; only a business's own data is specific.
