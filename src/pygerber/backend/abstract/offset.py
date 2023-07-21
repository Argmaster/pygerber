"""Offset representation used by drawing backend."""

from __future__ import annotations


class Offset:
    """Class representing offset in 2D space."""

    def as_millimeters(self) -> None:
        """Offset in millimeters."""
        raise NotImplementedError

    def as_inches(self) -> None:
        """Offset in millimeters."""
        raise NotImplementedError

    def as_pixels(self) -> None:
        """Offset in pixels with respect to drawing DPI."""
        raise NotImplementedError


class OffsetFromMillimeters:
    """Class representing offset in 2D space with internal value in millimeters."""


class OffsetFromInches:
    """Class representing offset in 2D space with internal value in inches."""
