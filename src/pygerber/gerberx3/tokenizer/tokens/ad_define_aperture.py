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
convey the meta information. Certainly do not abuse a zero-size object to indicate the
absence of an object, e.g. by flashing a zero-size aperture to indicate the absence of
a pad. This is just confusing. If there is nothing, put nothing.
"""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Iterable, List, Optional, Tuple

from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.state_enums import Polarity
from pygerber.gerberx3.tokenizer.tokens.dnn_select_aperture import ApertureID
from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class DefineAperture(Token):
    """Wrapper for aperture definition token.

    Defines a template-based aperture, assigns a D code to it. This class is never used
    to create objects, only its subclasses are used.

    See section 4.3 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """


class DefineCircle(DefineAperture):
    """Wrapper for aperture definition token.

    Defines a circle.
    """

    def __init__(
        self,
        string: str,
        location: int,
        aperture_id: ApertureID,
        diameter: Decimal,
        hole_diameter: Optional[Decimal],
    ) -> None:
        super().__init__(string, location)
        self.aperture_id = aperture_id
        self.diameter = diameter
        self.hole_diameter = hole_diameter

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        aperture_id = ApertureID(tokens["aperture_identifier"])
        diameter: Decimal = Decimal(str(tokens["diameter"]))
        hole_diameter: Optional[Decimal] = (
            Decimal(str(tokens["hole_diameter"]))
            if tokens.get("hole_diameter") is not None
            else None
        )
        return cls(
            string=string,
            location=location,
            aperture_id=aperture_id,
            diameter=diameter,
            hole_diameter=hole_diameter,
        )

    def update_drawing_state(
        self,
        state: State,
        backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Update drawing state."""
        handle = backend.create_aperture_handle(self.aperture_id)
        with handle:
            handle.add_draw(
                backend.get_draw_circle_cls()(
                    backend=backend,
                    diameter=Offset.new(self.diameter, state.get_units()),
                    polarity=Polarity.Dark,
                    center_position=Vector2D(x=Offset.NULL, y=Offset.NULL),
                ),
            )
            if self.hole_diameter is not None:
                handle.add_draw(
                    backend.get_draw_circle_cls()(
                        backend=backend,
                        diameter=Offset.new(self.hole_diameter, state.get_units()),
                        polarity=Polarity.Clear,
                        center_position=Vector2D(x=Offset.NULL, y=Offset.NULL),
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
            ),
            (),
        )

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        suffix = ""
        if self.hole_diameter is not None:
            suffix += f"X{self.hole_diameter}"
        return (
            f"{indent}%AD{self.aperture_id.get_gerber_code()}C,"
            f"{self.diameter}{suffix}*%"
        )


