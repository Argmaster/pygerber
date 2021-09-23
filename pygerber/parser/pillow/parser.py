# -*- coding: utf-8 -*-
from __future__ import annotations
from dataclasses import dataclass

from typing import Tuple

from PIL import Image, ImageDraw
from pygerber.mathclasses import BoundingBox
from pygerber.renderer.apertureset import ApertureSet
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
    (0, 0, 0, 0),
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
        file_path: str = None,
        string_source: str = None,
        *,
        dpi: int = 600,
        colors: ColorSet = DEFAULT_COLOR_SET_GREEN,
        ignore_deprecated: bool = True,
        image_padding: int = 0,
    ) -> None:
        """
        If `file_path` is None, `string_source` will be used as source,
        otherwise file_path will be used to read and parse file, then
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
            ignore_deprecated=ignore_deprecated,
        )
        self.colors = colors
        self.dpmm = dpi / 25.4
        self.__tokenize(file_path, string_source)

    def __tokenize(self, file_path: str, string_source: str) -> None:
        if file_path is not None:
            self.tokenizer.tokenize_file(file_path)
        elif string_source is not None:
            self.tokenizer.tokenize(string_source)
        else:
            raise RuntimeError("file_path and source_string can't be both None.")

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

    def save(self, file_path: str, format: str = None) -> None:
        """
        Saves rendered image.
        `file_path` A filename (string), pathlib.Path object or file object.
        `format` Optional format override. If omitted, the format to use is determined
        from the filename extension. If a file object was used instead of a filename,
        this parameter should always be used.
        """
        if format is not None:
            self.get_image().save(file_path, format)
        else:
            self.get_image().save(file_path)
