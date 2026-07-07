# GMTD — Agent Entry Point (Codex and other non-Claude harnesses)

This plugin was built for Claude (Cowork / Claude Code) but its core is portable: markdown skills, markdown data, one stdlib-only Python script. If you are an AI agent in another harness, operate GMTD like this:

## Reading order

1. `reference/schema.md` — file formats, buckets, task metadata, invariants. The contract.
2. `reference/environments.md` — what to do when a Claude-specific capability (interactive questions, dashboard artifact, scheduled tasks, connectors) is missing here. Read this before running any skill.
3. `reference/interaction.md` — how to ask questions and how much to say (Rule 5 is your question format).
4. `reference/gtd-primer.md` — the methodology you're running. `reference/frameworks.md` — optional planning styles on top.
5. `reference/matching-rules.md` — how to pick what the user should work on.
6. The user's `config.md` (in their GMTD folder) — their settings. NEVER act without reading it.
7. `skills/*/SKILL.md` — the five workflows (setup, inbox, now, done, review). Follow them as procedures.

## What to run

`scripts/gmtd.py` handles everything deterministic — parsing, filtering, validation, timestamps, backups:

```
python scripts/gmtd.py --dir <user gmtd folder> parse | query | validate | stale | state | stats | log | backup
```

Always use it instead of hand-parsing tasks.md or hand-editing state.json. Run `backup` before any batch write to tasks.md. (No Python at all? environments.md defines the degraded mode.)

## Hard rules

- Suggest-first: propose classifications/priorities with reasoning; the user confirms.
- Never rewrite raw user captures; never hand-edit `state.json`; append (never rewrite) `log.md`.
- Respect `config.md → communication_style` (default: simple, non-technical language).
