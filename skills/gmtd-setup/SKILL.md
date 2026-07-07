---
name: gmtd-setup
description: >
  Set up, reconfigure, or explain GMTD (Get More Things Done). Trigger on: "set up GMTD",
  "install GMTD", "GMTD setup", "get started with GMTD", "quick start GMTD", "migrate my
  task list to GMTD", "change my GMTD settings", "change my briefing time", "switch my
  capture to Slack", "change my daily planning style", "how does GMTD work",
  "what can GMTD do", "which GMTD skill does what", "GMTD help".
---

# GMTD Setup — Onboarding, Migration, Reconfiguration, Help

Read first: `${CLAUDE_PLUGIN_ROOT}/reference/schema.md` (file formats), `${CLAUDE_PLUGIN_ROOT}/reference/interaction.md` (how to ask), `${CLAUDE_PLUGIN_ROOT}/reference/environments.md` (capability fallbacks). For help questions also `${CLAUDE_PLUGIN_ROOT}/reference/skill-guide.md`.

Detect the mode:
- **Help** ("how does it work", "what does X do") → answer from skill-guide.md and gtd-primer.md. Done.
- **Reconfigure** ("change my briefing time", "switch to Big 3 mornings") → read the user's config.md, make the confirmed change, update any affected scheduled task, log with op `setup`. If the config predates the current template (`config_version` comment), silently add any missing keys with their defaults while you're in there. Done.
- **First-time setup / migration** → run the interview below.

## First question: quick or full?

Ask (interactive options, per interaction.md):
1. **Quick start (~3 minutes)** — "Three questions and a brain dump. You can add connectors, briefings, and schedules anytime later." ← recommended for new users
2. **Full setup (~10 minutes)** — "Everything configured in one pass: capture channel, connectors, briefing, schedules, planning style."

Either way: use interactive option questions wherever possible — the user should mostly click, not type. Match the user's language. Keep explanations short and plain; this may be a non-technical user's first contact with the system.

## Quick start path (~3 min)

