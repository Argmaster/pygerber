from __future__ import annotations

import math

import pytest

from pygerber.vm.types.vector import Unit, Vector

ANGLE_BETWEEN_CASES = [
    (
        Vector.from_values(0, 1),  # 12 o'clock
        Vector.from_values(0, 1),  # 12 o'clock
        0.0,
    ),
    (
        Vector.from_values(0, 1),  # 12 o'clock
        Vector.from_values(-1, 1),  # 10.30
        45.0,
    ),
    (
        Vector.from_values(0, 1),  # 12 o'clock
        Vector.from_values(-1, 0),  #  9 o'clock
        90.0,
    ),
    (
        Vector.from_values(0, 1),  # 12 o'clock
        Vector.from_values(-1, -1),  #  7.30
        135.0,
    ),
    (
        Vector.from_values(0, 1),  # 12 o'clock
        Vector.from_values(0, -1),  #  6 o'clock
        180.0,
    ),
    (
        Vector.from_values(0, 1),  # 12 o'clock
        Vector.from_values(1, -1),  #  7:30
        225.0,
    ),
    (
        Vector.from_values(0, 1),  # 12 o'clock
        Vector.from_values(1, 0),  #  9 o'clock
        270.0,
    ),
    (
        Vector.from_values(0, 1),  # 12 o'clock
        Vector.from_values(1, 1),  # 10:30
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
    v1 = Vector.from_values(1, 2)
    v2 = Vector.from_values(3, 4)
    result = v1 + v2
    assert result.x == Unit.from_float(4)
    assert result.y == Unit.from_float(6)


def test_unit_addition() -> None:
    v = Vector.from_values(1, 2)
    u = Unit.from_float(3)
    result = v + u
    assert result.x == Unit.from_float(4)
    assert result.y == Unit.from_float(5)


def test_scalar_addition() -> None:
    v = Vector.from_values(1, 2)
    scalar = 3
    result = v + scalar
    assert result.x == Unit.from_float(4)
    assert result.y == Unit.from_float(5)


def test_vector_subtraction() -> None:
    v1 = Vector.from_values(4, 6)
    v2 = Vector.from_values(1, 2)
    result = v1 - v2
    assert result.x == Unit.from_float(3)
    assert result.y == Unit.from_float(4)


def test_unit_subtraction() -> None:
    v = Vector.from_values(4, 6)
    u = Unit.from_float(3)
    result = v - u
    assert result.x == Unit.from_float(1)
    assert result.y == Unit.from_float(3)


def test_scalar_subtraction() -> None:
    v = Vector.from_values(4, 6)
    scalar = 3
    result = v - scalar
    assert result.x == Unit.from_float(1)
    assert result.y == Unit.from_float(3)


def test_vector_multiplication() -> None:
    v1 = Vector.from_values(2, 3)
    v2 = Vector.from_values(4, 5)
    result = v1 * v2
    assert result.x == Unit.from_float(8)
    assert result.y == Unit.from_float(15)


def test_unit_multiplication() -> None:
    v = Vector.from_values(2, 3)
    u = Unit.from_float(4)
    result = v * u
    assert result.x == Unit.from_float(8)
    assert result.y == Unit.from_float(12)


def test_scalar_multiplication() -> None:
    v = Vector.from_values(2, 3)
    scalar = 4
    result = v * scalar
    assert result.x == Unit.from_float(8)
    assert result.y == Unit.from_float(12)


def test_vector_division() -> None:
    v1 = Vector.from_values(8, 15)
    v2 = Vector.from_values(2, 3)
    result = v1 / v2
    assert result.x == Unit.from_float(4)
    assert result.y == Unit.from_float(5)


def test_unit_division() -> None:
    v = Vector.from_values(8, 15)
    u = Unit.from_float(2)
    result = v / u
    assert result.x == Unit.from_float(4)
    assert result.y == Unit.from_float(7.5)


def test_scalar_division() -> None:
    v = Vector.from_values(8, 15)
    scalar = 2
    result = v / scalar
    assert result.x == Unit.from_float(4)
    assert result.y == Unit.from_float(7.5)


def test_vector_equality() -> None:
    v1 = Vector.from_values(1, 2)
    v2 = Vector.from_values(1, 2)
    assert v1 == v2


def test_vector_inequality() -> None:
    v1 = Vector.from_values(1, 2)
    v2 = Vector.from_values(3, 4)
    assert v1 != v2


def test_vector_less_than() -> None:
    v1 = Vector.from_values(1, 2)
    v2 = Vector.from_values(3, 4)
    assert v1 < v2


def test_vector_greater_than() -> None:
    v1 = Vector.from_values(3, 4)
    v2 = Vector.from_values(1, 2)
    assert v1 > v2


def test_vector_greater_than_or_equal() -> None:
    v1 = Vector.from_values(3, 4)
    v2 = Vector.from_values(1, 2)
    assert v1 >= v2


def test_vector_less_than_or_equal() -> None:
    v1 = Vector.from_values(1, 2)
    v2 = Vector.from_values(3, 4)
    assert v1 <= v2


def test_vector_negation() -> None:
    v = Vector.from_values(1, 2)
    result = -v
    assert result.x == Unit.from_float(-1)
    assert result.y == Unit.from_float(-2)


def test_vector_normalize() -> None:
    v = Vector.from_values(3, 4)
    result = v.normalize()
    assert math.isclose(result.x.value, 0.6, rel_tol=1e-6)
    assert math.isclose(result.y.value, 0.8, rel_tol=1e-6)


def test_vector_length() -> None:
    v = Vector.from_values(3, 4)
    result = v.length()
    assert math.isclose(result.value, 5.0, rel_tol=1e-6)
