#!/usr/bin/env python3
"""HUD server — serves the shell page, the live UI fragment and state, and logs user events.

Endpoints:
  GET  /         shell page (assets/index.html, next to this file)
  GET  /ui       <workspace>/ui.html      (the agent-owned UI fragment)
  GET  /state    <workspace>/state.json   (the agent-owned data)
  GET  /version  {"ui": <mtime_ns>, "state": <mtime_ns>} — the shell polls this
  POST /event    append one JSON line to <workspace>/events.jsonl (user-action log)

Binds 127.0.0.1 only. Writes <workspace>/server.json with the actual port and pid.
"""
import argparse
import json
import os
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ASSETS = Path(__file__).resolve().parent
EVENT_LOCK = threading.Lock()


def free_port(start: int) -> int:
    for port in range(start, start + 100):
        with socket.socket() as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise SystemExit(f"no free port in {start}-{start + 99}")


def make_handler(workspace: Path):
    ui = workspace / "ui.html"
    state = workspace / "state.json"
    events = workspace / "events.jsonl"

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def _send(self, body: bytes, ctype: str, code: int = 200):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        @staticmethod
        def _mtime(path: Path) -> int:
            try:
                return path.stat().st_mtime_ns
            except OSError:
                return 0

        def do_GET(self):
            route = self.path.split("?")[0]
            if route == "/":
                self._send((ASSETS / "index.html").read_bytes(), "text/html; charset=utf-8")
            elif route == "/ui":
                body = ui.read_bytes() if ui.exists() else b""
                self._send(body, "text/html; charset=utf-8")
            elif route == "/state":
                body = state.read_bytes() if state.exists() else b"{}"
                self._send(body, "application/json")
            elif route == "/version":
                body = json.dumps({"ui": self._mtime(ui), "state": self._mtime(state)})
                self._send(body.encode(), "application/json")
            else:
                self._send(b"not found", "text/plain", 404)

        def do_POST(self):
            if self.path.split("?")[0] != "/event":
                self._send(b"not found", "text/plain", 404)
                return
            length = int(self.headers.get("Content-Length", 0))
            try:
                payload = json.loads(self.rfile.read(length) or b"{}")
            except json.JSONDecodeError:
                self._send(b"bad json", "text/plain", 400)
                return
            record = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), **payload}
            with EVENT_LOCK, events.open("a") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            self._send(b"", "text/plain", 204)

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", required=True, help="workspace directory")
    parser.add_argument("--port", type=int, default=7777, help="preferred port (auto-bumps if busy)")
    args = parser.parse_args()

    workspace = Path(args.dir).resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    (workspace / "events.jsonl").touch()

    port = free_port(args.port)
    (workspace / "server.json").write_text(json.dumps({"port": port, "pid": os.getpid(), "dir": str(workspace)}))
    print(f"HUD on http://localhost:{port}  (workspace: {workspace})", flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), make_handler(workspace)).serve_forever()


if __name__ == "__main__":
    main()
