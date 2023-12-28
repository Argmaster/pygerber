"""Decorators for reducing boilerplate required to implement token features."""
from __future__ import annotations

from typing import Callable, Generic, Optional, Type, TypeVar

from pygerber.gerberx3.parser2.context2 import Parser2Context
from pygerber.gerberx3.revisions import Revision, Revision202308
from pygerber.gerberx3.tokenizer.tokens.bases.token import Token

T = TypeVar("T")
TokenT = TypeVar("TokenT", bound=Token)


class UseType(Generic[T]):
    """Placeholder for passing type parameter specification as param."""


class UpdateDrawingState2Property(Generic[TokenT]):
    """Decorator class speeding up process of adding simple state updates to tokens."""

    def __init__(
        self,
        method: Callable[[Parser2Context, T], None],
        getter: Callable[[TokenT], T],
        _use_type: Optional[Type[UseType[TokenT]]] = None,
    ) -> None:
        self.method = method
        self.getter = getter

    def __call__(self, class_: type[TokenT]) -> type[TokenT]:
        """Add update_drawing_state2() method."""
        this = self
        original_parser2_visit_token = class_.parser2_visit_token

        def parser2_visit_token(
            self: TokenT,
            context: Parser2Context,
        ) -> None:
            original_parser2_visit_token(self, context)
            return this.method(context, this.getter(self))

        class_.parser2_visit_token = parser2_visit_token
        return class_


class AddHookCall:
    """Add hook call to parser2_visit_token() dispatch.

    Actions added by decorators are called in reverse order than decorators being called
    on class. Therefore, when recording hook calls post_*() hook call should be added
    last and pre_*() hooks should be added first.
    """

    def __init__(
        self,
        hook: Callable[[Parser2Context], None],
        _use_type: Optional[Type[UseType[TokenT]]] = None,
    ) -> None:
        self.hook = hook

    def __call__(self, class_: type[TokenT]) -> type[TokenT]:
        """Add update_drawing_state2() method."""
        this = self
        original_parser2_visit_token = class_.parser2_visit_token

        def parser2_visit_token(
            self: TokenT,
            context: Parser2Context,
        ) -> None:
            this.hook(context)
            return original_parser2_visit_token(self, context)

        class_.parser2_visit_token = parser2_visit_token
        return class_


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
