#!/usr/bin/env python3
"""protodoc CLI — scaffold, serve and annotate a design that has no code yet.

    pd.py init <slug> [--root DIR] [--addition]   create protodoc/<slug>/
    pd.py serve <dir> [--port N]                  review site on 127.0.0.1 (run in background)
    pd.py watch <dir> [--timeout S]               block until Nudge, print the batch, snapshot
    pd.py show <dir> [--json]                     fold the event log into annotation state
    pd.py reply <dir> --id N --state S [--text T] answer one annotation
    pd.py ask <dir> "<what you need>"             tell the page you are blocked on the user
    pd.py phase <dir> <user-doc|tech-doc|export>  advance the phase
    pd.py snapshot <dir>                          freeze current docs as the diff baseline

Annotations live in .state/events.jsonl as an append-only log; every command that
reads them folds the log rather than mutating it.
"""
import argparse
import json
import os
import re
import shutil
import socket
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.dont_write_bytecode = True  # the skill dir is not ours to litter in
sys.path.insert(0, str(Path(__file__).resolve().parent))
from render import render_page  # noqa: E402

ASSETS = Path(__file__).resolve().parent.parent / "assets"
SECTIONS = ("user-doc", "tech-doc")
STATES = ("applied", "applied-differently", "pushed-back", "needs-you")
VERBS = ("comment", "suggest", "doubt")
EVENTS = ("annotate", "reply", "followup", "edit", "delete", "undelete",
          "reopen", "resolve", "retract", "unretract", "nudge")
MAX_FIELD = 20000
WRITE_LOCK = threading.Lock()


def clean_event(payload: dict) -> dict | None:
    """Whitelist what the page may append. Returns None if it may not."""
    kind = payload.get("type")
    if kind not in EVENTS:
        return None

    def text(key: str) -> str:
        value = payload.get(key, "")
        return value[:MAX_FIELD] if isinstance(value, str) else ""

    if kind == "nudge":
        return {"type": "nudge"}
    if kind == "annotate":
        verb = payload.get("verb")
        return {
            "type": "annotate",
            "verb": verb if verb in VERBS else "comment",
            "page": text("page"), "heading": text("heading"),
            "quote": text("quote"), "sig": text("sig"), "text": text("text"),
        }

    if not isinstance(payload.get("id"), int):
        return None
    if kind == "reply":
        state = payload.get("state")
        if state not in STATES:
            return None
        return {"type": "reply", "id": payload["id"], "state": state, "text": text("text")}
    if kind in ("edit", "followup"):
        return {"type": kind, "id": payload["id"], "text": text("text")}
    if kind in ("retract", "unretract"):
        if not isinstance(payload.get("n"), int):
            return None
        return {"type": kind, "id": payload["id"], "n": payload["n"]}
    return {"type": kind, "id": payload["id"]}


# ── state ───────────────────────────────────────────────────────────────────

def paths(directory: str) -> dict[str, Path]:
    root = Path(directory).resolve()
    state = root / ".state"
    return {
        "root": root,
        "state": state,
        "events": state / "events.jsonl",
        "cursor": state / ".events.cursor",
        "meta": state / "meta.json",
        "server": state / "server.json",
        "snapshot": state / "snapshot",
        "agent": state / "agent.json",
    }


def set_state(p: dict[str, Path], state: str, note: str = "", pid: int | None = None) -> None:
    """Publish what the agent is doing: waiting for notes, working, or blocked on the user."""
    try:
        keep = json.loads(p["agent"].read_text()).get("pid", 0)
    except (OSError, json.JSONDecodeError):
        keep = 0
    p["agent"].parent.mkdir(parents=True, exist_ok=True)
    p["agent"].write_text(json.dumps({
        "state": state, "note": note,
        "pid": keep if pid is None else pid,
        "at": time.strftime("%H:%M:%S"),
    }))


