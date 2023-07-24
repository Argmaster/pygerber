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

        xy_position = Vector2D(x=x, y=y)
        start_position = state.current_position

        if state.draw_mode == DrawMode.Linear:
            draw_action = backend.get_draw_action_line_cls()(
                state.get_current_aperture(),
                backend,
                state.polarity,
                start_position,
                xy_position,
            )
        else:
            raise NotImplementedError

        return (
            state.model_copy(
                update={
                    "current_position": xy_position,
                },
                deep=True,
            ),
            (draw_action,),
        )

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"{self.x}{self.y}{self.i}{self.j}D01*"
