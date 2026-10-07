---
name: status-update
description: Generate a status update for a recurring report (wrike, gtm, mbr). Auto-invoked by launchd the day before each report is due, or run manually with /status-update [type].
---

# Status Update Generator

Generate copy-paste-ready status updates for Mike's 3 recurring reports. Each report has a distinct audience, format, and data source mix.

## Trigger Variations
- `/status-update wrike` — generate Wrike status update
- `/status-update gtm` — generate GTM biweekly update
- `/status-update mbr` — generate Monthly Business Report sections
- `/status-update` (no arg) — check schedule, generate anything due within 2 days

## Phase 1: Determine Scope and Reporting Period

1. Read `status-updates/schedule.yaml`
2. If a report type was specified, use that. If not, check each report's `next_due` — generate any due within 2 days of today.
3. Determine the reporting period:
   - Start: `last_generated` date + 1 day (if null, use `cadence_days` as lookback from today)
   - End: today
4. Store the period for use in data gathering.

## Phase 2: Data Gathering

Run these in parallel, filtered to the reporting period. Only pull sources relevant to the report type (see matrix below).

### 2a: Local Project Files (ALL report types)
- Read all files in `tasks/active/` — note priorities, statuses, progress log entries within the period
- Read `knowledge/private/WINS.md` — wins logged within the period
- Run `git log --after=PERIOD_START --before=PERIOD_END --oneline` — activity trail

### 2b: Google Calendar (ALL report types)
- Use `mcp__google__get_events` for the reporting period
- Filter out green/personal events (per existing rules)
- Note key meetings, attendees, and topics relevant to YA/IBCC/creative work

### 2c: Google Drive (ALL report types)
- Use `mcp__google__search_drive_files` with:
  - `query: "modifiedTime > 'PERIOD_START_ISO' AND (fullText contains 'IBCC' OR fullText contains 'YA' OR fullText contains 'creative' OR fullText contains 'Celtra')"` 
- Note docs created or significantly modified in the period — these are evidence of deliverables

