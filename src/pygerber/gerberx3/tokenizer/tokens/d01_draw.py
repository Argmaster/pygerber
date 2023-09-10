"""Wrapper for plot operation token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable, Tuple

from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.state_enums import DrawMode
from pygerber.gerberx3.tokenizer.tokens.coordinate import Coordinate, CoordinateType
from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class D01Draw(Token):
    """Wrapper for plot operation token.

    Outside a region statement D01 creates a draw or arc object with the current
    aperture. Inside it adds a draw/arc segment to the contour under construction. The
    current point is moved to draw/arc end point after the creation of the draw/arc.
    """

    x: Coordinate
    y: Coordinate
    i: Coordinate
    j: Coordinate

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        x = tokens.get("x")
        x = Coordinate.new(coordinate_type=CoordinateType.X, offset=x)
        y = tokens.get("y")
        y = Coordinate.new(coordinate_type=CoordinateType.Y, offset=y)
        i = tokens.get("i")
        i = Coordinate.new(coordinate_type=CoordinateType.I, offset=i)
        j = tokens.get("j")
        j = Coordinate.new(coordinate_type=CoordinateType.J, offset=j)
        return cls(x=x, y=y, i=i, j=j)

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
        current_aperture = backend.get_private_aperture_handle(
            state.get_current_aperture(),
        )

        if state.is_region:
            polarity = state.polarity.to_region_variant()
        else:
            polarity = state.polarity

        draw_commands.append(
            backend.get_draw_paste_cls()(
                backend=backend,
                polarity=polarity,
                center_position=start_position,
                other=current_aperture.drawing_target,
            ),
        )

        if state.draw_mode == DrawMode.Linear:
            if state.is_region:
                state.region_boundary_points.append(start_position)
                state.region_boundary_points.append(end_position)

            draw_commands.append(
                backend.get_draw_vector_line_cls()(
                    backend=backend,
                    polarity=polarity,
                    start_position=start_position,
                    end_position=end_position,
                    width=current_aperture.get_line_width(),
                ),
            )

        elif state.draw_mode in (
            DrawMode.ClockwiseCircular,
            DrawMode.CounterclockwiseCircular,
        ):
            i = state.parse_coordinate(self.i)
            j = state.parse_coordinate(self.j)

            center_offset = Vector2D(x=i, y=j)

            if state.is_region:
                state.region_boundary_points.append(start_position)
                # TODO(argmaster.world@gmail.com): Add region boundary points for region
                # https://github.com/Argmaster/pygerber/issues/29
                state.region_boundary_points.append(end_position)

            draw_commands.append(
                backend.get_draw_arc_cls()(
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
                ),
            )

        else:
            raise NotImplementedError(state.draw_mode)

        draw_commands.append(
            backend.get_draw_paste_cls()(
                backend=backend,
                polarity=polarity,
                center_position=end_position,
                other=current_aperture.drawing_target,
            ),
        )

        if not state.is_region or backend.options.draw_region_outlines:
            return (
                state.model_copy(
                    update={
                        "current_position": end_position,
                    },
                ),
                draw_commands,
            )

        return (
            state.model_copy(
                update={
                    "current_position": end_position,
                },
            ),
            (),
        )

    def __str__(self) -> str:
        return f"{self.x}{self.y}{self.i}{self.j}D01*"
