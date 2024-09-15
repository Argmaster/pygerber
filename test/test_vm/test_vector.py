from __future__ import annotations

import math

import pytest

from pygerber.vm.types.vector import Vector

ANGLE_BETWEEN_CASES = [
    (
        Vector(x=0, y=1),  # 12 o'clock
        Vector(x=0, y=1),  # 12 o'clock
        0.0,
    ),
    (
        Vector(x=0, y=1),  # 12 o'clock
        Vector(x=-1, y=1),  # 10.30
        45.0,
    ),
    (
        Vector(x=0, y=1),  # 12 o'clock
        Vector(x=-1, y=0),  #  9 o'clock
        90.0,
    ),
    (
        Vector(x=0, y=1),  # 12 o'clock
        Vector(x=-1, y=-1),  #  7.30
        135.0,
    ),
    (
        Vector(x=0, y=1),  # 12 o'clock
        Vector(x=0, y=-1),  #  6 o'clock
        180.0,
    ),
    (
        Vector(x=0, y=1),  # 12 o'clock
        Vector(x=1, y=-1),  #  7:30
        225.0,
    ),
    (
        Vector(x=0, y=1),  # 12 o'clock
        Vector(x=1, y=0),  #  9 o'clock
        270.0,
    ),
    (
        Vector(x=0, y=1),  # 12 o'clock
        Vector(x=1, y=1),  # 10:30
        315.0,
    ),
]


@pytest.mark.parametrize(
    ("vector0", "vector1", "expect_degrees"),
    [(v1, v0, ((360 - d) if d > 0 else d)) for v0, v1, d in ANGLE_BETWEEN_CASES],
)
def test_angle_between(
    vector0: Vector,
    vector1: Vector,
    expect_degrees: float,
) -> None:
    assert math.isclose(
        vector0.angle_between_cc(vector1),
        expect_degrees,
        rel_tol=1e-6,
    )


@pytest.mark.parametrize(
    ("vector0", "vector1", "expect_degrees"),
    ANGLE_BETWEEN_CASES,
)
def test_angle_between_flipped(
    vector0: Vector,
    vector1: Vector,
    expect_degrees: float,
) -> None:
    assert math.isclose(
        vector0.angle_between_cc(vector1),
        expect_degrees,
        rel_tol=1e-6,
    )


@pytest.mark.parametrize(
    ("vector0", "vector1", "expect_degrees"),
    ANGLE_BETWEEN_CASES,
)
def test_angle_between_cc(
    vector0: Vector,
    vector1: Vector,
    expect_degrees: float,
) -> None:
    assert math.isclose(
        vector0.angle_between_cc(vector1),
        expect_degrees,
        rel_tol=1e-6,
    )


@pytest.mark.parametrize(
    ("vector0", "vector1", "expect_degrees"),
    [(v1, v0, ((360 - d) if d > 0 else d)) for v0, v1, d in ANGLE_BETWEEN_CASES],
)
def test_angle_between_cc_flipped(
    vector0: Vector,
    vector1: Vector,
    expect_degrees: float,
) -> None:
    assert math.isclose(
        vector0.angle_between_cc(vector1),
        expect_degrees,
        rel_tol=1e-6,
    )


def test_vector_addition() -> None:
    v1 = Vector(x=1, y=2)
    v2 = Vector(x=3, y=4)
    result = v1 + v2
    assert result.x == float(4)
    assert result.y == float(6)


def test_unit_addition() -> None:
    v = Vector(x=1, y=2)
    u = 3
    result = v + u
    assert result.x == 4.0  # noqa: PLR2004
    assert result.y == 5.0  # noqa: PLR2004


def test_scalar_addition() -> None:
    v = Vector(x=1, y=2)
    scalar = 3
    result = v + scalar
    assert result.x == 4.0  # noqa: PLR2004
    assert result.y == 5.0  # noqa: PLR2004


def test_vector_subtraction() -> None:
    v1 = Vector(x=4, y=6)
    v2 = Vector(x=1, y=2)
    result = v1 - v2
    assert result.x == 3.0  # noqa: PLR2004
    assert result.y == 4.0  # noqa: PLR2004


def test_unit_subtraction() -> None:
    v = Vector(x=4, y=6)
    u = 3.0
    result = v - u
    assert result.x == 1.0
    assert result.y == 3.0  # noqa: PLR2004


def test_scalar_subtraction() -> None:
    v = Vector(x=4, y=6)
    scalar = 3
    result = v - scalar
    assert result.x == 1
    assert result.y == 3  # noqa: PLR2004


def test_vector_multiplication() -> None:
    v1 = Vector(x=2, y=3)
    v2 = Vector(x=4, y=5)
    result = v1 * v2
    assert result.x == 8  # noqa: PLR2004
    assert result.y == 15  # noqa: PLR2004


def test_unit_multiplication() -> None:
    v = Vector(x=2, y=3)
    u = 4.0
    result = v * u
    assert result.x == 8  # noqa: PLR2004
    assert result.y == 12  # noqa: PLR2004


def test_scalar_multiplication() -> None:
    v = Vector(x=2, y=3)
    scalar = 4
    result = v * scalar
    assert result.x == 8  # noqa: PLR2004
    assert result.y == 12  # noqa: PLR2004


def test_vector_division() -> None:
    v1 = Vector(x=8, y=15)
    v2 = Vector(x=2, y=3)
    result = v1 / v2
    assert result.x == 4  # noqa: PLR2004
    assert result.y == 5  # noqa: PLR2004


def test_unit_division() -> None:
    v = Vector(x=8, y=15)
    u = 2
    result = v / u
    assert result.x == 4  # noqa: PLR2004
    assert result.y == 7.5  # noqa: PLR2004


def test_scalar_division() -> None:
    v = Vector(x=8, y=15)
    scalar = 2
    result = v / scalar
    assert result.x == 4  # noqa: PLR2004
    assert result.y == 7.5  # noqa: PLR2004


def test_vector_equality() -> None:
    v1 = Vector(x=1, y=2)
    v2 = Vector(x=1, y=2)
    assert v1 == v2


def test_vector_inequality() -> None:
    v1 = Vector(x=1, y=2)
    v2 = Vector(x=3, y=4)
    assert v1 != v2


def test_vector_less_than() -> None:
    v1 = Vector(x=1, y=2)
    v2 = Vector(x=3, y=4)
    assert v1 < v2


def test_vector_greater_than() -> None:
    v1 = Vector(x=3, y=4)
    v2 = Vector(x=1, y=2)
    assert v1 > v2


def test_vector_greater_than_or_equal() -> None:
    v1 = Vector(x=3, y=4)
    v2 = Vector(x=1, y=2)
    assert v1 >= v2


def test_vector_less_than_or_equal() -> None:
    v1 = Vector(x=1, y=2)
    v2 = Vector(x=3, y=4)
    assert v1 <= v2


def test_vector_negation() -> None:
    v = Vector(x=1, y=2)
    result = -v
    assert result.x == -1
    assert result.y == -2  # noqa: PLR2004


def test_vector_normalize() -> None:
    v = Vector(x=3, y=4)
    result = v.normalized()
    assert math.isclose(result.x, 0.6, rel_tol=1e-6)
    assert math.isclose(result.y, 0.8, rel_tol=1e-6)


def test_vector_length() -> None:
    v = Vector(x=3, y=4)
    result = v.length()
    assert math.isclose(result, 5.0, rel_tol=1e-6)
