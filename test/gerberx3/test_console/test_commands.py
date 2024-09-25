from __future__ import annotations

import pytest
from click.testing import CliRunner
from PIL import Image

from pygerber.console.commands import _project, _raster, _vector
from pygerber.examples import ExamplesEnum, get_example_path
from pygerber.vm.types.style import Style
from test.conftest import cd_to_tempdir


@pytest.mark.xfail(reason="Not implemented")
def test_raster_render_all_default() -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            _raster,
            [
                get_example_path(ExamplesEnum.UCAMCO_2_11_2).as_posix(),
                "-o",
                "output.png",
            ],
        )
        assert result.exit_code == 0
        assert (temp_path / "output.png").exists()

        image = Image.open(temp_path / "output.png")
        assert image.size == (853, 761)

        assert image.getpixel((0, 0)) == (0, 0, 0)
        assert (
            image.getpixel((400, 100))
            == Style.presets.DEBUG_1_ALPHA.foreground.as_rgb_int()
        )


@pytest.mark.xfail(reason="Not implemented")
def test_raster_render_dpmm_40() -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            _raster,
            [
                get_example_path(ExamplesEnum.UCAMCO_2_11_2).as_posix(),
                "-o",
                "output.png",
                "-d",
                "40",
            ],
        )
        assert result.exit_code == 0
        assert (temp_path / "output.png").exists()

        image = Image.open(temp_path / "output.png")
        assert image.size == (1706, 1522)


@pytest.mark.xfail(reason="Not implemented")
def test_raster_render_pixel_format_rgba_png() -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            _raster,
            [
                get_example_path(ExamplesEnum.UCAMCO_2_11_2).as_posix(),
                "-o",
                "output.png",
                "-p",
                "RGBA",
            ],
        )
        assert result.exit_code == 0
        assert (temp_path / "output.png").exists()

        image = Image.open(temp_path / "output.png")
        assert image.size == (853, 761)

        assert image.getpixel((0, 0)) == (0, 0, 0, 0)
        assert (
            image.getpixel((400, 100))
            == Style.presets.DEBUG_1_ALPHA.foreground.as_rgba_int()
        )


@pytest.mark.xfail(reason="Not implemented")
def test_raster_render_file_type_copper_rgb_png() -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            _raster,
            [
                get_example_path(ExamplesEnum.UCAMCO_2_11_2).as_posix(),
                "-o",
                "output.png",
                "-p",
                "RGB",
                "-t",
                "COPPER",
            ],
        )
        assert result.exit_code == 0
        assert (temp_path / "output.png").exists()

        image = Image.open(temp_path / "output.png")
        assert image.size == (853, 761)

        assert image.getpixel((0, 0)) == (0, 0, 0)
        assert (
            image.getpixel((400, 100)) == Style.presets.COPPER.foreground.as_rgb_int()
        )


@pytest.mark.xfail(reason="Not implemented")
def test_raster_render_file_type_copper_rgba_png() -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            _raster,
            [
                get_example_path(ExamplesEnum.UCAMCO_2_11_2).as_posix(),
                "-o",
                "output.png",
                "-p",
                "RGBA",
                "-t",
                "COPPER",
            ],
        )
        assert result.exit_code == 0
        assert (temp_path / "output.png").exists()

        image = Image.open(temp_path / "output.png")
        assert image.size == (853, 761)

        assert image.getpixel((0, 0)) == (0, 0, 0, 0)
        assert (
            image.getpixel((400, 100))
            == Style.presets.COPPER_ALPHA.foreground.as_rgba_int()
        )


@pytest.mark.xfail(reason="Not implemented")
def test_raster_render_pixel_format_rgba_jpg() -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            _raster,
            [
                get_example_path(ExamplesEnum.UCAMCO_2_11_2).as_posix(),
                "-o",
                "output.jpg",
                "-p",
                "RGB",
            ],
        )
        assert result.exit_code == 0
        assert (temp_path / "output.jpg").exists()

        image = Image.open(temp_path / "output.jpg")
        assert image.size == (853, 761)

        assert image.getpixel((0, 0)) == (0, 0, 0)
        # Can't compare to exact color because of JPEG compression.
        assert image.getpixel((400, 100)) != (0, 0, 0)


