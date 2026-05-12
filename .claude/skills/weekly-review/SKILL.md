---
name: weekly-review
description: Reflect on weekly progress, log wins, surface blockers, and plan next week. Use when the user says "weekly review", asks what they accomplished, or wants to plan next week.
---

# Weekly Review

A 15-30 minute session to reflect on progress and plan ahead.

## Trigger Variations
- "What did I accomplish this week?"
- "Quick weekly review: What did I finish, what's blocked, what's most important next week?"
- "How am I tracking against my goals?"
- "What's blocked or stalled?"
- "Help me plan next week"
- "What wins should I log from this week?"

## When to Do It

- Friday afternoon (reflect while fresh)
- Sunday evening (prep for the week)
- Monday morning (start week with clarity)

## Phase 1: Data Gathering

Read and analyze these files:

**Completions:**
- All files in `tasks/completed/` — focus on tasks completed in the last 7 days
- All files in `tasks/active/` — note any tasks marked `status: done` that haven't been moved yet

**Goal Progress & Blockers:**
- `knowledge/private/GOALS.md` — all current goals and themes
- All files in `tasks/active/` — tasks with `status: blocked` and tasks with no progress in 7+ days

**Meeting Activity:**
- Use `mcp__google__get_events` for the past 7 days (primary calendar)
- Use `mcp__google__search_drive_files` to find all transcripts from the past 7 days
- Count: meetings attended, transcripts available, gaps
- Read `tasks/active/` and `tasks/completed/` filtering for `category: meeting-action`

**Planning (if available):**
- Any 1:1 notes or manager context you want to reference for next week

## Phase 2: Synthesized Output

Present this structure:

1. **This Week's Accomplishments**
2. **Goal Progress** — for each goal, which tasks supported it; flag goals with no recent activity
3. **Blockers and Stalled Work** — list with blocker reason and suggested next step
4. **Meeting Intelligence Summary**
   - Meetings attended this week: [N]
   - Transcripts captured: [N] / [N] ([percentage]%)
   - Meeting action items created: [N]
   - Meeting action items completed: [N]
   - Outstanding meeting commitments: [list with who's waiting on Mike]
   - Decisions made in meetings: [list for DECISIONS.md]
5. **Suggested Wins** — draft entries for `knowledge/private/WINS.md`
6. **Next Week Priorities** — top 3-5 recommended tasks with reasoning

## Phase 3: Optional Actions

After presenting, offer:
- "Want me to add these wins to `knowledge/private/WINS.md`?"
- "Should I update `knowledge/private/GOALS.md` to reflect any priority shifts?"
- "Want me to run a red team review on anything you're sending this week?"

## Tips

- Block 30 minutes on your calendar
- Do it in a quiet space, not between meetings
- Be honest about what's stalled
- Update `knowledge/private/GOALS.md` if priorities have shifted
- Add wins to `knowledge/private/WINS.md` before you forget them
