#!/bin/bash
# Status Update Auto-Generator
# Runs daily via launchd. Checks schedule.yaml for reports due tomorrow,
# then invokes Claude Code to generate each one.

set -euo pipefail

PROJECT_DIR="/Users/mromano/Documents/Mike-Claude-Master-Folder"
SCHEDULE="$PROJECT_DIR/status-updates/schedule.yaml"
LOG_DIR="$PROJECT_DIR/status-updates/logs"
CLAUDE="/Users/mromano/.local/bin/claude"
TODAY=$(date +%Y-%m-%d)
TOMORROW=$(date -v+1d +%Y-%m-%d)

mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_DIR/$TODAY.log"
}

log "Status update checker started"
log "Today: $TODAY, Tomorrow: $TOMORROW"

# Check if Claude CLI exists
if [ ! -x "$CLAUDE" ]; then
    log "ERROR: Claude CLI not found at $CLAUDE"
    osascript -e 'display notification "Claude CLI not found. Status updates cannot generate." with title "Status Update Bot"' 2>/dev/null || true
    exit 1
fi

# Check if schedule file exists
if [ ! -f "$SCHEDULE" ]; then
    log "ERROR: Schedule file not found at $SCHEDULE"
    exit 1
fi

# Parse schedule.yaml for reports due tomorrow
# Uses basic text parsing since PyYAML is not installed
# Looks for report blocks and their next_due fields
REPORTS_TO_GENERATE=""

current_report=""
while IFS= read -r line; do
    # Detect report type headers (indented under reports:)
    if echo "$line" | grep -qE '^  (wrike|gtm|mbr):'; then
        current_report=$(echo "$line" | tr -d ' :')
    fi
    # Check next_due for the current report
    if [ -n "$current_report" ] && echo "$line" | grep -q 'next_due:'; then
        due_date=$(echo "$line" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')
        if [ "$due_date" = "$TOMORROW" ]; then
            REPORTS_TO_GENERATE="$REPORTS_TO_GENERATE $current_report"
            log "Report '$current_report' is due tomorrow ($TOMORROW). Queuing generation."
        fi
        current_report=""
    fi
done < "$SCHEDULE"

# Generate each report
if [ -z "$REPORTS_TO_GENERATE" ]; then
    log "No reports due tomorrow. Exiting."
    exit 0
fi

for REPORT in $REPORTS_TO_GENERATE; do
    log "Generating $REPORT status update..."

    OUTPUT_FILE="$LOG_DIR/${TODAY}-${REPORT}-output.log"

    # Run Claude Code with the status-update skill
    cd "$PROJECT_DIR"
    if "$CLAUDE" -p "/status-update $REPORT" > "$OUTPUT_FILE" 2>&1; then
        log "Successfully generated $REPORT status update"

        # macOS notification on success
        osascript -e "display notification \"$REPORT status update is ready in status-updates/\" with title \"Status Update Bot\" sound name \"Glass\"" 2>/dev/null || true
    else
        log "ERROR: Failed to generate $REPORT status update. See $OUTPUT_FILE"

        # macOS notification on failure
        osascript -e "display notification \"Failed to generate $REPORT update. Check logs.\" with title \"Status Update Bot\" sound name \"Basso\"" 2>/dev/null || true
    fi
done

log "Status update checker finished"
