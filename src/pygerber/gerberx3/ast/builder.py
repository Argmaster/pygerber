"""The `builder` module provides a `stable` interface for constructing Gerber code
which can then be dumped using formatter interface to Gerber files.
"""

from __future__ import annotations

from io import StringIO
from typing import TYPE_CHECKING, Iterable, List, Optional, Sequence

from pydantic import BaseModel, Field

from pygerber.gerberx3.ast.nodes import (
    ADC,
    ADO,
    ADP,
    ADR,
    AM,
    D03,
    FS,
    LM,
    LP,
    LR,
    LS,
    M02,
    MO,
    TD,
    ADmacro,
    AMclose,
    AMopen,
    Code1,
    Code4,
    Code5,
    Code7,
    Code20,
    Code21,
    Constant,
    CoordinateX,
    CoordinateY,
    Dnn,
    File,
    Node,
    Point,
    TA_AperFunction,
    TA_DrillTolerance,
    TA_UserName,
)
from pygerber.gerberx3.ast.nodes.enums import (
    AperFunction,
    CoordinateNotation,
    Mirroring,
    Polarity,
    UnitMode,
    Zeros,
)
from pygerber.gerberx3.ast.nodes.types import ApertureIdStr
from pygerber.gerberx3.ast.state_tracking_visitor import CoordinateFormat
from pygerber.gerberx3.formatter import Formatter

if TYPE_CHECKING:
    from typing_extensions import Self


NUMBER_OF_VERTICES_IN_TRIANGLE = 3


class _Pad(BaseModel):
    """Base class for pads."""

    node: Node
    aperture_id: ApertureIdStr
    user_attributes: List[TA_UserName] = Field(default_factory=list)
    aper_function: Optional[TA_AperFunction] = None
    drill_tolerance: Optional[TA_DrillTolerance] = None

    def set_aperture_function(
        self,
        aper_function: str | AperFunction,
    ) -> None:
        """Set .AperFunction attribute for aperture."""
        self.aper_function = TA_AperFunction(
            function=(
                AperFunction(aper_function)
                if isinstance(aper_function, str)
                else aper_function
            )
        )

    def set_drill_tolerance(self, plus: float, minus: float) -> None:
        """Set .DrillTolerance attribute for aperture."""
        self.drill_tolerance = TA_DrillTolerance(
            plus_tolerance=plus,
            minus_tolerance=minus,
        )

    def set_custom_attribute(self, name: str, *values: str) -> None:
        """Add custom attribute to the pad."""
        self.user_attributes.append(TA_UserName(user_name=name, fields=list(values)))

    def _get_nodes(self) -> Iterable[Node]:
        has_any_attributes = False

        if self.aper_function is not None:
            has_any_attributes = True
            yield self.aper_function

        if self.drill_tolerance is not None:
            has_any_attributes = True
            yield self.drill_tolerance

        if self.user_attributes:
            has_any_attributes = True
            yield from self.user_attributes

        yield self.node

        if has_any_attributes:
            yield TD()


