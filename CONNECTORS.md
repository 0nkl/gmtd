# Connectors

GMTD works fully with **zero connectors** — you can capture, clarify, and engage entirely in chat. Connectors add convenience, chosen during `/gmtd-setup` and stored in your `config.md`.

## How tool references work

GMTD skills use `~~category` as a placeholder for whatever tool you connect in that category (a convention borrowed from Anthropic's official plugins). `~~project tracker` might mean ClickUp, monday.com, Asana, or Linear — the skills don't care which. `.mcp.json` pre-configures common MCP servers, but any MCP server in a category works.

## Connector categories

| Category | Placeholder | What GMTD uses it for | Included servers | Other options |
|----------|-------------|----------------------|------------------|---------------|
| Chat | `~~chat` | Braindump capture channel, tracking channel, briefing delivery to your phone | Slack | Microsoft Teams, Discord |
| Email | `~~email` | Action-item discovery: deep sweeps and reviews scan for threads needing a reply or decision | Gmail / Microsoft 365 (connect via Claude connectors) | — |
| Calendar | `~~calendar` | Today's events in your briefing; 14-day look-ahead in reviews; time-blocking tasks onto your calendar | Google Calendar / Microsoft 365 (connect via Claude connectors) | — |
| Project tracker | `~~project tracker` | Pull-to-inbox sync: your open tracker tasks flow into GMTD's Inbox so one system answers "what's next?" | ClickUp, monday.com, Asana, Linear, Atlassian | Shortcut, Basecamp, Wrike |
| Transcription | — | Voice memo captures → text (`scripts/transcribe.py`, needs an API key) | OpenAI Whisper API | ElevenLabs Scribe |

## What happens without a connector

- No chat → capture in conversation or via an inbox file; briefings appear in chat.
- No email/calendar → those steps are silently skipped in briefings and reviews.
- No tracker → GMTD is simply your only task system (many users prefer this).
- No transcription key → voice memos are flagged for manual transcription.
