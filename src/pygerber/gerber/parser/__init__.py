"""The `parser` package contains existing and future Gerber X3 parser
implementations.

Additionally, it exposes a high level `parse` function that allows to parse Gerber
source.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Optional, Type

from typing_extensions import Protocol

if TYPE_CHECKING:
    from pygerber.gerber.ast.nodes import File, Node


class ParserProtocol(Protocol):
    """Parser protocol."""

    def parse(self, code: str, *, strict: bool = True) -> Any:
        """Parse the input."""


def parse(
    code: str,
    *,
    strict: bool = True,
    parser: Literal["pyparsing"] = "pyparsing",
    resilient: bool = False,
    ast_node_class_overrides: Optional[dict[str, Type[Node]]] = None,
) -> File:
    """Parse Gerber X3 file source code and construct AST from it.

    Parameters
    ----------
    code : str
        Gerber source code.
    strict : bool, optional
        Toggle enforcement of parsing whole code, by default True
        When set to False, parser will try to parse as much as possible and will stop
        after it encounters first unrecognized token.
    parser : Literal[&quot;pyparsing&quot;], optional
        Parsing backend to use, by default "pyparsing"
    resilient : bool, optional
        Toggle resilient parsing. When set to True, when parser encounters invalid token
        it will wrap it in `InvalidToken` node and continue parsing, by default False
    ast_node_class_overrides : Optional[dict[str, Type[Node]]], optional
        Override classes representing nodes used by parser to construct abstract syntax
        tree, by default None
        When dictionary is provided, parser will check if there is a class override
        available for given node. Keys in dictionary have to be string corresponding to
        names of overridden node classes for parser to use them. In most cases it is
        necessary for replacement node class to inherit from original one.

    Returns
    -------
    File
        Abstract syntax tree of parsed Gerber file.

    Raises
    ------
    NotImplementedError
        For unrecognized parser backend names.

    """
    if parser == "pyparsing":
        from pygerber.gerber.parser.pyparsing.parser import Parser

        return Parser(
            resilient=resilient, ast_node_class_overrides=ast_node_class_overrides
        ).parse(code, strict=strict)

    msg = f"Parser '{parser}' is not supported."  # type: ignore[unreachable]
    raise NotImplementedError(msg)