def agent_state(p: dict[str, Path]) -> dict:
    """Is anyone listening, and if so what are they doing?

    A blocked watcher heartbeats, so a stale idle file means nothing is waiting
    for a nudge. Working and waiting have no heartbeat — nobody is blocked then —
    so they stand on their own until they go stale.
    """
    try:
        published = json.loads(p["agent"].read_text())
        age = time.time() - p["agent"].stat().st_mtime
    except (OSError, json.JSONDecodeError):
        return {"listening": False, "state": "idle", "note": ""}
    state = published.get("state", "idle")
    listening = age < 8 if state == "idle" else age < 900
    return {
        "listening": listening,
        "state": state if listening else "idle",
        "note": published.get("note", ""),
    }


def read_meta(p: dict[str, Path]) -> dict:
    try:
        return json.loads(p["meta"].read_text())
    except (OSError, json.JSONDecodeError):
        return {"slug": p["root"].name, "phase": "user-doc", "mode": "greenfield"}


def write_meta(p: dict[str, Path], meta: dict) -> None:
    p["meta"].write_text(json.dumps(meta, indent=2) + "\n")


def append_event(p: dict[str, Path], record: dict) -> dict:
    record = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), **record}
    with WRITE_LOCK:
        if record.get("type") == "annotate" and not record.get("id"):
            record["id"] = max((a["id"] for a in fold(p).values()), default=0) + 1
        p["events"].parent.mkdir(parents=True, exist_ok=True)
        with p["events"].open("a") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def fold(p: dict[str, Path]) -> dict[int, dict]:
    """Replay the event log into current annotation state, keyed by id."""
    annotations: dict[int, dict] = {}
    try:
        lines = p["events"].read_text().splitlines()
    except OSError:
        return annotations
    for line in lines:
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        kind, ident = event.get("type"), event.get("id")
        if kind == "annotate" and ident:
            annotations[ident] = {
                "id": ident,
                "verb": event.get("verb", "comment"),
                "page": event.get("page", ""),
                "heading": event.get("heading", ""),
                "quote": event.get("quote", ""),
                "sig": event.get("sig", ""),
                "text": event.get("text", ""),
                "ts": event.get("ts", ""),
                "turns": [],
                "status": "open",
            }
        elif kind == "reply" and ident in annotations:
            turns = annotations[ident]["turns"]
            turns.append({
                "n": len(turns), "who": "agent", "state": event.get("state", "applied"),
                "text": event.get("text", ""), "ts": event.get("ts", ""),
            })
            annotations[ident]["status"] = "resolved"     # answering closes it; reopen brings it back
        elif kind == "followup" and ident in annotations:
            turns = annotations[ident]["turns"]
            turns.append({"n": len(turns), "who": "you",
                          "text": event.get("text", ""), "ts": event.get("ts", "")})
            annotations[ident]["status"] = "open"         # saying more reopens the question
        elif kind in ("retract", "unretract") and ident in annotations:
            for turn in annotations[ident]["turns"]:
                if turn["n"] == event.get("n"):
                    turn["gone"] = kind == "retract"
            # whoever spoke last owns the state again
            spoken = [t for t in annotations[ident]["turns"] if not t.get("gone")]
            annotations[ident]["status"] = (
                "resolved" if spoken and spoken[-1]["who"] == "agent" else "open")
        elif kind == "reopen" and ident in annotations:
            annotations[ident]["status"] = "open"
        elif kind == "resolve" and ident in annotations:
            annotations[ident]["status"] = "resolved"
        elif kind == "edit" and ident in annotations:
            annotations[ident]["text"] = event.get("text", "")
        elif kind in ("delete", "undelete") and ident in annotations:
            # Struck out rather than dropped, so undo restores the replies too.
            annotations[ident]["deleted"] = kind == "delete"
    for a in annotations.values():
        a["turns"] = [t for t in a["turns"] if not t.get("gone")]
    return {i: a for i, a in annotations.items() if not a.get("deleted")}


# ── docs ────────────────────────────────────────────────────────────────────

def page_title(path: Path) -> str:
    try:
        for line in path.read_text().splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    except OSError:
        pass
    return re.sub(r"^\d+[-_]", "", path.stem).replace("-", " ").capitalize()


