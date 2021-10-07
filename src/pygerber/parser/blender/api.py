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

THIN_THICKNESS = 0.01
COPPER_THICKNESS = 0.78


TEMP_LOCAL = Path(__file__).parent / ".temp"
TEMP_LOCAL.mkdir(0o777, True, True)


NAMED_STRUCTURES = {
    "silk": LayerStructure(
        {
            "color": (255, 255, 255, 255),
        },
        THIN_THICKNESS,
    ),
    "paste_mask": LayerStructure(
        {
            "color": (117, 117, 117, 255),
        },
        THIN_THICKNESS * 5,
    ),
    "solder_mask": LayerStructure({"color": (153, 153, 153, 255)}, THIN_THICKNESS * 5),
    "copper": LayerStructure({"color": (40, 143, 40, 255)}, COPPER_THICKNESS),
    "green": LayerStructure({"color": (30, 156, 63, 255)}, COPPER_THICKNESS),
    "debug": LayerStructure({"color": (210, 23, 227, 255)}, COPPER_THICKNESS),
    "debug2": LayerStructure({"color": (227, 179, 23, 255)}, COPPER_THICKNESS),
    "debug3": LayerStructure({"color": (227, 84, 23, 255)}, COPPER_THICKNESS),
}


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


def render_from_spec(spec: Dict[str, Any]) -> None:
    """Render 3D model from specfile alike dictionary.
    Model is available globally via blender / PyR3.shortcuts API.

    :param spec: specfile parameters dictionary.
    :type spec: Dict
    :return: rendered and merged image.
    :rtype: Image.Image
    """
    return BlenderProjectSpec(spec).render()


def render_from_yaml(file_path: str) -> None:
    """Render 3D image from specfile written in yaml.
    Model is available globally via blender / PyR3.shortcuts API.

    :param file_path: yaml specfile path.
    :type file_path: str
    :return: rendered and merged image.
    :rtype: Image.Image
    """
    return BlenderProjectSpec.from_yaml(file_path).render()


def render_from_json(file_path: str) -> None:
    """Render 3D image from specfile written in json.
    Model is available globally via blender / PyR3.shortcuts API.

    :param file_path: json specfile path.
    :type file_path: str
    :return: rendered and merged image.
    :rtype: Image.Image
    """
    return BlenderProjectSpec.from_json(file_path).render()


def render_from_toml(file_path: str) -> None:
    """Render 3D image from specfile written in toml.
    Model is available globally via blender / PyR3.shortcuts API.

    :param file_path: toml specfile path.
    :type file_path: str
    :return: rendered and merged image.
    :rtype: Image.Image
    """
    return BlenderProjectSpec.from_toml(file_path).render()


class BlenderProjectSpec(ProjectSpecBase):
    ignore_deprecated: bool = True
    scale: float = 1.0
    layers: List[BlenderLayerSpec] = []

    @property
    def LayerSpecClass(self) -> BlenderLayerSpec:
        return BlenderLayerSpec

    def render(self) -> None:
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
    render_file_and_save(
        file_path,
        save_path,
        layer_structure=layer_structure,
        scale=scale,
        ignore_deprecated=ignore_deprecated,
    )
    return save_path, layer_structure


def render_file_and_save(
    file_path: str,
    save_path: str,
    *,
    layer_structure: LayerStructure = DEFAULT_LAYER_GREEN,
    scale: float = 1,
    ignore_deprecated: bool = True,
):
    """Loads, parses, renders file from file_path and saves it in save_path.
    File format is determined by save_path extension.

    :param file_path: Path to gerber file to render.
    :type file_path: str
    :param save_path: Path to save render.
    :type save_path: str
    :param scale: Output model scale, defaults to 1
    :type scale: float, optional
    :param layer_spec: Rendering specification, defaults to DEFAULT_LAYER_GREEN
    :type layer_spec: LayerSpec, optional
    :param ignore_deprecated: If false causes parser to stop when deprecated syntax is met, defaults to True
    :type ignore_deprecated: bool, optional
    """
    parser = ParserWithBlender(
        scale=scale,
        layer_structure=layer_structure,
        ignore_deprecated=ignore_deprecated,
    )
    parser.parse_file(file_path)
    parser.save(save_path)


def render_file(
    file_path: str,
    *,
    layer_spec: LayerStructure = DEFAULT_LAYER_GREEN,
    scale: float = 1,
    ignore_deprecated: bool = True,
) -> None:
    """Loads, parses and renders file from given path.

    :param file_path: Path to gerber file to render.
    :type file_path: str
    :param scale: Output model scale, defaults to 1
    :type scale: float, optional
    :param layer_spec: Rendering specification, defaults to DEFAULT_LAYER_GREEN
    :type layer_spec: LayerSpec, optional
    :param ignore_deprecated: If false causes parser to stop when deprecated syntax is met, defaults to True
    :type ignore_deprecated: bool, optional
    """
    parser = ParserWithBlender(
        scale=scale,
        layer_structure=layer_spec,
        ignore_deprecated=ignore_deprecated,
    )
    parser.parse_file(file_path)
