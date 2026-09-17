"""mcporter plugin — expose MCP servers to Hermes through the mcporter CLI."""

from __future__ import annotations

from functools import partial
from pathlib import Path

from . import tools


def register(ctx):
    """Register the two tools and the bundled calling-mcp skill."""
    ctx.register_tool(
        name="mcp_list",
        toolset="mcporter",
        schema=tools.MCP_LIST,
        handler=partial(tools.mcp_list, ctx),
        check_fn=tools.mcporter_available,
    )
    ctx.register_tool(
        name="mcp_call",
        toolset="mcporter",
        schema=tools.MCP_CALL,
        handler=partial(tools.mcp_call, ctx),
        check_fn=tools.mcporter_available,
    )

    skills_dir = Path(__file__).parent / "skills"
    for child in sorted(skills_dir.iterdir()):
        skill_md = child / "SKILL.md"
        if child.is_dir() and skill_md.exists():
            ctx.register_skill(child.name, skill_md)
