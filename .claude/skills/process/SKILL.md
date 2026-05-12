---
name: process
description: Turn messy brain dumps into organized, prioritized tasks. Use when the user says "process my backlog" or wants to organize captured notes into actionable tasks.
---

# Process Backlog

Turn messy brain dumps into organized, prioritized tasks.

## When to Use

- End of day: Process notes captured throughout the day
- Weekly: Clear out accumulated ideas
- After meetings: Turn action items into tasks

## Phase 1: Gather Context

Read `backlog/BACKLOG.md` first, then scan `backlog/` for any dropped files (CSVs, PDFs, etc.) that may relate to backlog items, or themselves implicitly be backlog items (e.g., the text of a JIRA ticket or email). Then gather context by reading:
- `knowledge/private/GOALS.md` — current goals and themes
- `knowledge/private/STAKEHOLDERS.md` — who people are when names are mentioned
- `tasks/active/` — existing tasks (to check for duplicates)

## Meeting Item Routing

Items prefixed with `[MEETING]` get special handling:
- Category: `meeting-action`
- Use the meeting-action task template (includes `source: meeting`, `meeting:`, `meeting_date:`, `assigned_by:` frontmatter fields)
- Cross-reference with calendar to fill in meeting date and attendees if possible

## Phase 2: Interactive Triage

Using the backlog items and context gathered, categorize each item and present to the user:

**Ready to create (N tasks):**
| Item | Category | Priority | Goal Alignment |
|------|----------|----------|----------------|
| ... | ... | ... | ... |

**Needs clarification (N items):**
- [item] — [specific question]

**Reference only (N items):**
- [item] — [where it will be filed]

**Duplicates skipped (N items):**
- [item] — [existing task it matches]

Get user confirmation before creating tasks.

## Phase 3: Task File Creation

After user confirms, create task files in `tasks/active/` for each confirmed task.

**Task naming format:** `YYYY-MM-DD-[category]-task-description.md`

**Task file template:**
```markdown
---
title: [Task title]
category: [category]
priority: P0/P1/P2
status: active
created: YYYY-MM-DD
due: YYYY-MM-DD (if applicable)
goal: [which goal this supports]
---

# [Task title]

## Context
[Why this task matters]

## Next Actions
- [ ] [First concrete step]
- [ ] [Second concrete step]

## Progress Log
- YYYY-MM-DD: [Note]
```

After creating all tasks, clear `backlog/BACKLOG.md` by replacing its contents with just the heading `# Backlog`. Leave any dropped files in `backlog/` — the user will clean those up manually.

## Tips

- Dump text notes into `backlog/BACKLOG.md` throughout the day — don't organize, just capture
- Drop files (CSVs, PDFs, screenshots) directly into the `backlog/` folder
- Process at least once per day to keep it manageable
- Be specific when clarifying — the AI will create better tasks
- Review created tasks briefly to catch misunderstandings
