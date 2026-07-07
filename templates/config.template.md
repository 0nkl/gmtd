# GMTD Config — {{NAME}}

<!-- Written by gmtd-setup. Hand-editable. Skills read this before doing anything. -->
<!-- config_version: 2 -->

## Profile
- name: {{NAME}}
- role: {{ROLE}}
- context: {{ONE_LINE_CONTEXT}}
- work_pattern: {{WORK_PATTERN}}
- communication_style: simple   # simple | technical — how the AI explains things

## Files
- gmtd_folder: {{GMTD_FOLDER}}
- tasks: tasks.md
- lists: lists.md
- goals: goals.md
- log: log.md                   # may point to an existing journal outside this folder
- state: state.json
- inbox_file: off               # off | inbox.md — file-based capture

## Capture
- capture_mode: chat-only       # slack | chat-only | inbox-file
- braindump_channel: none       # e.g. "#gmtd-braindump (ID: C0XXXXXXX)"
- voice_memos: off              # on requires a transcription API key

## Tracking & completion
- tracking_mode: inline         # inline | slack-channel | both
- tracking_channel: none
- time_logging: off             # on = keep ↳ time logs for review reflection

## Briefing
- briefing: on
- briefing_target: chat         # chat | slack #channel | dashboard-only

## Scheduled tasks
- morning_briefing: off         # off | "daily 07:00"
- weekly_review_reminder: off   # off | "weekly sun 18:00"
- inbox_processing: off         # off | "daily 17:00"
- system_self_check: off        # off | monthly | every-2-months

## Priorities
- priority_lens: goals.md → Current #1
- focus_max: 5

## Planning style (see plugin reference/frameworks.md)
- daily_shape: gtd              # gtd | big3 | 1-3-5 | frog — shapes the briefing & "plan my day"
- focus_sessions: on            # "start a focus session on X" — one task, one goal, no switching

## Review
- weekly_review_phases: [inbox-sweep, projects, buckets, someday-scan]
  # available: inbox-sweep, tracking-sweep, email-scan, tracker-sync, sessions-sweep,
  #            projects, buckets, calendar-lookahead, stale-audit, someday-scan, goals-checkin

## Connectors (all optional — see plugin CONNECTORS.md)
- chat: none                    # slack | teams | none
- email: none                   # gmail | ms365 | none
- calendar: none                # google | ms365 | none
- calendar_time_blocking: off
- project_tracker: none         # clickup | monday | asana | linear | none
- tracker_sync: off             # pull-to-inbox | off

## Second brain (optional)
- wiki_integration: off
- wiki_index: none
- wiki_log: none

## Stale thresholds (days)
- focus_next: 10
- later: 30
- someday: 90
