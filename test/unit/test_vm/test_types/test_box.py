from __future__ import annotations

from typing import cast

import pytest

from pygerber.vm.types.box import Box
from pygerber.vm.types.vector import Vector


def test_box_from_vectors() -> None:
    vectors = [Vector(x=1, y=2), Vector(x=3, y=4), Vector(x=-1, y=-2)]
    box = Box.from_vectors(*vectors)
    assert box.min_x == -1
    assert box.min_y == -2  # noqa: PLR2004
    assert box.max_x == 3  # noqa: PLR2004
    assert box.max_y == 4  # noqa: PLR2004


def test_box_from_center_width_height() -> None:
    box = Box.from_center_width_height(center=(0, 0), width=4, height=6)
    assert box.min_x == -2  # noqa: PLR2004
    assert box.min_y == -3  # noqa: PLR2004
    assert box.max_x == 2  # noqa: PLR2004
    assert box.max_y == 3  # noqa: PLR2004


def test_box_width() -> None:
    min_x = 1
    min_y = 2
    max_x = 5
    max_y = 6
    box = Box(min_x=min_x, min_y=min_y, max_x=max_x, max_y=max_y)

    assert box.width == max_x - min_x


def test_box_height() -> None:
    min_x = 1
    min_y = 2
    max_x = 5
    max_y = 6
    box = Box(min_x=min_x, min_y=min_y, max_x=max_x, max_y=max_y)

    assert box.height == max_y - min_y


def test_box_center() -> None:
    min_x = 1
    min_y = 2
    max_x = 5
    max_y = 6
    box = Box(min_x=min_x, min_y=min_y, max_x=max_x, max_y=max_y)

    assert box.center.x == (max_x + min_x) / 2
    assert box.center.y == (max_y + min_y) / 2


def test_box_add_vector() -> None:
    min_x = 1
    min_y = 2
    max_x = 5
    max_y = 6
    box = Box(min_x=min_x, min_y=min_y, max_x=max_x, max_y=max_y)
    vector = Vector(x=1, y=1)
    new_box = box + vector

    assert new_box.min_x == min_x + vector.x
    assert id(new_box) != id(box)


def test_box_subtract_vector() -> None:
    box = Box(min_x=1, min_y=2, max_x=5, max_y=6)
    vector = Vector(x=1, y=1)
    new_box = box - vector
    assert new_box.min_x == 0
    assert new_box.min_y == 1
    assert new_box.max_x == 4  # noqa: PLR2004
    assert new_box.max_y == 5  # noqa: PLR2004


def test_box_add_box() -> None:
    box1 = Box(min_x=1, min_y=2, max_x=5, max_y=6)
    box2 = Box(min_x=0, min_y=1, max_x=4, max_y=5)
    new_box = box1 + box2
    assert new_box.min_x == 0
    assert new_box.min_y == 1
    assert new_box.max_x == 5  # noqa: PLR2004
    assert new_box.max_y == 6  # noqa: PLR2004


def test_box_subtract_box() -> None:
    box1 = Box(min_x=1, min_y=2, max_x=5, max_y=6)
    box2 = Box(min_x=0, min_y=1, max_x=4, max_y=5)

    with pytest.raises(TypeError):
        assert box1 - box2


def test_box_add_other() -> None:
    box = Box(min_x=1, min_y=2, max_x=5, max_y=6)
    other = 1

    with pytest.raises(TypeError):
        assert box + other


def test_iadd() -> None:
    min_x = 1
    min_y = 2
    max_x = 5
    max_y = 6
    box = Box(min_x=min_x, min_y=min_y, max_x=max_x, max_y=max_y)
    vector = Vector(x=1, y=1)
    box_original = box
    box += vector

    assert box.min_x == min_x + vector.x
    assert id(box_original) != id(box)


def test_radd() -> None:
    min_x = 1
    min_y = 2
    max_x = 5
    max_y = 6
    box = Box(min_x=min_x, min_y=min_y, max_x=max_x, max_y=max_y)
    vector = Vector(x=1, y=1)
    box_original = box
    box: Box = cast(Box, vector + box)

    assert box.min_x == min_x + vector.x
    assert id(box_original) != id(box)


def test_isub() -> None:
    box = Box(min_x=1, min_y=2, max_x=5, max_y=6)
    vector = Vector(x=1, y=1)
    box_original = box
    box -= vector

    assert box.min_x == 0
    assert box.min_y == 1
    assert box.max_x == 4  # noqa: PLR2004
    assert box.max_y == 5  # noqa: PLR2004
    assert id(box_original) != id(box)