def list_pages(p: dict[str, Path]) -> list[dict]:
    pages = []
    for section in SECTIONS:
        for path in sorted((p["root"] / section).glob("*.md")):
            pages.append({"section": section, "path": f"{section}/{path.name}", "title": page_title(path)})
    return pages


def snapshot(p: dict[str, Path]) -> None:
    dest = p["snapshot"]
    if dest.exists():
        shutil.rmtree(dest)
    for section in SECTIONS:
        source = p["root"] / section
        if source.exists():
            shutil.copytree(source, dest / section)
    dest.mkdir(parents=True, exist_ok=True)


# ── commands ────────────────────────────────────────────────────────────────

STATUS_TEMPLATE = """# {slug} — protodoc status

- **phase**: user-doc
- **mode**: {mode}
- **gate 1 (product locked)**: not armed
- **gate 2 (architecture locked)**: not armed

The docs here describe a product that does not exist yet. `BUILD.md` appears
once both gates are locked; until then nothing in this folder is final.
"""

DECISIONS_TEMPLATE = """# Decisions

Distilled from answered annotations each round. Newest last.

| # | Decision | Rigidity | Why |
|---|---|---|---|
"""


def cmd_init(args) -> None:
    slug = re.sub(r"[^a-z0-9-]+", "-", args.slug.lower()).strip("-")
    if not slug:
        sys.exit("slug must contain letters or digits")
    root = Path(args.root).resolve() / "protodoc" / slug
    if root.exists():
        sys.exit(f"{root} already exists — resume it instead of re-initialising")
    p = paths(str(root))
    for section in SECTIONS:
        (root / section).mkdir(parents=True)
    p["state"].mkdir(parents=True)
    p["events"].touch()
    mode = "addition" if args.addition else "greenfield"
    (root / "STATUS.md").write_text(STATUS_TEMPLATE.format(slug=slug, mode=mode))
    (root / "DECISIONS.md").write_text(DECISIONS_TEMPLATE)
    write_meta(p, {"slug": slug, "phase": "user-doc", "mode": mode})
    exclude = Path(args.root).resolve() / ".git" / "info" / "exclude"
    if exclude.parent.exists():
        entry = f"protodoc/{slug}/.state/"
        current = exclude.read_text() if exclude.exists() else ""
        if entry not in current:
            exclude.write_text(current + ("" if current.endswith("\n") or not current else "\n") + entry + "\n")
    print(root)


def cmd_phase(args) -> None:
    p = paths(args.dir)
    meta = read_meta(p)
    meta["phase"] = args.name
    write_meta(p, meta)
    status = p["root"] / "STATUS.md"
    if status.exists():
        status.write_text(re.sub(r"(?m)^- \*\*phase\*\*: .*$", f"- **phase**: {args.name}", status.read_text()))
    print(f"phase: {args.name}")


def cmd_ask(args) -> None:
    p = paths(args.dir)
    set_state(p, "waiting", args.text)
    print(f"page now says you need an answer: {args.text}")


def cmd_snapshot(args) -> None:
    snapshot(paths(args.dir))
    print("baseline frozen")


def summarise(p: dict[str, Path]) -> str:
    meta = read_meta(p)
    annotations = fold(p)
    counts = {"open": 0, "resolved": 0}
    for a in annotations.values():
        counts[a["status"]] += 1
    out = [f"phase: {meta['phase']}  mode: {meta['mode']}  |  "
           f"open: {counts['open']}  resolved: {counts['resolved']}", ""]
    outstanding = [a for a in annotations.values() if a["status"] == "open"]
    if not outstanding:
        out.append("nothing outstanding")
        return "\n".join(out)
    for a in sorted(outstanding, key=lambda x: x["id"]):
        where = "the whole project" if a["page"] == "*" else f"{a['page']} § {a['heading'] or '-'}"
        out.append(f"#{a['id']} {a['verb']:<8} {where}   [{a['status']}]")
        if a["quote"]:
            out.append(f'    on:   "{a["quote"][:160]}"')
        if a["text"]:
            out.append(f"    said: {a['text']}")
        elif a["verb"] == "suggest":
            out.append("    said: (cut these words)")
        else:
            out.append("    said: (nothing — the quote is the doubt)")
        for turn in a["turns"]:
            who = f"-> {turn['state']}" if turn["who"] == "agent" else "<- they said"
            out.append(f"    {who}: {turn['text']}")
        out.append("")
    return "\n".join(out)


