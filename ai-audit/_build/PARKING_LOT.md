# Parking lot: ai-audit and lair-api

Things we decided to do later. Each item says where the work already is, so it can be picked up without starting over.

## Team password instead of team keys
For now the team signs in with the team key ("Team sign-in" under the home search box, "Team member? Run the live
scan" on the lead card, or a `?team=<key>` link). Later we'll switch to one shared team password.

- Page: built in lair-audit commit `3acca000` (reverted for now). The sign-in box says "Team password", checks it with
  the API's `/auth/me` before saving it, and the lead card runs the scan right after.
- API: built in lair-api commit `cbd4198` on `claude/outreach` (reverted for now): `/auth/me`, and ten wrong tries from
  one address wait 10 minutes. The password is the value of the `TEAM_KEYS` secret; how to set it is in that commit's
  `deploy/README.md` ("Setting the team password").
- To bring it back: revert the reverts in both repos, redeploy the API, then set the password and share it in person.
- Trade-offs to decide then: one shared daily scan limit for the whole team (`DAILY_SCAN_LIMIT`, 50), and changing the
  password signs everyone out.

## Sign in with Google (optional, after the password)
Built and reverted: lair-audit `46c7b002`, lair-api `c7f6940`. Only Google Workspace accounts on localairegistry.com get
in, sign-ins last 12 hours, and nobody handles keys. Needs an OAuth client ID (Web, origin
`https://audit.localairegistry.com`) set as `GOOGLE_CLIENT_ID` on the API.
