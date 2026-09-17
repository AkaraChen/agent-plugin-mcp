---
name: calling-mcp
description: "Call MCP servers through the mcporter CLI."
version: 1.0.0
author: AkaraChen
license: MIT
metadata:
  hermes:
    tags: [mcp, mcporter, tools]
    category: mcp
---

# Calling MCP Skill

Use the `mcporter` CLI to list and call MCP servers that are not wired into Hermes as native tools.
This skill covers the two shapes you need most: finding a server's tools, and calling one. Everything
else (generated CLIs, OAuth, stdio servers, the daemon, typed clients) is one `--help` away.

## When to Use

- The user names an MCP server (Linear, Context7, Supabase, a local stdio command, an HTTP URL) and wants data from it.
- A server is configured for Cursor / Claude / Codex / VS Code and you want the same tools here.
- You need a one-off call against a public MCP URL without touching config.

## Prerequisites

- `mcporter` on PATH (`npm install -g mcporter` or `brew install steipete/tap/mcporter`), or `npx` available.
  The plugin's `mcp_list` / `mcp_call` tools pick whichever exists.
- The `terminal` tool, since the CLI runs through it.

## How to Run

Prefer the plugin tools (`mcp_list`, `mcp_call`). Reach for `terminal` directly when you need a
subcommand the tools do not wrap, or extra flags.

```bash
mcporter list                              # every configured server
mcporter list context7 --brief             # one server, short descriptions
mcporter list context7 --schema            # full TypeScript-style signatures
mcporter call context7.resolve-library-id --args '{"query":"react hooks","libraryName":"react"}'
```

## Quick Reference

| Goal | Command |
|---|---|
| All configured servers | `mcporter list` |
| One server's tools | `mcporter list <server> --brief` or `--schema` |
| Call a tool | `mcporter call <server>.<tool> --args '{...}'` |
| Call with inline values | `mcporter call linear.create_comment issueId=ENG-123 body="Looks good!"` |
| Call a public URL | `mcporter call https://mcp.context7.com/mcp.resolve-library-id query="react hooks" libraryName=react` |
| Parse the result | add `--output json` |
| OAuth-gated server | `mcporter auth <server-or-url>` |
| Details on any subcommand | `mcporter <subcommand> --help` |

Output goes to stdout; progress and warnings go to stderr, so pipes stay parseable.

## Procedure

1. Run `mcporter list` to see what is already configured. Nothing configured is normal on a fresh
   machine — continue to step 2 with a URL or a stdio command instead.
2. Get the tool signatures for the server you need: `mcporter list <server> --schema`. Read the
   argument names and required fields off those signatures; do not guess them.
3. Call the tool with `--args` and a JSON object. Quote it so the shell does not eat the braces.
4. Add `--output json` when you intend to read values out of the result.

## Pitfalls

- `mcporter list` reads `./config/mcporter.json` first. Run from the project that owns that file, or
  pass `--config <path>`, or the server will look missing.
- Argument names are the server's, not the CLI's. `limit:5` on a server that calls it `count` is a
  server-side error, not a CLI error.
- First call to a server through `npx` includes install time. Give the command room to finish.
- OAuth servers return an auth error until `mcporter auth <server>` has run once. That command may
  open a browser; on a headless box, set up the token out of band first.
- `--output json` is the CLI's stable envelope. Anything else is meant for humans and may reflow.

## Verification

`mcporter list` prints a line per configured server; `mcporter call ... --output json` returns JSON on
stdout with nothing from stderr mixed in. Empty stdout with an error on stderr means the call failed,
even when the exit code looks unremarkable.
