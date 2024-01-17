from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pygerber.gerberx3.tokenizer.grammar import GerberGrammarBuilder

if TYPE_CHECKING:
    from pyparsing import ParserElement


"""
    ███    ███  █████   ██████ ██████   ██████     ███████ ██   ██ ██████  ██████
    ████  ████ ██   ██ ██      ██   ██ ██    ██    ██       ██ ██  ██   ██ ██   ██
    ██ ████ ██ ███████ ██      ██████  ██    ██    █████     ███   ██████  ██████
    ██  ██  ██ ██   ██ ██      ██   ██ ██    ██    ██       ██ ██  ██      ██   ██
    ██      ██ ██   ██  ██████ ██   ██  ██████     ███████ ██   ██ ██      ██   ██
"""


@pytest.fixture()
def macro_expr() -> ParserElement:
    return GerberGrammarBuilder()._build_macro_expr()


@pytest.fixture()
def macro_expr_raw() -> ParserElement:
    return GerberGrammarBuilder(is_raw=True)._build_macro_expr()


TEST_DATA_MACRO_EXPR = [
    "4",
    "0.0119",
    "-0.04349",
    "1+2",
    "0.2x0.01x1",
    "0.2+0.01x1",
    "0.2x0.01+1",
    "0.2+0.01+1",
    "0.2+0.01+1+4.0",
    "0.2+0.01x1+4.0",
    "-0.2+0.01+1",
    "(0.2+-0.01)x1+4.0",
    "(0.2+-0.01)x1+-$1",
]

TEST_DATA_MACRO_EXPR_EXPECTED_TOKENS_RAW = [
    "['4']",
    "['0.0119']",
    "['-', '0.04349']",
    "['1', '+', '2']",
    "['0.2', 'x', ['0.01', 'x', '1']]",
    "['0.2', '+', ['0.01', 'x', '1']]",
    "[['0.2', 'x', '0.01'], '+', '1']",
    "['0.2', '+', ['0.01', '+', '1']]",
    "['0.2', '+', ['0.01', '+', ['1', '+', '4.0']]]",
    "['0.2', '+', [['0.01', 'x', '1'], '+', '4.0']]",
    "[['-', '0.2'], '+', ['0.01', '+', '1']]",
    "[[['0.2', '+', ['-', '0.01']], 'x', '1'], '+', '4.0']",
    "[[['0.2', '+', ['-', '0.01']], 'x', '1'], '+', ['-', '$1']]",
]


@pytest.mark.parametrize(
    ("string", "tokens"),
    zip(TEST_DATA_MACRO_EXPR, TEST_DATA_MACRO_EXPR_EXPECTED_TOKENS_RAW),
)
def test_macro_expr_raw(
    string: str,
    tokens: str,
    macro_expr_raw: ParserElement,
) -> None:
    result = macro_expr_raw.parse_string(string, parse_all=True)
    assert str(result) == tokens


