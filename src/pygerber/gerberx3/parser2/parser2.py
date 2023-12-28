"""Implementation of Gerber AST parser, version 2."""
from __future__ import annotations

import logging
from enum import Enum
from typing import Generator, Optional

from pydantic import Field

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.gerberx3.parser.errors import ExitParsingProcessInterrupt
from pygerber.gerberx3.parser2.command_buffer2 import CommandBuffer2
from pygerber.gerberx3.parser2.context2 import Parser2Context, Parser2ContextOptions
from pygerber.gerberx3.parser2.errors2 import OnUpdateDrawingState2Error, Parser2Error
from pygerber.gerberx3.parser2.hooks2 import Hooks2
from pygerber.gerberx3.tokenizer.tokens.bases.token import Token
from pygerber.gerberx3.tokenizer.tokens.groups.ast import AST


class Parser2:
    """Gerber AST parser, version 2."""

    def __init__(
        self,
        options: Optional[Parser2Options] = None,
    ) -> None:
        """Initialize parser.

        Parameters
        ----------
        options : ParserOptions | None
            Additional options for modifying parser behavior.
        """
        self.options = Parser2Options() if options is None else options
        self.is_used = False
        self.context = Parser2Context()

    def parse(self, ast: AST) -> CommandBuffer2:
        """Parse token stack."""
        for _ in self.parse_iter(ast):
            pass

        return self.context.command_buffer

    def parse_iter(
        self,
        ast: AST,
    ) -> Generator[tuple[Token, Parser2Context], None, None]:
        """Iterate over tokens in stack and parse them."""
        self.is_used = True

        try:
            for token in ast:
                self.context.set_current_token(token)
                self._token_try_visit_except(token)

                yield token, self.context

        except ExitParsingProcessInterrupt:
            pass

    def _token_try_visit_except(self, token: Token) -> None:
        try:
            self.get_hooks().pre_parser_visit_token(self.context)
            token.parser2_visit_token(self.context)
            self.get_hooks().post_parser_visit_token(self.context)

        except ExitParsingProcessInterrupt:
            return

        except Exception as e:  # noqa: BLE001
            if (
                self.options.on_update_drawing_state_error
                == Parser2OnErrorAction.Ignore
            ):
                pass

            elif (
                self.options.on_update_drawing_state_error == Parser2OnErrorAction.Raise
            ):
                if not isinstance(e, Parser2Error):
                    raise OnUpdateDrawingState2Error(token) from e

                raise

            elif (
                self.options.on_update_drawing_state_error == Parser2OnErrorAction.Warn
            ):
                logging.warning(
                    "Encountered fatal error during call to update_drawing_state() "
                    "of '%s' token %s. Parser will skip this token and continue.",
                    token,
                    token.get_token_position(),
                )

            elif (
                self.options.on_update_drawing_state_error
                == Parser2OnErrorAction.UseHook
            ):
                if isinstance(e, Parser2Error):
                    self.get_hooks().on_parser_error(self.context, e)
                else:
                    self.get_hooks().on_other_error(self.context, e)

    def get_hooks(self) -> Hooks2:
        """Get hooks object."""
        return self.context.get_hooks()


class Parser2OnErrorAction(Enum):
    """Possible error actions."""

    Ignore = "ignore"
    """Ignore parser errors. Errors which occurred will not be signaled. May yield
    unexpected results for broken files, with missing draw commands or even more
    significant errors."""

    Warn = "warn"
    """Warn on parser error. Parser will log warning message about what went wrong.
    Best for supporting wide range of files without silently ignoring errors in code."""

    Raise = "raise"
    """Raise exception whenever parser encounters error. Will completely break out of
    parsing process, making it impossible to render slightly malformed files."""

    UseHook = "use_hook"
    """Use appropriate hooks to dispatch exception."""


class Parser2Options(FrozenGeneralModel):
    """Container class for Gerber parser options."""

    context_options: Optional[Parser2ContextOptions] = Field(default=None)
    on_update_drawing_state_error: Parser2OnErrorAction = Parser2OnErrorAction.Raise
