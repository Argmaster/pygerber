from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pygerber.gerberx3.tokenizer.grammar import GerberGrammarBuilder

if TYPE_CHECKING:
    from pyparsing import ParserElement


@pytest.fixture()
def define_aperture() -> ParserElement:
    return GerberGrammarBuilder()._build_define_aperture()  # type: ignore[no-any-return]


@pytest.fixture()
def define_aperture_raw() -> ParserElement:
    return GerberGrammarBuilder(is_raw=True)._build_define_aperture()  # type: ignore[no-any-return]


TEST_DATA = [
    "%ADD19CROSS,2.0*%",
    "%ADD72COMP142*%",
    "%ADD68O,1.500000X3.900000*%",
    "%ADD66O,3.801600X1.601600*%",
    "%ADD56R,1.016000X1.016000*%",
    "%ADD50C,0.005000*%",
    "%ADD35DONUTCAL,0.020X0X0X0.06*%",
    "%ADD21RoundRect,0.250000X-0.262500X-0.450000X0.262500X-0.450000X0.262500X0.450000X-0.262500X0.450000X0*%",
]

TEST_DATA_EXPECTED_TOKENS_RAW = [
    "['%', 'AD', 'D19', 'CROSS', ',', '2.0', '*', '%']",
    "['%', 'AD', 'D72', 'COMP142', '*', '%']",
    "['%', 'AD', 'D68', 'O', ',', '1.500000', 'X', '3.900000', '*', '%']",
    "['%', 'AD', 'D66', 'O', ',', '3.801600', 'X', '1.601600', '*', '%']",
    "['%', 'AD', 'D56', 'R', ',', '1.016000', 'X', '1.016000', '*', '%']",
    "['%', 'AD', 'D50', 'C', ',', '0.005000', '*', '%']",
    "['%', 'AD', 'D35', 'DONUTCAL', ',', '0.020', 'X', '0', 'X', '0', 'X', '0.06', '*', '%']",
    "['%', 'AD', 'D21', 'RoundRect', ',', '0.250000', 'X', '-0.262500', 'X', '-0.450000', 'X', '0.262500', 'X', '-0.450000', 'X', '0.262500', 'X', '0.450000', 'X', '-0.262500', 'X', '0.450000', 'X', '0', '*', '%']",
]


@pytest.mark.parametrize(
    ("string", "tokens"),
    zip(TEST_DATA, TEST_DATA_EXPECTED_TOKENS_RAW),
)
def test_define_aperture_raw(
    string: str,
    tokens: str,
    define_aperture_raw: ParserElement,
) -> None:
    result = define_aperture_raw.parse_string(string, parse_all=True)
    assert str(result) == tokens


TEST_DATA_EXPECTED_TOKENS = [
    "[GerberCode::Token::Statement[GerberCode::Token::DefineMacro, GerberCode::Token::EndOfExpression]]",
    "[GerberCode::Token::Statement[GerberCode::Token::DefineMacro, GerberCode::Token::EndOfExpression]]",
    "[GerberCode::Token::Statement[GerberCode::Token::DefineObround, GerberCode::Token::EndOfExpression]]",
    "[GerberCode::Token::Statement[GerberCode::Token::DefineObround, GerberCode::Token::EndOfExpression]]",
    "[GerberCode::Token::Statement[GerberCode::Token::DefineRectangle, GerberCode::Token::EndOfExpression]]",
    "[GerberCode::Token::Statement[GerberCode::Token::DefineCircle, GerberCode::Token::EndOfExpression]]",
    "[GerberCode::Token::Statement[GerberCode::Token::DefineMacro, GerberCode::Token::EndOfExpression]]",
    "[GerberCode::Token::Statement[GerberCode::Token::DefineMacro, GerberCode::Token::EndOfExpression]]",
]


@pytest.mark.parametrize(
    ("string", "tokens"),
    zip(TEST_DATA, TEST_DATA_EXPECTED_TOKENS),
)
def test_define_aperture(
    string: str,
    tokens: str,
    define_aperture: ParserElement,
) -> None:
    result = define_aperture.parse_string(string, parse_all=True)
    assert str(result) == tokens
