"""The `parser` module contains Gerber X3 parser implementation based on pyparsing
library.
"""

from __future__ import annotations

from typing import Optional, Type

from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.file import File
from pygerber.gerber.parser.pyparsing.grammar import Grammar


class Parser:
    """Gerber X3 parser implementation."""

    def __init__(
        self,
        ast_node_class_overrides: Optional[dict[str, Type[Node]]] = None,
        *,
        resilient: bool = False,
    ) -> None:
        builder = Grammar(ast_node_class_overrides or {})
        if resilient:
            self.grammar = builder.build_resilient()
        else:
            self.grammar = builder.build()

    def parse(self, code: str, *, strict: bool = True) -> File:
        """Parse the input."""
        parse_result = self.grammar.parseString(code, parse_all=strict).get("root_node")
        assert isinstance(parse_result, File)
        return parse_result
