# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import os
import sys
from concurrent.futures import Future
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from typing import Dict
from typing import List

import toml
import yaml
from PIL import Image

import pygerber
from pygerber.parser.pillow.parser import DEFAULT_COLOR_SET_GREEN
from pygerber.parser.pillow.parser import DEFAULT_COLOR_SET_ORANGE
from pygerber.parser.pillow.parser import ColorSet
from pygerber.parser.pillow.parser import ParserWithPillow
from pygerber.parser.project_spec import LayerSpecBase
from pygerber.parser.project_spec import ProjectSpecBase

NAMED_COLORS = {
    "silk": ColorSet((255, 255, 255, 255)),
    "paste_mask": ColorSet((117, 117, 117, 255)),
    "solder_mask": ColorSet((153, 153, 153, 255)),
    "copper": ColorSet((40, 143, 40, 255), (60, 181, 60, 255)),
    "orange": DEFAULT_COLOR_SET_ORANGE,
    "green": DEFAULT_COLOR_SET_GREEN,
    "debug": ColorSet(
        (120, 120, 255, 255),
        (255, 120, 120, 255),
        (0, 0, 0, 0),
    ),
}


def render_from_spec(spec: Dict) -> Image.Image:
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


class PillowProjectSpec(ProjectSpecBase):
    dpi: int = 600
    ignore_deprecated: bool = True
    image_padding: int = 0
    layers: List[PillowLayerSpec] = []

    @property
    def LayerSpecClass(self) -> PillowLayerSpec:
        return PillowLayerSpec

    def render(self) -> Image.Image:
        return self._join_layers(self._render_layers())

    def _join_layers(self, layer_images: List[Image.Image]) -> Image.Image:
        bottom_most_layer = layer_images[0].copy()
        base_size = bottom_most_layer.size
        for layer in layer_images[1:]:
            self.__paste_layer(base_size, layer, bottom_most_layer)
        return bottom_most_layer

    @staticmethod
    def __paste_layer(base_size, layer, bottom_most_layer):
        base_width, base_height = base_size
        width, height = layer.size
        delta_width = (width - base_width) // 2
        delta_height = (height - base_height) // 2
        bottom_most_layer.paste(layer, (delta_width, delta_height), layer)

    def _render_layers(self) -> List[Image.Image]:
        NEW_PATH = list(sys.path)
        sys.path = pygerber.SYS_PATH
        with ProcessPoolExecutor() as executor:
            processes = self.__submit_rendering_processes(executor)
            results = self.__get_rendering_processes_results(processes)
        sys.path = NEW_PATH
        return results

    def __submit_rendering_processes(self, executor: ProcessPoolExecutor):
        processes: List[Future] = []
        for layer in self.layers:
            future = executor.submit(
                render_file,
                layer.file_path,
                dpi=self.dpi,
                colors=layer.colors,
                ignore_deprecated=self.ignore_deprecated,
                image_padding=self.image_padding,
            )
            processes.append(future)
        return processes

    @staticmethod
    def __get_rendering_processes_results(processes):
        results: List[Image.Image] = []
        for future in processes:
            rendered_image: Image.Image = future.result()
            results.append(rendered_image)
        return results


@dataclass
class PillowLayerSpec(LayerSpecBase):
    file_path: str
    colors: ColorSet

    @classmethod
    def load(cls, contents: Dict):
        file_path = cls._get_checked_file_path(contents)
        colors = cls.__load_colors(contents)
        colors = cls._replace_none_color_with_named_color_based_on_file_name(
            colors, file_path, NAMED_COLORS
        )
        return cls(file_path, colors)

    @staticmethod
    def _get_checked_file_path(contents):
        file_path = contents.get("file_path")
        os.path.exists(file_path)
        return file_path

    @staticmethod
    def __load_colors(contents):
        colors = contents.get("colors", None)
        if isinstance(colors, str):
            colors = NAMED_COLORS.get(colors)
        elif isinstance(colors, dict):
            colors = ColorSet(
                tuple(colors.get("dark")),
                tuple(colors.get("clear", (0, 0, 0, 0))),
                tuple(colors.get("background", (0, 0, 0, 0))),
            )
        elif isinstance(colors, list):
            colors = ColorSet(
                tuple(colors[0]),
                tuple(colors[1] if 1 < len(colors) else (0, 0, 0, 0)),
                tuple(colors[2] if 2 < len(colors) else (0, 0, 0, 0)),
            )
        elif colors is None:
            pass
        else:
            raise TypeError(f"Invalid color specification for LayerSpec: {colors}")
        return colors


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
    parser = ParserWithPillow(
        dpi=dpi,
        colors=colors,
        ignore_deprecated=ignore_deprecated,
        image_padding=image_padding,
    )
    parser.parse_file(file_path)
    return parser.get_image()
