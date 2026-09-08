<!-- 💬 Ask your AI: "Update voice-guide-frameworks.md with my preferences for writing strategic frameworks. Ask me questions about my style." -->
<!-- This ships with a real example. Update it to match your organization's framework format. -->

# Voice Guide: Framework Documents

> **Prerequisite:** Core voice principles (sentence style, data presentation, hypothesis format, banned phrases) are auto-loaded from `.claude/rules/voice-and-tone.md` or `.cursor/rules/voice-and-tone.mdc`. This file covers only framework-specific rules.

This guide covers framework-specific voice and structure rules for writing strategic documents.

## Document Purpose

Frameworks are written 1-2 months before design/engineering starts to align cross-org stakeholders and leadership. They're meant to secure buy-in on strategic direction, not to provide detailed implementation specs.

## Core Structure

Every framework must address these elements:

1. **User Problem**: Psychology & Choreography
2. **Ecosystem**: Map execution/levers to user psychology
3. **Risks & Challenges**: Hardest parts to build, riskiest assumptions
4. **What Do You Have to Believe** (WDYHTB): Dent model, not predictive model
5. **Market Research**: What's happening in the market
6. **Level of Effort/Sequencing**: Fast vs slow parts
7. **Prioritization**: Now, Next, Later

## Opening Style

**Start with Executive Summary:**
- Problem statement in first sentence
- Recommendation with specific resource allocation
- Key risks if unaddressed
- Critical questions for alignment

**Example:**
```markdown
## Executive Summary

AI is transforming how users discover information, presenting both a challenge (60% of searches now end without clicks) and an opportunity (to increase our visibility by making our content more machine-readable).

Based on our analysis, I recommend a three-pillar approach with specific resource allocation: Relevance (70-80% of resources), Visibility (20-30% of resources), and Defensible Content (initial testing in Q1).
```

## User Psychology & Choreography

This is a key framework concept. Go beyond "user flow" to describe:
- **Psychology**: Cognitive friction, confusion, attitude, motivation
- **Choreography**: Physical actions (scrolling, tapping, eye-scanning), navigation patterns

## Critical Questions for Alignment

Frame decisions as Question + Recommendation:

```markdown
**1. Content Creation Ownership**
* **Question**: Should X team write requirements or create content directly?
* **Recommendation**: X team writes requirements; specialized teams execute

**2. Resource Allocation**
* **Question**: Is 70-80% on core initiative the right split?
* **Recommendation**: Yes. Maximizes near-term impact while testing future initiatives
```

## Now, Next, Later Structure

Always use phased approach with:
- Clear resource allocation percentages
- Specific deliverables for each phase
- Impact estimates where possible
- "Why it matters" for each initiative

**Example:**
```markdown
### Phase 1: Now (Q3-Q4) - Foundation Building (70-80% Resources)

**1. Core Initiative (40% of Phase 1 Resources)**
* Specific deliverable 1
* Specific deliverable 2
* Why it matters: [connection to user problem]

**Projected Impact**: [specific metric range]
```

## Tactical Best Practices

1. Show visual mocks with concept
2. Have a designated note taker in review sessions
3. Bring in data people early
4. Plan on coming back twice (first conversation = assimilation, second = decision)
5. Make slides a question, not a statement

## Voice Checklist

Before finalizing a framework, verify:
- [ ] Starts with clear executive summary
- [ ] User psychology/choreography addressed (not just "user flow")
- [ ] Data-driven with specific numbers and citations
- [ ] Clear "Now, Next, Later" sequencing
- [ ] Risks with mitigations
- [ ] Critical questions for alignment
- [ ] No jargon or corporate-speak
- [ ] No em dashes
- [ ] Headers are descriptive and active
- [ ] Short paragraphs throughout
- [ ] Impact estimates where possible
