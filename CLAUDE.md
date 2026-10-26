# lair-audit — audit.localairegistry.com

Static site served by GitHub Pages at https://audit.localairegistry.com. One folder per client/page.
Pushes to `main` publish automatically. An existing workflow in `.github/workflows/` also publishes reports — leave it alone.

## Adding a page
- New page = new folder with an `index.html`: `<slug>/index.html` → https://audit.localairegistry.com/<slug>/
- Slugs: lowercase, hyphenated (e.g. `pricing`, `acme-corp`).
- Start from `_template/index.html` (replace `{{TITLE}}`, `{{HEADLINE}}`, `{{SUBTEXT}}`); extend the design freely.
- Self-contained: inline CSS/JS, no build step, no external trackers. Must work on mobile and in dark mode.

## Never touch (unless the request explicitly says so)
- `CNAME`, root `index.html`, `404.html`, `robots.txt`, `.nojekyll`, existing workflows in `.github/workflows/`
- Existing client folders (e.g. `atrium/`, `test-client/`) — never edit or delete them.
- Never commit secrets, API keys, or tokens.

## When you finish
Reply with the live URL the page will have once merged to `main`.
