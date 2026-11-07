"""dev-toolbox: zero-dependency MCP server (stdio, newline-delimited JSON-RPC)."""
import base64
import hashlib
import json
import sys
import uuid
from datetime import datetime, timezone

PROTOCOL_VERSION = "2025-06-18"
RO = {"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False}


def _str(name, desc):
    return {"type": "string", "description": desc}


TOOLS = {
    "generate_uuid": {
        "title": "Generate UUID",
        "description": "Generate one or more random UUID v4 strings.",
        "inputSchema": {"type": "object", "properties": {
            "count": {"type": "integer", "minimum": 1, "maximum": 100, "default": 1}}},
        "fn": lambda a: "\n".join(str(uuid.uuid4()) for _ in range(min(max(int(a.get("count", 1)), 1), 100))),
    },
    "hash_text": {
        "title": "Hash Text",
        "description": "Hash text with md5, sha1, sha256 or sha512. Returns hex digest.",
        "inputSchema": {"type": "object", "required": ["text"], "properties": {
            "text": _str("text", "Text to hash"),
            "algorithm": {"type": "string", "enum": ["md5", "sha1", "sha256", "sha512"], "default": "sha256"}}},
        "fn": lambda a: hashlib.new(a.get("algorithm", "sha256"), a["text"].encode()).hexdigest(),
    },
    "base64_encode": {
        "title": "Base64 Encode",
        "description": "Encode UTF-8 text to base64.",
        "inputSchema": {"type": "object", "required": ["text"], "properties": {"text": _str("text", "Text to encode")}},
        "fn": lambda a: base64.b64encode(a["text"].encode()).decode(),
    },
    "base64_decode": {
        "title": "Base64 Decode",
        "description": "Decode base64 to UTF-8 text.",
        "inputSchema": {"type": "object", "required": ["data"], "properties": {"data": _str("data", "Base64 string")}},
        "fn": lambda a: base64.b64decode(a["data"], validate=True).decode(),
    },
    "convert_timestamp": {
        "title": "Convert Timestamp",
        "description": "Convert a Unix timestamp (seconds) to ISO 8601 UTC, or an ISO 8601 date to Unix seconds. Omit value for current time.",
        "inputSchema": {"type": "object", "properties": {"value": _str("value", "Unix seconds or ISO 8601 string")}},
        "fn": lambda a: _convert_ts(a.get("value")),
    },
}


def _convert_ts(value):
    if value in (None, ""):
        now = datetime.now(timezone.utc)
        return json.dumps({"unix": int(now.timestamp()), "iso": now.isoformat()})
    try:
        dt = datetime.fromtimestamp(float(value), timezone.utc)
    except ValueError:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
    return json.dumps({"unix": int(dt.timestamp()), "iso": dt.isoformat()})


def handle(msg):
    """Return a response dict, or None for notifications."""
    method, mid, params = msg.get("method"), msg.get("id"), msg.get("params") or {}
    if mid is None:
        return None
    if method == "initialize":
        result = {"protocolVersion": params.get("protocolVersion", PROTOCOL_VERSION),
                  "capabilities": {"tools": {}},
                  "serverInfo": {"name": "dev-toolbox", "version": "0.1.0"}}
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {"tools": [{"name": n, "title": t["title"], "description": t["description"],
                             "inputSchema": t["inputSchema"], "annotations": {"title": t["title"], **RO}}
                            for n, t in TOOLS.items()]}
    elif method == "tools/call":
        tool = TOOLS.get(params.get("name"))
        if not tool:
            return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32602, "message": f"Unknown tool: {params.get('name')}"}}
        try:
            result = {"content": [{"type": "text", "text": tool["fn"](params.get("arguments") or {})}]}
        except Exception as e:  # actionable error back to the model, not a crash
            result = {"content": [{"type": "text", "text": f"Error: {e}. Check the input and try again."}], "isError": True}
    else:
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"Method not found: {method}"}}
    return {"jsonrpc": "2.0", "id": mid, "result": result}


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            resp = handle(json.loads(line))
        except json.JSONDecodeError:
            resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}
        if resp:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
