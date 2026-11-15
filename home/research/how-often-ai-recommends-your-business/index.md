# How Often AI Recommends Your Business

> Local AI Registry reviews 14 sources: ask AI the same thing twice and Gemini’s sources overlap by only 0.46. How to measure how often AI recommends you.

Source: https://localairegistry.com/research/how-often-ai-recommends-your-business/
Updated: 2026-11-15
Publisher: Local AI Registry (https://localairegistry.com)

Research

By [Steve Lee](../../team/steve-lee/index.html), founder of Local AI Registry · Updated November 15, 2026

## Key findings

1. In research reviewed by Local AI Registry, the same query run twice shared 0.78 of its sources on Google Search, 0.66 on Google AI Overviews and 0.46 on Gemini (Grossman et al., SIGIR 2026).
2. In a preprint census of cafés, restaurants and bars in Bali reviewed by Local AI Registry, the overlap between repeated runs of the same query ranged from 0.45 for Gemini to 0.22 for Claude.
3. When ChatGPT was asked the same local question twice, a median of 39 minutes apart, a median of 29% of the businesses named in either answer were named in both, according to 8ight.AI data reviewed by Local AI Registry.
4. Only 10.8% of doctors named by an AI model without web search matched a real clinician in the queried city, versus 63.9% with web search on, in a preprint audit of the 100 largest US metro areas reviewed by Local AI Registry.
5. Wording changes who AI recommends: 74.7% of the people recommended for “an oculoplastic surgeon” were oculoplastic specialists, versus 46.6% for “a doctor who does eyelid lifts,” in a peer-reviewed study reviewed by Local AI Registry.
6. ChatGPT declined to recommend an orthopedic surgeon in 52.8% of 40,500 persona-based requests, and stated income, insurance status and location were the strongest predictors of a recommendation, according to research reviewed by Local AI Registry.
7. Only 3.5% of the businesses ChatGPT named in localized searches appeared at every point tested across a town, according to BrightLocal’s 2026 analysis reviewed by Local AI Registry.
8. In the Bali census reviewed by Local AI Registry, 85.6% of venues were never recommended by any of the four AI systems, and being named was associated with documentation such as a website, more reviews, listed prices and mentions elsewhere on the web.
9. Local AI Registry calculated that a business named in 40% of AI answers has a 95% confidence interval of roughly 17% to 69% after 10 answers and 31% to 50% after 100, so one answer cannot measure AI visibility.

## What is AI visibility, and why can’t one answer measure it?

Visibility in AI-generated local recommendations is best measured as how often a business is named under stated conditions. A single answer is a genuine observation, but on its own it cannot reliably estimate that frequency.

Consumers are adopting generative assistants for local decisions at speed. In BrightLocal’s 2026 survey of 1,002 US consumers, 45% reported using ChatGPT or another generative AI tool to find local businesses, up from 6% a year earlier.[1](../../research/how-often-ai-recommends-your-business/index.html#ref-1) As the behavior has spread, so has an informal method of judging it. An owner, marketer or analyst asks an assistant for the best provider in a category and city, and reads the reply as a verdict on where a business stands.

That reading carries over an assumption from conventional search, where a page of results could reasonably be treated as a ranking. A generative assistant does not return a stored list. It composes an answer at the moment of the request, from whatever it retrieves and infers under that request’s particular conditions. The research reviewed here points to a different unit of analysis.

### Terms used in this brief

AI visibility
:   How often, how prominently and how accurately a business is named in AI answers, measured as a rate across many answers to the same question.

Recommendation frequency
:   The share of AI answers that name a business under a stated set of systems, configurations, locations, phrasings and dates.

Answer engine optimization (AEO)
:   Making a business’s facts clear, consistent and machine-readable so AI systems include it accurately in their answers.

Generative engine optimization (GEO)
:   The academic term for optimizing content to be cited by generative AI search engines; used interchangeably with AEO.

Overlap (Jaccard similarity)
:   What two runs returned in both, divided by what they returned in either. 1 means identical results; 0 means nothing in common.

Confidence interval
:   The range that likely contains the true rate. A 95% interval only becomes narrow after many answers have been collected.

Web search (grounding)
:   When an AI assistant searches the web during a request instead of answering only from what its model learned in training.

Algorithm audit
:   A way to study a system that cannot be inspected directly, by querying it repeatedly and recording what it returns.

Preprint
:   A research paper shared publicly before peer review.

## Does AI recommend the same businesses every time you ask?

No. When the same query was run twice, Gemini’s sources overlapped by only 0.46, and in a census of Bali venues, Claude’s repeated local recommendations overlapped by just 0.22.

Variation in search results is not new. In a 2015 measurement study of Google Search, Kliman-Silver and colleagues found that 18% to 34% of results for local queries changed with the searcher’s location, and that local queries were also the noisiest category when repeated from the same place at the same time.[2](../../research/how-often-ai-recommends-your-business/index.html#ref-2) Generative systems add another layer of variability, because the answer is written rather than retrieved.

The clearest controlled comparison is a study presented at ACM SIGIR 2026 that examined Google Search, Google’s AI Overviews and Gemini on more than 11,000 real user queries.[3](../../research/how-often-ai-recommends-your-business/index.html#ref-3) When the same query was run twice, the overlap between the sources each system drew on, measured by Jaccard similarity, was 0.78 for conventional Search, 0.66 for AI Overviews and 0.46 for Gemini. Minor edits to a query, such as expanding a contraction or adding a question mark, reduced the rank-weighted similarity of AI Overview sources by 29%, compared with 14% for conventional Search.

Audits of local recommendations show the same pattern in the businesses named. A pre-registered census of every café, restaurant and bar in two Bali submarkets, conducted by a company that sells AI-visibility tools, collected 2,208 answers from four assistants over seven days.[4](../../research/how-often-ai-recommends-your-business/index.html#ref-4) Overlap between repeated runs of the same query ranged from 0.22 for Claude to 0.45 for Gemini. The study’s most consequential finding concerns time. When the queries were repeated two weeks later, overlap with the original answers (0.375) was comparable to overlap between reruns within the same period, and the author attributes most of the variation to sampling rather than drift.

**Figure 1. Ask the same question twice and Gemini's sources overlap by only 0.46, versus 0.78 for Google Search.** When the same query was run twice, the sources Google Search drew on overlapped by 0.78, Google AI Overviews by 0.66 and Gemini by 0.46 (Grossman et al., SIGIR 2026). In a separate preprint census of Bali venues, the local businesses named overlapped by 0.45 for Gemini down to 0.22 for Claude (Pitenin, 2026). Compare bars within a panel, not across panels. [SVG](https://localairegistry.com/research/how-often-ai-recommends-your-business/images/ai-recommendations-change-when-same-query-is-repeated.svg) · [PNG](https://localairegistry.com/research/how-often-ai-recommends-your-business/images/ai-recommendations-change-when-same-query-is-repeated.png) · [Phone SVG](https://localairegistry.com/research/how-often-ai-recommends-your-business/images/ai-recommendations-change-when-same-query-is-repeated-mobile.svg)

Data behind this chart

| Panel | System | Overlap between two runs (returned in both ÷ returned in either) |
| --- | --- | --- |
| A: sources, general queries | Google Search | 0.78 |
| A: sources, general queries | Google AI Overviews | 0.66 |
| A: sources, general queries | Gemini | 0.46 |
| B: venues recommended, Bali | Gemini | 0.45 |
| B: venues recommended, Bali | Perplexity | 0.40 |
| B: venues recommended, Bali | OpenAI | 0.29 |
| B: venues recommended, Bali | Claude | 0.22 |

Embed this figure

The distinction matters for measurement. If answers drifted steadily, the most recent answer would be an imperfect but current reading. If answers instead scatter around a relatively stable underlying tendency, as this evidence suggests, the tendency is the quantity worth estimating. Each answer is one observation of it, and only an accumulation of observations can show how strong it is.

AEO takeaway

One AI answer is a snapshot, not a ranking.

### What to do

Do not judge your AI visibility from one screenshot. Ask the same customer questions several times, on more than one assistant, and count how often your business is named.

### How Local AI Registry does it

Local AI Registry’s AI visibility audit shows how a business appears in AI answers today, where answers are wrong, and what competitors are cited for.

## What changes which business AI recommends?

Four conditions: the AI system and its settings, the place, the wording of the request, and time. With web search on, 63.9% of the doctors an AI model named matched a real clinician in the queried city, versus 10.8% with it off.

There is no single frequency. A business can be named often under some conditions and rarely under others. The literature identifies four sets of conditions that change the answer, and a credible measurement has to state which of them it holds fixed.

**Figure 2. Four conditions change which business AI recommends: real local doctors named rose from 10.8% to 63.9% with web search on.** System and configuration, place, wording and time each changed AI recommendations in published research. Each mini-chart comes from a different study and metric, so read each one on its own, not across quadrants. Findings selected and grouped by Local AI Registry. [SVG](https://localairegistry.com/research/how-often-ai-recommends-your-business/images/four-conditions-that-change-which-business-ai-recommends.svg) · [PNG](https://localairegistry.com/research/how-often-ai-recommends-your-business/images/four-conditions-that-change-which-business-ai-recommends.png) · [Phone SVG](https://localairegistry.com/research/how-often-ai-recommends-your-business/images/four-conditions-that-change-which-business-ai-recommends-mobile.svg)

Data behind this chart

| Condition | Finding | Value | Source |
| --- | --- | --- | --- |
| System and configuration | Doctors matching a real clinician in the queried city, web search off vs on (same model) | 10.8% vs 63.9% | Ibrahim & Zaki, 2026 (preprint) |
| System and configuration | Sources shared by AI Overviews and Gemini, “near me” queries (overlap) | 0.07 | Grossman et al., 2026 |
| Place | Real doctors named without web search, largest vs smallest third of US metro areas | 16.3% vs 9.5% | Ibrahim & Zaki, 2026 (preprint) |
| Place | Businesses ChatGPT named that appeared at every point tested across a town | 3.5% | BrightLocal, 2026 (industry) |
| Wording and context | Oculoplastic specialists recommended: “an oculoplastic surgeon” vs “a doctor who does eyelid lifts” | 74.7% vs 46.6% | Parikh et al., 2024 |
| Wording and context | ChatGPT responses declining to recommend an orthopedic surgeon | 52.8% | Haupt et al., 2026 |
| Time | Overlap with answers collected two weeks later | 0.375 | Pitenin, 2026 (preprint) |
| Time | Businesses named in either of two ChatGPT answers about 39 minutes apart that appeared in both (median) | 29% | 8ight.AI, 2026 (industry) |

Embed this figure

**System and configuration.** The assistant, the model behind it and whether it searches the web during the request all change the outcome. In an audit of provider recommendations across the 100 largest US metropolitan areas, Ibrahim and Zaki found that only 10.8% of doctors named by a proprietary model without web search matched a real clinician in the queried city; with search enabled, the same model reached 63.9%.[5](../../research/how-often-ai-recommends-your-business/index.html#ref-5) Systems also draw on different evidence. For “near me” queries in the SIGIR study, the overlap between sources used by AI Overviews and Gemini was 0.07.[3](../../research/how-often-ai-recommends-your-business/index.html#ref-3) Disagreement between platforms predates generative AI: Li and Hecht found that Google Maps ratings averaged about 0.7 stars higher than Yelp ratings for the same restaurants, and that the two platforms’ top-ten lists for a metropolitan area overlapped little.[6](../../research/how-often-ai-recommends-your-business/index.html#ref-6)

**Place.** Location operates at more than one scale. Between cities, Ibrahim and Zaki found that without search the share of real doctors named fell from 16.3% in the largest third of metropolitan areas to 9.5% in the smallest, a gradient that largely disappeared once search was enabled.[5](../../research/how-often-ai-recommends-your-business/index.html#ref-5) Haupt and colleagues found ChatGPT more likely to recommend an orthopedic surgeon for prompts set in New York City and Chicago than in Phoenix and Houston.[7](../../research/how-often-ai-recommends-your-business/index.html#ref-7) Within a single town, BrightLocal’s 2026 analysis of localized searches found that only 3.5% of the businesses ChatGPT named appeared at every point tested across the area.[8](../../research/how-often-ai-recommends-your-business/index.html#ref-8) Location effects are not uniform, however. For a stratified sample of general queries, the SIGIR study found that moving AI Overview requests from Newark to Austin reduced source similarity by only 0.01 to 0.02 relative to repeated runs from the same place.[3](../../research/how-often-ai-recommends-your-business/index.html#ref-3) How much place matters appears to depend on the system and the kind of question.

**Wording and context.** The words in a request, and what it reveals about the person asking, change who is named. In a peer-reviewed study of chatbot recommendations for oculoplastic surgeons in the 20 largest US cities, 74.7% of the individuals recommended in response to “an oculoplastic surgeon” were oculoplastic specialists, compared with 46.6% for “a doctor who does eyelid lifts.”[9](../../research/how-often-ai-recommends-your-business/index.html#ref-9) Haupt and colleagues submitted 40,500 persona-based requests for orthopedic surgeons to ChatGPT. It declined to recommend anyone in 52.8% of responses, and stated income, insurance status and location were the strongest predictors of whether a recommendation was given.[7](../../research/how-often-ai-recommends-your-business/index.html#ref-7) Research on brand recommendations points the same way: language models recommended luxury gifts disproportionately to people from high-income countries.[10](../../research/how-often-ai-recommends-your-business/index.html#ref-10)

**Time.** Repetition alone changes answers, as both the SIGIR study and the Bali census show, and it does so over short intervals. 8ight.AI’s 2026 study of local trades found that when ChatGPT was asked the same question twice, a median of 39 minutes apart, a median of 29% of the businesses named in either answer were named in both.[11](../../research/how-often-ai-recommends-your-business/index.html#ref-11) Over longer periods the systems themselves change, as model versions, retrieval sources and defaults are updated, which is why studies such as Parikh’s describe their findings as a record of a single point in time.[9](../../research/how-often-ai-recommends-your-business/index.html#ref-9)

AEO takeaway

State the conditions, or the number means nothing.

### What to do

When you check what AI says about your business, write down the assistant, whether it searched the web, the city, the exact wording and the date, and keep them the same when you check again.

### How Local AI Registry does it

Local AI Registry keeps an owner-confirmed public record of each business, so assistants that search the web find the same verified facts every time they look.

## What can AI visibility research prove, and what can’t it?

It can show how often, and under which conditions, a business is named. It cannot show why. Only 51.5% of sentences written by generative search engines were fully supported by their citations, and 38.3% of ChatGPT’s surgeon suggestions in one study were excluded on review.

Three limits shape what any measurement of AI visibility can claim.

The first is that being named and being named first appear to be different outcomes. In the Bali census, 85.6% of venues were never recommended by any of the four systems. Inclusion was associated with documentation, including having a website, more reviews, listed prices and mentions elsewhere on the web, while star rating was associated only with whether a venue was named first.[4](../../research/how-often-ai-recommends-your-business/index.html#ref-4) These are associations from one hospitality market, reported by a vendor-funded study, but they caution against collapsing inclusion and order into a single rank.

The second is that the sources an assistant displays are imperfect evidence of what produced its answer. In a peer-reviewed audit of four generative search engines, Liu, Zhang and Liang found that only 51.5% of generated sentences were fully supported by their citations, and only 74.5% of citations supported the sentence to which they were attached.[12](../../research/how-often-ai-recommends-your-business/index.html#ref-12) Citation patterns can indicate which sources are prominent in a category. They cannot establish cause.

The third is that a name in an answer is not necessarily a correct name. In the 2023 oculoplastic study, 38.3% of ChatGPT’s suggestions were excluded on review; across the three chatbots studied, the most common reasons were a provider practicing in a different city or not existing at all.[9](../../research/how-often-ai-recommends-your-business/index.html#ref-9) In the orthopedic study, 44.6% of recommended surgeons in a coded subset were valid.[7](../../research/how-often-ai-recommends-your-business/index.html#ref-7) Counting mentions without verifying them can overstate visibility, and in healthcare the cost of that error falls on patients as well as practices.

Underlying all three is a broader point: visibility is partly defined by the instrument that measures it. The foundational paper on generative engine optimization (GEO), the research term for what practitioners call answer engine optimization (AEO), measured visibility with explicitly defined impression metrics and reported that content changes raised it by up to 40% on its benchmark, with effects that varied by domain.[13](../../research/how-often-ai-recommends-your-business/index.html#ref-13) Findings of this kind show that visibility in generative answers responds to content. They do not show that a particular change will produce recommendations, or customers, for a particular business.

AEO takeaway

Being named is not the same as being named correctly.

### What to do

Check that AI answers that name you have the right city, services and details, and fix the sources AI reads when they do not.

### How Local AI Registry does it

Local AI Registry keeps a sourced, dated record of each business, which gives AI a verified source for the business’s name, location and services.

## How should a business measure how often AI recommends it?

Count across many answers under fixed conditions. A business named in 40% of answers has a 95% range of roughly 17% to 69% after 10 answers and 31% to 50% after 100.

If visibility is a frequency to be estimated, its measurement belongs to the tradition of the algorithm audit, which studies a system that cannot be inspected directly by querying it repeatedly and recording what it returns.[14](../../research/how-often-ai-recommends-your-business/index.html#ref-14) Read together, the evidence above suggests five principles for applying that method to local recommendations.

### Five principles for measuring AI visibility

1. **Report a rate, with its conditions.** The core quantity is the share of answers that name a business under a stated set of systems, configurations, locations, phrasings and dates. A rate reported without its conditions cannot be compared with another.
2. **Collect enough answers to support the claim.** One answer records only whether a business was named on that occasion; it cannot distinguish a business named in nine answers out of ten from one named in one out of ten. Under fixed conditions, a business observed in 40% of answers has a 95% confidence interval of roughly 17% to 69% after ten answers and 31% to 50% after one hundred.
3. **Separate inclusion from order.** Whether a business is named and where it appears when named respond to different factors and should be reported separately.
4. **Verify what is counted.** A mention should count only when the business exists, operates in the location asked about and offers the service requested.
5. **Distinguish noise from change.** A shift between two periods is meaningful only when it exceeds the variation seen within a period under the same protocol, the test the Bali census applied.

**Figure 3. A business named in 40% of AI answers has a 95% range of 17% to 69% after 10 answers and 31% to 50% after 100.** Illustrative calculation by Local AI Registry (95% Wilson score intervals, assuming independent answers under fixed conditions), not study data. The range narrows only as answers accumulate. [SVG](https://localairegistry.com/research/how-often-ai-recommends-your-business/images/ai-visibility-confidence-interval-by-number-of-answers.svg) · [PNG](https://localairegistry.com/research/how-often-ai-recommends-your-business/images/ai-visibility-confidence-interval-by-number-of-answers.png) · [Phone SVG](https://localairegistry.com/research/how-often-ai-recommends-your-business/images/ai-visibility-confidence-interval-by-number-of-answers-mobile.svg)

Data behind this chart

| Answers collected | 95% interval for an observed 40% rate |
| --- | --- |
| 5 | 12% to 77% |
| 10 | 17% to 69% |
| 20 | 22% to 61% |
| 50 | 28% to 54% |
| 100 | 31% to 50% |
| 200 | 33% to 47% |

Embed this figure
AEO takeaway

Measure a rate, not a rank.

### What to do

Track the share of answers that name your business, collect enough answers to trust it, and treat a change as real only when it is bigger than the normal variation between checks.

### How Local AI Registry does it

Local AI Registry’s free AI Score gives a broader diagnostic of how findable and recommendable a business is to ChatGPT, Gemini, Claude and Perplexity. It is a diagnostic, not the recommendation-frequency measure described in this brief.

From our data · 3D

## “best closed rhinoplasty surgeon in Los Angeles”: how often each business was named

**Is AI recommending you?**

See what AI says about your business, live, on a strategy call.

[Book a call](../../start/index.html)

## Named in AI in 90 days. *Guaranteed.*

Book a call and we’ll show you, live, what AI says about you today. If we miss the 90 days, we keep working for free until AI names you.

[Book a free AI check](../../start/index.html)[Call (213) 931-5633](tel:+12139315633)
