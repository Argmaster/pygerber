"""Wrapper for plot operation token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable, Tuple

from pygerber.backend.abstract.vector_2d import Vector2D
from pygerber.gerberx3.state_enums import DrawMode
from pygerber.gerberx3.tokenizer.tokens.coordinate import Coordinate, CoordinateType
from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_actions.draw_action import DrawAction
    from pygerber.gerberx3.parser.state import State


class Draw(Token):
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
    ) -> Tuple[State, Iterable[DrawAction]]:
        """Set coordinate parser."""
        x = state.parse_coordinate(self.x)
        y = state.parse_coordinate(self.y)

        end_position = Vector2D(x=x, y=y)
        start_position = state.current_position

        draw_action: DrawAction

        if state.draw_mode == DrawMode.Linear:
            draw_action = backend.get_draw_action_line_cls()(
                state.get_current_aperture(),
                backend,
                state.polarity,
                start_position,
                end_position,
            )

        elif state.draw_mode in (
            DrawMode.ClockwiseCircular,
            DrawMode.CounterclockwiseCircular,
        ):
            i = state.parse_coordinate(self.i)
            j = state.parse_coordinate(self.j)

            center_offset = Vector2D(x=i, y=j)

            draw_action = backend.get_draw_action_arc_cls()(
                state.get_current_aperture(),
                backend,
                state.polarity,
                start_position,
                center_offset,
                end_position,
                is_clockwise=(state.draw_mode == DrawMode.ClockwiseCircular),
                # Will require tweaking if support for single quadrant mode
                # will be desired.
                is_multi_quadrant=True,
            )

        else:
            raise NotImplementedError(state.draw_mode)

        return (
            state.model_copy(
                update={
                    "current_position": end_position,
                },
                deep=True,
            ),
            (draw_action,),
        )

    def __str__(self) -> str:
        return f"{self.x}{self.y}{self.i}{self.j}D01*"
