---
name: meetings
description: Find meeting transcripts, extract action items, and answer questions about past meetings. Use when the user asks about meeting follow-ups, action items from a meeting, what someone said/wanted, or says "process my meetings".
---

# Meeting Intelligence

Search Google Drive for meeting transcripts, extract action items for Mike, create tasks, and answer natural language questions about past meetings.

## Trigger Variations
- "Process my meetings from today"
- "What did [person] want from me?"
- "What are my follow-ups for next week?"
- "Find the transcript from my 1:1 with Lisa"
- "Summarize my meetings this week"
- "What action items came out of the YA working group?"
- "Did anyone assign me anything this week?"

## Phase 1: Gather Meeting Context

Run these in parallel:

### 1a: Check Calendar
Use `mcp__google__get_events` to pull Mike's calendar events for the relevant time period:
- "today" → today 00:00 to 23:59
- "yesterday" → yesterday 00:00 to 23:59
- "this week" → Monday through today
- Specific person → search calendar with their name as query
- Use `detailed: true` to get attendee lists

### 1b: Search for Transcripts in Drive
Use `mcp__google__search_drive_files` with:
- `query: "transcript" AND mimeType = 'application/vnd.google-apps.document' AND modifiedTime > 'YYYY-MM-DDT00:00:00'`
- Also search: `query: "meeting notes" AND modifiedTime > 'YYYY-MM-DDT00:00:00'`

### 1c: Check Backlog for Manual Meeting Notes
Read `backlog/BACKLOG.md` and scan for lines starting with `[MEETING]`.

## Phase 2: Match and Identify Gaps

- Cross-reference calendar events with found transcripts by matching titles and dates
- Flag calendar events that have NO matching transcript (the "gap audit")
- Match `[MEETING]` backlog entries to calendar events by date and keywords

## Phase 3: Read and Analyze Transcripts

For each matched transcript:
1. Use `mcp__google__get_doc_as_markdown` to read the full transcript
2. Reference `AGENTS.md` for stakeholder context and name resolution (e.g., "Joe" = Joe Kerber, SVP Head of MLoc Sales)

Extract:
- **Action items for Mike**: Commitments he made ("I'll send that over", "Let me take a look"), tasks assigned to him ("Mike, can you...", "Mike to follow up on...")
- **Action items Mike assigned to others**: Requests he made of other people
- **Decisions made**: Explicit agreements or choices reached
- **Deadlines mentioned**: Dates or timeframes referenced

## Phase 4: Output

Output varies by what the user asked.

### Mode A: "Process my meetings" (full extraction)

**Meetings Found:** [N meetings with transcripts, M without]

**Meetings Missing Transcripts:**
- [Meeting name] at [time] — no transcript found. Want to add manual notes?

**Action Items for Mike:**
| # | From Meeting | Action Item | Assigned By | Due | Priority |
|---|-------------|-------------|-------------|-----|----------|
| 1 | [meeting]   | [item]      | [person]    | [date/ASAP/unclear] | [P0-P2] |

**Action Items Mike Assigned to Others:**
| # | From Meeting | Action Item | Assigned To | Due |
|---|-------------|-------------|-------------|-----|
| 1 | [meeting]   | [item]      | [person]    | [date] |

**Decisions Made:**
- [Meeting]: [Decision and rationale]

Then ask: "Want me to create task files for these action items?"

### Mode B: Natural language query ("what did Joe want from me?")

- Search transcripts for mentions of the queried person (use AGENTS.md to resolve names)
- Return a direct, concise answer (under 50 words unless user asks for more)
- Quote or paraphrase the relevant portion
- Include meeting name, date, and link to the Google Doc

### Mode C: "Follow-ups for next week"

1. Read active tasks in `tasks/active/` with `category: meeting-action`
2. Search recent transcripts for items with future deadlines
3. Cross-reference with next week's calendar
4. Present a consolidated follow-up list sorted by date

## Phase 5: Task Creation

On user confirmation, create task files in `tasks/active/`:

**Naming:** `YYYY-MM-DD-meeting-action-[description].md`

**Template:**
```markdown
---
title: [Action item description]
category: meeting-action
priority: [P0 if due today/tomorrow, P1 if due this week, P2 if later/unclear]
status: active
created: YYYY-MM-DD
due: YYYY-MM-DD
goal: [matched goal from GOALS.md if applicable]
source: meeting
meeting: [Meeting title]
meeting_date: YYYY-MM-DD
assigned_by: [Person who assigned it]
---

# [Action item description]

## Context
From [Meeting title] on [date]. [Brief context of why this was requested.]

## Next Actions
- [ ] [First concrete step]
- [ ] [Second concrete step if applicable]

## Progress Log
- YYYY-MM-DD: Created from meeting transcript
```

After creating tasks, offer:
- "Want me to log any decisions to `knowledge/private/DECISIONS.md`?"

## Phase 6: Gap Audit

For each meeting without a transcript, ask: "Want to add a quick summary for [meeting name]?" If yes, capture the summary in `backlog/BACKLOG.md` with the `[MEETING]` prefix and process it immediately.

## Rules

- Only flag clear commitments, not vague discussion.
- When priority is unclear, default to P1.
- Use AGENTS.md stakeholder list to resolve first names.
- Never create duplicate tasks. Check `tasks/active/` before creating.
- Always provide a link to the source transcript Google Doc when available.

## Tips

- Run "process my meetings" at end of day (takes 2-3 minutes)
- Pair with `/standup` in the morning to see meeting follow-ups alongside regular tasks
- Before 1:1s, ask "summarize my last 3 meetings with [person]"
- Use `[MEETING]` prefix in BACKLOG.md for quick captures from non-Google-Meet calls
