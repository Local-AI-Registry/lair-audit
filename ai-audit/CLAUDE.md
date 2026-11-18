# ai-audit: the one-link AI visibility audit

Live at https://audit.localairegistry.com/ai-audit/ (search box loads any business in it).
This is the sales-call version: a light, 16:9 screen-share flow for walking a prospect through the audit on a call:
Find → Scan → Your score (3 steps) → Customers ask AI (2 steps) → 11 checks (Our system, then Your results; the verified business record is called the Blueprint on this page) → Why us → Plan.
← → keys step through everything; 1 to 6 jump to a chapter; `?b=<slug>#<chapter>` links straight in.
The older dark version stays at https://audit.localairegistry.com/ai-audit/classic.html. `v2/index.html` only forwards to the main page.

`index.html`, `classic.html`, `map-bg.html`, `map-light.html` and `three.min.js` here are BUILT files. Never hand-edit them.
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
- Status names and colors are the same on every screen: Passed (green), Needs work (amber), Failed (red), in that order.
- Why us: only the plastic surgery (New York) chart has real monthly data. The other cards have real start and end visits;
  the months between are a seeded path with its own shape per card (`shape` in `CARDS`, `cseries()`; flat year with a
  seasonal ripple, a lag, a climb with small pullbacks), drawn as a smooth line (`spath()`), labeled
  "Illustrative path; real start and end" until their monthly visits are added to `CARDS` in `sales.tpl.html`.
- Area exclusivity is described without a set distance ("one business like yours per area").

## Live scans (lair-api)
- API: https://lair-api-hps5or6egq-uw.a.run.app (`/places/autocomplete`, `/audit` streams NDJSON, `/audits/<id>` returns a saved scan).
  Its `d` result has the same shape as one `SETS` entry, so a live scan loads straight into this page.
- Scans and live search need the team password (`X-Team-Key` header, see Team sign-in below). A `?team=<key>` link is
  stored in that browser's localStorage as `lair-team` and removed from the URL. Never commit a key.
- Flow, one screen: picking a live search result (or `?id=<place id>` / `?q=<name>`) runs the scan on the Scan chapter's map
  as it happens (about 3 to 4 minutes): the progress follows the API's real steps and the pop-ups are its `find` facts
  (`liveScan()`, `LSTEP` in `sales.tpl.html`). When it finishes the URL becomes `?audit=<id>#scan` and "Your audit is ready"
  shows. Saved `?audit=` links open the scan already finished (no replay) and need no key. `/a/` only forwards here.
  `?b=<slug>` demo businesses still play the timed scan. The API only allows https://audit.localairegistry.com (CORS).
- No self-service for the public: scans are run by our team. A visitor without a key who picks a business gets a lead card on
  the Scan screen (no API calls): "Book my audit call" → Bridgette's Calendly (`BOOK` in `sales.tpl.html`), or text us.
  The business name is prefilled with `?a1=`, so the event's first question must be the business name.
- Team sign-in (`tsHTML()` in `sales.tpl.html`): one shared team password (the API's `TEAM_KEYS`; how to set it is in lair-api's
  deploy/README.md). "Team sign-in" under the home search box, or "Team member? Enter the team password to run the scan" on the
  lead card. The page checks it with `/auth/me` before saving it in `lair-team`, once per browser and device; then the card says
  "Team mode on", with Sign out. Ten wrong tries from one address wait 10 minutes. `?team=<password>` links still work.
  Without a sign-in, picking a business always shows the lead card, never a scan.

## Questions during the scan (rep only)
- With a team key, the Scan screen asks the owner up to 4 optional questions, each when its step comes up (`QDEF` in
  `sales.tpl.html`): who they lose clients to, services to grow (up to 3), first-visit spend, visits a year. Each has
  "Skip this one". On desktop the card sits on the map; on phones, or once the scan is done, it moves into the side panel.
- Answers are saved in the browser and, for live audits, with the audit (`PUT /audits/<id>/answers`; `GET /audits/<id>`
  returns `answers`). They change later pages and are always tagged "From you": spend replaces the cited price,
  visits add first-year value to the plan's full potential, services move those searches to the top of Customers ask AI,
  and the rival is tagged on the leaderboard and on "Who shows up when it isn't you".

## Customers ask AI
- Step 1: three summary numbers, then one grid: a row per search, a column per AI assistant, the result on the right.
- Step 2: "Who takes your spot" (ranked) beside a table of the searches where they're missing: Google's map top 3 and what AI says.

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
