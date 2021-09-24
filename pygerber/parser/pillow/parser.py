# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
from typing import Deque, Tuple

from PIL import Image, ImageDraw
from pygerber.mathclasses import BoundingBox
from pygerber.parser.parser import AbstractParser
from pygerber.parser.pillow.apertures import *
from pygerber.renderer.apertureset import ApertureSet
from pygerber.tokenizer import Tokenizer
from pygerber.tokens.token import Token

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


class ParserWithPillow(AbstractParser):

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
        *,
        ignore_deprecated: bool = True,
        dpi: int = 600,
        colors: ColorSet = DEFAULT_COLOR_SET_GREEN,
        image_padding: int = 0,
    ) -> None:
        super().__init__(ignore_deprecated=ignore_deprecated)
        self.image_padding = image_padding
        self.is_rendered = False
        self.colors = colors
        self.dpmm = float(dpi) / 25.4

    @property
    def canvas(self) -> Image.Image:
        return self.renderer.canvas

    def _pre_render(self, bbox: BoundingBox):
        self.__inject_canvas(bbox)
        self.renderer.colors = self.colors
        self.renderer.dpmm = self.dpmm

    def __inject_canvas(self, bbox: BoundingBox) -> None:
        width, height = self.__get_canvas_size(bbox)
        if width == 0 or height == 0:
            raise ImageSizeNullError("Image has null width or height.")
        self.renderer.canvas = Image.new(
            "RGBA", (width, height), self.colors.background
        )
        self.renderer.draw_canvas = ImageDraw.Draw(self.canvas)
        left_offset, bottom_offset = self.__get_drawing_offset(bbox)
        self.renderer.left_offset = left_offset
        self.renderer.bottom_offset = bottom_offset

    def __get_canvas_size(self, bbox: BoundingBox) -> Tuple[int, int]:
        return (
            self._to_pixel_value(bbox.width()) + self.image_padding * 2,
            self._to_pixel_value(bbox.height()) + self.image_padding * 2,
        )

    def __get_drawing_offset(self, bbox: BoundingBox) -> Tuple[int, int]:
        return (
            self._to_pixel_value(-bbox.left) + self.image_padding,
            self._to_pixel_value(-bbox.lower) + self.image_padding,
        )

    def _to_pixel_value(self, value: float) -> float:
        return int(value * self.dpmm)

    def _render(self, token_stack: Deque[Token]) -> None:
        if not self.is_rendered:
            self.renderer.render(token_stack)
            self.is_rendered = True
        else:
            raise RuntimeError("Attempt to render already rendered canvas.")

    def get_image(self) -> Image.Image:
        if self.is_rendered:
            return self.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        else:
            raise RuntimeError("Can't return canvas that was not rendered.")

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
