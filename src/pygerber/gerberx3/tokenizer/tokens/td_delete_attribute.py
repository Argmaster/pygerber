"""Comment token."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pygerber.gerberx3.tokenizer.tokens.attribute_token import AttributeToken

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.gerberx3.parser2.context2 import Parser2Context


class DeleteAttribute(AttributeToken):
    """Delete one or all attributes in the dictionary.

    The TD command deletes an aperture attribute or object attribute from the attributes
    dictionary. (File attributes are immutable and are not deleted.)

    See section 5.5 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def __init__(self, string: str, location: int, name: Optional[str]) -> None:
        super().__init__(string, location)
        self.name = name

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        name = tokens.get("attribute_name")
        if name is not None:
            name = str(name)

        return cls(
            string=string,
            location=location,
            name=name,
        )

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().delete_attribute.pre_parser_visit_token(self, context)
        context.get_hooks().delete_attribute.on_parser_visit_token(self, context)
        context.get_hooks().delete_attribute.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        name = self.name if self.name is not None else ""
        return f"TD{name}"

    def __str__(self) -> str:
        return f"{super().__str__()}::[{self.name}]"
