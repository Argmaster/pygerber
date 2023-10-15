from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

import pytest

from pygerber.gerberx3.tokenizer.grammar import GerberGrammarBuilder

if TYPE_CHECKING:
    from pyparsing import ParserElement


class TestLoadName:
    @staticmethod
    @pytest.fixture()
    def load_name() -> ParserElement:
        return GerberGrammarBuilder()._build_load_commands()  # type: ignore[no-any-return]

    @staticmethod
    @pytest.fixture()
    def load_name_raw() -> ParserElement:
        return GerberGrammarBuilder(is_raw=True)._build_load_commands()  # type: ignore[no-any-return]

    LOAD_NAME_DATA: ClassVar[list[str]] = [
        "%LN2G09E752G0.gbl*%",
        "%LN top copper *%",
        "%LN top silk *%",
    ]
    LOAD_NAME_DATA_EXPECTED_TOKENS: ClassVar[list[str]] = [
        "[GerberCode::Token::Statement[GerberCode::Token::LoadName, GerberCode::Token::EndOfExpression]]",
        "[GerberCode::Token::Statement[GerberCode::Token::LoadName, GerberCode::Token::EndOfExpression]]",
        "[GerberCode::Token::Statement[GerberCode::Token::LoadName, GerberCode::Token::EndOfExpression]]",
    ]

    @staticmethod
    @pytest.mark.parametrize(
        ("string", "tokens"),
        zip(LOAD_NAME_DATA, LOAD_NAME_DATA_EXPECTED_TOKENS),
    )
    def test_ln(string: str, tokens: str, load_name: ParserElement) -> None:
        result = load_name.parse_string(string)
        assert str(result) == tokens

    LOAD_NAME_DATA_EXPECTED_TOKENS_RAW: ClassVar[list[str]] = [
        "['%', 'LN', '2G09E752G0.gbl', '*', '%']",
        "['%', 'LN', ' top copper ', '*', '%']",
        "['%', 'LN', ' top silk ', '*', '%']",
    ]

    @staticmethod
    @pytest.mark.parametrize(
        ("string", "tokens"),
        zip(LOAD_NAME_DATA, LOAD_NAME_DATA_EXPECTED_TOKENS_RAW),
    )
    def test_ln_raw(string: str, tokens: str, load_name_raw: ParserElement) -> None:
        result = load_name_raw.parse_string(string)
        assert str(result) == tokens


class TestLoadScaling:
    @staticmethod
    @pytest.fixture()
    def load_scale() -> ParserElement:
        return GerberGrammarBuilder()._build_load_commands()  # type: ignore[no-any-return]

    @staticmethod
    @pytest.fixture()
    def load_scale_raw() -> ParserElement:
        return GerberGrammarBuilder(is_raw=True)._build_load_commands()  # type: ignore[no-any-return]

    LOAD_SCALE_DATA: ClassVar[list[str]] = [
        "%LS0.8*%",
        "%LS1.0*%",
        "%LS1.5*%",
    ]
    LOAD_SCALE_DATA_EXPECTED_TOKENS: ClassVar[list[str]] = [
        "[GerberCode::Token::Statement[GerberCode::Token::LoadScaling, GerberCode::Token::EndOfExpression]]",
        "[GerberCode::Token::Statement[GerberCode::Token::LoadScaling, GerberCode::Token::EndOfExpression]]",
        "[GerberCode::Token::Statement[GerberCode::Token::LoadScaling, GerberCode::Token::EndOfExpression]]",
    ]

    @staticmethod
    @pytest.mark.parametrize(
        ("string", "tokens"),
        zip(LOAD_SCALE_DATA, LOAD_SCALE_DATA_EXPECTED_TOKENS),
    )
    def test_ls(string: str, tokens: str, load_scale: ParserElement) -> None:
        result = load_scale.parse_string(string)
        assert str(result) == tokens

    LOAD_SCALE_DATA_EXPECTED_TOKENS_RAW: ClassVar[list[str]] = [
        "['%', 'LS', '0.8', '*', '%']",
        "['%', 'LS', '1.0', '*', '%']",
        "['%', 'LS', '1.5', '*', '%']",
    ]

    @staticmethod
    @pytest.mark.parametrize(
        ("string", "tokens"),
        zip(LOAD_SCALE_DATA, LOAD_SCALE_DATA_EXPECTED_TOKENS_RAW),
    )
    def test_ls_raw(string: str, tokens: str, load_scale_raw: ParserElement) -> None:
        result = load_scale_raw.parse_string(string)
        assert str(result) == tokens


