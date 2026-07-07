---
name: gmtd-inbox
description: >
  Turn captures into properly filed GMTD tasks — from chat mentions, the braindump
  channel, an inbox file, voice memos, project-tracker tasks, or a full sweep of
  email/calendar/chat. Trigger on: "add this to my tasks", "remind me to", "I want to
  add", "can you add", "I should probably", "capture this", "process my inbox",
  "process my captures", "check my braindump", "sync my braindump", "sync my tracker
  tasks", "pull in my ClickUp/monday tasks", "do a full sweep", "deep sweep",
  "add to my reading list", "add this book/video to my list".
---

# GMTD Inbox — Capture → Clarify → Organize

Read first: user `config.md`, then `${CLAUDE_PLUGIN_ROOT}/reference/schema.md`. Interaction style: `${CLAUDE_PLUGIN_ROOT}/reference/interaction.md`. If no config.md exists, suggest running gmtd-setup.

## Step 1 — Gather captures (detect mode from context)

- **Chat mode:** the user just said things to capture. Use those; do NOT read external sources.
- **Channel sync** ("process my inbox/braindump"): read the configured `~~chat` braindump channel since `gmtd.py state get braindump_synced` (convert with `gmtd.py epoch <iso>` for APIs needing unix time). Handle voice memos via `scripts/transcribe.py`; images by describing actionable content. After processing, `state set braindump_synced` to the timestamp of the LAST message processed (never "now").
- **Inbox file:** read the configured inbox file; clear it after successful processing.
- **Tracker sync** (if `tracker_sync: pull-to-inbox`): fetch the user's open tasks from `~~project tracker`; skip any whose id already appears as `[src:...]` in tasks.md (check via `gmtd.py parse`). Imported tasks keep `[src:<tracker>:<id>]` and a link back.
- **Deep sweep** ("full sweep"): all of the above PLUS scan `~~email` (threads needing reply/decision, past 7 days) and `~~calendar` (upcoming events needing prep) for candidate action items. Only propose — never auto-file from a sweep.

Also read tasks.md (`gmtd.py parse`) and goals.md before classifying — you need current projects and the priority lens.

## Step 2 — Clarify each item (the GTD decision tree)

For every capture, walk this tree. Always suggest an answer with a one-line reason; the user confirms.

1. **Actionable?**
   - No → trash (confirm), **Someday** (idea worth keeping), or **reference** (books/videos/topics → the right lists.md section; substantive knowledge → the user's wiki if `wiki_integration: on`).
2. **Under 2 minutes?** → Propose doing it NOW (user does it, or it's AI-doable and you do it on the spot). Log as done immediately.
3. **AI-doable but bigger?** → Offer: "I can draft/do this — now, or tag it [🤖] for later?"
4. **Multi-step outcome?** → It's a project: ask for the outcome ("done means…"), why it matters (one line), and the first action. Create the project entry + its [NEXT] task in Next.
5. **Someone else's move?** → Waiting On, with who + follow-up date.
6. **Otherwise:** single action → bucket (Next / Scheduled+defer / Later / Someday per schema.md) + tags: time, energy, priority (cite goals.md Current #1 in your reasoning), added date. Tasks ≥ 30min MUST get a `→ next step` (2–5 min, starts with a verb).

**Deadline check (every actionable item):** if the capture implies a real deadline ("by Friday", "before the call", "tax deadline") → add `[due:YYYY-MM-DD]`. Ask only when a deadline is implied but unclear ("you said 'soon' — is there an actual date this must be done by?"). Never invent one: `due` is for hard deadlines, priority covers everything soft. `defer` = when it starts appearing; `due` = when it must be finished.

## Step 3 — Batch triage (default for 3+ items)

Present ALL classified items in one compact table: capture → proposed destination + tags + next step. The user corrects only what's wrong (use interactive option questions for ambiguous ones). One confirmation → write everything in one pass. Process one-by-one only when items are few or genuinely ambiguous.

## Step 4 — Write and close

- **Batch writes: `gmtd.py backup` first.** Then write confirmed entries to tasks.md / lists.md (small, precise edits — never rewrite whole sections). Single captures don't need the backup.
- Update state timestamps (`gmtd.py state set`).
- Append a log entry: `gmtd.py log --op inbox --subject "..." --bullet "N captures → X tasks, Y list items, Z done immediately"`.
- Offer a dashboard refresh if many items changed.
- Report in 2–3 lines: what was filed where, anything done on the spot.

## Rules

- Suggest-first, always. Never silently file.
- Never lose a capture: anything unresolvable goes to the Inbox section of tasks.md flagged for the next review.
- Reference items are NOT tasks — no time/energy tags in lists.md.
- Respect `communication_style` from config.

*Other GMTD skills: gmtd-now (what's next/plan my day/briefing), gmtd-done (completions), gmtd-review (weekly review), gmtd-setup (settings/help).*
