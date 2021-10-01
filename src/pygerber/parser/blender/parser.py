# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from PyR3.shortcut.context import wipeScenes
from PyR3.shortcut.io import ExportGlobal

from pygerber.mathclasses import BoundingBox
from pygerber.parser.blender.apertures.circle import BlenderCircle
from pygerber.parser.blender.apertures.custom import BlenderCustom
from pygerber.parser.blender.apertures.obround import BlenderObround
from pygerber.parser.blender.apertures.polygon import BlenderPolygon
from pygerber.parser.blender.apertures.rectangle import BlenderRectangle
from pygerber.parser.blender.apertures.region import BlenderRegion
from pygerber.parser.parser import AbstractParser
from pygerber.renderer.apertureset import ApertureSet

Color_Type = Tuple[float, float, float, float]


@dataclass
class LayerSpec:
    color: Color_Type
    thickness: float = 0.78e-3


DEFAULT_LAYER_GREEN = LayerSpec((50, 150, 50, 255))


class ParserWithBlender(AbstractParser):

    apertureSet = ApertureSet(
        BlenderCircle,
        BlenderRectangle,
        BlenderObround,
        BlenderPolygon,
        BlenderCustom,
        BlenderRegion,
    )

    def __init__(
        self,
        *,
        scale: float = 1,
        layer_spec: LayerSpec = DEFAULT_LAYER_GREEN,
        ignore_deprecated: bool = True,
    ) -> None:
        super().__init__(ignore_deprecated=ignore_deprecated)
        self.scale = scale
        self.layer_spec = layer_spec

    def _pre_render(self, _: BoundingBox):
        wipeScenes()

    def save(self, file_path: str) -> None:
        """Saves scene content in file. File format is determined from file extension.

        :param file_path: File save path.
        :type file_path: str
        """
        ExportGlobal(file_path)
