"""PyGerber's Gerber language server state."""

from __future__ import annotations

from functools import cached_property
from hashlib import sha256
from pathlib import Path
from typing import Callable

from pygls import uris

from pygerber.gerberx3.language_server._internals.errors import EmptyASTError
from pygerber.gerberx3.parser.parser import Parser
from pygerber.gerberx3.parser.state import State
from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer
from pygerber.gerberx3.tokenizer.tokens.bases.token import Token
from pygerber.gerberx3.tokenizer.tokens.groups.ast import AST

MAX_CACHE_SIZE = 64


class LanguageServerState:
    """Container class instantiated per-language server."""

    def __init__(self) -> None:
        self.file_state: dict[bytes, FileServerState] = {}

    def get_by_uri(self, uri: str) -> FileServerState:
        content = self.get_file_content(uri)
        return self.get_by_file_content(content)

    def get_file_content(self, uri: str) -> str:
        """Get file source."""
        file_system_path = uris.to_fs_path(uri)

        if file_system_path is None:
            raise FileNotFoundError

        return Path(file_system_path).read_text(encoding="utf-8")

    def get_by_file_content(self, source: str) -> FileServerState:
        """Get per file state."""
        source_sha = sha256(source.encode("utf-8")).digest()
        state = self.file_state.get(source_sha, None)

        if state is None:
            while len(self.file_state) > MAX_CACHE_SIZE:
                self.file_state.popitem()

            self.file_state[source_sha] = state = FileServerState(source)

        return state


class FileServerState:
    """Container class instantiated per file content."""

    def __init__(self, source: str) -> None:
        self.source = source
        self.tokenizer = Tokenizer()
        self.parser = Parser()

    def tokenize(self) -> AST:
        """Tokenize file content."""
        return self._tokenize

    @cached_property
    def _tokenize(self) -> AST:
        """Tokenize file content."""
        return self.tokenizer.tokenize(self.source)

    def parse_until(
        self,
        condition: Callable[[Token, State], bool] = lambda *_: False,
    ) -> tuple[Token, State]:
        """Parse content of file and create token to state map.

        Optionally you can provide condition which will be check for every parsed token.
        When condition returns True, parsing will stop and return current token and
        state.
        """
        ast = self.tokenize()

        for token, state in self.parser.parse_iter(ast):
            if condition(token, state):
                return token, state

        if len(ast):
            return token, state  # type: ignore[pylance]

        raise EmptyASTError
