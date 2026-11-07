# Dev Toolbox

Dev Toolbox is a free Claude Code plugin. It bundles a small local MCP server that gives Claude a few developer utilities. Everything runs on your own machine. The server makes no network requests, collects no data, and reads or writes no files. It uses only the Python standard library, so you don't need to install any packages.

## Tools

All tools are read-only.

| Tool | What it does |
|------|--------------|
| `generate_uuid` | Generates 1 to 100 random UUID v4 strings |
| `hash_text` | Hashes text with md5, sha1, sha256 or sha512 |
| `base64_encode` | Encodes UTF-8 text as base64 |
| `base64_decode` | Decodes base64 back to UTF-8 text |
| `convert_timestamp` | Converts Unix seconds to ISO 8601 and back. With no value, it returns the current time |

## Requirements

You need Python 3.8 or later available as `python3` on your PATH.

## Install

```
claude plugin marketplace add <github-owner>/<repo>
claude plugin install dev-toolbox@pradeep-tools
```

## What it runs

The plugin starts `python3 main.py` as a stdio MCP server. Claude sends it JSON-RPC requests on stdin, and the server answers on stdout. It does nothing else.

## Privacy

The plugin collects, stores and sends no data. See [PRIVACY.md](PRIVACY.md).

## License

MIT. See [LICENSE](LICENSE).
