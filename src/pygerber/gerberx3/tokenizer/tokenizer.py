"""GerberX3 format tokenizer.

Parser is based on GerberX3 format described in Ucamco's `The Gerber Layer Format
Specification`.

"""
from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

from pygerber.gerberx3.tokenizer.grammar import GRAMMAR

if TYPE_CHECKING:
    from pygerber.gerberx3.tokenizer.tokens.token import Token


class Tokenizer:
    """GerberX3 format tokenizer."""

    def __init__(self, *, strict: bool = False) -> None:
        """GerberX3 format tokenizer."""
        self.grammar = GRAMMAR
        self.strict = strict

    def tokenize(self, source: str) -> TokenStack:
        """Convert source code into token stream."""
        tokens: list[Token] = []

        for token in self.grammar.parse_string(source, parse_all=self.strict):
            tokens.append(token)

        return TokenStack(tokens)


class TokenStack:
    """Token stack wrapper."""

    def __init__(self, tokens: list[Token]) -> None:
        """Initialize token stack."""
        self.stack: list[Token] = tokens

    def __iter__(self) -> Iterator[Token]:
        """Acquire token stack iterator."""
        return iter(self.stack)
