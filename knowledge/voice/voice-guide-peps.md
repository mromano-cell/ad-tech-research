<!-- 💬 Ask your AI: "Update voice-guide-peps.md with my preferences for writing product proposals. Ask me questions about my style." -->
<!-- This ships with a real example. Update it to match your organization's PEP or proposal format. -->

# Voice Guide: Product Enhancement Proposals (PEPs)

> **Prerequisite:** Core voice principles (sentence style, data presentation, hypothesis format, banned phrases) are auto-loaded from `.claude/rules/voice-and-tone.md` or `.cursor/rules/voice-and-tone.mdc`. This file covers only proposal-specific rules.

This guide covers proposal-specific voice and structure rules for writing product proposals.

## Document Purpose

Product proposals are structured documents that move through checkpoint-based approvals. They're meant to secure alignment on problem, opportunity, solution, and experimentation before engineering starts.

## Core Structure

Every proposal must follow this exact structure:

1. **Header Table**: Date, Status, Stakeholder roles
2. **TL;DR**: 2-3 sentence summary
3. **Step 1: What is the Problem?** (1-2 pages max)
4. **Step 2: What is the Opportunity?** (1-2 pages max)
5. **Step 3: What is the Solution?** (1-2 pages max)
6. **Step 4: Experimentation** (if applicable)
7. **Step 5: Tech Spec** (link)
8. **Step 6: Test Results** (as they come in)
9. **Step 7: Retrospective & Next Steps**

## Opening Style

**TL;DR Format:**
- One clear sentence stating what you're proposing
- One sentence on the goal
- One sentence on expected outcome
- Keep total to 2-3 sentences maximum

**Example:**
```markdown
**TL;DR**
This proposal introduces location-based Q&A pages (starting at the city and state level) where users can ask and answer broad, local questions. The goal is to capture more organic traffic from high-intent local search queries that are currently underserved. Success will be measured primarily by an increase in organic sessions to these new pages.
```

## Solution Design

**Break into clear subsections:**
- User Experience Flow (numbered steps)
- Structural and Technical Design (bullet points)
- URL Structure
- Content Generation approach
- Quality controls

## Checkpoints

Every proposal includes mandatory checkpoints:
- **Checkpoint #1**: Are we aligned this is a problem worth solving now?
- **Checkpoint #2**: Are we aligned this is a worthwhile opportunity?
- **Checkpoint #3**: Are we aligned this is the right solution approach?
- **Checkpoint #4**: Are we aligned on the experimentation approach?

## Target User Description

**Format (1-2 sentences):**
- Who specifically
- What platform
- What they're NOT (sometimes important to clarify)

## Metrics & KPIs

**Structure:**
- Primary metric (north star)
- Secondary metrics (context)
- Guardrails (what not to hurt)

## Decision Framework (RAPID)

Always include a decision-making framework with clear roles:
- **RECOMMEND**: max 2 people
- **APPROVE**: typically 2-3 people
- **PERFORM**: min 2 people
- **INPUT**: as many as needed
- **DECIDE**: only 1 person

## Experimental Design

If including experiments, be specific:
- Experiment hypothesis (If/then/because format)
- Launch date (actual date, not "Q1")
- Population definition
- Success criteria with specific metrics
- Duration to reach statistical significance

## Voice Checklist

Before finalizing a proposal, verify:
- [ ] TL;DR is 2-3 sentences max
- [ ] User/Business problems are 1-2 sentences each
- [ ] Each section respects 1-2 page max guideline
- [ ] All checkpoints included
- [ ] Stakeholder table filled with actual names
- [ ] Hypothesis follows If/then/because format
- [ ] Opportunity sizing shows clear calculations
- [ ] Anti-goals stated explicitly
- [ ] No jargon or corporate-speak
- [ ] No em dashes
- [ ] Specific numbers with attribution
