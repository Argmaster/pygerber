"""The `builder` module provides a `stable` interface for constructing Gerber code
which can then be dumped using formatter interface to Gerber files.
"""

from __future__ import annotations

from contextlib import contextmanager
from io import StringIO
from typing import Generator, Iterable, List, Optional

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
    CoordinateX,
    CoordinateY,
    Dnn,
    File,
    Node,
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

    def create(self) -> _Pad:
        """Create the custom pad."""
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
        return pad


class _PadCreator:
    """Helper class for creating pads."""

    def __init__(self) -> None:
        self._id = 9
        self._macro_id = 0
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

    @contextmanager
    def custom(self) -> Generator[_CustomPadCreator, None, None]:
        """Create a custom pad."""
        yield _CustomPadCreator(self)


class _Draw(BaseModel):
    """The _Draw class represents any drawing operation with addison state
    updating commands and attributes.
    """

    draw_op: Node
    state_updates: list[Node] = Field(default_factory=list)
    attributes: list[Node] = Field(default_factory=list)

    def _get_nodes(self) -> Iterable[Node]:
        yield from self.state_updates
        yield from self.attributes
        yield self.draw_op
        if self.attributes:
            yield TD()


class GerberX3Builder:
    """Builder class for constructing Gerber ASTs."""

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

    def get_code(self) -> GerberCode:
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

        return GerberCode(File(nodes=commands))

    def set_standard_attributes(self) -> None:
        """Set standard attributes for the file."""
        raise NotImplementedError


class GerberCode:
    """Container for Gerber code produced by the builder."""

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
