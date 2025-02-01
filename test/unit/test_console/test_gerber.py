from __future__ import annotations

import logging

import pytest
from click.testing import CliRunner
from PIL import Image

from pygerber.console.gerber import (
    bmp,
    format_cmd,
    jpeg,
    merge_convert_png,
    png,
    tiff,
    webp,
)
from pygerber.examples import ExamplesEnum, get_example_path
from pygerber.vm.shapely.vm import is_shapely_available
from test.assets.assetlib import ImageAnalyzer, SvgImageAsset
from test.assets.reference.pygerber.console.gerber import (
    CONVERT_BMP_REFERENCE_IMAGE,
    CONVERT_JPEG_REFERENCE_IMAGE,
    CONVERT_PNG_REFERENCE_IMAGE,
    CONVERT_SVG_REFERENCE_IMAGE,
    CONVERT_TIFF_REFERENCE_IMAGE,
    CONVERT_WEBP_LOSSLESS_REFERENCE_IMAGE,
    CONVERT_WEBP_LOSSY_REFERENCE_IMAGE,
    FORMAT_CMD_REFERENCE_CONTENT,
    MERGE_CONVERT_PNG_REFERENCE_IMAGE,
)
from test.conftest import cd_to_tempdir
from test.tags import Tag, tag

MIN_PNG_SSIM = 0.99


if is_shapely_available():
    from pygerber.console.gerber import svg


@tag(Tag.PILLOW, Tag.OPENCV, Tag.SKIMAGE)
def test_gerber_convert_png(*, is_regeneration_enabled: bool) -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            png,
            [
                get_example_path(ExamplesEnum.UCAMCO_2_11_2).as_posix(),
                "-o",
                "output.png",
                "-s",
                "DEBUG_1_ALPHA",
                "-d",
                "20",
            ],
        )
        logging.debug(result.output)
        assert result.exit_code == 0
        assert (temp_path / "output.png").exists()

        image = Image.open(temp_path / "output.png")
        if is_regeneration_enabled:
            CONVERT_PNG_REFERENCE_IMAGE.update(image)  # pragma: no cover
        else:
            ia = ImageAnalyzer(CONVERT_PNG_REFERENCE_IMAGE.load())
            assert ia.structural_similarity(image) > MIN_PNG_SSIM
            ia.assert_same_size(image)
            (
                ia.histogram_compare_color(image)
                .assert_channel_count(4)
                .assert_greater_or_equal_values(0.99)
            )


MIN_JPEG_SSIM = 0.95


@tag(Tag.PILLOW, Tag.OPENCV, Tag.SKIMAGE)
def test_gerber_convert_jpeg(*, is_regeneration_enabled: bool) -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            jpeg,
            [
                get_example_path(ExamplesEnum.UCAMCO_2_11_2).as_posix(),
                "-o",
                "output.jpg",
                "-s",
                "DEBUG_1_ALPHA",
                "-d",
                "20",
            ],
        )
        logging.debug(result.output)
        assert result.exit_code == 0
        assert (temp_path / "output.jpg").exists()

        image = Image.open(temp_path / "output.jpg")
        if is_regeneration_enabled:
            CONVERT_JPEG_REFERENCE_IMAGE.update(image)  # pragma: no cover
        else:
            ia = ImageAnalyzer(CONVERT_JPEG_REFERENCE_IMAGE.load())
            assert ia.structural_similarity(image) > MIN_JPEG_SSIM
            ia.assert_same_size(image)
            (
                ia.histogram_compare_color(image)
                .assert_channel_count(3)
                .assert_greater_or_equal_values(0.9)
            )


MIN_TIFF_SSIM = 0.99


