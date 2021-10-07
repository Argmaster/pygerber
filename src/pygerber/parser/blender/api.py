# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import sys
from asyncio import Future
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List

from PyR3.shortcut.context import Objects
from PyR3.shortcut.context import wipeScenes
from PyR3.shortcut.io import import_from
from PyR3.shortcut.transform import Transform

from pygerber.parser.project_spec import LayerSpecBase
from pygerber.parser.project_spec import ProjectSpecBase

from .parser import DEFAULT_LAYER_GREEN
from .parser import LayerStructure
from .parser import ParserWithBlender

THIN_THICKNESS = 0.04
COPPER_THICKNESS = 0.78
MASK_THICKNESS = 0.10


TEMP_LOCAL = Path(__file__).parent / ".temp"
TEMP_LOCAL.mkdir(0o777, True, True)


NAMED_STRUCTURES = {
    "silk": LayerStructure(
        {
            "color": (255, 255, 255, 255),
            "metallic": 0.0,
            "roughness": 1.0,
        },
        THIN_THICKNESS,
    ),
    "paste_mask": LayerStructure(
        {
            "color": (117, 117, 117, 255),
            "metallic": 1.0,
            "roughness": 0.5,
        },
        MASK_THICKNESS,
    ),
    "solder_mask": LayerStructure(
        {
            "color": (153, 153, 153, 255),
            "metallic": 1.0,
            "roughness": 0.5,
        },
        MASK_THICKNESS,
    ),
    "copper": LayerStructure(
        {"color": (35, 140, 35, 255), "metallic": 1.0, "roughness": 0.7},
        COPPER_THICKNESS,
    ),
    "green": LayerStructure({"color": (30, 156, 63, 255)}, COPPER_THICKNESS),
    "debug": LayerStructure({"color": (210, 23, 227, 255)}, COPPER_THICKNESS),
    "debug2": LayerStructure({"color": (227, 179, 23, 255)}, COPPER_THICKNESS),
    "debug3": LayerStructure({"color": (227, 84, 23, 255)}, COPPER_THICKNESS),
}
_skip_next_render_cache = False


def _skip_next_render():
    global _skip_next_render_cache
    _skip_next_render_cache = True


def _get_skip_next_render():
    global _skip_next_render_cache
    if _skip_next_render_cache:
        _skip_next_render_cache = False
        return True
    else:
        return False


@dataclass
class BlenderLayerSpec(LayerSpecBase):
    file_path: str
    structure: LayerStructure

    @classmethod
    def load(cls, contents: Dict):
        file_path = cls._get_checked_file_path(contents)
        structure = contents.get("structure", None)
        if isinstance(structure, str):
            structure = NAMED_STRUCTURES.get(structure, None)
        else:
            structure = cls._clean_non_predefined_structure(structure, file_path)
        return cls(file_path, structure)

    @classmethod
    def _clean_non_predefined_structure(cls, structure, file_path):
        if structure is None:
            return cls._replace_none_color_with_named_color_based_on_file_name(
                structure, file_path, NAMED_STRUCTURES
            )
        elif isinstance(structure, dict):
            return LayerStructure(**structure)
        else:
            raise TypeError(
                f"Invalid type of Layer Struture parameter, expected dict, got {structure.__class__.__qualname__}"
            )



class BlenderProjectSpec(ProjectSpecBase):
    ignore_deprecated: bool = True
    scale: float = 1.0
    layers: List[BlenderLayerSpec] = []

    @property
    def LayerSpecClass(self) -> BlenderLayerSpec:
        return BlenderLayerSpec

    def render(self) -> None:
        if _get_skip_next_render() is False:
            return self._join_layers(self._render_layers())

    def _join_layers(self, layers: List[str]) -> None:
        wipeScenes()
        layer_z_location = 0
        for path, layer_structure in layers:
            layer_structure: LayerStructure
            layer_z_location += layer_structure.thickness / 2
            import_from(path)
            Objects.active.location = (0, 0, layer_z_location)
            layer_z_location += layer_structure.thickness / 2
            os.remove(path)
        Objects.select_all()
        Transform.move((0, 0, -layer_z_location))
        return

    def _render_layers(self) -> List[str]:
        results = []
        for index, layer in enumerate(self.layers):
            path, struct = _render_file_and_save(
                layer.file_path,
                TEMP_LOCAL / f"{index}.glb",
                layer_structure=layer.structure,
                scale=self.scale,
                ignore_deprecated=self.ignore_deprecated,
            )
            results.append((path, struct))
        return results


def _render_file_and_save(
    file_path: str,
    save_path: str,
    *,
    layer_structure: LayerStructure = DEFAULT_LAYER_GREEN,
    scale: float = 1,
    ignore_deprecated: bool = True,
):
    parser = ParserWithBlender(
        scale=scale,
        layer_structure=layer_structure,
        ignore_deprecated=ignore_deprecated,
    )
    parser.parse_file(file_path)
    parser.save(save_path)
    return save_path, layer_structure


