# agent-plugin-mcp

A [Hermes Agent](https://github.com/NousResearch/hermes-agent) plugin that puts
[mcporter](https://mcporter.sh) behind two tools, plus the `calling-mcp` skill.

mcporter carries MCP tool calls between your agent and any MCP server: stdio, Streamable HTTP, or a
one-off URL, with OAuth handled. This plugin exposes that as tools instead of a mega tool-schema.

## Install

```bash
hermes plugins install AkaraChen/agent-plugin-mcp
hermes plugins enable mcporter
```

mcporter itself comes from npm or Homebrew. The tools work through `npx` too, so a global install is
optional:

```bash
npm install -g mcporter      # or: brew install steipete/tap/mcporter
```

## Tools

| Tool | What it does |
|---|---|
| `mcp_list` | Lists configured servers, or one server's tool signatures (`--schema`). |
| `mcp_call` | Calls one tool by `server.tool` selector or an HTTP URL selector. |

Both run the CLI through the `terminal` tool, so commands keep the normal approval and cwd
behaviour. They stay hidden when neither `mcporter` nor `npx` is on PATH.

## Skill

`calling-mcp` covers the two shapes you need most — finding a server's tools and calling one — and
points at `mcporter <subcommand> --help` for everything else. Load it explicitly:

```
skill_view("mcporter:calling-mcp")
```

## Layout

```
agent-plugin-mcp/
├── plugin.yaml
├── __init__.py            # register(ctx): two tools + bundled skill
├── tools.py               # schemas, mcporter invocation
└── skills/
    └── calling-mcp/
        └── SKILL.md
```

## License

MIT
