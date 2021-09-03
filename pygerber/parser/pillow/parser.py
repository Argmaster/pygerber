# -*- coding: utf-8 -*-
from __future__ import annotations

from concurrent.futures import Future, ProcessPoolExecutor
from dataclasses import dataclass
from typing import List, Tuple

from PIL import Image, ImageDraw
from pygerber.mathclasses import BoundingBox
from pygerber.meta.apertureset import ApertureSet
from pygerber.parser.pillow.apertures import *
from pygerber.tokenizer import Tokenizer

Color_Type = Tuple[float, float, float, float]


@dataclass
class ColorSet:

    dark: Color_Type
    clear: Color_Type = (0, 0, 0, 0)
    background: Color_Type = (0, 0, 0, 0)


DEFAULT_COLOR_SET_ORANGE = ColorSet(
    (209, 110, 44),
    (0, 0, 0, 0),
    (0, 0, 0, 0),
)
DEFAULT_COLOR_SET_GREEN = ColorSet(
    (66, 166, 66, 255),
    (16, 66, 36, 255),
    (16, 66, 36, 255),
)


class ImageSizeNullError(IndexError):
    pass


@dataclass
class LayerSpec:
    filepath: str
    colors: ColorSet


class ParserWithPillow:

    tokenizer: Tokenizer
    apertureSet = ApertureSet(
        PillowCircle,
        PillowRectangle,
        PillowObround,
        PillowPolygon,
        PillowCustom,
        PillowRegion,
    )
    is_rendered: bool

    def __init__(
        self,
        filepath: str = None,
        string_source: str = None,
        *,
        dpi: int = 600,
        colors: ColorSet = DEFAULT_COLOR_SET_GREEN,
        ignore_deprecated: bool = True,
        image_padding: int = 0,
    ) -> None:
        """
        If `filepath` is None, `string_source` will be used as source,
        otherwise filepath will be used to read and parse file, then
        string_source will be complitely ignored. Passing None to both
        will result in RuntimeError.
        `dpi` controls DPI of output image.
        `colors` represents colorset to be used to render file.
        `ignore_deprecated` causes parser to ignore deprecated syntax.
        `image_padding` specifies padding in pixels of output image in every direction.
        """
        self.image_padding = image_padding
        self.is_rendered = False
        self.tokenizer = Tokenizer(
            self.apertureSet,
            ignore_deprecated=ignore_deprecated,
        )
        self.colors = colors
        self.dpmm = dpi / 25.4
        self.__tokenize(filepath, string_source)

    def __tokenize(self, filepath: str, string_source: str) -> None:
        if filepath is not None:
            self.tokenizer.tokenize_file(filepath)
        elif string_source is not None:
            self.tokenizer.tokenize_string(string_source)
        else:
            raise RuntimeError("filepath and source_string can't be both None.")

    @property
    def canvas(self) -> Image.Image:
        return self.tokenizer.meta.canvas

    def render(self) -> None:
        if not self.is_rendered:
            self.__preprare_meta()
            self.tokenizer.render()
            self.is_rendered = True
        else:
            raise RuntimeError("Attempt to render already rendered canvas.")

    def __preprare_meta(self) -> None:
        self.__prepare_canvas()
        self.tokenizer.meta.colors = self.colors
        self.tokenizer.meta.dpmm = self.dpmm

    def __prepare_canvas(self) -> None:
        bbox = self.__get_canvas_bbox()
        width, height = self.__get_canvas_size(bbox)
        self.tokenizer.meta.canvas = Image.new(
            "RGBA", (width, height), self.colors.background
        )
        self.tokenizer.meta.draw_canvas = ImageDraw.Draw(self.canvas)
        left_offset, bottom_offset = self.__get_drawing_offset(bbox)
        self.tokenizer.meta.left_offset = left_offset
        self.tokenizer.meta.bottom_offset = bottom_offset

    def __get_canvas_bbox(self) -> BoundingBox:
        bbox = self.tokenizer.get_bbox()
        if bbox.width() == 0 or bbox.height() == 0:
            raise ImageSizeNullError("Image has null width or height.")
        return bbox

    def __get_canvas_size(self, bbox: BoundingBox) -> Tuple[int, int]:
        return (
            self._prepare_co(bbox.width()) + self.image_padding * 2,
            self._prepare_co(bbox.height()) + self.image_padding * 2,
        )

    def __get_drawing_offset(self, bbox: BoundingBox) -> Tuple[int, int]:
        return (
            self._prepare_co(-bbox.left) + self.image_padding,
            self._prepare_co(-bbox.lower) + self.image_padding,
        )

    def _prepare_co(self, value: float) -> float:
        return int(value * self.dpmm)

    def get_image(self) -> Image.Image:
        if self.is_rendered:
            return self.__get_image()
        else:
            raise RuntimeError("Can't return canvas that was not rendered.")

    def __get_image(self) -> Image.Image:
        return self.canvas.transpose(Image.FLIP_TOP_BOTTOM)

    def save(self, filepath: str, format: str = None) -> None:
        """
        Saves rendered image.
        `filepath` A filename (string), pathlib.Path object or file object.
        `format` Optional format override. If omitted, the format to use is determined
        from the filename extension. If a file object was used instead of a filename,
        this parameter should always be used.
        """
        if format is not None:
            self.get_image().save(filepath, format)
        else:
            self.get_image().save(filepath)

    @staticmethod
    def render_file_and_save(filepath: str, savepath: str, **kwargs):
        """
        Loads, parses, renders file from `filepath` and saves it in `savepath`.
        **kwargs will be passed to ParserWithPillow, check it out for available params.
        """
        image = ParserWithPillow.render_file(filepath, **kwargs)
        image.save(savepath)

    @staticmethod
    def render_file(filepath: str, **kwargs) -> Image.Image:
        """
        Loads, parses and renders file from given path and returns its render as PIL.Image.Image.
        **kwargs will be passed to ParserWithPillow, check it out for available params.
        """
        parser = ParserWithPillow(filepath, **kwargs)
        parser.render()
        return parser.get_image()

    @staticmethod
    def render_all(
        layers: List[LayerSpec],
        *,
        dpi: int = 600,
        ignore_deprecated: bool = True,
        image_padding: int = 0,
    ) -> List[Image.Image]:
        with ProcessPoolExecutor() as executor:
            processes: List[Future] = []
            for layer in layers:
                future = executor.submit(
                    _render_layer,
                    layer,
                    dpi,
                    ignore_deprecated,
                    image_padding,
                )
                processes.append(future)
            results: List[Image.Image] = []
            for future in processes:
                rendered_image: Image.Image = future.result()
                results.append(rendered_image)
        return results

    @staticmethod
    def join_layers(layers: List[Image.Image]) -> Image.Image:
        pass


def _render_layer(
    layer: LayerSpec, dpi: int, ignore_deprecated: bool, image_padding: int
) -> Image.Image:
    return ParserWithPillow.render_file(
        layer.filepath,
        dpi=dpi,
        colors=layer.colors,
        ignore_deprecated=ignore_deprecated,
        image_padding=image_padding,
    )
