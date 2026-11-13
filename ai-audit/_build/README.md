# Handoff: AI visibility audit (for Aneesh)

## What this is
One web page that runs our AI visibility audit for any business we've scanned.
Live: https://audit.localairegistry.com/ai-audit/  (type a business name in the search box)

Businesses in it today: Quiktox (demo), Spiritleaf Sherwood Park, Spiritleaf Salisbury,
Key Cannabis Belton, Key Cannabis KC North, Bridge City Collective, EsthetixMD,
Hello Smooth Med Spa, Illumé Med Spa.

Screens: AI score, What it's worth, Audit (11 checks), Our system (3D record), Why us, Proposal.

## Getting set up (one time, about 10 minutes)
1. Make sure Steve has added you to the GitHub repo `Local-AI-Registry/lair-audit`.
2. Install Claude Code if you don't have it: https://claude.com/claude-code
3. In a terminal:
   git clone https://github.com/Local-AI-Registry/lair-audit.git
   cd lair-audit
   claude
4. Tell Claude: "Read ai-audit/CLAUDE.md and ai-audit/_build/README.md, then rebuild the audit page and run the tests."
   If that works, you're set up.

## Everyday use: just ask Claude in plain English
- "Add <business name, full address> to the ai-audit page." It runs the scan and adds it to the search box.
- "In the ai-audit page, change <thing> on the <screen> screen."
- "Rebuild the ai-audit page, test it, and show me screenshots."
Always ask it to rebuild with ai-audit/_build/build.sh and test before publishing.

## Publishing
Anything pushed to the `main` branch goes live at audit.localairegistry.com in about a minute.
Safest habit: ask Claude to "commit on a new branch and open a pull request", review it, then merge.

## Rules Steve cares about (Claude knows these from CLAUDE.md, but you should too)
- The 11 audit findings all use the same simple template. One competitor comparison each. No extra notes or sources.
- Never make up numbers. If we don't know, it shows "–".
- Dispensaries and other high-risk categories show 4x search volume, labeled "Est. searches".
- No em dashes. Plain language a business owner understands.

## Don't touch
The other client folders in this repo, CNAME, the root index.html, 404.html, robots.txt and the
.github workflows. Never commit passwords, API keys or tokens.

## Scanning tools
A new business scan uses Semrush and DataForSEO (keyword volumes, rankings, map packs, AI answers).
Claude needs those connected in your Claude account to run scans. Editing the page needs nothing extra.
