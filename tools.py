"""mcporter wrappers: run the CLI through the terminal tool.

Every handler returns a JSON string, as the tool registry requires. Commands go
through ``ctx.dispatch_tool("terminal", ...)`` rather than ``subprocess`` so they
keep the normal approval, cwd, and output-redaction behaviour.
"""

from __future__ import annotations

import json
import shlex
import shutil

COMMAND_TIMEOUT_SECONDS = 300
NPX_SPEC = "mcporter"

MCP_LIST = {
    "name": "mcp_list",
    "description": (
        "List MCP servers reachable through mcporter, or one server's tools. "
        "Without a server, shows every configured server (mcporter config plus imports from "
        "Cursor / Claude Code / Codex / Windsurf / OpenCode / VS Code). With a server or URL, "
        "shows its tool signatures."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "server": {
                "type": "string",
                "description": "Configured server name or an HTTP MCP URL. Omit to list all servers.",
            },
            "detail": {
                "type": "string",
                "enum": ["brief", "schema"],
                "description": "brief: names and one-line summaries. schema: full TypeScript-style signatures. Default brief.",
            },
        },
    },
}

MCP_CALL = {
    "name": "mcp_call",
    "description": (
        "Call one tool on an MCP server through mcporter. Give a selector like "
        "'linear.list_issues', or a URL selector like 'https://mcp.context7.com/mcp.resolve-library-id'. "
        "Arguments are passed as a JSON object."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "selector": {
                "type": "string",
                "description": "server.tool, or <http url>.tool. Takes precedence over server + tool.",
            },
            "server": {"type": "string", "description": "Configured server name."},
            "tool": {"type": "string", "description": "Tool name on that server."},
            "selector_args": {
                "type": "object",
                "description": "Arguments for the tool, e.g. {\"query\": \"react hooks\", \"libraryName\": \"react\"}.",
            },
            "output": {
                "type": "string",
                "enum": ["text", "markdown", "json", "raw"],
                "description": "Output format. Use json when you need to parse the result. Default: mcporter's own default.",
            },
        },
    },
}


def mcporter_available() -> bool:
    """True when mcporter or npx can be invoked."""
    return bool(shutil.which("mcporter") or shutil.which("npx"))


def _command(args: list[str]) -> str:
    if shutil.which("mcporter"):
        return shlex.join(["mcporter", *args])
    if shutil.which("npx"):
        return shlex.join(["npx", "-y", NPX_SPEC, *args])
    return ""


def run(ctx, args: list[str]) -> str:
    """Run ``mcporter <args>`` and return a JSON envelope."""
    command = _command(args)
    if not command:
        return json.dumps(
            {"ok": False, "error": "mcporter not found. Install it (npm install -g mcporter) or make npx available."}
        )
    raw = ctx.dispatch_tool("terminal", {"command": command, "timeout": COMMAND_TIMEOUT_SECONDS})
    try:
        result = json.loads(raw)
    except (TypeError, ValueError):
        return json.dumps({"ok": False, "command": command, "error": "unreadable terminal output", "raw": str(raw)[:2000]})
    if isinstance(result, dict) and "output" in result:
        return json.dumps({"ok": True, "command": command, "output": result["output"]})
    return json.dumps({"ok": False, "command": command, "terminal_result": result})


def mcp_list(ctx, args, **kwargs) -> str:
    argv = ["list"]
    server = (args.get("server") or "").strip()
    if server:
        argv.append(server)
        argv.append("--schema" if args.get("detail") == "schema" else "--brief")
    return run(ctx, argv)


def mcp_call(ctx, args, **kwargs) -> str:
    selector = (args.get("selector") or "").strip()
    if not selector:
        server = (args.get("server") or "").strip()
        tool = (args.get("tool") or "").strip()
        if not (server and tool):
            return json.dumps({"ok": False, "error": "pass selector, or both server and tool"})
        selector = f"{server}.{tool}"

    argv = ["call", selector]
    call_args = args.get("selector_args")
    if isinstance(call_args, dict) and call_args:
        argv += ["--args", json.dumps(call_args)]
    if args.get("output"):
        argv += ["--output", str(args["output"])]
    return run(ctx, argv)