class TestLoadRotation:
    @staticmethod
    @pytest.fixture()
    def load_rotation() -> ParserElement:
        return GerberGrammarBuilder()._build_load_commands()  # type: ignore[no-any-return]

    @staticmethod
    @pytest.fixture()
    def load_rotation_raw() -> ParserElement:
        return GerberGrammarBuilder(is_raw=True)._build_load_commands()  # type: ignore[no-any-return]

    LOAD_ROTATION_DATA: ClassVar[list[str]] = [
        "%LR0.0*%",
        "%LR30.0*%",
        "%LR45.0*%",
    ]
    LOAD_ROTATION_DATA_EXPECTED_TOKENS: ClassVar[list[str]] = [
        "[GerberCode::Token::Statement[GerberCode::Token::LoadRotation, GerberCode::Token::EndOfExpression]]",
        "[GerberCode::Token::Statement[GerberCode::Token::LoadRotation, GerberCode::Token::EndOfExpression]]",
        "[GerberCode::Token::Statement[GerberCode::Token::LoadRotation, GerberCode::Token::EndOfExpression]]",
    ]

    @staticmethod
    @pytest.mark.parametrize(
        ("string", "tokens"),
        zip(LOAD_ROTATION_DATA, LOAD_ROTATION_DATA_EXPECTED_TOKENS),
    )
    def test_lr(string: str, tokens: str, load_rotation: ParserElement) -> None:
        result = load_rotation.parse_string(string)
        assert str(result) == tokens

    LOAD_ROTATION_DATA_EXPECTED_TOKENS_RAW: ClassVar[list[str]] = [
        "['%', 'LR', '0.0', '*', '%']",
        "['%', 'LR', '30.0', '*', '%']",
        "['%', 'LR', '45.0', '*', '%']",
    ]

    @staticmethod
    @pytest.mark.parametrize(
        ("string", "tokens"),
        zip(LOAD_ROTATION_DATA, LOAD_ROTATION_DATA_EXPECTED_TOKENS_RAW),
    )
    def test_lr_raw(string: str, tokens: str, load_rotation_raw: ParserElement) -> None:
        result = load_rotation_raw.parse_string(string)
        assert str(result) == tokens


class TestLoadMirroring:
    @staticmethod
    @pytest.fixture()
    def load_mirroring() -> ParserElement:
        return GerberGrammarBuilder()._build_load_commands()  # type: ignore[no-any-return]

    @staticmethod
    @pytest.fixture()
    def load_mirroring_raw() -> ParserElement:
        return GerberGrammarBuilder(is_raw=True)._build_load_commands()  # type: ignore[no-any-return]

    LOAD_MIRRORING_DATA: ClassVar[list[str]] = [
        "%LMN*%",
        "%LMX*%",
        "%LMXY*%",
        "%LMY*%",
    ]
    LOAD_MIRRORING_DATA_EXPECTED_TOKENS: ClassVar[list[str]] = [
        "[GerberCode::Token::Statement[GerberCode::Token::LoadMirroring, GerberCode::Token::EndOfExpression]]",
        "[GerberCode::Token::Statement[GerberCode::Token::LoadMirroring, GerberCode::Token::EndOfExpression]]",
        "[GerberCode::Token::Statement[GerberCode::Token::LoadMirroring, GerberCode::Token::EndOfExpression]]",
        "[GerberCode::Token::Statement[GerberCode::Token::LoadMirroring, GerberCode::Token::EndOfExpression]]",
    ]

    @staticmethod
    @pytest.mark.parametrize(
        ("string", "tokens"),
        zip(LOAD_MIRRORING_DATA, LOAD_MIRRORING_DATA_EXPECTED_TOKENS),
    )
    def test_lr(string: str, tokens: str, load_mirroring: ParserElement) -> None:
        result = load_mirroring.parse_string(string)
        assert str(result) == tokens

    LOAD_MIRRORING_DATA_EXPECTED_TOKENS_RAW: ClassVar[list[str]] = [
        "['%', 'LM', 'N', '*', '%']",
        "['%', 'LM', 'X', '*', '%']",
        "['%', 'LM', 'XY', '*', '%']",
        "['%', 'LM', 'Y', '*', '%']",
    ]

    @staticmethod
    @pytest.mark.parametrize(
        ("string", "tokens"),
        zip(LOAD_MIRRORING_DATA, LOAD_MIRRORING_DATA_EXPECTED_TOKENS_RAW),
    )
    def test_lr_raw(
        string: str,
        tokens: str,
        load_mirroring_raw: ParserElement,
    ) -> None:
        result = load_mirroring_raw.parse_string(string)
        assert str(result) == tokens


class TestLoadPolarity:
    @staticmethod
    @pytest.fixture()
    def load_polarity() -> ParserElement:
        return GerberGrammarBuilder()._build_load_commands()  # type: ignore[no-any-return]

    @staticmethod
    @pytest.fixture()
    def load_polarity_raw() -> ParserElement:
        return GerberGrammarBuilder(is_raw=True)._build_load_commands()  # type: ignore[no-any-return]

    LOAD_POLARITY_DATA: ClassVar[list[str]] = [
        "%LPC*%",
        "%LPD*%",
    ]
    LOAD_POLARITY_DATA_EXPECTED_TOKENS: ClassVar[list[str]] = [
        "[GerberCode::Token::Statement[GerberCode::Token::LoadPolarity, GerberCode::Token::EndOfExpression]]",
        "[GerberCode::Token::Statement[GerberCode::Token::LoadPolarity, GerberCode::Token::EndOfExpression]]",
    ]

    @staticmethod
    @pytest.mark.parametrize(
        ("string", "tokens"),
        zip(LOAD_POLARITY_DATA, LOAD_POLARITY_DATA_EXPECTED_TOKENS),
    )
    def test_lr(string: str, tokens: str, load_polarity: ParserElement) -> None:
        result = load_polarity.parse_string(string)
        assert str(result) == tokens

    LOAD_POLARITY_DATA_EXPECTED_TOKENS_RAW: ClassVar[list[str]] = [
        "['%', 'LP', 'C', '*', '%']",
        "['%', 'LP', 'D', '*', '%']",
    ]

    @staticmethod
    @pytest.mark.parametrize(
        ("string", "tokens"),
        zip(LOAD_POLARITY_DATA, LOAD_POLARITY_DATA_EXPECTED_TOKENS_RAW),
    )
    def test_lr_raw(
        string: str,
        tokens: str,
        load_polarity_raw: ParserElement,
    ) -> None:
        result = load_polarity_raw.parse_string(string)
        assert str(result) == tokens
