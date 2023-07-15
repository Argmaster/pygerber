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

from typing import TYPE_CHECKING, Any, List, Optional

from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self


class DefineAperture(Token):
    """Wrapper for aperture definition token.

    Defines a template-based aperture, assigns a D code to it. This class is never used
    to create objects, only its subclasses are used.
    """

    @classmethod
    def new(
        cls,
        _string: str,
        _location: int,
        tokens: ParseResults,
    ) -> DefineAperture:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        aperture_type = tokens.pop("aperture_type")
        if not isinstance(aperture_type, str):
            msg = "Expected aperture type to be string."
            raise TypeError(msg)

        if aperture_type == "C":
            return DefineCircle.from_tokens(**tokens.as_dict())

        if aperture_type == "R":
            return DefineRectangle.from_tokens(**tokens.as_dict())

        if aperture_type == "O":
            return DefineObround.from_tokens(**tokens.as_dict())

        if aperture_type == "P":
            return DefinePolygon.from_tokens(**tokens.as_dict())

        return DefineMacro.from_tokens(aperture_type=aperture_type, **tokens.as_dict())

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return "<ADDefineAperture-INVALID>"


class DefineCircle(DefineAperture):
    """Wrapper for aperture definition token.

    Defines a circle.
    """

    aperture_identifier: str
    diameter: float
    hole_diameter: Optional[float]

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        aperture_identifier: str = tokens["aperture_identifier"]
        diameter: float = float(tokens["diameter"])
        hole_diameter: Optional[float] = (
            float(tokens["hole_diameter"])
            if tokens.get("hole_diameter") is not None
            else None
        )
        return cls(
            aperture_identifier=aperture_identifier,
            diameter=diameter,
            hole_diameter=hole_diameter,
        )

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        suffix = ""
        if self.hole_diameter is not None:
            suffix += f"X{self.hole_diameter}"
        return f"%AD{self.aperture_identifier}C,{self.diameter}{suffix}*%"


class DefineRectangle(DefineAperture):
    """Wrapper for aperture definition token.

    Defines a rectangle
    """

    aperture_identifier: str
    x_size: float
    y_size: float
    hole_diameter: Optional[float]

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        aperture_identifier: str = tokens["aperture_identifier"]
        x_size: float = float(tokens["x_size"])
        y_size: float = float(tokens["y_size"])
        hole_diameter: Optional[float] = (
            float(tokens["hole_diameter"])
            if tokens.get("hole_diameter") is not None
            else None
        )
        return cls(
            aperture_identifier=aperture_identifier,
            x_size=x_size,
            y_size=y_size,
            hole_diameter=hole_diameter,
        )

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        suffix = ""
        if self.hole_diameter is not None:
            suffix += f"X{self.hole_diameter}"
        return f"%AD{self.aperture_identifier}R,{self.x_size}X{self.y_size}{suffix}*%"


class DefineObround(DefineAperture):
    """Wrapper for aperture definition token.

    Defines a obround.
    """

    aperture_identifier: str
    x_size: float
    y_size: float
    hole_diameter: Optional[float]

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        aperture_identifier: str = tokens["aperture_identifier"]
        x_size: float = float(tokens["x_size"])
        y_size: float = float(tokens["y_size"])
        hole_diameter: Optional[float] = (
            float(tokens["hole_diameter"])
            if tokens.get("hole_diameter") is not None
            else None
        )
        return cls(
            aperture_identifier=aperture_identifier,
            x_size=x_size,
            y_size=y_size,
            hole_diameter=hole_diameter,
        )

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        suffix = ""
        if self.hole_diameter is not None:
            suffix += f"X{self.hole_diameter}"
        return f"%AD{self.aperture_identifier}O,{self.x_size}X{self.y_size}{suffix}*%"


class DefinePolygon(DefineAperture):
    """Wrapper for aperture definition token.

    Defines a polygon.
    """

    aperture_identifier: str
    outer_diameter: float
    number_of_vertices: int
    rotation: Optional[float]
    hole_diameter: Optional[float]

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        aperture_identifier: str = tokens["aperture_identifier"]
        outer_diameter: float = float(tokens["outer_diameter"])
        number_of_vertices: int = int(tokens["number_of_vertices"])
        rotation: Optional[float] = (
            float(tokens["rotation"]) if tokens.get("rotation") is not None else None
        )
        hole_diameter: Optional[float] = (
            float(tokens["hole_diameter"])
            if tokens.get("hole_diameter") is not None
            else None
        )
        return cls(
            aperture_identifier=aperture_identifier,
            outer_diameter=outer_diameter,
            number_of_vertices=number_of_vertices,
            rotation=rotation,
            hole_diameter=hole_diameter,
        )

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        suffix = ""
        if self.hole_diameter is not None:
            suffix += f"X{self.hole_diameter}"
        return (
            f"%AD{self.aperture_identifier}P,{self.outer_diameter}"
            f"X{self.number_of_vertices}X{self.rotation}{suffix}*%"
        )


class DefineMacro(DefineAperture):
    """Wrapper for aperture definition token.

    Defines a macro based aperture.
    """

    aperture_type: str
    aperture_identifier: str
    am_param: List[str]

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        aperture_type: str = tokens["aperture_type"]
        aperture_identifier: str = tokens["aperture_identifier"]
        am_param: list[str] = tokens.get("am_param", [])
        return cls(
            aperture_type=aperture_type,
            aperture_identifier=aperture_identifier,
            am_param=am_param,
        )

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return (
            f"%AD{self.aperture_identifier}{self.aperture_type},"
            f"{'X'.join(self.am_param)}"
        )