TEST_DATA_MACRO_EXPR_EXPECTED_TOKENS = [
    "[GerberCode::Token::NumericConstant::[4]]",
    "[GerberCode::Token::NumericConstant::[0.0119]]",
    "[GerberCode::Token::NegationOperator::[GerberCode::Token::NumericConstant::[0.04349]]]",
    "[GerberCode::Token::AdditionOperator::[GerberCode::Token::NumericConstant::[1], GerberCode::Token::NumericConstant::[2]]]",
    "[GerberCode::Token::MultiplicationOperator::[GerberCode::Token::NumericConstant::[0.2], GerberCode::Token::MultiplicationOperator::[GerberCode::Token::NumericConstant::[0.01], GerberCode::Token::NumericConstant::[1]]]]",
    "[GerberCode::Token::AdditionOperator::[GerberCode::Token::NumericConstant::[0.2], GerberCode::Token::MultiplicationOperator::[GerberCode::Token::NumericConstant::[0.01], GerberCode::Token::NumericConstant::[1]]]]",
    "[GerberCode::Token::AdditionOperator::[GerberCode::Token::MultiplicationOperator::[GerberCode::Token::NumericConstant::[0.2], GerberCode::Token::NumericConstant::[0.01]], GerberCode::Token::NumericConstant::[1]]]",
    "[GerberCode::Token::AdditionOperator::[GerberCode::Token::NumericConstant::[0.2], GerberCode::Token::AdditionOperator::[GerberCode::Token::NumericConstant::[0.01], GerberCode::Token::NumericConstant::[1]]]]",
    "[GerberCode::Token::AdditionOperator::[GerberCode::Token::NumericConstant::[0.2], GerberCode::Token::AdditionOperator::[GerberCode::Token::NumericConstant::[0.01], GerberCode::Token::AdditionOperator::[GerberCode::Token::NumericConstant::[1], GerberCode::Token::NumericConstant::[4.0]]]]]",
    "[GerberCode::Token::AdditionOperator::[GerberCode::Token::NumericConstant::[0.2], GerberCode::Token::AdditionOperator::[GerberCode::Token::MultiplicationOperator::[GerberCode::Token::NumericConstant::[0.01], GerberCode::Token::NumericConstant::[1]], GerberCode::Token::NumericConstant::[4.0]]]]",
    "[GerberCode::Token::AdditionOperator::[GerberCode::Token::NegationOperator::[GerberCode::Token::NumericConstant::[0.2]], GerberCode::Token::AdditionOperator::[GerberCode::Token::NumericConstant::[0.01], GerberCode::Token::NumericConstant::[1]]]]",
    "[GerberCode::Token::AdditionOperator::[GerberCode::Token::MultiplicationOperator::[GerberCode::Token::AdditionOperator::[GerberCode::Token::NumericConstant::[0.2], GerberCode::Token::NegationOperator::[GerberCode::Token::NumericConstant::[0.01]]], GerberCode::Token::NumericConstant::[1]], GerberCode::Token::NumericConstant::[4.0]]]",
    "[GerberCode::Token::AdditionOperator::[GerberCode::Token::MultiplicationOperator::[GerberCode::Token::AdditionOperator::[GerberCode::Token::NumericConstant::[0.2], GerberCode::Token::NegationOperator::[GerberCode::Token::NumericConstant::[0.01]]], GerberCode::Token::NumericConstant::[1]], GerberCode::Token::NegationOperator::[GerberCode::Token::MacroVariableName]]]",
]


@pytest.mark.parametrize(
    ("string", "tokens"),
    zip(TEST_DATA_MACRO_EXPR, TEST_DATA_MACRO_EXPR_EXPECTED_TOKENS),
)
def test_macro_expr(
    string: str,
    tokens: str,
    macro_expr: ParserElement,
) -> None:
    result = macro_expr.parse_string(string, parse_all=True)
    assert str(result) == tokens


"""
    ███    ███  █████   ██████ ██████   ██████     ██████  ██████  ██ ███    ███ ██ ████████ ██ ██    ██ ███████
    ████  ████ ██   ██ ██      ██   ██ ██    ██    ██   ██ ██   ██ ██ ████  ████ ██    ██    ██ ██    ██ ██
    ██ ████ ██ ███████ ██      ██████  ██    ██    ██████  ██████  ██ ██ ████ ██ ██    ██    ██ ██    ██ █████
    ██  ██  ██ ██   ██ ██      ██   ██ ██    ██    ██      ██   ██ ██ ██  ██  ██ ██    ██    ██  ██  ██  ██
    ██      ██ ██   ██  ██████ ██   ██  ██████     ██      ██   ██ ██ ██      ██ ██    ██    ██   ████   ███████
"""


@pytest.fixture()
def macro_primitive() -> ParserElement:
    return GerberGrammarBuilder()._build_macro_primitive()


@pytest.fixture()
def macro_primitive_raw() -> ParserElement:
    return GerberGrammarBuilder(is_raw=True)._build_macro_primitive()


TEST_DATA_MACRO_PRIMITIVE = [
    """4,1,3,0.04349,0.0120,-0.04349,0.0119,-0.04349,-0.0120,0.04349,-0.0119,0*""",
    """1,0,$4,$2,$3*""",
]

TEST_DATA_MACRO_PRIMITIVE_EXPECTED_TOKENS_RAW = [
    "['4', '1', '3', '0.04349', '0.0120', '-', '0.04349', '0.0119', '-', '0.04349', '-', '0.0120', '0.04349', '-', '0.0119', '0', '*']",
    "['1', '0', '$4', '$2', '$3', '*']",
]


@pytest.mark.parametrize(
    ("string", "tokens"),
    zip(TEST_DATA_MACRO_PRIMITIVE, TEST_DATA_MACRO_PRIMITIVE_EXPECTED_TOKENS_RAW),
)
def test_macro_primitive(
    string: str,
    tokens: str,
    macro_primitive_raw: ParserElement,
) -> None:
    result = macro_primitive_raw.parse_string(string)
    assert str(result) == tokens


