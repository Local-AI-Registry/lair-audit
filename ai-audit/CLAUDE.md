# ai-audit: the one-link AI visibility audit

Live at https://audit.localairegistry.com/ai-audit/ (search box loads any business in it).
This is the sales-call version: a light, 16:9 screen-share flow for walking a prospect through the audit on a call:
Find → Scan → Your score (3 steps) → Patients ask AI (2 steps) → 11 checks (Our system, then Your results) → Why us → Plan.
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
- Plan: Get started opens a card form with a promo code (KODY25 = 25% off until Dec 1, 2026, set in `PROMOS` in
  `sales.tpl.html`). Card checkout is not connected to a payment processor yet: card details never leave the page,
  and a valid card shows "nothing was charged, we'll reach out".
- Tests: `tests/v2map.js` checks the live map and the checkout. Set `MAPLIBRE_DIST` to a local maplibre-gl/dist/ folder
  to test the live map where map tiles are blocked.
- Status names and colors are the same on every screen: Passed (green), Needs work (amber), Failed (red), in that order.
- Why us: only the plastic surgery (New York) chart has real monthly data; the other result cards are labeled
  "Illustrative" until their monthly visits are added to `CARDS` in `sales.tpl.html`.

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
