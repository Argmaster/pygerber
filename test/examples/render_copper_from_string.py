from __future__ import annotations

from pygerber.gerberx3.api import (
    ColorScheme,
    Rasterized2DLayer,
    Rasterized2DLayerParams,
)


def render() -> None:
    source_code = """
    %FSLAX26Y26*%
    %MOMM*%
    %ADD100C,1.5*%
    D100*
    X0Y0D03*
    M02*
    """

    Rasterized2DLayer(
        options=Rasterized2DLayerParams(
            source_code=source_code,
            colors=ColorScheme.COPPER_ALPHA,
        ),
    ).render().save("output.png")


if __name__ == "__main__":
    render()
