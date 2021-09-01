# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from PIL import Image, ImageDraw
from pygerber.mathclasses import BoundingBox
from pygerber.meta.apertureset import ApertureSet
from pygerber.parser.pillow.apertures import *
from pygerber.tokenizer import Tokenizer


@dataclass
class ColorSet:

    Color = Tuple[float, float, float, float]

    dark: Color
    clear: Color
    region: Color


DEFAULT_COLOR_SET_ORANGE = ColorSet(
    (209, 110, 44),
    (0, 0, 0, 0),
    (209, 110, 44),
)
DEFAULT_COLOR_SET_GREEN = ColorSet(
    (66, 166, 66, 255),
    (16, 66, 36, 255),
    (66, 166, 66, 255),
)


class ImageSizeNullError(IndexError):
    pass


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
        colors: ColorSet = DEFAULT_COLOR_SET_ORANGE,
        ignore_deprecated: bool = True,
    ) -> None:
        """
        If filepath is None, string_source will be used as source,
        otherwise filepath will be used to read and parse file, then
        string_source will be complitely ignored. Passing None to both
        will result in RuntimeError.
        """
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
        self.tokenizer.meta.canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
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
        return self._prepare_co(bbox.width()), self._prepare_co(bbox.height())

    def __get_drawing_offset(self, bbox: BoundingBox) -> Tuple[int, int]:
        return self._prepare_co(-bbox.left), self._prepare_co(-bbox.lower)

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
        if format is not None:
            self.canvas.save(filepath, format)
        else:
            self.canvas.save(filepath)


def render_file_and_save(filepath: str, savepath: str, **kwargs):
    image = render_file(filepath, **kwargs)
    image.save(savepath)


def render_file(filepath: str, **kwargs) -> Image.Image:
    parser = ParserWithPillow(filepath, **kwargs)
    parser.render()
    return parser.get_image()
