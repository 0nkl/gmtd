# Matching Rules — choosing what to work on

Used by gmtd-now (and the dashboard). Candidates come from `gmtd.py query`; these rules govern selection.

## Selection order

1. **Focus first.** If any Focus item fits the time + energy, recommend it.
2. **Then Next**, filtered by time + energy.
3. **Tiebreak 1: priority** — 🔴 > 🟡 > 🟢.
4. **Tiebreak 2: goals alignment** — prefer the task that most directly serves goals.md "Current #1".
5. **Tiebreak 3: staleness** — older `[added:]` wins (it's waited longer).

## Time matching

| Available | Eligible tags |
|---|---|
| 2–5 min | time:2min, time:5min |
| 15 min | + time:15min |
| 30 min | + time:30min |
| 60+ min / deep work | any; PREFER time:30min / time:60min+ (don't burn deep work on 2-min tasks) |

## Energy matching

| User energy | Eligible tags |
|---|---|
| low | energy:low only |
| medium | low, medium |
| high | any; prefer energy:high (don't waste a sharp mind on admin) |

## Defaults & special cases

- No time/energy given → ask ONCE with quick options; vague answer ("a bit") → assume 15 min / medium.
- "I want to work on [Project]" → skip filters, return that project's [NEXT] task.
- Never recommend from Later or Someday unless explicitly asked.
- Expired `[defer:]` items count as Next.
- If nothing fits (e.g. low energy but only high-energy tasks): say so honestly, offer the closest option's `→ next step` (the small first action often fits when the full task doesn't).

## Output contract (gmtd-now "what's next")

ONE recommendation, 5–8 lines: task, one-sentence why (cite goals.md or urgency), first step, time + energy tags. Alternatives only if the user asks "what else?". If the pick is stale (per schema thresholds), add one gentle line asking if it's still the right priority.
