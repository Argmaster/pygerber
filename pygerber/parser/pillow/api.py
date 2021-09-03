# -*- coding: utf-8 -*-
from __future__ import annotations

from concurrent.futures import Future, ProcessPoolExecutor
from dataclasses import dataclass
from typing import List, Tuple

from PIL import Image
from pygerber.parser.pillow.parser import ColorSet, ParserWithPillow


@dataclass
class LayerSpec:
    filepath: str
    colors: ColorSet


def render_file_and_save(filepath: str, savepath: str, **kwargs):
    """
    Loads, parses, renders file from `filepath` and saves it in `savepath`.
    **kwargs will be passed to ParserWithPillow, check it out for available params.
    """
    image = render_file(filepath, **kwargs)
    image.save(savepath)


def render_file(filepath: str, **kwargs) -> Image.Image:
    """
    Loads, parses and renders file from given path and returns its render as PIL.Image.Image.
    **kwargs will be passed to ParserWithPillow, check it out for available params.
    """
    parser = ParserWithPillow(filepath, **kwargs)
    parser.render()
    return parser.get_image()


def join_layers(layers: List[Image.Image]) -> Image.Image:
    if not layers:
        raise ValueError("You have to provide at least one layer.")
    bottom_most_layer = layers[0].copy()
    base_size = bottom_most_layer.size
    for layer in layers[1:]:
        base_width, base_height = base_size
        width, height = layer.size
        delta_width = (width - base_width) // 2
        delta_height = (height - base_height) // 2
        bottom_most_layer.paste(layer, (delta_width, delta_height), layer)
    return bottom_most_layer


def render_layers(
    layers: List[LayerSpec],
    *,
    dpi: int = 600,
    ignore_deprecated: bool = True,
    image_padding: int = 0,
) -> List[Image.Image]:
    with ProcessPoolExecutor() as executor:
        processes = __submit_rendering_processes(
            layers, executor, dpi, ignore_deprecated, image_padding
        )
        results = __get_rendering_processes_results(processes)
    return results


def __get_rendering_processes_results(processes):
    results: List[Image.Image] = []
    for future in processes:
        rendered_image: Image.Image = future.result()
        results.append(rendered_image)
    return results


def __submit_rendering_processes(
    layers, executor, dpi, ignore_deprecated, image_padding
):
    processes: List[Future] = []
    for layer in layers:
        future = executor.submit(
            render_file,
            layer.filepath,
            dpi=dpi,
            colors=layer.colors,
            ignore_deprecated=ignore_deprecated,
            image_padding=image_padding,
        )
        processes.append(future)
    return processes
