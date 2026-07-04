---
name: gmtd-done
description: >
  Mark work complete and close sessions cleanly. Trigger on: "I finished X", "mark X
  done", "X is done", "I did X", "wrap up", "session done", "close out", "I'm done for
  today", "end session", "sync my tracking channel", "log what I did", "I worked on X
  for an hour".
---

# GMTD Done — Completion · Session Wrap · Tracking

Read first: user `config.md`, `${CLAUDE_PLUGIN_ROOT}/reference/schema.md`. Three entry modes:

## Mode A — "I finished X" (anytime, no ceremony)

1. Fuzzy-match X against tasks.md (`gmtd.py parse`) — Focus, Next, Projects, Later. Multiple candidates → quick pick list. No match → "Not in your list — add it as done anyway?" (capture-then-complete; it still counts).
2. Mark `- [x] … ✓ (YYYY-MM-DD)`, move to Done (recent), remove from Focus if present.
3. **Keep the project moving:** if it was a project's [NEXT], promote the project's next sub-task — move it to Next with full metadata (ask time/energy if unknown) and the [NEXT] marker. If the project has no remaining tasks: "Is [project] complete, or what's the next action?"
4. If `time_logging: on`, append a `↳` time log (infer duration from what the user said; state your inference, e.g. "~30 min ending now — right?").
5. No confirmation needed to mark done — the user said it's done.

## Mode B — "Wrap up" (session close, 2–3 minutes max)

1. Ask once if not obvious: "What got done this session?" Accept vague answers; fuzzy-match.
2. Process completions as Mode A. Also check the tracking channel (if configured) for unsynced posts and process them inline.
3. **Write the Resume Here block** (always — overwrite the section):
   ```
   **Last session (YYYY-MM-DD):** [1-line summary]
   **Next:** [single most important next action — specific, with time/energy]
   [⚠️ only if something is genuinely time-sensitive]
   ```
4. Log via `gmtd.py log --op done` ONLY if the session produced meaningful progress (decisions, deliverables, completed priorities) — skip for pure triage. If `wiki_integration: on`, use the user's wiki log conventions.
5. Handoff in one sentence. No walls of text.

## Mode C — "Sync tracking" (channel users)

1. Read the `~~chat` tracking channel since `gmtd.py state get tracking_synced` (use `gmtd.py epoch` for the cutoff). Nothing new → say so, done.
2. Per message: match task (fuzzy), infer time (explicit > "worked for X" > default ~30 min ending at message timestamp — always show the inference), status done vs. progress.
3. Confirm each (quick options: done / progress / wrong task), then write: done → Mode A steps; progress → `↳` time log, task stays put.
4. `state set tracking_synced` to the LAST message's timestamp (never "now"). Report counts in one line.

## Rules

- Completions must never be lost — when in doubt, record it.
- Every project must keep a live [NEXT] after processing (run `gmtd.py validate`; fix or flag before closing).
- Fast. This skill runs between real work; keep responses to a few lines.

*Other GMTD skills: gmtd-inbox (captures→tasks), gmtd-now (what's next/briefing), gmtd-review (reviews), gmtd-setup (settings/help).*
