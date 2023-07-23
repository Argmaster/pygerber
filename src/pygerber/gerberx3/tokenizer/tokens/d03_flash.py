"""Wrapper for flash operation token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable, Tuple

from pygerber.backend.abstract.offset import Offset
from pygerber.backend.abstract.vector_2d import Vector2D
from pygerber.gerberx3.tokenizer.tokens.coordinate import Coordinate, CoordinateType
from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_actions.draw_action import DrawAction
    from pygerber.gerberx3.parser.state import State


class Flash(Token):
    """Wrapper for flash operation token.

    Creates a flash object with the current aperture. The current point is moved to the
    flash point.
    """

    x: Coordinate
    y: Coordinate

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        x = tokens.get("x", "0")
        x = Coordinate.new(coordinate_type=CoordinateType.X, offset=x)
        y = tokens.get("y", "0")
        y = Coordinate.new(coordinate_type=CoordinateType.Y, offset=y)
        return cls(x=x, y=y)

    def update_drawing_state(
        self,
        state: State,
        backend: Backend,
    ) -> Tuple[State, Iterable[DrawAction]]:
        """Set coordinate parser."""
        x = Offset.new(
            state.get_coordinate_parser().parse(self.x),
            unit=state.get_units(),
        )
        y = Offset.new(
            state.get_coordinate_parser().parse(self.y),
            unit=state.get_units(),
        )
        position = Vector2D(x=x, y=y)
        draw_action = backend.get_draw_action_flash_cls()(
            state.get_current_aperture(),
            backend,
            position,
        )

        return (
            state.model_copy(
                update={
                    "current_position": position,
                },
                deep=True,
            ),
            (draw_action,),
        )

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"{self.x}{self.y}D03*"