@pytest.mark.xfail(reason="Not implemented")
def test_raster_render_file_type_copper_rgb_jpg() -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            _raster,
            [
                get_example_path(ExamplesEnum.UCAMCO_2_11_2).as_posix(),
                "-o",
                "output.jpg",
                "-p",
                "RGB",
                "-t",
                "COPPER",
            ],
        )
        assert result.exit_code == 0
        assert (temp_path / "output.jpg").exists()

        image = Image.open(temp_path / "output.jpg")
        assert image.size == (853, 761)

        assert image.getpixel((0, 0)) == (0, 0, 0)
        # Can't compare to exact color because of JPEG compression.
        assert image.getpixel((400, 100)) != (0, 0, 0)


@pytest.mark.xfail(reason="Not implemented")
def test_vector_render_all_default() -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            _vector,
            [
                get_example_path(ExamplesEnum.UCAMCO_2_11_2).as_posix(),
                "-o",
                "output.svg",
            ],
        )
        assert result.exit_code == 0
        assert (temp_path / "output.svg").exists()

        image = (temp_path / "output.svg").read_bytes()
        assert len(image) > 0
        assert image.startswith(b"""<?xml version="1.0" encoding="UTF-8"?>""")

        color_hex = Style.presets.DEBUG_1_ALPHA.foreground.to_hex()

        assert f"""fill="{color_hex}" """.encode() in image


@pytest.mark.xfail(reason="Not implemented")
def test_vector_render_file_type_copper() -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            _vector,
            [
                get_example_path(ExamplesEnum.UCAMCO_2_11_2).as_posix(),
                "-o",
                "output.svg",
                "-t",
                "COPPER",
            ],
        )
        assert result.exit_code == 0
        assert (temp_path / "output.svg").exists()

        image = (temp_path / "output.svg").read_bytes()
        assert len(image) > 0
        assert image.startswith(b"""<?xml version="1.0" encoding="UTF-8"?>""")

        color_hex = Style.presets.COPPER.foreground.to_hex()

        assert f"""fill="{color_hex}" """.encode() in image


@pytest.mark.xfail(reason="Not implemented")
def test_project_render_default() -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            _project,
            [
                get_example_path(ExamplesEnum.simple_2layer_F_Cu).as_posix(),
                get_example_path(ExamplesEnum.simple_2layer_F_Mask).as_posix(),
                get_example_path(ExamplesEnum.simple_2layer_F_Paste).as_posix(),
                get_example_path(ExamplesEnum.simple_2layer_F_Silkscreen).as_posix(),
                "-o",
                "output.png",
            ],
        )
        assert result.exit_code == 0
        assert (temp_path / "output.png").exists()

        image = Image.open(temp_path / "output.png")
        assert image.size == (766, 1071)

        assert image.getpixel((0, 0)) == (0, 0, 0)
        assert (
            image.getpixel((400, 100)) == Style.presets.COPPER.foreground.as_rgb_int()
        )
        assert (
            image.getpixel((80, 100))
            == Style.presets.PASTE_MASK.foreground.as_rgb_int()
        )
        assert image.getpixel((190, 392)) == Style.presets.SILK.foreground.as_rgb_int()


@pytest.mark.xfail(reason="Not implemented")
def test_project_render_with_file_type_tags() -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            _project,
            [
                f"{get_example_path(ExamplesEnum.simple_2layer_F_Cu).as_posix()}@copper",
                f"{get_example_path(ExamplesEnum.simple_2layer_F_Mask).as_posix()}@mask",
                f"{get_example_path(ExamplesEnum.simple_2layer_F_Paste).as_posix()}@paste",
                f"{get_example_path(ExamplesEnum.simple_2layer_F_Silkscreen).as_posix()}@silk",
                "-o",
                "output.png",
            ],
        )
        assert result.exit_code == 0
        assert (temp_path / "output.png").exists()

        image = Image.open(temp_path / "output.png")
        assert image.size == (766, 1071)

        assert image.getpixel((0, 0)) == (0, 0, 0)
        assert (
            image.getpixel((400, 100)) == Style.presets.COPPER.foreground.as_rgb_int()
        )
        assert (
            image.getpixel((80, 100))
            == Style.presets.PASTE_MASK.foreground.as_rgb_int()
        )
        assert image.getpixel((190, 392)) == Style.presets.SILK.foreground.as_rgb_int()
