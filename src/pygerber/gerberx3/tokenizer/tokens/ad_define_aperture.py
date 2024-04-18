"""AD Command logic.

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
from pygerber.gerberx3.tokenizer.tokens.bases.extended_command import (
    ExtendedCommandToken,
)
from pygerber.gerberx3.tokenizer.tokens.dnn_select_aperture import ApertureID

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.gerberx3.parser.state import State
    from pygerber.gerberx3.parser2.context2 import Parser2Context


class DefineAperture(ExtendedCommandToken):
    """## 4.3.1 AD Command.

    The AD command creates an aperture, attaches the aperture attributes at that moment in the
    attribute dictionary to it and adds it to the apertures dictionary.

    ```ebnf
    AD = '%' ('AD' aperture_ident template_call) '*%';
    template_call = template_name [',' parameter {'X' parameter}*];
    ```

    The AD command must precede the first use of the aperture. It is recommended to put all AD
    commands in the file header.

    ---

    ## Example

    ```gerber
    %ADD10C,.025*%
    %ADD10C,0.5X0.25*%
    ```

    ---

    See section 4.3 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=48)

    """  # noqa: E501


class DefineCircle(DefineAperture):
    """## 4.3.1 AD Command.

    The AD command creates an aperture, attaches the aperture attributes at that moment in the
    attribute dictionary to it and adds it to the apertures dictionary.

    ```ebnf
    AD = '%' ('AD' aperture_ident template_call) '*%';
    template_call = template_name [',' parameter {'X' parameter}*];
    ```

    The AD command must precede the first use of the aperture. It is recommended to put all AD
    commands in the file header.

    ---

    ## Example

    ```gerber
    %ADD10C,.025*%
    %ADD10C,0.5X0.25*%
    ```

    ---

    See section 4.3 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=48)

    ---

    ## 4.4.2 Circle

    The syntax of the circle standard template call is:

    ```ebnf
    template_call = 'C' ',' diameter 'X' hole_diameter
    ```

    - `C` - Indicates the circle aperture template.
    - `diameter` - Diameter. A decimal ≥0.
    - `hole_diameter` - Diameter of a round hole. A decimal >0. If omitted the aperture is solid. See also section [4.4.6](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=55).

    ---

    See section 4.4.2 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=50)

    """  # noqa: E501

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

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().define_circle_aperture.pre_parser_visit_token(self, context)
        context.get_hooks().define_aperture.pre_parser_visit_token(self, context)

        context.get_hooks().define_circle_aperture.on_parser_visit_token(self, context)
        context.get_hooks().define_aperture.on_parser_visit_token(self, context)

        context.get_hooks().define_circle_aperture.post_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().define_aperture.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",
    ) -> str:
        """Get gerber code represented by this token."""
        suffix = ""
        if self.hole_diameter is not None:
            suffix += f"X{self.hole_diameter}"
        return (
            f"AD{self.aperture_id.get_gerber_code(indent, endline)}C,"
            f"{self.diameter}{suffix}"
        )


class DefineRectangle(DefineAperture):
    """## 4.3.1 AD Command.

    The AD command creates an aperture, attaches the aperture attributes at that moment in the
    attribute dictionary to it and adds it to the apertures dictionary.

    ```ebnf
    AD = '%' ('AD' aperture_ident template_call) '*%';
    template_call = template_name [',' parameter {'X' parameter}*];
    ```

    The AD command must precede the first use of the aperture. It is recommended to put all AD
    commands in the file header.

    ---

    ### Example:

    ```gerber
    %ADD22R,0.044X0.025*%
    %ADD23R,0.044X0.025X0.019*%
    ```

    ---

    See section 4.3 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=48)

    ---

    ## 4.4.3 Rectangle

    The syntax of the rectangle or square standard template call is:

    ```ebnf
    template_call = 'R' ',' x_size 'X' y_size 'X' hole_diameter
    ```

    - `T` - Indicates the rectangle aperture template.
    - `x_size`, `x_size` - X and Y sizes of the rectangle. Decimals >0. If x_size = y_size the effective shape is a square
    - `hole_diameter` - Diameter of a round hole. A decimal >0. If omitted the aperture is solid. See also section [4.4.6](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=55).

    ---

    See section 4.4.3 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=52)

    """  # noqa: E501

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

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().define_rectangle_aperture.pre_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().define_aperture.pre_parser_visit_token(self, context)

        context.get_hooks().define_rectangle_aperture.on_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().define_aperture.on_parser_visit_token(self, context)

        context.get_hooks().define_rectangle_aperture.post_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().define_aperture.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",
    ) -> str:
        """Get gerber code represented by this token."""
        suffix = ""
        if self.hole_diameter is not None:
            suffix += f"X{self.hole_diameter}"
        return (
            f"AD{self.aperture_id.get_gerber_code(indent, endline)}R,"
            f"{self.x_size}X{self.y_size}{suffix}"
        )


class DefineObround(DefineAperture):
    """## 4.3.1 AD Command.

    The AD command creates an aperture, attaches the aperture attributes at that moment in the
    attribute dictionary to it and adds it to the apertures dictionary.

    ```ebnf
    AD = '%' ('AD' aperture_ident template_call) '*%';
    template_call = template_name [',' parameter {'X' parameter}*];
    ```

    The AD command must precede the first use of the aperture. It is recommended to put all AD
    commands in the file header.

    ---

    ### Example:

    ```gerber
    %ADD22O,0.046X0.026*%
    %ADD22O,0.046X0.026X0.019*%
    ```

    ---

    See section 4.3 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=48)

    ---

    ## 4.4.4 Obround

    Obround (oval) is a rectangle where the smallest side is rounded to a half-circle. The syntax is:

    ```ebnf
    template_call = 'O' ',' x_size 'X' y_size 'X' hole_diameter
    ```

    - `O` - Indicates the obround aperture template.
    - `x_size`, `x_size` - X and Y sizes of enclosing box. Decimals >0. If x_size = y_size the effective shape is a circle.
    - `hole_diameter` - Diameter of a round hole. A decimal >0. If omitted the aperture is solid. See also section [4.4.6](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=55).

    ---

    See section 4.4.4 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=53)

    """  # noqa: E501

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

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().define_obround_aperture.pre_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().define_aperture.pre_parser_visit_token(self, context)

        context.get_hooks().define_obround_aperture.on_parser_visit_token(self, context)
        context.get_hooks().define_aperture.on_parser_visit_token(self, context)

        context.get_hooks().define_obround_aperture.post_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().define_aperture.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",
    ) -> str:
        """Get gerber code represented by this token."""
        suffix = ""
        if self.hole_diameter is not None:
            suffix += f"X{self.hole_diameter}"
        return (
            f"AD{self.aperture_id.get_gerber_code(indent, endline)}O,"
            f"{self.x_size}X{self.y_size}{suffix}"
        )


class DefinePolygon(DefineAperture):
    """## 4.3.1 AD Command.

    The AD command creates an aperture, attaches the aperture attributes at that moment in the
    attribute dictionary to it and adds it to the apertures dictionary.

    ```ebnf
    AD = '%' ('AD' aperture_ident template_call) '*%';
    template_call = template_name [',' parameter {'X' parameter}*];
    ```

    The AD command must precede the first use of the aperture. It is recommended to put all AD
    commands in the file header.

    ---

    ### Example:

    ```gerber
    %ADD17P,.040X6*%
    %ADD17P,.040X6X0.0X0.019*%
    ```

    ---

    See section 4.3 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=48)

    ---

    ## 4.4.5 Polygon

    Creates a regular polygon aperture. The syntax of the polygon template is:

    ```ebnf
    template_call = 'P' ',' outer_diameter 'X' vertices 'X' rotation 'X' hole_diameter
    ```

    - `P` - Indicates the polygon aperture template.
    - `outer_diameter` - Diameter of the circle circumscribing the regular polygon, i.e. the circle through the polygon vertices. A decimal > 0.
    - `vertices` - Number of vertices n, 3 ≤ n ≤ 12. An integer.
    - `rotation` - The rotation angle, in degrees counterclockwise. A decimal. With rotation angle zero there is a vertex on the positive X-axis through the aperture center.
    - `hole_diameter` - Diameter of a round hole. A decimal >0. If omitted the aperture is solid. See also section [4.4.6](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=55).

    ---

    See section 4.4.5 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=54)

    """  # noqa: E501

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

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().define_polygon_aperture.pre_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().define_aperture.pre_parser_visit_token(self, context)

        context.get_hooks().define_polygon_aperture.on_parser_visit_token(self, context)
        context.get_hooks().define_aperture.on_parser_visit_token(self, context)

        context.get_hooks().define_polygon_aperture.post_parser_visit_token(
            self,
            context,
        )
        context.get_hooks().define_aperture.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",
    ) -> str:
        """Get gerber code represented by this token."""
        suffix = ""
        if self.hole_diameter is not None:
            suffix += f"X{self.hole_diameter}"
        return (
            f"AD{self.aperture_id.get_gerber_code(indent, endline)}P,"
            f"{self.outer_diameter}X{self.number_of_vertices}X{self.rotation}{suffix}"
        )


class DefineMacro(DefineAperture):
    """## 4.3.1 AD Command.

    The AD command creates an aperture, attaches the aperture attributes at that moment in the
    attribute dictionary to it and adds it to the apertures dictionary.

    ```ebnf
    AD = '%' ('AD' aperture_ident template_call) '*%';
    template_call = template_name [',' parameter {'X' parameter}*];
    ```

    The AD command must precede the first use of the aperture. It is recommended to put all AD
    commands in the file header.

    ---

    ## Example

    ```gerber
    %ADD10C,.025*%
    %ADD10C,0.5X0.25*%
    ```

    ---

    See section 4.3 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=48)

    ---

    ## 4.5 Aperture Macro (AM)

    The AM command creates a macro aperture template and adds it to the aperture template
    dictionary (see 2.2). A template is a parametrized shape. The AD command instantiates a
    template into an aperture by supplying values to the template parameters.

    Templates of any shape or parametrization can be created. Multiple simple shapes called
    primitives can be combined in a single template. An aperture macro can contain variables
    whose actual values are defined by:

    - Values provided by the AD command,
    - Arithmetic expressions with other variables.

    The template is created by positioning primitives in a coordinate space. The origin of that
    coordinate space will be the origin of all apertures created with the state.

    A template must be defined before the first AD that refers to it. The AM command can be used
    multiple times in a file.

    Attributes are not attached to templates. They are attached to the aperture at the time of its
    creation with the AD command.

    An AM command contains the following words:

    - The AM declaration with the macro name
    - Primitives with their comma-separated parameters
    - Macro variables, defined by an arithmetic expression

    ```ebnf
    AM = '%' ('AM' macro_name macro_body) '%';
    macro_name = name '*';
    macro_body = {in_macro_block}+;
    in_macro_block =
    |primitive
    |variable_definition
    ;
    variable_definition = (macro_variable '=' expression) '*';
    macro_variable = '$' positive_integer;
    primitive = primitive_code {',' par}*
    par = ',' (expression);
    ```

    ---

    See section 4.5 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=56)

    """  # noqa: E501

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

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().define_macro_aperture.pre_parser_visit_token(self, context)
        context.get_hooks().define_aperture.pre_parser_visit_token(self, context)

        context.get_hooks().define_macro_aperture.on_parser_visit_token(self, context)
        context.get_hooks().define_aperture.on_parser_visit_token(self, context)

        context.get_hooks().define_macro_aperture.post_parser_visit_token(self, context)
        context.get_hooks().define_aperture.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",
    ) -> str:
        """Get gerber code represented by this token."""
        return (
            f"AD{self.aperture_id.get_gerber_code(indent, endline)}"
            f"{self.aperture_type},{'X'.join(self.am_param)}"
        )
