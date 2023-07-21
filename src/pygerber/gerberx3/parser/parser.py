"""GerberX3 format parser."""


from __future__ import annotations

import logging
from enum import Enum
from typing import Callable, Generator, Optional

from pygerber.backend import BackendName
from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.draw_list import DrawList
from pygerber.gerberx3.parser.errors import OnCreateDrawActionError, ParserError
from pygerber.gerberx3.parser.state import State
from pygerber.gerberx3.tokenizer.tokenizer import TokenStack
from pygerber.gerberx3.tokenizer.tokens.token import Token


class Parser:
    """Gerber X3 parser object."""

    def __init__(
        self,
        tokens: TokenStack,
        options: Optional[ParserOptions] = None,
    ) -> None:
        """Initialize parser.

        Parameters
        ----------
        tokens : TokenStack
            Gerber X3 tokens retrieved with Tokenizer.
        options : ParserOptions | None
            Additional options for modifying parser behavior.
        """
        self.tokens = tokens
        self.options = ParserOptions() if options is None else options
        self.state = (
            State()
            if self.options.initial_state is None
            else self.options.initial_state
        )
        self.operations: DrawList = DrawList()

    def parse(self) -> DrawList:
        """Parse token stack."""
        for _ in self.parse_iter():
            pass

        return self.operations

    def parse_iter(self) -> Generator[Token, None, None]:
        """Iterate over tokens in stack and parse them."""
        for token in self.tokens:
            self._update_drawing_state(token)
            self._create_draw_action(token)

            yield token

    def _update_drawing_state(self, token: Token) -> None:
        try:
            self.state = token.update_drawing_state(self.state)
        except Exception as e:  # noqa: BLE001
            if self.options.on_update_drawing_state_error == ParserOnErrorAction.Ignore:
                pass

            elif (
                self.options.on_update_drawing_state_error == ParserOnErrorAction.Raise
            ):
                if not isinstance(e, ParserError):
                    raise OnCreateDrawActionError from e

                raise

            elif self.options.on_update_drawing_state_error == ParserOnErrorAction.Warn:
                logging.warning(
                    "Encountered fatal error during call to create_draw_action() "
                    "of '%s' token. Parser will skip this token and continue.",
                    token,
                )
            else:
                self.options.on_update_drawing_state_error(e, self, token)

    def _create_draw_action(self, token: Token) -> None:
        try:
            action = token.create_draw_action(self.state)
            if action is not None:
                self.operations.append(action)

        except Exception as e:  # noqa: BLE001
            if self.options.on_create_draw_action_error == ParserOnErrorAction.Ignore:
                pass

            elif self.options.on_create_draw_action_error == ParserOnErrorAction.Raise:
                if not isinstance(e, ParserError):
                    raise OnCreateDrawActionError from e

                raise

            elif self.options.on_create_draw_action_error == ParserOnErrorAction.Warn:
                logging.warning(
                    "Encountered fatal error during call to create_draw_action() "
                    "of '%s' token. Parser will skip this token and continue.",
                    token,
                )
            else:
                self.options.on_create_draw_action_error(e, self, token)


class ParserOnErrorAction(Enum):
    """Possible error actions."""

    Ignore = "ignore"
    Warn = "warn"
    Raise = "raise"


class ParserOptions:
    """Container class for Gerber parser options."""

    def __init__(
        self,
        backend: BackendName | str | Backend = BackendName.Rasterized2D,
        initial_state: Optional[State] = None,
        on_update_drawing_state_error: Callable[[Exception, Parser, Token], None]
        | ParserOnErrorAction = ParserOnErrorAction.Raise,
        on_create_draw_action_error: Callable[[Exception, Parser, Token], None]
        | ParserOnErrorAction = ParserOnErrorAction.Raise,
    ) -> None:
        """Initialize options."""
        self.backend = (
            BackendName.get_backend_class(backend)()
            if not isinstance(backend, Backend)
            else backend
        )
        self.initial_state = initial_state
        self.on_update_drawing_state_error = on_update_drawing_state_error
        self.on_create_draw_action_error = on_create_draw_action_error