class _CustomPadCreator:
    """Custom pad class."""

    def __init__(self, pad_creator: _PadCreator) -> None:
        self._pad_creator = pad_creator
        self._primitives: list[Node] = []
        self._finalized = False

    def create(self) -> _Pad:
        """Finalize process of creating custom pad.

        This method can be called only once.
        After calling this method, no more primitives can be added to the pad.
        """
        self._check_finalized()
        macro_id = self._pad_creator._new_macro_id()  # noqa: SLF001

        self._pad_creator._macros.append(  # noqa: SLF001
            AM(
                open=AMopen(name=macro_id),
                primitives=self._primitives,
                close=AMclose(),
            )
        )
        aperture_id = self._pad_creator._new_id()  # noqa: SLF001
        pad = _Pad(
            aperture_id=aperture_id,
            node=ADmacro(
                aperture_id=aperture_id,
                name=macro_id,
            ),
        )
        self._pad_creator._pads.append(pad)  # noqa: SLF001
        self._finalized = True
        return pad

    def _check_finalized(self) -> None:
        if self._finalized:
            msg = "Custom pad already finalized"
            raise RuntimeError(msg)

    def add_circle(
        self, diameter: float, center: tuple[float, float], rotation: float = 0.0
    ) -> Self:
        """Add a circle to the custom pad.

        For corresponding element of Gerber standard see section 4.5.1.3 of
        `The Gerber Layer Format Specification - Revision 2024.05`.

        https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=61
        """
        self._circle(1, diameter, center, rotation)
        return self

    def _circle(
        self,
        exposition: int,
        diameter: float,
        center: tuple[float, float],
        rotation: float,
    ) -> None:
        self._check_finalized()
        self._primitives.append(
            Code1(
                exposure=Constant(constant=exposition),
                diameter=Constant(constant=diameter),
                center_x=Constant(constant=center[0]),
                center_y=Constant(constant=center[1]),
                rotation=Constant(constant=rotation),
            )
        )

    def cut_circle(
        self, diameter: float, center: tuple[float, float], rotation: float = 0.0
    ) -> Self:
        """Add cut out in the shape of a circle.

        For corresponding element of Gerber standard see section 4.5.1.3 of
        `The Gerber Layer Format Specification - Revision 2024.05`.

        https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=61
        """
        self._circle(0, diameter, center, rotation)
        return self

    def add_vector_line(
        self,
        width: float,
        start: tuple[float, float],
        end: tuple[float, float],
        rotation: float = 0.0,
    ) -> Self:
        """Add a vector line to the custom pad.

        For corresponding element of Gerber standard see section 4.5.1.4 of
        `The Gerber Layer Format Specification - Revision 2024.05`.

        https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=62
        """
        self._vector_line(1, width, start, end, rotation)
        return self

    def _vector_line(
        self,
        exposition: int,
        width: float,
        start: tuple[float, float],
        end: tuple[float, float],
        rotation: float,
    ) -> None:
        self._check_finalized()
        self._primitives.append(
            Code20(
                exposure=Constant(constant=exposition),
                width=Constant(constant=width),
                start_x=Constant(constant=start[0]),
                start_y=Constant(constant=start[1]),
                end_x=Constant(constant=end[0]),
                end_y=Constant(constant=end[1]),
                rotation=Constant(constant=rotation),
            )
        )

    def cut_vector_line(
        self,
        width: float,
        start: tuple[float, float],
        end: tuple[float, float],
        rotation: float = 0.0,
    ) -> Self:
        """Add cut out in the shape of a vector line.

        For corresponding element of Gerber standard see section 4.5.1.4 of
        `The Gerber Layer Format Specification - Revision 2024.05`.

        https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=62
        """
        self._vector_line(0, width, start, end, rotation)
        return self

    def add_center_line(
        self,
        width: float,
        height: float,
        center: tuple[float, float],
        rotation: float = 0.0,
    ) -> Self:
        """Add a center line to the custom pad.

        For corresponding element of Gerber standard see section 4.5.1.5 of
        `The Gerber Layer Format Specification - Revision 2024.05`.

        https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=63
        """
        self._center_line(1, width, height, center, rotation)
        return self

    def _center_line(
        self,
        exposition: int,
        width: float,
        height: float,
        center: tuple[float, float],
        rotation: float,
    ) -> None:
        self._check_finalized()
        self._primitives.append(
            Code21(
                exposure=Constant(constant=exposition),
                width=Constant(constant=width),
                height=Constant(constant=height),
                center_x=Constant(constant=center[0]),
                center_y=Constant(constant=center[1]),
                rotation=Constant(constant=rotation),
            )
        )

    def cut_center_line(
        self,
        width: float,
        height: float,
        center: tuple[float, float],
        rotation: float = 0.0,
    ) -> Self:
        """Add cut out in the shape of a center line.

        For corresponding element of Gerber standard see section 4.5.1.5 of
        `The Gerber Layer Format Specification - Revision 2024.05`.

        https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=63
        """
        self._center_line(0, width, height, center, rotation)
        return self

    def add_outline(
        self,
        points: Sequence[tuple[float, float]],
        rotation: float = 0.0,
    ) -> Self:
        """Add an outline to the custom pad.

        For corresponding element of Gerber standard see section 4.5.1.6 of
        `The Gerber Layer Format Specification - Revision 2024.05`.

        https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=64
        """
        assert (
            len(points) >= NUMBER_OF_VERTICES_IN_TRIANGLE
        ), "An outline must have at least 3 points"
        self._outline(1, points, rotation=rotation)
        return self

    def _outline(
        self,
        exposition: int,
        points: Sequence[tuple[float, float]],
        rotation: float,
    ) -> None:
        self._check_finalized()
        points_packed = [
            Point(x=Constant(constant=point[0]), y=Constant(constant=point[1]))
            for point in points
        ]
        self._primitives.append(
            Code4(
                exposure=Constant(constant=exposition),
                number_of_points=Constant(constant=len(points_packed)),
                start_x=points_packed[-1].x,
                start_y=points_packed[-1].y,
                points=points_packed,
                rotation=Constant(constant=rotation),
            )
        )

    def cut_outline(
        self,
        points: Sequence[tuple[float, float]],
        rotation: float = 0.0,
    ) -> Self:
        """Add cut out in the shape of an outline.

        For corresponding element of Gerber standard see section 4.5.1.6 of
        `The Gerber Layer Format Specification - Revision 2024.05`.

        https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=64
        """
        assert (
            len(points) >= NUMBER_OF_VERTICES_IN_TRIANGLE
        ), "An outline must have at least 3 points"
        self._outline(0, points, rotation=rotation)
        return self

    def add_polygon(
        self,
        vertex_count: int,
        center: tuple[float, float],
        outer_diameter: float,
        rotation: float = 0.0,
    ) -> Self:
        """Add a regular polygon to the custom pad.

        For corresponding element of Gerber standard see section 4.5.1.7 of
        `The Gerber Layer Format Specification - Revision 2024.05`.

        https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=66
        """
        self._polygon(1, vertex_count, center, outer_diameter, rotation)
        return self

    def _polygon(
        self,
        exposition: int,
        vertex_count: int,
        center: tuple[float, float],
        outer_diameter: float,
        rotation: float,
    ) -> None:
        self._check_finalized()
        self._primitives.append(
            Code5(
                exposure=Constant(constant=exposition),
                number_of_vertices=Constant(constant=vertex_count),
                diameter=Constant(constant=outer_diameter),
                center_x=Constant(constant=center[0]),
                center_y=Constant(constant=center[1]),
                rotation=Constant(constant=rotation),
            )
        )

    def cut_polygon(
        self,
        vertex_count: int,
        center: tuple[float, float],
        outer_diameter: float,
        rotation: float = 0.0,
    ) -> Self:
        """Add cut out in the shape of a polygon.

        For corresponding element of Gerber standard see section 4.5.1.7 of
        `The Gerber Layer Format Specification - Revision 2024.05`.

        https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=66
        """
        self._polygon(0, vertex_count, center, outer_diameter, rotation)
        return self

    def add_thermal(
        self,
        center: tuple[float, float],
        outer_diameter: float,
        inner_diameter: float,
        gap_thickness: float,
        rotation: float = 0.0,
    ) -> Self:
        """Add a thermal shape to the custom pad.

        For corresponding element of Gerber standard see section 4.5.1.8 of
        `The Gerber Layer Format Specification - Revision 2024.05`.

        https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=67
        """
        self._check_finalized()
        self._primitives.append(
            Code7(
                center_x=Constant(constant=center[0]),
                center_y=Constant(constant=center[1]),
                outer_diameter=Constant(constant=outer_diameter),
                inner_diameter=Constant(constant=inner_diameter),
                gap_thickness=Constant(constant=gap_thickness),
                rotation=Constant(constant=rotation),
            )
        )
        return self


