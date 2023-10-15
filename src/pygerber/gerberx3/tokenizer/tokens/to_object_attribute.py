"""Comment token."""


from __future__ import annotations

from typing import TYPE_CHECKING, List

from pyparsing import ParseResults

from pygerber.gerberx3.tokenizer.tokens.attribute_token import AttributeToken

if TYPE_CHECKING:
    from typing_extensions import Self


class ObjectAttribute(AttributeToken):
    """Add an object attribute to the dictionary or modify it.

    An object attribute is attached to graphical objects. When a D01, D03 or region
    statement (G36/G37) creates an object all object attributes in the attribute
    dictionary are attached to it. As attribute commands are not allowed inside a region
    statement, all regions created by that statement have the same object attributes.
    Once attached to an object they cannot be chan

    See section 5.4 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def __init__(self, string: str, location: int, name: str, value: List[str]) -> None:
        super().__init__(string, location)
        self.name = name
        self.value = value

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        name: str = str(tokens["attribute_name"])
        value = tokens.get("field", [])

        if isinstance(value, ParseResults):
            value = value.as_list()

        return cls(
            string=string,
            location=location,
            name=name,
            value=value,  # type: ignore[pylance]
        )

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"TO{','.join((self.name, *self.value))}"

    def __str__(self) -> str:
        return f"{super().__str__()}::[{self.name} -> {self.value}]"
