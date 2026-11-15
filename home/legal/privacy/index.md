# Privacy Policy

> How Local AI Registry collects, uses, and protects information about you and the businesses we serve, including data accessed via Google Business Profile.

Source: https://localairegistry.com/legal/privacy/
Updated: 2026-11-15
Publisher: Local AI Registry (https://localairegistry.com)

Legal

Section 01

## Introduction

Local AI Registry is a product of **Blind LLC** (“we,” “our,” or “us”). When we say “the Services,” we mean our website at localairegistry.com, the owner dashboards it hosts, the public business profile pages we generate, the review-collection and photo-upload tools we host on your behalf, and the integrations that connect those tools to Google and the other platforms listed below.

By using the Services, you accept the practices described in this policy. If you do not agree, please do not use the Services. We’ll always tell you when this document materially changes (see Section 14).

Section 02

## Information we collect

### Information you give us directly

When you create an account, claim a business, or buy a plan, you provide your name, email address, phone number, business name and address, the services your business offers, and the keywords you want us to track. If you pay for a plan, your card details go directly to our payment processor, we never store or see full card numbers, CVV codes, or bank details.

### Information from the public web and our partners

For every business we surface on the public site, we collect information from Google Maps, public review platforms, business websites we scrape with permission, and SEO data providers (DataForSEO and others listed in Section 7). This includes hours, categories, photos, opening times, popular times, organic keyword rankings, backlinks, and reviews. We compute a Digital Score from these signals.

### Information from connected accounts

When you authorize a paid plan that includes the Google Business Profile integration, we receive access tokens that let us read and (with your approval) write to your listing on your behalf. See Section 4 for exactly what we do with that access, and how to revoke it at any time.

### Information collected automatically

When you visit the public site or your dashboard, we record limited usage information: your IP address (used briefly for spam protection and rate limiting), browser and device type, the pages you view, and how you arrived. We use this to keep the site fast, fix bugs, and protect against abuse.

We log a salted SHA-256 hash of (IP + 30-minute time bucket) on public profile pageviews so business owners can see how many distinct visitors viewed their profile this week without us storing the raw IP. After the bucket window expires, the hash cannot be reversed.

### Customers your business sends to us

If you use our review collection or photo upload tools, your customers may give us their name, rating, written feedback, and photos via your branded link. We process this on your behalf as your service provider; you remain the controller of that data. We do not contact those customers for any reason other than the flow they entered.

Section 03

## How we use your information

We use the information described in Section 2 to:

- Provide, operate, secure, and improve the Services.
- Compute Digital Scores and editorial summaries for every business listed on the public site.
- Deliver the SEO modules you have purchased, including drafting Google Business Profile posts, replying to reviews, building citations, and producing monthly reports.
- Process payments, manage subscriptions, and prevent fraud.
- Send transactional messages: phone verification codes, approval requests, billing receipts, weekly progress digests, and monthly reports.
- Respond to support requests and dispute resolution.
- Comply with legal obligations and enforce our Terms of Service.

We do not sell your personal information. We do not share it for cross-context behavioral advertising. We do not buy advertising profiles to target you.

Section 04

## Google API Services data

Local AI Registry accesses your Google account data only with your explicit OAuth authorization and only for the purposes you sign up for. **Local AI Registry’s use and transfer of information received from Google APIs to any other app will adhere to the [Google API Services User Data Policy](https://developers.google.com/terms/api-services-user-data-policy), including the Limited Use requirements.**

### Scopes we may request

Depending on the modules you purchase, we request access to the following Google services:

Sign in with Google
:   Basic profile (name, email, profile photo) so you can log in to Local AI Registry with your Google account.

Google Business Profile
:   Read your business listing details, posts, photos, reviews, and Q&A. Write new posts, photos, and review replies on your behalf when you approve them (or pre-approve them via Auto-Approve in Settings).

### How we use Google data

Google account information is used solely to identify you when you sign in. Google Business Profile data is used to populate your owner dashboard, surface what needs attention, draft content for your approval, and publish that content to your listing after you (or your designated approver) approve it. We do not use Google data to train generalized AI/ML models, and we do not transfer Google data to third parties except the sub-processors strictly necessary to operate the Services (Section 7).

### How to revoke access

You can revoke our access to your Google account at any time at [myaccount.google.com/permissions](https://myaccount.google.com/permissions). When you revoke access, any pending automated actions on your Google Business Profile are cancelled within minutes. The associated tokens are deleted from our systems within 24 hours.

Section 05

## AI-generated content

Local AI Registry uses large language models (OpenAI and Google Gemini, principally) to draft Google Business Profile posts, review replies, FAQ answers, monthly report narratives, and content suggestions. These drafts are generated against your business’s data, your selected brand voice, and your written brand rules.

Every AI-generated artifact that publishes to a public platform passes through an approval gate by default. You can pre-approve specific content types under Settings → Auto-Approve, in which case those drafts ship without per-item review, you remain fully responsible for the published output. We log every draft, every approval, and every publish so you can audit the chain end-to-end from your dashboard.

AI providers may briefly cache prompts and responses for safety and abuse-monitoring purposes per their published policies. We do not authorize providers to use your data for model training, and we use API tiers that contractually prohibit such use where available.

Section 06

## Cookies and similar technologies

Local AI Registry uses a small number of essential cookies: a session cookie when you log in, a CSRF protection cookie, and a preference cookie for any dashboard layout choices you make.

We also use two privacy-respecting analytics tools to understand how the site is used: Google Analytics and Microsoft Clarity. They tell us which pages people visit, how they arrive, and where the site is slow or confusing. Microsoft Clarity records anonymized session activity, clicks, scrolls, and page navigation, so we can find and fix bugs and rough edges. We use this only to measure and improve the Services. We do not use advertising cookies, we do not sell your information, and we do not track you across other sites for advertising (see Section 3).

Where we use a third party to deliver part of the Services (a hosted Stripe Checkout page, for example), that third party may set its own cookies on its own domain; their cookie policies govern that use.

Section 07

## Third-party processors

We rely on the sub-processors below to operate the Services. Each one receives only the data needed for its specific function, under a data-processing agreement that restricts re-use. You can request a current list at any time by contacting us.

Stripe
:   Payment processing, subscription billing, customer portal. We send Stripe your email, business name, and the modules you bought.

Twilio
:   Phone-number verification (SMS OTP) and outbound transactional SMS. We send Twilio your phone number and the message to deliver.

Resend
:   Transactional email (verification, approval requests, weekly digests, monthly reports). We send Resend recipient email addresses and message contents.

Google (Cloud, Places, Maps, PageSpeed, Business Profile)
:   Sign-in, location autocomplete, map rendering, site performance scoring, GBP read and write. Data flows are scoped per Section 4.

DataForSEO
:   Keyword ranking data, SERP screenshots, organic traffic estimates, backlink data, review ingestion, business listing data. We send DataForSEO public business identifiers (website, name, address, GBP placeId) and target keywords.

BrightLocal
:   Citation campaign management for paid customers on the Off-Page module. We send BrightLocal the business NAP (name, address, phone) and category data.

OpenAI
:   AI-generated content drafting (posts, replies, summaries, reports). We send OpenAI sanitized prompts containing business context, brand voice notes, and content goals. We use API tiers that prohibit training use of submitted data.

Google Gemini
:   AI-generated content drafting and AI visibility checks. Same handling as OpenAI.

SerpZilla / SerpClix / Adsy / RedPress
:   Off-page module vendors used only for customers actively enrolled in those modules &mdash; backlinks, CTR campaigns, press release distribution.

DigitalOcean
:   Application hosting, managed Postgres, object storage (DO Spaces) for photos and report PDFs.

Cloudflare
:   CDN, DDoS protection, bot mitigation in front of public routes.

Sentry
:   Error monitoring. Sentry may capture stack traces and request metadata when our application encounters an error. We scrub personally identifying parameters before sending.

No mobile information will be shared with third parties or affiliates for marketing or promotional purposes. Information sharing to subcontractors in support services, such as customer service, is permitted. All other use case categories exclude text messaging originator opt-in data and consent; this information will not be shared with any third parties.

Section 08

From our data · 3D

## “best rhinoplasty surgeon in San Diego”: how often each business was named

**Is AI recommending you?**

See what AI says about your business, live, on a strategy call.

[Book a call](../../start/index.html)

## Named in AI in 90 days. *Guaranteed.*

Book a call and we’ll show you, live, what AI says about you today. If we miss the 90 days, we keep working for free until AI names you.

[Book a free AI check](../../start/index.html)[Call (213) 931-5633](tel:+12139315633)
