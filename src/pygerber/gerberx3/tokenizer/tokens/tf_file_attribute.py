"""Comment token."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokens.attribute_token import (
    SetAttributeToken,
)

if TYPE_CHECKING:
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class FileAttribute(SetAttributeToken):
    """File attribute token.

    The semantics of a file attribute specifies where it must be defined, typically in
    the header of the file. File attributes are immutable. They cannot be redefined or
    deleted.

    See section 5.2 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().file_attribute.pre_parser_visit_token(self, context)
        context.get_hooks().file_attribute.on_parser_visit_token(self, context)
        context.get_hooks().file_attribute.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        value = f",{self.value}" if self.value else ""
        return f"TF{self.name}{value}"

    def __str__(self) -> str:
        return f"{super().__str__()}::[{self.name} -> {self.value}]"
