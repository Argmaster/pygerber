from __future__ import annotations

from pygerber.gerberx3.api import (
    ColorScheme,
    Rasterized2DLayer,
    Rasterized2DLayerParams,
)

source_code = """
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
"""

Rasterized2DLayer(
    options=Rasterized2DLayerParams(
        source_code=source_code,
        colors=ColorScheme.SILK,
        dpi=3000,
    ),
).render().save("output.png")
