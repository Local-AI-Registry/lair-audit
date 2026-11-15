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

## Faster delivery for AI agents and repeat visitors

### 1. Markdown at the same address (content negotiation)

Every indexable page already has a Markdown twin at <path>/index.md. Serve it at the page's own URL
when a request asks for Markdown, and the HTML to everyone else.

- If the request's Accept header contains text/markdown, answer with <path>/index.md,
  Content-Type: text/markdown; charset=utf-8.
- Always send Vary: Accept on these URLs, so caches and CDNs keep the two versions apart.
- Keep X-Robots-Tag: noindex on the Markdown response. Google keeps indexing the HTML.
- Browsers and Googlebot never send text/markdown first, so nothing changes for people or search.

Next.js (App Router) middleware, as a starting point:

```ts
// middleware.ts
import { NextResponse, type NextRequest } from "next/server";

export function middleware(req: NextRequest) {
  const accept = req.headers.get("accept") ?? "";
  const { pathname } = req.nextUrl;
  if (!accept.includes("text/markdown") || pathname.includes(".")) return NextResponse.next();
  const url = req.nextUrl.clone();
  url.pathname = (pathname.endsWith("/") ? pathname : pathname + "/") + "index.md";
  const res = NextResponse.rewrite(url);
  res.headers.set("Vary", "Accept");
  res.headers.set("X-Robots-Tag", "noindex");
  return res;
}
```

Only rewrite paths that have an index.md (deploy-manifest.json lists the indexable ones), and set the
Markdown Content-Type in the static file headers. Test:  curl -H "Accept: text/markdown" https://localairegistry.com/ai/chatgpt/

### 2. Compression

- Baseline: Brotli for HTML, CSS, JS, SVG, JSON, Markdown and TXT, with gzip as the fallback.
  Zstandard (zstd) where the CDN supports it.
- Compression dictionaries (RFC 9842, supported in Chromium browsers): HTML pages share most of their
  code, so a repeat visitor can download only the difference.
  - On HTML responses send:  Use-As-Dictionary: match="/*", match-dest=("document")
  - When a later request carries an Available-Dictionary header, compress against that page with
    Content-Encoding: dcb (Brotli) or dcz (Zstandard), and send Vary: Accept-Encoding, Available-Dictionary.
  - If the CDN offers this as a setting, use the setting rather than custom code. Crawlers don't keep
    dictionaries, so they keep getting normal Brotli or gzip.

### 3. An MCP server for AI agents

See MCP_SPEC.md: a small read-mostly server at https://localairegistry.com/mcp so assistants can look up
registry records and book a free AI check without scraping pages.

## Checks after go-live

- Every "index" URL returns 200 with the canonical equal to its own URL.
- Every "redirect" URL returns a single 301 hop to its target.
- No "noindex" URL appears in any sitemap.
- /llms.txt, /sitemap-ai.xml and a sample /<page>/index.md return 200.
- curl -H "Accept: text/markdown" on an indexable page returns Markdown with Vary: Accept; without the header it returns HTML.
- Response headers on HTML show Content-Encoding: br (or zstd), and dcb/dcz on a second page view in Chrome.