class DefineRectangle(DefineAperture):
    """Wrapper for aperture definition token.

    Defines a rectangle
    """

    def __init__(
        self,
        string: str,
        location: int,
        aperture_id: ApertureID,
        x_size: Decimal,
        y_size: Decimal,
        hole_diameter: Optional[Decimal],
    ) -> None:
        super().__init__(string, location)
        self.aperture_id = aperture_id
        self.x_size = x_size
        self.y_size = y_size
        self.hole_diameter = hole_diameter

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        aperture_id = ApertureID(tokens["aperture_identifier"])
        x_size: Decimal = Decimal(str(tokens["x_size"]))
        y_size: Decimal = Decimal(str(tokens["y_size"]))
        hole_diameter: Optional[Decimal] = (
            Decimal(str(tokens["hole_diameter"]))
            if tokens.get("hole_diameter") is not None
            else None
        )
        return cls(
            string=string,
            location=location,
            aperture_id=aperture_id,
            x_size=x_size,
            y_size=y_size,
            hole_diameter=hole_diameter,
        )

    def update_drawing_state(
        self,
        state: State,
        backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Update drawing state."""
        handle = backend.create_aperture_handle(self.aperture_id)
        with handle:
            handle.add_draw(
                backend.get_draw_rectangle_cls()(
                    backend=backend,
                    x_size=Offset.new(self.x_size, state.get_units()),
                    y_size=Offset.new(self.y_size, state.get_units()),
                    polarity=Polarity.Dark,
                    center_position=Vector2D(x=Offset.NULL, y=Offset.NULL),
                ),
            )
            if self.hole_diameter is not None:
                handle.add_draw(
                    backend.get_draw_circle_cls()(
                        backend=backend,
                        diameter=Offset.new(self.hole_diameter, state.get_units()),
                        polarity=Polarity.Clear,
                        center_position=Vector2D(x=Offset.NULL, y=Offset.NULL),
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
            ),
            (),
        )

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        suffix = ""
        if self.hole_diameter is not None:
            suffix += f"X{self.hole_diameter}"
        return (
            f"{indent}%AD{self.aperture_id.get_gerber_code()}R,"
            f"{self.x_size}X{self.y_size}{suffix}*%"
        )


class DefineObround(DefineAperture):
    """Wrapper for aperture definition token.

    Defines an obround.
    """

    def __init__(
        self,
        string: str,
        location: int,
        aperture_id: ApertureID,
        x_size: Decimal,
        y_size: Decimal,
        hole_diameter: Optional[Decimal],
    ) -> None:
        super().__init__(string, location)
        self.aperture_id = aperture_id
        self.x_size = x_size
        self.y_size = y_size
        self.hole_diameter = hole_diameter

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        aperture_id = ApertureID(tokens["aperture_identifier"])
        x_size: Decimal = Decimal(str(tokens["x_size"]))
        y_size: Decimal = Decimal(str(tokens["y_size"]))
        hole_diameter: Optional[Decimal] = (
            Decimal(str(tokens["hole_diameter"]))
            if tokens.get("hole_diameter") is not None
            else None
        )
        return cls(
            string=string,
            location=location,
            aperture_id=aperture_id,
            x_size=x_size,
            y_size=y_size,
            hole_diameter=hole_diameter,
        )

    def update_drawing_state(
        self,
        state: State,
        backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Update drawing state."""
        handle = backend.create_aperture_handle(self.aperture_id)

        x_size = Offset.new(self.x_size, state.get_units())
        y_size = Offset.new(self.y_size, state.get_units())

        if self.x_size < self.y_size:
            # Obround is thin and tall.
            circle_diameter = x_size

            middle_rectangle_x = x_size
            middle_rectangle_y = y_size - x_size

            circle_positive = Vector2D(x=Offset.NULL, y=middle_rectangle_y / 2)
            circle_negative = Vector2D(x=Offset.NULL, y=-middle_rectangle_y / 2)

        else:
            # Obround is wide and short.
            circle_diameter = y_size

            middle_rectangle_x = x_size - y_size
            middle_rectangle_y = y_size

            circle_positive = Vector2D(x=middle_rectangle_x / 2, y=Offset.NULL)
            circle_negative = Vector2D(x=-middle_rectangle_x / 2, y=Offset.NULL)

        with handle:
            handle.add_draw(
                backend.get_draw_rectangle_cls()(
                    backend=backend,
                    x_size=middle_rectangle_x,
                    y_size=middle_rectangle_y,
                    polarity=Polarity.Dark,
                    center_position=Vector2D(x=Offset.NULL, y=Offset.NULL),
                ),
            )
            handle.add_draw(
                backend.get_draw_circle_cls()(
                    backend=backend,
                    diameter=circle_diameter,
                    polarity=Polarity.Dark,
                    center_position=circle_positive,
                ),
            )
            handle.add_draw(
                backend.get_draw_circle_cls()(
                    backend=backend,
                    diameter=circle_diameter,
                    polarity=Polarity.Dark,
                    center_position=circle_negative,
                ),
            )
            if self.hole_diameter is not None:
                handle.add_draw(
                    backend.get_draw_circle_cls()(
                        backend=backend,
                        diameter=Offset.new(self.hole_diameter, state.get_units()),
                        polarity=Polarity.Clear,
                        center_position=Vector2D(x=Offset.NULL, y=Offset.NULL),
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
            ),
            (),
        )

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        suffix = ""
        if self.hole_diameter is not None:
            suffix += f"X{self.hole_diameter}"
        return (
            f"{indent}%AD{self.aperture_id.get_gerber_code()}O,"
            f"{self.x_size}X{self.y_size}{suffix}*%"
        )


class DefinePolygon(DefineAperture):
    """Wrapper for aperture definition token.

    Defines a polygon.
    """

    def __init__(
        self,
        string: str,
        location: int,
        aperture_id: ApertureID,
        outer_diameter: Decimal,
        number_of_vertices: int,
        rotation: Optional[Decimal],
        hole_diameter: Optional[Decimal],
    ) -> None:
        super().__init__(string, location)
        self.aperture_id = aperture_id
        self.outer_diameter = outer_diameter
        self.number_of_vertices = number_of_vertices
        self.rotation = rotation
        self.hole_diameter = hole_diameter

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        aperture_id = ApertureID(tokens["aperture_identifier"])
        outer_diameter: Decimal = Decimal(str(tokens["outer_diameter"]))
        number_of_vertices: int = int(str(tokens["number_of_vertices"]))
        rotation: Optional[Decimal] = (
            Decimal(str(tokens["rotation"]))
            if tokens.get("rotation") is not None
            else None
        )
        hole_diameter: Optional[Decimal] = (
            Decimal(str(tokens["hole_diameter"]))
            if tokens.get("hole_diameter") is not None
            else None
        )
        return cls(
            string=string,
            location=location,
            aperture_id=aperture_id,
            outer_diameter=outer_diameter,
            number_of_vertices=number_of_vertices,
            rotation=rotation,
            hole_diameter=hole_diameter,
        )

    def update_drawing_state(
        self,
        state: State,
        backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Update drawing state."""
        handle = backend.create_aperture_handle(self.aperture_id)
        with handle:
            handle.add_draw(
                backend.get_draw_polygon_cls()(
                    backend=backend,
                    outer_diameter=Offset.new(self.outer_diameter, state.get_units()),
                    number_of_vertices=self.number_of_vertices,
                    rotation=Decimal("0.0") if self.rotation is None else self.rotation,
                    polarity=Polarity.Dark,
                    center_position=Vector2D(x=Offset.NULL, y=Offset.NULL),
                ),
            )
            if self.hole_diameter is not None:
                handle.add_draw(
                    backend.get_draw_circle_cls()(
                        backend=backend,
                        diameter=Offset.new(self.hole_diameter, state.get_units()),
                        polarity=Polarity.Clear,
                        center_position=Vector2D(x=Offset.NULL, y=Offset.NULL),
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
            ),
            (),
        )

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        suffix = ""
        if self.hole_diameter is not None:
            suffix += f"X{self.hole_diameter}"
        return (
            f"{indent}%AD{self.aperture_id.get_gerber_code()}P,{self.outer_diameter}"
            f"X{self.number_of_vertices}X{self.rotation}{suffix}*%"
        )


class DefineMacro(DefineAperture):
    """Wrapper for aperture definition token.

    Defines a macro based aperture.
    """

    def __init__(
        self,
        string: str,
        location: int,
        aperture_type: str,
        aperture_id: ApertureID,
        am_param: List[str],
    ) -> None:
        super().__init__(string, location)
        self.aperture_type = aperture_type
        self.aperture_id = aperture_id
        self.am_param = am_param

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        aperture_type: str = str(tokens["aperture_type"])
        aperture_id = ApertureID(tokens["aperture_identifier"])

        raw_am_param = e if (e := tokens.get("am_param")) is not None else []
        am_param: List[str] = [str(p) for p in raw_am_param]

        return cls(
            string=string,
            location=location,
            aperture_type=aperture_type,
            aperture_id=aperture_id,
            am_param=am_param,
        )

    def update_drawing_state(
        self,
        state: State,
        backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Update drawing state."""
        handle = backend.create_aperture_handle(self.aperture_id)
        with handle:
            macro = state.macros[self.aperture_type]
            parameters = {
                f"${i + 1}": Offset.new(value, state.get_units())
                for i, value in enumerate(self.am_param)
            }
            macro.evaluate(state, handle, parameters)

        frozen_handle = handle.get_public_handle()

        new_aperture_dict = {**state.apertures}
        new_aperture_dict[self.aperture_id] = frozen_handle

        return (
            state.model_copy(
                update={
                    "apertures": new_aperture_dict,
                },
            ),
            (),
        )

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return (
            f"{indent}%AD{self.aperture_id.get_gerber_code()}{self.aperture_type}"
            f",{'X'.join(self.am_param)}*%"
        )