class _PadCreator:
    """Helper class for creating pads."""

    def __init__(self) -> None:
        self._id = 9
        self._macro_id = -1
        self._pads: list[_Pad] = []
        self._macros: list[AM] = []

    def _new_id(self) -> ApertureIdStr:
        self._id += 1
        return ApertureIdStr(f"D{self._id}")

    def _new_macro_id(self) -> str:
        self._macro_id += 1
        return f"M{self._macro_id}"

    def _get_nodes(self) -> Iterable[Node]:
        yield from self._macros
        for pad in self._pads:
            yield from pad._get_nodes()  # noqa: SLF001

    def circle(self, diameter: float, hole_diameter: Optional[float] = None) -> _Pad:
        """Create a circle pad."""
        aperture_id = self._new_id()
        pad = _Pad(
            aperture_id=aperture_id,
            node=ADC(
                aperture_id=aperture_id,
                diameter=diameter,
                hole_diameter=hole_diameter,
            ),
        )
        self._pads.append(pad)
        return pad

    def rectangle(
        self,
        width: float,
        height: float,
        hole_diameter: Optional[float] = None,
    ) -> _Pad:
        """Create a rectangle pad."""
        aperture_id = self._new_id()
        pad = _Pad(
            aperture_id=aperture_id,
            node=ADR(
                aperture_id=aperture_id,
                width=width,
                height=height,
                hole_diameter=hole_diameter,
            ),
        )
        self._pads.append(pad)
        return pad

    def rounded_rectangle(
        self,
        width: float,
        height: float,
        hole_diameter: Optional[float] = None,
    ) -> _Pad:
        """Create a rounded rectangle pad."""
        aperture_id = self._new_id()
        pad = _Pad(
            aperture_id=aperture_id,
            node=ADO(
                aperture_id=aperture_id,
                width=width,
                height=height,
                hole_diameter=hole_diameter,
            ),
        )
        self._pads.append(pad)
        return pad

    def regular_polygon(
        self,
        outer_diameter: float,
        number_of_vertices: int,
        base_rotation_degrees: float,
        hole_diameter: Optional[float] = None,
    ) -> _Pad:
        """Create a regular polygon pad."""
        aperture_id = self._new_id()
        pad = _Pad(
            aperture_id=aperture_id,
            node=ADP(
                aperture_id=aperture_id,
                outer_diameter=outer_diameter,
                vertices=number_of_vertices,
                rotation=base_rotation_degrees,
                hole_diameter=hole_diameter,
            ),
        )
        self._pads.append(pad)
        return pad

    def custom(self) -> _CustomPadCreator:
        """Create a custom pad."""
        return _CustomPadCreator(self)


