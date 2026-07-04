# GMTD Schema — Single Source of Truth

Every GMTD skill reads this file for file formats, bucket definitions, and the task metadata schema. **Never duplicate this content into a skill — link to it.** User-specific values (paths, channels, names) live in the user's `config.md`, never here.

## User files

All in the user's GMTD folder (default `<workspace>/gmtd/`, actual paths in `config.md`):

| File | Purpose | Written by |
|------|---------|-----------|
| `config.md` | Personalization: profile, capture/tracking modes, connectors, schedules | gmtd-setup (and reconfiguration requests) |
| `tasks.md` | All tasks, all buckets | gmtd-inbox, gmtd-done, gmtd-review |
| `lists.md` | Reference lists (books, videos, learning…) — NOT to-dos | gmtd-inbox |
| `goals.md` | Horizons of focus: current #1 priority, areas of responsibility, 1–2yr goals | gmtd-setup, gmtd-review |
| `log.md` | Append-only activity journal (may point to an existing user journal) | every skill that writes, via `gmtd.py log` |
| `inbox.md` | Optional file-capture dump; cleared after each processing | user writes, gmtd-inbox clears |
| `state.json` | Machine state: sync timestamps, review dates | `gmtd.py state` ONLY — never hand-edit, never edit via LLM |

## tasks.md structure

Sections, in order (all H2):

```
## 📌 Resume Here      — 2–3 line handoff, overwritten by gmtd-done at each wrap
## 🗂 Inbox            — unprocessed captures awaiting clarification
## 🎯 Focus            — this week's top priorities; max per config focus_max (default 5); all 🔴
## ⚡ Next              — all active next actions with full metadata
## 📅 Scheduled        — deferred to a date ([defer:YYYY-MM-DD]); surfaces when due
## ⏳ Later             — active but not soon; reviewed weekly
## 👥 Waiting On        — blocked on someone else ([who] [since:date] [follow-up:date])
## 📁 Projects          — multi-step outcomes; each has exactly one [NEXT] task mirrored in Next
## 💤 Someday           — no commitment; reviewed monthly
## ✅ Done (recent)     — completed tasks with dates; pruned at monthly review
```

## Task line format

```
- [ ] Task description [time:2min|5min|15min|30min|60min+] [energy:low|medium|high] [priority:🔴|🟡|🟢] [added:YYYY-MM-DD]
  → next step: Smallest first action, starts with a verb [time:Xmin] [energy:low]
  (← Project Name)
  ↳ [YYYY-MM-DD] ~Xmin logged — optional note
```

- `→ next step:` is REQUIRED for any task with time ≥ 30min. Must be doable in 2–5 min.
- `(← Project Name)` links a task to its project.
- `↳` lines are time logs (optional per config).
- Optional markers: `[🤖]` = AI-delegable (Claude can do or draft this autonomously — say "do [task]"); `[defer:YYYY-MM-DD]` (Scheduled only); `[src:<tracker>:<id>]` = imported from a project tracker (used for de-duplication; keep on the line); `[NEXT]` = a project's current next action.
- Done: `- [x] Task ✓ (YYYY-MM-DD) — optional outcome note`. Dropped/superseded: `- [~] Task — reason`.

## Priority guide

- 🔴 Critical — directly serves the user's Current #1 in goals.md, or has real consequences if dropped
- 🟡 Important — strategic, matters for goals, not immediately blocking
- 🟢 Whenever — nice to do, no urgency

Priority suggestions must cite goals.md, e.g. "🔴 because it's on the direct path to [Current #1]."

## Buckets: which one?

| Situation | Bucket |
|---|---|
| Will work on it soon (days–2 weeks) | Next |
| This week's committed top items (≤ focus_max, all 🔴) | Focus (also stays in Next context) |
| Has a specific start/due date | Scheduled with `[defer:]` |
| Active but not soon | Later |
| Blocked on another person | Waiting On |
| Multi-step outcome | Projects (+ its [NEXT] task in Next) |
| Maybe someday, no commitment | Someday |
| Not a task at all (book, video, idea) | lists.md |

## lists.md structure

H2 sections chosen at setup (defaults: 📚 Books to Read, 🎬 Videos to Watch, 🎓 Things to Learn, 🎥 Movies / Shows, 💡 Ideas, 🔗 Other References). Entry: `- Title/description — context [added:YYYY-MM-DD]`. One line per item.

## goals.md structure

```
## Current #1        — the single most important outcome, 1–3 month horizon (THE priority lens)
## Areas of responsibility   — 3–7 ongoing areas (work, family, health…)
## Goals (1–2 years)  — optional
## Notes              — optional context
```

## log.md entry format

```
## [YYYY-MM-DD] <op> | <subject>
- 2–4 bullets: what changed, counts, notable decisions
```

`<op>` ∈ `setup | inbox | done | brief | review | system-check | edit`. Append-only, via `gmtd.py log`. If config points at an existing user journal, match its established format instead.

## state.json keys

`braindump_synced`, `tracking_synced`, `tracker_synced`, `last_brief`, `last_weekly_review`, `last_monthly_review`, `last_someday_review`, `last_system_check` — ISO 8601 datetimes. Read/write ONLY through `gmtd.py state get|set`.

## Stale thresholds (defaults; overridable in config)

- Focus/Next: 10 days with no time log or edit
- Later: 30 days
- Someday: 90 days (flag at monthly review)
- Waiting On: past its `[follow-up:]` date

## Invariants (checked by `gmtd.py validate`)

1. Focus ≤ focus_max, every Focus item 🔴.
2. Every project has exactly one [NEXT] task, and it exists in Next.
3. Every task ≥ 30min has a `→ next step`.
4. Every open task has time, energy, priority, and added tags.
5. No `[defer:]` date in the past (expired defers must move to Next).
6. No Waiting item past follow-up without a flag.
