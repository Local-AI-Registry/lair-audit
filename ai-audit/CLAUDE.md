# ai-audit: the one-link AI visibility audit

Live at https://audit.localairegistry.com/ai-audit/ (search box loads any business in it).
`index.html`, `map-bg.html` and `three.min.js` here are BUILT files. Never hand-edit them.
Edit the source in `_build/` and run `_build/build.sh`, which rewrites them.

## Source (`_build/`)
- `hud.tpl.html`: the page template (all screens, styles, scripts).
- `hudbuild3.py`: merges the template with every business's data into `../index.html`.
- `build.sh`: the one command to rebuild. It lists every business included.
- `biz/<slug>.json`: one business's scan (score, AI answers, 11 checks, competitors, traffic, volumes).
  Optional sidecars: `dir_<slug>.json` (directory check), `dirc_<slug>.json` (competitors' directories),
  `packs_<slug>.json` (Google map pack), `vol2_`/`kwlocal_`/`kwfull_` (keyword volumes).
- `biz/SPEC.md`, `DIR_SPEC.md`, `DIRC_SPEC.md`, `KW_SPEC.md`: how a new business scan is done. Follow them exactly.
  Their output paths are relative to the repo root.
- `mapbg.html` + `darkmap.py` + `darkmap.css`: the 3D map, converted to dark by build.sh.
- `quiktox-audit.html`, `qx6.py`, `extract.json`, `art.json`, `vouch.json`, `hud_ev.json`, `hud_fix.json`, `logos.json`: shared content (Quiktox demo data, news, references, illustrations, logos).
- `tests/`: Playwright checks. Run from `_build`: `tests/serve.sh node tests/audt.js` (needs playwright).

## Add a business
1. Run the scan per `biz/SPEC.md` (plus DIR_SPEC and DIRC_SPEC), writing `biz/<slug>.json` and its sidecars.
2. Add `biz/<slug>.json` to the list in `build.sh`, run it, run the tests, check it at `?b=<slug>`.

## Rules from Steve (always)
- Audit findings follow ONE template, 11 times: status, issue sentence, a visual of only this business's own data,
  the findings table, then exactly ONE "You vs. your 3 closest competitors" measure. No "How we fix it", no sources, no extra notes.
- Never invent numbers. Every figure comes from a tool result; unknown = null (shows as "–").
- High-risk categories (dispensary, cannabis, CBD, vape, smoke shop, hemp, kratom) show 4x the measured search volume,
  labeled "Est. searches" (Google hides most of that volume). `?concept=N` multiplies volumes for internal concepting only.
- `?news=preview` shows the scheduled press stories; the normal link shows only live coverage.
- Plain language, no em dashes, no orphan words on their own line, no new unverified claims or stats in subtext.
- Template copy stays industry-neutral; only a business's own data is specific.
