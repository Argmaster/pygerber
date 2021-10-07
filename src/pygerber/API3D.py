# -*- coding: utf-8 -*-

from typing import Any
from typing import Dict

from pygerber.parser.blender.parser import DEFAULT_LAYER_GREEN
from pygerber.parser.blender.parser import LayerStructure
from pygerber.parser.blender.parser import ParserWithBlender

from .parser.blender.api import BlenderProjectSpec
from .parser.blender.api import _render_file_and_save


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
    _render_file_and_save(
        file_path,
        save_path,
        layer_structure=layer_structure,
        scale=scale,
        ignore_deprecated=ignore_deprecated,
    )


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
