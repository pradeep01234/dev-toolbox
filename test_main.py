import json
import subprocess
import sys
from pathlib import Path

msgs = [
    {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}},
    {"jsonrpc": "2.0", "method": "notifications/initialized"},
    {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
    {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "hash_text", "arguments": {"text": "abc", "algorithm": "md5"}}},
    {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "base64_decode", "arguments": {"data": "aGVsbG8="}}},
    {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "convert_timestamp", "arguments": {"value": "0"}}},
    {"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "base64_decode", "arguments": {"data": "!!"}}},
]
out = subprocess.run([sys.executable, str(Path(__file__).with_name("main.py"))],
                     input="\n".join(map(json.dumps, msgs)) + "\n", capture_output=True, text=True).stdout
r = {m["id"]: m for m in map(json.loads, out.splitlines())}
assert len(r) == 6, r  # notification got no reply
assert r[1]["result"]["serverInfo"]["name"] == "dev-toolbox"
assert all(t["annotations"]["readOnlyHint"] and t["title"] for t in r[2]["result"]["tools"])
assert r[3]["result"]["content"][0]["text"] == "900150983cd24fb0d6963f7d28e17f72"
assert r[4]["result"]["content"][0]["text"] == "hello"
assert json.loads(r[5]["result"]["content"][0]["text"])["iso"].startswith("1970-01-01T00:00:00")
assert r[6]["result"]["isError"]
print("ok")
