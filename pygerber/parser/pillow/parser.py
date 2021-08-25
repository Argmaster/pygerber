# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
from pygerber.parser.pillow.apertures import *
from typing import Generator, Tuple

from PIL import Image, ImageDraw
from pygerber.meta.apertureset import ApertureSet
from pygerber.tokenizer import Tokenizer


@dataclass
class ColorSet:

    Color = Tuple[float, float, float, float]

    dark: Color
    clear: Color
    region: Color


DEFAULT_COLOR_SET = ColorSet((255, 255, 255, 255), (0, 0, 0, 0), (255, 255, 255, 255))


class ParserWithPillow:

    tokenizer: Tokenizer
    apertureSet = ApertureSet(
        PillowCircle,
        PillowRectangle,
        PillowObround,
        PillowPolygon,
        PillowCustom,
        PillowRegion
    )

    def __init__(
        self,
        filepath: str = None,
        string_source: str = None,
        *,
        dpi: int = 600,
        colors: ColorSet = DEFAULT_COLOR_SET,
        ignore_deprecated: bool = True,
    ) -> None:
        """
        If filepath is None, string_source will be used as source,
        otherwise filepath will be used to read and parse file, then
        string_source will be complitely ignored. Passing None to both
        will result in RuntimeError.
        """
        self.tokenizer = Tokenizer(
            self.apertureSet,
            ignore_deprecated=ignore_deprecated,
        )
        self.tokenizer.meta.colors = colors
        self.tokenizer.meta.dpmm = dpi / 25.4
        self._tokenize(filepath, string_source)

    def _tokenize(self, filepath: str, string_source: str) -> None:
        if filepath is not None:
            self.tokenizer.tokenize_file(filepath)
        elif string_source is not None:
            self.tokenizer.tokenize_string(string_source)
        else:
            raise RuntimeError("filepath and source_string can't be both None.")

    @property
    def canvas(self) -> Image.Image:
        return self.tokenizer.meta.canvas

    def render(self):
        self.tokenizer.meta.canvas = self.make_canvas()
        self.tokenizer.meta.draw_canvas = ImageDraw.Draw(self.tokenizer.canvas)
        return self.tokenizer.render()

    def make_canvas(self) -> Image.Image:
        bbox = self.tokenizer.get_bbox()
        width = bbox.width() * self.dpi
        height = bbox.height() * self.dpi
        return Image.new("RGBA", (width, height), (0, 0, 0, 0))

    def render_generator(self, yield_after: int = 10) -> Generator[int]:
        return self.tokenizer.render_generator(yield_after)

    def save(self, filepath: str, format: str) -> None:
        self.canvas.save(filepath, format)
