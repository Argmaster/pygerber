"""The `api` module provides simple, high-level API for rendering
Gerber X3/X2 files.
"""

from __future__ import annotations

from pygerber.gerber.api._composite_view import (
    CompositeImage,
    CompositePillowImage,
    CompositeView,
)
from pygerber.gerber.api._enums import (
    DEFAULT_ALPHA_COLOR_MAP,
    DEFAULT_COLOR_MAP,
    FileTypeEnum,
)
from pygerber.gerber.api._errors import PathToGerberJobProjectNotDefinedError
from pygerber.gerber.api._gerber_file import (
    GerberFile,
    Image,
    ImageSpace,
    PillowImage,
    ShapelyImage,
    Units,
)
from pygerber.gerber.api._gerber_job_file import (
    DesignRules,
    FilesAttributes,
    GeneralSpecs,
    GenerationSoftware,
    GerberJobFile,
    Header,
    MaterialStackup,
    ProjectId,
    Size,
)
from pygerber.gerber.formatter.options import Options
from pygerber.vm.types import Color, Style

__all__ = [
    "DEFAULT_ALPHA_COLOR_MAP",
    "DEFAULT_COLOR_MAP",
    "Color",
    "CompositeImage",
    "CompositePillowImage",
    "CompositeView",
    "DesignRules",
    "FileTypeEnum",
    "FilesAttributes",
    "GeneralSpecs",
    "GenerationSoftware",
    "GerberFile",
    "GerberJobFile",
    "Header",
    "Image",
    "ImageSpace",
    "MaterialStackup",
    "Options",
    "PathToGerberJobProjectNotDefinedError",
    "PillowImage",
    "ProjectId",
    "ShapelyImage",
    "Size",
    "Style",
    "Units",
]
