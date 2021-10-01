# -*- coding: utf-8 -*-
from __future__ import annotations

from .parser import DEFAULT_LAYER_GREEN
from .parser import LayerSpec
from .parser import ParserWithBlender

THIN_THICKNESS = 0.01e-3
COPPER_THICKNESS = 0.78e-3

NAMED_LAYER_SPEC = {
    "silk": LayerSpec((255, 255, 255, 255), THIN_THICKNESS),
    "paste_mask": LayerSpec((117, 117, 117, 255), THIN_THICKNESS),
    "solder_mask": LayerSpec((153, 153, 153, 255), THIN_THICKNESS),
    "copper": LayerSpec((40, 143, 40, 255), COPPER_THICKNESS),
    "green": LayerSpec((30, 156, 63, 255), COPPER_THICKNESS),
    "debug": LayerSpec((210, 23, 227, 255), COPPER_THICKNESS),
    "debug2": LayerSpec((227, 179, 23, 255), COPPER_THICKNESS),
    "debug3": LayerSpec((227, 84, 23, 255), COPPER_THICKNESS),
}


def render_file_and_save(
    file_path: str,
    save_path: str,
    *,
    layer_spec: LayerSpec = DEFAULT_LAYER_GREEN,
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
        layer_spec=layer_spec,
        ignore_deprecated=ignore_deprecated,
    )
    parser.parse_file(file_path)
    parser.save(save_path)


def render_file(
    file_path: str,
    *,
    layer_spec: LayerSpec = DEFAULT_LAYER_GREEN,
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
        layer_spec=layer_spec,
        ignore_deprecated=ignore_deprecated,
    )
    parser.parse_file(file_path)
