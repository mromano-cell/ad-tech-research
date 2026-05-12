---
name: standup
description: Quick daily focus planning. Use when the user asks what to work on today, needs help prioritizing their tasks, or signals they're overwhelmed.
---

# Morning Standup

A quick 2-minute check-in to set your focus for the day.

## Trigger Variations
- "I'm overwhelmed. What's the ONE thing I should focus on?"
- "I only have 2 hours before meetings. What can I realistically finish?"
- "Remind me what I was working on and what's next."

## What This Workflow Does

1. Reads all files in `tasks/active/` — notes priorities (P0-P3), statuses, due dates
2. Reads `knowledge/private/GOALS.md` — for alignment context
3. Checks yesterday's calendar via `mcp__google__get_events` for meetings
4. Searches Drive via `mcp__google__search_drive_files` for matching transcripts
5. Filters `tasks/active/` for `category: meeting-action` tasks due today
6. If today is Monday: gathers all outstanding `meeting-action` tasks from the previous week and sends a Slack DM summary to Mike (user ID: U02K11D88N5) via `mcp__slack__slack_send_message`
7. Returns a focused, prioritized daily plan

## Output Format

**Today's Recommendation:**

1. **[P0/P1] Task Name** (estimated time)
   - Why: [due date, blocking others, goal alignment]

2. **[Priority] Task Name** (estimated time)
   - Why: [reason]

3. **[Priority] Task Name** (estimated time)
   - Why: [reason]

**Meeting Follow-ups Due Today:**
- [action item] (from [meeting name], assigned by [person])

**Quick Wins Available** (< 30 min):
- [task]

**Unprocessed Meetings:**
- If yesterday's meetings lack transcripts/action items: "[N] meetings from yesterday lack action items. Run `/meetings` to process."

**Waiting On / Follow Up Needed:**
- [blocked tasks needing follow-up]

## Monday Slack Summary

If today is Monday, before presenting the daily plan:

1. Read all tasks in `tasks/active/` with `category: meeting-action`
2. Also check `tasks/active/` for any tasks created in the last 7 days that are still open
3. Send a Slack DM to Mike (channel_id: `U02K11D88N5`) via `mcp__slack__slack_send_message` with this format:

```
**Weekly Meeting Action Items**

Outstanding from last week:
- [ ] [Action item] (from [meeting name], assigned by [person], due [date])
- [ ] [Action item] ...

Completed last week:
- [x] [Action item]
```

Only include `meeting-action` tasks. Keep it scannable. After sending, include the Slack message link in the standup output.

## Rules

- Suggest no more than 3 focus tasks unless the variation says otherwise.
- If the user is overwhelmed, suggest only ONE task.
- If time-limited, only suggest tasks that fit the time window.
- Flag blocked tasks (status: blocked) and propose next steps.
- Prioritize by: overdue > P0 > blocking others > P1 with due dates > goal alignment.

## Tips

- Do this first thing, before Slack/email
- Keep it under 2 minutes — pick and start
- Use "Quick Wins" for gaps between meetings
- If stuck deciding, ask the AI to pick for you
