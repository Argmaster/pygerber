# -*- coding: utf-8 -*-

from typing import Any, Dict

from PIL import Image

from pygerber.parser.pillow.parser import DEFAULT_COLOR_SET_GREEN, ColorSet

from .parser.pillow.api import PillowProjectSpec, _render_file


def render_from_spec(spec: Dict[str, Any]) -> Image.Image:
    """Render 2D image from specfile alike dictionary.

    :param spec: specfile parameters dictionary.
    :type spec: Dict
    :return: rendered and merged image.
    :rtype: Image.Image
    """
    return PillowProjectSpec(spec).render()


def render_from_yaml(file_path: str) -> Image.Image:
    """Render 2D image from specfile written in yaml.

    :param file_path: yaml specfile path.
    :type file_path: str
    :return: rendered and merged image.
    :rtype: Image.Image
    """
    return PillowProjectSpec.from_yaml(file_path).render()


def render_from_json(file_path: str) -> Image.Image:
    """Render 2D image from specfile written in json.

    :param file_path: json specfile path.
    :type file_path: str
    :return: rendered and merged image.
    :rtype: Image.Image
    """
    return PillowProjectSpec.from_json(file_path).render()


def render_from_toml(file_path: str) -> Image.Image:
    """Render 2D image from specfile written in toml.

    :param file_path: toml specfile path.
    :type file_path: str
    :return: rendered and merged image.
    :rtype: Image.Image
    """
    return PillowProjectSpec.from_toml(file_path).render()


def render_file_and_save(
    file_path: str,
    save_path: str,
    *,
    dpi: int = 600,
    colors: ColorSet = DEFAULT_COLOR_SET_GREEN,
    ignore_deprecated: bool = True,
    image_padding: int = 0,
):
    """Loads, parses, renders file from file_path and saves it in save_path.

    :param file_path: Path to gerber file.
    :type file_path: str
    :param save_path: Path to save render.
    :type save_path: str
    :param dpi: DPI of output image, defaults to 600
    :type dpi: int, optional
    :param colors: Color set to use, defaults to DEFAULT_COLOR_SET_GREEN
    :type colors: ColorSet, optional
    :param ignore_deprecated: If true, causes parser to not stop when deprecated syntax is found, defaults to True
    :type ignore_deprecated: bool, optional
    :param image_padding: Additional pixel padding for image, defaults to 0
    :type image_padding: int, optional
    """
    image = render_file(
        file_path,
        dpi=dpi,
        colors=colors,
        ignore_deprecated=ignore_deprecated,
        image_padding=image_padding,
    )
    image.save(save_path)


def render_file(
    file_path: str,
    *,
    dpi: int = 600,
    colors: ColorSet = DEFAULT_COLOR_SET_GREEN,
    ignore_deprecated: bool = True,
    image_padding: int = 0,
) -> Image.Image:
    """
    Loads, parses and renders file from given path and returns its render as PIL.Image.Image.

    :param file_path: Path to gerber file to render.
    :type file_path: str
    :param dpi: Output image DPI, defaults to 600
    :type dpi: int, optional
    :param colors: Color specification, defaults to DEFAULT_COLOR_SET_GREEN
    :type colors: ColorSet, optional
    :param ignore_deprecated: If false causes parser to stop when deprecated syntax is met, defaults to True
    :type ignore_deprecated: bool, optional
    :param image_padding: Additional image padding, defaults to 0
    :type image_padding: int, optional
    :return: Output image.
    :rtype: Image.Image
    """
    return _render_file(
        file_path,
        dpi,
        colors,
        ignore_deprecated,
        image_padding,
    )
