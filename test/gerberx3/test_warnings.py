"""Test warnings in code."""

from __future__ import annotations

import logging
from decimal import Decimal
from typing import TYPE_CHECKING
from unittest.mock import MagicMock

from pygerber.backend.rasterized_2d.draw_commands.draw_bounding_box import (
    Rasterized2DApertureDrawBoundingBox,
)
from pygerber.backend.rasterized_2d.draw_commands.draw_circle import (
    Rasterized2DApertureDrawCircle,
)
from pygerber.backend.rasterized_2d.draw_commands.draw_polygon import (
    Rasterized2DApertureDrawPolygon,
)
from pygerber.backend.rasterized_2d.draw_commands.draw_rectangle import (
    Rasterized2DApertureDrawRectangle,
)
from pygerber.backend.rasterized_2d.draw_commands.draw_region import (
    Rasterized2DDrawRegion,
)
from pygerber.backend.rasterized_2d.drawing_target import Rasterized2DDrawingTarget
from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.state_enums import Polarity

if TYPE_CHECKING:
    import pytest


class TestRasterized2DWarnings:
    def test_draw_circle_zero_surface(self, caplog: pytest.LogCaptureFixture) -> None:
        caplog.set_level(logging.WARNING)

        class MockTarget(Rasterized2DDrawingTarget):
            pass

        cmd = Rasterized2DApertureDrawCircle(
            MagicMock(dpi=0),
            polarity=Polarity.Clear,
            center_position=Vector2D.NULL,
            diameter=Offset.new(2.0),
        )

        with caplog.at_level(logging.WARNING):
            cmd.draw(
                MockTarget(
                    coordinate_origin=Vector2D.NULL,
                    bounding_box=MagicMock(),
                    target_image=MagicMock(),
                ),
            )

        assert "Drawing zero surface circle. DPI may be too low." in caplog.text

    def test_draw_rectangle_zero_surface(
        self,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        caplog.set_level(logging.WARNING)

        class MockTarget(Rasterized2DDrawingTarget):
            pass

        cmd = Rasterized2DApertureDrawRectangle(
            MagicMock(dpi=0),
            polarity=Polarity.Clear,
            center_position=Vector2D.NULL,
            x_size=Offset.new(2.0),
            y_size=Offset.new(2.0),
        )

        with caplog.at_level(logging.WARNING):
            cmd.draw(
                MockTarget(
                    coordinate_origin=Vector2D.NULL,
                    bounding_box=MagicMock(),
                    target_image=MagicMock(),
                ),
            )

        assert "Drawing zero surface rectangle. DPI may be too low." in caplog.text

    def test_draw_polygon_number_of_vertices(
        self,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        caplog.set_level(logging.WARNING)

        class MockTarget(Rasterized2DDrawingTarget):
            pass

        cmd = Rasterized2DApertureDrawPolygon(
            MagicMock(dpi=0),
            polarity=Polarity.Clear,
            center_position=Vector2D.NULL,
            outer_diameter=Offset.new(0.0),
            number_of_vertices=0,
            rotation=Decimal("0.0"),
        )

        with caplog.at_level(logging.WARNING):
            cmd.draw(
                MockTarget(
                    coordinate_origin=Vector2D.NULL,
                    bounding_box=MagicMock(),
                    target_image=MagicMock(),
                ),
            )

        assert "Drawing invalid polygon, number of vertices < 3" in caplog.text

    def test_draw_polygon_zero_surface(
        self,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        caplog.set_level(logging.WARNING)

        class MockTarget(Rasterized2DDrawingTarget):
            pass

        cmd = Rasterized2DApertureDrawPolygon(
            MagicMock(dpi=0),
            polarity=Polarity.Clear,
            center_position=Vector2D.NULL,
            outer_diameter=Offset.new(0.0),
            number_of_vertices=3,
            rotation=Decimal("0.0"),
        )

        with caplog.at_level(logging.WARNING):
            cmd.draw(
                MockTarget(
                    coordinate_origin=Vector2D.NULL,
                    bounding_box=MagicMock(),
                    target_image=MagicMock(),
                ),
            )

        assert "Drawing zero surface polygon. DPI may be too low." in caplog.text

    def test_draw_region_number_of_vertices(
        self,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        caplog.set_level(logging.WARNING)

        class MockTarget(Rasterized2DDrawingTarget):
            pass

        cmd = Rasterized2DDrawRegion(
            MagicMock(dpi=0),
            polarity=Polarity.Clear,
            region_boundary_points=[],
        )

        with caplog.at_level(logging.WARNING):
            cmd.draw(
                MockTarget(
                    coordinate_origin=Vector2D.NULL,
                    bounding_box=MagicMock(),
                    target_image=MagicMock(),
                ),
            )

        assert "Drawing invalid region, number of vertices < 3" in caplog.text

    def test_draw_bounding_box_zero_surface(
        self,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        caplog.set_level(logging.WARNING)

        class MockTarget(Rasterized2DDrawingTarget):
            pass

        cmd = Rasterized2DApertureDrawBoundingBox(
            MagicMock(dpi=0),
            polarity=Polarity.Clear,
            bounding_box=BoundingBox.NULL,
            outline_padding=Offset.NULL,
        )

        with caplog.at_level(logging.WARNING):
            cmd.draw(
                MockTarget(
                    coordinate_origin=Vector2D.NULL,
                    bounding_box=MagicMock(),
                    target_image=MagicMock(),
                ),
            )

        assert "Drawing zero surface bounding box. DPI may be too low." in caplog.text
