# audit.localairegistry.com

Prospect audit reports for Local AI Registry. This repo publishes straight to
`https://audit.localairegistry.com` through GitHub Pages. Nothing here touches
localairegistry.com or any other Local AI Registry system.

## Publishing a report (Bridgette)

You do not need any special access. GitHub turns your file into a pull request and
a bot merges it for you.

1. Open this repo on GitHub and click **Add file** then **Create new file**
2. In the name box type the client folder and file: `sunrise-aesthetics/index.html`
   (lowercase, dashes, no spaces)
3. Paste the finished report HTML
4. Click **Propose new file**, then **Create pull request**
5. Within about a minute the bot merges it and comments with the live link:
   `https://audit.localairegistry.com/sunrise-aesthetics/`

To update a report, open the file in its folder, click the pencil, paste the new
version, and propose the change the same way.

Images or other files the report needs go in the same folder and are linked
relatively, for example `<img src="before.png">`.

## What the bot allows

Only files inside a client folder are merged automatically. Anything touching the
root files or `.github` stays open for Steve to review.

- `CNAME` keeps the site on audit.localairegistry.com
- `index.html` and `404.html` send anyone without a client link back to localairegistry.com
- `robots.txt` keeps reports out of search engines
- `.nojekyll` makes GitHub serve files exactly as committed
- `.github/workflows/publish-reports.yml` is the bot

Every report should carry `<meta name="robots" content="noindex">` in its head.
Reports are reachable only by their direct link.
