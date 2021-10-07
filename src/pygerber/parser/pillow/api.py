# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import sys
from concurrent.futures import Future
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List

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


class PillowProjectSpec(ProjectSpecBase):
    dpi: int = 600
    ignore_deprecated: bool = True
    image_padding: int = 0
    layers: List[PillowLayerSpec] = []

    @property
    def LayerSpecClass(self) -> PillowLayerSpec:
        return PillowLayerSpec

    def render(self) -> Image.Image:
        if _get_skip_next_render() is False:
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
                _render_file,
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


def _render_file(
    file_path: str,
    dpi: int = 600,
    colors: ColorSet = DEFAULT_COLOR_SET_GREEN,
    ignore_deprecated: bool = True,
    image_padding: int = 0,
):
    parser = ParserWithPillow(
        dpi=dpi,
        colors=colors,
        ignore_deprecated=ignore_deprecated,
        image_padding=image_padding,
    )
    parser.parse_file(file_path)
    return parser.get_image()
