from __future__ import annotations

from click.testing import CliRunner
from PIL import Image

from pygerber.backend.rasterized_2d.color_scheme import ColorScheme
from pygerber.console.commands import _project, _raster, _vector
from pygerber.examples import ExamplesEnum, get_example_path
from test.conftest import cd_to_tempdir


def test_raster_render_all_default() -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            _raster,
            [
                get_example_path(ExamplesEnum.UCAMCO_ex_2_Shapes).as_posix(),
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
            == ColorScheme.DEBUG_1_ALPHA.solid_region_color.as_rgb_int()
        )


def test_raster_render_dpmm_40() -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            _raster,
            [
                get_example_path(ExamplesEnum.UCAMCO_ex_2_Shapes).as_posix(),
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


def test_raster_render_pixel_format_rgba_png() -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            _raster,
            [
                get_example_path(ExamplesEnum.UCAMCO_ex_2_Shapes).as_posix(),
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
            == ColorScheme.DEBUG_1_ALPHA.solid_region_color.as_rgba_int()
        )


def test_raster_render_file_type_copper_rgb_png() -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            _raster,
            [
                get_example_path(ExamplesEnum.UCAMCO_ex_2_Shapes).as_posix(),
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
            image.getpixel((400, 100))
            == ColorScheme.COPPER.solid_region_color.as_rgb_int()
        )


def test_raster_render_file_type_copper_rgba_png() -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            _raster,
            [
                get_example_path(ExamplesEnum.UCAMCO_ex_2_Shapes).as_posix(),
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
            == ColorScheme.COPPER_ALPHA.solid_region_color.as_rgba_int()
        )


def test_raster_render_pixel_format_rgba_jpg() -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            _raster,
            [
                get_example_path(ExamplesEnum.UCAMCO_ex_2_Shapes).as_posix(),
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


def test_raster_render_file_type_copper_rgb_jpg() -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            _raster,
            [
                get_example_path(ExamplesEnum.UCAMCO_ex_2_Shapes).as_posix(),
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


def test_vector_render_all_default() -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            _vector,
            [
                get_example_path(ExamplesEnum.UCAMCO_ex_2_Shapes).as_posix(),
                "-o",
                "output.svg",
            ],
        )
        assert result.exit_code == 0
        assert (temp_path / "output.svg").exists()

        image = (temp_path / "output.svg").read_bytes()
        assert len(image) > 0
        assert image.startswith(b"""<?xml version="1.0" encoding="UTF-8"?>""")

        color_hex = ColorScheme.DEBUG_1_ALPHA.solid_region_color.to_hex()

        assert f"""fill="{color_hex}" """.encode() in image


def test_vector_render_file_type_copper() -> None:
    runner = CliRunner()
    with cd_to_tempdir() as temp_path:
        result = runner.invoke(
            _vector,
            [
                get_example_path(ExamplesEnum.UCAMCO_ex_2_Shapes).as_posix(),
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

        color_hex = ColorScheme.COPPER.solid_region_color.to_hex()

        assert f"""fill="{color_hex}" """.encode() in image


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
            image.getpixel((400, 100))
            == ColorScheme.COPPER.solid_region_color.as_rgb_int()
        )
        assert (
            image.getpixel((80, 100))
            == ColorScheme.PASTE_MASK.solid_region_color.as_rgb_int()
        )
        assert (
            image.getpixel((190, 392))
            == ColorScheme.SILK.solid_region_color.as_rgb_int()
        )


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
        image.show()
        assert image.size == (766, 1071)

        assert image.getpixel((0, 0)) == (0, 0, 0)
        assert (
            image.getpixel((400, 100))
            == ColorScheme.COPPER.solid_region_color.as_rgb_int()
        )
        assert (
            image.getpixel((80, 100))
            == ColorScheme.PASTE_MASK.solid_region_color.as_rgb_int()
        )
        assert (
            image.getpixel((190, 392))
            == ColorScheme.SILK.solid_region_color.as_rgb_int()
        )
