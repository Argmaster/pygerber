"""Implementation of hooks for Gerber AST Parser, version 2."""
# ruff: noqa: D401
from __future__ import annotations

from pygerber.gerberx3.parser2.context2 import Parser2Context
from pygerber.gerberx3.parser2.ihooks import IHooks
from pygerber.gerberx3.tokenizer.tokens.ln_load_name import LoadName
from pygerber.gerberx3.tokenizer.tokens.ta_aperture_attribute import ApertureAttribute
from pygerber.gerberx3.tokenizer.tokens.tf_file_attribute import FileAttribute


class Parser2Hooks(IHooks):
    """Implementation of hooks for Gerber AST Parser, version 2."""

    class FileAttributeHooks(IHooks.FileAttributeHooks):
        """Hooks for visiting file attribute token (TF)."""

        def on_parser_visit_token(
            self,
            token: FileAttribute,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.
            """
            context.set_file_attribute(token.name, ",".join(token.value))
            return super().on_parser_visit_token(token, context)

    class ApertureAttributeHooks(IHooks.ApertureAttributeHooks):
        """Hooks for visiting aperture attribute token (TA)."""

        def on_parser_visit_token(
            self,
            token: ApertureAttribute,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.
            """
            context.get_current_aperture_mutable_proxy().set_attribute(
                token.name,
                ",".join(token.value),
            )
            return super().on_parser_visit_token(token, context)

    class LoadNameTokenHooks(IHooks.LoadNameTokenHooks):
        """Hooks for visiting load name token (LN)."""

        def on_parser_visit_token(
            self,
            token: LoadName,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.
            """
            context.set_file_name(token.content)
            return super().on_parser_visit_token(token, context)
