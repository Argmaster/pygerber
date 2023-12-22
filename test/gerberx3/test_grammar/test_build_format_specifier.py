from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pygerber.gerberx3.tokenizer.grammar import GerberGrammarBuilder
from pygerber.gerberx3.tokenizer.tokens.bases.gerber_code import get_gerber_code

if TYPE_CHECKING:
    from pyparsing import ParserElement


@pytest.fixture()
def format_specifier() -> ParserElement:
    return GerberGrammarBuilder()._build_format_specifier()


@pytest.fixture()
def format_specifier_raw() -> ParserElement:
    return GerberGrammarBuilder(is_raw=True)._build_format_specifier()


FORMAT_SPECIFIER_DATA = [
    "%FSLAX23Y23*%",
    "%FSLAX24Y24*%",
    "%FSLAX25Y25*%",
    "%FSLAX26Y26*%",
    "%FSLAX34Y34*%",
    "%FSLAX36Y36*%",
    "%FSLAX45Y45*%",
    "%FSLAX46Y46*%",
]
FORMAT_SPECIFIER_DATA_EXPECTED_TOKENS = [
    "[GerberCode::Token::Statement[GerberCode::Token::CoordinateFormat, GerberCode::Token::EndOfExpression]]",
    "[GerberCode::Token::Statement[GerberCode::Token::CoordinateFormat, GerberCode::Token::EndOfExpression]]",
    "[GerberCode::Token::Statement[GerberCode::Token::CoordinateFormat, GerberCode::Token::EndOfExpression]]",
    "[GerberCode::Token::Statement[GerberCode::Token::CoordinateFormat, GerberCode::Token::EndOfExpression]]",
    "[GerberCode::Token::Statement[GerberCode::Token::CoordinateFormat, GerberCode::Token::EndOfExpression]]",
    "[GerberCode::Token::Statement[GerberCode::Token::CoordinateFormat, GerberCode::Token::EndOfExpression]]",
    "[GerberCode::Token::Statement[GerberCode::Token::CoordinateFormat, GerberCode::Token::EndOfExpression]]",
    "[GerberCode::Token::Statement[GerberCode::Token::CoordinateFormat, GerberCode::Token::EndOfExpression]]",
]


@pytest.mark.parametrize(
    ("string", "tokens"),
    zip(FORMAT_SPECIFIER_DATA, FORMAT_SPECIFIER_DATA_EXPECTED_TOKENS),
)
def test_fs(string: str, tokens: str, format_specifier: ParserElement) -> None:
    result = format_specifier.parse_string(string)
    assert str(result) == tokens


FORMAT_SPECIFIER_DATA_EXPECTED_TOKENS_RAW = [
    "['%', 'FS', 'L', 'A', 'X', '23', 'Y', '23', '*', '%']",
    "['%', 'FS', 'L', 'A', 'X', '24', 'Y', '24', '*', '%']",
    "['%', 'FS', 'L', 'A', 'X', '25', 'Y', '25', '*', '%']",
    "['%', 'FS', 'L', 'A', 'X', '26', 'Y', '26', '*', '%']",
    "['%', 'FS', 'L', 'A', 'X', '34', 'Y', '34', '*', '%']",
    "['%', 'FS', 'L', 'A', 'X', '36', 'Y', '36', '*', '%']",
    "['%', 'FS', 'L', 'A', 'X', '45', 'Y', '45', '*', '%']",
    "['%', 'FS', 'L', 'A', 'X', '46', 'Y', '46', '*', '%']",
]


@pytest.mark.parametrize(
    ("string", "tokens"),
    zip(FORMAT_SPECIFIER_DATA, FORMAT_SPECIFIER_DATA_EXPECTED_TOKENS_RAW),
)
def test_fs_raw(string: str, tokens: str, format_specifier_raw: ParserElement) -> None:
    result = format_specifier_raw.parse_string(string)
    assert str(result) == tokens


FORMAT_SPECIFIER_DATA_GET_GERBER_CODE = [
    "%FSLAX23Y23*%",
    "%FSLAX24Y24*%",
    "%FSLAX25Y25*%",
    "%FSLAX26Y26*%",
    "%FSLAX34Y34*%",
    "%FSLAX36Y36*%",
    "%FSLAX45Y45*%",
    "%FSLAX46Y46*%",
]


@pytest.mark.parametrize(
    ("string", "tokens"),
    zip(FORMAT_SPECIFIER_DATA, FORMAT_SPECIFIER_DATA_GET_GERBER_CODE),
)
def test_fs_get_gerber_code(
    string: str,
    tokens: str,
    format_specifier: ParserElement,
) -> None:
    result = format_specifier.parse_string(string)
    assert get_gerber_code(result) == tokens
