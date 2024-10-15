"""The `builder` module provides a `stable` API for constructing Gerber code.

Construction is done by creating a `GerberX3Builder` object and using its methods to
add elements to image. When the image is ready, call `get_code()` method to get the
Gerber code.
"""

from __future__ import annotations

from abc import abstractmethod
from io import StringIO
from typing import (
    TYPE_CHECKING,
    Iterable,
    List,
    Optional,
    Sequence,
    TextIO,
    Tuple,
)

from pydantic import BaseModel, Field

from pygerber.gerber.ast import CoordinateFormat
from pygerber.gerber.ast.nodes import (
    ADC,
    ADO,
    ADP,
    ADR,
    AM,
    D01,
    D02,
    D03,
    FS,
    G36,
    G37,
    G75,
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
    AperFunction,
    ApertureIdStr,
    Code1,
    Code4,
    Code5,
    Code7,
    Code20,
    Code21,
    Constant,
    CoordinateNotation,
    CoordinateX,
    CoordinateY,
    Dnn,
    File,
    Mirroring,
    Node,
    Point,
    Polarity,
    TA_AperFunction,
    TA_DrillTolerance,
    TA_UserName,
    UnitMode,
    Zeros,
)
from pygerber.gerber.ast.nodes.g_codes.G01 import G01
from pygerber.gerber.ast.nodes.g_codes.G02 import G02
from pygerber.gerber.ast.nodes.g_codes.G03 import G03
from pygerber.gerber.ast.nodes.other.coordinate import CoordinateI, CoordinateJ
from pygerber.gerber.ast.state_tracking_visitor import PlotMode

if TYPE_CHECKING:
    from typing_extensions import Self, TypeAlias


NUMBER_OF_VERTICES_IN_TRIANGLE = 3


Loc2D: TypeAlias = Tuple[float, float]
"""Type alias of tuple of two floats representing 2D location."""


