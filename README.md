# dev-toolbox

This repository holds two things:

- [`plugin/`](plugin/) is the Claude Code plugin. It contains only JSON and Markdown and points Claude Code at the hosted MCP server. This folder is what gets submitted to the Claude plugin directory.
- [`api/mcp.py`](api/mcp.py) is the MCP server. It uses only the Python standard library and runs as a Vercel Python function at `/api/mcp`.

Install the plugin:

```
claude plugin marketplace add pradeep01234/dev-toolbox
claude plugin install dev-toolbox@pradeep-tools
```

Run the server locally with `python api/mcp.py`, which serves `http://127.0.0.1:8000`. Run the smoke test with `python test_mcp.py`.

MIT licensed.
