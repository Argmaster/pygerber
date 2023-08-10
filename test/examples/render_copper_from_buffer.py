from __future__ import annotations

from io import BytesIO

from pygerber.gerberx3.api.color_scheme import ColorScheme
from pygerber.gerberx3.api.layers import Rasterized2DLayer, Rasterized2DLayerParams


def render() -> None:
    source_buffer = BytesIO(
        b"""
    %FSLAX26Y26*%
    %MOMM*%
    %ADD100R,1.5X1.0X0.5*%
    %ADD200C,1.5X1.0*%
    %ADD300O,1.5X1.0X0.6*%
    %ADD400P,1.5X3X5.0*%
    D100*
    X0Y0D03*
    D200*
    X0Y2000000D03*
    D300*
    X2000000Y0D03*
    D400*
    X2000000Y2000000D03*
    M02*
    """,
    )

    Rasterized2DLayer(
        options=Rasterized2DLayerParams(
            source_buffer=source_buffer,
            colors=ColorScheme.COPPER_ALPHA,
        ),
    ).render().save("output.png")


if __name__ == "__main__":
    render()
