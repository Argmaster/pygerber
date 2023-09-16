"""Tests for Vector2D class."""
from __future__ import annotations

import math

import pytest

from pygerber.gerberx3.math.vector_2d import Vector2D

DATA = [
    (  # 1
        Vector2D.new(x=1.0, y=1.0),  # 1:30 o'clock
        Vector2D.new(x=-1.0, y=-1.0),  # 7:30 o'clock
        180,
    ),
    (  # 2
        Vector2D.new(x=-1.0, y=-1.0),  # 7:30 o'clock
        Vector2D.new(x=1.0, y=1.0),  # 1:30 o'clock
        180,
    ),
    # ---
    (  # 3
        Vector2D.new(x=1.0, y=0.0),  # 3:00 o'clock
        Vector2D.new(x=-1.0, y=0.0),  # 9:00 o'clock
        180,
    ),
    (  # 4
        Vector2D.new(x=-1.0, y=0.0),  # 3:00 o'clock
        Vector2D.new(x=1.0, y=0.0),  # 9:00 o'clock
        180,
    ),
    # ---
    (  # 5
        Vector2D.new(x=1.0, y=0.0),  # 3:00 o'clock
        Vector2D.new(x=0.0, y=1.0),  # 12:00 o'clock
        270,
    ),
    (
        Vector2D.new(x=1.0, y=0.0),  # 3:00 o'clock
        Vector2D.new(x=0.0, y=-1.0),  # 6:00 o'clock
        90,
    ),
    (
        Vector2D.new(x=-1.0, y=0.0),  # 9:00 o'clock
        Vector2D.new(x=0.0, y=1.0),  # 12:00 o'clock
        90,
    ),
    (
        Vector2D.new(x=-1.0, y=0.0),  # 9:00 o'clock
        Vector2D.new(x=0.0, y=-1.0),  # 6:00 o'clock
        270,
    ),
    # ---
    (
        Vector2D.new(x=0.0, y=1.0),  # 12:00 o'clock
        Vector2D.new(x=0.0, y=-1.0),  # 6:00 o'clock
        180,
    ),
    (
        Vector2D.new(x=0.0, y=-1.0),  # 6:00 o'clock
        Vector2D.new(x=0.0, y=1.0),  # 12:00 o'clock
        180,
    ),
    # ---
    (
        Vector2D.new(x=-1.0, y=-1.0),  # 7:30 o'clock
        Vector2D.new(x=1.0, y=0.0),  # 3:00 o'clock
        225,
    ),
    (
        Vector2D.new(x=1.0, y=0.0),  # 3:00 o'clock
        Vector2D.new(x=-1.0, y=-1.0),  # 7:30 o'clock
        135,
    ),
]


# Assume clockwise
@pytest.mark.parametrize(
    ("a", "b", "angle"),
    DATA,
    ids=[
        f"{i[0].__pytest_alias__()} | {i[1].__pytest_alias__()} | {i[2]}" for i in DATA
    ],
)
def test_angle_starting_from_vector_a_towards_vector_b(
    a: Vector2D,
    b: Vector2D,
    angle: float,
) -> None:
    """Test if angle_between_clockwise() method works correctly."""
    retval_angle = angle_starting_from_vector_a_towards_vector_b(a, b)
    assert retval_angle == angle


def angle_starting_from_vector_a_towards_vector_b(
    a: Vector2D,
    b: Vector2D,
) -> float:
    """Calculate angle between two vectors in degrees clockwise."""
    a_normalized = a / a.length()
    b_normalized = b / b.length()

    dot = b_normalized.dot(a_normalized)

    theta = math.acos(dot)

    if ((a_normalized.y * b_normalized.y) > 0) or (
        (a_normalized.x * b_normalized.x) < 0
    ):
        return math.degrees(theta)

    return math.degrees(math.tau - theta)
