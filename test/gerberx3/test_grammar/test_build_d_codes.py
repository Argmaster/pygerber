from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pygerber.gerberx3.tokenizer.grammar import (
    GerberGrammarBuilder,
)

if TYPE_CHECKING:
    from pyparsing import ParserElement


@pytest.fixture()
def d_codes() -> ParserElement:
    return GerberGrammarBuilder()._build_d_codes()


@pytest.fixture()
def d_codes_raw() -> ParserElement:
    return GerberGrammarBuilder(
        is_raw=True,
    )._build_d_codes()


TEST_DATA_COORDINATES = [
    # XY
    "X1000Y2000",
    "X1000",
    "Y1000",
]

TEST_DATA_COORDINATES_IJ = [
    *TEST_DATA_COORDINATES,
    # IJ
    "X001000Y2000I3000J4000",
    "X1000I003000J4000",
    "Y1000I3000J004000",
    # Signed
    "X-1000Y2000I+3000J-4000",
    "X1000I-3000J4000",
    "Y+1000I3000J+4000",
    # I
    "X1000Y2000I3000",
    "X1000I3000",
    "Y1000I3000",
    # J
    "X1000Y2000J4000",
    "X1000J4000",
    "Y1000J4000",
]

TEST_DATA_D01_CODES = [
    "D1",
    "D01",
    "D001",
]

TEST_DATA_CODES = [
    *TEST_DATA_D01_CODES,
    "D2",
    "D02",
    "D002",
    "D3",
    "D03",
    "D003",
]

TEST_DATA_D01_CODES_EXPECTED_TOKENS = [
    "[GerberCode::Token::D01Draw]",
    "[GerberCode::Token::D01Draw]",
    "[GerberCode::Token::D01Draw]",
]

TEST_DATA_CODES_EXPECTED_TOKENS = [
    *TEST_DATA_D01_CODES_EXPECTED_TOKENS,
    "[GerberCode::Token::D02Move]",
    "[GerberCode::Token::D02Move]",
    "[GerberCode::Token::D02Move]",
    "[GerberCode::Token::D03Flash]",
    "[GerberCode::Token::D03Flash]",
    "[GerberCode::Token::D03Flash]",
]

TEST_DATA = [co + d_code for co in TEST_DATA_COORDINATES for d_code in TEST_DATA_CODES]
TEST_DATA_EXPECTED_TOKENS = [
    token for _ in TEST_DATA_COORDINATES for token in TEST_DATA_CODES_EXPECTED_TOKENS
]


@pytest.mark.parametrize(
    ("string", "tokens"),
    zip(TEST_DATA, TEST_DATA_EXPECTED_TOKENS),
)
def test_g_codes(string: str, tokens: str, d_codes: ParserElement) -> None:
    result = d_codes.parse_string(string)
    assert str(result) == tokens, str(result)


TEST_DATA_IJ = [
    co + d_code for co in TEST_DATA_COORDINATES_IJ for d_code in TEST_DATA_D01_CODES
]
TEST_DATA_IJ_EXPECTED_TOKENS = [
    token
    for _ in TEST_DATA_COORDINATES_IJ
    for token in TEST_DATA_D01_CODES_EXPECTED_TOKENS
]


@pytest.mark.parametrize(
    ("string", "tokens"),
    zip(TEST_DATA_IJ, TEST_DATA_IJ_EXPECTED_TOKENS),
)
def test_g_codes_ij(string: str, tokens: str, d_codes: ParserElement) -> None:
    result = d_codes.parse_string(string)
    assert str(result) == tokens, str(result)


TEST_DATA_RAW = [
    "X50000Y100I3230J0032D01",
    "X+50000Y-100D01",
    "X+0490D02",
    "Y+1000D02",
    "X+0490Y-230000D03",
    "Y+1000D03",
]
TEST_DATA_RAW_TOKENS = [
    "['X', '50000', 'Y', '100', 'I', '3230', 'J', '0032', 'D01']",
    "['X', '+50000', 'Y', '-100', 'D01']",
    "['X', '+0490', 'D02']",
    "['Y', '+1000', 'D02']",
    "['X', '+0490', 'Y', '-230000', 'D03']",
    "['Y', '+1000', 'D03']",
]


@pytest.mark.parametrize(
    ("string", "tokens"),
    zip(TEST_DATA_RAW, TEST_DATA_RAW_TOKENS),
)
def test_g_codes_raw(string: str, tokens: str, d_codes_raw: ParserElement) -> None:
    result = d_codes_raw.parse_string(string)
    assert str(result) == tokens, str(result)