@tag(Tag.PILLOW, Tag.OPENCV, Tag.SKIMAGE)
def test_gerber_convert_tiff(*, is_regeneration_enabled: bool) -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            tiff,
            [
                get_example_path(ExamplesEnum.UCAMCO_2_11_2).as_posix(),
                "-o",
                "output.tiff",
                "-s",
                "DEBUG_1_ALPHA",
                "-d",
                "20",
            ],
        )
        logging.debug(result.output)
        assert result.exit_code == 0
        assert (temp_path / "output.tiff").exists()

        image = Image.open(temp_path / "output.tiff")
        if is_regeneration_enabled:
            CONVERT_TIFF_REFERENCE_IMAGE.update(image)  # pragma: no cover
        else:
            ia = ImageAnalyzer(CONVERT_TIFF_REFERENCE_IMAGE.load())
            assert ia.structural_similarity(image) > MIN_TIFF_SSIM
            ia.assert_same_size(image)
            (
                ia.histogram_compare_color(image)
                .assert_channel_count(4)
                .assert_greater_or_equal_values(0.99)
            )


MIN_BMP_SSIM = 0.99


@tag(Tag.PILLOW, Tag.OPENCV, Tag.SKIMAGE)
def test_gerber_convert_bmp(*, is_regeneration_enabled: bool) -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            bmp,
            [
                get_example_path(ExamplesEnum.UCAMCO_2_11_2).as_posix(),
                "-o",
                "output.bmp",
                "-s",
                "DEBUG_1_ALPHA",
                "-d",
                "10",
            ],
        )
        logging.debug(result.output)
        assert result.exit_code == 0
        assert (temp_path / "output.bmp").exists()

        image = Image.open(temp_path / "output.bmp")
        if is_regeneration_enabled:
            CONVERT_BMP_REFERENCE_IMAGE.update(image)  # pragma: no cover
        else:
            ia = ImageAnalyzer(CONVERT_BMP_REFERENCE_IMAGE.load())
            assert ia.structural_similarity(image) > MIN_BMP_SSIM
            ia.assert_same_size(image)
            (
                ia.histogram_compare_color(image)
                .assert_channel_count(3)
                .assert_greater_or_equal_values(0.99)
            )


MIN_WEBP_LOSSY_SSIM = 0.95


@tag(Tag.PILLOW, Tag.OPENCV, Tag.SKIMAGE)
def test_gerber_convert_webp_lossy(*, is_regeneration_enabled: bool) -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            webp,
            [
                get_example_path(ExamplesEnum.UCAMCO_2_11_2).as_posix(),
                "-o",
                "output.webp",
                "-s",
                "DEBUG_1_ALPHA",
                "-d",
                "20",
            ],
        )
        logging.debug(result.output)
        assert result.exit_code == 0
        assert (temp_path / "output.webp").exists()

        image = Image.open(temp_path / "output.webp")
        if is_regeneration_enabled:
            CONVERT_WEBP_LOSSY_REFERENCE_IMAGE.update(image)  # pragma: no cover
        else:
            ia = ImageAnalyzer(CONVERT_WEBP_LOSSY_REFERENCE_IMAGE.load())
            assert ia.structural_similarity(image) > MIN_WEBP_LOSSY_SSIM
            ia.assert_same_size(image)
            (
                ia.histogram_compare_color(image)
                .assert_channel_count(3)
                .assert_greater_or_equal_values(0.99)
            )


MIN_WEBP_LOSSLESS_SSIM = 0.98


@tag(Tag.PILLOW, Tag.OPENCV, Tag.SKIMAGE)
def test_gerber_convert_webp_lossless(*, is_regeneration_enabled: bool) -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            webp,
            [
                get_example_path(ExamplesEnum.UCAMCO_2_11_2).as_posix(),
                "-o",
                "output.webp",
                "-s",
                "DEBUG_1_ALPHA",
                "-d",
                "20",
                "--lossless",
            ],
        )
        logging.debug(result.output)
        assert result.exit_code == 0
        assert (temp_path / "output.webp").exists()

        image = Image.open(temp_path / "output.webp")
        if is_regeneration_enabled:
            CONVERT_WEBP_LOSSLESS_REFERENCE_IMAGE.update(image)  # pragma: no cover
        else:
            ia = ImageAnalyzer(CONVERT_WEBP_LOSSLESS_REFERENCE_IMAGE.load())
            assert ia.structural_similarity(image) > MIN_WEBP_LOSSLESS_SSIM
            ia.assert_same_size(image)
            (
                ia.histogram_compare_color(image)
                .assert_channel_count(3)
                .assert_greater_or_equal_values(0.9)
            )


