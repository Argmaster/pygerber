"""`pygerber.gerberx3.parser` package contains Gerber X3 parser implementations."""

from __future__ import annotations

from typing import Any, Literal

from typing_extensions import Protocol

from pygerber.gerberx3.ast.nodes.file import File


class ParserProtocol(Protocol):
    """Parser protocol."""

    def parse(self, code: str, *, strict: bool = True) -> Any:
        """Parse the input."""


def parse(
    code: str,
    *,
    strict: bool = True,
    parser: Literal["pyparsing"] = "pyparsing",
    **options: Any,
) -> File:
    """Parse GerberX3 file source code and construct AST from it."""
    if parser == "pyparsing":
        from pygerber.gerberx3.parser.pyparsing.parser import Parser

        return Parser(**options).parse(code, strict=strict)

    msg = f"Parser '{parser}' is not supported."  # type: ignore[unreachable]
    raise NotImplementedError(msg)
