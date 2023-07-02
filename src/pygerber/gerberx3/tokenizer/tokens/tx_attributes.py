"""Comment token."""


from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.token import Token


class AttributeToken(Token):
    """Base class for all attribute manipulation tokens."""


class FileAttribute(AttributeToken):
    """File attribute token.

    The semantics of a file attribute specifies where it must be defined, typically in
    the header of the file. File attributes are immutable. They cannot be redefined or
    deleted.
    """

    def __init__(
        self,
        file_attribute_name: str,
        field: list[str] | None = None,
    ) -> None:
        """Initialize token object."""
        super().__init__()
        self.attribute_name = file_attribute_name
        self.fields = field if field is not None else []

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"TF{','.join((self.attribute_name, *self.fields))}*"


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

    def __init__(
        self,
        aperture_attribute_name: str,
        field: list[str] | None = None,
    ) -> None:
        """Initialize token object."""
        super().__init__()
        self.attribute_name = aperture_attribute_name
        self.fields = field if field is not None else []

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"TA{','.join((self.attribute_name, *self.fields))}*"


class ObjectAttribute(AttributeToken):
    """Add an object attribute to the dictionary or modify it.

    An object attribute is attached to graphical objects. When a D01, D03 or region
    statement (G36/G37) creates an object all object attributes in the attribute
    dictionary are attached to it. As attribute commands are not allowed inside a region
    statement, all regions created by that statement have the same object attributes.
    Once attached to an object they cannot be chan
    """

    def __init__(
        self,
        object_attribute_name: str,
        field: list[str] | None = None,
    ) -> None:
        """Initialize token object."""
        super().__init__()
        self.attribute_name = object_attribute_name
        self.fields = field if field is not None else []

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"TO{','.join((self.attribute_name, *self.fields))}*"


class DeleteAttribute(AttributeToken):
    """Delete one or all attributes in the dictionary.

    The TD command deletes an aperture attribute or object attribute from the attributes
    dictionary. (File attributes are immutable and are not deleted.)
    """

    def __init__(self, attribute_name: str | None = None) -> None:
        """Initialize token object."""
        super().__init__()
        self.attribute_name = attribute_name

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"TD{self.attribute_name if self.attribute_name is not None else ''}*"
