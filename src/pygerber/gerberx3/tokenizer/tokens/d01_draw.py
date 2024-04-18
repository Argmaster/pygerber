"""Plot (D01) logic."""

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
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class D01Draw(CommandToken):
    """## 4.8.2 Plot (D01).

    Performs a plotting operation, creating a draw or an arc segment. The plot state defines which
    type of segment is created, see 4.7. The syntax depends on the required parameters, and,
    hence, on the plot state.

    D01 creates a linear or circular line segment by plotting from the current point to the
    coordinate pair in the command. Outside a region statement (see 2.3.2) these segments
    are converted to draw or arc objects by stroking them with the current aperture (see 2.3.1).
    Within a region statement these segments form a contour defining a region (see 4.10). The
    effect of D01, e.g. whether a straight or circular segment is created, depends on the
    graphics state (see 2.3.2).

    ### Syntax

    For linear (G01):

    ```ebnf
    D01 = (['X' x_coordinate] ['Y' y_coordinate] 'D01') '*';
    ```

    For Circular (G02|G03)

    ```ebnf
    D01 = (['X' x_coordinate] ['Y' y_coordinate] 'I' x_offset 'J' y-offset ) 'D01' '*';
    ```

    - x_coordinate - `<Coordinate>` is coordinate data - see section 0. It defines the X coordinate of the
        new current point. The default is the X coordinate of the old current point.

    ---

    ## Example

    ```gerber
    X275000Y115000D02*
    G01*
    X2512000Y115000D01*
    G75*
    G03*
    X5005000Y3506000I3000J0D01*
    G01*
    X15752000D01*
    Y12221000D01*
    ```

    ---

    See section 4.8.2 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=83)

    """  # noqa: E501

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

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().command_draw.pre_parser_visit_token(self, context)
        context.get_hooks().command_draw.on_parser_visit_token(self, context)
        context.get_hooks().command_draw.post_parser_visit_token(self, context)

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

    def get_state_based_hover_message(
        self,
        state: State,
    ) -> str:
        """Return operation specific extra information about token."""
        units = state.get_units()

        x0 = state.current_position.x.as_unit(units)
        y0 = state.current_position.x.as_unit(units)

        x1 = state.parse_coordinate(self.x).as_unit(units)
        y1 = state.parse_coordinate(self.y).as_unit(units)

        draw_mode = state.draw_mode.to_human_readable()

        aperture = state.get_current_aperture().aperture_id

        u = units.value.lower()
        d = state.draw_mode.value

        return (
            f"Draw {draw_mode} (`{d}`) from (`{x0}`{u}, `{y0}`{u}) to "
            f"(`{x1}`{u}, `{y1}`{u}) with aperture `{aperture}`"
        )
