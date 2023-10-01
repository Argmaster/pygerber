"""Wrapper for plot operation token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Generator, Iterable, Tuple

from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.state_enums import DrawMode, Polarity
from pygerber.gerberx3.tokenizer.tokens.bases.command import CommandToken
from pygerber.gerberx3.tokenizer.tokens.coordinate import Coordinate, CoordinateType

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class D01Draw(CommandToken):
    """Wrapper for plot operation token.

    Outside a region statement D01 creates a draw or arc object with the current
    aperture. Inside it adds a draw/arc segment to the contour under construction. The
    current point is moved to draw/arc end point after the creation of the draw/arc.

    See section 4.7 of The Gerber Layer Format Specification Revision 2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html
    """

    def __init__(
        self,
        string: str,
        location: int,
        x: Coordinate,
        y: Coordinate,
        i: Coordinate,
        j: Coordinate,
    ) -> None:
        super().__init__(string, location)
        self.x = x
        self.y = y
        self.i = i
        self.j = j

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        x = tokens.get("x")
        x = Coordinate.new(
            coordinate_type=CoordinateType.X,
            offset=str(x) if x is not None else None,
        )
        y = tokens.get("y")
        y = Coordinate.new(
            coordinate_type=CoordinateType.Y,
            offset=str(y) if y is not None else None,
        )
        i = tokens.get("i")
        i = Coordinate.new(
            coordinate_type=CoordinateType.I,
            offset=str(i) if i is not None else None,
        )
        j = tokens.get("j")
        j = Coordinate.new(
            coordinate_type=CoordinateType.J,
            offset=str(j) if j is not None else None,
        )

        return cls(
            string=string,
            location=location,
            x=x,
            y=y,
            i=i,
            j=j,
        )

    def update_drawing_state(
        self,
        state: State,
        backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set coordinate parser."""
        x = state.parse_coordinate(self.x)
        y = state.parse_coordinate(self.y)

        end_position = Vector2D(x=x, y=y)
        start_position = state.current_position

        draw_commands: list[DrawCommand] = []

        if state.is_region:
            polarity = state.polarity.to_region_variant()
        else:
            polarity = state.polarity

        if not state.is_region or backend.options.draw_region_outlines:
            draw_commands.extend(
                self._create_draw_commands(
                    state,
                    backend,
                    end_position,
                    start_position,
                    polarity,
                ),
            )

        if state.is_region:
            self._create_region_points(
                state,
                backend,
                end_position,
                start_position,
                polarity,
            )

        return (
            state.model_copy(
                update={
                    "current_position": end_position,
                },
            ),
            draw_commands,
        )

    def _create_region_points(
        self,
        state: State,
        backend: Backend,
        end_position: Vector2D,
        start_position: Vector2D,
        polarity: Polarity,
    ) -> None:
        if state.draw_mode == DrawMode.Linear:
            state.region_boundary_points.append(start_position)
            state.region_boundary_points.append(end_position)

        elif state.draw_mode in (
            DrawMode.ClockwiseCircular,
            DrawMode.CounterclockwiseCircular,
        ):
            i = state.parse_coordinate(self.i)
            j = state.parse_coordinate(self.j)

            center_offset = Vector2D(x=i, y=j)

            state.region_boundary_points.extend(
                backend.get_draw_arc_cls()(
                    backend=backend,
                    polarity=polarity,
                    start_position=start_position,
                    dx_dy_center=center_offset,
                    end_position=end_position,
                    width=Offset.NULL,
                    is_clockwise=(state.draw_mode == DrawMode.ClockwiseCircular),
                    # Will require tweaking if support for single quadrant mode
                    # will be desired.
                    is_multi_quadrant=True,
                ).calculate_arc_points(),
            )

        else:
            raise NotImplementedError(state.draw_mode)

    def _create_draw_commands(
        self,
        state: State,
        backend: Backend,
        end_position: Vector2D,
        start_position: Vector2D,
        polarity: Polarity,
    ) -> Generator[DrawCommand, None, None]:
        current_aperture = backend.get_private_aperture_handle(
            state.get_current_aperture(),
        )
        yield backend.get_draw_paste_cls()(
            backend=backend,
            polarity=polarity,
            center_position=start_position,
            other=current_aperture.drawing_target,
        )

        if state.draw_mode == DrawMode.Linear:
            if not state.is_region or backend.options.draw_region_outlines:
                yield backend.get_draw_vector_line_cls()(
                    backend=backend,
                    polarity=polarity,
                    start_position=start_position,
                    end_position=end_position,
                    width=current_aperture.get_line_width(),
                )

        elif state.draw_mode in (
            DrawMode.ClockwiseCircular,
            DrawMode.CounterclockwiseCircular,
        ):
            i = state.parse_coordinate(self.i)
            j = state.parse_coordinate(self.j)

            center_offset = Vector2D(x=i, y=j)
            if not state.is_region or backend.options.draw_region_outlines:
                yield backend.get_draw_arc_cls()(
                    backend=backend,
                    polarity=polarity,
                    start_position=start_position,
                    dx_dy_center=center_offset,
                    end_position=end_position,
                    width=current_aperture.get_line_width(),
                    is_clockwise=(state.draw_mode == DrawMode.ClockwiseCircular),
                    # Will require tweaking if support for single quadrant mode
                    # will be desired.
                    is_multi_quadrant=True,
                )

        else:
            raise NotImplementedError(state.draw_mode)

        yield backend.get_draw_paste_cls()(
            backend=backend,
            polarity=polarity,
            center_position=end_position,
            other=current_aperture.drawing_target,
        )

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",
    ) -> str:
        """Get gerber code represented by this token."""
        return (
            f"{indent}"
            f"{self.x.get_gerber_code(indent, endline)}"
            f"{self.y.get_gerber_code(indent, endline)}"
            f"{self.i.get_gerber_code(indent, endline)}"
            f"{self.j.get_gerber_code(indent, endline)}"
            "D01"
        )
