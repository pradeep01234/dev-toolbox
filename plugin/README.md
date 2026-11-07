# Dev Toolbox

Dev Toolbox is a free Claude Code plugin that gives Claude a few everyday developer utilities. It connects Claude to a hosted MCP server at `https://dev-toolbox-jade-rho.vercel.app/api/mcp`. Nothing is installed or run on your computer. The server's source code is public in this repository under `api/mcp.py`.

## Tools

All tools are read-only. They compute a result from your input and return it, and they never change anything.

| Tool | What it does |
|------|--------------|
| `generate_uuid` | Generates 1 to 100 random UUID v4 strings |
| `hash_text` | Hashes text with md5, sha1, sha256 or sha512 |
| `base64_encode` | Encodes UTF-8 text as base64 |
| `base64_decode` | Decodes base64 back to UTF-8 text |
| `convert_timestamp` | Converts Unix seconds to ISO 8601 and back. With no value, it returns the current time |

## Install

```
claude plugin marketplace add pradeep01234/dev-toolbox
claude plugin install dev-toolbox@pradeep-tools
```

## What it sends

When Claude calls a tool, Claude Code sends the tool's input (for example, the text to hash) over HTTPS to the server above. The server returns the result. It does not store, log or forward your input, and it calls no other services. See [PRIVACY.md](PRIVACY.md).

## License

MIT. See [LICENSE](LICENSE).