"""
    ███    ███  █████   ██████ ██████   ██████     ██    ██  █████  ██████     ██████  ███████ ███████
    ████  ████ ██   ██ ██      ██   ██ ██    ██    ██    ██ ██   ██ ██   ██    ██   ██ ██      ██
    ██ ████ ██ ███████ ██      ██████  ██    ██    ██    ██ ███████ ██████     ██   ██ █████   █████
    ██  ██  ██ ██   ██ ██      ██   ██ ██    ██     ██  ██  ██   ██ ██   ██    ██   ██ ██      ██
    ██      ██ ██   ██  ██████ ██   ██  ██████       ████   ██   ██ ██   ██    ██████  ███████ ██
"""


@pytest.fixture()
def macro_variable_declaration() -> ParserElement:
    return GerberGrammarBuilder()._build_macro_variable_definition()


@pytest.fixture()
def macro_variable_declaration_raw() -> ParserElement:
    return GerberGrammarBuilder(is_raw=True)._build_macro_variable_definition()


TEST_DATA_MACRO_VARIABLE_DECLARATION = [
    "$4=$1x0.75*",
]

TEST_DATA_MACRO_VARIABLE_DECLARATION_EXPECTED_TOKENS_RAW = [
    "['$4', '=', '$1', 'x', '0.75', '*']",
]


@pytest.mark.parametrize(
    ("string", "tokens"),
    zip(
        TEST_DATA_MACRO_VARIABLE_DECLARATION,
        TEST_DATA_MACRO_VARIABLE_DECLARATION_EXPECTED_TOKENS_RAW,
    ),
)
def test_macro_variable_declaration_raw(
    string: str,
    tokens: str,
    macro_variable_declaration_raw: ParserElement,
) -> None:
    result = macro_variable_declaration_raw.parse_string(string)
    assert str(result) == tokens


TEST_DATA_MACRO_VARIABLE_DECLARATION_EXPECTED_TOKENS = [
    "[GerberCode::Token::MacroVariableAssignment::[GerberCode::Token::MacroVariableName = GerberCode::Token::MultiplicationOperator::[GerberCode::Token::MacroVariableName, GerberCode::Token::NumericConstant::[0.75]]]]",
]


@pytest.mark.parametrize(
    ("string", "tokens"),
    zip(
        TEST_DATA_MACRO_VARIABLE_DECLARATION,
        TEST_DATA_MACRO_VARIABLE_DECLARATION_EXPECTED_TOKENS,
    ),
)
def test_macro_variable_declaration(
    string: str,
    tokens: str,
    macro_variable_declaration: ParserElement,
) -> None:
    result = macro_variable_declaration.parse_string(string)
    assert str(result) == tokens


"""
    ███████ ██    ██ ██      ██         ███    ███  █████   ██████ ██████   ██████
    ██      ██    ██ ██      ██         ████  ████ ██   ██ ██      ██   ██ ██    ██
    █████   ██    ██ ██      ██         ██ ████ ██ ███████ ██      ██████  ██    ██
    ██      ██    ██ ██      ██         ██  ██  ██ ██   ██ ██      ██   ██ ██    ██
    ██       ██████  ███████ ███████    ██      ██ ██   ██  ██████ ██   ██  ██████
"""


@pytest.fixture()
def macro_tokens() -> ParserElement:
    return GerberGrammarBuilder()._build_macro_tokens()


@pytest.fixture()
def macro_tokens_raw() -> ParserElement:
    return GerberGrammarBuilder(is_raw=True)._build_macro_tokens()


TEST_DATA = [
    """%AMREC1090*
4,1,3,
0.04349,0.0120,
-0.04349,0.0119,
-0.04349,-0.0120,
0.04349,-0.0119,
0*%
""",
    """%AMDonut*
1,1,$1,$2,$3*
$4=$1x0.75*
1,0,$4,$2,$3*%
""",
]

TEST_DATA_EXPECTED_TOKENS_RAW = [
    "['%', 'AM', 'REC1090', '*', '4', '1', '3', '0.04349', '0.0120', '-', '0.04349', '0.0119', '-', '0.04349', '-', '0.0120', '0.04349', '-', '0.0119', '0', '*', '%']",
    "['%', 'AM', 'Donut', '*', '1', '1', '$1', '$2', '$3', '*', '$4', '=', '$1', 'x', '0.75', '*', '1', '0', '$4', '$2', '$3', '*', '%']",
]


@pytest.mark.parametrize(
    ("string", "tokens"),
    zip(TEST_DATA, TEST_DATA_EXPECTED_TOKENS_RAW),
)
def test_am_raw(string: str, tokens: str, macro_tokens_raw: ParserElement) -> None:
    result = macro_tokens_raw.parse_string(string)
    assert str(result) == tokens
