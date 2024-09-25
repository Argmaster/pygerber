"""The `_enums` module contains all enumerations used by API."""

from __future__ import annotations

import re
from enum import Enum, unique
from typing import TYPE_CHECKING, Dict, Optional

from pygerber.vm.types.style import Style

if TYPE_CHECKING:
    from typing_extensions import TypeAlias


@unique
class OnParserErrorEnum(Enum):
    """Enumeration of possible actions to take on parser error."""

    Ignore = "ignore"
    """Ignore parser errors. Errors which occurred will not be signaled. May yield
    unexpected results for broken files, with missing draw commands or even more
    significant errors."""

    Warn = "warn"
    """Warn on parser error. Parser will log warning message about what went wrong.
    Best for supporting wide range of files without silently ignoring errors in code."""

    Raise = "raise"
    """Raise exception whenever parser encounters error. Will completely break out of
    parsing process, making it impossible to render slightly malformed files."""


@unique
class FileTypeEnum(Enum):
    """Enumeration of possible Gerber file types.

    If file type is not listed here you can request adding it by creating an issue on
    https://github.com/Argmaster/pygerber/issues
    """

    COPPER = "COPPER"
    MASK = "MASK"
    PASTE = "PASTE"
    SILK = "SILK"
    EDGE = "EDGE"

    PLATED = "PLATED"
    NON_PLATED = "NON_PLATED"
    PROFILE = "PROFILE"
    SOLDERMASK = "SOLDERMASK"
    LEGEND = "LEGEND"
    COMPONENT = "COMPONENT"
    GLUE = "GLUE"
    CARBONMASK = "CARBONMASK"
    GOLDMASK = "GOLDMASK"
    HEATSINKMASK = "HEATSINKMASK"
    PEELABLEMASK = "PEELABLEMASK"
    SILVERMASK = "SILVERMASK"
    TINMASK = "TINMASK"
    DEPTHROUT = "DEPTHROUT"
    VCUT = "VCUT"
    VIAFILL = "VIAFILL"
    PADS = "PADS"

    OTHER = "OTHER"
    UNDEFINED = "UNDEFINED"

    INFER_FROM_EXTENSION = "INFER_FROM_EXTENSION"
    INFER_FROM_ATTRIBUTES = "INFER_FROM_ATTRIBUTES"
    INFER = "INFER"

    @classmethod
    def infer_from_attributes(cls, file_function: Optional[str] = None) -> FileTypeEnum:
        """Infer file type from file extension."""
        if file_function is None:
            return cls.UNDEFINED

        function, *_ = file_function.split(",")
        function = function.upper()

        try:
            return FileTypeEnum(function)
        except (ValueError, TypeError, KeyError):
            return cls.UNDEFINED

    @classmethod
    def infer_from_extension(cls, extension: str) -> FileTypeEnum:
        if re.match(r"\.g[0-9]+", extension):
            return FileTypeEnum.COPPER

        if re.match(r"\.gp[0-9]+", extension):
            return FileTypeEnum.COPPER

        if re.match(r"\.gm[0-9]+", extension):
            return FileTypeEnum.COPPER

        return GERBER_EXTENSION_TO_FILE_TYPE_MAPPING.get(
            extension.lower(), FileTypeEnum.UNDEFINED
        )


GERBER_EXTENSION_TO_FILE_TYPE_MAPPING: Dict[str, FileTypeEnum] = {
    ".grb": FileTypeEnum.INFER_FROM_ATTRIBUTES,
    ".gbr": FileTypeEnum.INFER_FROM_ATTRIBUTES,
    ".gto": FileTypeEnum.SILK,
    ".gbo": FileTypeEnum.SILK,
    ".gpt": FileTypeEnum.PADS,
    ".gpb": FileTypeEnum.PADS,
    ".gts": FileTypeEnum.SOLDERMASK,
    ".gbs": FileTypeEnum.SOLDERMASK,
    ".gtl": FileTypeEnum.COPPER,
    ".gbl": FileTypeEnum.COPPER,
    ".gtp": FileTypeEnum.PASTE,
    ".gbp": FileTypeEnum.PASTE,
}

