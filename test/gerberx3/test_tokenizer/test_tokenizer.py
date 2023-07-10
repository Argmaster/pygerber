"""Test tokenizer class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer

if TYPE_CHECKING:
    from test.conftest import AssetLoader


class TestTokenizerBasic:
    """Tokenizer tests based on basic examples."""

    def test_tokenizer_sample_0(self, asset_loader: AssetLoader) -> None:
        """Test tokenizer on sample 0."""
        Tokenizer().tokenize(
            asset_loader.load_asset("gerberx3/basic/sample-0/source.grb").decode(
                "utf-8",
            ),
        )

    def test_tokenizer_sample_1(self, asset_loader: AssetLoader) -> None:
        """Test tokenizer on sample 1."""
        Tokenizer().tokenize(
            asset_loader.load_asset("gerberx3/basic/sample-1/source.grb").decode(
                "utf-8",
            ),
        )

    def test_tokenizer_sample_2(self, asset_loader: AssetLoader) -> None:
        """Test tokenizer on sample 2."""
        Tokenizer().tokenize(
            asset_loader.load_asset("gerberx3/basic/sample-2/source.grb").decode(
                "utf-8",
            ),
        )

    def test_tokenizer_sample_3(self, asset_loader: AssetLoader) -> None:
        """Test tokenizer on sample 3."""
        Tokenizer().tokenize(
            asset_loader.load_asset("gerberx3/basic/sample-3/source.grb").decode(
                "utf-8",
            ),
        )

    def test_tokenizer_sample_4(self, asset_loader: AssetLoader) -> None:
        """Test tokenizer on sample 4."""
        Tokenizer().tokenize(
            asset_loader.load_asset("gerberx3/basic/sample-4/source.grb").decode(
                "utf-8",
            ),
        )

    def test_tokenizer_sample_5(self, asset_loader: AssetLoader) -> None:
        """Test tokenizer on sample 5."""
        Tokenizer().tokenize(
            asset_loader.load_asset("gerberx3/basic/sample-5/source.grb").decode(
                "utf-8",
            ),
        )


class TestTokenizerKicadArduino:
    """Tokenizer tests based on Kicad arduino template."""

    def test_tokenizer_sample_b_cu(self, asset_loader: AssetLoader) -> None:
        """Test tokenizer on sample B_Cu.gbr."""
        Tokenizer().tokenize(
            asset_loader.load_asset("gerberx3/kicad/arduino/B_Cu.gbr").decode("utf-8"),
        )

    def test_tokenizer_sample_f_cu(self, asset_loader: AssetLoader) -> None:
        """Test tokenizer on sample F_Cu.gbr."""
        Tokenizer().tokenize(
            asset_loader.load_asset("gerberx3/kicad/arduino/F_Cu.gbr").decode("utf-8"),
        )

    def test_tokenizer_sample_f_mask(self, asset_loader: AssetLoader) -> None:
        """Test tokenizer on sample F_Mask.gbr."""
        Tokenizer().tokenize(
            asset_loader.load_asset("gerberx3/kicad/arduino/F_Mask.gbr").decode(
                "utf-8",
            ),
        )

    def test_tokenizer_sample_f_silkscreen(self, asset_loader: AssetLoader) -> None:
        """Test tokenizer on sample F_Silkscreen.gbr."""
        Tokenizer().tokenize(
            asset_loader.load_asset("gerberx3/kicad/arduino/F_Silkscreen.gbr").decode(
                "utf-8",
            ),
        )

    def test_tokenizer_sample_user_drawings(self, asset_loader: AssetLoader) -> None:
        """Test tokenizer on sample User_Drawings.gbr."""
        Tokenizer().tokenize(
            asset_loader.load_asset("gerberx3/kicad/arduino/User_Drawings.gbr").decode(
                "utf-8",
            ),
        )


class TestTokenizerKicadHello:
    """Tokenizer tests based on Kicad hello."""

    def test_tokenizer_sample_b_cu(self, asset_loader: AssetLoader) -> None:
        """Test tokenizer on sample B_Cu.gbr."""
        Tokenizer().tokenize(
            asset_loader.load_asset("gerberx3/kicad/hello/B_Cu/B_Cu.gbr").decode(
                "utf-8",
            ),
        )

    def test_tokenizer_sample_edge_cuts(self, asset_loader: AssetLoader) -> None:
        """Test tokenizer on sample Edge_Cuts.gbr."""
        Tokenizer().tokenize(
            asset_loader.load_asset(
                "gerberx3/kicad/hello/Edge_Cuts/Edge_Cuts.gbr",
            ).decode("utf-8"),
        )

    def test_tokenizer_sample_f_cu(self, asset_loader: AssetLoader) -> None:
        """Test tokenizer on sample F_Cu.gbr."""
        Tokenizer().tokenize(
            asset_loader.load_asset(
                "gerberx3/kicad/hello/F_Cu/F_Cu.gbr",
            ).decode("utf-8"),
        )

    def test_tokenizer_sample_f_mask(self, asset_loader: AssetLoader) -> None:
        """Test tokenizer on sample F_Mask.gbr."""
        Tokenizer().tokenize(
            asset_loader.load_asset(
                "gerberx3/kicad/hello/F_Mask/F_Mask.gbr",
            ).decode("utf-8"),
        )

    def test_tokenizer_sample_f_paste(self, asset_loader: AssetLoader) -> None:
        """Test tokenizer on sample F_Paste.gbr."""
        Tokenizer().tokenize(
            asset_loader.load_asset(
                "gerberx3/kicad/hello/F_Paste/F_Paste.gbr",
            ).decode("utf-8"),
        )

    def test_tokenizer_sample_f_silkscreen(self, asset_loader: AssetLoader) -> None:
        """Test tokenizer on sample F_Silkscreen.gbr."""
        Tokenizer().tokenize(
            asset_loader.load_asset(
                "gerberx3/kicad/hello/F_Silkscreen/F_Silkscreen.gbr",
            ).decode("utf-8"),
        ).debug_display()


class TestTokenizerExpressions:
    """Test tokenizer on expression samples."""

    class TestAM:
        """Test AM (Aperture Macro) definition tokenization."""

        def test_tokenizer_sample_am_sample_0(self, asset_loader: AssetLoader) -> None:
            """Test tokenizer on sample 0."""
            Tokenizer().tokenize_expressions(
                asset_loader.load_asset(
                    "gerberx3/expressions/AM/sample-0.gbr",
                ).decode("utf-8"),
            ).debug_display()

        def test_tokenizer_sample_am_sample_1(self, asset_loader: AssetLoader) -> None:
            """Test tokenizer on sample 1."""
            Tokenizer().tokenize_expressions(
                asset_loader.load_asset(
                    "gerberx3/expressions/AM/sample-1.gbr",
                ).decode("utf-8"),
            ).debug_display()

        def test_tokenizer_sample_am_sample_2(self, asset_loader: AssetLoader) -> None:
            """Test tokenizer on sample 2."""
            Tokenizer().tokenize_expressions(
                asset_loader.load_asset(
                    "gerberx3/expressions/AM/sample-2.gbr",
                ).decode("utf-8"),
            ).debug_display()
