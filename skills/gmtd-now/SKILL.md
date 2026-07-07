---
name: gmtd-now
description: >
  Tell the user what to work on right now, plan their day, run a focus session, give
  the daily briefing, or show the GMTD dashboard. Trigger on: "what's next", "what
  should I work on", "what do I do next", "I have X minutes", "I have low energy",
  "quick win", "what can I do right now", "what's on my plate", "what do I have today",
  "plan my day", "help me plan today", "what are my big 3", "what's my frog",
  "start a focus session", "let's focus", "focus on X", "pomodoro", "daily briefing",
  "morning briefing", "post my briefing", "today's overview", "show my dashboard",
  "open my GMTD dashboard", "refresh my dashboard".
---

# GMTD Now — Engage: Next Action · Day Plan · Focus Session · Briefing · Dashboard

Read first: user `config.md`, `${CLAUDE_PLUGIN_ROOT}/reference/matching-rules.md`. Interaction style: `${CLAUDE_PLUGIN_ROOT}/reference/interaction.md`. Detect the depth requested:

## Mode A — "What's next?" (one recommendation)

1. If time/energy not given, ask ONCE with quick options (2–5 min any energy / 15 min low / 15 min medium+ / 30+ deep work / tell me). Vague answer → 15 min medium.
2. Get candidates: `gmtd.py --dir <gmtd folder> query --time N --energy E` (overdue/due-today already rank first). Read goals.md for tie-breaks.
3. Apply matching-rules.md. Return ONE task, 5–8 lines: task · one-sentence why (cite goals.md Current #1, a deadline, or urgency) · first step (the `→ next step`, or synthesize one) · time + energy tags. If the pick is [🤖], offer to just do it.
4. Stale nudge: if the pick exceeds the stale threshold (check `gmtd.py stale`), add one gentle line.
5. Alternatives only if asked ("what else?").

## Mode B — Daily briefing ("what's on my plate", scheduled morning task)

Build from `gmtd.py parse` + `stale` + `validate`:

```
📋 *GMTD — [Day, Date]*
🎯 *Focus:* (Focus items; if empty: "No Focus set — want to pick 1–3 for this week?")
⚡ *Up next:* (top 2–3 Next by priority, with time/energy tags)
📅 *Today:* (⚠️ overdue + due-today items FIRST; calendar events if ~~calendar connected; expired defers; Scheduled due ≤2 days)
⏳ *Waiting:* (overdue follow-ups only)
💡 *First move:* (single smallest action from top Focus/Next item)
⚠️ (max one stale flag — oldest item only)
```

- **Shape it by `daily_shape`** (see `${CLAUDE_PLUGIN_ROOT}/reference/frameworks.md`): `gtd` = format above · `big3` = lead with "Today's Big 3" · `1-3-5` = "1 big / 3 medium / 5 small" plan · `frog` = "🐸 Your frog:" first, everything else after. Same candidate pool, different frame.
- Deliver to `briefing_target` from config (chat, or post to the `~~chat` channel — short lines, readable on a phone in 30 seconds).
- If `calendar_time_blocking: on` and the day has open gaps: end with "Want me to block time for [top task] today?" → create the calendar event on confirm.
- `gmtd.py state set last_brief <now>`; log only if delivered to an external channel (op `brief`).
- If a briefing was already sent today, say so instead of double-posting (unless explicitly asked).

## Mode C — "Plan my day" (interactive day plan)

Like the briefing, but a two-way session (~2 min):

1. Build the day plan per `daily_shape` from `gmtd.py query` + calendar (if connected): what fits around today's hard landscape.
2. Propose it; let the user swap items with ONE option question (per interaction.md). Keep the shape's discipline — a Big 3 day gets exactly three; 1-3-5 fills the 1 and the 3 before any 5.
3. On confirm: offer time-blocking (if on + calendar connected). Don't rewrite Focus — the day plan is today's slice, Focus is the week's.
4. Close with the first move: "Start with [X] — [first step]."

## Mode D — Focus session ("start a focus session", "let's focus on X")

If `focus_sessions` is off in config, mention it can be enabled and stop. Otherwise (see frameworks.md):

1. Task given → use it (fuzzy-match against tasks.md). Not given → recommend one via Mode A rules.
2. Open the session, 3 lines max: the task · the session goal ("in ~25 min, [outcome] exists") · the first physical step. Then stop talking — no check-ins, no narration.
3. When the user returns ("done", "I'm back") → hand off to gmtd-done: mark done or log progress + time. Offer exactly one follow-up: break, or next session.

## Mode E — Dashboard ("show/refresh my dashboard")

Generate or refresh the visual dashboard from `${CLAUDE_PLUGIN_ROOT}/templates/dashboard.template.html`:

1. Collect data: `gmtd.py parse` + `stale` + `stats` + `validate`, plus name/Current #1/focus_max/daily_shape from config + goals.
2. Inject into the template: replace the single line `const GMTD_DATA = /*GMTD_DATA*/null;` with the real JSON (the template's header comment documents the expected shape). Set the generated timestamp.
3. Render: in Claude, as a live artifact/preview (create once, update thereafter). In harnesses without artifacts: write `dashboard.html` next to tasks.md and tell the user to open it (double-click).
4. Data is embedded at refresh time — after big task changes, other skills offer a refresh. Buttons (What's next / Plan my day / Process inbox / Wrap up / Weekly review) work only inside Claude and hide themselves elsewhere.

## Rules

- Mode A returns ONE thing. The entire point is killing decision fatigue.
- Overdue items are never silently skipped — if one exists and doesn't fit the current gap, say so in one line.
- Never recommend from Later/Someday unless asked.
- Keep every mode fast — no ceremony, the user may have 5 minutes.

*Other GMTD skills: gmtd-inbox (captures→tasks), gmtd-done (completions), gmtd-review (reviews), gmtd-setup (settings/help).*
