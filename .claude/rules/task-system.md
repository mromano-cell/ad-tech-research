# Task System

## Task Files

- **Location:** `tasks/active/` for current work, `tasks/completed/` for finished tasks.
- **Naming format:** `YYYY-MM-DD-[category]-description.md`
- **Priorities:** P0 (Today, max 3), P1 (This week, max 7), P2 (Scheduled).

## Task File Template

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

## Priority Rules

When recommending tasks, prioritize in this order:
1. Overdue tasks
2. P0 tasks
3. Tasks blocking others
4. P1 tasks with approaching due dates
5. Tasks aligned to current goals (`knowledge/private/GOALS.md`)
