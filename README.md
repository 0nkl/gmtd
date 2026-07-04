# GMTD — Get More Things Done

**An AI-run productivity system inspired by David Allen's *Getting Things Done®*.**

Your head is for having ideas, not holding them. GMTD gives everything on your mind to an AI that clarifies it with you, organizes it, and always knows your single best next action — so you never stare at a to-do list wondering where to start.

## Why this exists

Classic GTD works — until the *system maintenance* kills it. Clarifying captures takes discipline. Weekly reviews get skipped. Lists rot, trust dies, the system collapses. GMTD moves the heavy lifting to the AI:

- **You capture** — a message from your phone, a voice memo, a sentence in chat. Zero friction.
- **The AI clarifies** — asks the GTD questions (actionable? two minutes? whose move? which project?), suggests answers, you confirm with a tap.
- **The AI engages you** — "I have 20 minutes and low energy" → one recommendation, with the tiny first step to start in 30 seconds.
- **The AI reviews with you** — a guided 20–30 min weekly review that leaves every list current.
- **The AI *does* tasks** — GMTD's extension to GTD: tasks the AI can do or draft get tagged 🤖 and executed on demand. The 2-minute rule at machine speed.

Everything lives in plain markdown files in your own folder. No server, no database, no lock-in.

## Install

### Claude (Desktop app, Cowork, or claude.ai) — no technical skills needed

1. Open Claude and click **Customize** in the left sidebar (in Cowork: open the Cowork tab first, then Customize).
2. Go to the **Plugins** tab.
3. Under **Personal plugins**, click **+** → **Add marketplace** → **Add from a repository**.
4. Paste this repository's address: `https://github.com/<owner>/gmtd` — click Add.
5. Find **GMTD** in your plugin list and click **Install**.
6. Start a new conversation and say: **"set up GMTD"**.

That's it. Claude will interview you for about 10 minutes — where you want to capture thoughts, whether you want a morning briefing, what matters most to you right now — and then build your whole system, including a first brain-dump session so you finish with everything on your mind already organized.

You need a paid Claude plan (Pro, Max, Team, or Enterprise) to use plugins.

### Claude Code (for developers)

```
/plugin marketplace add <owner>/gmtd
/plugin install gmtd
/gmtd-setup
```

### Other AI agents (Codex and similar)

No plugin system needed — GMTD is just markdown and one Python script:

1. Download this repository (green **Code** button → **Download ZIP**, or `git clone`) into a folder your agent can access.
2. Tell your agent: *"Read AGENTS.md in the gmtd folder and set up GMTD for me."*

[AGENTS.md](AGENTS.md) tells the agent exactly how to run the system, including fallbacks for features it may not have.

Setup is a ~10-minute interview: who you are, what matters most right now, where you want to capture (Slack channel / chat / a file), whether you want a daily briefing (and scheduled when), which connectors to use — then a guided "mind sweep" so you finish with a full, working system, and a visual dashboard.

## The 5 skills

| Skill | Say | Does |
|-------|-----|------|
| `gmtd-setup` | "set up GMTD" | Onboarding interview, migration, settings changes, help |
| `gmtd-inbox` | "process my inbox", "remind me to…" | Captures → clarified, filed tasks (suggest-first, you confirm) |
| `gmtd-now` | "what's next?", "what's on my plate?" | One recommendation · daily briefing · dashboard |
| `gmtd-done` | "I finished X", "wrap up" | Complete tasks, keep projects moving, session handoff |
| `gmtd-review` | "weekly review", "quick priority check" | Guided weekly review · 5-min triage · system self-check |

Full guide: [reference/skill-guide.md](reference/skill-guide.md)

## Connectors (all optional)

GMTD works fully in chat with zero connectors. Connect tools for more:

- **Chat (Slack/Teams)** — capture channel on your phone; briefings delivered there
- **Calendar** — meetings in your briefing; GMTD can time-block tasks onto your calendar
- **Email** — sweeps find action items hiding in threads
- **Project tracker (ClickUp, monday.com, Asana, Linear…)** — your tracker tasks pull into GMTD so ONE system answers "what's next?"

See [CONNECTORS.md](CONNECTORS.md).

## How it maps to GTD

Capture → your channel/chat/file. Clarify → the AI-guided decision tree, incl. the 2-minute rule. Organize → Next / Scheduled / Later / Waiting / Projects / Someday + reference lists. Reflect → guided weekly review, monthly someday scan, goals check-in. Engage → time/energy-matched recommendations from a system you trust. Details: [reference/gtd-primer.md](reference/gtd-primer.md).

## Your data

`tasks.md` · `lists.md` · `goals.md` · `log.md` (what the AI did, when) · `config.md` (your settings) — readable markdown in your folder. `state.json` holds machine timestamps. Delete the folder and GMTD is gone; copy it and GMTD moves with you.

## FAQ

**Do I need Slack?** No. Chat-only and inbox-file capture work fully.
**Do I need to know GTD?** No. The AI runs the method; you just answer questions.
**Other AI tools (Codex etc.)?** The core is portable markdown + Python; see [AGENTS.md](AGENTS.md). First-class support is on the roadmap.
**Privacy?** Everything is local files + your own connected tools. No telemetry, no server.

---

*Getting Things Done® and GTD® are registered trademarks of the David Allen Company. GMTD is an independent open-source project, not affiliated with or endorsed by the David Allen Company.*
