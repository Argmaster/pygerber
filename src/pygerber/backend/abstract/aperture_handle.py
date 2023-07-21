"""Aperture Handle base class which represents Gerber X3 aperture."""

from __future__ import annotations

from pydantic import BaseModel


class ApertureHandle(BaseModel):
    """Base class for creating Gerber X3 apertures."""
