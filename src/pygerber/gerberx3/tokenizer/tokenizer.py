"""GerberX3 format tokenizer.

Parser is based on GerberX3 format described in Ucamco's `The Gerber Layer Format
Specification`.

"""
from __future__ import annotations

from pygerber.gerberx3.tokenizer._grammar import GRAMMAR


class Tokenizer:
    """GerberX3 format tokenizer."""

    def __init__(self, *, strict: bool = False) -> None:
        """GerberX3 format tokenizer."""
        self.grammar = GRAMMAR
        self.strict = strict

    def tokenize(self, source: str):
        for token in self.grammar.parse_string(source, parse_all=self.strict):
            print(token, type(token))
