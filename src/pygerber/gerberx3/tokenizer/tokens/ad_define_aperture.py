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

from decimal import Decimal
from typing import TYPE_CHECKING, Any, Iterable, List, Optional, Tuple

from pygerber.backend.abstract.offset import Offset
from pygerber.gerberx3.tokenizer.tokens.dnn_select_aperture import ApertureID
from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_actions.draw_action import DrawAction
    from pygerber.gerberx3.parser.state import State


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

    aperture_id: ApertureID
    diameter: Decimal
    hole_diameter: Optional[Decimal]

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        aperture_id = ApertureID(tokens["aperture_identifier"])
        diameter: Decimal = Decimal(tokens["diameter"])
        hole_diameter: Optional[Decimal] = (
            Decimal(tokens["hole_diameter"])
            if tokens.get("hole_diameter") is not None
            else None
        )
        return cls(
            aperture_id=aperture_id,
            diameter=diameter,
            hole_diameter=hole_diameter,
        )

    def update_drawing_state(
        self,
        state: State,
        backend: Backend,
    ) -> Tuple[State, Iterable[DrawAction]]:
        """Update drawing state."""
        handle = backend.create_aperture_handle(self.aperture_id)
        handle.add_draw(
            backend.get_aperture_draw_circle_cls()(
                diameter=Offset.new(self.diameter, state.units),
                polarity=state.polarity,
            ),
        )
        if self.hole_diameter is not None:
            handle.add_draw(
                backend.get_aperture_draw_circle_cls()(
                    diameter=Offset.new(self.hole_diameter, state.units),
                    polarity=state.polarity.invert(),
                ),
            )
        frozen_handle = handle.get_public_handle()

        new_aperture_dict = {**state.apertures}
        new_aperture_dict[self.aperture_id] = frozen_handle

        return (
            state.model_copy(
                update={
                    "apertures": new_aperture_dict,
                },
                deep=True,
            ),
            (),
        )

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        suffix = ""
        if self.hole_diameter is not None:
            suffix += f"X{self.hole_diameter}"
        return f"%AD{self.aperture_id}C,{self.diameter}{suffix}*%"


class DefineRectangle(DefineAperture):
    """Wrapper for aperture definition token.

    Defines a rectangle
    """

    aperture_id: ApertureID
    x_size: Decimal
    y_size: Decimal
    hole_diameter: Optional[Decimal]

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        aperture_id = ApertureID(tokens["aperture_identifier"])
        x_size: Decimal = Decimal(tokens["x_size"])
        y_size: Decimal = Decimal(tokens["y_size"])
        hole_diameter: Optional[Decimal] = (
            Decimal(tokens["hole_diameter"])
            if tokens.get("hole_diameter") is not None
            else None
        )
        return cls(
            aperture_id=aperture_id,
            x_size=x_size,
            y_size=y_size,
            hole_diameter=hole_diameter,
        )

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        suffix = ""
        if self.hole_diameter is not None:
            suffix += f"X{self.hole_diameter}"
        return f"%AD{self.aperture_id}R,{self.x_size}X{self.y_size}{suffix}*%"


class DefineObround(DefineAperture):
    """Wrapper for aperture definition token.

    Defines a obround.
    """

    aperture_id: ApertureID
    x_size: Decimal
    y_size: Decimal
    hole_diameter: Optional[Decimal]

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        aperture_id = ApertureID(tokens["aperture_identifier"])
        x_size: Decimal = Decimal(tokens["x_size"])
        y_size: Decimal = Decimal(tokens["y_size"])
        hole_diameter: Optional[Decimal] = (
            Decimal(tokens["hole_diameter"])
            if tokens.get("hole_diameter") is not None
            else None
        )
        return cls(
            aperture_id=aperture_id,
            x_size=x_size,
            y_size=y_size,
            hole_diameter=hole_diameter,
        )

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        suffix = ""
        if self.hole_diameter is not None:
            suffix += f"X{self.hole_diameter}"
        return f"%AD{self.aperture_id}O,{self.x_size}X{self.y_size}{suffix}*%"


class DefinePolygon(DefineAperture):
    """Wrapper for aperture definition token.

    Defines a polygon.
    """

    aperture_id: ApertureID
    outer_diameter: Decimal
    number_of_vertices: int
    rotation: Optional[Decimal]
    hole_diameter: Optional[Decimal]

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        aperture_id = ApertureID(tokens["aperture_identifier"])
        outer_diameter: Decimal = Decimal(tokens["outer_diameter"])
        number_of_vertices: int = int(tokens["number_of_vertices"])
        rotation: Optional[Decimal] = (
            Decimal(tokens["rotation"]) if tokens.get("rotation") is not None else None
        )
        hole_diameter: Optional[Decimal] = (
            Decimal(tokens["hole_diameter"])
            if tokens.get("hole_diameter") is not None
            else None
        )
        return cls(
            aperture_id=aperture_id,
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
            f"%AD{self.aperture_id}P,{self.outer_diameter}"
            f"X{self.number_of_vertices}X{self.rotation}{suffix}*%"
        )


class DefineMacro(DefineAperture):
    """Wrapper for aperture definition token.

    Defines a macro based aperture.
    """

    aperture_type: str
    aperture_id: ApertureID
    am_param: List[str]

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        aperture_type: str = tokens["aperture_type"]
        aperture_id = ApertureID(tokens["aperture_identifier"])
        am_param: list[str] = tokens.get("am_param", [])
        return cls(
            aperture_type=aperture_type,
            aperture_id=aperture_id,
            am_param=am_param,
        )

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"%AD{self.aperture_id}{self.aperture_type},{'X'.join(self.am_param)}"