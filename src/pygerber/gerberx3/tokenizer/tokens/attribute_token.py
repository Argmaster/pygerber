"""Base class for attribute tokens."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pygerber.gerberx3.tokenizer.tokens.bases.extended_command import (
    ExtendedCommandToken,
)

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self


class AttributeToken(ExtendedCommandToken):
    """## 5.1 Attributes Overview,.

    Attributes add meta-information to a Gerber file. Attributes are akin to labels providing
    information about the file or features within them. Examples of meta-information conveyed by
    attributes are:

    - The function of the file in the layer structure. Is the file the top solder mask, the bottom
    copper layer, …?
    - The function of a pad. Is the pad an SMD pad, or a via pad, or a fiducial, ...?

    The attribute syntax provides a flexible and standardized way to add meta-information to a
    Gerber file, independent of the specific semantics or application.

    Attributes do not affect the image. A Gerber reader will generate the correct image if it simply
    ignores the attributes.

    Each attribute consists of an attribute name and an optional attribute value:

    ```ebnf
    <Attribute> = <AttributeName>[,<AttributeValue>]*
    ```

    Attribute names follow the name syntax in section 3.4.3.

    The attribute value consists of one or more comma-separated fields, see section 3.4.4.

    ```ebnf
    <AttributeValue> = <Field>{,<Field>}
    ```

    There are three types of attributes by the item they attach to:

    - `Attachment type` - The item to which they attach meta-information.
    - `File attributes` - Attach meta-information to the file as a whole.
    - `Aperture attributes` - Attach meta-information to an aperture or a region. Objects created by
    the aperture inherit the aperture meta-information.
    - `Object attributes` - Attach meta-information to on object directly.

    There are two types of attributes by the scope of their use:

    - `Standard attributes`. Standard attribute names, values and semantics are defined in this
    specification and are part of it. As they are standardized, they can exchange meta information between all applications.

    - `User attributes`. User attributes can be chosen freely by users to extend the format with
    custom meta-information. Use custom attributes only for unequivocally defined
    machine-readable information, use G04 for mere human-readable comments.

    In accordance with the general rule in 3.4.3 standard attribute names must begin with a dot "."
    while user attribute names cannot begin with a dot. The dot, if present, is part of the attribute
    name and indicates that it is a standard attribute whose syntax and semantics are defined in
    section 5.6.

    ---

    ## Example

    ```gerber
    %TFMyAttribute,Yes*%
    %TFZap*%
    %TFZonk*%
    ```

    ---

    See section 5.1 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=122)

    """  # noqa: E501


class SetAttributeToken(AttributeToken):
    """Base class for all classes which set some kind of attribute."""

    def __init__(
        self,
        string: str,
        location: int,
        name: str,
        value: Optional[str],
    ) -> None:
        super().__init__(string, location)
        self.name = name
        self.value = value

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        name: str = str(tokens["attribute_name"])
        value = tokens.get("field", None)
        if value is not None:
            value = str(value)

        return cls(
            string=string,
            location=location,
            name=name,
            value=value,
        )