1. **Folder:** create `gmtd/` in the current workspace (don't ask unless the location is genuinely ambiguous). Copy templates; run the migration check below if an existing task file is found.
2. **You:** "What's your name, and what do you do?" (one question)
3. **What matters:** "What's the single most important outcome for you in the next 1–3 months?" → goals.md Current #1. One line on why this matters: every priority suggestion will be anchored to it.
4. **Mind sweep (do not skip):** "Now tell me everything on your mind — tasks, worries, ideas, commitments. Messy and unsorted is perfect." Process via the gmtd-inbox clarify flow (batch triage).
5. **Defaults for everything else** (say this in one line, don't enumerate): capture = just tell me in chat, briefing = on demand, planning style = classic, no connectors, no schedules. Write config.md, initialize state.json, log the setup.
6. **Finish:** dashboard + one "what's next?" dry run + the 5-skill cheat sheet + "Want your morning briefing on a schedule, or your Slack/calendar/email connected? Just ask anytime — say 'change my GMTD settings'."

## Full setup path (~10 minutes)

### Step 1 — Folder

Confirm which folder GMTD should live in (the current workspace folder is the default). Create `gmtd/` inside it. Copy each markdown file from `${CLAUDE_PLUGIN_ROOT}/templates/` (fill `{{PLACEHOLDERS}}` as the interview progresses). The dashboard template stays in the plugin — gmtd-now renders it on demand.

**Migration check (both paths):** if an existing task file is found (tasks.md or similar), offer to migrate: back it up first (`gmtd.py backup`, or a manual dated copy if it lives elsewhere), then map its content to the GMTD schema (run `gmtd.py parse` on it if it's schema-compatible; otherwise read and restructure with the user's confirmation). Carry over any sync timestamps into state.json.

### Step 2 — Who are you?

Name, role, one-line context, work pattern (long focus blocks vs. fragmented gaps — affects task recommendations), and communication style:
> "When I explain things about the system, plain language or technical detail?" → `communication_style`

### Step 3 — What matters most? (goals.md)

- "What's the single most important outcome for you in the next 1–3 months?" → `Current #1`
- "What are the 3–7 areas of your life/work you can't drop?" → Areas of responsibility

Explain in one line why this matters: every priority suggestion will be anchored to this.

### Step 4 — Capture

"Where will you capture thoughts when they hit you — especially away from your computer?"
- **A chat channel (Slack/Teams)** — check the connector is actually available (try listing channels). If not installed, guide installation, or fall back gracefully. Find or create the braindump channel; save its name + ID.
- **Just tell Claude in chat** — no setup needed.
- **A file** — create `gmtd/inbox.md`; the user dumps text there anytime; it's cleared on each processing.

Voice memos? If yes, confirm a transcription API key is available (test `scripts/transcribe.py`); otherwise set off and note the option.

### Step 5 — Connectors (all optional)

Detect which connectors are available. Offer each in plain language, only what exists or is easily installable (see `${CLAUDE_PLUGIN_ROOT}/CONNECTORS.md`):
- **Email** — "I can spot to-dos hiding in your inbox during sweeps and reviews."
- **Calendar** — "Your briefing will include today's meetings — and I can block time on your calendar for important tasks." (also ask: time-blocking on/off)
- **Project tracker (ClickUp, monday.com, Asana, Linear…)** — "I'll pull your open tracker tasks into GMTD so one system answers 'what's next?'."

Record choices in config. Nothing is required.

### Step 6 — Planning style

"How do you like your day to start?" (see `${CLAUDE_PLUGIN_ROOT}/reference/frameworks.md`; explain each in its one-liner):
- **Classic (recommended)** — priorities + one first move; you pick tasks as gaps appear → `gtd`
- **Big 3** — three must-dos, everything else after → `big3`
- **1-3-5** — one big, three medium, five small; then the day is full → `1-3-5`
- **Eat the Frog** — hardest important thing first, every day → `frog`

Mention once: "You can switch styles anytime — and focus sessions ('start a focus session') are always available."

### Step 7 — Tracking, briefing, log

- Tracking: "How do you want to log what you've done?" inline (just tell me — recommended) / a chat channel / both. Time-logging on/off (default off; on = weekly reviews show hours per project).
- Briefing: on/off; delivered where (chat / chat-channel / dashboard-only)?
- Log: "Do you already have a journal/log file an AI writes to? I'll use it — otherwise I'll create one." → config log path.

### Step 8 — Scheduled tasks (each opt-in)

Offer one at a time, create immediately on yes (via the scheduled-tasks capability; if this harness lacks it, say so and skip — see environments.md):
- Morning briefing (what time?)
- Weekly review reminder (which day/time?)
- Inbox processing reminder
- System self-check (monthly or every 2 months) — "the system reviews how well it's working for you and suggests improvements"

### Step 9 — Mind sweep (do not skip)

> "Now let's fill the system. Tell me everything on your mind — tasks, worries, ideas, commitments. Messy and unsorted is perfect."

Process the dump with the gmtd-inbox clarify flow (batch triage). The user must finish setup with a populated tasks.md — an empty system won't be trusted or used.

### Step 10 — Dashboard + dry run + close

Create the dashboard (see gmtd-now). Demo: "what's next?" against their real data. Write config.md (all answers), initialize state.json (`gmtd.py state set` for each key), log the setup (`gmtd.py log --op setup`), and print the cheat sheet: the 5 skills, one line each, from skill-guide.md.

## Rules

- Suggest-first everywhere; the user confirms. Interactive option questions per interaction.md.
- Every choice is changeable later — say so once.
- Skip gracefully: no connector, no problem; the system must work chat-only.
- Never put user-specific facts anywhere except the user's own config/goals files.

*Other GMTD skills: gmtd-inbox (captures→tasks), gmtd-now (what's next/plan my day/briefing/dashboard), gmtd-done (completions), gmtd-review (reviews).*
