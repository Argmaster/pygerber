"""Macro primitives tokens."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from pygerber.gerberx3.tokenizer.tokens.macro.element import Element
from pygerber.sequence_tools import unwrap

if TYPE_CHECKING:
    from pygerber.gerberx3.tokenizer.tokens.macro.expression import Expression
    from pygerber.gerberx3.tokenizer.tokens.macro.point import Point


class Primitive(Element):
    """Wrapper for macro primitive token, common base class for specialized tokens."""

    symbol: ClassVar[str] = "X"


class PrimitiveCircle(Primitive):
    """Wrapper for macro circle primitive token."""

    symbol = "1"

    def __init__(  # noqa: PLR0913
        self,
        exposure: Expression,
        diameter: Expression,
        center_x: Expression,
        center_y: Expression,
        rotation: Expression | None = None,
    ) -> None:
        """Initialize token object."""
        super().__init__()

        self.exposure = unwrap(exposure)
        self.diameter = unwrap(diameter)
        self.center_x = unwrap(center_x)
        self.center_y = unwrap(center_y)
        self.rotation = unwrap(rotation) if rotation is not None else None

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        string = self.symbol

        string += f",{self.exposure}"
        string += f",{self.diameter}"
        string += f",{self.center_x}"
        string += f",{self.center_y}"

        if self.rotation is not None:
            string += f",{self.rotation}"

        return string + "*"


class PrimitiveVectorLine(Primitive):
    """Wrapper for macro vector line primitive token."""

    symbol = "20"

    def __init__(  # noqa: PLR0913
        self,
        exposure: Expression,
        width: Expression,
        start_x: Expression,
        start_y: Expression,
        end_x: Expression,
        end_y: Expression,
        rotation: Expression,
    ) -> None:
        """Initialize token object."""
        super().__init__()
        self.exposure = unwrap(exposure)
        self.width = unwrap(width)
        self.start_x = unwrap(start_x)
        self.start_y = unwrap(start_y)
        self.end_x = unwrap(end_x)
        self.end_y = unwrap(end_y)
        self.rotation = unwrap(rotation)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        string = self.symbol

        string += f",{self.exposure}"
        string += f",{self.width}"
        string += f",{self.start_x}"
        string += f",{self.start_y}"
        string += f",{self.end_x}"
        string += f",{self.end_y}"
        string += f",{self.rotation}"

        return string + "*"


class PrimitiveCenterLine(Primitive):
    """Wrapper for macro center line primitive token."""

    symbol = "21"

    def __init__(  # noqa: PLR0913
        self,
        exposure: Expression,
        width: Expression,
        hight: Expression,
        center_x: Expression,
        center_y: Expression,
        rotation: Expression,
    ) -> None:
        """Initialize token object."""
        super().__init__()
        self.exposure = unwrap(exposure)
        self.width = unwrap(width)
        self.hight = unwrap(hight)
        self.center_x = unwrap(center_x)
        self.center_y = unwrap(center_y)
        self.rotation = unwrap(rotation)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        string = self.symbol

        string += f",{self.exposure}"
        string += f",{self.width}"
        string += f",{self.hight}"
        string += f",{self.center_x}"
        string += f",{self.center_y}"
        string += f",{self.rotation}"

        return string + "*"


class PrimitiveOutline(Primitive):
    """Wrapper for macro outline primitive token."""

    symbol = "4"

    def __init__(  # noqa: PLR0913
        self,
        exposure: Expression,
        number_of_vertices: Expression,
        start_x: Expression,
        start_y: Expression,
        rotation: Expression,
        point: list[Point] | None = None,
    ) -> None:
        """Initialize token object."""
        super().__init__()
        self.exposure = unwrap(exposure)
        self.number_of_vertices = unwrap(number_of_vertices)
        self.start_x = unwrap(start_x)
        self.start_y = unwrap(start_y)
        self.rotation = unwrap(rotation)
        self.point = point if point is not None else []

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        string = self.symbol

        string += f",{self.exposure}"
        string += f",{self.number_of_vertices}"
        string += f",{self.start_x}"
        string += f",{self.start_y}"
        string += f",{self.rotation}"

        for point in self.point:
            string += f",{point}"

        return string + "*"


class PrimitivePolygon(Primitive):
    """Wrapper for macro outline primitive token."""

    symbol = "5"

    def __init__(  # noqa: PLR0913
        self,
        exposure: Expression,
        number_of_vertices: Expression,
        center_x: Expression,
        center_y: Expression,
        diameter: Expression,
        rotation: Expression,
    ) -> None:
        """Initialize token object."""
        super().__init__()
        self.exposure = unwrap(exposure)
        self.number_of_vertices = unwrap(number_of_vertices)
        self.center_x = unwrap(center_x)
        self.center_y = unwrap(center_y)
        self.diameter = unwrap(diameter)
        self.rotation = unwrap(rotation)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        string = self.symbol

        string += f",{self.exposure}"
        string += f",{self.number_of_vertices}"
        string += f",{self.center_x}"
        string += f",{self.center_y}"
        string += f",{self.diameter}"
        string += f",{self.rotation}"

        return string + "*"


class PrimitiveThermal(Primitive):
    """Wrapper for macro outline primitive token."""

    symbol = "7"

    def __init__(  # noqa: PLR0913
        self,
        center_x: Expression,
        center_y: Expression,
        outer_diameter: Expression,
        inner_diameter: Expression,
        gap: Expression,
        rotation: Expression,
    ) -> None:
        """Initialize token object."""
        super().__init__()
        self.center_x = unwrap(center_x)
        self.center_y = unwrap(center_y)
        self.outer_diameter = unwrap(outer_diameter)
        self.inner_diameter = unwrap(inner_diameter)
        self.gap = unwrap(gap)
        self.rotation = unwrap(rotation)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        string = self.symbol

        string += f",{self.center_x}"
        string += f",{self.center_y}"
        string += f",{self.outer_diameter}"
        string += f",{self.inner_diameter}"
        string += f",{self.gap}"
        string += f",{self.rotation}"

        return string + "*"
