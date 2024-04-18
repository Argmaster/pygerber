"""Decorators for reducing boilerplate required to implement token features."""

from __future__ import annotations

from typing import Generic, TypeVar

from pygerber.gerberx3.revisions import Revision, Revision202308
from pygerber.gerberx3.tokenizer.tokens.bases.token import Token

T = TypeVar("T")
TokenT = TypeVar("TokenT", bound=Token)


class UseType(Generic[T]):
    """Placeholder for passing type parameter specification as param."""


class AnnotateSpecSection:
    """Add Gerber specification reference link to docstring."""

    def __init__(self, spec_section: Revision202308) -> None:
        self.spec_section = spec_section

    def __call__(self, class_: type[TokenT]) -> type[TokenT]:
        """Update docstring with specification reference."""
        class_.__doc__ = (class_.__doc__ or "") + (
            "\n\n"
            f"See section {self.spec_section.get_sec_id()} of "
            "The Gerber Layer Format Specification "
            f"{Revision.Revision_2023_08} - "
            f"{self.spec_section.get_url()}"
        )
        return class_