class _Draw(BaseModel):
    """The _Draw class represents any drawing operation with addison state
    updating commands and attributes.
    """

    draw_op: Node
    state_updates: List[Node] = Field(default_factory=list)
    attributes: List[Node] = Field(default_factory=list)

    def _get_nodes(self) -> Iterable[Node]:
        yield from self.state_updates
        yield from self.attributes
        yield self.draw_op
        if self.attributes:
            yield TD()


class GerberX3Builder:
    """Builder class for constructing Gerber ASTs.

    Code generated is compliant with
    `The Gerber Layer Format Specification - Revision 2024.05`.

    https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf
    """

    def __init__(self) -> None:
        self._pad_creator = _PadCreator()
        self._draws: list[_Draw] = []

        self._coordinate_format = CoordinateFormat(
            zeros=Zeros.SKIP_LEADING,
            coordinate_mode=CoordinateNotation.ABSOLUTE,
            x_integral=4,
            x_decimal=6,
            y_integral=4,
            y_decimal=6,
        )

        self._current_location = (0.0, 0.0)

        self._selected_aperture: Optional[ApertureIdStr] = None
        self._rotation: float = 0.0
        self._mirroring: Mirroring = Mirroring.NONE
        self._mirror_x: bool = False
        self._mirror_y: bool = False
        self._scale: float = 1.0
        self._polarity: Polarity = Polarity.Dark

    def new_pad(self) -> _PadCreator:
        """Create a new pad."""
        return self._pad_creator

    def add_pad(
        self,
        pad: _Pad,
        at: tuple[float, float],
        *,
        rotation: float = 0.0,
        mirror_x: bool = False,
        mirror_y: bool = False,
        scale: float = 1.0,
    ) -> _Draw:
        """Add a pad to the current layer."""
        state_updates = list(
            self._update_state(
                selected_aperture=pad.aperture_id,
                polarity=Polarity.Dark,
                rotation=rotation,
                mirror_x=mirror_x,
                mirror_y=mirror_y,
                scale=scale,
            )
        )
        draw = _Draw(
            state_updates=state_updates,
            draw_op=D03(
                x=CoordinateX(value=self._coordinate_format.pack_x(at[0])),
                y=CoordinateY(value=self._coordinate_format.pack_y(at[1])),
            ),
        )
        self._draws.append(draw)
        return draw

    def _update_state(
        self,
        selected_aperture: Optional[ApertureIdStr] = None,
        polarity: Optional[Polarity] = None,
        rotation: Optional[float] = None,
        mirror_x: Optional[bool] = None,
        mirror_y: Optional[bool] = None,
        scale: Optional[float] = None,
    ) -> Iterable[Node]:
        if (
            selected_aperture is not None
            and self._selected_aperture != selected_aperture
        ):
            self._selected_aperture = selected_aperture
            yield Dnn(is_standalone=True, aperture_id=selected_aperture)

        if polarity is not None and polarity != self._polarity:
            self._polarity = polarity
            yield LP(polarity=polarity)

        if rotation is not None and rotation != self._rotation:
            self._rotation = rotation
            yield LR(rotation=rotation)

        if mirror_x is None:
            mirror_x = self._mirror_x

        if mirror_y is None:
            mirror_y = self._mirror_y

        mirroring = Mirroring.new(x=mirror_x, y=mirror_y)

        if mirroring != self._mirroring:
            self._mirroring = mirroring
            yield LM(mirroring=mirroring)

        if scale is not None and scale != self._scale:
            self._scale = scale
            yield LS(scale=scale)

    def add_cutout_pad(
        self,
        pad: _Pad,
        at: tuple[float, float],
        *,
        rotation: float = 0.0,
        mirror_x: bool = False,
        mirror_y: bool = False,
        scale: float = 1.0,
    ) -> _Draw:
        """Add cutout in shape of a pad to image."""
        state_updates = list(
            self._update_state(
                selected_aperture=pad.aperture_id,
                polarity=Polarity.Clear,
                rotation=rotation,
                mirror_x=mirror_x,
                mirror_y=mirror_y,
                scale=scale,
            )
        )
        draw = _Draw(
            state_updates=state_updates,
            draw_op=D03(
                x=CoordinateX(value=self._coordinate_format.pack_x(at[0])),
                y=CoordinateY(value=self._coordinate_format.pack_y(at[1])),
            ),
        )
        self._draws.append(draw)
        return draw

    def get_code(self) -> GerberX3Code:
        """Get the AST."""
        commands: list[Node] = []
        commands.append(
            FS(
                zeros=Zeros.SKIP_LEADING,
                coordinate_mode=CoordinateNotation.ABSOLUTE,
                x_integral=4,
                x_decimal=6,
                y_integral=4,
                y_decimal=6,
            )
        )
        commands.append(MO(mode=UnitMode.METRIC))
        commands.extend(self._pad_creator._get_nodes())  # noqa: SLF001
        for draw in self._draws:
            commands.extend(draw._get_nodes())  # noqa: SLF001
        commands.append(M02())

        return GerberX3Code(File(nodes=commands))

    def set_standard_attributes(self) -> None:
        """Set standard attributes for the file."""
        raise NotImplementedError


class GerberX3Code:
    """Container for Gerber code produced by the builder.

    Code generated is compliant with
    `The Gerber Layer Format Specification - Revision 2024.05`.

    https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf
    """

    def __init__(self, ast: File) -> None:
        self._ast = ast

    def dump(self, dst: StringIO) -> None:
        """Dump the Gerber code to file or other buffer."""
        Formatter().format(self._ast, dst)

    def dumps(self) -> str:
        """Dump the Gerber code to string."""
        dst = StringIO()
        self.dump(dst)
        return dst.getvalue()

    @property
    def raw(self) -> File:
        """Get the raw AST."""
        return self._ast