def cmd_show(args) -> None:
    p = paths(args.dir)
    if args.json:
        print(json.dumps({"meta": read_meta(p), "annotations": list(fold(p).values())}, indent=2))
        return
    print(summarise(p))


def cmd_reply(args) -> None:
    p = paths(args.dir)
    if args.id not in fold(p):
        sys.exit(f"no annotation #{args.id}")
    append_event(p, {"type": "reply", "id": args.id, "state": args.state, "text": args.text})
    print(f"#{args.id} -> {args.state}")


def cmd_watch(args) -> None:
    p = paths(args.dir)
    set_state(p, "idle", pid=os.getpid())   # blocking here means the last round is done
    deadline = time.time() + args.timeout
    beat = time.time()
    while time.time() < deadline:
        if time.time() - beat > 2:           # so the page can tell a dead watcher from a busy one
            set_state(p, "idle", pid=os.getpid())
            beat = time.time()
        offset = int(p["cursor"].read_text() or 0) if p["cursor"].exists() else 0
        size = p["events"].stat().st_size if p["events"].exists() else 0
        if size < offset:
            p["cursor"].write_text("0")
            continue
        if size > offset:
            with p["events"].open("rb") as f:
                f.seek(offset)
                raw = f.read()
            batch = raw.decode("utf-8", errors="replace")
            events = [json.loads(line) for line in batch.splitlines() if line.strip() and _is_json(line)]
            if any(e.get("type") == "nudge" for e in events):
                p["cursor"].write_text(str(offset + len(raw)))
                set_state(p, "working", pid=os.getpid())
                snapshot(p)
                added = sum(1 for e in events if e.get("type") == "annotate")
                gone = sum(1 for e in events if e.get("type") == "delete")
                print(f"nudged — {added} new note(s), {gone} withdrawn\n")
                print(summarise(p))
                return
        time.sleep(0.2)
    print(f"TIMEOUT: no nudge after {int(args.timeout)}s")


def _is_json(line: str) -> bool:
    try:
        json.loads(line)
        return True
    except json.JSONDecodeError:
        return False


# ── server ──────────────────────────────────────────────────────────────────

def free_port(start: int) -> int:
    for port in range(start, start + 100):
        with socket.socket() as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise SystemExit(f"no free port in {start}-{start + 99}")


