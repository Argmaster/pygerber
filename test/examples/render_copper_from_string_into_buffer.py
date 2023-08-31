from __future__ import annotations

from io import BytesIO

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

    output = BytesIO()
    Rasterized2DLayer(
        options=Rasterized2DLayerParams(
            source_code=source_code,
            colors=ColorScheme.COPPER_ALPHA,
        ),
    ).render().save(output, format="png")

    output.seek(0)
    content = output.read()
    assert len(content) > 0


if __name__ == "__main__":
    render()
