# Brian's Voice Guide

This guide captures Brian's writing voice and style for professional documents at Yelp. Use this when drafting any written content: PEPs, frameworks, presentations, emails, Slack messages, or strategic docs.

## Core Principles

### Be Direct
- Lead with the point, not the context
- One idea per sentence
- Short paragraphs (2-8 sentences max)
- Get to recommendations quickly

### Be Specific
- Use real numbers, not "significant" or "many"
- Show calculations and logic
- Attribute data sources inline
- Estimate impact with ranges when uncertain

### Be Concise
- Cut unnecessary words
- Avoid corporate-speak and jargon
- No warm-up paragraphs
- Respect page limits in templates

### Be Simple
- Simple is always better than complex
- Favor plain language; avoid technical terms unless essential
- Use common words, not synonyms for flair
- Explain concepts with analogies or visuals when helpful
- Split up long or dense explanations
---

## Sentence Style

**Good:**
- "AI is transforming how users discover information, presenting both a challenge (60% of searches now end without clicks) and an opportunity."
- "Of the 2.2 million Q&A pages currently live on Yelp, more than half (approximately 52.6%) have zero answers."
- "If we generate and populate Q&A pages for high-intent business questions, then organic traffic to Yelp will increase."

**Bad:**
- "There are several key challenges and opportunities that AI presents to the search landscape that we should be thinking about."
- "A significant portion of our Q&A pages are underperforming relative to their potential."
- "We believe this could potentially have a positive impact on traffic metrics going forward."

---

## Opening Documents

Start with the most important information. No throat-clearing.

**For PEPs - TL;DR (2-8 sentences max):**
1. What you're proposing
2. The goal
3. How you'll measure success

**For Frameworks - Executive Summary:**
1. Problem statement (first sentence)
2. Recommendation with resource allocation
3. Key risks if unaddressed
4. Critical questions for alignment

**Example TL;DR:**
```markdown
This PEP proposes launching location-based Q&A pages where users can ask questions like "What's the best taco in Austin TX?" The goal is to capture organic traffic from high-intent local queries currently underserved on Yelp. Success will be measured by organic sessions to these new pages.
```

---

## Problem Statements

**User Problem (1-2 sentences):**
- What the user is trying to achieve
- What's blocking them
- Stay customer-focused

**Business Problem (1-2 sentences):**
- Which metric is impacted
- Why it matters now
- Impact-driven, not feature-driven

**Example:**
```markdown
### User Problem
Yelp users often have specific questions about businesses ("Are dogs allowed?", "Is there outdoor seating?") that go unanswered or are scattered across reviews, making it difficult to find reliable answers.

### Business Problem
Our Q&A coverage is limited and not optimized for search intent. Many high-traffic queries related to business attributes are not answered by indexable Yelp pages, resulting in missed SEO opportunities.
```

---

## Presenting Data

Lead with the insight, then cite the source:

**Good:**
- "Users search 10% more frequently when AI results are shown ([Google](link))"
- "In just five months, Yelp-ranking keywords triggering AI Overviews jumped from 0.81M to 6.4M (674% increase)"
- "Year-to-date, Q&A pages generated 3.5 million clicks from 665,000 indexed pages, an average of 5.26 clicks per page"

**Bad:**
- "According to Google, there has been an increase in search frequency"
- "We've seen significant growth in AI-related queries"
- "Our pages perform well on average"

---

## Hypothesis Format

Use the If/Then/Because structure:

> "If we [build this] then [this metric] will move because [this change in behavior]"

**Example:**
```markdown
If we use BAA to systematically source, answer, and surface high-intent Biz Q&A pages, then we will create indexable pages that match user intent, leading to increased organic sessions from Google Search.
```

---

## Opportunity Sizing

1. State the scale
2. Show the math
3. Include caveats

**Example:**
```markdown
Yelp hosts over 20.8 million businesses. If we generate one quality question for half of these, we could add 10.4 million new indexable Q&A pages. Using our current benchmark of 5.26 clicks per page, this could represent 54 million incremental clicks.

Caveats:
* Actual volume will vary based on query intent and popularity
* Longer-tail Q&A may see lower per-page engagement
* We lack granular data on zero-answer page performance
```

---

## Risks & Constraints

Use paired structure:

```markdown
**Constraints**
* **Quality Control**: Maintaining accuracy and helpfulness of answers is critical
* **Duplicate Content**: Preventing duplicate questions is important for SEO
* **Scalability**: Generating content at scale requires strong automation

**Risks**
* **SEO Cannibalization**: New pages may compete with existing Yelp content
* **Low Engagement**: If questions are too broad, pages may see minimal interaction
* **Moderation Challenges**: Open-ended questions invite spam
```

---

## Anti-Goals

State what you explicitly DON'T want:

```markdown
### Anti-Goal
* Creating a new 'Yelp Talk'
* Low-quality, duplicate, or thin-content questions/answers
* Misinformation, off-topic answers, or SEO spam
```

---

## Phasing / Sequencing

Use Now, Next, Later with:
- Resource allocation percentages
- Specific deliverables
- Impact estimates
- "Why it matters"

```markdown
### Phase 1: Now (Q3-Q4 2025) - Foundation (70-80% Resources)

**1. Structured Data Expansion (40% of Phase 1)**
* Deploy Schema markup across key page types
* Add entity associations
* Why it matters: Structured data is the foundation for AI visibility

**Projected Impact**: +500K to 1M+ incremental sessions
```

---

## Critical Questions

Frame decisions as Question + Recommendation:

```markdown
**1. Content Creation Ownership**
* **Question**: Should SEO write requirements or create content directly?
* **Recommendation**: SEO writes requirements; specialized teams execute

**2. Resource Allocation**
* **Question**: Is 70-80% on Relevance the right split?
* **Recommendation**: Yes. Maximizes near-term impact while testing future initiatives
```

---

## Never Say

These phrases are banned:

| Banned | Use Instead |
|--------|-------------|
| boost, enhance, robust | improve, strengthen, reliable |
| Key insight | [just state the insight] |
| Here's the thing | [delete] |
| Moving forward / Going forward | [delete] |
| At the end of the day | [delete] |
| It's worth noting that | [delete] |
| Em dashes (-) | commas, periods, or parentheses |
| leverage (as verb) | use |
| utilize | use |
| synergy | [delete or be specific] |

---

## Document-Specific Guides

### PEPs
- Follow the 7-step structure exactly
- Respect "1-2 pages max" per section
- Include all 4 checkpoints
- Fill RAPID table with actual names
- Reference: `knowledge/voice/voice-guide-peps.md`

### Frameworks
- Start with Executive Summary
- Address User Psychology & Choreography (not just "user flow")
- Include Now/Next/Later sequencing
- End with Critical Questions for Alignment
- Reference: `knowledge/voice/voice-guide-frameworks.md`
- Reference: `knowledge/frameworks/qualities/qualities-of-good-framework-review.md`

---

## Voice Checklist

Before sending any document:

- [ ] Starts with the point, not context
- [ ] Short paragraphs (2-8 sentences max)
- [ ] Specific numbers with attribution
- [ ] Calculations shown where relevant
- [ ] No banned phrases
- [ ] No em dashes
- [ ] Recommendations stated clearly ("I recommend...")
- [ ] Risks acknowledged with mitigations
- [ ] Impact estimated where possible