MIN_SVG_SSIM = 0.99


@tag(Tag.PILLOW, Tag.OPENCV, Tag.SKIMAGE, Tag.SVGLIB)
def test_gerber_convert_svg(*, is_regeneration_enabled: bool) -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            svg,
            [
                get_example_path(ExamplesEnum.UCAMCO_2_11_2).as_posix(),
                "-o",
                "output.svg",
                "-s",
                "DEBUG_1_ALPHA",
            ],
        )
        logging.debug(result.output)
        assert result.exit_code == 0
        assert (temp_path / "output.svg").exists()

        image = (temp_path / "output.svg").read_text()
        if is_regeneration_enabled:
            CONVERT_SVG_REFERENCE_IMAGE.update(image)  # pragma: no cover
        else:
            dpi = 72
            image_png = SvgImageAsset.svg_to_png(image, dpi=dpi)

            ia = ImageAnalyzer(CONVERT_SVG_REFERENCE_IMAGE.load_png(dpi=dpi))
            assert ia.structural_similarity(image_png) > MIN_SVG_SSIM
            ia.assert_same_size(image_png)
            (
                ia.histogram_compare_color(image_png)
                .assert_channel_count(3)
                .assert_greater_or_equal_values(0.9)
            )


@tag(Tag.FORMATTER)
def test_gerber_format_cmd(*, is_regeneration_enabled: bool) -> None:
    runner = CliRunner()
    file_name = "output.formatted.gbr"

    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            format_cmd,
            [
                get_example_path(ExamplesEnum.UCAMCO_2_11_2).as_posix(),
                "-o",
                file_name,
            ],
        )
        logging.debug(result.output)

        file_path = temp_path / file_name
        assert result.exit_code == 0
        assert (file_path).exists()

        if is_regeneration_enabled:
            FORMAT_CMD_REFERENCE_CONTENT.update(file_path.read_text())
            pytest.skip("Reference updated")
        else:
            assert FORMAT_CMD_REFERENCE_CONTENT.load() == file_path.read_text()


MIN_MERGE_PNG_SSIM = 0.99


@tag(Tag.PILLOW, Tag.OPENCV, Tag.SKIMAGE)
def test_gerber_merge_convert_png(*, is_regeneration_enabled: bool) -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            merge_convert_png,
            [
                get_example_path(ExamplesEnum.carte_test_B_Cu).as_posix(),
                get_example_path(ExamplesEnum.carte_test_B_Mask).as_posix(),
                get_example_path(ExamplesEnum.carte_test_B_Silkscreen).as_posix(),
                "-o",
                "output.png",
                "-d",
                "20",
            ],
        )
        logging.debug(result.output)
        assert result.exit_code == 0
        assert (temp_path / "output.png").exists()

        image = Image.open(temp_path / "output.png")
        if is_regeneration_enabled:
            MERGE_CONVERT_PNG_REFERENCE_IMAGE.update(image)  # pragma: no cover
        else:
            ia = ImageAnalyzer(MERGE_CONVERT_PNG_REFERENCE_IMAGE.load())
            assert ia.structural_similarity(image) > MIN_MERGE_PNG_SSIM
            ia.assert_same_size(image)
            (
                ia.histogram_compare_color(image)
                .assert_channel_count(4)
                .assert_greater_or_equal_values(0.99)
            )
