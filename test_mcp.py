"""Smoke test: starts the server locally and calls it over HTTP. Run: python test_mcp.py"""
import importlib.util
import json
import threading
import urllib.error
import urllib.request
from http.server import HTTPServer
from pathlib import Path

spec = importlib.util.spec_from_file_location("mcp_server", Path(__file__).parent / "api" / "mcp.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
srv = HTTPServer(("127.0.0.1", 0), mod.handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_port}/api/mcp"


def post(msg):
    req = urllib.request.Request(URL, json.dumps(msg).encode(), {"Content-Type": "application/json",
                                                                  "Accept": "application/json, text/event-stream"})
    with urllib.request.urlopen(req) as r:
        return r.status, (json.loads(r.read()) if r.status == 200 else None)


def call(i, name, args):
    return post({"jsonrpc": "2.0", "id": i, "method": "tools/call", "params": {"name": name, "arguments": args}})[1]["result"]


assert post({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}})[1]["result"]["serverInfo"]["name"] == "dev-toolbox"
assert post({"jsonrpc": "2.0", "method": "notifications/initialized"})[0] == 202
tools = post({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})[1]["result"]["tools"]
assert len(tools) == 5 and all(t["annotations"]["readOnlyHint"] and t["title"] for t in tools)
assert call(3, "hash_text", {"text": "abc", "algorithm": "md5"})["content"][0]["text"] == "900150983cd24fb0d6963f7d28e17f72"
assert call(4, "base64_decode", {"data": "aGVsbG8="})["content"][0]["text"] == "hello"
assert json.loads(call(5, "convert_timestamp", {"value": "0"})["content"][0]["text"])["iso"].startswith("1970-01-01T00:00:00")
assert call(6, "base64_decode", {"data": "!!"})["isError"]
assert len(call(7, "generate_uuid", {"count": 3})["content"][0]["text"].splitlines()) == 3
try:
    urllib.request.urlopen(URL)
    raise AssertionError("GET should be 405")
except urllib.error.HTTPError as e:
    assert e.code == 405
print("ok")
