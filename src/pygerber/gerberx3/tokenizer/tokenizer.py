"""GerberX3 format tokenizer.

Parser is based on GerberX3 format described in Ucamco's `The Gerber Layer Format
Specification`.

"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from pygerber.gerberx3.tokenizer.grammar import (
    GerberGrammarBuilder,
    GerberGrammarBuilderOptions,
)
from pygerber.gerberx3.tokenizer.tokens.groups.ast import AST

if TYPE_CHECKING:
    from pyparsing import ParserElement


@dataclass
class TokenizerOptions:
    """Tokenizer options."""

    grammar_options: GerberGrammarBuilderOptions = field(
        default_factory=GerberGrammarBuilderOptions,
    )


class Tokenizer:
    """GerberX3 format tokenizer."""

    def __init__(self, options: Optional[TokenizerOptions] = None) -> None:
        """GerberX3 format tokenizer."""
        logging.debug("Created %s GerberX3 tokenizer.")
        self.options = TokenizerOptions() if options is None else options
        self.grammar = GerberGrammarBuilder(
            options=self.options.grammar_options,
        ).build()

    def tokenize(self, source: str) -> AST:
        """Convert source code into token stack.

        Supports only full, valid GerberX3 files.
        """
        return self._tokenize_grammar(
            source,
            self.grammar.strict_grammar,
            parse_all=False,
        )

    def tokenize_expressions(self, source: str) -> AST:
        """Convert source code into token stack.

        Supports arbitrary sequences of valid GerberX3 expressions.
        """
        return self._tokenize_grammar(
            source,
            self.grammar.expression_grammar,
            parse_all=True,
        )

    def tokenize_resilient(self, source: str) -> AST:
        """Convert source code into token stack.

        Supports arbitrary sequences of valid GerberX3 expressions.
        """
        return self._tokenize_grammar(
            source,
            self.grammar.resilient_grammar,
            parse_all=True,
        )

    def _tokenize_grammar(
        self,
        source: str,
        grammar: ParserElement,
        *,
        parse_all: bool,
    ) -> AST:
        ast = grammar.parse_string(source, parse_all=parse_all)[0]
        if not isinstance(ast, AST):
            raise TypeError(ast)
        return ast
