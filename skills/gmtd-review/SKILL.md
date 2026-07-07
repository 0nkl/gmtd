---
name: gmtd-review
description: >
  The GMTD weekly/monthly review, a 5-minute priority triage, or a system self-check.
  Trigger on: "weekly review", "monthly review", "GTD review", "review my tasks",
  "review my system", "clean up my task list", "quick priority check", "triage my
  priorities", "help me prioritize", "are my priorities right", "what should my focus
  be", "eisenhower", "urgent vs important", "everything feels urgent", "system check",
  "GMTD health check", "how am I using the system".
---

# GMTD Review — Weekly Review · Priority Triage · System Self-Check

Read first: user `config.md`, `${CLAUDE_PLUGIN_ROOT}/reference/schema.md`, goals.md. Interaction style: `${CLAUDE_PLUGIN_ROOT}/reference/interaction.md`. Detect the mode from the trigger.

**Cardinal rule for every mode: SHOW, don't reference.** Any time you ask the user to decide about a bucket, render its complete current contents as a compact list first (from `gmtd.py parse`). Never ask "anything in Later to move?" against a list the user can't see. Offer a dashboard refresh at the start so they can follow along visually.

## Mode A — Quick priority triage (5 min)

1. Show Focus and Next (sorted by priority, overdue/due flagged), plus `gmtd.py validate` results.
2. Propose specific changes anchored to goals.md Current #1: move to/from Focus, upgrade/downgrade priorities — one-line reason each. If priorities look right, say so; don't reshuffle for its own sake.
3. **Eisenhower option:** if the user asks by name, says everything feels urgent, or Focus+Next is overloaded (> ~15 open items with competing priorities), offer the urgent × important grid instead — build it per `${CLAUDE_PLUGIN_ROOT}/reference/frameworks.md` (urgent = due/defer ≤3 days or overdue; important = 🔴 or serves Current #1), render all four quadrants with the actual tasks, propose moves. The not-urgent/not-important quadrant gets the hard questions (Later? Someday? delete?).
4. Write confirmed changes (`gmtd.py backup` first if 3+ tasks move); ensure Focus passes validate (≤ focus_max, all critical). Log op `review`, subject "priority triage".

## Mode B — Full review (weekly ~20–30 min; monthly adds deep passes)

Run the phases listed in config `weekly_review_phases`, in this order, grouped GTD-style. Announce the arc once ("Get clear → get current → get creative — about 25 minutes"), then move briskly; confirm at the end of each phase, not each item.

**GET CLEAR** — empty the inboxes:
- `inbox-sweep`: unprocessed captures (braindump channel / Inbox section / inbox file) → offer to process now via the gmtd-inbox flow, or note for after.
- `tracking-sweep`: unsynced tracking posts → process via the gmtd-done flow.
- `email-scan` *(if `~~email`)*: threads needing reply/decision → propose as tasks.
- `tracker-sync` *(if `~~project tracker`)*: pull new open tracker tasks to Inbox.
- `sessions-sweep` *(if available)*: skim the week's AI-session history for loose ends; hold candidates for the projects phase.

**GET CURRENT** — make every list true:
- `projects`: for EACH project (show its goal + open tasks): progress this week? sub-tasks done-but-unmarked? still active, or → Later/Someday? Does it have a live [NEXT]? (script-verified; a project without a next action is stalled by definition).
- `buckets`: Waiting On (show all; overdue follow-ups → chase or move to Next) · Scheduled (expired defers → Next) · **due dates** (every overdue or due-this-week item: on track, reschedule with the user, or drop — an overdue due date must never survive the review) · Later (show all; anything ready for Next? >30 days → Someday?).
- `calendar-lookahead` *(if `~~calendar`)*: next 14 days; propose prep tasks for gaps.
- `stale-audit`: `gmtd.py stale` — for each flagged item: delete / defer / keep with a reason.
- If `time_logging: on`: show `gmtd.py stats` (done count, hours per project) and ask ONE reflection question ("match how the week felt?").

**GET CREATIVE:**
- `someday-scan`: monthly (check `state get last_someday_review`; if <28 days, 30-second glance instead). Show ALL Someday items: still someday / promote / delete.
- `goals-checkin`: "Is [Current #1] still the right #1?" Update goals.md if not — this keeps every future priority suggestion honest.

**CLOSE:** `gmtd.py backup`, then fix violations with the user until `gmtd.py validate` passes. Set Focus for the coming week (≤ focus_max, all 🔴). Update state keys (`last_weekly_review`, etc.). Log op `review` with counts. One-paragraph close: done count, changes, next week's Focus.

## Mode C — System self-check (absorbs "gtd-meta"; monthly scheduled or on demand)

Audience: possibly non-technical — obey `communication_style` strictly (default: no jargon, no file paths, no tool names).

1. Evidence: `gmtd.py state all` (gaps between timestamps = unused flows), `stats --days 30`, `stale`, log.md history, validate.
2. Diagnose in plain language, e.g.: "You haven't used the tracking channel in 5 weeks — everything gets logged in our chats instead. Want me to switch tracking to chat-only so the system matches how you actually work?"
3. Propose 1–3 concrete improvements max (config changes, schedule changes, habit suggestions — including, at most once, a planning-style suggestion per the evidence table in `${CLAUDE_PLUGIN_ROOT}/reference/frameworks.md`). **Apply only what the user confirms.** Update config/scheduled tasks accordingly.
4. Log op `system-check` with findings + decisions. `state set last_system_check`.

## Rules

- Show every list you ask about (cardinal rule above).
- Brisk > exhaustive: the review must feel like 25 minutes, not an interrogation.
- The review is the trust-building ritual — always end with a clean, validated system.

*Other GMTD skills: gmtd-inbox (captures→tasks), gmtd-now (what's next/plan my day/briefing/dashboard), gmtd-done (completions), gmtd-setup (settings/help).*
