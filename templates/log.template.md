# GMTD Log — {{NAME}}

Append-only activity journal. Every GMTD operation records what happened here.
Format: `## [YYYY-MM-DD] <op> | <subject>` + 2–4 bullets. Ops: setup, inbox, done, brief, review, system-check, edit.
Greppable: `grep "^## \[" log.md | tail -10`
