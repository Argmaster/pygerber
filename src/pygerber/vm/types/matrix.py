"""`matrix` module contains specialized implementation of 3x3 Matrix used to apply
2D transformations to Vectors.
"""

from __future__ import annotations

from math import cos, radians, sin
from typing import TYPE_CHECKING, Tuple, TypeVar

from pygerber.gerber.ast.nodes.types import Double
from pygerber.vm.types.vector import Vector

if TYPE_CHECKING:
    from typing_extensions import Self, TypeAlias

MatrixRowT: TypeAlias = Tuple[Double, Double, Double]
MatrixInitializerT: TypeAlias = Tuple[MatrixRowT, MatrixRowT, MatrixRowT]

T = TypeVar("T")


class Matrix3x3:
    """3x3 Matrix used to apply 2D transformations to Vectors."""

    no_columns: int = 3
    no_rows: int = 3

    def __init__(self, mtx: MatrixInitializerT) -> None:
        assert len(mtx) == self.no_rows
        assert len(mtx[0]) == self.no_columns
        assert len(mtx[1]) == self.no_columns
        assert len(mtx[2]) == self.no_columns
        self.mtx = mtx

    @classmethod
    def new_translate(cls, x: Double, y: Double) -> Matrix3x3:
        """Create new translation matrix."""
        return cls(
            (
                (1.0, 0.0, x),
                (0.0, 1.0, y),
                (0.0, 0.0, 1.0),
            )
        )

    @classmethod
    def new_rotate(cls, angle: Double) -> Matrix3x3:
        """Create new rotation matrix.

        Parameters
        ----------
        angle : Double
            Rotation angle in degrees.

        Returns
        -------
        Matrix3x3
            New matrix instance.

        """
        angle = radians(angle)
        c = cos(angle)
        s = sin(angle)
        return cls(
            (
                (c, -s, 0.0),
                (s, c, 0.0),
                (0.0, 0.0, 1.0),
            )
        )

    @classmethod
    def new_reflect(cls, *, x: bool, y: bool) -> Matrix3x3:
        """Create new reflection matrix."""
        return cls(
            (
                (-1.0 if x else 1.0, 0.0, 0.0),
                (0.0, -1.0 if y else 1.0, 0.0),
                (0.0, 0.0, 1.0),
            )
        )

    @classmethod
    def new_scale(cls, x: Double, y: Double) -> Self:
        """Create new scaling matrix."""
        return cls(
            (
                (x, 0.0, 0.0),
                (0.0, y, 0.0),
                (0.0, 0.0, 1.0),
            )
        )

    def __matmul__(self, other: T) -> T:
        if isinstance(other, Matrix3x3):
            result = [
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
            ]

            for i in range(len(self.mtx)):
                for j in range(len(other.mtx[0])):
                    for k in range(len(other.mtx)):
                        result[i][j] += self.mtx[i][k] * other.mtx[k][j]

            return other.__class__(tuple(map(tuple, result)))  # type: ignore[arg-type, return-value]

        if isinstance(other, Vector):
            x = self.mtx[0][0] * other.x + self.mtx[0][1] * other.y + self.mtx[0][2]
            y = self.mtx[1][0] * other.x + self.mtx[1][1] * other.y + self.mtx[1][2]
            return Vector(x=x, y=y)  # type: ignore[return-value]

        return NotImplemented

    @property
    def tag(self) -> str:
        """Return tag representing this matrix transform."""
        return str(self.mtx).encode("utf-8").hex()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.mtx})"

    __repr__ = __str__

    def __getitem__(self, key: int) -> MatrixRowT:
        return self.mtx[key]
