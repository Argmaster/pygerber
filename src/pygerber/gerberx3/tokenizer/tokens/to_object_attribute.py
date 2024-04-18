"""Comment token."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokens.attribute_token import (
    SetAttributeToken,
)

if TYPE_CHECKING:
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class ObjectAttribute(SetAttributeToken):
    """Add an object attribute to the dictionary or modify it.

    An object attribute is attached to graphical objects. When a D01, D03 or region
    statement (G36/G37) creates an object all object attributes in the attribute
    dictionary are attached to it. As attribute commands are not allowed inside a region
    statement, all regions created by that statement have the same object attributes.
    Once attached to an object they cannot be chan

    See section 5.4 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().object_attribute.pre_parser_visit_token(self, context)
        context.get_hooks().object_attribute.on_parser_visit_token(self, context)
        context.get_hooks().object_attribute.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        value = f",{self.value}" if self.value else ""
        return f"TO{self.name}{value}"

    def __str__(self) -> str:
        return f"{super().__str__()}::[{self.name} -> {self.value}]"
