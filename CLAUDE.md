# lair-audit — audit.localairegistry.com

Static site served by GitHub Pages at https://audit.localairegistry.com. One folder per client/page.
Pushes to `main` publish automatically. An existing workflow in `.github/workflows/` also publishes reports — leave it alone.

## Adding a page
- New page = new folder with an `index.html`: `<slug>/index.html` → https://audit.localairegistry.com/<slug>/
- Slugs: lowercase, hyphenated (e.g. `pricing`, `acme-corp`).
- Start from `_template/index.html` (replace `{{TITLE}}`, `{{HEADLINE}}`, `{{SUBTEXT}}`); extend the design freely.
- Self-contained: inline CSS/JS, no build step, no external trackers. Must work on mobile and in dark mode.

## SEO data for audits and proposals
- Use the **DataForSEO** connector for all SEO data: rankings, keywords, live Google results (SERPs), backlinks, competitors and Lighthouse speed tests.
- Do **not** use Ahrefs.
- Run live Google results from the client's own city (e.g. `Stroudsburg,Pennsylvania,United States`), and cite "DataForSEO" with the date in the page's sources.

## "What being AI's answer is worth" section (every proposal and audit)
Every new proposal or audit page includes this section, placed right after the scoreboard / "What you told us".
It uses the same math as Steve's ai-audit "What it's worth" screen: searches a month × 2.3% conversion (Ruler Analytics) × average price per customer, with a price slider and a per-search table.
1. Get real monthly volumes with DataForSEO `kw_data_google_ads_search_volume`, about 10 keywords per call:
   - Searches naming a town ("botox <town> pa", "med spa <town>", "<service> <town>") at the state level.
   - "Near me" searches at each trade-area city level.
   - Use the client's real services. Leave out searches with no volume, and leave out off-intent searches that would inflate the number (say which in `left_out`). Never estimate a volume.
2. Price: a cited average spend per visit for the category (med spa: $527, American Med Spa Association 2024 report). If none can be found, ask.
3. Write `<client>/worth.json` (format in `_template/worth.py`), then run `python3 _template/worth.py <client>/worth.json` and paste the output into the page, plus `_template/worth.css` into its `<style>`.
4. Tie the plan prices back to the estimated added revenue in the pricing part.

## Never touch (unless the request explicitly says so)
- `CNAME`, root `index.html`, `404.html`, `robots.txt`, `.nojekyll`, existing workflows in `.github/workflows/`
- Existing client folders (e.g. `atrium/`, `test-client/`) — never edit or delete them.
- Never commit secrets, API keys, or tokens.

## When you finish
Reply with the live URL the page will have once merged to `main`.
