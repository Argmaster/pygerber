from __future__ import annotations

from typing import Generator

import pytest

from pygerber.gerberx3.parser2.command_buffer2 import (
    ReadonlyCommandBuffer2,
)
from pygerber.gerberx3.parser2.parser2 import (
    Parser2,
    Parser2OnErrorAction,
    Parser2Options,
)
from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer
from pygerber.gerberx3.tokenizer.tokens.groups.ast import AST


@pytest.fixture()
def parser() -> Parser2:
    return Parser2()


def to_ast(source: str) -> AST:
    """Create AST from Gerber source."""
    return Tokenizer().tokenize_expressions(source)


def test_parser_parse(parser: Parser2) -> None:
    """Test the parse method of the Parser2 class."""
    ast = to_ast(
        """

        """,
    )
    command_buffer: ReadonlyCommandBuffer2 = parser.parse(ast)
    assert isinstance(command_buffer, ReadonlyCommandBuffer2)


def test_parser_parse_iter(parser: Parser2) -> None:
    """Test the parse_iter method of the Parser2 class."""
    ast = to_ast(
        """
        %TF.FilePolarity,Positive*%
        %FSLAX46Y46*%
        %MOMM*%
        %LPD*%
        %TA.AperFunction,EtchedComponent*%
        %ADD10C,0.508000*%
        D10*
        %TO.C,3.3V/VCC-PE:2.8V1*%
        X151892000Y-58801000D02*
        X151892000Y-57658000D01*
        """,
    )
    token_generator = parser.parse_iter(ast)
    assert isinstance(token_generator, Generator)


def test_parser_get_hooks(parser: Parser2) -> None:
    """Test the get_hooks method of the Parser2 class."""
    hooks = parser.get_hooks()
    assert hooks is not None


def test_parser_options() -> None:
    """Test the Parser2Options class."""
    options = Parser2Options(
        initial_context=None,
        context_options=None,
        on_update_drawing_state_error=Parser2OnErrorAction.Raise,
    )
    assert options.initial_context is None
    assert options.context_options is None
    assert options.on_update_drawing_state_error == Parser2OnErrorAction.Raise
