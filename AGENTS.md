# GMTD — Agent Entry Point (Codex and other non-Claude harnesses)

This plugin was built for Claude (Cowork / Claude Code) but its core is portable: markdown skills, markdown data, one stdlib-only Python script. If you are an AI agent in another harness, operate GMTD like this:

## What to read

1. `reference/schema.md` — file formats, buckets, task metadata, invariants. The contract.
2. `reference/gtd-primer.md` — the methodology you're running.
3. `reference/matching-rules.md` — how to pick what the user should work on.
4. The user's `config.md` (in their GMTD folder) — their settings. NEVER act without reading it.
5. `skills/*/SKILL.md` — the five workflows (setup, inbox, now, done, review). Follow them as procedures.

## What to run

`scripts/gmtd.py` handles everything deterministic — parsing, filtering, validation, timestamps:

```
python scripts/gmtd.py --dir <user gmtd folder> parse | query | validate | stale | state | stats | log
```

Always use it instead of hand-parsing tasks.md or hand-editing state.json.

## Capability fallbacks (Claude-specific features)

- **Interactive option questions** → ask numbered questions in plain chat.
- **Dashboard artifact** → generate a static `dashboard.html` next to the user's tasks.md instead.
- **Scheduled tasks** → tell the user this harness can't schedule; suggest they run the briefing/review manually or via their own cron.
- **Slack/email/calendar/tracker MCPs** → if this harness lacks the connector, skip those steps silently (config marks them optional).

## Hard rules

- Suggest-first: propose classifications/priorities with reasoning; the user confirms.
- Never write to `raw` user captures; never hand-edit `state.json`; append (never rewrite) `log.md`.
- Respect `config.md → communication_style` (default: simple, non-technical language).
