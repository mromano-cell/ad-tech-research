# Weekly Standup & To-Do List Tool

A Claude Code skill that processes your meetings, Slack messages, and emails into a prioritized weekly action item list. Drop this into your `.claude/skills/` folder to use it.

---

## Prerequisites

### MCP Servers Required
- **Google Workspace MCP** (for Calendar, Drive, Gmail, Docs)
- **Slack MCP** (for message search)

### Permissions to Allow (in `.claude/settings.local.json`)
Add these to your `permissions.allow` array:

```json
"mcp__google__get_events",
"mcp__google__search_drive_files",
"mcp__google__get_doc_as_markdown",
"mcp__google__list_drive_items",
"mcp__google__get_drive_file_content",
"mcp__google__search_gmail_messages",
"mcp__google__get_gmail_messages_content_batch",
"mcp__slack__slack_search_public_and_private"
```

### Folder Structure
Create these folders in your project directory:

```
tasks/
  active/        # Current action items
  completed/     # Done items
knowledge/
  private/
    GOALS.md     # Your current goals/priorities
backlog/
  BACKLOG.md     # Brain dump capture file
```

---

## Setup Instructions

1. Create the folder `.claude/skills/weekly-standup/` in your project
2. Save the skill definition below as `SKILL.md` in that folder
3. Ensure your Google Workspace and Slack MCP servers are connected
4. Add the permissions above to your `.claude/settings.local.json`
5. Customize the `AGENTS.md` or equivalent file with your stakeholder list

---

## Skill Definition (copy into `.claude/skills/weekly-standup/SKILL.md`)

```markdown
---
name: weekly-standup
description: Process meetings, Slack, and email from a given time period into prioritized action items. Use when the user asks to process their week, wants a standup, asks "what do I need to follow up on", or says "process my meetings".
---

# Weekly Standup & To-Do List Tool

Search Google Calendar, Drive transcripts, Slack messages, and Gmail to compile a complete picture of commitments, action items, and follow-ups.

## Trigger Variations
- "Process my meetings from last week"
- "What do I need to follow up on this week?"
- "What did [person] want from me?"
- "Give me my weekly standup"
- "What are my action items?"
- "Summarize my week"
- "What's on my plate?"

## Phase 1: Gather Context (Run in Parallel)

### 1a: Check Calendar
Use `mcp__google__get_events` to pull calendar events for the relevant time period:
- "today" → today 00:00 to 23:59
- "yesterday" → yesterday 00:00 to 23:59
- "this week" → Monday through today
- "last week" → previous Monday through Friday
- Use `detailed: true` to get attendee lists

### 1b: Search for Transcripts in Drive
Use `mcp__google__search_drive_files` with:
- `query: "transcript" AND mimeType = 'application/vnd.google-apps.document' AND modifiedTime > 'YYYY-MM-DDT00:00:00'`
- Also search: `query: "meeting notes" AND mimeType = 'application/vnd.google-apps.document' AND modifiedTime > 'YYYY-MM-DDT00:00:00'`

### 1c: Search Slack Messages
Use `mcp__slack__slack_search_public_and_private` to find:
- **Outbound messages** (commitments made): `query: "from:<@YOUR_SLACK_USER_ID> after:YYYY-MM-DD before:YYYY-MM-DD"`
- **Inbound messages** (requests received): `query: "to:<@YOUR_SLACK_USER_ID> after:YYYY-MM-DD before:YYYY-MM-DD"`
- Use `sort: "timestamp"`, `include_context: true`, `max_context_length: 300`

Look for:
- Commitments you made ("I'll send that", "let me check", "I can do that")
- Requests from others ("can you", "could you", "when you get a chance", "need you to")
- Unresolved threads where you said you'd follow up
- Escalation flags

### 1d: Search Gmail
Use `mcp__google__search_gmail_messages` to find:
- `query: "from:me after:YYYY/MM/DD before:YYYY/MM/DD"` (sent emails with commitments)
- `query: "to:me after:YYYY/MM/DD before:YYYY/MM/DD is:starred OR is:important"` (inbound requests)

Then use `mcp__google__get_gmail_messages_content_batch` to read message content.

Look for:
- Action items committed to in replies ("I'll send this over", "will follow up")
- Inbound requests awaiting response
- Emails sent that are awaiting a reply from someone else
- Client-facing communications with open loops

### 1e: Check Backlog
Read `backlog/BACKLOG.md` for any manually captured items prefixed with `[MEETING]` or `[TODO]`.

## Phase 2: Match and Identify Gaps

- Cross-reference calendar events with found transcripts by matching titles and dates
- Flag calendar events that have NO matching transcript (the "gap audit")
- Deduplicate: if the same action item appears in a transcript AND a Slack follow-up, list it once (cite the meeting as primary source)

## Phase 3: Read and Analyze Transcripts

For each matched transcript:
1. Use `mcp__google__get_doc_as_markdown` to read the full content
2. Reference your stakeholder/team context file for name resolution

Extract:
- **Action items for you**: Commitments you made, tasks assigned to you
- **Action items you assigned to others**: Requests you made of other people
- **Decisions made**: Explicit agreements or choices reached
- **Deadlines mentioned**: Dates or timeframes referenced

## Phase 4: Output

### Full Weekly Processing Output

**Meetings Found:** [N meetings with transcripts, M without]

**Meetings Missing Transcripts:**
- [Meeting name] at [time] — no transcript found

---

**Action Items for You (from Meetings):**
| # | Source | Action Item | Assigned By | Due | Priority |
|---|--------|-------------|-------------|-----|----------|
| 1 | [meeting name] | [item] | [person] | [date/ASAP/unclear] | P0-P2 |

**Action Items for You (from Slack & Email):**
| # | Source | Action Item | From | Due | Priority |
|---|--------|-------------|------|-----|----------|
| 1 | Slack DM / Email thread | [item] | [person] | [date/ASAP/unclear] | P0-P2 |

**Action Items You Assigned to Others:**
| # | Source | Action Item | Assigned To | Status |
|---|--------|-------------|-------------|--------|
| 1 | [source] | [item] | [person] | Open/Done |

**Decisions Made:**
- [Meeting/Source]: [Decision and rationale]

---

**Top Follow-ups for This Week (Prioritized):**

**P0 (Today/Tomorrow):**
1. [item] — [why it's urgent]

**P1 (This week):**
2. [item] — [context]
3. [item] — [context]

**P2 (When time allows):**
4. [item] — [context]

---

Then ask: "Want me to create task files for these action items?"

## Phase 5: Task Creation (On User Confirmation)

Create task files in `tasks/active/` with this naming convention:
`YYYY-MM-DD-[category]-description.md`

Categories: `meeting-action`, `comms-action`, `follow-up`, `deliverable`

**Template:**
```
---
title: [Action item description]
category: [category]
priority: P0/P1/P2
status: active
created: YYYY-MM-DD
due: YYYY-MM-DD
source: [meeting/slack/email]
source_detail: [Meeting title or thread subject]
source_date: YYYY-MM-DD
assigned_by: [Person who assigned it]
---

