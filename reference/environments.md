# Environments — capabilities & fallbacks per harness

GMTD's primary home is **Claude Cowork**; it also runs in Claude Code, Codex, and any agent that can read files and (ideally) run Python. Detect what's available **once per session, silently** — never ask the user "which harness is this?"; try the capability or check the tool list.

## Capability matrix

| Capability | Cowork / Claude Desktop | Claude Code | Codex / other agents | Fallback when missing |
|---|---|---|---|---|
| Interactive option questions | ✅ AskUserQuestion | ✅ AskUserQuestion | usually ❌ | Numbered-list questions in chat (interaction.md Rule 5) |
| Live dashboard artifact | ✅ artifact/preview | ✅ preview | ❌ | Write `dashboard.html` next to tasks.md from the template; tell the user to open it in a browser (double-click) |
| Scheduled tasks | ✅ | ✅ | mostly ❌ | Say scheduling isn't available here; user runs briefing/review on demand (or their own cron) |
| MCP connectors (chat/email/calendar/tracker) | ✅ via claude.ai connectors + plugin .mcp.json | ✅ | varies | Skip connector-dependent steps silently — config marks them all optional |
| Python (for gmtd.py) | ✅ (sandboxed shell) | ✅ | usually ✅ | See "No Python" below |
| Voice transcription (transcribe.py + API key) | ✅ if key set | ✅ if key set | varies | Flag voice memos for manual transcription |

## No Python? (rare)

`gmtd.py` owns parsing, filtering, validation, and state. If Python genuinely isn't available:

1. Tell the user once, plainly: "I'll manage your tasks directly; a couple of automatic safety checks are off in this environment."
2. Parse and edit tasks.md directly, following schema.md **exactly** — the file format is the contract.
3. Skip `validate`/`stale`/`stats`; do the checks by careful reading during reviews instead.
4. NEVER touch state.json without the script — keep timestamps in a `<!-- state: key=value -->` comment block at the top of log.md instead, and say so in config.

## Environment etiquette

- **Cowork:** the user is likely non-technical. Default `communication_style: simple` hard: no file paths, no tool names, no JSON in user-facing output. Briefly say why before running the helper script the first time ("checking your list for anything overdue").
- **Claude Code:** technical users; paths and script output are fine if `communication_style: technical`.
- **Codex / other agents:** start from AGENTS.md; all five SKILL.md files are plain-markdown procedures that work as prompts. Follow interaction.md Rule 5 for questions.
- Everything degrades gracefully. **No capability is ever required** — a plain chat with file access runs the whole system.
