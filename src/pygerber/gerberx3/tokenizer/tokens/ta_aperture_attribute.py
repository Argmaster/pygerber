"""Comment token."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokens.attribute_token import (
    SetAttributeToken,
)

if TYPE_CHECKING:
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class ApertureAttribute(SetAttributeToken):
    """Add an aperture attribute to the dictionary or modify it.

    An aperture attribute is attached to an aperture or a region. They are a method to
    assign attributes to graphical objects in bulk: all objects that are created with
    an aperture inherit its attributes; for example, a via attribute on an aperture
    means that all pads flashed with this aperture are via pads. Providing information
    about graphical objects via their apertures is elegant, compact and efficient. As
    region objects are created without intermediary aperture, aperture objects can be
    assigned to regions directly.

    See section 5.3 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().aperture_attribute.pre_parser_visit_token(self, context)
        context.get_hooks().aperture_attribute.on_parser_visit_token(self, context)
        context.get_hooks().aperture_attribute.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        value = f",{self.value}" if self.value else ""
        return f"TA{self.name}{value}"

    def __str__(self) -> str:
        return f"{super().__str__()}::[{self.name} -> {self.value}]"
