# agent-plugin-mcp

An [Agent Plugins](https://agent-plugins.org/specification) v1 package that teaches any compatible
agent to call MCP servers through [mcporter](https://mcporter.sh).

mcporter carries MCP tool calls between an agent and any MCP server — stdio, Streamable HTTP, or a
one-off URL, with OAuth handled. It is a CLI, so the portable way to package it is one skill rather
than a server declaration. This package is exactly that: one skill.

```
agent-plugin-mcp/
├── plugin.json
├── skills/
│   └── calling-mcp/
│       └── SKILL.md
├── README.md
└── LICENSE
```

## What the skill covers

`calling-mcp` gives the agent the three commands it needs almost every time — list servers, read a
server's tool signatures, call one tool — one worked example against a real public server, and the
pitfalls that produce silent failures. Everything else is a `mcporter <subcommand> --help` away
instead of being restated here.

## Requirements

- `mcporter` on PATH (`npm install -g mcporter`, `brew install steipete/tap/mcporter`), or `npx`
  available so `npx -y mcporter` works.
- Node 24+ for npm installs.

## Install

Any client that supports Agent Plugins v1 can load this directory. With Hermes Agent:

```bash
hermes plugins install AkaraChen/agent-plugin-mcp
hermes plugins enable agent-plugin-mcp
```

Portable packages install disabled, so enable it explicitly. Other clients point at the repository
or copy the directory into their own plugin location.

## Verify it works

```bash
npx -y mcporter list https://mcp.context7.com/mcp --brief
npx -y mcporter call https://mcp.context7.com/mcp.resolve-library-id \
  query="react hooks" libraryName=react --output json
```

The second command returns matching library IDs. Nothing to configure or authenticate.

## License

MIT
