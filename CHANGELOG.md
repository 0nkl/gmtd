# Changelog

All notable changes to GMTD. Format loosely follows [Keep a Changelog](https://keepachangelog.com/); versions follow semver.

## [0.2.0] — 2026-07-06

Cowork-first release: easier onboarding, optional productivity frameworks on top of GTD, due dates, and a real user manual.

### Added
- **GUIDE.md** — plain-language user manual: how the system works, the five habits, cheat sheet, troubleshooting, FAQ.
- **Quick Start setup** (~3 minutes) alongside the full interview — three questions and a mind sweep; everything else defaults, changeable anytime.
- **Due dates** — `[due:YYYY-MM-DD]` for hard deadlines (distinct from `defer:`). Overdue/due-today items outrank everything in "what's next", show first in the briefing, and are flagged by `validate`.
- **Frameworks layer** ([reference/frameworks.md](reference/frameworks.md)) — opt-in lenses on the GTD backbone: daily shapes (**Big 3**, **1-3-5**, **Eat the Frog**) for briefings and the new **"plan my day"** mode; **Eisenhower** urgent-vs-important triage in reviews; **focus sessions** in gmtd-now. New config section `## Planning style` (config_version: 2; old configs keep working).
- **Dashboard template** ([templates/dashboard.template.html](templates/dashboard.template.html)) — polished, self-contained, with time/energy filter chips, due/overdue strip, and skill-launcher buttons (auto-hidden outside Claude). Skills inject data instead of improvising HTML.
- **Backups** — `gmtd.py backup` snapshots tasks.md (keeps last 10); all skills back up before batch writes.
- **reference/interaction.md** — interactive-question rules: in Claude/Cowork every decision is a tappable option question; numbered-list fallback elsewhere.
- **reference/environments.md** — capability matrix and exact fallbacks for Cowork, Claude Code, Codex, and other agents (including a defined no-Python mode).
- **examples/** — a fictional freelancer's fully populated system; doubles as the smoke-test fixture.
- **Daily shutdown** — "I'm done for today" closes the day: honest tally, tomorrow teed up per your planning style.
- `gmtd.py --version`; done-count de-duplication in `stats`.

### Fixed
- `gmtd.py` output is now forced to UTF-8 — emoji-heavy JSON no longer crashes on Windows consoles (cp1252).
- `parse` no longer drops the Resume Here block: `**bold**` content lines were being skipped along with `*italic*` template comments, so `resume_here` always came back empty.

### Changed
- gmtd-now grew from 3 to 5 modes (what's next · briefing · plan my day · focus session · dashboard); triggers updated across all skills.
- AGENTS.md slimmed to an entry point that defers to the reference docs.
- README tightened; points to GUIDE.md and examples/.

## [0.1.0] — 2026-07-04

Initial release: 5 skills (setup, inbox, now, done, review), markdown data layer, deterministic `gmtd.py` helper (parse/query/validate/stale/state/stats/log), connector categories with `~~category` placeholders, voice transcription script, templates, AGENTS.md portability shim.
