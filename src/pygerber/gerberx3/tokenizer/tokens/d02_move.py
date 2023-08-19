"""Wrapper for move operation token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable, Tuple

from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.tokenizer.tokens.coordinate import Coordinate, CoordinateType
from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State


class D02Move(Token):
    """Wrapper for move operation token.

    D02 moves the current point to the coordinate in the command. No graphical object is
    generated.
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
        _backend: Backend,
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set coordinate parser."""
        x = state.parse_coordinate(self.x)
        y = state.parse_coordinate(self.y)

        position = Vector2D(x=x, y=y)
        return (
            state.model_copy(
                update={
                    "current_position": position,
                },
            ),
            (),
        )

    def __str__(self) -> str:
        return f"{self.x}{self.y}D02*"
