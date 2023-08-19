"""Wrapper for flash operation token."""
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


class D03Flash(Token):
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
    ) -> Tuple[State, Iterable[DrawCommand]]:
        """Set coordinate parser."""
        x = state.parse_coordinate(self.x)
        y = state.parse_coordinate(self.y)

        position = Vector2D(x=x, y=y)
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
                center_position=position,
                other=current_aperture.drawing_target,
            ),
        )

        return (
            state.model_copy(
                update={
                    "current_position": position,
                },
            ),
            draw_commands,
        )

    def __str__(self) -> str:
        return f"{self.x}{self.y}D03*"
