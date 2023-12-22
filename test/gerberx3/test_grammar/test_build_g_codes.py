from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pygerber.gerberx3.tokenizer.grammar import (
    GerberGrammarBuilder,
)

if TYPE_CHECKING:
    from pyparsing import ParserElement


@pytest.fixture()
def g_codes() -> ParserElement:
    return GerberGrammarBuilder()._build_g_codes()


@pytest.fixture()
def eoex() -> ParserElement:
    return GerberGrammarBuilder()._build_eoex()


@pytest.fixture()
def g_codes_raw() -> ParserElement:
    return GerberGrammarBuilder(
        is_raw=True,
    )._build_g_codes()


@pytest.fixture()
def eoex_raw() -> ParserElement:
    return GerberGrammarBuilder(
        is_raw=True,
    )._build_eoex()


TEST_DATA = [
    "G1",
    "G01",
    "G001",
    "G2",
    "G02",
    "G002",
    "G3",
    "G03",
    "G003",
    "G36",
    "G37",
    "G70",
    "G71",
    "G74",
    "G75",
    "G90",
    "G91",
    "G54D10",
]

TEST_DATA_EXPECTED_TOKENS = [
    "[GerberCode::Token::SetLinear]",
    "[GerberCode::Token::SetLinear]",
    "[GerberCode::Token::SetLinear]",
    "[GerberCode::Token::SetClockwiseCircular]",
    "[GerberCode::Token::SetClockwiseCircular]",
    "[GerberCode::Token::SetClockwiseCircular]",
    "[GerberCode::Token::SetCounterclockwiseCircular]",
    "[GerberCode::Token::SetCounterclockwiseCircular]",
    "[GerberCode::Token::SetCounterclockwiseCircular]",
    "[GerberCode::Token::BeginRegion]",
    "[GerberCode::Token::EndRegion]",
    "[GerberCode::Token::SetUnitInch]",
    "[GerberCode::Token::SetUnitMillimeters]",
    "[GerberCode::Token::SetMultiQuadrantMode]",
    "[GerberCode::Token::SetMultiQuadrantMode]",
    "[GerberCode::Token::SetAbsoluteNotation]",
    "[GerberCode::Token::SetIncrementalNotation]",
    "[GerberCode::Token::G54SelectAperture]",
]


@pytest.mark.parametrize(
    ("string", "tokens"),
    zip(TEST_DATA, TEST_DATA_EXPECTED_TOKENS),
)
def test_g_codes(string: str, tokens: str, g_codes: ParserElement) -> None:
    result = g_codes.parse_string(string)
    assert str(result) == tokens, str(result)


TEST_DATA_EXPECTED_TOKENS_RAW = [
    "['G1']",
    "['G01']",
    "['G001']",
    "['G2']",
    "['G02']",
    "['G002']",
    "['G3']",
    "['G03']",
    "['G003']",
    "['G36']",
    "['G37']",
    "['G70']",
    "['G71']",
    "['G74']",
    "['G75']",
    "['G90']",
    "['G91']",
    "['G54', 'D10']",
]


@pytest.mark.parametrize(
    ("string", "tokens"),
    zip(TEST_DATA, TEST_DATA_EXPECTED_TOKENS_RAW),
)
def test_g_codes_raw(string: str, tokens: str, g_codes_raw: ParserElement) -> None:
    result = g_codes_raw.parse_string(string)
    assert str(result) == tokens, str(result)


TEST_DATA_WITH_EOEX = [
    "G1*",
    "G01*",
    "G001*",
    "G2*",
    "G02*",
    "G002*",
    "G3*",
    "G03*",
    "G003*",
    "G36*",
    "G37*",
    "G70*",
    "G71*",
    "G74*",
    "G75*",
    "G90*",
    "G91*",
    "G54D10*",
]
TEST_DATA_WITH_EOEX_EXPECTED_TOKENS = [
    "[GerberCode::Token::SetLinear, GerberCode::Token::EndOfExpression]",
    "[GerberCode::Token::SetLinear, GerberCode::Token::EndOfExpression]",
    "[GerberCode::Token::SetLinear, GerberCode::Token::EndOfExpression]",
    "[GerberCode::Token::SetClockwiseCircular, GerberCode::Token::EndOfExpression]",
    "[GerberCode::Token::SetClockwiseCircular, GerberCode::Token::EndOfExpression]",
    "[GerberCode::Token::SetClockwiseCircular, GerberCode::Token::EndOfExpression]",
    "[GerberCode::Token::SetCounterclockwiseCircular, GerberCode::Token::EndOfExpression]",
    "[GerberCode::Token::SetCounterclockwiseCircular, GerberCode::Token::EndOfExpression]",
    "[GerberCode::Token::SetCounterclockwiseCircular, GerberCode::Token::EndOfExpression]",
    "[GerberCode::Token::BeginRegion, GerberCode::Token::EndOfExpression]",
    "[GerberCode::Token::EndRegion, GerberCode::Token::EndOfExpression]",
    "[GerberCode::Token::SetUnitInch, GerberCode::Token::EndOfExpression]",
    "[GerberCode::Token::SetUnitMillimeters, GerberCode::Token::EndOfExpression]",
    "[GerberCode::Token::SetMultiQuadrantMode, GerberCode::Token::EndOfExpression]",
    "[GerberCode::Token::SetMultiQuadrantMode, GerberCode::Token::EndOfExpression]",
    "[GerberCode::Token::SetAbsoluteNotation, GerberCode::Token::EndOfExpression]",
    "[GerberCode::Token::SetIncrementalNotation, GerberCode::Token::EndOfExpression]",
    "[GerberCode::Token::G54SelectAperture, GerberCode::Token::EndOfExpression]",
]


@pytest.mark.parametrize(
    ("string", "tokens"),
    zip(TEST_DATA_WITH_EOEX, TEST_DATA_WITH_EOEX_EXPECTED_TOKENS),
)
def test_g_codes_and_eoex(
    string: str,
    tokens: str,
    g_codes: ParserElement,
    eoex: ParserElement,
) -> None:
    result = (g_codes + eoex).parse_string(string)
    assert str(result) == tokens, str(result)


RAW_TEST_DATA_WITH_EOEX_EXPECTED_TOKENS = [
    "['G1', '*']",
    "['G01', '*']",
    "['G001', '*']",
    "['G2', '*']",
    "['G02', '*']",
    "['G002', '*']",
    "['G3', '*']",
    "['G03', '*']",
    "['G003', '*']",
    "['G36', '*']",
    "['G37', '*']",
    "['G70', '*']",
    "['G71', '*']",
    "['G74', '*']",
    "['G75', '*']",
    "['G90', '*']",
    "['G91', '*']",
    "['G54', 'D10', '*']",
]


@pytest.mark.parametrize(
    ("string", "tokens"),
    zip(TEST_DATA_WITH_EOEX, RAW_TEST_DATA_WITH_EOEX_EXPECTED_TOKENS),
)
def test_g_codes_and_eoex_raw(
    string: str,
    tokens: str,
    g_codes_raw: ParserElement,
    eoex_raw: ParserElement,
) -> None:
    result = (g_codes_raw + eoex_raw).parse_string(string)
    assert str(result) == tokens, str(result)
