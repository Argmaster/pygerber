"""GerberX3 format parser."""

from __future__ import annotations

import logging
from enum import Enum
from typing import TYPE_CHECKING, Callable, Generator, Optional

from pygerber.backend.rasterized_2d.backend_cls import Rasterized2DBackend
from pygerber.gerberx3.parser.errors import (
    ExitParsingProcessInterrupt,
    OnUpdateDrawingStateError,
    ParserError,
)
from pygerber.gerberx3.parser.state import State

if TYPE_CHECKING:
    from pygerber.backend.abstract.backend_cls import Backend
    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
    from pygerber.backend.abstract.draw_commands_handle import DrawCommandsHandle
    from pygerber.gerberx3.tokenizer.tokens.bases.token import Token
    from pygerber.gerberx3.tokenizer.tokens.groups.ast import AST


class Parser:
    """Gerber X3 parser object."""

    def __init__(
        self,
        options: Optional[ParserOptions] = None,
    ) -> None:
        """Initialize parser.

        Parameters
        ----------
        options : ParserOptions | None
            Additional options for modifying parser behavior.

        """
        self.options = ParserOptions() if options is None else options
        self.state = (
            State()
            if self.options.initial_state is None
            else self.options.initial_state
        )
        self.draw_actions: list[DrawCommand] = []

    @property
    def backend(self) -> Backend:
        """Get reference to backend object."""
        return self.options.backend

    def parse(self, ast: AST) -> DrawCommandsHandle:
        """Parse token stack."""
        for _ in self.parse_iter(ast):
            pass

        return self.get_draw_commands_handle()

    def parse_iter(self, ast: AST) -> Generator[tuple[Token, State], None, None]:
        """Iterate over tokens in stack and parse them."""
        self.state = (
            State()
            if self.options.initial_state is None
            else self.options.initial_state
        )
        self.draw_actions = []

        try:
            for token in ast:
                self._update_drawing_state(token)

                yield token, self.state

        except ExitParsingProcessInterrupt:
            pass

    def get_draw_commands_handle(self) -> DrawCommandsHandle:
        """Return handle to drawing commands."""
        return self.backend.get_draw_commands_handle_cls()(
            self.draw_actions,
            self.backend,
        )

    def _update_drawing_state(self, token: Token) -> None:
        try:
            self.state, actions = token.update_drawing_state(self.state, self.backend)
            if actions is not None:
                self.draw_actions.extend(actions)

        except ExitParsingProcessInterrupt:
            return

        except Exception as e:
            if self.options.on_update_drawing_state_error == ParserOnErrorAction.Ignore:
                pass

            elif (
                self.options.on_update_drawing_state_error == ParserOnErrorAction.Raise
            ):
                if not isinstance(e, ParserError):
                    raise OnUpdateDrawingStateError(token) from e

                raise

            elif self.options.on_update_drawing_state_error == ParserOnErrorAction.Warn:
                logging.warning(
                    "Encountered fatal error during call to update_drawing_state() "
                    "of '%s' token %s. Parser will skip this token and continue.",
                    token,
                    token.get_token_position(),
                )
            else:
                self.options.on_update_drawing_state_error(e, self, token)


class StatePreservingParser(Parser):
    """Parser class which preserves all states for all tokens.

    Caution: High memory consumption.
    """

    state_index: list[tuple[int, State]]

    def __init__(self, options: ParserOptions | None = None) -> None:
        super().__init__(options)
        self.state_index = []

    def parse(self, ast: AST) -> DrawCommandsHandle:
        """Parse token stack."""
        self.state_index = []
        current_state = self.state

        for token, state in self.parse_iter(ast):
            if state != current_state:
                self.state_index.append((token.location, state))

        return self.get_draw_commands_handle()

    def get_state_at(self, token: Token) -> State:
        """Get state at given token.

        Parser must have been already used to parse some AST.
        """
        for location, state in self.state_index:
            if location <= token.location:
                continue
            return state

        return self.state


class ParserOnErrorAction(Enum):
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


class ParserOptions:
    """Container class for Gerber parser options."""

    def __init__(
        self,
        backend: Backend | None = None,
        initial_state: State | None = None,
        on_update_drawing_state_error: Callable[[Exception, Parser, Token], None]
        | ParserOnErrorAction = ParserOnErrorAction.Raise,
    ) -> None:
        """Initialize options."""
        self.backend = Rasterized2DBackend() if backend is None else backend
        self.initial_state = initial_state
        self.on_update_drawing_state_error = on_update_drawing_state_error
