---
name: gmtd-now
description: >
  Tell the user what to work on right now, give the daily briefing, or show the GMTD
  dashboard. Trigger on: "what's next", "what should I work on", "what do I do next",
  "I have X minutes", "I have low energy", "quick win", "what can I do right now",
  "what's on my plate", "what do I have today", "daily briefing", "morning briefing",
  "post my briefing", "today's overview", "show my dashboard", "open my GMTD dashboard",
  "refresh my dashboard".
---

# GMTD Now — Engage: Next Action · Briefing · Dashboard

Read first: user `config.md`, `${CLAUDE_PLUGIN_ROOT}/reference/matching-rules.md`. Detect the depth requested:

## Mode A — "What's next?" (one recommendation)

1. If time/energy not given, ask ONCE with quick options (2–5 min any energy / 15 min low / 15 min medium+ / 30+ deep work / tell me). Vague answer → 15 min medium.
2. Get candidates: `gmtd.py --dir <gmtd folder> query --time N --energy E`. Read goals.md for tie-breaks.
3. Apply matching-rules.md. Return ONE task, 5–8 lines: task · one-sentence why (cite goals.md Current #1 or urgency) · first step (the `→ next step`, or synthesize one) · time + energy tags. If the pick is [🤖], offer to just do it.
4. Stale nudge: if the pick exceeds the stale threshold (check `gmtd.py stale`), add one gentle line.
5. Alternatives only if asked ("what else?").

## Mode B — Daily briefing ("what's on my plate", scheduled morning task)

Build from `gmtd.py parse` + `stale` + `validate`:

```
📋 *GMTD — [Day, Date]*
🎯 *Focus:* (Focus items; if empty: "No Focus set — want to pick 1–3 for this week?")
⚡ *Up next:* (top 2–3 Next by priority, with time/energy tags)
📅 *Today:* (calendar events if ~~calendar connected; expired defers; Scheduled due ≤2 days)
⏳ *Waiting:* (overdue follow-ups only)
💡 *First move:* (single smallest action from top Focus/Next item)
⚠️ (max one stale flag — oldest item only)
```

- Deliver to `briefing_target` from config (chat, or post to the `~~chat` channel — short lines, readable on a phone in 30 seconds).
- If `calendar_time_blocking: on` and the day has open gaps: end with "Want me to block time for [top task] today?" → create the calendar event on confirm.
- `gmtd.py state set last_brief <now>`; log only if delivered to an external channel (op `brief`).
- If a briefing was already sent today, say so instead of double-posting (unless explicitly asked).

## Mode C — Dashboard ("show/refresh my dashboard")

Generate or refresh the visual dashboard from `gmtd.py parse` + `stale` + `stats` JSON:

- **Panels:** Resume Here · Focus (warning banner if validate shows a Focus violation) · Next with time/energy filter chips ("I have: 5 / 15 / 30+ min · low / med / high") · Waiting (overdue highlighted) · Scheduled (due soon) · Later & Someday (full contents, collapsible) · Reference lists summary · mini-stats (done this week, last review date, inbox count).
- **Buttons** (via sendPrompt): "What's next?" (pre-filled with selected chips) · "Process inbox" · "Wrap up" · "Weekly review".
- In Claude: render as a live artifact (create once, update thereafter). In harnesses without artifacts: write `dashboard.html` next to tasks.md and tell the user to open it.
- Data is embedded at refresh time — after big task changes, other skills offer a refresh.
- Read-only v1: buttons launch skills; direct editing in the dashboard is not supported (yet).

## Rules

- Mode A returns ONE thing. The entire point is killing decision fatigue.
- Never recommend from Later/Someday unless asked.
- Keep every mode fast — no ceremony, the user may have 5 minutes.

*Other GMTD skills: gmtd-inbox (captures→tasks), gmtd-done (completions), gmtd-review (reviews), gmtd-setup (settings/help).*
