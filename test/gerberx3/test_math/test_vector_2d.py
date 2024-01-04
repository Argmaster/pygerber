from __future__ import annotations

import math

import pytest

from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.state_enums import Unit


def test_vector2d_as_pixels() -> None:
    vector = Vector2D(
        x=Offset.new(1, unit=Unit.Inches),
        y=Offset.new(2, unit=Unit.Inches),
    )
    dpi = 300
    expected_pixels = (300, 600)
    assert vector.as_pixels(dpi) == expected_pixels


def test_vector2d_equality() -> None:
    vector1 = Vector2D(x=Offset.new(1), y=Offset.new(2))
    vector2 = Vector2D(x=Offset.new(1), y=Offset.new(2))
    vector3 = Vector2D(x=Offset.new(3), y=Offset.new(4))
    assert vector1 == vector2
    assert vector1 != vector3


def test_vector2d_addition() -> None:
    vector1 = Vector2D(x=Offset.new(1), y=Offset.new(2))
    vector2 = Vector2D(x=Offset.new(3), y=Offset.new(4))
    expected_result = Vector2D(x=Offset.new(4), y=Offset.new(6))
    assert vector1 + vector2 == expected_result


def test_vector2d_subtraction() -> None:
    vector1 = Vector2D(x=Offset.new(3), y=Offset.new(4))
    vector2 = Vector2D(x=Offset.new(1), y=Offset.new(2))
    expected_result = Vector2D(x=Offset.new(2), y=Offset.new(2))
    assert vector1 - vector2 == expected_result


def test_vector2d_multiplication() -> None:
    vector = Vector2D(x=Offset.new(2), y=Offset.new(3))
    scalar = 2
    expected_result = Vector2D(x=Offset.new(4), y=Offset.new(6))
    assert vector * scalar == expected_result


def test_vector2d_division() -> None:
    vector = Vector2D(x=Offset.new(4), y=Offset.new(6))
    scalar = 2
    expected_result = Vector2D(x=Offset.new(2), y=Offset.new(3))
    assert vector / scalar == expected_result


def test_vector2d_negation() -> None:
    vector = Vector2D(x=Offset.new(2), y=Offset.new(3))
    expected_result = Vector2D(x=Offset.new(-2), y=Offset.new(-3))
    assert -vector == expected_result


def test_vector2d_length() -> None:
    vector = Vector2D(x=Offset.new(3), y=Offset.new(4))
    expected_length = Offset.new(5)
    assert vector.length() == expected_length


ANGLE_BETWEEN_CASES = [
    (
        Vector2D.new(0, 1),  # 12 o'clock
        Vector2D.new(0, 1),  # 12 o'clock
        0.0,
    ),
    (
        Vector2D.new(0, 1),  # 12 o'clock
        Vector2D.new(-1, 1),  # 10.30
        45.0,
    ),
    (
        Vector2D.new(0, 1),  # 12 o'clock
        Vector2D.new(-1, 0),  #  9 o'clock
        90.0,
    ),
    (
        Vector2D.new(0, 1),  # 12 o'clock
        Vector2D.new(-1, -1),  #  7.30
        135.0,
    ),
    (
        Vector2D.new(0, 1),  # 12 o'clock
        Vector2D.new(0, -1),  #  6 o'clock
        180.0,
    ),
    (
        Vector2D.new(0, 1),  # 12 o'clock
        Vector2D.new(1, -1),  #  7:30
        225.0,
    ),
    (
        Vector2D.new(0, 1),  # 12 o'clock
        Vector2D.new(1, 0),  #  9 o'clock
        270.0,
    ),
    (
        Vector2D.new(0, 1),  # 12 o'clock
        Vector2D.new(1, 1),  # 10:30
        315.0,
    ),
]


@pytest.mark.xfail(reason="Broken implementation?")
@pytest.mark.parametrize(
    ("vector0", "vector1", "expect_degrees"),
    ANGLE_BETWEEN_CASES,
)
def test_vector2d_angle_between_clockwise(
    vector0: Vector2D,
    vector1: Vector2D,
    expect_degrees: float,
) -> None:
    assert math.isclose(
        vector0.angle_between_clockwise(vector1),
        expect_degrees,
        rel_tol=1e-6,
    )


@pytest.mark.parametrize(
    ("vector0", "vector1", "expect_degrees"),
    ANGLE_BETWEEN_CASES,
)
def test_vector2d_angle_between(
    vector0: Vector2D,
    vector1: Vector2D,
    expect_degrees: float,
) -> None:
    assert math.isclose(
        vector0.angle_between(vector1),
        expect_degrees,
        rel_tol=1e-6,
    )


@pytest.mark.parametrize(
    ("vector0", "vector1", "expect_degrees"),
    [(v1, v0, ((360 - d) if d > 0 else d)) for v0, v1, d in ANGLE_BETWEEN_CASES],
)
def test_vector2d_angle_between_flipped(
    vector0: Vector2D,
    vector1: Vector2D,
    expect_degrees: float,
) -> None:
    assert math.isclose(
        vector0.angle_between(vector1),
        expect_degrees,
        rel_tol=1e-6,
    )


def test_vector2d_dot_product() -> None:
    vector1 = Vector2D(x=Offset.new(2), y=Offset.new(3))
    vector2 = Vector2D(x=Offset.new(4), y=Offset.new(5))
    expected_dot_product = Offset.new(23)
    assert vector1.dot(vector2) == expected_dot_product


def test_vector2d_determinant() -> None:
    vector1 = Vector2D(x=Offset.new(2), y=Offset.new(3))
    vector2 = Vector2D(x=Offset.new(4), y=Offset.new(5))
    expected_determinant = Offset.new(-2)
    assert vector1.determinant(vector2) == expected_determinant
