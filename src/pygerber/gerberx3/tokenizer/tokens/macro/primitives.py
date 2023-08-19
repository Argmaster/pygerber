"""Macro primitives tokens."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Any, ClassVar, List, Optional

from pygerber.backend.abstract.aperture_handle import PrivateApertureHandle
from pygerber.gerberx3.parser.state import State
from pygerber.gerberx3.tokenizer.tokens.macro.arithmetic_expression import (
    NumericConstant,
)
from pygerber.gerberx3.tokenizer.tokens.macro.expression import Expression
from pygerber.gerberx3.tokenizer.tokens.macro.macro_context import MacroContext
from pygerber.gerberx3.tokenizer.tokens.macro.numeric_expression import (
    NumericExpression,
)
from pygerber.gerberx3.tokenizer.tokens.macro.point import Point
from pygerber.sequence_tools import unwrap

if TYPE_CHECKING:
    from typing_extensions import Self


class Primitive(Expression):
    """Wrapper for macro primitive token, common base class for specialized tokens."""

    symbol: ClassVar[str] = "X"


class PrimitiveCircle(Primitive):
    """Wrapper for macro circle primitive token."""

    symbol: ClassVar[str] = "1"

    exposure: NumericExpression
    diameter: NumericExpression
    center_x: NumericExpression
    center_y: NumericExpression
    rotation: NumericExpression

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        exposure: NumericExpression = unwrap(tokens["exposure"])
        diameter: NumericExpression = unwrap(tokens["diameter"])
        center_x: NumericExpression = unwrap(tokens["center_x"])
        center_y: NumericExpression = unwrap(tokens["center_y"])
        rotation: Optional[NumericExpression] = (
            unwrap(tokens["rotation"]) if tokens.get("rotation") is not None else None
        )
        if rotation is None:
            rotation = NumericConstant(value=Decimal("0.0"))

        return cls(
            exposure=exposure,
            diameter=diameter,
            center_x=center_x,
            center_y=center_y,
            rotation=rotation,
        )

    def evaluate(
        self,
        macro_context: MacroContext,
        state: State,
        handle: PrivateApertureHandle,
    ) -> None:
        """Evaluate macro expression."""
        self.exposure.evaluate_numeric(macro_context, state)
        self.diameter.evaluate_numeric(macro_context, state)
        self.center_x.evaluate_numeric(macro_context, state)
        self.center_y.evaluate_numeric(macro_context, state)
        self.rotation.evaluate_numeric(macro_context, state)

        return super().evaluate(macro_context, state, handle)

    def __str__(self) -> str:
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

    symbol: ClassVar[str] = "20"

    exposure: NumericExpression
    width: NumericExpression
    start_x: NumericExpression
    start_y: NumericExpression
    end_x: NumericExpression
    end_y: NumericExpression
    rotation: NumericExpression

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        exposure: NumericExpression = unwrap(tokens["exposure"])
        width: NumericExpression = unwrap(tokens["width"])
        start_x: NumericExpression = unwrap(tokens["start_x"])
        start_y: NumericExpression = unwrap(tokens["start_y"])
        end_x: NumericExpression = unwrap(tokens["end_x"])
        end_y: NumericExpression = unwrap(tokens["end_y"])
        rotation: NumericExpression = unwrap(tokens["rotation"])

        return cls(
            exposure=exposure,
            width=width,
            start_x=start_x,
            start_y=start_y,
            end_x=end_x,
            end_y=end_y,
            rotation=rotation,
        )

    def __str__(self) -> str:
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

    symbol: ClassVar[str] = "21"

    exposure: NumericExpression
    width: NumericExpression
    hight: NumericExpression
    center_x: NumericExpression
    center_y: NumericExpression
    rotation: NumericExpression

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        exposure: NumericExpression = unwrap(tokens["exposure"])
        width: NumericExpression = unwrap(tokens["width"])
        hight: NumericExpression = unwrap(tokens["hight"])
        center_x: NumericExpression = unwrap(tokens["center_x"])
        center_y: NumericExpression = unwrap(tokens["center_y"])
        rotation: NumericExpression = unwrap(tokens["rotation"])

        return cls(
            exposure=exposure,
            width=width,
            hight=hight,
            center_x=center_x,
            center_y=center_y,
            rotation=rotation,
        )

    def __str__(self) -> str:
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

    symbol: ClassVar[str] = "4"

    exposure: NumericExpression
    number_of_vertices: NumericExpression
    start_x: NumericExpression
    start_y: NumericExpression
    rotation: NumericExpression
    point: List[Point]

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        exposure: NumericExpression = unwrap(tokens["exposure"])
        number_of_vertices: NumericExpression = unwrap(tokens["number_of_vertices"])
        start_x: NumericExpression = unwrap(tokens["start_x"])
        start_y: NumericExpression = unwrap(tokens["start_y"])
        rotation: NumericExpression = unwrap(tokens["rotation"])
        point: list[Point] = list(tokens.get("point", []))

        return cls(
            exposure=exposure,
            number_of_vertices=number_of_vertices,
            start_x=start_x,
            start_y=start_y,
            rotation=rotation,
            point=point,
        )

    def __str__(self) -> str:
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

    symbol: ClassVar[str] = "5"

    exposure: NumericExpression
    number_of_vertices: NumericExpression
    center_x: NumericExpression
    center_y: NumericExpression
    diameter: NumericExpression
    rotation: NumericExpression

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        exposure: NumericExpression = unwrap(tokens["exposure"])
        number_of_vertices: NumericExpression = unwrap(tokens["number_of_vertices"])
        center_x: NumericExpression = unwrap(tokens["center_x"])
        center_y: NumericExpression = unwrap(tokens["center_y"])
        diameter: NumericExpression = unwrap(tokens["diameter"])
        rotation: NumericExpression = unwrap(tokens["rotation"])
        return cls(
            exposure=exposure,
            number_of_vertices=number_of_vertices,
            center_x=center_x,
            center_y=center_y,
            diameter=diameter,
            rotation=rotation,
        )

    def __str__(self) -> str:
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

    symbol: ClassVar[str] = "7"

    center_x: NumericExpression
    center_y: NumericExpression
    outer_diameter: NumericExpression
    inner_diameter: NumericExpression
    gap: NumericExpression
    rotation: NumericExpression

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        center_x: NumericExpression = unwrap(tokens["center_x"])
        center_y: NumericExpression = unwrap(tokens["center_y"])
        outer_diameter: NumericExpression = unwrap(tokens["outer_diameter"])
        inner_diameter: NumericExpression = unwrap(tokens["inner_diameter"])
        gap: NumericExpression = unwrap(tokens["gap"])
        rotation: NumericExpression = unwrap(tokens["rotation"])
        return cls(
            center_x=center_x,
            center_y=center_y,
            outer_diameter=outer_diameter,
            inner_diameter=inner_diameter,
            gap=gap,
            rotation=rotation,
        )

    def __str__(self) -> str:
        string = self.symbol

        string += f",{self.center_x}"
        string += f",{self.center_y}"
        string += f",{self.outer_diameter}"
        string += f",{self.inner_diameter}"
        string += f",{self.gap}"
        string += f",{self.rotation}"

        return string + "*"
