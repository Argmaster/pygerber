"""Comment token."""


from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

from pyparsing import ParseResults

from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self


class AttributeToken(Token):
    """Base class for all attribute manipulation tokens."""


class FileAttribute(AttributeToken):
    """File attribute token.

    The semantics of a file attribute specifies where it must be defined, typically in
    the header of the file. File attributes are immutable. They cannot be redefined or
    deleted.
    """

    name: str
    value: List[str]

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        name: str = tokens["file_attribute_name"]
        value = tokens.get("field", [])

        if isinstance(value, ParseResults):
            value = value.as_list()

        return cls(name=name, value=value)

    def __str__(self) -> str:
        return f"TF{','.join((self.name, *self.value))}*"


class ApertureAttribute(AttributeToken):
    """Add an aperture attribute to the dictionary or modify it.

    An aperture attribute is attached to an aperture or a region. They are a method to
    assign attributes to graphical objects in bulk: all objects that are created with
    an aperture inherit its attributes; for example, a via attribute on an aperture
    means that all pads flashed with this aperture are via pads. Providing information
    about graphical objects via their apertures is elegant, compact and efficient. As
    region objects are created without intermediary aperture, aperture objects can be
    assigned to regions directly.
    """

    name: str
    value: List[str]

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        name: str = tokens["aperture_attribute_name"]
        value = tokens.get("field", [])

        if isinstance(value, ParseResults):
            value = value.as_list()

        return cls(name=name, value=value)

    def __str__(self) -> str:
        return f"TA{','.join((self.name, *self.value))}*"


class ObjectAttribute(AttributeToken):
    """Add an object attribute to the dictionary or modify it.

    An object attribute is attached to graphical objects. When a D01, D03 or region
    statement (G36/G37) creates an object all object attributes in the attribute
    dictionary are attached to it. As attribute commands are not allowed inside a region
    statement, all regions created by that statement have the same object attributes.
    Once attached to an object they cannot be chan
    """

    name: str
    value: List[str]

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        name: str = tokens["object_attribute_name"]
        value = tokens.get("field", [])

        if isinstance(value, ParseResults):
            value = value.as_list()

        return cls(name=name, value=value)

    def __str__(self) -> str:
        return f"TO{','.join((self.name, *self.value))}*"


class DeleteAttribute(AttributeToken):
    """Delete one or all attributes in the dictionary.

    The TD command deletes an aperture attribute or object attribute from the attributes
    dictionary. (File attributes are immutable and are not deleted.)
    """

    name: Optional[str]

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        name: Optional[str] = tokens.get("attribute_name")
        return cls(name=name)

    def __str__(self) -> str:
        return f"TD{self.name if self.name is not None else ''}*"
