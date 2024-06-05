"""Common elements of Rasterized2D tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.parser2.context2 import Parser2Context
from pygerber.gerberx3.parser2.parser2 import Parser2, Parser2Options
from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer

if TYPE_CHECKING:
    from pathlib import Path


def debug_dump_context(ctx: Parser2Context, dest_dir: Path) -> None:
    """Dump parser context to JSON file."""
    dest_dir.mkdir(exist_ok=True, parents=True)
    (dest_dir / "state.json").write_text(
        ctx.state.model_dump_json(indent=4),
        encoding="utf-8",
    )
    (dest_dir / "main_command_buffer.json").write_text(
        ctx.main_command_buffer.get_readonly().debug_buffer_to_json(),
        encoding="utf-8",
    )
    (dest_dir / "region_command_buffer.json").write_text(
        (
            ctx.region_command_buffer.get_readonly().debug_buffer_to_json()
            if ctx.region_command_buffer
            else "null"
        ),
        encoding="utf-8",
    )
    for i, buffer in enumerate(ctx.block_command_buffer_stack):
        (dest_dir / f"block_command_buffer_{i}.json").write_text(
            buffer.get_readonly().debug_buffer_to_json(),
            encoding="utf-8",
        )


def parse_code(
    gerber_source_code: str,
    initial_context: Parser2Context,
) -> Parser2Context:
    ast = Tokenizer().tokenize_expressions(gerber_source_code)
    p = Parser2(Parser2Options(initial_context=initial_context))
    p.parse(ast)
    return p.context