def make_handler(p: dict[str, Path]):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass

        def _send(self, body: bytes, ctype: str, code: int = 200):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _json(self, payload):
            self._send(json.dumps(payload).encode(), "application/json")

        def do_GET(self):
            url = urlparse(self.path)
            query = parse_qs(url.query)
            if url.path == "/":
                self._send((ASSETS / "shell.html").read_bytes(), "text/html; charset=utf-8")
            elif url.path == "/api/tree":
                annotations = fold(p)
                pages = list_pages(p)
                for page in pages:
                    page["open"] = sum(1 for a in annotations.values()
                                       if a["page"] == page["path"] and a["status"] == "open")
                meta = read_meta(p)
                self._json({
                    "slug": meta["slug"], "phase": meta["phase"], "mode": meta["mode"],
                    "agent": agent_state(p), "pages": pages,
                    "counts": {
                        "open": sum(1 for a in annotations.values() if a["status"] == "open"),
                        "resolved": sum(1 for a in annotations.values() if a["status"] == "resolved"),
                    },
                })
            elif url.path == "/api/page":
                rel = (query.get("p") or [""])[0]
                page = p["root"] / rel
                if ".." in rel or not page.is_file() or page.suffix != ".md":
                    self._json({"error": "no such page"})
                    return
                baseline = p["snapshot"] / rel
                previous = baseline.read_text() if baseline.is_file() else ""
                annotations = [a for a in fold(p).values() if a["page"] in (rel, "*")]
                for a in annotations:
                    a["turns"] = a["turns"][-6:]
                self._json({
                    "path": rel, "title": page_title(page),
                    "html": render_page(page.read_text(), previous),
                    "annotations": sorted(annotations, key=lambda a: a["id"]),
                })
            elif url.path == "/api/version":
                docs = sum(f.stat().st_mtime_ns for section in SECTIONS
                           for f in (p["root"] / section).glob("*.md"))
                events = p["events"].stat().st_size if p["events"].exists() else 0
                meta = p["meta"].stat().st_mtime_ns if p["meta"].exists() else 0
                # The watcher's heartbeat touches agent.json every couple of
                # seconds; key off what it *says*, or the page re-renders
                # constantly and folds every card the reader opened.
                agent = agent_state(p)
                self._json({"docs": docs, "events": events, "meta": meta,
                            "agent": f"{agent['listening']}:{agent['state']}:{agent['note']}"})
            else:
                self._send(b"not found", "text/plain", 404)

        def do_POST(self):
            if urlparse(self.path).path != "/api/event":
                self._send(b"not found", "text/plain", 404)
                return
            # A page on any other origin can post here otherwise; the loopback
            # bind is not a boundary once a browser is doing the asking.
            origin = self.headers.get("Origin")
            if origin and urlparse(origin).netloc != self.headers.get("Host"):
                self._send(b"cross-origin", "text/plain", 403)
                return
            length = int(self.headers.get("Content-Length", 0))
            try:
                payload = json.loads(self.rfile.read(length) or b"{}")
            except json.JSONDecodeError:
                self._send(b"bad json", "text/plain", 400)
                return
            event = clean_event(payload) if isinstance(payload, dict) else None
            if event is None:
                self._send(b"unsupported event", "text/plain", 400)
                return
            self._json(append_event(p, event))

    return Handler


def cmd_serve(args) -> None:
    p = paths(args.dir)
    p["state"].mkdir(parents=True, exist_ok=True)
    p["events"].touch()
    port = free_port(args.port)
    p["server"].write_text(json.dumps({"port": port, "pid": os.getpid(), "dir": str(p["root"])}))
    print(f"protodoc on http://localhost:{port}  ({p['root']})", flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), make_handler(p)).serve_forever()


# ── entry ───────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    init = sub.add_parser("init")
    init.add_argument("slug")
    init.add_argument("--root", default=".")
    init.add_argument("--addition", action="store_true")
    init.set_defaults(func=cmd_init)

    serve = sub.add_parser("serve")
    serve.add_argument("dir")
    serve.add_argument("--port", type=int, default=7900)
    serve.set_defaults(func=cmd_serve)

    watch = sub.add_parser("watch")
    watch.add_argument("dir")
    watch.add_argument("--timeout", type=float, default=1800)
    watch.set_defaults(func=cmd_watch)

    show = sub.add_parser("show")
    show.add_argument("dir")
    show.add_argument("--json", action="store_true")
    show.set_defaults(func=cmd_show)

    reply = sub.add_parser("reply")
    reply.add_argument("dir")
    reply.add_argument("--id", type=int, required=True)
    reply.add_argument("--state", choices=STATES, required=True)
    reply.add_argument("--text", default="")
    reply.set_defaults(func=cmd_reply)

    ask = sub.add_parser("ask")
    ask.add_argument("dir")
    ask.add_argument("text")
    ask.set_defaults(func=cmd_ask)

    phase = sub.add_parser("phase")
    phase.add_argument("dir")
    phase.add_argument("name", choices=["user-doc", "tech-doc", "export"])
    phase.set_defaults(func=cmd_phase)

    snap = sub.add_parser("snapshot")
    snap.add_argument("dir")
    snap.set_defaults(func=cmd_snapshot)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
