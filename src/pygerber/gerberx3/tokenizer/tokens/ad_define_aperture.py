"""Wrapper for aperture definition token.

Generally, apertures with size zero are invalid, and so are objects created with them.
There is one exception. The C (circular) standard aperture with zero diameter is
allowed, and so are objects created with it. Attributes can be attached to them. For the
avoidance of doubt, zero size is only allowed for the C aperture, not another aperture
type whose shape is fortuitously circular.

Zero-size objects do not affect the image. They can be used to provide meta-information
to locations in the image plane.

Allowed does not mean recommended, quite the contrary. If you are tempted to use a
zero-size object, consider whether it is useful, and whether there is no proper way to
convey the metainformation. Certainly do not abuse a zero-size object to indicate the
absence of an object, e.g. by flashing a zero-size aperture to indicate the absence of
a pad. This is just confusing. If there is nothing, put nothing.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from pyparsing import ParseResults


class ADDefineAperture(Token):
    """Wrapper for aperture definition token.

    Defines a template-based aperture, assigns a D code to it. This class is never used
    to create objects, only its subclasses are used.
    """

    def __init__(self) -> None:
        """Initialize token object."""
        super().__init__()

    @classmethod
    def new(
        cls,
        _string: str,
        _location: int,
        tokens: ParseResults,
    ) -> ADDefineAperture:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        aperture_type = tokens.pop("aperture_type")
        if not isinstance(aperture_type, str):
            msg = "Expected aperture type to be string."
            raise TypeError(msg)

        if aperture_type == "C":
            return ADDefineCircle(**tokens.as_dict())

        if aperture_type == "R":
            return ADDefineRectangle(**tokens.as_dict())

        if aperture_type == "O":
            return ADDefineObround(**tokens.as_dict())

        if aperture_type == "P":
            return ADDefinePolygon(**tokens.as_dict())

        return ADDefineMacro(aperture_type=aperture_type, **tokens.as_dict())

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return "<ADDefineAperture-INVALID>"


class ADDefineCircle(ADDefineAperture):
    """Wrapper for aperture definition token.

    Defines a circle.
    """

    def __init__(
        self,
        aperture_identifier: str,
        diameter: str,
        hole_diameter: str | None = None,
    ) -> None:
        """Initialize token object."""
        super().__init__()
        self.aperture_identifier = aperture_identifier
        self.diameter = float(diameter)
        self.hole_diameter = float(hole_diameter) if hole_diameter is not None else None

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        suffix = ""
        if self.hole_diameter is not None:
            suffix += f"X{self.hole_diameter}"
        return f"%AD{self.aperture_identifier}C,{self.diameter}{suffix}*%"


class ADDefineRectangle(ADDefineAperture):
    """Wrapper for aperture definition token.

    Defines a rectangle
    """

    def __init__(
        self,
        aperture_identifier: str,
        x_size: str,
        y_size: str,
        hole_diameter: str | None = None,
    ) -> None:
        """Initialize token object."""
        super().__init__()
        self.aperture_identifier = aperture_identifier
        self.x_size = float(x_size)
        self.y_size = float(y_size)
        self.hole_diameter = float(hole_diameter) if hole_diameter is not None else None

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        suffix = ""
        if self.hole_diameter is not None:
            suffix += f"X{self.hole_diameter}"
        return f"%AD{self.aperture_identifier}R,{self.x_size}X{self.y_size}{suffix}*%"


class ADDefineObround(ADDefineAperture):
    """Wrapper for aperture definition token.

    Defines a obround.
    """

    def __init__(
        self,
        aperture_identifier: str,
        x_size: str,
        y_size: str,
        hole_diameter: str | None = None,
    ) -> None:
        """Initialize token object."""
        super().__init__()
        self.aperture_identifier = aperture_identifier
        self.x_size = float(x_size)
        self.y_size = float(y_size)
        self.hole_diameter = float(hole_diameter) if hole_diameter is not None else None

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        suffix = ""
        if self.hole_diameter is not None:
            suffix += f"X{self.hole_diameter}"
        return f"%AD{self.aperture_identifier}O,{self.x_size}X{self.y_size}{suffix}*%"


class ADDefinePolygon(ADDefineAperture):
    """Wrapper for aperture definition token.

    Defines a polygon.
    """

    def __init__(  # noqa: PLR0913
        self,
        aperture_identifier: str,
        outer_diameter: str,
        number_of_vertices: str,
        rotation: str,
        hole_diameter: str | None = None,
    ) -> None:
        """Initialize token object."""
        super().__init__()
        self.aperture_identifier = aperture_identifier
        self.outer_diameter = float(outer_diameter)
        self.number_of_vertices = int(number_of_vertices)
        self.rotation = float(rotation)
        self.hole_diameter = float(hole_diameter) if hole_diameter is not None else None

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        suffix = ""
        if self.hole_diameter is not None:
            suffix += f"X{self.hole_diameter}"
        return (
            f"%AD{self.aperture_identifier}P,{self.outer_diameter}"
            f"X{self.number_of_vertices}X{self.rotation}{suffix}*%"
        )


class ADDefineMacro(ADDefineAperture):
    """Wrapper for aperture definition token.

    Defines a macro based aperture.
    """

    def __init__(
        self,
        aperture_type: str,
        aperture_identifier: str,
        am_param: list[str],
    ) -> None:
        """Initialize token object."""
        super().__init__()
        self.aperture_type = aperture_type
        self.aperture_identifier = aperture_identifier
        self.am_param = am_param

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return (
            f"%AD{self.aperture_identifier}{self.aperture_type},"
            f"{'X'.join(self.am_param)}"
        )
