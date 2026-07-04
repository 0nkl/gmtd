#!/usr/bin/env python3
"""gmtd.py — deterministic helper CLI for GMTD (Get More Things Done).

Owns everything that must be exact: parsing tasks.md, filtering candidates,
validating invariants, stale detection, state timestamps, stats, and log appends.
The AI owns judgment; this script owns arithmetic.

Stdlib only. Python 3.8+. Path-agnostic (pathlib).

Usage:
  gmtd.py --dir <gmtd folder> <command> [options]

Commands:
  parse                      Dump all tasks as JSON
  query [--time N] [--energy low|medium|high] [--bucket B] [--priority P]
                             Filtered candidate list (JSON)
  validate                   Invariant report (JSON; exit 1 if violations)
  stale                      Items past their bucket's stale threshold (JSON)
  state get <key> | set <key> <value> | all
                             Read/write state.json (ISO 8601 values)
  epoch <iso-datetime>       Convert ISO datetime to unix epoch (for Slack 'oldest')
  stats [--days N]           Done counts + time logged per project (default 7 days)
  log --op OP --subject S [--bullet B ...] [--file PATH]
                             Append a journal entry (default: <dir>/log.md)
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ---------------------------------------------------------------- constants

BUCKETS = {
    "resume": ["resume here"],
    "inbox": ["inbox"],
    "focus": ["focus"],
    "next": ["next"],
    "scheduled": ["scheduled"],
    "later": ["later"],
    "waiting": ["waiting on", "waiting"],
    "projects": ["projects"],
    "someday": ["someday"],
    "done": ["done (recent)", "done"],
}

TIME_ORDER = ["2min", "5min", "15min", "30min", "60min+"]
ENERGY_ORDER = ["low", "medium", "high"]
PRIORITY_MAP = {"\U0001F534": "critical", "\U0001F7E1": "important", "\U0001F7E2": "whenever"}
PRIORITY_RANK = {"critical": 0, "important": 1, "whenever": 2, None: 3}

TAG_RE = re.compile(r"\[(time|energy|priority|added|defer|since|follow-up|src):([^\]\s][^\]]*)\]")
TASK_RE = re.compile(r"^(\s*)- \[([ x~])\]\s*(.*)$")
HEADER_RE = re.compile(r"^(#{2,3})\s+(.*)$")
PROJECT_LINK_RE = re.compile(r"\(←\s*([^)]+)\)")
TIMELOG_RE = re.compile(r"^\s*↳\s*\[(\d{4}-\d{2}-\d{2})\]\s*~?(\d+)\s*(min|h|hr|hrs|hours?)", re.IGNORECASE)
NEXTSTEP_RE = re.compile(r"^\s*→\s*next step:\s*(.*)$", re.IGNORECASE)

DEFAULT_THRESHOLDS = {"focus_next": 10, "later": 30, "someday": 90}


def norm_header(text):
    """Strip emoji/decoration from a section header and lowercase it."""
    cleaned = re.sub(r"[^\w\s()\-/]", "", text, flags=re.UNICODE).strip().lower()
    return re.sub(r"\s+", " ", cleaned)


def bucket_for_header(text):
    n = norm_header(text)
    for bucket, names in BUCKETS.items():
        for name in names:
            if n == name or n.startswith(name):
                return bucket
    return None


# ---------------------------------------------------------------- parsing

def parse_tasks(path):
    """Parse tasks.md into a dict: buckets -> task list, projects, meta."""
    text = Path(path).read_text(encoding="utf-8")
    lines = text.splitlines()

    tasks = []
    projects = {}
    resume_here = []
    current_bucket = None
    current_project = None  # inside Projects section (### headers)
    current_task = None

    for idx, line in enumerate(lines):
        h = HEADER_RE.match(line)
        if h:
            level, title = h.group(1), h.group(2).strip()
            if level == "##":
                b = bucket_for_header(title)
                if b:
                    current_bucket = b
                    current_project = None
                    current_task = None
                continue
            if level == "###" and current_bucket == "projects":
                name = re.sub(r"\s*[—–-]\s*(SKIPPED|DONE).*$", "", title).strip()
                current_project = name
                projects[name] = {"name": name, "title": title, "line": idx + 1,
                                  "goal": None, "tasks": [], "has_next_marker": False}
                current_task = None
                continue

        if current_bucket == "resume":
            if line.strip() and not line.strip().startswith(("---", "*")):
                resume_here.append(line.strip())
            continue

        if current_project and line.strip().lower().startswith("goal:"):
            projects[current_project]["goal"] = line.strip()[5:].strip()
            continue

        # A project's [NEXT] marker may sit on a non-checkbox line: "- [NEXT] Task (→ in Next above)"
        if current_project and re.match(r"^\s*- \[NEXT\]", line):
            projects[current_project]["has_next_marker"] = True

        m = TASK_RE.match(line)
        if m and current_bucket:
            indent, status_ch, body = m.group(1), m.group(2), m.group(3)
            tags = {k: v.strip() for k, v in TAG_RE.findall(body)}
            desc = TAG_RE.sub("", body)
            has_next_marker = "[NEXT]" in desc
            ai_delegable = "[\U0001F916]" in desc or "[🤖]" in body
            desc = desc.replace("[NEXT]", "").replace("[🤖]", "")
            plink = PROJECT_LINK_RE.search(desc)
            project = plink.group(1).strip() if plink else current_project
            desc = PROJECT_LINK_RE.sub("", desc).strip(" ——-").strip()

            prio = None
            for emoji, name in PRIORITY_MAP.items():
                if tags.get("priority") == emoji or emoji in body:
                    prio = name
                    break

            task = {
                "description": desc,
                "bucket": current_bucket,
                "status": {" ": "open", "x": "done", "~": "dropped"}[status_ch],
                "line": idx + 1,
                "time": tags.get("time"),
                "energy": tags.get("energy"),
                "priority": prio,
                "added": tags.get("added"),
                "defer": tags.get("defer"),
                "since": tags.get("since"),
                "follow_up": tags.get("follow-up"),
                "src": tags.get("src"),
                "project": project,
                "is_project_next": has_next_marker,
                "ai_delegable": ai_delegable,
                "next_step": None,
                "time_logs": [],
            }
            tasks.append(task)
            current_task = task
            if current_project:
                projects[current_project]["tasks"].append(task)
                if has_next_marker:
                    projects[current_project]["has_next_marker"] = True
            continue

        if current_task:
            ns = NEXTSTEP_RE.match(line)
            if ns:
                current_task["next_step"] = ns.group(1).strip()
                continue
            tl = TIMELOG_RE.match(line)
            if tl:
                minutes = int(tl.group(2))
                if tl.group(3).lower().startswith("h"):
                    minutes *= 60
                current_task["time_logs"].append({"date": tl.group(1), "minutes": minutes})
                continue
            plink = PROJECT_LINK_RE.search(line)
            if plink and line.strip().startswith("("):
                current_task["project"] = plink.group(1).strip()
                continue

    return {"tasks": tasks, "projects": list(projects.values()), "resume_here": resume_here}


# ---------------------------------------------------------------- query

def time_fits(task_time, available_min):
    if task_time is None:
        return True  # untagged: let the AI judge, but flag via validate
    limits = {"2min": 2, "5min": 5, "15min": 15, "30min": 30, "60min+": 60}
    need = limits.get(task_time, 999)
    return need <= available_min


def energy_fits(task_energy, user_energy):
    if task_energy is None or user_energy is None:
        return True
    order = {e: i for i, e in enumerate(ENERGY_ORDER)}
    return order.get(task_energy, 0) <= order.get(user_energy, 2)


def cmd_query(data, args, today):
    out = []
    buckets = [args.bucket] if args.bucket else ["focus", "next"]
    for t in data["tasks"]:
        if t["status"] != "open":
            continue
        b = t["bucket"]
        # expired defers count as next
        if b == "scheduled" and t.get("defer") and t["defer"] <= today:
            b = "next"
        if b not in buckets:
            continue
        if args.time and not time_fits(t["time"], args.time):
            continue
        if args.energy and not energy_fits(t["energy"], args.energy):
            continue
        if args.priority and t["priority"] != args.priority:
            continue
        out.append(t)
    out.sort(key=lambda t: (0 if t["bucket"] == "focus" else 1,
                            PRIORITY_RANK.get(t["priority"], 3),
                            t["added"] or "9999"))
    return out


# ---------------------------------------------------------------- validate

def cmd_validate(data, config, today):
    v = []
    focus = [t for t in data["tasks"] if t["bucket"] == "focus" and t["status"] == "open"]
    focus_max = int(config.get("focus_max", 5))
    if len(focus) > focus_max:
        v.append({"rule": "focus_max", "detail": f"Focus has {len(focus)} items (max {focus_max})",
                  "items": [t["description"] for t in focus]})
    for t in focus:
        if t["priority"] not in ("critical", None):
            v.append({"rule": "focus_priority", "detail": f"Focus item not critical: {t['description']}"})

    for p in data["projects"]:
        if any(t["status"] == "open" for t in p["tasks"]) and not p["has_next_marker"]:
            v.append({"rule": "project_next", "detail": f"Project '{p['name']}' has no [NEXT] task"})

    for t in data["tasks"]:
        if t["status"] != "open" or t["bucket"] in ("someday", "done", "inbox", "waiting"):
            continue
        if t["time"] in ("30min", "60min+") and not t["next_step"]:
            v.append({"rule": "next_step_missing", "detail": f"Big task without next step: {t['description']}", "line": t["line"]})
        # Focus items are often pointers to Next entries; only Next/Later need full metadata.
        if t["bucket"] in ("next", "later"):
            for field in ("time", "energy", "priority", "added"):
                if not t.get(field):
                    v.append({"rule": "metadata_missing", "detail": f"Missing [{field}:] on: {t['description']}", "line": t["line"]})
        if t["bucket"] == "scheduled" and t.get("defer") and t["defer"] < today:
            v.append({"rule": "defer_expired", "detail": f"Defer date passed, move to Next: {t['description']}"})
        if t["bucket"] == "waiting" and t.get("follow_up") and t["follow_up"] < today:
            v.append({"rule": "waiting_overdue", "detail": f"Follow-up overdue: {t['description']}"})
    return v


# ---------------------------------------------------------------- stale

def cmd_stale(data, thresholds, today_dt):
    out = []
    for t in data["tasks"]:
        if t["status"] != "open" or not t.get("added"):
            continue
        try:
            added = datetime.strptime(t["added"], "%Y-%m-%d")
        except ValueError:
            continue
        age = (today_dt - added).days
        limit = None
        if t["bucket"] in ("focus", "next"):
            if not t["time_logs"]:
                limit = thresholds["focus_next"]
        elif t["bucket"] == "later":
            limit = thresholds["later"]
        elif t["bucket"] == "someday":
            limit = thresholds["someday"]
        if limit and age > limit:
            out.append({"description": t["description"], "bucket": t["bucket"],
                        "age_days": age, "threshold": limit, "line": t["line"]})
    out.sort(key=lambda x: -x["age_days"])
    return out


# ---------------------------------------------------------------- stats

def cmd_stats(data, days, today_dt):
    cutoff = (today_dt - timedelta(days=days)).strftime("%Y-%m-%d")
    done = [t for t in data["tasks"] if t["status"] == "done"]
    done_recent = []
    for t in done:
        m = re.search(r"\((\d{4}-\d{2}-\d{2})\)", t["description"]) or (
            re.search(r"✓\s*\((\d{4}-\d{2}-\d{2})\)", t["description"]))
        d = m.group(1) if m else None
        if d and d >= cutoff:
            done_recent.append({"description": t["description"], "date": d, "project": t["project"]})
    time_per_project = {}
    for t in data["tasks"]:
        for tl in t["time_logs"]:
            if tl["date"] >= cutoff:
                key = t["project"] or "(no project)"
                time_per_project[key] = time_per_project.get(key, 0) + tl["minutes"]
    open_counts = {}
    for t in data["tasks"]:
        if t["status"] == "open":
            open_counts[t["bucket"]] = open_counts.get(t["bucket"], 0) + 1
    return {"window_days": days, "done_count": len(done_recent), "done": done_recent,
            "minutes_per_project": time_per_project, "open_by_bucket": open_counts}


# ---------------------------------------------------------------- state / log

def state_path(d):
    return d / "state.json"


def load_state(d):
    p = state_path(d)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def cmd_state(d, args):
    st = load_state(d)
    if args.action == "all":
        return st
    if args.action == "get":
        return {args.key: st.get(args.key)}
    if args.action == "set":
        st[args.key] = args.value
        st["_updated"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        state_path(d).write_text(json.dumps(st, indent=2), encoding="utf-8")
        return {args.key: args.value, "written": True}


def cmd_log(args, default_dir):
    path = Path(args.file) if args.file else default_dir / "log.md"
    date = datetime.now().strftime("%Y-%m-%d")
    entry = [f"\n## [{date}] {args.op} | {args.subject}\n"]
    for b in (args.bullet or []):
        entry.append(f"- {b}\n")
    with open(path, "a", encoding="utf-8") as f:
        f.writelines(entry)
    return {"appended": str(path), "op": args.op, "subject": args.subject}


# ---------------------------------------------------------------- config (light)

def load_config(d):
    """Light parse of config.md: 'key: value' bullet lines. Enough for thresholds/focus_max."""
    cfg = {}
    p = d / "config.md"
    if not p.exists():
        return cfg
    for line in p.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*-\s*([a-z_]+):\s*(.+?)(\s*#.*)?$", line)
        if m:
            cfg[m.group(1)] = m.group(2).strip()
    return cfg


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="GMTD deterministic helper")
    ap.add_argument("--dir", required=True, help="User GMTD folder (contains tasks.md, state.json…)")
    ap.add_argument("--tasks", help="Override tasks.md path")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("parse")
    q = sub.add_parser("query")
    q.add_argument("--time", type=int, help="Available minutes")
    q.add_argument("--energy", choices=ENERGY_ORDER)
    q.add_argument("--bucket")
    q.add_argument("--priority", choices=["critical", "important", "whenever"])
    sub.add_parser("validate")
    sub.add_parser("stale")
    st = sub.add_parser("state")
    st.add_argument("action", choices=["get", "set", "all"])
    st.add_argument("key", nargs="?")
    st.add_argument("value", nargs="?")
    ep = sub.add_parser("epoch")
    ep.add_argument("datetime", help="ISO datetime, e.g. 2026-07-04T14:16:00-05:00")
    s = sub.add_parser("stats")
    s.add_argument("--days", type=int, default=7)
    lg = sub.add_parser("log")
    lg.add_argument("--op", required=True,
                    choices=["setup", "inbox", "done", "brief", "review", "system-check", "edit"])
    lg.add_argument("--subject", required=True)
    lg.add_argument("--bullet", action="append")
    lg.add_argument("--file", help="Log file (default <dir>/log.md; set for external journals)")

    args = ap.parse_args()
    d = Path(args.dir)
    today_dt = datetime.now()
    today = today_dt.strftime("%Y-%m-%d")

    if args.cmd == "state":
        if args.action in ("get", "set") and not args.key:
            ap.error("state get/set requires a key")
        if args.action == "set" and args.value is None:
            ap.error("state set requires a value")
        print(json.dumps(cmd_state(d, args), indent=2))
        return

    if args.cmd == "epoch":
        dt = datetime.fromisoformat(args.datetime)
        if dt.tzinfo is None:
            dt = dt.astimezone()
        print(int(dt.timestamp()))
        return

    if args.cmd == "log":
        print(json.dumps(cmd_log(args, d), indent=2))
        return

    tasks_file = Path(args.tasks) if args.tasks else d / "tasks.md"
    if not tasks_file.exists():
        print(json.dumps({"error": f"tasks file not found: {tasks_file}"}))
        sys.exit(2)
    data = parse_tasks(tasks_file)
    config = load_config(d)
    thresholds = dict(DEFAULT_THRESHOLDS)
    for k in thresholds:
        if k in config:
            try:
                thresholds[k] = int(config[k])
            except ValueError:
                pass

    if args.cmd == "parse":
        print(json.dumps(data, indent=2, ensure_ascii=False))
    elif args.cmd == "query":
        print(json.dumps(cmd_query(data, args, today), indent=2, ensure_ascii=False))
    elif args.cmd == "validate":
        v = cmd_validate(data, config, today)
        print(json.dumps({"violations": v, "count": len(v)}, indent=2, ensure_ascii=False))
        sys.exit(1 if v else 0)
    elif args.cmd == "stale":
        print(json.dumps(cmd_stale(data, thresholds, today_dt), indent=2, ensure_ascii=False))
    elif args.cmd == "stats":
        print(json.dumps(cmd_stats(data, args.days, today_dt), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
