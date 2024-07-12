from __future__ import annotations

import math

import pytest

from pygerber.vm.types.vector import Vector

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
