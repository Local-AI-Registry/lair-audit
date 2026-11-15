# Local AI Registry MCP server: spec

## Why

AI assistants that act for people (find a business, compare options, book something) work better
calling a tool than reading web pages. The Model Context Protocol (MCP) is the common way to give them
those tools; Claude and ChatGPT both connect to MCP servers. Our product is the registry data, so a
small MCP server lets any assistant read a verified business record straight from the source.

## Shape

- Endpoint: https://localairegistry.com/mcp (Streamable HTTP transport).
- No sign-in for the read tools. They return only what is already public on the site.
- Built on the official MCP TypeScript SDK, inside the Next.js app as an API route or a small separate
  service. Tools call the existing service layer; no new data paths.
- Rate limit per IP and per client (start at 60 calls a minute), log every call (tool, args, latency,
  client name), no logging of personal data.

## Tools

### lookup_business
Find a business in the registry and return its record.
- Input: name (string, required), city (string), state (string), website (string)
- Output: matches (max 5), each with: name, address, phone, website, categories, hours, profile_url,
  record_last_checked (date), claimed (boolean), sources (list of where each fact came from)
- Only facts shown on the public profile page. No owner contact details.

### get_ai_visibility
What AI assistants said about a business the last time we checked.
- Input: profile_url or business id
- Output: checks (list): assistant, question asked, date, named (boolean), position, link to the
  public evidence when there is one
- Read from stored results only. The tool never runs new AI queries, so it can't be used to run up cost.

### find_businesses
Registry businesses for a category and place, in the order of our published best-of lists.
- Input: category (string), city (string), state (string), limit (default 10)
- Output: list of { name, profile_url, why_listed, last_checked }
- Same order and wording as the public best-of pages. Never returns a paid ranking.

### get_research
Our published findings on how AI picks local businesses.
- Input: topic (string, optional)
- Output: findings (list): claim, number, date, method summary, source_url
- Only published research pages. Every finding carries its page URL so the assistant can cite it.

### book_free_ai_check
Help someone book a free AI check for their own business.
- Input: business_name (string), website (string, optional), name (string, optional), email (string, optional)
- Output: booking_url (the scheduling page, with name and email pre-filled when given) and a one-line
  summary of what the check covers
- Returns a link for the person to confirm. The tool doesn't book on its own, so nothing is scheduled
  without the person choosing a time.

## Answers the server must not give

- Prices (the price is shared on a call).
- Anything about a business that isn't on its public profile.
- Health, legal or financial advice. The research tool reports findings only.

## Discovery

- Add the endpoint to llms.txt under a "For AI agents" heading once it is live.
- Add a short /developers page with the endpoint, the tool list and the rate limits.
- Register the server in the public MCP registries once it is stable.

## Done when

- An MCP client (for example Claude with a custom connector) can connect to https://localairegistry.com/mcp,
  list the five tools and get correct answers for a test business.
- Each tool's output matches the public page it comes from.
- Rate limits and logging are on, and the server returns a clear error for unknown businesses.
