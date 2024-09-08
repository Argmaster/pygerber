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
    FS,
    M02,
    MO,
    TD,
    ADmacro,
    AMclose,
    AMopen,
    File,
    Node,
    TA_AperFunction,
    TA_DrillTolerance,
    TA_UserName,
)
from pygerber.gerberx3.ast.nodes.enums import (
    AperFunction,
    CoordinateNotation,
    UnitMode,
    Zeros,
)
from pygerber.gerberx3.ast.nodes.types import ApertureIdStr
from pygerber.gerberx3.formatter import Formatter


class _Pad(BaseModel):
    """Base class for pads."""

    node: Node
    user_attributes: List[TA_UserName] = Field(default_factory=list)
    aper_function: Optional[TA_AperFunction] = None
    drill_tolerance: Optional[TA_DrillTolerance] = None

    def add_standard_attribute(
        self,
        aper_function: Optional[str] = None,
        drill_tolerance_plus: Optional[float] = None,
        drill_tolerance_minus: Optional[float] = None,
    ) -> None:
        """Add standard attributes to the pad."""
        if aper_function is not None:
            self.aper_function = TA_AperFunction(function=AperFunction(aper_function))

        if drill_tolerance_plus is not None or drill_tolerance_minus is not None:
            self.drill_tolerance = TA_DrillTolerance(
                plus_tolerance=drill_tolerance_plus,
                minus_tolerance=drill_tolerance_minus,
            )

    def add_custom_attribute(self, name: str, *values: str) -> None:
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
        pad = _Pad(
            node=ADmacro(
                aperture_id=self._pad_creator._new_id(),  # noqa: SLF001
                name=macro_id,
            )
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
        pad = _Pad(
            node=ADC(
                aperture_id=self._new_id(),
                diameter=diameter,
                hole_diameter=hole_diameter,
            )
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
        pad = _Pad(
            node=ADR(
                aperture_id=self._new_id(),
                width=width,
                height=height,
                hole_diameter=hole_diameter,
            )
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
        pad = _Pad(
            node=ADO(
                aperture_id=self._new_id(),
                width=width,
                height=height,
                hole_diameter=hole_diameter,
            )
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
        pad = _Pad(
            node=ADP(
                aperture_id=self._new_id(),
                outer_diameter=outer_diameter,
                vertices=number_of_vertices,
                rotation=base_rotation_degrees,
                hole_diameter=hole_diameter,
            )
        )
        self._pads.append(pad)
        return pad

    @contextmanager
    def custom(self) -> Generator[_CustomPadCreator, None, None]:
        """Create a custom pad."""
        yield _CustomPadCreator(self)


class GerberX3Builder:
    """Builder class for constructing Gerber ASTs."""

    def __init__(self) -> None:
        self._pad_creator = _PadCreator()
        self._ops: list[Node] = []

    def new_pad(self) -> _PadCreator:
        """Create a new pad."""
        return self._pad_creator

    def add_pad(self, pad: _Pad) -> None:
        """Add a pad to the current layer."""

    def add_cutout(self) -> None:
        """Add a cutout to the current layer."""

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
        commands.append(M02())

        return GerberCode(File(nodes=commands))


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
