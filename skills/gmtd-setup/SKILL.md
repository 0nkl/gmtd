---
name: gmtd-setup
description: >
  Set up, reconfigure, or explain GMTD (Get More Things Done). Trigger on: "set up GMTD",
  "install GMTD", "GMTD setup", "get started with GMTD", "migrate my task list to GMTD",
  "change my GMTD settings", "change my briefing time", "switch my capture to Slack",
  "how does GMTD work", "what can GMTD do", "which GMTD skill does what", "GMTD help".
---

# GMTD Setup — Onboarding, Migration, Reconfiguration, Help

Read first: `${CLAUDE_PLUGIN_ROOT}/reference/schema.md` (file formats) and `${CLAUDE_PLUGIN_ROOT}/reference/skill-guide.md` (for help questions).

Detect the mode:
- **Help** ("how does it work", "what does X do") → answer from skill-guide.md and gtd-primer.md. Done.
- **Reconfigure** ("change my briefing time") → read the user's config.md, make the confirmed change, update any affected scheduled task, log with op `setup`. Done.
- **First-time setup / migration** → run the interview below.

## The setup interview (~10 minutes)

Use interactive option questions (AskUserQuestion) wherever possible — the user should mostly click, not type. Match the user's language. Keep explanations short and plain; this may be a non-technical user's first contact with the system.

### Step 1 — Folder

Confirm which folder GMTD should live in (the current workspace folder is the default). Create `gmtd/` inside it. Copy each file from `${CLAUDE_PLUGIN_ROOT}/templates/` (fill `{{PLACEHOLDERS}}` as the interview progresses).

**Migration check:** if an existing task file is found (tasks.md or similar), offer to migrate: back up the original (`tasks.backup-YYYY-MM-DD.md`), then map its content to the GMTD schema (run `gmtd.py parse` on it if it's schema-compatible; otherwise read and restructure with the user's confirmation). Carry over any sync timestamps into state.json.

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

### Step 6 — Tracking, briefing, log

- Tracking: "How do you want to log what you've done?" inline (just tell me — recommended) / a chat channel / both. Time-logging on/off (default off; on = weekly reviews show hours per project).
- Briefing: on/off; delivered where (chat / chat-channel / dashboard-only)?
- Log: "Do you already have a journal/log file an AI writes to? I'll use it — otherwise I'll create one." → config log path.

### Step 7 — Scheduled tasks (each opt-in)

Offer one at a time, create immediately on yes (via the scheduled-tasks capability; if this harness lacks it, say so and skip):
- Morning briefing (what time?)
- Weekly review reminder (which day/time?)
- Inbox processing reminder
- System self-check (monthly or every 2 months) — "the system reviews how well it's working for you and suggests improvements"

### Step 8 — Mind sweep (do not skip)

> "Now let's fill the system. Tell me everything on your mind — tasks, worries, ideas, commitments. Messy and unsorted is perfect."

Process the dump with the gmtd-inbox clarify flow (batch triage). The user must finish setup with a populated tasks.md — an empty system won't be trusted or used.

### Step 9 — Dashboard + dry run

Create the dashboard (see gmtd-now). Then demo: "what's next?" against their real data.

### Step 10 — Close

Write config.md (all answers), initialize state.json (`gmtd.py state set` for each key), log the setup (`gmtd.py log --op setup`), and print the cheat sheet: the 5 skills, one line each, from skill-guide.md.

## Rules

- Suggest-first everywhere; the user confirms.
- Every choice is changeable later — say so once.
- Skip gracefully: no connector, no problem; the system must work chat-only.
- Never put user-specific facts anywhere except the user's own config/goals files.

*Other GMTD skills: gmtd-inbox (captures→tasks), gmtd-now (what's next/briefing/dashboard), gmtd-done (completions), gmtd-review (reviews).*
