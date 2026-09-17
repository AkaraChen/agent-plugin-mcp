---
name: calling-mcp
description: Call MCP servers through the mcporter CLI. Use when a task needs a server that is not wired in natively, a server already configured for another editor, or a one-off MCP URL.
license: MIT
metadata:
  author: AkaraChen
  version: "1.0.0"
---

# Calling MCP

mcporter carries MCP tool calls between an agent and any MCP server: stdio, Streamable HTTP, or a
one-off URL, with OAuth handled. You call it as a CLI. This skill covers the shape you need for
almost every task; run `mcporter <subcommand> --help` for the rest.

## When to use

- The task names a server that is not available as a native tool.
- A server is already configured for Cursor, Claude Code, Codex, Windsurf, OpenCode, or VS Code
  and you want the same tools here.
- You need one call against a public MCP URL without editing any config.

## Before you call

Check the CLI is present and which version it is:

```bash
mcporter --version || echo "mcporter: not installed"
```

Nothing printed means it is not installed. Then either install it:

```bash
npm install -g mcporter                  # needs Node 24+
brew install steipete/tap/mcporter       # macOS/Linux, no Node needed
```

or skip the install and let npx fetch it per command:

```bash
npx -y mcporter list
```

The command set moves between releases, so treat `--help` on the installed build as the source of
truth for what exists, ahead of any doc.

## Commands

| Goal | Command |
|---|---|
| See configured servers | `mcporter list` |
| One server's tools | `mcporter list <server> --brief` or `--schema` |
| Call a tool | `mcporter call <server>.<tool> --args '{...}'` |
| Call with inline values | `mcporter call linear.create_comment issueId=ENG-123 body="Looks good!"` |
| Call a public URL | `mcporter call https://mcp.context7.com/mcp.resolve-library-id query="react hooks" libraryName=react` |
| Stable output for parsing | add `--json` (list) or `--output json` (call) |
| OAuth-gated server | `mcporter auth <server-or-url>` |
| Add a server | `mcporter config add <name> <url> --scope home` |

## Procedure

1. Confirm the CLI before anything else: `mcporter --version`. Install it if that prints nothing.
2. `mcporter list` shows what is already configured. An empty list is normal on a fresh machine.
3. Read the tool signatures before calling: `mcporter list <server> --schema`. Take argument names
   and required fields from those signatures instead of guessing.
4. Call the tool with `--args` and a JSON object, quoted so the shell keeps the braces.
5. Add `--output json` when you intend to read values out of the result.

## Pitfalls

- Server list is resolved from `./config/mcporter.json` first, then the home config. Run from the
  project that owns that file, or pass `--config <path>`, or the server will look missing.
- Argument names belong to the server, not to mcporter. A name that does not exist on the server is
  a server-side error.
- Server output goes to stdout; progress and warnings go to stderr. A pipe stays parseable.
- OAuth servers fail until `mcporter auth <server>` has run once. That may open a browser, so on a
  headless machine set the credential up out of band.
- First call through `npx` includes install time. Give the command room to finish.
