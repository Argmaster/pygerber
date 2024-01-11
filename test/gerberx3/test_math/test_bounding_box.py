from __future__ import annotations

from decimal import Decimal

from pygerber.gerberx3.math.bounding_box import BoundingBox, Offset, Vector2D
from pygerber.gerberx3.state_enums import Unit


def test_bounding_box_from_diameter() -> None:
    diameter = Offset.new(value=Decimal("2"), unit=Unit.Millimeters)
    bbox = BoundingBox.from_diameter(diameter)
    assert bbox.max_x == Offset.new(value=Decimal("1"), unit=Unit.Millimeters)
    assert bbox.max_y == Offset.new(value=Decimal("1"), unit=Unit.Millimeters)
    assert bbox.min_x == Offset.new(value=Decimal("-1"), unit=Unit.Millimeters)
    assert bbox.min_y == Offset.new(value=Decimal("-1"), unit=Unit.Millimeters)


def test_bounding_box_from_rectangle() -> None:
    x_size = Offset.new(value=Decimal("2"), unit=Unit.Millimeters)
    y_size = Offset.new(value=Decimal("3"), unit=Unit.Millimeters)
    bbox = BoundingBox.from_rectangle(x_size, y_size)
    assert bbox.max_x == Offset.new(value=Decimal("1"), unit=Unit.Millimeters)
    assert bbox.max_y == Offset.new(value=Decimal("1.5"), unit=Unit.Millimeters)
    assert bbox.min_x == Offset.new(value=Decimal("-1"), unit=Unit.Millimeters)
    assert bbox.min_y == Offset.new(value=Decimal("-1.5"), unit=Unit.Millimeters)


def test_bounding_box_width() -> None:
    bbox = BoundingBox(
        max_x=Offset.new(value=Decimal("2"), unit=Unit.Millimeters),
        max_y=Offset.new(value=Decimal("3"), unit=Unit.Millimeters),
        min_x=Offset.new(value=Decimal("-1"), unit=Unit.Millimeters),
        min_y=Offset.new(value=Decimal("-2"), unit=Unit.Millimeters),
    )
    assert bbox.width == Offset.new(value=Decimal("3"), unit=Unit.Millimeters)


def test_bounding_box_height() -> None:
    bbox = BoundingBox(
        max_x=Offset.new(value=Decimal("2"), unit=Unit.Millimeters),
        max_y=Offset.new(value=Decimal("3"), unit=Unit.Millimeters),
        min_x=Offset.new(value=Decimal("-1"), unit=Unit.Millimeters),
        min_y=Offset.new(value=Decimal("-2"), unit=Unit.Millimeters),
    )
    assert bbox.height == Offset.new(value=Decimal("5"), unit=Unit.Millimeters)


def test_bounding_box_get_size() -> None:
    bbox = BoundingBox(
        max_x=Offset.new(value=Decimal("2"), unit=Unit.Millimeters),
        max_y=Offset.new(value=Decimal("3"), unit=Unit.Millimeters),
        min_x=Offset.new(value=Decimal("-1"), unit=Unit.Millimeters),
        min_y=Offset.new(value=Decimal("-2"), unit=Unit.Millimeters),
    )
    size = bbox.get_size()
    assert size.x == Offset.new(value=Decimal("3"), unit=Unit.Millimeters)
    assert size.y == Offset.new(value=Decimal("5"), unit=Unit.Millimeters)


def test_bounding_box_center() -> None:
    bbox = BoundingBox(
        max_x=Offset.new(value=Decimal("2"), unit=Unit.Millimeters),
        max_y=Offset.new(value=Decimal("3"), unit=Unit.Millimeters),
        min_x=Offset.new(value=Decimal("-1"), unit=Unit.Millimeters),
        min_y=Offset.new(value=Decimal("-2"), unit=Unit.Millimeters),
    )
    center = bbox.center
    assert center.x == Offset.new(value=Decimal("0.5"), unit=Unit.Millimeters)
    assert center.y == Offset.new(value=Decimal("0.5"), unit=Unit.Millimeters)


def test_bounding_box_include_point() -> None:
    bbox = BoundingBox(
        max_x=Offset.new(value=Decimal("2"), unit=Unit.Millimeters),
        max_y=Offset.new(value=Decimal("3"), unit=Unit.Millimeters),
        min_x=Offset.new(value=Decimal("-1"), unit=Unit.Millimeters),
        min_y=Offset.new(value=Decimal("-2"), unit=Unit.Millimeters),
    )
    point = Vector2D(
        x=Offset.new(value=Decimal("0"), unit=Unit.Millimeters),
        y=Offset.new(value=Decimal("1"), unit=Unit.Millimeters),
    )
    new_bbox = bbox.include_point(point)
    assert new_bbox.max_x == Offset.new(value=Decimal("2"), unit=Unit.Millimeters)
    assert new_bbox.max_y == Offset.new(value=Decimal("3"), unit=Unit.Millimeters)
    assert new_bbox.min_x == Offset.new(value=Decimal("-1"), unit=Unit.Millimeters)
    assert new_bbox.min_y == Offset.new(value=Decimal("-2"), unit=Unit.Millimeters)


def test_bounding_box_as_pixel_box() -> None:
    bbox = BoundingBox(
        max_x=Offset.new(value=Decimal("2"), unit=Unit.Millimeters),
        max_y=Offset.new(value=Decimal("3"), unit=Unit.Millimeters),
        min_x=Offset.new(value=Decimal("-1"), unit=Unit.Millimeters),
        min_y=Offset.new(value=Decimal("-2"), unit=Unit.Millimeters),
    )
    pixel_box = bbox.as_pixel_box(dpi=300, dx_max=10, dy_max=20, dx_min=5, dy_min=15)
    assert pixel_box == (-6, -8, 33, 55)


def test_bounding_box_add() -> None:
    bbox1 = BoundingBox(
        max_x=Offset.new(value=Decimal("2"), unit=Unit.Millimeters),
        max_y=Offset.new(value=Decimal("3"), unit=Unit.Millimeters),
        min_x=Offset.new(value=Decimal("-1"), unit=Unit.Millimeters),
        min_y=Offset.new(value=Decimal("-2"), unit=Unit.Millimeters),
    )
    bbox2 = BoundingBox(
        max_x=Offset.new(value=Decimal("1"), unit=Unit.Millimeters),
        max_y=Offset.new(value=Decimal("2"), unit=Unit.Millimeters),
        min_x=Offset.new(value=Decimal("-2"), unit=Unit.Millimeters),
        min_y=Offset.new(value=Decimal("-3"), unit=Unit.Millimeters),
    )
    result = bbox1 + bbox2
    assert result.max_x == Offset.new(value=Decimal("2"), unit=Unit.Millimeters)
    assert result.max_y == Offset.new(value=Decimal("3"), unit=Unit.Millimeters)
    assert result.min_x == Offset.new(value=Decimal("-2"), unit=Unit.Millimeters)
    assert result.min_y == Offset.new(value=Decimal("-3"), unit=Unit.Millimeters)
