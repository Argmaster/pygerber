# -*- coding: utf-8 -*-
from __future__ import annotations

import os
from concurrent.futures import Future, ProcessPoolExecutor
from dataclasses import dataclass
from typing import Dict, List

from PIL import Image
from pygerber.parser.pillow.parser import (
    DEFAULT_COLOR_SET_GREEN,
    DEFAULT_COLOR_SET_ORANGE,
    ColorSet,
    ParserWithPillow,
)
import yaml
import json
import toml

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
    return ProjectSpec(spec).render()


def render_from_yaml(file_path: str) -> Image.Image:
    return ProjectSpec.from_yaml(file_path).render()


def render_from_json(file_path: str) -> Image.Image:
    return ProjectSpec.from_json(file_path).render()


def render_from_toml(file_path: str) -> Image.Image:
    return ProjectSpec.from_toml(file_path).render()


class ProjectSpec:
    dpi: int = 600
    ignore_deprecated: bool = True
    image_padding: int = 0
    layers: List[LayerSpec] = []

    def __init__(self, init_spec: Dict) -> None:
        self._load_init_spec(init_spec)

    def _load_init_spec(self, init_spec: Dict) -> None:
        for name in self.__class__.__annotations__:
            default = getattr(self.__class__, name, None)
            value = init_spec.get(name, default)
            setattr(self, name, value)
        self.__load_layers_as_LayerSpec()

    def __load_layers_as_LayerSpec(self):
        if not self.layers:
            raise ValueError("You have to provide at least one layer.")
        layers = []
        for layer_data in self.layers:
            layers.append(LayerSpec.load(layer_data))
        self.layers = layers

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
        with ProcessPoolExecutor() as executor:
            processes = self.__submit_rendering_processes(executor)
            results = self.__get_rendering_processes_results(processes)
        return results

    @staticmethod
    def __get_rendering_processes_results(processes):
        results: List[Image.Image] = []
        for future in processes:
            rendered_image: Image.Image = future.result()
            results.append(rendered_image)
        return results

    def __submit_rendering_processes(self, executor):
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
    def from_yaml(file_path: str) -> ProjectSpec:
        with open(file_path, "rb") as file:
            spec = yaml.safe_load(file)
        return ProjectSpec(spec)

    @staticmethod
    def from_json(file_path: str) -> ProjectSpec:
        with open(file_path, "r", encoding="utf-8") as file:
            spec = json.load(file)
        return ProjectSpec(spec)

    @staticmethod
    def from_toml(file_path: str) -> ProjectSpec:
        with open(file_path, "r", encoding="utf-8") as file:
            spec = toml.load(file)
        return ProjectSpec(spec)


@dataclass
class LayerSpec:
    file_path: str
    colors: ColorSet

    @staticmethod
    def load(contents: Dict):
        file_path = LayerSpec.__load_file_path(contents)
        colors = LayerSpec.__load_colors(contents)
        colors = LayerSpec.__replace_none_color_with_named_color_based_on_file_name(
            colors, file_path
        )
        return LayerSpec(file_path, colors)

    @staticmethod
    def __replace_none_color_with_named_color_based_on_file_name(colors, file_path):
        if colors is None:
            file_name = os.path.basename(file_path)
            for name, named_colors in NAMED_COLORS.items():
                if name in file_name:
                    colors = named_colors
                    break
        return colors

    @staticmethod
    def __load_file_path(contents):
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
    """
    Loads, parses, renders file from `file_path` and saves it in `save_path`.
    **kwargs will be passed to ParserWithPillow, check it out for available params.
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
    **kwargs will be passed to ParserWithPillow, check it out for available params.
    """
    parser = ParserWithPillow(
        file_path,
        dpi=dpi,
        colors=colors,
        ignore_deprecated=ignore_deprecated,
        image_padding=image_padding,
    )
    parser.render()
    return parser.get_image()
