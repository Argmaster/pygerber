"""Wrapper for G70 token."""
from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.dnn_select_aperture import DNNSelectAperture


class G54SelectAperture(DNNSelectAperture):
    """Wrapper for G54DNN token.

    Select aperture.

    This historic code optionally precedes an aperture selection Dnn command. It has no
    effect. Sometimes used. Deprecated in 2012.
    """

    def __str__(self) -> str:
        return f"G54{self.aperture_id}*"
