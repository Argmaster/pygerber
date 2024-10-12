"""Utility for loading example Gerber files shipped with PyGerber."""

from __future__ import annotations

from enum import Enum
from pathlib import Path


class ExamplesEnum(Enum):
    """Enumeration of all available examples."""

    UCAMCO_2_11_2 = "ucamco_2_11_2.grb"
    ShapeFlashes = "shape_flashes.grb"
    simple_2layer_F_Cu = "simple_2layer-F_Cu.gbr"  # noqa: N815
    simple_2layer_F_Mask = "simple_2layer-F_Mask.gbr"  # noqa: N815
    simple_2layer_F_Paste = "simple_2layer-F_Paste.gbr"  # noqa: N815
    simple_2layer_F_Silkscreen = "simple_2layer-F_Silkscreen.gbr"  # noqa: N815

    carte_test_B_Cu = "carte_test-B_Cu.gbr"  # noqa: N815
    carte_test_B_Mask = "carte_test-B_Mask.gbr"  # noqa: N815
    carte_test_B_Paste = "carte_test-B_Paste.gbr"  # noqa: N815
    carte_test_B_Silkscreen = "carte_test-B_Silkscreen.gbr"  # noqa: N815

    carte_test_Edges = "carte_test-Edge_Cuts.gbr"  # noqa: N815

    carte_test_F_Cu = "carte_test-F_Cu.gbr"  # noqa: N815
    carte_test_F_Mask = "carte_test-F_Mask.gbr"  # noqa: N815
    carte_test_F_Silkscreen = "carte_test-F_Silkscreen.gbr"  # noqa: N815

    carte_test_gbrjob = "carte_test-job.gbrjob"


DIRECTORY = Path(__file__).parent


def get_example_path(example: ExamplesEnum) -> Path:
    """Get path to example Gerber file."""
    return DIRECTORY / example.value


def load_example(example: ExamplesEnum) -> str:
    """Load example Gerber file."""
    return get_example_path(example).read_text(encoding="utf-8")