class GerberX3Builder:
    """Builder class for constructing Gerber ASTs.

    Builder uses metric units (millimeters) and absolute coordinates.
    This default can not be changed. Use of imperial units and incremental coordinates
    in Gerber files is deprecated.

    Code generated is compliant with
    [The Gerber Layer Format Specification - Revision 2024.05](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf).
    """

    def __init__(self) -> None:
        self._pad_creator = PadCreator(self)
        self._draws: list[Draw] = []

        self._coordinate_format = CoordinateFormat(
            zeros=Zeros.SKIP_LEADING,
            coordinate_mode=CoordinateNotation.ABSOLUTE,
            x_integral=4,
            x_decimal=6,
            y_integral=4,
            y_decimal=6,
        )

        self._current_location: Optional[Loc2D] = None

        self._selected_aperture: Optional[ApertureIdStr] = None
        self._rotation: float = 0.0
        self._mirroring: Mirroring = Mirroring.NONE
        self._mirror_x: bool = False
        self._mirror_y: bool = False
        self._scale: float = 1.0
        self._polarity: Polarity = Polarity.Dark
        self._plot_mode: Optional[PlotMode] = None

        self._trace_pads: dict[float, Pad] = {}

    def _pack_x(self, x: float) -> CoordinateX:
        return CoordinateX(value=self._coordinate_format.pack_x(x))

    def _pack_y(self, y: float) -> CoordinateY:
        return CoordinateY(value=self._coordinate_format.pack_y(y))

    def _pack_i(self, i: float) -> CoordinateI:
        return CoordinateI(value=self._coordinate_format.pack_x(i))

    def _pack_j(self, j: float) -> CoordinateJ:
        return CoordinateJ(value=self._coordinate_format.pack_y(j))

    def _add_draw(self, draw: Draw) -> None:
        self._current_location = draw._new_current_location  # noqa: SLF001
        self._draws.append(draw)

    def new_pad(self) -> PadCreator:
        """Create a new pad."""
        return self._pad_creator

    def add_pad(
        self,
        pad: Pad,
        at: Loc2D | TraceDraw,
        *,
        rotation: float = 0.0,
        mirror_x: bool = False,
        mirror_y: bool = False,
        scale: float = 1.0,
    ) -> PadDraw:
        """Add pad in shape of a pad to image.

        This corresponds to the flash with positive polarity in Gerber standard.

        Parameters
        ----------
        pad : Pad
            Previously defined pad object to be used for drawing.
        at : Loc2D | TraceDraw
            Location to flash at. Can be a 2-tuple of floats or TraceDraw object
            returned from `add_line_trace()` or `add_clockwise_arc_trace()`, then the
            end location of that trace will be used.
        rotation : float, optional
            Pad rotation (rotation around pad origin), by default 0.0
        mirror_x : bool, optional
            Pad X mirroring (mirroring of pad orientation relative to pad origin
            X axis), by default False
        mirror_y : bool, optional
            Pad Y mirroring (mirroring of pad orientation relative to pad origin
            Y axis), by default False
        scale : float, optional
            Pad scaling (pad grows in all directions), by default 1.0

        Returns
        -------
        PadDraw
            Object which can be used to set attributes of the pad or use it as start
            point for another  trace.

        """
        self._check_pad_not_a_pad_creator(pad)

        state_updates = list(
            self._create_state_updates(
                selected_aperture=pad.aperture_id,
                polarity=Polarity.Dark,
                rotation=rotation,
                mirror_x=mirror_x,
                mirror_y=mirror_y,
                scale=scale,
            )
        )
        location = at.end_location if isinstance(at, TraceDraw) else at

        draw = PadDraw(
            state_updates=state_updates,
            draw_ops=[
                D03(
                    x=CoordinateX(value=self._coordinate_format.pack_x(location[0])),
                    y=CoordinateY(value=self._coordinate_format.pack_y(location[1])),
                )
            ],
            location=location,
        )
        self._add_draw(draw)
        return draw

    def _check_pad_not_a_pad_creator(self, pad: Pad | PadCreator) -> None:
        if not isinstance(pad, Pad):
            raise NotAPadError(pad)

    def _create_state_updates(  # noqa: C901
        self,
        selected_aperture: Optional[ApertureIdStr] = None,
        polarity: Optional[Polarity] = None,
        rotation: Optional[float] = None,
        mirror_x: Optional[bool] = None,
        mirror_y: Optional[bool] = None,
        scale: Optional[float] = None,
        plot_mode: Optional[PlotMode] = None,
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

        if plot_mode is not None and self._plot_mode != plot_mode:
            if plot_mode == PlotMode.LINEAR:
                yield G01()
            elif plot_mode == PlotMode.ARC:
                yield G02()
            elif plot_mode == PlotMode.CCW_ARC:
                yield G03()
            else:
                raise NotImplementedError(plot_mode)
            self._plot_mode = plot_mode

    def add_cutout_pad(
        self,
        pad: Pad,
        at: Loc2D | TraceDraw,
        *,
        rotation: float = 0.0,
        mirror_x: bool = False,
        mirror_y: bool = False,
        scale: float = 1.0,
    ) -> PadDraw:
        """Add cutout in shape of a pad to image.

        This corresponds to the flash with negative polarity in Gerber standard.
        The result will be a hole in shape of a pad cut out of whatever was previously
        at the given location.

        Parameters
        ----------
        pad : Pad
            Previously defined pad object to be used for drawing.
        at : Loc2D | TraceDraw
            Location to flash at. Can be a 2-tuple of floats or TraceDraw object
            returned from `add_line_trace()` or `add_clockwise_arc_trace()`, then the
            end location of that trace will be used.
        rotation : float, optional
            Pad rotation (rotation around pad origin), by default 0.0
        mirror_x : bool, optional
            Pad X mirroring (mirroring of pad orientation relative to pad origin
            X axis), by default False
        mirror_y : bool, optional
            Pad Y mirroring (mirroring of pad orientation relative to pad origin
            Y axis), by default False
        scale : float, optional
            Pad scaling (pad grows in all directions), by default 1.0

        Returns
        -------
        PadDraw
            Object which can be used to set attributes of the pad or use it as start
            point for trace.

        """
        self._check_pad_not_a_pad_creator(pad)

        state_updates = list(
            self._create_state_updates(
                selected_aperture=pad.aperture_id,
                polarity=Polarity.Clear,
                rotation=rotation,
                mirror_x=mirror_x,
                mirror_y=mirror_y,
                scale=scale,
            )
        )
        location = at.end_location if isinstance(at, TraceDraw) else at

        draw = PadDraw(
            state_updates=state_updates,
            draw_ops=[
                D03(
                    x=CoordinateX(value=self._coordinate_format.pack_x(location[0])),
                    y=CoordinateY(value=self._coordinate_format.pack_y(location[1])),
                )
            ],
            location=location,
        )
        self._add_draw(draw)
        return draw

    def add_line_trace(
        self,
        width: float,
        begin: Loc2D | PadDraw | TraceDraw,
        end: Loc2D | PadDraw | TraceDraw,
    ) -> TraceDraw:
        """Add a trace to the image.

        Parameters
        ----------
        width : float
            Width of a trace.
        begin : Loc2D | PadDraw | TraceDraw
            Begin point of the trace. When 2-tuple of floats is provided, it is
            interpreted as absolute coordinates. When PadDraw is provided, the
            location of the center of the pad is used. When TraceDraw is provided, the
            end location of the trace is used.
        end : Loc2D | PadDraw | TraceDraw
            End point of the trace. When 2-tuple of floats is provided, it is
            interpreted as absolute coordinates. When PadDraw is provided, the
            location of the center of the pad is used. When TraceDraw is provided, the
            begin location of the trace is used.

        Returns
        -------
        TraceDraw
            Object which can be used to set attributes of the trace, as start
            point for another trace or a center of a pad.

        """
        aperture = self._get_trace_aperture(width)

        begin_location = self._dispatch_begin_location(begin)
        end_location = self._dispatch_end_location(end)

        state_updates = list(
            self._create_state_updates(
                selected_aperture=aperture.aperture_id,
                polarity=Polarity.Dark,
                rotation=0.0,
                mirror_x=False,
                mirror_y=False,
                scale=1.0,
                plot_mode=PlotMode.LINEAR,
            )
        )

        draw_ops: list[Node] = []
        if self._current_location != begin_location:
            draw_ops.append(
                D02(
                    x=self._pack_x(begin_location[0]),
                    y=self._pack_y(begin_location[1]),
                )
            )

        draw_ops.append(
            D01(
                x=self._pack_x(end_location[0]),
                y=self._pack_y(end_location[1]),
            )
        )

        draw = TraceDraw(
            state_updates=state_updates,
            draw_ops=draw_ops,
            begin_location=begin_location,
            end_location=end_location,
        )
        self._add_draw(draw)
        return draw

    def _dispatch_end_location(self, end: Loc2D | PadDraw | TraceDraw) -> Loc2D:
        if isinstance(end, tuple):
            end_location = end
        elif isinstance(end, PadDraw):
            end_location = end.location
        elif isinstance(end, TraceDraw):
            end_location = end.begin_location
        else:
            raise NotImplementedError
        return end_location

    def _dispatch_begin_location(self, begin: Loc2D | PadDraw | TraceDraw) -> Loc2D:
        if isinstance(begin, tuple):
            begin_location = begin
        elif isinstance(begin, PadDraw):
            begin_location = begin.location
        elif isinstance(begin, TraceDraw):
            begin_location = begin.end_location
        else:
            raise NotImplementedError
        return begin_location

    def _get_trace_aperture(self, width: float) -> Pad:
        if (aperture := self._trace_pads.get(width)) is None:
            aperture = self.new_pad().circle(width)
            self._trace_pads[width] = aperture

        return aperture

    def add_clockwise_arc_trace(
        self,
        width: float,
        begin: Loc2D | PadDraw | TraceDraw,
        end: Loc2D | PadDraw | TraceDraw,
        center: Loc2D,
    ) -> TraceDraw:
        """Add a clockwise arc trace to the image.

        Parameters
        ----------
        width : float
            Width of a trace.
        begin : Loc2D | PadDraw | TraceDraw
            Begin point of the trace. When 2-tuple of floats is provided, it is
            interpreted as absolute coordinates. When PadDraw is provided, the
            location of the center of the pad is used. When TraceDraw is provided, the
            end location of the trace is used.
        end : Loc2D | PadDraw | TraceDraw
            End point of the trace. When 2-tuple of floats is provided, it is
            interpreted as absolute coordinates. When PadDraw is provided, the
            location of the center of the pad is used. When TraceDraw is provided, the
            begin location of the trace is used.
        center : Loc2D
            Center of the arc.

        Returns
        -------
        TraceDraw
            Object which can be used to set attributes of the trace, as start
            point for another trace or a center of a pad.

        """
        aperture = self._get_trace_aperture(width)

        begin_location = self._dispatch_begin_location(begin)
        end_location = self._dispatch_end_location(end)

        state_updates = list(
            self._create_state_updates(
                selected_aperture=aperture.aperture_id,
                polarity=Polarity.Dark,
                rotation=0.0,
                mirror_x=False,
                mirror_y=False,
                scale=1.0,
                plot_mode=PlotMode.ARC,
            )
        )

        draw_ops: list[Node] = []
        if self._current_location != begin_location:
            draw_ops.append(
                D02(
                    x=self._pack_x(begin_location[0]),
                    y=self._pack_y(begin_location[1]),
                )
            )

        draw_ops.append(
            D01(
                x=self._pack_x(end_location[0]),
                y=self._pack_y(end_location[1]),
                i=self._pack_i(center[0] - begin_location[0]),
                j=self._pack_j(center[1] - begin_location[1]),
            )
        )

        draw = ArcTraceDraw(
            state_updates=state_updates,
            draw_ops=draw_ops,
            begin_location=begin_location,
            end_location=end_location,
            center_location=center,
            is_clockwise=True,
        )
        self._add_draw(draw)
        return draw

    def add_counter_clockwise_arc_trace(
        self,
        width: float,
        begin: Loc2D | PadDraw | TraceDraw,
        end: Loc2D | PadDraw | TraceDraw,
        center: Loc2D,
    ) -> TraceDraw:
        """Add a counter clockwise arc trace to the image.

        Parameters
        ----------
        width : float
            Width of a trace.
        begin : Loc2D | PadDraw | TraceDraw
            Begin point of the trace. When 2-tuple of floats is provided, it is
            interpreted as absolute coordinates. When PadDraw is provided, the
            location of the center of the pad is used. When TraceDraw is provided, the
            end location of the trace is used.
        end : Loc2D | PadDraw | TraceDraw
            End point of the trace. When 2-tuple of floats is provided, it is
            interpreted as absolute coordinates. When PadDraw is provided, the
            location of the center of the pad is used. When TraceDraw is provided, the
            begin location of the trace is used.
        center : Loc2D
            Center of the arc.

        Returns
        -------
        TraceDraw
            Object which can be used to set attributes of the trace, as start
            point for another trace or a center of a pad.

        """
        aperture = self._get_trace_aperture(width)

        begin_location = self._dispatch_begin_location(begin)
        end_location = self._dispatch_end_location(end)

        state_updates = list(
            self._create_state_updates(
                selected_aperture=aperture.aperture_id,
                polarity=Polarity.Dark,
                rotation=0.0,
                mirror_x=False,
                mirror_y=False,
                scale=1.0,
                plot_mode=PlotMode.CCW_ARC,
            )
        )

        draw_ops: list[Node] = []
        if self._current_location != begin_location:
            draw_ops.append(
                D02(
                    x=self._pack_x(begin_location[0]),
                    y=self._pack_y(begin_location[1]),
                )
            )

        draw_ops.append(
            D01(
                x=self._pack_x(end_location[0]),
                y=self._pack_y(end_location[1]),
                i=self._pack_i(center[0] - begin_location[0]),
                j=self._pack_j(center[1] - begin_location[1]),
            )
        )

        draw = ArcTraceDraw(
            state_updates=state_updates,
            draw_ops=draw_ops,
            begin_location=begin_location,
            end_location=end_location,
            center_location=center,
            is_clockwise=False,
        )
        self._add_draw(draw)
        return draw

    def new_region(self, begin: Loc2D) -> RegionCreator:
        """Return RegionCreator object ready for creating a region.

        Parameters
        ----------
        begin : Optional[Loc2D], optional
            Location to start the region outline.

        Returns
        -------
        RegionCreator
            Object handling process of region creation.

        """
        return RegionCreator(self, begin)

    def get_code(self) -> GerberCode:
        """Generate Gerber code created with builder until this point."""
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
        commands.append(G75())
        for draw in self._draws:
            commands.extend(draw._get_nodes())  # noqa: SLF001
        commands.append(M02())

        return GerberCode(File(nodes=commands))

    def set_standard_attributes(self) -> None:
        """Set standard attributes for the file."""
        raise NotImplementedError


class GerberCode:
    """Container for Gerber code produced by the builder."""

    def __init__(self, ast: File) -> None:
        self._ast = ast

    def dump(self, dst: TextIO) -> None:
        """Dump the Gerber code to file or other buffer."""
        from pygerber.gerber.formatter import Formatter

        Formatter().format(self._ast, dst)

    def dumps(self) -> str:
        """Dump the Gerber code to string."""
        dst = StringIO()
        self.dump(dst)
        return dst.getvalue()

    @property
    def raw(self) -> File:
        """Get raw abstract syntax tree of Gerber code."""
        return self._ast


class PadCreator:
    """The `PadCreator` is responsible for managing creation of pads.

    Do not directly instantiate this class, instead use `new_pad()` method of
    `GerberX3Builder`.
    """

    def __init__(self, builder: GerberX3Builder) -> None:
        # We don't actually need builder, but we don't want users to create PadCreator
        # instances manually, so we require it to be passed to make it much harder to
        # get wrong.
        assert isinstance(builder, GerberX3Builder)
        self._builder = builder
        self._id = 9
        self._macro_id = -1
        self._pads: list[Pad] = []
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

    def circle(self, diameter: float, hole_diameter: Optional[float] = None) -> Pad:
        """Create a circle pad.

        For corresponding element of Gerber standard see section 4.4.2 of
        [The Gerber Layer Format Specification - Revision 2024.05](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=51).

        Parameters
        ----------
        diameter : float
            Circle diameter.
        hole_diameter : Optional[float], optional
            Diameter circle shaped hole in aperture, by default None, meaning no hole.

        Returns
        -------
        Pad
            New pad object.

        """
        aperture_id = self._new_id()
        pad = Pad(
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
    ) -> Pad:
        """Create a rectangle pad.

        For corresponding element of Gerber standard see section 4.4.3 of
        [The Gerber Layer Format Specification - Revision 2024.05](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=53).

        Parameters
        ----------
        width : float
            Width (x dimension) of rectangle aperture.
        height : float
            Height (y dimension) of rectangle aperture.
        hole_diameter : Optional[float], optional
            Diameter circle shaped hole in aperture, by default None, meaning no hole.

        Returns
        -------
        Pad
            New pad object.

        """
        aperture_id = self._new_id()
        pad = Pad(
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
    ) -> Pad:
        """Create a rounded rectangle pad.

        For corresponding element of Gerber standard see section 4.4.4 of
        [The Gerber Layer Format Specification - Revision 2024.05](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=54).

        Parameters
        ----------
        width : float
            Width (x dimension) of rounded rectangle aperture.
        height : float
            Height (y dimension) of rounded rectangle aperture.
        hole_diameter : Optional[float], optional
            Diameter circle shaped hole in aperture, by default None, meaning no hole.

        Returns
        -------
        Pad
            New pad object.

        """
        aperture_id = self._new_id()
        pad = Pad(
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
    ) -> Pad:
        """Create a regular polygon pad.

        For corresponding element of Gerber standard see section 4.4.5 of
        [The Gerber Layer Format Specification - Revision 2024.05](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=55).

        Parameters
        ----------
        outer_diameter : float
            Diameter of the circle circumscribed around the polygon.
        number_of_vertices : int
            Number of vertices of the polygon.
        base_rotation_degrees : float
            Rotation of the polygon in degrees.
        hole_diameter : Optional[float], optional
            Diameter circle shaped hole in aperture, by default None, meaning no hole.

        Returns
        -------
        Pad
            New pad object.

        """
        aperture_id = self._new_id()
        pad = Pad(
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

    def custom(self) -> CustomPadCreator:
        """Get an object for creating custom pads.

        For corresponding element of Gerber standard see section 4.5 of
        [The Gerber Layer Format Specification - Revision 2024.05](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=57).

        Returns
        -------
        CustomPadCreator
            Object allowing you to add shapes to custom aperture.

        """
        return CustomPadCreator(self)


class Pad(BaseModel):
    """The `Pad` class represents a pad object created with `PadCreator` which can be
    added to the image managed by `GerberX3Builder` with use of `add_pad()` method.

    Do not directly instantiate this class, use methods available on `PadCreator` class.
    """

    node: Node
    aperture_id: ApertureIdStr
    user_attributes: List[TA_UserName] = Field(default_factory=list)
    aper_function: Optional[TA_AperFunction] = None
    drill_tolerance: Optional[TA_DrillTolerance] = None

    def set_aperture_function(
        self,
        aper_function: str | AperFunction,
    ) -> None:
        """Set `.AperFunction` attribute for aperture.

        For corresponding element of Gerber standard see section 5.6.10 of
        [The Gerber Layer Format Specification - Revision 2024.05](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=140).

        Parameters
        ----------
        aper_function : str | AperFunction
            Aperture function value. Can be an `AperFunction` enum value or a string
            conversable to it.

        """
        self.aper_function = TA_AperFunction(
            function=(
                AperFunction(aper_function)
                if isinstance(aper_function, str)
                else aper_function
            )
        )

    def set_drill_tolerance(self, plus: float, minus: float) -> None:
        """Set `.DrillTolerance` attribute for aperture.

        For corresponding element of Gerber standard see section 5.6.11 of
        [The Gerber Layer Format Specification - Revision 2024.05](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=148).

        Parameters
        ----------
        plus : float
            Plus tolerance of a drill hole.
        minus : float
            Minus tolerance of a drill hole.

        """
        self.drill_tolerance = TA_DrillTolerance(
            plus_tolerance=plus,
            minus_tolerance=minus,
        )

    def set_custom_attribute(self, name: str, *values: str) -> None:
        """Add custom attribute to the pad.

        For corresponding element of Gerber standard see section 5.1 of
        [The Gerber Layer Format Specification - Revision 2024.05](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=122).

        Parameters
        ----------
        name : str
            Name of custom attribute.
        *values : str
            Values of custom attribute.

        """
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


class CustomPadCreator:
    """The `CustomPadCreator` is single use driver of process of creating custom pad.

    Do not directly instantiate this class, instead use `new_pad()` method of
    `GerberX3Builder`.
    """

    def __init__(self, pad_creator: PadCreator) -> None:
        self._pad_creator = pad_creator
        self._primitives: list[Node] = []
        self._finalized = False

    def create(self) -> Pad:
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
        pad = Pad(
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

    def add_circle(self, diameter: float, center: Loc2D, rotation: float = 0.0) -> Self:
        """Add a circle to the custom pad.

        For corresponding element of Gerber standard see section 4.5.1.3 of
        [The Gerber Layer Format Specification - Revision 2024.05](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=61).

        Parameters
        ----------
        diameter : float
            Circle diameter.
        center : Loc2D
            Location of circle center relative to pad origin.
        rotation : float, optional
            Rotation of the circle relative to the pad origin in degrees
            counterclockwise, by default 0.0

        Returns
        -------
        Self
            Same CustomPadCreator object for method chaining.

        """
        self._circle(1, diameter, center, rotation)
        return self

    def _circle(
        self,
        exposition: int,
        diameter: float,
        center: Loc2D,
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

    def cut_circle(self, diameter: float, center: Loc2D, rotation: float = 0.0) -> Self:
        """Add a cut out in a shape of a circle to the custom pad.

        For corresponding element of Gerber standard see section 4.5.1.3 of
        [The Gerber Layer Format Specification - Revision 2024.05](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=61).

        Parameters
        ----------
        diameter : float
            Circle diameter.
        center : Loc2D
            Location of circle center relative to pad origin.
        rotation : float, optional
            Rotation of the circle relative to the pad origin in degrees
            counterclockwise, by default 0.0

        Returns
        -------
        Self
            Same CustomPadCreator object for method chaining.

        """
        self._circle(0, diameter, center, rotation)
        return self

    def add_vector_line(
        self,
        width: float,
        start: Loc2D,
        end: Loc2D,
        rotation: float = 0.0,
    ) -> Self:
        """Add a vector line to the custom pad.

        For corresponding element of Gerber standard see section 4.5.1.4 of
        [The Gerber Layer Format Specification - Revision 2024.05](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=62).

        Parameters
        ----------
        width : float
            Vector line width.
        start : Loc2D
            Start point coordinates relative to origin of the pad.
        end : Loc2D
            End point coordinates relative to origin of the pad.
        rotation : float, optional
            Rotation of the vector line relative to the pad origin in degrees
            counterclockwise, by default 0.0

        Returns
        -------
        Self
            Same CustomPadCreator object for method chaining.

        """
        self._vector_line(1, width, start, end, rotation)
        return self

    def _vector_line(
        self,
        exposition: int,
        width: float,
        start: Loc2D,
        end: Loc2D,
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
        start: Loc2D,
        end: Loc2D,
        rotation: float = 0.0,
    ) -> Self:
        """Add a cut out in a shape of a vector line to the custom pad.

        For corresponding element of Gerber standard see section 4.5.1.4 of
        [The Gerber Layer Format Specification - Revision 2024.05](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=62).

        Parameters
        ----------
        width : float
            Vector line width.
        start : Loc2D
            Start point coordinates relative to origin of the pad.
        end : Loc2D
            End point coordinates relative to origin of the pad.
        rotation : float, optional
            Rotation of the vector line relative to the pad origin in degrees
            counterclockwise, by default 0.0

        Returns
        -------
        Self
            Same CustomPadCreator object for method chaining.

        """
        self._vector_line(0, width, start, end, rotation)
        return self

    def add_center_line(
        self,
        width: float,
        height: float,
        center: Loc2D,
        rotation: float = 0.0,
    ) -> Self:
        """Add a center line to the custom pad.

        For corresponding element of Gerber standard see section 4.5.1.5 of
        [The Gerber Layer Format Specification - Revision 2024.05](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=63).

        Parameters
        ----------
        width : float
            Line width (x dimension).
        height : float
            Line height (y dimension).
        center : Loc2D
            Line center coordinates relative to origin of the pad.
        rotation : float, optional
            Rotation of the center line relative to the pad origin in degrees
            counterclockwise, by default 0.0

        Returns
        -------
        Self
            Same CustomPadCreator object for method chaining.

        """
        self._center_line(1, width, height, center, rotation)
        return self

    def _center_line(
        self,
        exposition: int,
        width: float,
        height: float,
        center: Loc2D,
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
        center: Loc2D,
        rotation: float = 0.0,
    ) -> Self:
        """Add a cut out in a shape of a center line to the custom pad.

        For corresponding element of Gerber standard see section 4.5.1.5 of
        [The Gerber Layer Format Specification - Revision 2024.05](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=63).

        Parameters
        ----------
        width : float
            Line width (x dimension).
        height : float
            Line height (y dimension).
        center : Loc2D
            Line center coordinates relative to origin of the pad.
        rotation : float, optional
            Rotation of the center line relative to the pad origin in degrees
            counterclockwise, by default 0.0

        Returns
        -------
        Self
            Same CustomPadCreator object for method chaining.

        """
        self._center_line(0, width, height, center, rotation)
        return self

    def add_outline(
        self,
        points: Sequence[Loc2D],
        rotation: float = 0.0,
    ) -> Self:
        """Add an outline to the custom pad.

        For corresponding element of Gerber standard see section 4.5.1.6 of
        [The Gerber Layer Format Specification - Revision 2024.05](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=64).

        Parameters
        ----------
        points : Sequence[Loc2D]
            Points of the outline as coordinates relative to the center of the pad.
            First and last point are implicitly connected.
        rotation : float, optional
            Rotation of the outline relative to the pad origin in degrees
            counterclockwise, by default 0.0

        Returns
        -------
        Self
            Same CustomPadCreator object for method chaining.

        """
        assert (
            len(points) >= NUMBER_OF_VERTICES_IN_TRIANGLE
        ), "An outline must have at least 3 points"
        self._outline(1, points, rotation=rotation)
        return self

    def _outline(
        self,
        exposition: int,
        points: Sequence[Loc2D],
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
        points: Sequence[Loc2D],
        rotation: float = 0.0,
    ) -> Self:
        """Add a cut out in a shape of an outline to the custom pad.

        For corresponding element of Gerber standard see section 4.5.1.6 of
        [The Gerber Layer Format Specification - Revision 2024.05](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=64).

        Parameters
        ----------
        points : Sequence[Loc2D]
            Points of the outline as coordinates relative to the center of the pad.
            First and last point are implicitly connected.
        rotation : float, optional
            Rotation of the outline relative to the pad origin in degrees
            counterclockwise, by default 0.0

        Returns
        -------
        Self
            Same CustomPadCreator object for method chaining.

        """
        assert (
            len(points) >= NUMBER_OF_VERTICES_IN_TRIANGLE
        ), "An outline must have at least 3 points"
        self._outline(0, points, rotation=rotation)
        return self

    def add_polygon(
        self,
        vertex_count: int,
        center: Loc2D,
        outer_diameter: float,
        rotation: float = 0.0,
    ) -> Self:
        """Add a regular polygon to the custom pad.

        For corresponding element of Gerber standard see section 4.5.1.7 of
        [The Gerber Layer Format Specification - Revision 2024.05](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=66).

        Parameters
        ----------
        vertex_count : int
            Number of vertices of the polygon.
        center : Loc2D
            Coordinates of center of the polygon relative to the pad origin.
        outer_diameter : float
            Diameter of the circle circumscribed around the polygon.
        rotation : float, optional
            Rotation of the polygon relative to the pad origin in degrees
            counterclockwise, by default 0.0

        Returns
        -------
        Self
            Same CustomPadCreator object for method chaining.

        """
        self._polygon(1, vertex_count, center, outer_diameter, rotation)
        return self

    def _polygon(
        self,
        exposition: int,
        vertex_count: int,
        center: Loc2D,
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
        center: Loc2D,
        outer_diameter: float,
        rotation: float = 0.0,
    ) -> Self:
        """Add a regular polygon to the custom pad.

        For corresponding element of Gerber standard see section 4.5.1.7 of
        [The Gerber Layer Format Specification - Revision 2024.05](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=66).

        Parameters
        ----------
        vertex_count : int
            Number of vertices of the polygon.
        center : Loc2D
            Coordinates of center of the polygon relative to the pad origin.
        outer_diameter : float
            Diameter of the circle circumscribed around the polygon.
        rotation : float, optional
            Rotation of the polygon relative to the pad origin in degrees
            counterclockwise, by default 0.0

        Returns
        -------
        Self
            Same CustomPadCreator object for method chaining.

        """
        self._polygon(0, vertex_count, center, outer_diameter, rotation)
        return self

    def add_thermal(
        self,
        center: Loc2D,
        outer_diameter: float,
        inner_diameter: float,
        gap_thickness: float,
        rotation: float = 0.0,
    ) -> Self:
        """Add a thermal shape to the custom pad.

        For corresponding element of Gerber standard see section 4.5.1.8 of
        [The Gerber Layer Format Specification - Revision 2024.05](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf#page=67).

        Parameters
        ----------
        center : Loc2D
            Center point coordinates.
        outer_diameter : float
            Outer diameter > inner diameter
        inner_diameter : float
            Inner diameter >= 0
        gap_thickness : float
            Gap thickness < (outer diameter)/√2. Note that if the (gap
            thickness)*√2 ≥ (inner diameter) the inner circle disappears. This is
            not invalid.
            The gaps are on the X and Y axes through the center without
            rotation. They rotate with the primitive.
        rotation : float, optional
            Rotation of the thermal relative to the pad origin in degrees
            counterclockwise, by default 0.0

        Returns
        -------
        Self
            Same CustomPadCreator object for method chaining.

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


class _OutlineSegment(BaseModel):
    end: Loc2D


class _LineSegment(_OutlineSegment):
    pass


class _CwArcSegment(_OutlineSegment):
    begin: Loc2D
    center: Loc2D


class _CcwArcSegment(_OutlineSegment):
    begin: Loc2D
    center: Loc2D


class RegionCreator:
    """The `RegionCreator` is responsible for managing creation of regions.

    Do not directly instantiate this class, instead use `new_region()` method of
    `GerberX3Builder`.
    """

    def __init__(self, builder: GerberX3Builder, begin: Loc2D) -> None:
        # We don't actually need builder, but we don't want users to create
        # RegionCreator instances manually, so we require it to be passed to make it
        # much harder to get wrong.
        assert isinstance(builder, GerberX3Builder)
        self._builder = builder
        self._begin = begin
        self._outline: list[_OutlineSegment] = []
        self._previous_end = begin

    def add_line(self, to: tuple[float, float]) -> Self:
        """Add a line to the region outline.

        Parameters
        ----------
        to : tuple[float, float]
            End point of the line.

        Returns
        -------
        Self
            Same RegionCreator object for method chaining.

        """
        self._outline.append(_LineSegment(end=to))
        self._previous_end = to
        return self

    def add_clockwise_arc(
        self, to: tuple[float, float], center: tuple[float, float]
    ) -> Self:
        """Add a clockwise arc to the region outline.

        Parameters
        ----------
        to : tuple[float, float]
            End point of the arc.
        center : tuple[float, float]
            Center of the arc.

        Returns
        -------
        Self
            Same RegionCreator object for method chaining.

        """
        self._outline.append(
            _CwArcSegment(begin=self._previous_end, center=center, end=to)
        )
        self._previous_end = to
        return self

    def add_counterclockwise_arc(
        self, to: tuple[float, float], center: tuple[float, float]
    ) -> Self:
        """Add a counterclockwise arc to the region outline.

        Parameters
        ----------
        to : tuple[float, float]
            End point of the arc.
        center : tuple[float, float]
            Center of the arc.

        Returns
        -------
        Self
            Same RegionCreator object for method chaining.

        """
        self._outline.append(
            _CcwArcSegment(begin=self._previous_end, center=center, end=to)
        )
        self._previous_end = to
        return self

    def create(self) -> Region:  # noqa: C901
        """Finalize process of creating region and automatically add it to the image.

        This method can be called only once.
        After calling this method, no more elements can be added to the region.
        """
        if len(self._outline) < NUMBER_OF_VERTICES_IN_TRIANGLE:
            msg = "A region must have at least 3 points"
            raise InvalidRegionOutlineError(msg)

        def _() -> Iterable[Node]:
            aperture = self._builder._get_trace_aperture(1)  # noqa: SLF001
            yield from self._builder._create_state_updates(  # noqa: SLF001
                selected_aperture=aperture.aperture_id,
                polarity=Polarity.Dark,
                rotation=0.0,
                mirror_x=False,
                mirror_y=False,
                scale=1.0,
            )

            mode: Optional[PlotMode] = None

            yield G36()
            yield D02(
                x=self._builder._pack_x(self._begin[0]),  # noqa: SLF001
                y=self._builder._pack_y(self._begin[1]),  # noqa: SLF001
            )

            last = self._outline[-1]
            if last.end != self._begin:
                self._outline.append(_LineSegment(end=self._begin))

            for segment in self._outline:
                if isinstance(segment, _LineSegment):
                    if mode != PlotMode.LINEAR:
                        yield G01()
                        mode = PlotMode.LINEAR

                    yield D01(
                        x=self._builder._pack_x(segment.end[0]),  # noqa: SLF001
                        y=self._builder._pack_y(segment.end[1]),  # noqa: SLF001
                    )

                elif isinstance(segment, _CwArcSegment):
                    if mode != PlotMode.ARC:
                        yield G02()
                        mode = PlotMode.ARC

                    yield D01(
                        x=self._builder._pack_x(segment.end[0]),  # noqa: SLF001
                        y=self._builder._pack_y(segment.end[1]),  # noqa: SLF001
                        i=self._builder._pack_i(  # noqa: SLF001
                            segment.center[0] - segment.begin[0]
                        ),
                        j=self._builder._pack_j(  # noqa: SLF001
                            segment.center[1] - segment.begin[1]
                        ),
                    )

                elif isinstance(segment, _CcwArcSegment):
                    if mode != PlotMode.CCW_ARC:
                        yield G03()
                        mode = PlotMode.CCW_ARC

                    yield D01(
                        x=self._builder._pack_x(segment.end[0]),  # noqa: SLF001
                        y=self._builder._pack_y(segment.end[1]),  # noqa: SLF001
                        i=self._builder._pack_i(  # noqa: SLF001
                            segment.center[0] - segment.begin[0]
                        ),
                        j=self._builder._pack_j(  # noqa: SLF001
                            segment.center[1] - segment.begin[1]
                        ),
                    )

                else:
                    raise NotImplementedError

            yield G37()
            yield D02(
                x=self._builder._pack_x(self._begin[0]),  # noqa: SLF001
                y=self._builder._pack_y(self._begin[1]),  # noqa: SLF001
            )

        region = Region(nodes=list(_()), attributes=[], location=self._begin)
        self._builder._add_draw(region)  # noqa: SLF001
        return region


class Draw(BaseModel):
    """The `Draw` class is a base class for all drawing operations."""

    @property
    @abstractmethod
    def _new_current_location(self) -> Loc2D:
        """Get new current location after the draw operation."""

    @abstractmethod
    def _get_nodes(self) -> Iterable[Node]:
        """Get nodes representing the draw operation."""


class SimpleDraw(Draw):
    """The `Draw` class represents any drawing operation with additional state
    updating commands and attributes.
    """

    draw_ops: List[Node]
    state_updates: List[Node] = Field(default_factory=list)
    attributes: List[Node] = Field(default_factory=list)

    def _get_nodes(self) -> Iterable[Node]:
        yield from self.state_updates
        yield from self.attributes
        yield from self.draw_ops
        if self.attributes:
            yield TD()


class PadDraw(SimpleDraw):
    """The `PadDraw` represents a drawing operation of creating a pad."""

    location: Loc2D

    @property
    def _new_current_location(self) -> Loc2D:
        """Get new current location after the draw operation."""
        return self.location


class TraceDraw(SimpleDraw):
    """The `TraceDraw` represents a drawing operation of creating a trace."""

    begin_location: Loc2D
    end_location: Loc2D

    @property
    def _new_current_location(self) -> Loc2D:
        """Get new current location after the draw operation."""
        return self.end_location


class ArcTraceDraw(TraceDraw):
    """The `ArcTraceDraw` represents a drawing operation of creating an arc trace."""

    center_location: Loc2D
    is_clockwise: bool

    @property
    def _new_current_location(self) -> Loc2D:
        """Get new current location after the draw operation."""
        return self.end_location


class Region(Draw):
    """The `Region` represents a drawing operation of creating a region."""

    nodes: List[Node] = Field(default_factory=list)
    attributes: List[Node] = Field(default_factory=list)
    location: Loc2D

    def _get_nodes(self) -> Iterable[Node]:
        yield from self.attributes
        yield from self.nodes
        if self.attributes:
            yield TD()

    @property
    def _new_current_location(self) -> Loc2D:
        """Get new current location after the draw operation."""
        return self.location


class GerberX3BuilderError(Exception):
    """Base class for exceptions raised by `GerberX3Builder`."""


class NotAPadError(GerberX3BuilderError):
    """Raised when a pad is expected but different object is provided."""

    def __init__(self, obj: object) -> None:
        super().__init__(
            f"Expected a {Pad.__qualname__} class instance, got "
            f"{type(obj).__qualname__}. Make sure "
            f"you are calling pad creation method on object returned by new_pad() "
            "method, eg. `circle()`, `rectangle()`, etc. If you are using custom pad, "
            "make sure you are calling `create()` method after adding all custom "
            "aperture elements."
        )


class InvalidRegionOutlineError(GerberX3BuilderError):
    """Raised when a region outline is invalid."""
