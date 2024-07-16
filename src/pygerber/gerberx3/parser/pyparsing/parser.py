"""`pygerber.gerberx3.parser.pyparsing.parser` module contains Gerber X3 parser
implementation based on pyparsing library.
"""

from __future__ import annotations

from typing import Optional, Type, cast

from pygerber.gerberx3.ast.nodes.base import Node
from pygerber.gerberx3.parser.pyparsing.grammar import Grammar


class Parser:
    """Gerber X3 parser implementation."""

    def __init__(
        self, ast_node_class_overrides: Optional[dict[str, Type[Node]]] = None
    ) -> None:
        if ast_node_class_overrides is not None:
            self.grammar = Grammar(ast_node_class_overrides).build()
        else:
            self.grammar = Grammar.DEFAULT

    def parse(self, code: str) -> list[Node]:
        """Parse the input."""
        parse_result = self.grammar.parseString(code)
        return cast(list[Node], parse_result.as_list())