# [Action item description]

## Context
[Brief context of why this was requested and where it came from.]

## Next Actions
- [ ] [First concrete step]
- [ ] [Second concrete step if applicable]

## Progress Log
- YYYY-MM-DD: Created from [source]
```

## Priority Rules

- **P0**: Due today/tomorrow, or blocking others, or has been explicitly escalated
- **P1**: Due this week, or committed to a stakeholder with a near-term expectation
- **P2**: No hard deadline, low urgency, or "when you get a chance" requests

## Rules

- Only flag clear commitments, not vague discussion
- Use your stakeholder/context file to resolve first names to full identities
- Never create duplicate tasks — check `tasks/active/` before creating
- For Slack: skip casual conversation, social messages, and emoji-only replies
- For Email: prioritize starred/important messages and threads with commitments in replies
- Deduplicate across sources: same item in transcript + Slack = list once, cite meeting as primary
- When priority is unclear, default to P1
```

---

## Customization Guide

### Things to personalize before using:

1. **Your Slack User ID**: Replace `YOUR_SLACK_USER_ID` in Phase 1c with your actual Slack member ID (find it in your Slack profile > three dots > "Copy member ID")

2. **Stakeholder Context File**: Create an `AGENTS.md` or `CONTEXT.md` in your project root that includes:
   - Your name, role, and team
   - Key stakeholders you work with (name, role, relationship)
   - Common acronyms your team uses
   - Active projects/initiatives

3. **Goals File**: Create `knowledge/private/GOALS.md` with your current quarterly goals so the tool can flag goal-aligned vs. unaligned work

4. **Adjust trigger phrases**: Add any team-specific language to the trigger variations

---

## Usage Tips

| When | What to do | Time |
|------|------------|------|
| Monday morning | Run "process my meetings from last week" | ~3 min |
| Daily | Run "what do I need to follow up on today?" | ~1 min |
| Before a 1:1 | Run "summarize my last 3 meetings with [person]" | ~2 min |
| End of day | Dump notes into `backlog/BACKLOG.md` with `[MEETING]` prefix | ~30 sec |
| Ad-hoc | Ask "what did [person] want from me?" | instant |

---

## How It Works (Plain English)

1. Pulls your calendar to know what meetings you had
2. Searches Google Drive for matching Gemini transcripts
3. Reads each transcript and extracts commitments you made and tasks assigned to you
4. Searches your Slack messages for requests and promises
5. Searches your Gmail for action-oriented threads
6. Deduplicates everything and prioritizes by urgency
7. Presents a single consolidated view of everything you owe
8. Optionally creates trackable task files

The gap audit tells you which meetings have NO transcript so you can backfill context before it fades.

---

## Troubleshooting

- **"MCP server disconnected"**: Reconnect Google Workspace MCP in Claude Code settings (Cmd+Shift+P > "MCP: Reconnect")
- **No transcripts found**: You must manually click "Transcribe" in Google Meet. There is no always-on auto-transcription toggle.
- **Slack search returns nothing**: Verify your Slack user ID is correct. Test with a simple search first.
- **Gmail permissions error**: Make sure the Gmail MCP tools are in your allowed permissions list.
- **Too many results**: Narrow the date range or ask for a specific person/topic.

---

## Optional Add-ons

### Monday Slack Summary
Add this to your skill to auto-send yourself a DM every Monday with outstanding items:
- Read all tasks in `tasks/active/`
- Filter for open items from the previous week
- Send via `mcp__slack__slack_send_message` to your own DM channel (your Slack user ID)

### Integration with `/standup`
Create a separate daily standup skill that:
1. Reads `tasks/active/` for today's priorities
2. Checks today's calendar for meetings
3. Surfaces meeting follow-ups due today
4. Returns a focused 3-item daily plan

### Win/Decision Logging
After completing P0/P1 tasks, prompt to log wins to `knowledge/private/WINS.md` and strategic decisions to `knowledge/private/DECISIONS.md`.
