# Deploying the marketing site to localairegistry.com

This folder is the static build of the marketing site. Every page says, in the first line of its
<head>, what it must be in production. The full list is in deploy-manifest.json.

## The three page states

| State | What to serve | Robots | Sitemap |
|---|---|---|---|
| index | the page, HTTP 200 | index,follow (already in the page) | listed in its sitemap-*.xml |
| noindex | the page, HTTP 200 | noindex,follow (already in the page) | never listed |
| redirect | an HTTP 301 to the "to" path | n/a | never listed |

The preview copy at audit.localairegistry.com/home/ marks every page noindex on purpose.
Only the production build (out-clean) carries the real robots tags. Never ship the preview copy.

## Rules for developers

1. Serve each folder's index.html at its path with a trailing slash: /ai/chatgpt/ serves ai/chatgpt/index.html.
   Paths without the slash 301 to the slash version, so canonicals and sitemaps match exactly.
2. Redirect pages are stand-ins because GitHub Pages can't send real redirects. In production,
   configure each "redirect" entry in deploy-manifest.json as a server-side 301 (for example in
   next.config.js redirects) and don't serve the stand-in HTML.
3. Don't change robots tags, canonicals or JSON-LD by hand. Change the generator and rebuild, or the
   manifest and the pages disagree.
4. Each indexable page has a Markdown twin at index.md and a <link rel="alternate" type="text/markdown">.
   Serve index.md with Content-Type text/markdown; charset=utf-8.
5. llms.txt and llms-full.txt live at the site root. They replace the current /llms.txt on the main site.
   The Markdown twins and llms files are for AI tools, not for search results: serve every *.md,
   llms.txt and llms-full.txt with the header  X-Robots-Tag: noindex  so Google doesn't index them as
   duplicates of the HTML pages. The HTML page stays the canonical version.
6. Keep the Organization @id https://localairegistry.com/#org and person @ids (/team/<slug>/#person)
   unchanged. Other surfaces (profiles, reports) should reference the same ids.

## Rules for cloud ops

1. robots.txt: keep the current main-site rules (they allow GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot,
   Claude-SearchBot, Claude-User, PerplexityBot, Perplexity-User, Google-Extended, Applebot-Extended)
   and add:  Sitemap: https://localairegistry.com/sitemap-ai.xml
2. Don't put a WAF or bot challenge in front of these paths for the AI crawlers above. A challenge page
   served to a crawler is the same as a blank page.
3. Cache: HTML 5 minutes, assets/ one year (file names change when content changes).
4. Compression: gzip or brotli on HTML, CSS, JS, SVG, JSON, Markdown and TXT.
5. After each deploy: submit sitemap-ai.xml in Google Search Console and Bing Webmaster Tools, and
   ping IndexNow with the changed URLs (indexnow.py does this).

## Checks after go-live

- Every "index" URL returns 200 with the canonical equal to its own URL.
- Every "redirect" URL returns a single 301 hop to its target.
- No "noindex" URL appears in any sitemap.
- /llms.txt, /sitemap-ai.xml and a sample /<page>/index.md return 200.
