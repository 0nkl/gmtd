# Frameworks — optional lenses on top of GTD

GTD is GMTD's backbone: capture → clarify → organize → reflect → engage never changes. These frameworks are **opt-in lenses** that shape how the day is planned and how priorities are triaged. All are off by default; the user picks them at setup or anytime ("change my GMTD settings"), stored in config under `## Planning style`.

## Daily shapes (`daily_shape` — used by briefing and "plan my day")

All shapes draw from the same candidate pool (`gmtd.py query`, matching-rules.md order: deadlines → Focus → Next). The shape changes how the day is framed, not what qualifies.

### `gtd` (default)
Classic GMTD briefing: Focus, top Next items, today's hard landscape, one first move. No imposed day structure — the user engages by time/energy as gaps appear. Best for: fragmented days, calendar-driven work.

### `big3`
The day gets **three must-dos** ("if only these three happen, today was a win"). Pick from Focus first, then deadline/priority order. Briefing leads with them; everything else is listed as "after the three." Best for: people who overplan and finish nothing.

### `1-3-5`
**1 big thing (30–60min+), 3 medium (15–30min), 5 small (2–5min)** — nine slots, then the day is full. Great fit with GMTD's time tags. When proposing, fill the 1 and the 3 before the 5. Best for: list-lovers who need a realistic cap.

### `frog`
**Eat the Frog** (Brian Tracy): the day starts with the hardest, most-avoided important task — "the frog" — before anything else. Pick the frog by: overdue/due first, then the Focus item with the highest energy tag or the oldest added date (avoidance leaves fingerprints). Briefing names the frog and its first step; everything else comes after. Best for: procrastination on the big stuff.

**Building a day plan (any shape):** propose it (suggest-first), let the user swap items via one option question, then — if `calendar_time_blocking: on` and a calendar is connected — offer to block the plan onto today's calendar.

## Eisenhower triage (gmtd-review quick-triage option)

When the user asks "help me prioritize" and has many competing items (or asks for it by name), offer the **urgent × important grid**:

- **Urgent** = overdue or `[due:]`/`[defer:]` within 3 days, or an overdue Waiting follow-up.
- **Important** = 🔴, or directly serves goals.md Current #1.

| | Urgent | Not urgent |
|---|---|---|
| **Important** | Do first → Focus | Schedule → Next/Scheduled with a plan |
| **Not important** | Minimize → delegate ([🤖]?), shrink, or decline | Question → Later/Someday or delete |

Render the four quadrants with the actual tasks in each, then propose moves (suggest-first). The bottom-right quadrant is the point of the exercise: it's where lists go to bloat.

## Focus sessions (`focus_sessions` — gmtd-now)

Pomodoro's spirit without a timer dependency: **one task, one stated goal, no switching.**

1. "Start a focus session (on X)" → pick the task (given, or recommend one), state the session goal in one line ("in 25 minutes, the draft outline exists"), name the first physical step, then get out of the way.
2. The user works. No check-ins, no narration.
3. When they return ("done", "I'm back", "that took an hour") → gmtd-done handles it: mark done or log progress, time log if `time_logging: on`, and offer one thing: break or next session.

If the harness supports scheduled reminders, offer (once, at setup) an optional "check in after X min" nudge — never by default.

## Time-blocking (already built in)

Putting tasks on the calendar as appointments. GMTD implements it via `calendar_time_blocking: on` + a calendar connector: briefings and day plans end with "want me to block time for [task]?" GTD purists keep the calendar for hard commitments only — GMTD lets the user choose; a block created by choice IS a commitment.

## The 2-minute rule, machine speed (already built in)

GTD's "under 2 minutes → do it now" extended: if the AI can do or draft it, the AI does it now or tags it [🤖]. See gtd-primer.md.

## Suggesting a style (system self-check)

The monthly self-check may suggest ONE style change when the evidence fits — always as a proposal, never applied silently:

| Observed pattern | Suggest |
|---|---|
| Asks for "quick wins" often; big tasks stall | `1-3-5` (guarantees a big one daily) |
| Many done items but Focus untouched week after week | `frog` or `big3` |
| Briefings ignored, engages ad-hoc all day | stay `gtd`; suggest focus sessions instead |
| Long unstructured days, few completions | `big3` + time-blocking |
| Overwhelmed, everything feels urgent | one-off Eisenhower triage in the next review |
