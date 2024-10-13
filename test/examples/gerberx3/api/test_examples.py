from __future__ import annotations

from pathlib import Path
import shutil

import pytest

from pygerber.examples import ExamplesEnum, get_example_path
from test.conftest import cd_to_tempdir

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent


@pytest.mark.parametrize(
    "example_path",
    [
        *THIS_DIRECTORY.glob("*.example.py"),
    ],
    ids=lambda path: path.name,
)
def test_examples_with_output_png_image(example_path: Path) -> None:
    # with cd_to_tempdir():
    exec(example_path.read_text(encoding="utf-8"))  # noqa: S102
    assert (Path.cwd() / "output.png").exists()


@pytest.mark.parametrize(
    "example_path",
    [
        *THIS_DIRECTORY.glob("*.example_svg.py"),
    ],
    ids=lambda path: path.name,
)
def test_examples_with_output_svg_image(example_path: Path) -> None:
    # with cd_to_tempdir():
    exec(example_path.read_text(encoding="utf-8"))  # noqa: S102
    assert (Path.cwd() / "output.svg").exists()


@pytest.mark.parametrize(
    "example_path",
    [
        *THIS_DIRECTORY.glob("*.quickstart.py"),
    ],
    ids=lambda path: path.name,
)
def test_quickstart_examples(example_path: Path) -> None:
    with cd_to_tempdir():
        shutil.copy(
            get_example_path(ExamplesEnum.UCAMCO_2_11_2).as_posix(), "example.grb"
        )
        exec(example_path.read_text(encoding="utf-8"))  # noqa: S102


@pytest.mark.parametrize(
    "example_path",
    [
        *THIS_DIRECTORY.glob("*.singlefile.py"),
    ],
    ids=lambda path: path.name,
)
def test_single_file_examples(example_path: Path) -> None:
    with cd_to_tempdir():
        exec(example_path.read_text(encoding="utf-8"))  # noqa: S102


@pytest.mark.parametrize(
    "example_path",
    [
        *THIS_DIRECTORY.glob("*.no_output.py"),
    ],
    ids=lambda path: path.name,
)
def test_no_output_examples(example_path: Path) -> None:
    with cd_to_tempdir():
        exec(example_path.read_text(encoding="utf-8"))  # noqa: S102


def test_multi_layer_gerber_job() -> None:
    from pygerber.gerber.api._gerber_job_file import GerberJobFile
    from test.assets.gerberx3.A64_OLinuXino_rev_G import A64_OlinuXino_Rev_G

    gerber_job = GerberJobFile.from_file(A64_OlinuXino_Rev_G.gbrjob.path)
    project = gerber_job.to_project()

    assert len(project.top) != 0
    assert len(project.inner) != 0
    assert len(project.bottom) != 0
