# Interaction Rules — how GMTD talks to the user

Every GMTD skill follows these rules. The user should mostly **tap, not type** — and never be asked to decide about something they can't see.

## Rule 1 — Interactive questions, always (in Claude)

In any Claude surface that has the interactive question tool (AskUserQuestion) — Cowork, Desktop, Claude Code — **every decision point uses it** with tappable options. Never ask an open "what do you think?" in plain chat when options exist. Decision points include:

| Skill | Decision points that MUST be option questions |
|---|---|
| gmtd-setup | Quick vs. full setup; every interview step with enumerable answers; connector choices; schedule opt-ins |
| gmtd-inbox | Ambiguous classifications in batch triage; trash confirmations; "do now vs. tag [🤖]" |
| gmtd-now | The time/energy prompt (2–5 min / 15 low / 15 med+ / 30+ deep / tell me) |
| gmtd-done | Multi-candidate fuzzy matches; tracking-sync confirmations (done / progress / wrong task) |
| gmtd-review | Every keep / move / drop decision; self-check proposals (apply / skip) |

## Rule 2 — The suggestion IS option 1

Suggest-first, made concrete: the recommended answer is always the **first option**, with the one-line reason in its description ("Next — it serves your Current #1"). The user confirms the default with one tap or picks something else.

## Rule 3 — Batch over serial

One question with multiple selections (or one compact triage table + one "fix anything?" question) beats five questions in a row. Ask serially only when a later question genuinely depends on an earlier answer.

## Rule 4 — Show before asking

Never ask the user to decide about a list they can't see. Render the bucket / candidates / proposal first, then ask. (This is gmtd-review's cardinal rule — it applies everywhere.)

## Rule 5 — Fallback for other harnesses

No interactive question tool (Codex and most other agents)? Ask the same question as a **numbered list** in chat ("Reply 1, 2, or 3 — or type your own answer"), one question per message, recommendation listed first and marked. Everything else in these rules still applies.

## Rule 6 — Output discipline

- gmtd-now / gmtd-done: a few lines. These run between real work.
- gmtd-inbox: one triage table, one confirmation.
- gmtd-review: complete lists (Rule 4), brisk pace, confirm per phase not per item.
- Respect `communication_style` from config everywhere (default: simple — no jargon, no file paths, no tool names).