COLOR_MAP_T: TypeAlias = Dict[FileTypeEnum, Style]
DEFAULT_COLOR_MAP: COLOR_MAP_T = {
    FileTypeEnum.COPPER: Style.presets.COPPER,
    FileTypeEnum.MASK: Style.presets.SOLDER_MASK,
    FileTypeEnum.PASTE: Style.presets.PASTE_MASK,
    FileTypeEnum.SILK: Style.presets.SILK,
    FileTypeEnum.EDGE: Style.presets.SILK,
    FileTypeEnum.OTHER: Style.presets.DEBUG_1_ALPHA,
    FileTypeEnum.UNDEFINED: Style.presets.DEBUG_1_ALPHA,
    FileTypeEnum.PLATED: Style.presets.SOLDER_MASK,
    FileTypeEnum.NON_PLATED: Style.presets.PASTE_MASK,
    FileTypeEnum.PROFILE: Style.presets.SILK,
    FileTypeEnum.SOLDERMASK: Style.presets.SOLDER_MASK,
    FileTypeEnum.LEGEND: Style.presets.SILK,
    FileTypeEnum.COMPONENT: Style.presets.PASTE_MASK,
    FileTypeEnum.GLUE: Style.presets.PASTE_MASK,
    FileTypeEnum.CARBONMASK: Style.presets.SOLDER_MASK,
    FileTypeEnum.GOLDMASK: Style.presets.SOLDER_MASK,
    FileTypeEnum.HEATSINKMASK: Style.presets.SOLDER_MASK,
    FileTypeEnum.PEELABLEMASK: Style.presets.SOLDER_MASK,
    FileTypeEnum.SILVERMASK: Style.presets.SOLDER_MASK,
    FileTypeEnum.TINMASK: Style.presets.SOLDER_MASK,
    FileTypeEnum.DEPTHROUT: Style.presets.PASTE_MASK,
    FileTypeEnum.VCUT: Style.presets.PASTE_MASK,
    FileTypeEnum.VIAFILL: Style.presets.PASTE_MASK,
    FileTypeEnum.PADS: Style.presets.PASTE_MASK,
}
DEFAULT_ALPHA_COLOR_MAP: COLOR_MAP_T = {
    FileTypeEnum.COPPER: Style.presets.COPPER_ALPHA,
    FileTypeEnum.MASK: Style.presets.SOLDER_MASK_ALPHA,
    FileTypeEnum.PASTE: Style.presets.PASTE_MASK_ALPHA,
    FileTypeEnum.SILK: Style.presets.SILK_ALPHA,
    FileTypeEnum.EDGE: Style.presets.SILK_ALPHA,
    FileTypeEnum.OTHER: Style.presets.DEBUG_1_ALPHA,
    FileTypeEnum.UNDEFINED: Style.presets.DEBUG_1_ALPHA,
    FileTypeEnum.PLATED: Style.presets.SOLDER_MASK_ALPHA,
    FileTypeEnum.NON_PLATED: Style.presets.PASTE_MASK_ALPHA,
    FileTypeEnum.PROFILE: Style.presets.SILK_ALPHA,
    FileTypeEnum.SOLDERMASK: Style.presets.SOLDER_MASK_ALPHA,
    FileTypeEnum.LEGEND: Style.presets.SILK_ALPHA,
    FileTypeEnum.COMPONENT: Style.presets.PASTE_MASK_ALPHA,
    FileTypeEnum.GLUE: Style.presets.PASTE_MASK_ALPHA,
    FileTypeEnum.CARBONMASK: Style.presets.SOLDER_MASK_ALPHA,
    FileTypeEnum.GOLDMASK: Style.presets.SOLDER_MASK_ALPHA,
    FileTypeEnum.HEATSINKMASK: Style.presets.SOLDER_MASK_ALPHA,
    FileTypeEnum.PEELABLEMASK: Style.presets.SOLDER_MASK_ALPHA,
    FileTypeEnum.SILVERMASK: Style.presets.SOLDER_MASK_ALPHA,
    FileTypeEnum.TINMASK: Style.presets.SOLDER_MASK_ALPHA,
    FileTypeEnum.DEPTHROUT: Style.presets.PASTE_MASK_ALPHA,
    FileTypeEnum.VCUT: Style.presets.PASTE_MASK_ALPHA,
    FileTypeEnum.VIAFILL: Style.presets.PASTE_MASK_ALPHA,
    FileTypeEnum.PADS: Style.presets.PASTE_MASK_ALPHA,
}
