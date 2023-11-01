"""Wrapper for move operation token."""
from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Tuple

from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.tokenizer.tokens.bases.command import CommandToken
from pygerber.gerberx3.tokenizer.tokens.coordinate import Coordinate, CoordinateType

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.language_server._internals.state import LanguageServerState
    from pygerber.gerberx3.parser.state import State


class D02Move(CommandToken):
    """## 4.8.3 Move (D02).

    Moves the current point to the (X,Y) in the comment. The syntax is:

    ```ebnf
    D02 = (['X' x_coordinate] ['Y' y_coordinate] 'D02') '*';
    ```

    - x_coordinate - `<Coordinate>` is coordinate data - see section 0. It defines the X
        coordinate of the new current point. The default is the X coordinate of
        the old current point.
    - y_coordinate - As above, but for the Y coordinate.
    - D02 - Move operation code

    ---

    ## Example

    ```gerber
    X2152000Y1215000D02*
    ```

    ---

    See section 4.8.3 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=83)

    """

    def __init__(
        self,
        string: str,
        location: int,
        x: Coordinate,
        y: Coordinate,
    ) -> None:
        super().__init__(string, location)
        self.x = x
        self.y = y

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

        return cls(
            string=string,
            location=location,
            x=x,
            y=y,
        )

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
            "D02"
        )

    def get_operation_specific_info(
        self,
        state: LanguageServerState,
    ) -> str:
        """Return operation specific extra information about token."""
        file_state = state.get_by_file_content(self.string)
        _, parser_state = file_state.parse_until(lambda t, _s: t == self)

        units = parser_state.get_units()

        x0 = parser_state.current_position.x.as_unit(units)
        y0 = parser_state.current_position.x.as_unit(units)

        x1 = parser_state.parse_coordinate(self.x).as_unit(units)
        y1 = parser_state.parse_coordinate(self.y).as_unit(units)

        u = units.value.lower()

        return f"Move from (`{x0}`{u}, `{y0}`{u}) to (`{x1}`{u}, `{y1}`{u})"
