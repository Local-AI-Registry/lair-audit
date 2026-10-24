# audit.localairegistry.com

Prospect audit reports for Local AI Registry. This repo publishes straight to
`https://audit.localairegistry.com` through GitHub Pages. Nothing here touches
localairegistry.com or any other Local AI Registry system.

## Adding a report

1. Make a folder named after the client, lowercase with dashes: `sunrise-aesthetics`
2. Put the finished report in it as `index.html`
3. Commit to `main`

About a minute later the report is live at
`https://audit.localairegistry.com/sunrise-aesthetics/`

Images or other files the report needs go in the same folder and are linked
relatively, for example `<img src="before.png">`.

## Do not touch

- `CNAME` keeps the site on audit.localairegistry.com
- `index.html` and `404.html` send anyone without a client link back to localairegistry.com
- `robots.txt` keeps reports out of search engines
- `.nojekyll` makes GitHub serve files exactly as committed

Every report should carry `<meta name="robots" content="noindex">` in its head.
Reports are reachable only by their direct link.
