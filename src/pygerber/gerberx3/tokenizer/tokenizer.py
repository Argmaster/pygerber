"""GerberX3 format tokenizer.

Parser is based on GerberX3 format described in Ucamco's `The Gerber Layer Format
Specification`.

"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List

from pygerber.gerberx3.tokenizer.grammar import EXPRESSIONS, GRAMMAR
from pygerber.gerberx3.tokenizer.tokens.token import Token
from pygerber.sequence_tools import flatten

if TYPE_CHECKING:
    from pyparsing import ParserElement
    from typing_extensions import Self


class Tokenizer:
    """GerberX3 format tokenizer."""

    def __init__(self) -> None:
        """GerberX3 format tokenizer."""
        logging.debug(
            "Created %s GerberX3 tokenizer.",
        )

    def tokenize(self, source: str) -> TokenStack:
        """Convert source code into token stack.

        Supports only full, valid GerberX3 files.
        """
        return self._tokenize_grammar(source, GRAMMAR, parse_all=False)

    def tokenize_expressions(self, source: str) -> TokenStack:
        """Convert source code into token stack.

        Supports arbitrary sequences of valid GerberX3 expressions.
        """
        return self._tokenize_grammar(source, EXPRESSIONS, parse_all=True)

    def _tokenize_grammar(
        self,
        source: str,
        grammar: ParserElement,
        *,
        parse_all: bool,
    ) -> TokenStack:
        tokens: list[Token] = [
            token
            for token in flatten(
                grammar.parse_string(source, parse_all=parse_all).as_list(),
            )
            if isinstance(token, Token)
        ]

        return TokenStack(tokens)


class TokenStack(List[Token]):
    """Token stack wrapper."""

    def debug_display(self) -> Self:
        """Debug display."""
        for token in self:
            logging.debug(token)

        if len(self) == 0:
            logging.debug("<Empty token stack>")

        return self

    def format_gerberx3(self) -> str:
        """Return formatted GerberX3 code."""
        return str.join("\n", (str(token) for token in self))
