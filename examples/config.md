# GMTD Config — Sam Rivera

<!-- Written by gmtd-setup. Hand-editable. Skills read this before doing anything. -->
<!-- config_version: 2 -->
<!-- EXAMPLE FILE: Sam is a fictional freelance designer. This folder shows what a running GMTD system looks like. -->

## Profile
- name: Sam Rivera
- role: Freelance brand designer
- context: Solo designer juggling 3 client projects while trying to launch a template shop
- work_pattern: mornings deep work, afternoons fragmented (client calls, school pickup)
- communication_style: simple   # simple | technical — how the AI explains things

## Files
- gmtd_folder: gmtd/
- tasks: tasks.md
- lists: lists.md
- goals: goals.md
- log: log.md
- state: state.json
- inbox_file: off               # off | inbox.md — file-based capture

## Capture
- capture_mode: chat-only       # slack | chat-only | inbox-file
- braindump_channel: none
- voice_memos: off              # on requires a transcription API key

## Tracking & completion
- tracking_mode: inline         # inline | slack-channel | both
- tracking_channel: none
- time_logging: on              # keep ↳ time logs for review reflection

## Briefing
- briefing: on
- briefing_target: chat         # chat | slack #channel | dashboard-only

## Scheduled tasks
- morning_briefing: "daily 07:30"
- weekly_review_reminder: "weekly fri 16:00"
- inbox_processing: off
- system_self_check: monthly

## Priorities
- priority_lens: goals.md → Current #1
- focus_max: 5

## Planning style (see plugin reference/frameworks.md)
- daily_shape: big3             # gtd | big3 | 1-3-5 | frog — shapes the briefing & "plan my day"
- focus_sessions: on            # "start a focus session on X" — one task, one goal, no switching

## Review
- weekly_review_phases: [inbox-sweep, projects, buckets, stale-audit, someday-scan, goals-checkin]

## Connectors (all optional — see plugin CONNECTORS.md)
- chat: none                    # slack | teams | none
- email: gmail                  # gmail | ms365 | none
- calendar: google              # google | ms365 | none
- calendar_time_blocking: on
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
