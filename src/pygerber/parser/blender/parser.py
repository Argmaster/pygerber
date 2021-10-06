# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Deque
from typing import Tuple

from PyR3.shortcut.context import Objects
from PyR3.shortcut.context import wipeScenes
from PyR3.shortcut.io import export_to
from PyR3.shortcut.material import new_node_material
from PyR3.shortcut.material import update_BSDF_node
from PyR3.shortcut.mesh import fromPyData
from PyR3.shortcut.mesh import join

from pygerber.parser.blender.apertures.circle import BlenderCircle
from pygerber.parser.blender.apertures.custom import BlenderCustom
from pygerber.parser.blender.apertures.obround import BlenderObround
from pygerber.parser.blender.apertures.polygon import BlenderPolygon
from pygerber.parser.blender.apertures.rectangle import BlenderRectangle
from pygerber.parser.blender.apertures.region import BlenderRegion
from pygerber.parser.parser import AbstractParser
from pygerber.renderer.apertureset import ApertureSet
from pygerber.tokens.token import Token


@dataclass
class LayerSpec:
    material: dict
    thickness: float = 0.78


DEFAULT_LAYER_GREEN = LayerSpec({"color": (50 / 255, 150 / 255, 50 / 255, 1)})

BLENDER_APERTURE_SET = ApertureSet(
    BlenderCircle,
    BlenderRectangle,
    BlenderObround,
    BlenderPolygon,
    BlenderCustom,
    BlenderRegion,
)


class ParserWithBlender(AbstractParser):

    apertureSet = BLENDER_APERTURE_SET

    def __init__(
        self,
        *,
        scale: float = 1.0,
        layer_spec: LayerSpec = DEFAULT_LAYER_GREEN,
        ignore_deprecated: bool = True,
    ) -> None:
        super().__init__(ignore_deprecated=ignore_deprecated)
        self.scale = scale
        self.layer_spec = layer_spec

    def _inject_layer_spec_to_renderer(self):
        self.renderer.material = new_node_material()
        update_BSDF_node(self.renderer.material, **self.layer_spec.material)
        self.renderer.thickness = self.layer_spec.thickness
        self.renderer.tree = None

    def _render(self, token_stack: Deque[Token]) -> None:
        wipeScenes()
        self._inject_layer_spec_to_renderer()
        self.renderer.render(token_stack)
        Objects.select_all()
        tree = fromPyData([(0.0, 0.0, 0.0)])
        join(tree, *self.renderer.tree)

    def save(self, file_path: str) -> None:
        """Saves scene content in file. File format is determined from file extension.

        :param file_path: File save path.
        :type file_path: str
        """
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        export_to(file_path)