### 2d: Slack Messages (GTM and MBR only)
- Use `mcp__slack__slack_search_public_and_private` with:
  - `query: "from:<@U02K11D88N5> after:PERIOD_START before:PERIOD_END"` (Mike's messages: commitments, updates shared)
- Focus on channels related to YA, IBCC, GTM, enablement, creative
- Skip #random, #social, casual conversation

### 2e: Gmail (MBR only)
- Use `mcp__google__search_gmail_messages` with:
  - `query: "from:me after:PERIOD_START before:PERIOD_END (IBCC OR YA OR creative OR Celtra OR pipeline)"` 
- Use `mcp__google__get_gmail_messages_content_batch` to read found messages
- Look for: stakeholder communications, leadership updates, partner discussions

### 2f: Salesforce Pipeline (MBR only)
- Use `mcp__salesforce__soqlQuery` with the query from `schedule.yaml` under `mbr_topics` where `include_sfdc: true`
- Pull: opportunity count, pipeline value, closed won count/value, new opps created in period
- Compare to prior period if prior data exists in previous status update files

### 2g: Knowledge Files (MBR only)
- Read `knowledge/private/DECISIONS.md` — decisions made within the period
- Scan most recent file in `reports/` — latest ad tech digest for market context

### 2h: Previous Status Updates
- Check `status-updates/` for the most recent file of this report type
- Use it to understand what was already reported (avoid repeating, show progression)

### 2i: Pending Context
- Read the `pending_context` list from `schedule.yaml`
- Include any items where the current report type appears in `pending_for`
- These are facts/decisions from recent periods that haven't been reported in this report type yet

## Phase 3: Generate Output

### For type: `wrike`

Read the `wrike_projects` list from `schedule.yaml`. For each project:

1. Search the gathered data (Calendar, Drive, Git, WINS.md, tasks) for activity matching that project's `search_terms`
2. Generate a dated status note in June Han's style: `M/DD: [lowercase narrative, 1-2 sentences, action-oriented]`
3. For `on_hold` projects: note the hold reason if known, or write "no updates" if nothing found
4. For `in_progress` projects: summarize the most significant activity

**Output format:**
```
# Wrike Status Update — [today's date]
Reporting period: [start] to [end]

## 1. YA Roadmap 2026 (On Hold)
[M/DD]: [status note]

## 2. Market research to identify YA adoption drivers (On Hold)
[M/DD]: [status note]

## 3. YA Creative Product Exploration (In Progress)
[M/DD]: [status note]

## 4. DCO GTM + Audience-specific Custom Creative Narrative (In Progress)
[M/DD]: [status note]

## 5. Drive DCO (IBCC) Adoption (In Progress)
[M/DD]: [status note]

## 6. YA IBCC White Paper (In Progress)
[M/DD]: [status note]

## 7. Updated YA Landing Page (On Hold)
[M/DD]: [status note]
```

**Style guide (match June's notes):**
- Lowercase start after the date
- Brief, action-oriented language
- Reference specific deliverables, people, or milestones
- Examples from June:
  - "9/17: established pre-sales creative process across GTM teams. working on communicating the new process out"
  - "9/3: proposed a pre-sales process for Celtra to YA working group. finetuning some details over email for key stakeholders."
  - "8/18: creating a new process for pre-sales creative exploration"

---

### For type: `gtm`

Generate one section for the GTM biweekly shared doc.

1. From gathered data, identify what was completed in the period (shipped, delivered, decided, shared)
2. From tasks/active, calendar, and recent communications, identify what's coming up next
3. Focus on strategic outcomes and decisions, not operational blow-by-blow. Individual deal closes, seller interviews, and partner feedback details belong in MBR, not GTM.

**Output format:**
```
# GTM Biweekly Update — [today's date]
Reporting period: [start] to [end]

**Intent-Based Custom Creative & YA Creative Partnerships (Mike Romano):**

- **Completed:**
  - [Outcome or decision 1. 1-2 sentences. What happened and why it matters.]
  - [Outcome or decision 2. Include sub-bullets for specific details like pricing changes or guardrail updates.]
  - [Outcome or decision 3.]
  - [3-5 bullets total]

- **Coming Up:**
  - [Next action 1 — specific, with timeframe if known]
  - [Next action 2]
  - [Next action 3]
  - [Next action 4 if applicable]
```

**Style guide:**
- Completed uses **bullets**, not a narrative paragraph. Each bullet is one outcome or decision, 1-2 sentences max. Use sub-bullets for specifics (e.g., pricing numbers, guardrail changes).
- Coming Up is a bulleted list of forward-looking actions with timeframes where known.
- Keep it strategic: process changes, pricing decisions, tool launches, cross-functional milestones. Not individual account updates or detailed enablement play-by-play.
- Conversational but specific. This is verbally delivered in most cases.
- Include names of teams involved, not individuals (unless leadership-level).
- If Mike can't attend, add slightly more detail so it reads well standalone.

---

### For type: `mbr`

Generate two sections for the Monthly Business Report.

**Section 1: Live Topic (optional)**

1. Review the gathered data for anything that warrants live leadership discussion:
   - New strategic decisions pending leadership input
   - Significant wins that leadership should hear directly
   - Cross-functional issues needing alignment
   - New partnerships or product developments with open questions
2. If a strong candidate exists, generate the live topic. If nothing qualifies, skip this section and note "No live topic recommended this month."

**Live topic output format:**
```
**Marketing (Mike):**

- **(LIVE TOPIC) [Topic Title]:** [Summary paragraph — what it is, why it matters, what you need from the room. 3-5 sentences.]
  - **[Sub-point 1 header]:** [Detail with specific data, pricing, comparisons]
  - **[Sub-point 2 header]:** [Detail]
  - **[Sub-point 3 header]:** [Detail]
  - **Recommendation:** [Clear recommendation with rationale]
```

**Section 2: Read-only update**

Read the `mbr_topics` list from `schedule.yaml`. For each topic:

1. Search the gathered data for activity matching that topic's `search_terms`
2. If `include_sfdc: true`, incorporate the Salesforce pipeline data
3. Generate a detailed update with specific metrics, names, dates, and links to docs

**Read-only output format:**
```
**Celtra / Intent Based Custom Creative (Mike Romano):**

- **Intent-Based Custom Creative (IBCC):**
  - **IBCC GTM Launch:** [Status narrative. Include SFDC data: N opportunities, $X pipeline, N closed won. Reference specific accounts if notable. Compare to prior period if data available.]
  - **IBCC Enablement:** [Training status, materials delivered, adoption metrics like seller confidence scores, teams reached.]
  - **IBCC Tactical Sprint:** [Outreach progress, number of target accounts, verticals covered, results so far.]
  - **Whitepaper Development:** [Current status, partners involved, ETA on asset.]
  - **IBCC Phase 2 – Search-Based Audiences:** [Product/eng scoping status, proposed scope, resource/timeline status.]
- **TTD Creative Partner Exploration:** [Partner status updates, any new developments, open questions.]
```

**Style guide:**
- This is the most detailed of the 3 reports
- Include specific numbers with sources (e.g., "SFDC data shows 22 YA Custom Display/Rich Media opportunities")
- Link to Google Docs where relevant (use the Drive file URLs found in Phase 2c)
- Bold partner names and key terms on first mention
- Be thorough — this is read-only, so it needs to stand on its own without verbal explanation

## Phase 4: Write Output and Update Schedule

1. Write the generated update to `status-updates/YYYY-MM-DD-[type].md`
2. Display the full output in the terminal for immediate copy-paste
3. Update `status-updates/schedule.yaml`:
   - Set `last_generated` to today's date
   - Bump `next_due` forward:
     - For `wrike` and `gtm`: add `cadence_days` (14) to current `next_due`
     - For `mbr`: calculate the first Wednesday of the next month
4. Update `pending_context` in schedule.yaml:
   - For any item where the current report type was in `pending_for`, remove this report type from the list
   - If `pending_for` is now empty, remove the entire item (it's been reported everywhere)
5. Offer: "Want me to copy this to your clipboard?" (use `pbcopy` on macOS)

## Rules

- Match the exact format and tone of each report type. Do not blend styles across reports.
- For Wrike: match June's lowercase, action-oriented style exactly.
- For GTM: use bullets for "Completed" (not a narrative paragraph). Keep each bullet strategic and outcome-focused.
- For MBR: be thorough and specific. This is the most detailed report.
- Never fabricate data. If Salesforce query fails or returns no results, say so explicitly.
- If a Wrike project has no activity in the period, say "no updates this period" rather than inventing content.
- Always check the previous status update file to avoid repeating the same content.
- For on_hold projects, only report if something changed the hold status.
- Reference AGENTS.md for stakeholder name resolution.
- Follow voice-and-tone rules: direct, specific, concise, no banned phrases, no em dashes.
